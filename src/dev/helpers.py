
"""
`opyn.stats.helpers`

A collection of conveninece classes for representing the various
datasets in the package.

The main aim of the classes is to hide labourious data transformations
behind pre-defined *views*, as as not to obscure the main teaching point.
"""

import pandas as pd
from ..pandasloader import PandasLoader


class BikeRentalDaily:
    """
    A class to return simplified views of the bikesharedaily dataset.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initialises the object.
        """
        self._data: pd.DataFrame = df

    def _make_time_series(self) -> None:
        """
        Sets the `dteday` column to type `datetime`, renames the column
        to date, and then sets it to the index.

        Raises:
            `AssertionError`: if receiver var _data is None.
        """
        assert self._data is not None, "View has not been initialised"
        self._data.rename(
                    columns={"dteday": "date", "yr": "year"}, inplace=True)
        dt_idx = pd.to_datetime(self._data["date"], format="%d/%m/%Y")
        self._data.set_index(dt_idx, inplace=True)
        self._data.drop(columns="date", inplace=True)

    def get_casual_by_day(self) -> pd.DataFrame:
        """
        Returns:
            Number of casual customers by day.
        """
        # self._data = pdloader.get()
        self._make_time_series()
        self._data.drop(
            columns=["instant", "holiday", "weekday", "workingday",
                     "mnth", "season", "weathersit", "temp",
                     "atemp", "hum", "windspeed", "registered",
                     "dailycount"],
            inplace=True)
        self._data.rename(columns={"casual": "total"}, inplace=True)
        self._data.replace(to_replace={0: 2011, 1: 2012}, inplace=True)
        return self._data

    def get_casual_by_month(self) -> pd.DataFrame:
        """
        Returns:
            Number of casual customers by month.
        """
        self._data = self.get_casual_by_day()
        # add month label
        month_order = ["January", "February", "March", "April",
                       "May", "June", "July", "August",
                       "September", "October", "November", "December"]
        self._data["month"] = pd.Categorical(
                                    values=self._data.index.month_name(),
                                    categories=month_order)
        # aggregate the data by month, year
        self._data = self._data.groupby(["month", "year"]).sum()[["total"]]
        self._data.reset_index(inplace=True)
        return self._data

    def get_casual_by_week(self) -> pd.DataFrame:
        """
        Returns:
            Number of casual customers by week.
        """
        self._data = self.get_casual_by_day()
        # add week label
        self._data["week"] = self._data.index.isocalendar().week
        # aggregate the data by week, year
        self._data = self._data.groupby(["week", "year"]).sum()[["total"]]
        self._data.reset_index(inplace=True)
        return self._data

    def get_casual_by_atemp(self) -> pd.DataFrame:
        """
        Returns:
            Number of casual customers per day by atemp.
        """
        self._make_time_series()
        self._data.drop(
            columns=["instant", "holiday", "weekday", "workingday",
                     "mnth", "season", "weathersit", "temp",
                     "hum", "windspeed", "registered",
                     "dailycount"],
            inplace=True)
        self._data.rename(columns={"casual": "total"}, inplace=True)
        self._data.replace(to_replace={0: 2011, 1: 2012}, inplace=True)
        return self._data
