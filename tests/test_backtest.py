"""
Test for backtest.py
"""
import pytest
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backtest import run_backtest, _get_price_on_or_near

@pytest.fixture
def sample_stock_data():
    """Create a sample stock data DataFrame for testing."""
    dates = pd.to_datetime([
        '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06',
        '2023-01-09', '2023-01-10', '2023-01-11', '2023-01-12', '2023-01-13'
    ])
    data = {'Close': [100, 102, 105, 103, 106, 110, 108, 112, 115, 114]}
    df = pd.DataFrame(data, index=dates)
    return df

def test_get_price_on_or_near(sample_stock_data):
    # Test exact date
    price = _get_price_on_or_near(pd.to_datetime('2023-01-04'), sample_stock_data)
    assert price == 105

    # Test non-trading day (weekend), should get previous day
    price = _get_price_on_or_near(pd.to_datetime('2023-01-08'), sample_stock_data)
    assert price == 106 # Price of Jan 6th

    # Test date before any data
    price = _get_price_on_or_near(pd.to_datetime('2022-12-31'), sample_stock_data)
    assert np.isnan(price)

def test_run_backtest(sample_stock_data):
    start_date = '2023-01-01'
    end_date = '2023-01-13'
    amount = 100

    # Weekly investment on Mondays (Jan 2, Jan 9)
    result = run_backtest(sample_stock_data, amount, start_date, end_date, strategy='weekly', strategy_params={'day_of_week': 0})

    # Manually calculate expected result
    # Investment 1 (Jan 2): 100 / 100 = 1 share
    # Investment 2 (Jan 9): 100 / 110 = 0.90909 shares
    total_shares = 1 + (100 / 110)
    total_investment = 200
    final_price = 114 # Price on Jan 13
    final_value = total_shares * final_price

    assert result['total_investment'] == pytest.approx(total_investment)
    assert result['final_value'] == pytest.approx(final_value)
    assert result['investment_count'] == 2
    assert result['total_return'] == pytest.approx(((final_value - total_investment) / total_investment) * 100)
