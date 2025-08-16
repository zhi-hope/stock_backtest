"""
定投策略模块
"""
import pandas as pd
from typing import Dict, List
from datetime import datetime, timedelta
import pytz

def weekly_investment_dates(start_date: str, end_date: str) -> List[datetime]:
    """
    生成每周定投日期列表
    
    Args:
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        
    Returns:
        定投日期列表
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    # 调整到最近的周一
    days_ahead = 0 - start.weekday()  # Monday is 0
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    first_monday = start + timedelta(days_ahead)
    
    # 生成每周一的日期
    dates = []
    current = first_monday
    while current <= end:
        dates.append(current)
        current += timedelta(weeks=1)
    
    return dates

def monthly_investment_dates(start_date: str, end_date: str) -> List[datetime]:
    """
    生成每月定投日期列表（每月第一个交易日）
    
    Args:
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        
    Returns:
        定投日期列表
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    dates = []
    current_year = start.year
    current_month = start.month
    
    while True:
        # 生成每月第一天
        try:
            first_day = datetime(current_year, current_month, 1)
        except ValueError:
            # 处理月份溢出情况
            break
            
        # 如果超过结束日期则退出
        if first_day > end:
            break
            
        # 添加到日期列表
        dates.append(first_day)
        
        # 移动到下一个月
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
    
    return dates

def calculate_investment_shares(stock_data: pd.DataFrame, investment_dates: List[datetime], 
                               weekly_amount: float) -> pd.DataFrame:
    """
    计算每次定投的股份数量
    
    Args:
        stock_data: 股票数据
        investment_dates: 定投日期列表
        weekly_amount: 每周定投金额
        
    Returns:
        包含定投记录的DataFrame
    """
    investment_records = []
    
    # 获取股票数据的时区信息
    if hasattr(stock_data.index, 'tz') and stock_data.index.tz is not None:
        stock_tz = stock_data.index.tz
    else:
        stock_tz = None
    
    for date in investment_dates:
        # 如果股票数据有时区信息，将日期转换为相同时区
        if stock_tz is not None:
            if date.tzinfo is None:
                # 如果日期没有时区信息，使用股票数据的时区
                date = stock_tz.localize(date)
            else:
                # 如果日期有时区信息，转换为股票数据的时区
                date = date.astimezone(stock_tz)
        
        # 找到最接近的交易日
        if date in stock_data.index:
            price = stock_data.loc[date, 'Close']
        else:
            # 如果当天不是交易日，找到下一个交易日
            try:
                future_dates = stock_data[stock_data.index >= date]
                if future_dates.empty:
                    continue
                next_trading_day = future_dates.index[0]
                price = stock_data.loc[next_trading_day, 'Close']
                date = next_trading_day
            except Exception:
                # 如果比较失败，尝试使用iloc方法找到最近的日期
                try:
                    # 找到最接近的索引位置
                    date_index = stock_data.index.get_indexer([date], method='bfill')[0]
                    if date_index == -1:
                        # 如果没有找到后续日期，使用前向填充
                        date_index = stock_data.index.get_indexer([date], method='ffill')[0]
                    if date_index != -1:
                        next_trading_day = stock_data.index[date_index]
                        price = stock_data.loc[next_trading_day, 'Close']
                        date = next_trading_day
                    else:
                        continue
                except Exception:
                    continue
            
        shares = weekly_amount / price
        investment_records.append({
            'Date': date,
            'Price': price,
            'Amount': weekly_amount,
            'Shares': shares
        })
    
    return pd.DataFrame(investment_records)