import warnings

import torch
from sklearn.metrics import balanced_accuracy_score, jaccard_score


class BatchAccumulator:
    """
    Accumulates 'y's and 'y_p's in torch.Tensors()
    Was designed to basically keep track of classification predictions for use with
        callbacks like BinaryScore or AccuracyScorerCallback.

    Parameters
    ----------
    acc_training: boolean
        Whether to accumulate the training or validation batches
    batch_dim:
        What dimension is the batch on, so we can concatenate along that one.
    """

    def __init__(self, acc_training=False, batch_dim=0):
        self.reset()
        self.acc_training = acc_training
        self.batch_dim = batch_dim

        # if we are distributed
        self.is_dist = torch.distributed.is_initialized()
        self.rank = 0 if not self.is_dist else torch.distributed.get_rank()

    def begin_validate(self, trainer):
        self.reset()

    def begin_eval(self, trainer):
        self.reset()

    def reset(self):
        self.all_y = torch.Tensor()
        self.all_y_p = torch.Tensor()

    def after_batch(self, trainer):
        if trainer.model.training is self.acc_training:
            if hasattr(trainer, 'y') and trainer.y is not None:
                y = self.gather(trainer.y)
                if self.rank == 0:  # We only gather on 0
                    y = y.cpu().detach()
                    self.all_y = torch.cat((self.all_y.type(y.type()), y), dim=0)

            y_p = self.gather(trainer.y_p, self.batch_dim)
            if self.rank == 0:  # We only gather on 0
                y_p = y_p.cpu().detach()
                self.all_y_p = torch.cat((self.all_y_p.type(y_p.type()), y_p), dim=self.batch_dim)

    def gather(self, tensor, dim=0):
        """If we are doing distributed training we need to gather the results to
        one device.
        """
        if not self.is_dist:
            return tensor
        world_size = torch.distributed.get_world_size()
        if self.rank == 0:
            gather_list = [tensor.new_zeros(tensor.size()) for _ in range(world_size)]
        else:
            gather_list = None
        torch.distributed.gather(tensor, gather_list)
        if self.rank == 0:
            return torch.cat(gather_list, dim=dim)
        return None


class MetricScoreCallback(BatchAccumulator):
    """Given a metric_func will compute the metric and save it as a score.

    Parameters
    ----------
    acc_training: boolean
        Whether to accumulate the training or validation batches
    max_matches: int
        If you only want to accumulate a number of batched rather than the whole
        epoch
    """

    def __init__(self, metric_func, acc_training=False, batch_dim=0, max_batches=-1):
        super().__init__(acc_training, batch_dim)
        self.metric_func = metric_func
        self.max_batches = max_batches
        self.cur_batch = 0

    def all_batches(self, trainer):
        self.cur_batch = 0

    def after_batch(self, trainer):
        super().after_batch(trainer)

        if self.rank != 0:
            return
        if self.max_batches != -1:
            self.cur_batch += 1
            if self.max_batches % self.cur_batch == 0:
                trainer.score = self.get_scores()
                self.reset()

    def after_epoch(self, trainer):
        if self.rank != 0:
            return
        trainer.score = self.get_scores()

    def get_scores(self):
        if self.all_y_p.dim() == 2:
            y_p = self.all_y_p.float().topk(1)[1].squeeze(1)
        elif self.all_y_p.dtype == torch.float16:  # Round isn't supported for float16s for some reason.
            y_p = torch.round(self.all_y_p.to(torch.float32)).to(torch.float16)
        else:
            y_p = torch.round(self.all_y_p)

        if self.all_y.dim() == 2:
            y = self.all_y.topk(1)[1].squeeze(1)
        else:
            y = self.all_y

        return self.metric_func(y, y_p)

    def get_preds(self):
        y_p = self.all_y_p.float().topk(1)[1].squeeze(1)
        return self.all_y, y_p


class AccuracyScorerCallback(MetricScoreCallback):
    """
    Keeps track of 'y's and 'y_p's to then calculate an accuracy score for
    Since this adds trainer.score, should be before other callbacks that might depend on it.
    """

    def __init__(self):
        super().__init__(balanced_accuracy_score)
        warnings.warn(
            'AccuracyScorerCallback is deprecated in favor of using MetricScoreCallback(sklearn.metric.balanced_accuracy_score)',
            DeprecationWarning,
        )


class BinaryScore(BatchAccumulator):
    """Calculates accuracy score of binary predictions by applying a sigmoid and > threshold."""

    def __init__(self, threshold):
        self.thresh = threshold
        super().__init__(False)

    def after_epoch(self, trainer):
        trainer.score = self.get_scores()

    def get_scores(self):
        y_p = torch.sigmoid(self.all_y_p) > self.thresh
        return jaccard_score(self.all_y.long(), y_p.long(), average='macro')

    def get_preds(self):
        y_p = torch.sigmoid(self.all_y_p)
        return self.all_y, y_p
