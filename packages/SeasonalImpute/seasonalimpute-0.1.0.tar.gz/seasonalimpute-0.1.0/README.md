# SeasonalImpute

A Python package for imputing missing values in time series data using a seasonal weighted average approach.

## Installation

```bash
pip install SeasonalImpute
```

## Usage

```python
import numpy as np
from SeasonalImpute import SeasonalWeightedAverageImputation

# Example data
data = np.array([1.0, np.nan, 3.0, 1.0, np.nan, 3.0])

# Impute with seasonality
imputer = SeasonalWeightedAverageImputation(window=3, seasonality={2: 0.5})
imputed_data = imputer(data)
print(imputed_data)
```

## Features

- Imputes missing values using nearby values and seasonal patterns.
- Customizable window size and seasonal weights.
- Built on `gluonts` and `numpy` for robust time series handling.

## Development

To contribute:

1. Clone the repository:

   ```bash
   git clone https://github.com/hanifkia/SeasonalImpute.git
   ```

2. Install dependencies:

   ```bash
   pip install -e .[dev]
   ```

3. Run tests:

   ```bash
   pytest
   ```

## License

MIT License. See [LICENSE](LICENSE) for details.
