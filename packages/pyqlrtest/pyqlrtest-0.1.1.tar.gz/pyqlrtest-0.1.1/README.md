# pyqlrtest

[![PyPI version](https://badge.fury.io/py/pyqlrtest.svg)](https://badge.fury.io/py/pyqlrtest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/yourusername/pyqlrtest/actions/workflows/python-package.yml/badge.svg)](https://github.com/yourusername/pyqlrtest/actions/workflows/python-package.yml) `pyqlrtest` is a Python package for performing Quandt-Likelihood Ratio (QLR) tests, also known as sup-F tests, to detect structural breaks in time series regression models. This test is crucial for identifying points in time where the parameters of a model may have changed.

The implementation calculates F-statistics across a trimmed range of potential breakpoints and uses Hansen's (1997, 2000) approximations for asymptotic p-values.

## Features

- Calculation of QLR (sup-F) statistic.
- Estimation of the most likely breakpoint.
- Asymptotic p-value calculation using Hansen's (1997, 2000) method.
- Approximated critical values based on Andrews (2003) for 15% trimming.
- Supports `numpy` arrays and `pandas` Series/DataFrames as input.
- Flexible trimming parameter.

## Installation

You can install `pyqlrtest` using pip (once it's published to PyPI):

```bash
pip install pyqlrtest