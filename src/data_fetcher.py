"""
数据获取模块
"""
import yfinance as yf
import pandas as pd
from typing import Dict, Optional

def get_stock_data(symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    获取股票历史数据
    
    Args:
        symbol: 股票代码
        start_date: 开始日期
        end_date: 结束日期
        
    Returns:
        包含股票数据的Pandas DataFrame，如果失败则返回None
    """
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)
        if data.empty:
            print(f"未能获取 {symbol} 在 {start_date} 到 {end_date} 之间的数据")
            return None
        return data
    except Exception as e:
        print(f"获取 {symbol} 数据时出错: {e}")
        return None

def get_stock_info(symbol: str) -> Dict:
    """
    获取股票基本信息
    
    Args:
        symbol: 股票代码
        
    Returns:
        包含股票信息的字典
    """
    try:
        stock = yf.Ticker(symbol)
        return stock.info
    except Exception as e:
        print(f"获取 {symbol} 信息时出错: {e}")
        return {}
