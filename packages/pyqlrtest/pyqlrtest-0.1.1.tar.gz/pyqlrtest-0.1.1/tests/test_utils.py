import pytest
import numpy as np
import pandas as pd
from qlrtest.utils import _ensure_numpy_array, _calculate_rss

def test_ensure_numpy_array():
    # Test with numpy array input
    arr_in = np.array([1, 2, 3])
    assert np.array_equal(_ensure_numpy_array(arr_in), arr_in)

    # Test with list input
    list_in = [1, 2, 3]
    assert np.array_equal(_ensure_numpy_array(list_in), np.array(list_in))

    # Test with pandas Series input
    try:
        series_in = pd.Series([1, 2, 3])
        assert np.array_equal(_ensure_numpy_array(series_in), series_in.to_numpy())
    except ImportError:
        pytest.skip("Pandas not installed, skipping Series test.")

    # Test with pandas DataFrame input (single column)
    try:
        df_in_single_col = pd.DataFrame({'a': [1, 2, 3]})
        # Should convert to a 2D numpy array
        assert np.array_equal(_ensure_numpy_array(df_in_single_col), df_in_single_col.to_numpy())
    except ImportError:
        pytest.skip("Pandas not installed, skipping DataFrame test.")

    # Test with None input
    with pytest.raises(ValueError):
        _ensure_numpy_array(None)

def test_calculate_rss_simple():
    """Test _calculate_rss with a simple known case."""
    X = np.column_stack((np.ones(5), np.arange(5, dtype=float))) # y = c0 + c1*x
    
    # Manual OLS for y = beta0 + beta1*x
    # beta = (X'X)^-1 X'y
    # XTX = np.array([[5, 10], [10, 30]])
    # XTY = np.array([15, 40])
    # XTX_inv = np.linalg.inv(XTX) # [[0.6, -0.2], [-0.2, 0.1]]
    # beta_hat = XTX_inv @ XTY # [1., 1.]
    beta_hat = np.array([1.,1.]) # For y = 1 + 1*x, exact fit for first 3 points of y = x+1
    
    # For y = [1,2,3,4,5] and X0=[1,1,1,1,1], X1=[0,1,2,3,4]
    # if beta = [1,1], y_hat = [1,2,3,4,5]. SSR = 0
    
    # Let's use y = x + 1 + noise
    y_noisy = X @ beta_hat + np.array([0.1, -0.1, 0.05, -0.02, 0.15])
    # y_noisy = [1.1, 1.9, 3.05, 3.98, 5.15]
    
    # Using statsmodels directly to get expected SSR
    import statsmodels.api as sm
    model = sm.OLS(y_noisy, X).fit()
    expected_rss = model.ssr
    
    calculated_rss = _calculate_rss(y_noisy, X)
    assert np.isclose(calculated_rss, expected_rss)

def test_calculate_rss_insufficient_data():
    """Test _calculate_rss when N < K."""
    y = np.array([1, 2], dtype=float)
    X = np.column_stack((np.ones(2), np.arange(2, dtype=float), np.arange(2, dtype=float)**2)) # N=2, K=3
    with pytest.raises(np.linalg.LinAlgError): # Or the specific error from OLS
        _calculate_rss(y, X)

def test_calculate_rss_perfect_collinearity():
    """Test _calculate_rss with perfect multicollinearity."""
    y = np.array([1, 2, 3, 4, 5], dtype=float)
    X = np.column_stack((np.ones(5), np.arange(5, dtype=float), np.arange(5, dtype=float)*2)) # X2 = 2*X1
    try:
        rss = _calculate_rss(y, X)
        assert isinstance(rss, float) 
        # Optionally, you could check if it's very small if y can be perfectly explained
        # For this specific y and X, SSR should be near zero.
        assert np.isclose(rss, 0, atol=1e-9) 
    except np.linalg.LinAlgError:
        pytest.fail("np.linalg.LinAlgError was raised unexpectedly by _calculate_rss")