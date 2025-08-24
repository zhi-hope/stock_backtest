"""
可视化模块
"""
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict

def plot_investment_growth(result: Dict, symbol: str):
    """
    绘制投资增长图
    """
    if 'investment_records' not in result:
        return None

    records = result['investment_records']
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(records.index, records['Cumulative_Amount'], label='总投入', color='orange')
    ax.plot(records.index, records['Cumulative_Shares'] * records['Price'], label='总价值', color='blue')
    
    ax.set_title(f'{symbol} 定投增长曲线')
    ax.set_xlabel('日期')
    ax.set_ylabel('金额 ($)')
    ax.legend()
    ax.grid(True)
    
    return fig

def plot_price_vs_investment(stock_data: pd.DataFrame, result: Dict, symbol: str):
    """
    绘制股价与定投点对比图
    """
    if 'investment_records' not in result:
        return None

    records = result['investment_records']
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(stock_data.index, stock_data['Close'], label='股价', color='gray', alpha=0.7)
    ax.scatter(records.index, records['Price'], label='定投点', color='red', marker='v')
    
    ax.set_title(f'{symbol} 股价与定投点')
    ax.set_xlabel('日期')
    ax.set_ylabel('价格 ($)')
    ax.legend()
    ax.grid(True)

    return fig
