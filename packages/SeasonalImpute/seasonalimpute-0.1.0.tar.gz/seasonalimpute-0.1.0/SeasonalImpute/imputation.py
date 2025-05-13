"""
Proposed imputation methods for time series data.

This module provides the SeasonalWeightedAverageImputation class for
    handling missing values in time series datasets using a weighted average
based on seasonality and nearest non-missing values.

Classes:
SeasonalWeightedAverageImputation: Implements a custom imputation method
that uses both the window and seasonal components to impute missing values.

"""

import warnings

import numpy as np
from gluonts.core.component import validated
from gluonts.transform.feature import DummyValueImputation, MissingValueImputation

warnings.filterwarnings("ignore")


class SeasonalWeightedAverageImputation(MissingValueImputation):
    """
    A custom imputation method for time series data based on weighted averages
    and seasonality.

    Args:
        window (int): The window size for finding nearby values to impute.
        seasonality (dict): A dictionary where the keys are seasonal periods
                            and the values are weights for seasonal components.
    """

    @validated()
    def __init__(self, window: int = None, seasonality: dict = None) -> None:
        """
        Initialize the imputation method.

        Args:
            window (int): The window size for finding nearby values to impute.
            seasonality (dict): A dictionary where the keys are seasonal periods
                                and the values are weights for seasonal components.
        """
        super().__init__()
        self.window = window
        self.seasonality = seasonality

    @staticmethod
    def __nth_nearest_values(lst, value, n):
        """
        Find the n nearest values in lst to the given value.
        """
        array = np.array(lst)
        differences = np.abs(array - value)
        sorted_indices = np.argsort(differences)
        nth_nearest_values = array[sorted_indices[:n]]
        return nth_nearest_values

    @staticmethod
    def __add_seasonality(idx, weights, wnn, seasonality):
        for i, v in seasonality.items():
            sesonal_idx = list(
                set(
                    np.concatenate(
                        [np.arange(idx, wnn[-1] + 1, i), np.arange(wnn[0] - 1, idx, i)]
                    )
                ).intersection(set(wnn))
            )
            if len(sesonal_idx) > 0:
                sorter = np.argsort(wnn)
                sesonal_idx = sorter[np.searchsorted(wnn, sesonal_idx, sorter=sorter)]
                weights[sesonal_idx] = weights[sesonal_idx] + v
        return weights

    @staticmethod
    def __weight_adjustment(x):
        max_val = np.max(x)
        return x / max_val if max_val != 0 else x  # Avoiding division by zero

    def __point_impute(self, x, idx, non_missing_index, w, seasonality):
        """
        Impute the missing value at index `idx` using nearby non-missing values.
        """
        wnn = self.__nth_nearest_values(non_missing_index, idx, w)
        if idx == 0:
            return x[non_missing_index[0]]
        if idx == len(x) - 1:
            return x[non_missing_index[-1]]
        weights = idx / np.abs(idx - wnn)
        weights = self.__weight_adjustment(weights)
        weights = self.__add_seasonality(idx, weights, wnn, seasonality)
        return np.average(x[wnn], weights=weights)

    def __call__(self, values: np.ndarray) -> np.ndarray:
        if len(values) <= 1 or np.all(np.isnan(values)):
            return DummyValueImputation()(values)

        array = values.copy()
        missing_index = np.where(np.isnan(array))[0]

        if missing_index.size > 0:
            non_missing_index = np.where(~np.isnan(array))[0]
            sw = (
                max(self.seasonality.keys(), default=0) * 2
                if self.seasonality
                else len(non_missing_index)
            )
            window = (
                min(len(non_missing_index), sw) if self.window is None else self.window
            )

            filled_values = [
                self.__point_impute(
                    array, x, non_missing_index, window, self.seasonality
                )
                for x in missing_index
            ]
            array[missing_index] = filled_values

        return array
