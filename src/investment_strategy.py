"""
投资策略模块
"""
import pandas as pd
from typing import List

def weekly_investment_dates(start_date: str, end_date: str, day_of_week: int = 0) -> List[pd.Timestamp]:
    """
    生成每周固定的投资日期列表 (0=Monday, 6=Sunday)
    """
    dates = pd.date_range(start=start_date, end=end_date, freq=f'W-MON')
    return [d.to_pydatetime() for d in dates]

def monthly_investment_dates(start_date: str, end_date: str, day_of_month: int = 1) -> List[pd.Timestamp]:
    """
    生成每月固定的投资日期列表
    """
    dates = pd.date_range(start=start_date, end=end_date, freq='MS')
    # Adjust day of month
    return [d.replace(day=day_of_month).to_pydatetime() for d in dates]

def calculate_investment_shares(stock_data: pd.DataFrame, investment_dates: List[pd.Timestamp], amount: float) -> pd.DataFrame:
    """
    计算每次定投的股份
    """
    records = []
    for date in investment_dates:
        price = stock_data[stock_data.index <= date]['Close'].iloc[-1]
        shares = amount / price
        records.append({'Date': date, 'Price': price, 'Amount': amount, 'Shares': shares})
    return pd.DataFrame(records).set_index('Date')
