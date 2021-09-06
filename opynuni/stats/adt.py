
"""
A collection of abstract data types to represent various data descriptions.
"""


class ConfInt:
    """
    A confidence interval with lower and upper boundaries
    """

    def __init__(self, res: tuple[float], prec: int = 4) -> None:
        """
        Args:
            res: a tuple of floats
            prec: precision to return the results
        """
        self.lower: float = res[0]
        self.upper: float = res[1]
        self.prec: int = prec

    def __str__(self) -> str:
        return (
            f"lower={round(self.lower, self.prec)}, "
            f"upper={round(self.upper, self.prec)}"
            )

    def __repr__(self) -> str:
        return f"confint({self})"


class NormRepr:
    """
    A normal distribution with mean and var
    """

    def __init__(
        self, mean: float, var: float, prec: int = 4
    ) -> None:
        """
        Args:
            mean: mean of normal dist
            var: variance of normal dist
            prec: prec: precision to return the results
        """
        self.mean: float = mean
        self.var = var
        self.prec: int = prec

    def __str__(self) -> str:
        return (
            f"mean={round(self.mean, self.prec)}, "
            f"var={round(self.var, self.prec)}"
            )

    def __repr__(self) -> str:
        return f"N({self})"


class PairedVarsRepr:
    """
    Description of paried variables.

    Currently returns:
    - Covariance
    - Correlation coefficient
    """

    def __init__(
        self, cov: float, corr_coeff: float, prec: int = 4
    ) -> None:
        """
        Args:
            cov: Cov(x, y)
            corr_coeff: Pearson's correlation coefficient, *r*
            prec: prec: precision to return the results
        """
        self.cov: float = cov
        self.corr_coeff = corr_coeff
        self.prec: int = prec

    def __str__(self) -> str:
        return (
            f"cov={round(self.cov, self.prec)}, "
            f"r={round(self.corr_coeff, self.prec)}"
            )

    def __repr__(self) -> str:
        return f"pairedvars({self})"
