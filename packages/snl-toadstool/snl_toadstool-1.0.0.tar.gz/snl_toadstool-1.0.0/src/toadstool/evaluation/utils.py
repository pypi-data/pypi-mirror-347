"""Helper functions for evaluating models."""

import matplotlib.pyplot as plt
import numpy as np
import scipy
from sklearn.metrics import (
    auc,
    average_precision_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    roc_curve,
)
from sklearn.utils import resample


def conv_bool(x):
    """Convert a bool to a string."""
    if isinstance(x, bool | np.bool_):
        return 'True' if x else 'False'
    return x


""" Remember these assume that y is the probability of the pos_label """


def plot_roc_curve(y, y_p, pos_label=1, pos_label_info='', filename=None):
    """Plot a ROC curve."""
    fpr, tpr, thresh = roc_curve(y, y_p, pos_label=pos_label)
    area = auc(fpr, tpr)

    label = f'AUC = {area:0.2f}'
    info_pos_label = f' (Positive label: {pos_label_info})'
    xlabel = f'False Positive Rate {info_pos_label}'
    ylabel = f'True Positive Rate {info_pos_label}'

    plot_curve(fpr, tpr, xlabel, ylabel, label)

    return fpr, tpr, thresh


def plot_pr_curve(y, y_p, pos_label=1, pos_label_info='', filename=None):
    """Plot a Precision Recall curve."""
    avg = average_precision_score(y, y_p, pos_label=pos_label)
    precision, recall, thresh = precision_recall_curve(y, y_p, pos_label=pos_label)

    label = f'AP = {avg:0.2f}'
    info_pos_label = f'(Positive label: {pos_label_info})'
    xlabel = f'Recall {info_pos_label}'
    ylabel = f'Precision {info_pos_label}'

    plot_curve(recall, precision, xlabel, ylabel, label)

    return precision, recall, thresh


def plot_curve(x, y, xlabel, ylabel, linelabel, filename=None):
    """Generic plot code."""
    _, ax = plt.subplots()
    ax.plot(x, y, label=linelabel)
    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.legend(loc='lower right')
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)


def print_classification(y, y_hat, classes):
    """Do sklearn's classification report."""
    classes = list(map(conv_bool, classes))
    classes = [str(x) for x in classes]
    print(classification_report(y, y_hat, labels=range(len(classes)), target_names=classes))


def plot_confusion(y, y_hat, classes, filename=None):
    """Create a confusion matrix and either show or save to filename."""
    classes = list(map(conv_bool, classes))
    c_mat = confusion_matrix(y, y_hat, labels=range(len(classes)))

    c_mat_norm = c_mat.astype('float') / c_mat.sum(axis=1)[:, np.newaxis]
    c_mat_norm = np.nan_to_num(c_mat_norm)
    plt.figure(figsize=(20, 10))
    plt.matshow(c_mat_norm, fignum=0, vmin=0, vmax=1)
    # plt.title('Confusion matrix')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.xticks(np.arange(len(classes)), labels=classes, rotation=90)
    plt.yticks(np.arange(len(classes)), labels=classes)
    plt.colorbar()
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
    print('Class Average Accuracy:', balanced_accuracy_score(y, y_hat))
    return c_mat, c_mat_norm


def permutation_test(first, second, scorer, repeat=10000, bootstrap=False, plot=False):
    """
    Parameters
    ----------
    first: distribution
    second: distribution
    scorer: function that takes in the resampling of first and second and computes whatever metric value is of interest
    plot: bool
        If you want a plot of the histogram and the actual difference line.
        If the line is lower then it means the second is higher than the first and if its to the right its lower.

    Returns
    -------
    dist: distribution of calculated resampling `scorer` statistics
    x: the average time the difference between the resampled distributions was greater than the actual difference of scorer(first) - scorer(second)
        i.e. p-value of how different the distributions are
    """
    dist = []
    pool = np.concatenate((first, second))
    for _ in range(repeat):
        shuffle = resample(pool)
        f_p = resample(shuffle[: len(first)], replace=bootstrap)
        s_p = resample(shuffle[len(first) :], replace=bootstrap)
        dist.append(scorer(f_p) - scorer(s_p))
    actual_diff = scorer(first) - scorer(second)
    if plot:
        plt.hist(dist)
        plt.axvline(actual_diff)
        print(actual_diff)
    return dist, np.mean(dist > actual_diff)


def power_test(first, second, scorer, sample_size, significance=0.05, iters=1000):
    power = 0
    for _ in range(iters):
        _, x = permutation_test(
            resample(first, n_samples=sample_size, replace=True),
            resample(second, n_samples=sample_size, replace=True),
            scorer,
            repeat=1000,
        )
        if x < significance:
            power += 1
    return power / iters


def plot_attention(seq, vocab, attention, filename=None):
    """To plot attention weights."""
    fig = plt.figure(figsize=(100, 10))
    plt.plot(attention.flatten().np()[: len(seq)], figure=fig)
    plt.xticks(range(len(seq)), labels=[vocab[x] for x in seq], rotation=45)
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)


def heuristic_eval(get_eval_data, label, hlabel):
    """Old code to compare heuristic results."""
    print(label)
    data, dataset = get_eval_data(label)
    data_test = dataset.data.iloc[data.test.indices]

    def to_valid_numericalized_label(x):
        if x in dataset.labels:
            return dataset.labels.get_loc(x)
        if x == 'True' and True in dataset.labels:
            return dataset.labels.get_loc(True)
        if x == 'False' and False in dataset.labels:
            return dataset.labels.get_loc(False)
        return -1

    y = data.test[:][1].values
    y_p = data_test[hlabel].apply(to_valid_numericalized_label).values
    print(y.shape, y_p.shape)
    print_classification(y, y_p, dataset.labels)
    plot_confusion(y, y_p, dataset.labels)


def threshold_score(score, metric):
    """
    score: np.array
        array of score values for each instance that could be thresholded
    metric: np.array
        array of evaluation metrics for each score.
    """
    nan = np.isnan(score) | np.isnan(metric)
    score, metric = score[~nan], metric[~nan]
    print(len(score))
    # Sort the score and values
    ## -score so we can have it descending for calculating the average metric based on thresholds
    sort_indices = np.argsort(-score)
    sorted_score, sorted_metric = score[sort_indices], metric[sort_indices]

    # Find unique thresholds and grab those positions
    threshold_idxs = np.where(np.diff(sorted_score))[0]
    thresh_score = sorted_score[threshold_idxs]

    # Average the previous instances metric up to this point
    cumulative_metric = np.cumsum(sorted_metric)
    average_metric = cumulative_metric / (np.arange(len(cumulative_metric)) + 1)

    # Plot threshold to average metric
    plt.plot(thresh_score, average_metric[threshold_idxs])
    plt.title('Threshold to Average Metric Value')
    plt.xlabel('Score')
    plt.ylabel('Metric')
    plt.show()

    # Plot a smoothed metric
    thresh_score, thresh_metric = np.flip(thresh_score), np.flip(average_metric[threshold_idxs])
    smoothed_metric = scipy.interpolate.UnivariateSpline(thresh_score, thresh_metric, s=0.1)(thresh_score)

    elbow = np.diff(np.gradient(smoothed_metric, thresh_score)).argmin() + 1

    plt.plot(thresh_score, smoothed_metric)
    plt.plot(thresh_score[elbow], smoothed_metric[elbow], markersize=5, marker='o', color='red')
    plt.title('Smoothed with highest gradient difference')
    plt.xlabel('Score')
    plt.ylabel('Metric')
    plt.show()

    # Plot a coverage to metric
    coverage = []
    for s in thresh_score:
        coverage.append((score >= s).sum() / len(thresh_score))
    plt.plot(thresh_score, coverage)
    plt.plot(thresh_score[elbow], coverage[elbow], markersize=5, marker='o', color='red')
    plt.title('Coverage')
    plt.xlabel('Metric')
    plt.ylabel('Coverage')
    plt.show()
    print(
        f'Suggested Threshold: {thresh_score[elbow]}, Expected Metric: {smoothed_metric[elbow]}, Expected Coverage: {coverage[elbow]}'
    )
    return thresh_score[elbow]


def threshold_coverage(score, gt=True, thresh=None):
    """
    score: np.array
        array of score values for each instance that could be thresholded.
    """
    # Sort the score and values
    ## -score so we can have it descending for calculating the average metric based on thresholds
    score_indices = np.argsort(-score)
    sorted_score = score[score_indices]

    # Find unique thresholds and grab those positions
    thresholds = np.where(np.diff(sorted_score))[0]
    thresh_score = np.flip(sorted_score[thresholds])

    # Plot a coverage to metric
    coverage = []
    for s in thresh_score:
        if gt:
            coverage.append((score >= s).sum() / len(score))
        else:
            coverage.append((score <= s).sum() / len(score))
    plt.plot(thresh_score, coverage)
    if thresh is not None:
        plt.plot(thresh, np.interp(thresh, thresh_score, coverage), markersize=5, marker='o', color='red')
    plt.ylabel('Coverage')
    plt.xlabel('Score')
    plt.show()
