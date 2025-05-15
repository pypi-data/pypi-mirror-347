class ClassifierCallback:
    """Helper callback for TransformerModel during classification to squeeze out the sequence dimension (because its 1)."""

    def __init__(self, pos=0):
        self.cls_pos = pos

    def after_pred(self, trainer):
        trainer.y_p = trainer.y_p[:, self.cls_pos, :]
