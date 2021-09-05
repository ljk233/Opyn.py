
"""
`opynuni.stats.probmodels`

TODO: Add module sting
"""


from __future__ import annotations
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import rv_discrete, rv_continuous


def _is_cts(obj) -> None:
    assert getattr(obj, "pdf", False), "Not a continuous distribution."


def _is_discrete(obj) -> bool:
    assert getattr(obj, "pmf", False), "Not a discete distribution."


def get_cts_points(model: rv_continuous) -> tuple:
    """
    Generates the points that can be used for visualisations of some
    continuous probability model.

    Args:
        dist (rv_continuous): A continuous **SciPy** distribution

    Raises:
        AssertionError: if arg dist is not of type `rv_continuous`

    Returns:
        `x`, `pdf`:
            tuple of `np.arrays` that can used for plotting
    """

    # type checking: is model continuous from scipy?
    _is_cts(model)
    rng = np.linspace(model.ppf(0.01), model.ppf(0.99), num=100)
    prob_function = model.pdf(rng)
    return rng, prob_function


def plot_cts(model: rv_continuous) -> None:
    """
    Plots the probability function of some probability model as a
    lineplot.

    Args:
        model: a continuous **SciPy** distribution

    Raises:
        AssertionError: if arg dist is not of type `rv_continuous`
    """
    pts = get_cts_points(model)
    f, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(x=pts[0], y=pts[1], lw=2, color="r")
    ax.set(xlabel="X", ylabel="Pr")
    plt.show()


def get_discrete_points(model: rv_discrete) -> tuple:
    """
    Generates the points that can be used for visualisations of some
    discrete probability model.

    Args:
        model: a discrete  **SciPy** distribution

    Raises:
        AssertionError: if arg dist is not of type `rv_discrete`

    Returns:
        `x`, `pmf`:
            tuple of `np.arrays` that can used for plotting
    """
    # type checking: is model discrete from scipy?
    _is_discrete(model)
    rng = np.arange(
        model.ppf(0.01), model.ppf(0.99)+1, dtype="int32")
    prob_function = model.pmf(rng)
    return rng, prob_function


def plot_discrete(model: rv_discrete) -> None:
    """
    Plots the probability function of some probability model as a
    barplot.

    Args:
        model: a discrete **SciPy** distribution
    """
    pts = get_discrete_points(model)
    f, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=pts[0], y=pts[1], color="cornflowerblue")
    ax.set(xlabel="X", ylabel="Pr")
    plt.show()
