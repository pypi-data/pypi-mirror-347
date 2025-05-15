import logging
import os
import re
import shutil
import tempfile
import warnings
from pathlib import Path

import numpy as np
import torch

from toadstool.models.dl_utils import CancelTrainException
from toadstool.utils import filter_instance

log = logging.getLogger(__name__)


class EarlyStopping:
    """
    Record best evaluation performance and stops training if it doesn't improve in `patience` # of epochs
    expects higher score to be better
    Checks if trainer.score is set otherwise uses -loss.

    Tries to detect if running in distributed environment and handle that
    Note
    ----
    Saves a temporary file using mkstemp
    """

    def __init__(self, patience, checkpoint_dir=None, every=-1, resume=True):
        """
        Parameters
        ----------
        patience: int
            How many epochs to wait for performance improvement before canceling training
        checkpoint_dir: Path | None
            If we should save a `checkpoint_latest.pth` and `checkpoint_best.pth` for reloading
                training.
        """
        # Check if we are running in distributed mode
        self.dist, self.rank = False, 0
        if torch.distributed.is_initialized():
            self.dist, self.rank = True, torch.distributed.get_rank()

        self.patience = patience
        self.checkpoint = False
        self.epoch_offset = 0

        self.every = every
        self.resume = resume
        if checkpoint_dir is not None:
            self.checkpoint = True
            self.checkdir = Path(checkpoint_dir)
            self.save_name = self.checkdir / 'checkpoint_best.pth'
            self.latest_name = self.checkdir / 'checkpoint_latest.pth'
            if self.rank == 0:
                self.checkdir.mkdir(parents=True, exist_ok=True)
        else:
            if self.dist:
                log.error(
                    'EarlyStopping running in distributed without a canonical save location'
                    'Model state will be unable to be automatically loaded'
                )
            if self.rank == 0:
                fd, self.save_name = tempfile.mkstemp(prefix='EarlyStopping')
                self.save_name = Path(self.save_name)
                os.close(fd)
        self.total_loss = 0

    def begin_fit(self, trainer):
        self.impatient = 0
        self.highscore = -np.inf
        self.bestloss = np.inf
        self.load_best = False
        # Reload latest checkpoint
        if self.resume and self.checkpoint and self.latest_name.exists():
            self.load(trainer, self.latest_name)

    def begin_validate(self, trainer):
        self.total_loss = 0

    def after_loss(self, trainer):
        if not trainer.model.training:
            self.total_loss += trainer.loss.cpu().detach().item()

    def begin_epoch(self, trainer):
        trainer.epoch += self.epoch_offset

    def after_epoch(self, trainer):
        curscore = trainer.loss.new_tensor(getattr(trainer, 'score', -np.inf))
        curloss = trainer.loss.new_tensor([self.total_loss])

        # Synchronize metrics so all processes behave same
        if self.dist:
            torch.distributed.all_reduce(curloss, op=torch.distributed.ReduceOp.SUM)
            torch.distributed.broadcast(
                curscore, 0
            )  # MetricScoreCallback only accumulates thing for the score on rank 0
        curloss = curloss.cpu().item()
        curscore = curscore.item()

        # Check best performing
        if curscore > self.highscore or (curscore == self.highscore and curloss < self.bestloss):
            self.impatient = 0
            self.highscore = curscore
            self.bestloss = curloss if curloss < self.bestloss else self.bestloss
            self.save_best(trainer)
        else:
            self.impatient += 1
            self.save_latest(trainer)
            # optionally save a specific checkpoint for the epoch
            if self.rank == 0 and self.checkpoint and self.every != -1:  # noqa SIM102: conceptually different ifs
                if (trainer.epoch % self.every) == 0:
                    shutil.copyfile(self.latest_name, self.checkdir / f'checkpoint_{trainer.epoch}.pth')

        if self.impatient > self.patience:
            raise CancelTrainException()

    def after_fit(self, trainer):
        self.load(trainer, self.save_name)

    def save_best(self, trainer):
        self.load_best = True
        self.save(trainer, self.save_name)
        if self.checkpoint and self.rank == 0:
            shutil.copyfile(self.save_name, self.latest_name)

    def save_latest(self, trainer):
        if self.checkpoint:
            self.save(trainer, self.latest_name)

    def save(self, trainer, fn):
        meta = {}
        meta['highscore'] = self.highscore
        meta['bestloss'] = self.bestloss
        meta['epoch'] = trainer.epoch
        trainer.checkpoint(fn, meta)

    def load(self, trainer, fn):
        # If I should reload and if I'm main process
        try:
            meta = trainer.load_checkpoint(fn)
            self.highscore = meta['highscore']
            self.bestloss = meta['bestloss']
            self.epoch_offset = meta['epoch'] + 1
        except (FileNotFoundError, NotImplementedError, EOFError) as e:
            # may not because we don't distinguish if the last epoch was best
            log.error(f"Can't reload model from {fn}.\n{e}")

    def __del__(self):
        if not self.checkpoint and self.rank == 0 and self.save_name.exists():
            self.save_name.unlink()


class CheckpointCallback:
    """Periodically save the Trainer
    Does not measure the most performant checkpoint.

    Warning:
        When EarlyStopping and CheckpointCallback are used together,
            whichever is last in the trainer callbacks will overwrite/overload the other.
        This **shouldn't** be a problem. It's a bit redundant and wasteful
        If they are saving to the same directory then they will step on each other's toes with the naming
        If you are expecting EarlyStopping's 'checkpoint_latest.pth' to be the latest of all the checkpoints that isn't the case when CheckpointCallback is saving on steps.
    """

    def __init__(self, outdir, on_step=False, every=1, resume=False):
        """
        Parameters
        ----------
        outdir: PathLike
        on_step: bool
            Whether to save on step or epochs
        every: int
            mods the epoch or step (based on `on_step`) to know when to save
        resume: bool
            Whether to load the latest checkpoint on .begin_fit
        """
        self.outdir = Path(outdir)
        self.on_step = on_step
        self.every = every
        self.outdir.mkdir(parents=True, exist_ok=True)
        self.resume = resume
        self.resume_epoch = 0

    def begin_fit(self, trainer):
        try:
            next(filter_instance(EarlyStopping, trainer.cbs))
            log.warning(
                'When EarlyStopping and CheckpointCallback are used together,'
                'whichever is last in the trainer callbacks will overwrite/overload the other.'
                "This **shouldn't** be a problem. It's a bit redundant and wasteful"
                "If they are saving to the same directory then they will step on each other's toes with the naming"
                "If you are expecting EarlyStopping's 'checkpoint_latest.pth' to be the latest of all the checkpoints that isn't the case when CheckpointCallback is saving on steps."
            )
        except StopIteration:
            pass

        if self.resume:
            self.load_latest_checkpoint(trainer)
        self.step = 0
        if self.on_step:
            if self.every < trainer.acc_grads:
                self.every = trainer.acc_grads
                warnings.warn(f'Checkpointing on non-updating steps: Adjusting every to match={self.every}.')
                return
            mod = self.every % trainer.acc_grads
            if mod != 0:
                self.every = trainer.acc_grads * (self.every // trainer.acc_grads)
                warnings.warn(f'Checkpointing on non-updating steps: Adjusting every to match={self.every}.')

    def begin_epoch(self, trainer):
        trainer.epoch += self.resume_epoch

    def after_batch(self, trainer):
        if self.on_step:
            self.step += 1
            if (self.step % self.every) == 0:
                self.checkpoint(trainer, self.step)

    def after_epoch(self, trainer):
        if not self.on_step and (trainer.epoch % self.every) == 0:
            self.checkpoint(trainer, trainer.epoch)

    def checkpoint(self, trainer, num):
        meta = {'epoch': trainer.epoch}
        trainer.checkpoint(self.outdir / f'checkpoint_{num}.pth', meta=meta)

    def load_latest_checkpoint(self, trainer):
        num_chkpt = re.compile(r'checkpoint_\d+.pth')
        files = os.listdir(self.outdir)
        checkpoints = [x for x in files if num_chkpt.match(x)]
        if len(checkpoints) == 0:
            warnings.warn('No checkpoints to load from')
            return
        # sort based on the # in `checkpoint_#.pth`
        latest = sorted(checkpoints, key=lambda fn: int(fn.split('.pth')[0].split('_')[1]))[-1]
        meta = trainer.load_checkpoint(self.outdir / latest)
        self.resume_epoch = meta['epoch'] + 1
