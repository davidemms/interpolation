# Interpolation
This module replaces missing values in a CSV file with the average of the surrounding
values. Missing values are indicated by 'nan'

# Requirements
Python 3 

# Usage
```
python3 interpolator.py input_filename output_filename
```

# Tests
Unit tests:
```
python3 -m unittest test.test_interpolator
```

Acceptance tests:
```
python3 -m unittest test.acceptance_test
```
