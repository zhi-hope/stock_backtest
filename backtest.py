"""
回测计算模块
"""
import pandas as pd
import numpy as np
from typing import Dict, List
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def run_backtest(stock_data: pd.DataFrame, amount: float, 
                start_date: str, end_date: str, strategy: str = 'weekly') -> Dict:
    """
    运行定投回测
    
    Args:
        stock_data: 股票数据
        amount: 每期定投金额
        start_date: 开始日期
        end_date: 结束日期
        strategy: 定投策略 ('weekly' 或 'monthly')
        
    Returns:
        回测结果字典
    """
    from investment_strategy import weekly_investment_dates, monthly_investment_dates, calculate_investment_shares
    
    # 生成定投日期
    if strategy == 'monthly':
        investment_dates = monthly_investment_dates(start_date, end_date)
    else:
        investment_dates = weekly_investment_dates(start_date, end_date)
    
    # 计算每次定投的股份数量
    investment_records = calculate_investment_shares(stock_data, investment_dates, amount)
    
    if investment_records.empty:
        return {}
    
    # 计算累计股份数和投资金额
    investment_records['Cumulative_Shares'] = investment_records['Shares'].cumsum()
    investment_records['Cumulative_Amount'] = investment_records['Amount'].cumsum()
    
    # 获取最终股价
    final_date = investment_records['Date'].max()
    if final_date in stock_data.index:
        final_price = stock_data.loc[final_date, 'Close']
    else:
        # 获取最接近的交易日价格
        past_dates = stock_data[stock_data.index <= final_date]
        if not past_dates.empty:
            final_price = stock_data.loc[past_dates.index[-1], 'Close']
        else:
            final_price = stock_data['Close'].iloc[-1]
    
    # 计算最终价值
    final_value = investment_records['Cumulative_Shares'].iloc[-1] * final_price
    
    # 计算总投入
    total_investment = investment_records['Cumulative_Amount'].iloc[-1]
    
    # 计算收益率
    total_return = (final_value - total_investment) / total_investment * 100
    
    # 计算年化收益率
    years = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days / 365.25
    annual_return = (final_value / total_investment) ** (1/years) - 1
    annual_return_percent = annual_return * 100
    
    return {
        'total_investment': total_investment,
        'final_value': final_value,
        'total_return': total_return,
        'annual_return': annual_return_percent,
        'investment_records': investment_records,
        'final_price': final_price,
        'investment_count': len(investment_records)
    }

def compare_with_lump_sum(stock_data: pd.DataFrame, amount: float,
                         start_date: str, end_date: str, strategy: str = 'weekly') -> Dict:
    """
    与一次性投资进行比较
    
    Args:
        stock_data: 股票数据
        amount: 每期定投金额
        start_date: 开始日期
        end_date: 结束日期
        strategy: 定投策略 ('weekly' 或 'monthly')
        
    Returns:
        比较结果字典
    """
    # 定投结果
    drip_result = run_backtest(stock_data, amount, start_date, end_date, strategy)
    
    if not drip_result:
        return {}
    
    # 一次性投资结果
    start_prices = stock_data[stock_data.index >= start_date]
    if start_prices.empty:
        return drip_result
    
    initial_price = start_prices['Close'].iloc[0]
    lump_sum_shares = drip_result['total_investment'] / initial_price
    
    final_date = drip_result['investment_records']['Date'].max()
    if final_date in stock_data.index:
        final_price = stock_data.loc[final_date, 'Close']
    else:
        past_dates = stock_data[stock_data.index <= final_date]
        if not past_dates.empty:
            final_price = stock_data.loc[past_dates.index[-1], 'Close']
        else:
            final_price = stock_data['Close'].iloc[-1]
    
    lump_sum_value = lump_sum_shares * final_price
    lump_sum_return = (lump_sum_value - drip_result['total_investment']) / drip_result['total_investment'] * 100
    
    return {
        'drip_result': drip_result,
        'lump_sum_value': lump_sum_value,
        'lump_sum_return': lump_sum_return,
        'difference': drip_result['total_return'] - lump_sum_return
    }