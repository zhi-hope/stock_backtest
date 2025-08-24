"""
Test for investment_strategy.py
"""
import pytest
from datetime import datetime

from src.investment_strategy import weekly_investment_dates, monthly_investment_dates

def test_weekly_investment_dates():
    # Test case 1: Default (Monday)
    dates = weekly_investment_dates('2023-01-01', '2023-01-20')
    expected = [
        datetime(2023, 1, 2),
        datetime(2023, 1, 9),
        datetime(2023, 1, 16)
    ]
    assert dates == expected

    # Test case 2: Wednesday (day_of_week=2)
    dates = weekly_investment_dates('2023-01-01', '2023-01-20', day_of_week=2)
    expected = [
        datetime(2023, 1, 4),
        datetime(2023, 1, 11),
        datetime(2023, 1, 18)
    ]
    assert dates == expected

def test_monthly_investment_dates():
    # Test case 1: Default (1st of month)
    dates = monthly_investment_dates('2023-01-01', '2023-03-15')
    expected = [
        datetime(2023, 1, 1),
        datetime(2023, 2, 1),
        datetime(2023, 3, 1)
    ]
    assert dates == expected

    # Test case 2: 15th of month
    dates = monthly_investment_dates('2023-01-01', '2023-03-15', day_of_month=15)
    expected = [
        datetime(2023, 1, 15),
        datetime(2023, 2, 15),
        datetime(2023, 3, 15)
    ]
    assert dates == expected

    # Test case 3: Edge case (31st) - should skip months without 31 days
    dates = monthly_investment_dates('2023-01-01', '2023-05-01', day_of_month=31)
    expected = [
        datetime(2023, 1, 31),
        datetime(2023, 3, 31),
    ]
    assert dates == expected
