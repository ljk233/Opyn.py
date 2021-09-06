
"""
A module to help with calculating various confidence intervals and
performing simple signifigance tests.
There is no implementation for when dealing with proportions (i.e.,
normal approximation to the binomial).
Use `statsmodels` instead.
"""


from __future__ import annotations
from scipy import stats
import math


def pretty_print():
    ...


def get_ste_mean(std: float, nobs: int) -> float:
    """
    Returns the standard error of the mean.

    Args:
        std (`float`): sample standard deviation
        nobs (`int`): sample size

    Returns:
        `float`: standard error of the mean
    """
    return std / math.sqrt(nobs)


def zconfint_mean(
        x_bar: float,
        std: float,
        nobs: int,
        alpha: float = 0.05) -> tuple[float, float]:
    """
    Returns the 100(1-a)% z-interval

    Args:
        x_bar (`float`): sample mean
        std (`float`): sample standard deviation
        nobs (`int`): sample size
        alpha (`float`, optional): significance level for the
        confidence interval, coverage is 1-alpha. Defaults to 0.05.

    Returns:
        `tuple[float, float]`: lower and upper bound of confidence
        interval
    """
    ste_mean: float = get_ste_mean(std, nobs)
    zcrit: float = stats.norm().ppf(1-(alpha/2))
    return x_bar - zcrit*ste_mean, x_bar + zcrit*ste_mean


def get_ste_prop(p_hat: float, nobs: int) -> float:
    """
    Returns the standard error of the proportion

    Args:
        p_hat (`float`): estimated probability
        nobs (`int`): sample size

    Returns:
        `float`: standard error of the proportion
    """
    std: stats.bernoulli(p_hat).std()
    return std / math.sqrt(nobs)


def prop_confint(
        p_hat: float,
        nobs: int,
        alpha: float = 0.05) -> tuple[float, float]:
    """
    [summary]

    Args:
        p_hat (`float`): estimated proportion
        nobs (`int`): sample size
        alpha (`float`, optional): significance level for the
        confidence interval, coverage is 1-alpha. Defaults to 0.05.

    Returns:
        `tuple[float, float]`: lower and upper bound of confidence
        interval
    """
