
"""A module to help perform analyses on various observatioanl studies.

This module was implemented following studies of M249, Book 1.

Classes:
    - **TwoByTwo**:
        Models an observational study with two exposures.
    - **StratifiedTable**:
        Models an observational study with three exposure cateogries.

Dependencies:
    - **scipy**
    - **statsmodels**
    - **pandas**
    - **numpy**

Examples:
    - To be added.
"""


from __future__ import annotations
from scipy import stats
from statsmodels.stats import contingency_tables
from .dataclasses import ChiSqTest, OddsRatio, RelativeRisk
import pandas as pd
import numpy as np
from numpy.typing import ArrayLike
from typing import Union


class TwoByTwo:
    """Models an observational study with two exposures.

    It has a composite relationship with `Table2x2` class from
    `statsmodels`, such that a `TwoByTwo` *has-a* `Table2x2`.

    Parameters:
        table (ArrayLike): Observations from the study. It is expected that\
            the data structure can be cast to a **numpy** `array`.

    Attributes:
        col_labels (list[str]): Column labels to be used in a `DataFrame`.\
            Default is `["Disease", "No Disease"]`.
        table (np.ndarray): Table of results.
        row_labels (list[str]): Column labels to be used in a `DataFrame`.\
            Default is `["Exposed", "Not Exposed"]`.
        table2x2 (Table2x2): Initialised instance of **statsmodels**\
            `Table2x2` used for modelling the analysis.

    Warning:
        There is no type checking on **col_labels** and **row_label**.

    Class Methods:
        from_dataframe: Initialise a `TwoByTwo` object from a **Pandas**\
            `DataFrame`.

    Methods:
        chi2_contribs: Return the chi-squared contributions for each\
            observation used in a chi-squared test of no association.
        chi2_test: Return the results of a chi-squared test of no\
            association.
        expected_freq: Return the expected frequencies from a contingency\
            table under the null hypothesis of no association.
        odds_ratio: Return point and interval estimates for the odds ratio.
        relative_risk: Return point and interval estimates for the relative\
            risk.
        show: Return the table as a **Pandas** `DataFrame`.
    """

    def __init__(self, table: ArrayLike) -> None:
        """Initialises the object.

        Args:
            table: some data structure representing the data.\
                Do not include marginal totals.\
                Example data structure: `[[1, 5], [10, 15]]`.
        """
        self.table: np.ndarray = np.array(table)
        self.table2x2: contingency_tables.Table2x2 = (
            contingency_tables.Table2x2(self.table)
        )
        self.row_labels: list[str] = ["Exposed", "Not Exposed"]
        self.col_labels: list[str] = ["Disease", "No Disease"]

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        exposure: str = "exposure",
        outcome: str = "outcome"
    ) -> TwoByTwo:
        """Return an initialised instance of TwoByTwo.

        Args:
            df: [description]
            exposure: [description].
            outcome: [description].

        Returns:
            StratifiedTable: [description]
        """
        arr = df.pivot(index=exposure, columns=outcome).to_numpy()
        return cls(arr.reshape((2, 2)))

    def __getitem__(self, row: int) -> np.ndarray:
        """Return a row from the TwoByTwo table.

        Args:
            row: Row num, either 0, 1.
        """
        return self.table[row]

    def relative_risk(
        self, alpha: float = 0.05, as_pandas: bool = True
    ) -> Union[pd.DataFrame, RelativeRisk]:
        """Return the point and (1-alpha)% confidence interval estimates for
        the relative risk.

        Args:
            alpha: Significance level for the confidence interval.
            as_pandas: bool: It True, return the estimates as a DataFrame.\
                Otherwise, return the dataclass representation.

        Returns:
            Point and (1-alpha)% confidence interval estimates for\
            the relative risk.
        """
        ci = self.table2x2.riskratio_confint(alpha)
        riskratio = RelativeRisk(
            self.table2x2.riskratio,
            self.table2x2.log_riskratio_se,
            ci[0],
            ci[1]
        )
        if as_pandas:
            return riskratio.as_df()
        else:
            return riskratio   

    def odds_ratio(
        self, alpha: float = 0.05, as_pandas: bool = True
    ) -> Union[pd.DataFrame, OddsRatio]:
        """Return the point and (1-alpha)% confidence interval estimates for
        the odds ratio.

        Args:
            alpha: Significance level for the confidence interval.
            as_pandas: bool: It True, return the estimates as a DataFrame.\
                Otherwise, return the dataclass representation.

        Returns:
            Point and (1-alpha)% confidence interval estimates for\
            the odds ratio.
        """
        ci = self.table2x2.oddsratio_confint(alpha)
        oddsratio = OddsRatio(
            self.table2x2.oddsratio,
            self.table2x2.log_oddsratio_se,
            ci[0],
            ci[1]
        )
        if as_pandas:
            return oddsratio.as_df()
        else:
            return oddsratio       

    def expected_freq(
        self, row_totals: bool = False, col_totals: bool = False
    ) -> pd.DataFrame:
        """Return the expected frequencies from a contingency table under
        the hypothesis of no association.

        Args:
            show_row_totals: If `True`, then include the row marginal\
                totals in the `DataFrame`. Otherwise, do not include them.
            show_col_totals: If `True`, then include the column\
                marginal totals in the the `DataFrame`. Otherwise, do not\
                include them.

        Returns:
            Expected frequencies.
        """
        res = stats.contingency.expected_freq(self.table)
        return self._to_pandas(res, row_totals, col_totals)

    def chi2_contribs(self) -> pd.DataFrame:
        """Return the chi-squared contributions for each observation used in a
        chi-squared test of no association.

        Returns:
            chi-squared contributions.
        """
        res = self.table2x2.chi2_contribs
        return self._to_pandas(res, False, False)

    def chi2_test(
        self,
        as_pandas: bool = True
    ) -> Union[pd.DataFrame, ChiSqTest]:
        """Return the results of a chi-squared test of no association.

        Args:
            as_pandas: bool: It True, return the estimates as a DataFrame.\
                Otherwise, return the dataclass representation.

        Returns:
            Results of a chi-squared test of no association.
        """
        res = stats.chi2_contingency(self.table, correction=False)
        chisq = ChiSqTest(res[0], res[1], res[2])
        if as_pandas:
            return chisq.as_df()
        else:
            return chisq   

    def show(
        self, row_totals: bool = False, col_totals: bool = False
    ) -> pd.DataFrame:
        """Return a contingency table of the study.

        Args:
            show_row_totals: If `True`, then include the row marginal\
                totals in the `DataFrame`. Otherwise, do not include them.
            show_col_totals: If `True`, then include the column marginal\
                totals in the the `DataFrame`. Otherwise, do not include them.

        Returns:
            Contingency table of the study.
        """
        return self._to_pandas(self.table, row_totals, col_totals)

    def _to_pandas(
        self,
        res: np.ndarray,
        show_row_totals: bool,
        show_col_totals: bool
    ) -> pd.DataFrame:
        """Helper method.

        Args:
            res: Results to display as a DataFrame.
            show_row_totals: If `True`, then include the row marginal\
                totals in the `DataFrame`. Otherwise, do not include them.
            show_col_totals: If `True`, then include the column\
                marginal totals in the the `DataFrame`. Otherwise, do not\
                include them.

        Returns:
            Receiver's table as a **pandas** DataFrame.
        """

        # initialise a new DataFrame
        df: pd.DataFrame = pd.DataFrame(res, self.row_labels, self.col_labels)

        # melt the df, then pivot it
        df.reset_index(inplace=True)
        df.rename(columns={"index": "Exposure"}, inplace=True)
        df = df.melt(id_vars="Exposure")
        df = df.pivot_table(
            index="Exposure",
            columns="variable",
            values="value",
            aggfunc=np.sum,
            margins=True,
            margins_name="Total")
        df.rename_axis(["Outcome"], axis=1, inplace=True)

        # remove marginal totals
        if not show_row_totals:
            df.drop(columns="Total", inplace=True)
        if not show_col_totals:
            df.drop(index="Total", inplace=True)

        return df


class StratifiedTable:
    """Analyses for a collection of 2x2 contingency tables.
    """

    def __init__(
        self,
        data: ArrayLike,
        strata_labels: list[str]
    ) -> None:
        """Initialise an instance of `StratifiedTable`
        """
        self._tables: ArrayLike = data
        if isinstance(data, np.ndarray):
            data = data.tolist()
        self.statified_table: contingency_tables.StratifiedTable = (
            contingency_tables.StratifiedTable(data)
        )
        self.row_labels: list[str] = ["Exposed", "Not Exposed"]
        self.col_labels: list[str] = ["Disease", "No Disease"]
        self.strata_labels = strata_labels

    @property
    def aggregated(self) -> TwoByTwo:
        """Return the aggregated data as a 2x2 contingency table.
        """
        obs: list[list[int, int]] = [[0, 0], [0, 0]]
        for table in self._tables:
            obs[0][0] += table[0][0]
            obs[0][1] += table[0][1]
            obs[1][0] += table[1][0]
            obs[1][1] += table[1][1]
        two_by_two: TwoByTwo = TwoByTwo(obs)
        two_by_two.row_labels = self.row_labels
        two_by_two.col_labels = self.col_labels
        return two_by_two

    @property
    def strata(self) -> dict[str, TwoByTwo]:
        """Return a dictionary of stratified tables for stratum-specific
        analysis.

        Returns:
            Add summary
        """
        tables: dict[str, TwoByTwo] = {}
        for count, stratum in enumerate(self._tables):
            table: TwoByTwo = TwoByTwo(stratum)
            table.row_labels = self.row_labels
            table.col_labels = self.col_labels
            tables[self.strata_labels[count]] = table
        return tables

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        strata_labels: list[str],
        exposure: str = "exposure",
        outcome: str = "outcome",
        stratum: str = "stratum"
    ) -> StratifiedTable:
        """Return an instance of StratifiedTable.

        Args:
            df (pd.DataFrame): [description]
            strata_labels: Descriptive labels for the strata.
            exposure (str, optional): [description]. Defaults to "exposure".
            outcome (str, optional): [description]. Defaults to "outcome".
            stratum (str, optional): [description]. Defaults to "stratum".

        Returns:
            StratifiedTable: [description]
        """
        arr = df.pivot(index=[stratum, exposure], columns=outcome).to_numpy()
        print(arr.reshape((2, 2, len(strata_labels))))
        return cls(arr.reshape((2, 2, len(strata_labels))), strata_labels)

    def adjusted_odds_ratio(
        self, alpha: float = 0.05, as_pandas: bool = True
    ) -> Union[pd.DataFrame, OddsRatio]:
        """Return the point and (1-alpha)% confidence interval estimates for
        the adjusted odds ratio.

        It uses the Mantel-Haenszel odds ratio.

        Args:
            alpha: Significance level for the confidence interval.
            as_pandas:

        Returns:
            Point and (1-alpha)% confidence interval estimates for\
            the odds ratio.
        """
        ci = self.statified_table.oddsratio_pooled_confint(alpha)
        oddsratio = OddsRatio(
            self.statified_table.oddsratio_pooled,
            self.statified_table.logodds_pooled_se,
            ci[0],
            ci[1]
        )
        if as_pandas:
            return oddsratio.as_df()
        else:
            return oddsratio 

    def unadjusted_odds_ratio(
        self, alpha: float = 0.05, as_pandas: bool = True
    ) -> Union[pd.DataFrame, OddsRatio]:
        """Return the point and (1-alpha)% confidence interval estimates for
        the unadjusted odds ratio.

        Args:
            alpha: Significance level for the confidence interval.
            as_pandas:

        Returns:
            Point and (1-alpha)% confidence interval estimates for\
            the odds ratio.
        """
        if as_pandas:
            return self.aggregated.odds_ratio(alpha)
        else:
            return self.aggregated.odds_ratio(alpha, as_pandas=False)

    def test_no_association(
        self, as_pandas: bool = True
    ) -> Union[ChiSqTest, pd.DataFrame]:
        """Return the results of a test that of the null hypothesis of
        no between the exposure and the disease, adjusted for the
        stratifying variable.

        Uses the Mantel-Haenszel test.

        Returns:
            test statistic and the p-value.
        """
        # get result
        res = self.statified_table.test_null_odds(True)
        chisq = ChiSqTest(
            res.statistic,
            res.pvalue,
            1
        )
        if as_pandas:
            return chisq.as_df()
        else:
            return chisq

    def test_homogeneity(
        self,
        as_pandas: bool = True
    ) -> Union[ChiSqTest, pd.DataFrame]:
        """Return the results test of the null hypothesis that the odds
        ratio is the same in all _k_ strata.

        This is the Tarone test.

        Args:
            adjust: If true, use the Tarone adjustment to achieve the chi^2\
                asymptotic distribution. 

        Returns:
            test statistic and the p-value.
        """
        # get result
        res = self.statified_table.test_equal_odds(True)
        chisq = ChiSqTest(
            res.statistic,
            res.pvalue,
            1
        )
        if as_pandas:
            return chisq.as_df()
        else:
            return chisq
