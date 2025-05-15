import warnings


class CudaCallback:
    """Moves all `x` and `y` values to given GPU."""

    def __init__(self, device, mov_y=True):
        self.device = device
        self.mov_y = mov_y

    def begin_fit(self, trainer):
        pass
        # https://pytorch.org/docs/stable/optim.html
        # The optimizer expects the model is already at the correct location,
        #     (i.e. they had to do it before they created the Trainer)
        #     therefore so do we
        # trainer.model = trainer.model.to(self.device)

    def begin_batch(self, trainer):
        def mov_to_dev(x):
            if hasattr(x, 'to'):
                return x.to(self.device)
            if isinstance(x, list | tuple):
                return [mov_to_dev(xp) for xp in x]
            if isinstance(x, dict):
                mov = {}
                for k in x:
                    mov[k] = mov_to_dev(x[k])
                return mov
            return x

        trainer.x = mov_to_dev(trainer.x)
        if self.mov_y and hasattr(trainer, 'y') and trainer.y is not None:
            trainer.y = mov_to_dev(trainer.y)

    def after_pred(self, trainer):
        if not self.mov_y:
            trainer.y_p = trainer.y_p.cpu()


class DeepSpeedCallback:
    """DeepSpeed handles the optimizer and training a little differently.
    This tries to monkey patch the correct handling.
    """

    def begin_fit(self, trainer):
        trainer.opt = trainer.model  # sanity check

    def after_loss(self, trainer):
        trainer.model.training = False  # prevent running backward and optimizer step

    def after_batch(self, trainer):
        if trainer.acc_grads != 1:
            warnings.warn('Accumulate gradients not supported like this with DeepSpeed')
        trainer.model.trainining = True
        trainer.model.backward(trainer.loss)
        trainer.model.step()
