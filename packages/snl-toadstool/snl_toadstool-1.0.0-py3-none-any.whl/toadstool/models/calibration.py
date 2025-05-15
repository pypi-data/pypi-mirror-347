"""Code to help calibrate or measure Calibration Error of models."""

import itertools

import matplotlib.pyplot as plt
import torch

from toadstool.utils import filter_instance


class TemperatureScalingCallback:
    """Used to calculate temperature scaling value after model fit.

    `after_fit` will utilize the `Trainer`'s `eval` `_stage_name` to run
    a custom `temp_scale` stage to accumulate labels and predictions to then
    run the Temperature Scaling loss function against to calculate the temperature value.

    See: https://arxiv.org/pdf/1706.04599.pdf
    """

    def __init__(self):
        self.y = torch.Tensor()
        self.y_p = torch.Tensor()
        self.temperature = torch.nn.Parameter(torch.ones(1))

    def begin_temp_scale(self, trainer):
        self.y = torch.Tensor()
        self.y_p = torch.Tensor()
        self.after_batch = self.acc

    def after_temp_scale(self, trainer):
        del self.after_batch

    def acc(self, trainer):
        """Accumulate the labels and predictions. Gets placed as `after_batch` by
        `begin_temp_scale` and remove by `after_temp_scale` so we aren't accumulating
        when we don't need to.
        """
        y = trainer.y.cpu().detach()
        y_p = trainer.y_p.cpu().detach()
        self.y = torch.cat((self.y.type(y.type()), y), dim=0)
        self.y_p = torch.cat((self.y_p.type(y_p.type()), y_p), dim=0)

    def after_fit(self, trainer):
        assert trainer.eval_loader is not None
        trainer.eval(trainer.eval_loader, _stage_name='temp_scale')

        optimizer = torch.optim.LBFGS([self.temperature], lr=0.01, max_iter=20000)

        def closure():
            optimizer.zero_grad()
            scaled = self.y_p / self.temperature
            loss = torch.nn.functional.cross_entropy(scaled, self.y)
            loss.backward()
            return loss

        optimizer.step(closure)


def temp_scale(y, y_p, lr=0.01, max_iter=20000):
    """Calculate the temperature value."""
    if y.ndim == 2:
        y = y.max(1)[1]

    temperature = torch.nn.Parameter(torch.ones(1))
    loss_fn = torch.nn.functional.cross_entropy

    optimizer = torch.optim.LBFGS([temperature], lr=lr, max_iter=max_iter)

    def closure():
        optimizer.zero_grad()
        scaled = y_p / temperature
        loss = loss_fn(scaled, y)
        loss.backward()
        return loss

    optimizer.step(closure)
    return temperature.detach()


class TemperatureWrapper(torch.nn.Module):
    """Scale a models output based on the temperature.
    Assumes all the model's return value needs to be scaled.

    See: TemperatureScalingCallback
    """

    def __init__(self, model, temp):
        super().__init__()
        self.model = model
        self.temp = temp

    def forward(self, x):
        y_p = self.model(x)
        return y_p / self.temp


def calibration_test(trainer, loader):
    """Setup a CalibrationReportCallback and run the loader data through the model."""
    if len(list(filter_instance(CalibrationReportCallback, trainer.cbs))) == 0:
        trainer.cbs += [CalibrationReportCallback()]
    reporter = next(filter_instance(CalibrationReportCallback, trainer.cbs))
    trainer.eval(loader, _stage_name='calib_test')
    reporter.mce, reporter.ece, reporter.rd = calibration_report(reporter.y, reporter.y_p)
    print(f'MCE: {reporter.mce}, ECE: {reporter.ece}')
    reporter.reliability_plot()
    return reporter


class CalibrationReportCallback:
    """Similar to how TemperatureScalingCallback works, run an evaluation pass `after_fit`
    to measure the calibration error of the model.

    Calculates the Expected Calibration Error, Maximum Calibration Error, and stores the
    results necessary to create Reliability Plots
    """

    def __init__(self, n_bins=10):
        self.n_bins = n_bins

    def begin_calib_test(self, trainer):
        self.y = torch.Tensor()
        self.y_p = torch.Tensor()
        self.after_batch = self.accumulate

    def after_calib_test(self, trainer):
        del self.after_batch
        self.mce, self.ece, self.rd = calibration_report(self.y, self.y_p, n_bins=self.n_bins)
        print(f'MCE: {self.mce}, ECE: {self.ece}')

    def accumulate(self, trainer):
        y = trainer.y.cpu().detach()
        y_p = trainer.y_p.cpu().detach()
        self.y = torch.cat((self.y.type(y.type()), y), dim=0)
        self.y_p = torch.cat((self.y_p.type(y_p.type()), y_p), dim=0)

    def after_fit(self, trainer):
        assert trainer.eval_loader is not None
        trainer.eval(trainer.eval_loader, _stage_name='calib_test')

    def reliability_plot(self):
        reliability_plot(self.rd)


def calibration_report(y, y_p, filtr_idx=None, n_bins=10):
    """
    Calculate the Maximum Calibration Error (MCE), Expected Calibration Error (ECE), and the points for a Reliability Diagram (RD).

    Parameters
    ----------
    y: torch.LongTensor
        Tensor of labels
    y_p: torch.FloatTensor
        Logits of model predictions
    filter_idx: int
        Filter the y_p predictions to only those predicted to be filter_idx label to get calibration for just that value (Default: None)
    n_bins: int
        Number of bins to group into, e.g., % granularity (Default: 10)
    Return
    ------
    mce: float
        Maximum Calibration Error
    ece: float
        Expected (average) Calibration Error
    rd: torch.Tensor
        2d tensor of [# bins, calibration error]
    """
    bins = torch.linspace(0, 1, n_bins + 1)
    ece = torch.zeros(1)  # Expected calibration error
    mce = torch.zeros(1)  # Maximum calibration error
    rd = torch.zeros((len(bins) - 1, 2))  # For reliability plots
    bin_iter = list(itertools.pairwise(bins))  # to read them in bounds [1,2,3,4] -> [1,2], [2,3], etc.

    if y.ndim == 2:
        y = y.max(1)[1]
        probs = torch.sigmoid(y_p)
    else:
        probs = torch.nn.functional.softmax(y_p, dim=1)

    # If we just want to get one label's calibration
    if filtr_idx is not None:
        conf = probs[:, filtr_idx]
        preds = probs.max(1)[1].eq(filtr_idx)
        correct = y.eq(filtr_idx) & preds
    else:
        conf, preds = probs.max(1)
        correct = preds.eq(y)

    for i, (low, high) in enumerate(bin_iter):
        in_bin = conf.gt(low) & conf.le(high)
        perc_in_bin = in_bin.float().mean()
        rd[i, 0] = (low + high) / 2
        if perc_in_bin > 0:
            accuracy = correct[in_bin].float().mean()
            avg_conf = conf[in_bin].mean()

            rd[i, 1] = accuracy
            ce = torch.abs(accuracy - avg_conf)  # calibration error
            mce = max(mce, ce)
            ece += ce * perc_in_bin

    return mce, ece, rd


def reliability_plot(rd, filename=None):
    """Plot reliability plot from calibration_report."""
    plt.plot(rd[:, 0], rd[:, 1])
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.title('Reliability Plot')
    plt.xlabel('Predicted probability')
    plt.ylabel('Actual probability')
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
