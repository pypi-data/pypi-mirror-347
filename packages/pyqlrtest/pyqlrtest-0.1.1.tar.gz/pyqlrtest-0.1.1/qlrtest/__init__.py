"""
QLRTest: A Python package for Quandt-Likelihood Ratio (QLR) tests 
to detect structural breaks in time series regression models.
"""
from .core import qlr_test
from .critical_values import get_qlr_pvalue
from ._exceptions import QLRTestError, InvalidTrimmingError

__version__ = "0.1.1"

__all__ = [
    "qlr_test",
    "get_qlr_pvalue",
    "get_approx_qlr_critical_value",
    "QLRTestError",
    "InvalidTrimmingError",
]