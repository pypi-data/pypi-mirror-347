# eventimpact/plot.py

import matplotlib.pyplot as plt

def plot_impact(
    time,
    values,
    summary: dict,
    event_start: float,
    event_end: float,
    pred_mean: list = None,
    ci_lower: list = None,
    ci_upper: list = None
):
    """
    Plot observed data, optional fit & credible band, and shade the event window.

    Parameters
    ----------
    time : array-like
    values : array-like
    summary : dict
        The output of EventImpactAnalyzer.summary(). Used for title annotation.
    event_start : float
        Start of event window.
    event_end : float
        End of event window.
    pred_mean : array-like or None
        Posterior predictive mean (optional).
    ci_lower, ci_upper : array-like or None
        95% credible band bounds (optional).
    """
    fig, ax = plt.subplots()
    ax.plot(time, values, marker="o", linestyle="-", label="Observed")

    if pred_mean is not None and ci_lower is not None and ci_upper is not None:
        ax.plot(time, pred_mean, label="Fit mean")
        ax.fill_between(time, ci_lower, ci_upper, alpha=0.3, label="95% CI")

    # Shade event window
    ax.axvspan(event_start, event_end, alpha=0.2, color="orange",
               label="Event window")

    ax.set_xlabel("Time")
    ax.set_ylabel("Metric")
    title = "Event Impact Analysis"
    title += f": jump={summary['immediate']['mean']:.2f}"
    title += f", slope={summary['slope']['mean']:.2f}"
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.show()