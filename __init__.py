"""
美股股票每周定投回测程序
"""
__version__ = "1.0.0"
__author__ = "Claude Code"

from .main import StockDripBacktester
from .data_fetcher import get_stock_data, get_multiple_stocks_data
from .backtest import run_backtest, compare_with_lump_sum
from .investment_strategy import weekly_investment_dates, calculate_investment_shares
from .visualization import plot_investment_growth, plot_price_vs_investment

__all__ = [
    'StockDripBacktester',
    'get_stock_data',
    'get_multiple_stocks_data',
    'run_backtest',
    'compare_with_lump_sum',
    'weekly_investment_dates',
    'calculate_investment_shares',
    'plot_investment_growth',
    'plot_price_vs_investment'
]