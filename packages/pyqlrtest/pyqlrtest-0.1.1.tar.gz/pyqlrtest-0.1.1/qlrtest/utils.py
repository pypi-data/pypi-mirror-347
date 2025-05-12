import numpy as np
import statsmodels.api as sm # For OLS if not passed as pre-fitted

def _ensure_numpy_array(data, name="data"):
    """Converts input to a numpy array if it isn't already."""
    if data is None:
        raise ValueError(f"Input '{name}' cannot be None.")
    if not isinstance(data, np.ndarray):
        try:
            # Attempt to convert pandas Series/DataFrame or list-like to numpy
            import pandas as pd
            if isinstance(data, (pd.Series, pd.DataFrame)):
                return data.to_numpy()
            else:
                return np.asarray(data)
        except ImportError: # If pandas is not available
            return np.asarray(data)
        except Exception as e:
            raise ValueError(f"Could not convert '{name}' to a NumPy array: {e}")
    return data

def _calculate_rss(y, X):
    """
    Calculates Residual Sum of Squares (RSS) for OLS.
    y: dependent variable (1D numpy array)
    X: independent variables (2D numpy array)
    """
    if len(y) < X.shape[1]: # Not enough observations
        raise np.linalg.LinAlgError(
            "Not enough observations for OLS estimation in a segment."
            f"Obs: {len(y)}, Params: {X.shape[1]}"
        )
    try:
        model = sm.OLS(y, X).fit()
        return model.ssr
    except Exception as e: # Catch errors from OLS fitting (e.g. singular matrix)
        # print(f"Warning: OLS estimation failed in a segment: {e}")
        # Return a large RSS or re-raise, depending on desired handling.
        # For Chow test, a failed segment model means that breakpoint is problematic.
        raise np.linalg.LinAlgError(f"OLS estimation failed: {e}")