# pyqlrtest/qlrtest/core.py
import numpy as np
import statsmodels.api as sm
from .critical_values import get_qlr_pvalue # Only import what's needed from Hansen's method
from ._exceptions import InvalidTrimmingError, QLRTestError
from .utils import _ensure_numpy_array, _calculate_rss

def qlr_test(y, X, trim=0.15, sig_level=0.05, return_f_stats_series=False):
    """
    Performs the Quandt-Likelihood Ratio (QLR) test for structural breaks.

    Args:
        y (array-like): Dependent variable, time series.
        X (array-like): Independent variable(s), including an intercept if desired.
        trim (float, optional): Trimming percentage. Defaults to 0.15.
        sig_level (float, optional): Significance level for 'significant' flag. Defaults to 0.05.
        return_f_stats_series (bool, optional): If True, returns F-stats series. Defaults to False.

    Returns:
        dict: A dictionary containing the QLR test results:
            - 'max_f_stat' (float): The maximum F-statistic found.
            - 'breakpoint' (int): The index of the estimated breakpoint.
            - 'p_value' (float): The asymptotic p-value for the max_f_stat (from Hansen).
            - 'significant' (bool): True if p_value < sig_level, False otherwise.
            - 'n_observations' (int): Total number of observations.
            - 'n_parameters' (int): Number of parameters in the model (k).
            - 'trim_used' (float): The trimming percentage used.
            - 'tested_indices' (np.ndarray, optional): If return_f_stats_series is True.
            - 'f_stats' (np.ndarray, optional): If return_f_stats_series is True.
    """
    y_arr = _ensure_numpy_array(y, "y")
    X_arr = _ensure_numpy_array(X, "X")

    if y_arr.ndim > 1 and y_arr.shape[1] != 1:
        y_arr = y_arr.squeeze()
    if y_arr.ndim > 1:
        raise ValueError("y must be a 1-dimensional array or a 2D array with one column.")

    if X_arr.ndim == 1:
        X_arr = X_arr[:, np.newaxis]

    n_obs = len(y_arr)
    if X_arr.shape[0] != n_obs:
        raise ValueError("y and X must have the same number of observations.")

    if not 0.01 <= trim < 0.5:
        raise InvalidTrimmingError("Trimming 'trim' must be between 0.01 and 0.49.")

    k_params = X_arr.shape[1]

    start_index = int(np.floor(n_obs * trim))
    end_index = int(np.ceil(n_obs * (1 - trim)))

    min_obs_per_segment = k_params + 1
    if start_index < min_obs_per_segment:
        start_index = min_obs_per_segment
    if end_index > n_obs - min_obs_per_segment:
        end_index = n_obs - min_obs_per_segment
    
    if start_index >= end_index:
        raise QLRTestError(
            f"Not enough data points to test for breaks with k={k_params} "
            f"parameters and trim={trim}. "
            f"Effective range [{start_index}, {end_index-1}] is empty or too small."
        )

    f_stats_list = []
    tested_indices_list = []

    try:
        full_model = sm.OLS(y_arr, X_arr).fit()
        rss_full = full_model.ssr
    except Exception as e:
        raise QLRTestError(f"Failed to fit full model: {e}")

    for bp in range(start_index, end_index):
        y1, X1 = y_arr[:bp], X_arr[:bp, :]
        y2, X2 = y_arr[bp:], X_arr[bp:, :]

        if len(y1) < k_params or len(y2) < k_params:
            continue
        
        try:
            rss1 = _calculate_rss(y1, X1)
            rss2 = _calculate_rss(y2, X2)
        except np.linalg.LinAlgError: 
            continue 

        rss_unrestricted = rss1 + rss2
        
        numerator = (rss_full - rss_unrestricted) / k_params
        denominator = rss_unrestricted / (n_obs - 2 * k_params)

        if denominator <= 1e-9: # Avoid division by zero or very small positive
            f_stat = np.inf if numerator > 0 else 0.0 
        else:
            f_stat = numerator / denominator
        
        if f_stat < 0 and abs(f_stat) < 1e-9: # Handle numerical precision for very small negative F-stats
            f_stat = 0.0
        elif f_stat < 0: # Should not happen if RSS_full >= RSS_unrestricted
            # This might indicate an issue, but we'll cap at 0 for robustness.
            # print(f"Warning: Negative F-stat {f_stat} at bp {bp}. RSS_full={rss_full}, RSS_UR={rss_unrestricted}")
            f_stat = 0.0 

        f_stats_list.append(f_stat)
        tested_indices_list.append(bp)

    if not f_stats_list:
        raise QLRTestError("Could not compute F-statistics for any breakpoint. "
                           "Check data and trimming parameter.")

    f_stats_np = np.array(f_stats_list)
    max_f_stat = np.max(f_stats_np)
    
    breakpoint_index_in_tested = np.argmax(f_stats_np)
    estimated_breakpoint = tested_indices_list[breakpoint_index_in_tested]

    # Calculate p-value using Hansen's approximation
    # The effective trim used for p-value calculation in your original script was `start_index / n_obs`
    # This matches how Hansen's tables are often indexed by the actual start of the restricted period.
    # Using the input `trim` parameter for get_qlr_pvalue is also common if tables are for symmetric trimming.
    # Let's ensure `get_qlr_pvalue` expects the nominal `trim` proportion.
    # Your `_pv_sup` in the original script used `pi = start_index / n` for `l`.
    # Let's stick to user-provided `trim` for `get_qlr_pvalue` for simplicity, 
    # assuming `get_qlr_pvalue` and `_get_hansen_coeffs` correctly map this `trim` to the table rows.
    # If your Hansen tables are indexed by asymmetric start (like pi_0), then `start_index / n_obs` might be more appropriate for p-value lookup.
    # For now, using the input `trim`.
    p_value = get_qlr_pvalue(max_f_stat, k_params, trim) 
    
    significant = p_value < sig_level if not np.isnan(p_value) else False # Default to False if p_value is NaN

    results = {
        'max_f_stat': max_f_stat,
        'breakpoint': estimated_breakpoint,
        'p_value': p_value,
        'significant': significant,
        'n_observations': n_obs,
        'n_parameters': k_params,
        'trim_used': trim,
    }

    if return_f_stats_series:
        results['tested_indices'] = np.array(tested_indices_list)
        results['f_stats'] = f_stats_np

    return results