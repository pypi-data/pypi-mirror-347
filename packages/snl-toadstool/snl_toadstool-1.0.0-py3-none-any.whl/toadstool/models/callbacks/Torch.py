class SamplerCallback:
    """Calls the sampler `set_epoch` on every epoch."""

    def __init__(self, sampler):
        self.sampler = sampler

    def begin_epoch(self, t):
        self.sampler.set_epoch(t.epoch)
