# SeasonalImpute Documentation

`SeasonalImpute` is a Python package for imputing missing values in time series data using a seasonal weighted average approach.

## Installation

Install the package via pip:

```bash
pip install SeasonalImpute
```

## Usage

The main class is `SeasonalWeightedAverageImputation`, which imputes missing values based on nearby values and seasonal patterns.

```python
import numpy as np
from SeasonalImpute import SeasonalWeightedAverageImputation

# Example data with missing values
data = np.array([1.0, np.nan, 3.0, 1.0, np.nan, 3.0])

# Initialize imputer with window and seasonality
imputer = SeasonalWeightedAverageImputation(window=3, seasonality={2: 0.5})

# Impute missing values
imputed_data = imputer(data)
print(imputed_data)
```

## Parameters

- `window` (int, optional): The number of nearby values to consider for imputation.
- `seasonality` (dict, optional): A dictionary mapping seasonal periods to weights (e.g., `{2: 0.5}` for a period of 2 with weight 0.5).

## Dependencies

- `numpy`
- `gluonts`
