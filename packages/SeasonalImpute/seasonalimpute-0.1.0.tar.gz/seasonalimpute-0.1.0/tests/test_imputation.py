import numpy as np

from SeasonalImpute import SeasonalWeightedAverageImputation


def test_imputation_basic():
    # Test case: simple array with one missing value
    data = np.array([1.0, 2.0, np.nan, 4.0, 5.0])
    imputer = SeasonalWeightedAverageImputation(window=2)
    result = imputer(data)
    assert not np.any(np.isnan(result)), "Imputed array contains NaN"
    assert abs(result[2] - 3.0) < 0.1, "Imputed value is not close to expected"


def test_imputation_with_seasonality():
    # Test case: array with seasonality
    data = np.array([1.0, np.nan, 3.0, 1.0, np.nan, 3.0])
    seasonality = {2: 0.5}  # Seasonal period of 2
    imputer = SeasonalWeightedAverageImputation(window=3, seasonality=seasonality)
    result = imputer(data)
    assert not np.any(np.isnan(result)), "Imputed array contains NaN"
    assert abs(result[1] - 1.0) < 0.5, "Imputed value does not respect seasonality"


def test_edge_cases():
    # Test case: all NaN or single value
    data = np.array([np.nan, np.nan])
    imputer = SeasonalWeightedAverageImputation()
    result = imputer(data)
    assert np.all(np.isnan(result)), "All NaN input should return NaN"

    data = np.array([1.0])
    result = imputer(data)
    assert np.array_equal(result, data), "Single value should remain unchanged"
