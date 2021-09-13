
"""
A collection of abstract data types to represent various data descriptions.
"""

# %%
from __future__ import annotations
from dataclasses import dataclass
from typing import Any


class _GenericADT:
    """
    A helper class that handles the __repr__ and __str__ methods, and the
    prec
    """

    def __init__(self, prec: int, **kwargs) -> None:
        """
        Args:
            prec: precision to return the results
        """
        self._prec: int = prec
        self._params: dict[str, Any] = {}
        for key, value in kwargs.items():
            self._params[key] = value

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
        _str: str = ""
        for k, v in self._params.items():
            if k == 'name':
                pass
            elif _str == '':
                _str = f"{k}={round(v, self.prec)}"
            else:
                _str += f", {k}={round(v, self.prec)}"
        return _str

    def __repr__(self) -> str:
        return f"{self._params['name']}({self})"


class ZTestADT(_GenericADT):
    """
    A class to represent the results of a z-test
    """

    def __init__(self, res: tuple[float], prec: int = 4) -> None:
        """
        Args:
            res: a tuple of floats
            prec: precision to return the results
        """
        super().__init__(prec, name='hypothtest', zstat=res[0], pval=res[1])
        self._zstat: float = res[0]
        self._pval: float = res[1]

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


class NormADT(_GenericADT):
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
        super().__init__(prec, name='N', mean=mean, var=var)
        self._mean: float = mean
        self._var = var

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


class PairedVarsADT(_GenericADT):
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
        super().__init__(
            prec, name='pairedvars', cov=cov, corr_coeff=corr_coeff
            )
        self._cov: float = cov
        self._corr_coeff = corr_coeff

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


@dataclass
class ChiSqTest():
    """Models the results of a chi-sqared test of no association.
    """

    _chisq: float = 0.0
    _pval: float = 0.0
    _df: int = 0

    @property
    def chisq(self) -> float:
        """
        """
        return float(self._chisq)

    @property
    def pval(self) -> float:
        """
        """
        return float(self._pval)

    @property
    def df(self) -> int:
        """
        """
        return self._df

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"chisq={self.chisq:.6f}, pval={self.pval:.6f}, df={self.df}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"ChiSqTest({self})"
        )


@dataclass
class ConfInt:
    """Models a confidence interval.
    """

    _lower: float = 0.0
    _upper: float = 0.0

    @property
    def lower(self) -> float:
        """
        """
        return float(self._lower)

    @property
    def upper(self) -> float:
        """
        """
        return float(self._upper)


@dataclass
class RelativeRisk:
    """A dataclass to model the relative risk of a cohort study.
    """

    _point: float = 0.0
    _lower: float = 0.0
    _upper: float = 0.0

    @property
    def point(self) -> float:
        return float(self._point)

    @property
    def lower(self) -> float:
        """
        """
        return float(self._lower)

    @property
    def upper(self) -> float:
        """
        """
        return float(self._upper)

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"point={self.point:.6f}"
            f", zconfint={{lower={self.lower:.6f}, upper={self.upper:.6f}}}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"RelativeRisk({self})"
        )


@dataclass
class OddsRatio:
    """A dataclass to model the odds ratio of a cohort and case-control study.
    """

    _point: float = 0.0
    _lower: float = 0.0
    _upper: float = 0.0

    @property
    def point(self) -> float:
        return float(self._point)

    @property
    def lower(self) -> float:
        """
        """
        return float(self._lower)

    @property
    def upper(self) -> float:
        """
        """
        return float(self._upper)

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"point={self.point:.6f}"
            f", zconfint={{lower={self.lower:.6f}, upper={self.upper:.6f}}}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"OddsRatio({self})"
        )


@dataclass
class OddsDiseaseExposure:
    """Models the odds of disease given exposure in a cohort and case-control
    study.
    """

    _d_given_e: float = 0.0
    _d_given_not_e: float = 0.0
    _e_given_d: float = 0.0
    _e_given_not_d: float = 0.0

    @property
    def disease_exposed(self) -> float:
        """
        """
        return float(self._d_given_e)

    @property
    def disease_not_exposed(self) -> float:
        """
        """
        return float(self._d_given_not_e)

    @property
    def exposed_disease(self) -> float:
        """
        """
        return float(self._d_given_e)

    @property
    def exposed_no_disease(self) -> float:
        """
        """
        return float(self._d_given_not_e)

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"OD(D|E)={self.disease_exposed:.6f}"
            f", OD(D|Not E)={self.disease_not_exposed:.6f}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"OddsDiseaseExposure({self})"
        )
