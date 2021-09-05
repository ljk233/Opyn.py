
"""
"""


from __future__ import annotations
from typing import Tuple
from numpy.typing import ArrayLike
from scipy.stats import rv_discrete, rv_continuous
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def _is_cts(obj) -> None:
    assert getattr(obj, "pdf", False), "Not a continuous distribution."


def _is_discrete(obj) -> bool:
    assert getattr(obj, "pmf", False), "Not a discete distribution."


def get_cts_points(model: rv_continuous) -> Tuple[ArrayLike, ArrayLike]:
    """
    Generates the points that can be used for visualisations of some
    continuous probability model.

    Args:
        dist (rv_continuous): A continuous scipy distribution

    Returns:
        Tuple[ArrayLike, ArrayLike]: x, pdf
    """

    # type checking: is model continuous from scipy?
    _is_cts(model)
    rng: ArrayLike = np.linspace(model.ppf(0.01), model.ppf(0.99), num=100)
    prob_function: ArrayLike = model.pdf(rng)
    return rng, prob_function


def plot_cts(model: rv_discrete) -> None:
    """
    Plots the probability function of some probability model as a
    lineplot.

    Args:
        model: A scipy distribution

    Raises
        AssertionError: if arg dist is not of type rv_discrete or
        rv_continuous
    """
    pts: Tuple[ArrayLike, ArrayLike] = get_cts_points(model)
    f, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(x=pts[0], y=pts[1], lw=2, color="r")
    ax.set(xlabel="X", ylabel="Pr")
    plt.show()


def get_discrete_points(model: rv_discrete) -> Tuple[ArrayLike, ArrayLike]:
    """
    [summary]

    Args:
        model (rv_discrete): A discrete scipy distribution

    Returns:
        Tuple[ArrayLike, ArrayLike]: x, pmf
    """
    # type checking: is model discrete from scipy?
    # _is_discrete(model)
    rng: ArrayLike = np.arange(
        model.ppf(0.01), model.ppf(0.99)+1, dtype="int32")
    prob_function: ArrayLike = model.pmf(rng)
    return rng, prob_function


def plot_discrete(model: rv_continuous) -> None:
    """
    [summary]

    Args:
        model (rv_discrete):
    """
    pts: Tuple[ArrayLike, ArrayLike] = get_discrete_points(model)
    f, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=pts[0], y=pts[1], color="cornflowerblue")
    ax.set(xlabel="X", ylabel="Pr")
    plt.show()
