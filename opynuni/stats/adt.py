
"""
A collection of abstract data types to represent various data descriptions.
"""


from __future__ import annotations


class ZTestADT:
    """
    *class* `opynuni.stats.adt.ZTestRepr`

    A dataclass to represent the results of a z-test
    """

    def __init__(self, res: tuple[float], prec: int = 4) -> None:
        """
        Args:
            res: a tuple of floats
            prec: precision to return the results
        """
        self._zstat: float = res[0]
        self._pval: float = res[1]
        self._prec: int = prec

    @property
    def zstat(self) -> float:
        """
        """
        return self._zstat

    @property
    def pval(self) -> float:
        """
        """
        return self._pval

    @property
    def prec(self) -> float:
        """
        """
        return self._prec

    @prec.setter
    def prec(self, num: int) -> None:
        """
        """
        self._prec = num

    def __str__(self) -> str:
        return (
            f"zstat={round(self.zstat, self.prec)}, "
            f"pval={round(self.pval, self.prec)}"
            )

    def __repr__(self) -> str:
        return f"results({self})"


class ConfIntADT:
    """
    *class* `opynuni.stats.adt.ZTestRepr`

    A class to represent any confidence interval.
    """

    def __init__(self, res: tuple[float], prec: int = 4) -> None:
        """
        Args:
            res: a tuple of floats
            prec: precision to return the results
        """
        self._lower: float = res[0]
        self._upper: float = res[1]
        self._prec: int = prec

    @property
    def lower(self) -> float:
        """
        """
        return self._lower

    @property
    def upper(self) -> float:
        """
        """
        return self._upper

    @property
    def prec(self) -> float:
        """
        """
        return self._prec

    @prec.setter
    def prec(self, num: int) -> None:
        """
        """
        self._prec = num

    def __str__(self) -> str:
        return (
            f"lower={round(self.lower, self.prec)}, "
            f"upper={round(self.upper, self.prec)}"
            )

    def __repr__(self) -> str:
        return f"confint({self})"


class NormADT:
    """
    A class to represent a normal distribution.
    """

    def __init__(
        self, mean: float, var: float, prec: int = 4
    ) -> None:
        """
        Args:
            mean: mean of normal dist
            var: variance of normal dist
            prec: precision to return the results
        """
        self._mean: float = mean
        self._var = var
        self._prec: int = prec

    @property
    def mean(self) -> float:
        """
        """
        return self._mean

    @property
    def var(self) -> float:
        """
        """
        return self._var

    @property
    def prec(self) -> float:
        """
        """
        return self._prec

    @prec.setter
    def prec(self, num: int) -> float:
        """
        """
        self._prec = num

    def __str__(self) -> str:
        return (
            f"mean={round(self.mean, self.prec)}, "
            f"var={round(self.var, self.prec)}"
            )

    def __repr__(self) -> str:
        return f"N({self})"


class PairedVarsADT:
    """
    A class to represent paried variables.
    Currently returns:
    """

    def __init__(
        self, cov: float, corr_coeff: float, prec: int = 4
    ) -> None:
        """
        Args:
            cov: Cov(x, y)
            corr_coeff: Pearson's correlation coefficient, *r*
            prec: precision to return the results
        """
        self._cov: float = cov
        self._corr_coeff = corr_coeff
        self._prec: int = prec

    @property
    def cov(self) -> float:
        """
        """
        return self._cov

    @property
    def corr_coeff(self) -> float:
        """
        """
        return self._corr_coeff

    @property
    def prec(self) -> float:
        """
        """
        return self._prec

    @prec.setter
    def prec(self, num: int) -> float:
        """
        """
        self._prec = num

    def __str__(self) -> str:
        return (
            f"cov={round(self.cov, self.prec)}, "
            f"r={round(self.corr_coeff, self.prec)}"
            )

    def __repr__(self) -> str:
        return f"pairedvars({self})"
