
"""
`opynuni.stats.probmodels`

TODO: Add module sting
"""


from __future__ import annotations
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import rv_discrete, rv_continuous
from typing import Union
from numpy.typing import ArrayLike


def get_cts_points(model: rv_continuous) -> tuple:
    """
    Generates the points that can be used for visualisations of some
    continuous probability model.

    Args:
        dist (rv_continuous): A continuous **SciPy** distribution

    Raises:
        AssertionError: if arg `dist` is not of type `rv_continuous`

    Returns:
        `x`, `pdf`:
            tuple of `np.arrays` that can used for plotting
    """
    assert getattr(model, "pdf", False), "Not a continuous distribution."
    rng = np.linspace(model.ppf(0.01), model.ppf(0.99), num=100)
    prob_function = model.pdf(rng)
    return rng, prob_function


def plot_cts(model: rv_continuous, title: str = "") -> None:
    """
    Plots the probability function of some probability model as a
    lineplot.

    Args:
        model: a continuous **SciPy** distribution
        title: title of the outputted graph
    """
    pts = get_cts_points(model)
    f, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(x=pts[0], y=pts[1], lw=2, color="r")
    ax.set(title=title, xlabel="X", ylabel="Pr")
    plt.show()


def get_discrete_points(model: rv_discrete) -> tuple:
    """
    Generates the points that can be used for visualisations of some
    discrete probability model.

    Args:
        model: a discrete  **SciPy** distribution

    Raises:
        AssertionError: if arg `dist` is not of type `rv_discrete`

    Returns:
        `x`, `pmf`:
            tuple of `np.arrays` that can used for plotting
    """
    assert getattr(model, "pmf", False), "Not a discete distribution."
    rng = np.arange(
        model.ppf(0.01), model.ppf(0.99)+1, dtype="int32")
    prob_function = model.pmf(rng)
    return rng, prob_function


def plot_discrete(model: rv_discrete, title: str = "") -> None:
    """
    Plots the probability function of some probability model as a
    barplot.

    Args:
        model: a discrete **SciPy** distribution
        title: title of the outputted graph
    """
    pts = get_discrete_points(model)
    f, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=pts[0], y=pts[1], color="cornflowerblue")
    ax.set(title=title, xlabel="X", ylabel="Pr")
    plt.show()


class ProbModel:
    """
    A class to represent a probability model as implemented by **SciPy**.

    It is used to produce a plot of the probability function.
    """

    def __init__(
        self, model: Union[stats.rv_discrete, stats.rv_continuous], type: str
    ) -> None:
        """
        Args:
            model: an object from **SciPy**, either discrete or continuous.
            type: must be one of either `['discrete', 'continuous']`

        Raises:
            AssertionError: if arg `type` is not in \
                `['discrete', 'continuous']`
            AssertionError: if arg `type` is `'continous'` and arg `model` is \
                not of type `rv_continuous`, or arg if `type` is `'discrete'` \
                and arg `model` is not of type `rv_discrete`
        """
        assert type in ["discrete", "continuous"], (
            f"{type} is not in [\"discrete\", \"continuous\"]"
            )
        if type == 'continuous':
            assert getattr(model, "pdf", False), (
                "`model` is not a continuous distribution from SciPy")
        else:  # type == 'discrete':
            assert getattr(model, "pmf", False), (
                "`model` is not a discrete distribution from SciPy")
        self.model: Union[stats.rv_discrete, stats.rv_continuous] = model
        self.type: str = type

    @property
    def rng(self) -> ArrayLike[float]:
        """
        """
        if self.type == 'discrete':
            return np.arange(self.model.ppf(0.01), self.model.ppf(0.99)+1)
        else:  # type == 'continuous'
            return (
                np.linspace(
                    self.model.ppf(0.01), self.model.ppf(0.99), num=100
                    )
                )

    @property
    def prob_func(self) -> ArrayLike[float]:
        """
        """
        if self.type == 'discrete':
            return self.model.pmf(self.rng)
        else:  # type == 'continuous'
            return self.model.pdf(self.rng)

    def plot(self, title: str = "") -> None:
        """
        Plots the probability function of the receiver's `model`

        Args:
            title: title of the outputted graph
        """
        f, ax = plt.subplots(figsize=(8, 6))
        if self.type == 'discrete':
            sns.barplot(x=self.rng, y=self.prob_func, color="cornflowerblue")
        else:  # type == 'continuous'
            sns.lineplot(x=self.rng, y=self.prob_func, lw=2, color="r")
        ax.set(title=title, xlabel="X", ylabel="Pr")
        plt.show()
