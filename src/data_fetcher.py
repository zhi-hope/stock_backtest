"""
数据获取模块
"""
import yfinance as yf
import pandas as pd
from typing import Optional, List, Dict
import warnings
warnings.filterwarnings('ignore')

def get_stock_data(symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    获取股票数据
    
    Args:
        symbol: 股票代码 (如 'AAPL')
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        
    Returns:
        包含股票数据的DataFrame
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
        info = stock.info
        return info
    except Exception as e:
        print(f"获取 {symbol} 信息时出错: {e}")
        return {}

def get_multiple_stocks_data(symbols: List[str], start_date: str, end_date: str) -> Dict:
    """
    获取多个股票的数据
    
    Args:
        symbols: 股票代码列表
        start_date: 开始日期
        end_date: 结束日期
        
    Returns:
        股票数据字典
    """
    data_dict = {}
    for symbol in symbols:
        data = get_stock_data(symbol, start_date, end_date)
        if data is not None:
            data_dict[symbol] = data
    return data_dict