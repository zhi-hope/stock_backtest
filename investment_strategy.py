"""
定投策略模块
"""
import pandas as pd
from typing import Dict, List
from datetime import datetime, timedelta
import pytz

def weekly_investment_dates(start_date: str, end_date: str, day_of_week: int = 0) -> List[datetime]:
    """
    生成每周定投日期列表
    
    Args:
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        day_of_week: 周几定投 (0=周一, 1=周二, ..., 6=周日)
        
    Returns:
        定投日期列表
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    # 调整到第一个定投日
    days_ahead = day_of_week - start.weekday()
    if days_ahead < 0:  # Target day already happened this week
        days_ahead += 7
    first_investment_date = start + timedelta(days=days_ahead)
    
    # 生成每周指定日的日期
    dates = []
    current = first_investment_date
    while current <= end:
        dates.append(current)
        current += timedelta(weeks=1)
    
    return dates

def monthly_investment_dates(start_date: str, end_date: str, day_of_month: int = 1) -> List[datetime]:
    """
    生成每月定投日期列表
    
    Args:
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        day_of_month: 每月几号定投 (1-31)
        
    Returns:
        定投日期列表
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    dates = []
    # 从开始日期的年份和月份开始
    year = start.year
    month = start.month

    while True:
        # 构造当前循环月份的定投日期
        current_date_to_try = datetime(year, month, 1)
        if current_date_to_try > end:
            break

        try:
            # 尝试创建指定日的日期
            invest_date = datetime(year, month, day_of_month)
            # 只有当定投日在回测范围内时才添加
            if start <= invest_date <= end:
                dates.append(invest_date)
        except ValueError:
            # 如果日期无效 (例如2月31日)，则静默跳过这个月
            pass

        # 移至下一个月
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
            
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