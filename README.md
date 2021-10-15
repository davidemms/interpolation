# Interpolation
This module replaces missing values in a CSV file with the average of the surrounding
values. Missing values are indicated by 'nan'

# Requirements
Python 3 

# Usage
```
python interpolation.py input_filename output_filename
```

# Tests
Unit tests:
```
python -m unittest test.test_interpolation
```

Acceptance tests:
```
python -m unittest test.acceptance_test
```
