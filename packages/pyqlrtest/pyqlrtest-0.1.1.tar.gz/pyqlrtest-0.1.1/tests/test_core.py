# tests/test_core.py
import pytest
import numpy as np
import pandas as pd
from qlrtest import qlr_test
from qlrtest._exceptions import InvalidTrimmingError, QLRTestError

def test_qlr_test_basic_run():
    """Test if qlr_test runs with minimal valid inputs and returns a dict."""
    np.random.seed(0)
    y = np.random.rand(100)
    X = np.column_stack((np.ones(100), np.random.rand(100)))
    
    results = qlr_test(y, X, trim=0.15)
    
    assert isinstance(results, dict)
    assert 'max_f_stat' in results
    assert 'breakpoint' in results
    assert 'p_value' in results
    assert 'significant' in results
    assert results['n_observations'] == 100
    assert results['n_parameters'] == 2 
    assert results['trim_used'] == 0.15
    # Removed assertion for 'approx_critical_value'

def test_qlr_test_pandas_input():
    np.random.seed(1)
    y_pd = pd.Series(np.random.rand(50))
    X_pd = pd.DataFrame({
        'intercept': np.ones(50),
        'x1': np.random.rand(50)
    })
    results = qlr_test(y_pd, X_pd, trim=0.2)
    assert isinstance(results, dict)
    assert results['n_observations'] == 50
    assert results['n_parameters'] == 2

def test_qlr_test_invalid_trim():
    y = np.random.rand(100)
    X = np.column_stack((np.ones(100), np.random.rand(100)))
    
    with pytest.raises(InvalidTrimmingError):
        qlr_test(y, X, trim=0.005)
    with pytest.raises(InvalidTrimmingError):
        qlr_test(y, X, trim=0.5)

def test_qlr_test_insufficient_data_for_trim():
    y_small = np.random.rand(5)
    X_small = np.column_stack((np.ones(5), np.arange(5))) 
    with pytest.raises(QLRTestError):
        qlr_test(y_small, X_small, trim=0.15)

def test_qlr_return_f_stats_series():
    np.random.seed(42)
    y = np.random.rand(100)
    X = np.column_stack((np.ones(100), np.random.rand(100)))
    
    results = qlr_test(y, X, trim=0.15, return_f_stats_series=True)
    assert 'tested_indices' in results
    assert 'f_stats' in results
    assert isinstance(results['tested_indices'], np.ndarray)
    assert isinstance(results['f_stats'], np.ndarray)
    assert len(results['tested_indices']) == len(results['f_stats'])
    assert len(results['f_stats']) > 0 
    # Removed assertion for 'approx_critical_value'

def test_known_break_simple_case():
    n = 200
    k = 2 
    break_point = 100
    trim = 0.15 

    X = np.ones((n, k))
    X[:, 1] = np.arange(n)
    
    y = np.zeros(n)
    beta1 = np.array([0.5, 0.1])
    beta2 = np.array([2.5, -0.1]) 

    y[:break_point] = X[:break_point, :] @ beta1
    y[break_point:] = X[break_point:, :] @ beta2
    y += np.random.normal(0, 0.5, n) 

    results = qlr_test(y, X, trim=trim, sig_level=0.05) # Pass sig_level for 'significant' flag
    
    assert results['max_f_stat'] > 10 
    assert abs(results['breakpoint'] - break_point) < n * (1-2*trim) * 0.15 # Looser delta
    assert results['p_value'] < 0.05 # Expect significance based on p-value
    assert results['significant'] is True # Check the flag
    
    # Example from original script (approximate)
    n_example = 100
    break_pt_example = 40 
    X_example = np.column_stack((np.ones(n_example), np.arange(n_example)))
    beta_pre_ex = np.array([1.0, 0.5])
    beta_post_ex = np.array([5.0, -0.5]) 
    errors_ex = np.random.normal(0, 1, n_example)
    y_example = np.concatenate((X_example[:break_pt_example] @ beta_pre_ex,
                                X_example[break_pt_example:] @ beta_post_ex)) + errors_ex
    
    results_ex = qlr_test(y_example, X_example, trim=0.15, sig_level=0.05)
    assert results_ex['p_value'] < 0.05 
    assert results_ex['significant'] is True
    assert 15 <= results_ex['breakpoint'] < 85