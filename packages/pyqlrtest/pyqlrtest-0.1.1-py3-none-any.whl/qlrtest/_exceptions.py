class QLRTestError(Exception):
    """Base class for exceptions in the qlrtest package."""
    pass

class InvalidTrimmingError(QLRTestError):
    """Raised when the trimming percentage is outside the allowed range."""
    pass

class CriticalValueNotFoundError(QLRTestError):
    """Raised when critical values cannot be found or approximated."""
    pass

class ModelEstimationError(QLRTestError):
    """Raised when an underlying OLS model cannot be estimated."""
    pass