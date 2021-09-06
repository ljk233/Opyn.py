
"""
`opynuni.stats.probmodels`

TODO: Add module sting
"""


from __future__ import annotations
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from typing import Union
from numpy.typing import ArrayLike


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
        if type == 'discrete':
            assert getattr(model, "pmf", False), (
                "`model` is not a discrete distribution from SciPy")
        else:
            assert getattr(model, "pdf", False), (
                "`model` is not a continuous distribution from SciPy")
        self.model: Union[stats.rv_discrete, stats.rv_continuous] = model
        self.type: str = type

    @property
    def rng(self) -> ArrayLike[float]:
        """
        """
        if self.is_discrete():
            return np.arange(self.model.ppf(0.01), self.model.ppf(0.99)+1)
        else:
            return (
                np.linspace(
                    self.model.ppf(0.01), self.model.ppf(0.99), num=100
                    )
                )

    @property
    def prob_func(self) -> ArrayLike[float]:
        """
        """
        if self.is_discrete():
            return self.model.pmf(self.rng)
        else:
            return self.model.pdf(self.rng)

    def is_discrete(self) -> bool:
        """
        Returns:
            `True` if receiver's `type` is `'discrete'`, otherwise `False`
        """
        return self.type == 'discrete'

    def plot(self, title: str = "") -> None:
        """
        Plots the probability function of the receiver's `model`

        Args:
            title: title of the outputted graph
        """
        f, ax = plt.subplots(figsize=(8, 6))
        if self.is_discrete():
            ylab: str = 'p(x)'
            sns.barplot(x=self.rng, y=self.prob_func, color="cornflowerblue")
        else:
            ylab: str = 'f(x)'
            sns.lineplot(x=self.rng, y=self.prob_func, lw=2, color="r")
        ax.set(title=title, xlabel="x", ylabel=ylab)
        plt.show()
