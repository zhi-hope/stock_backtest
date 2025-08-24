"""
可视化模块
"""
import pandas as pd
import matplotlib.pyplot as plt
<<<<<<< HEAD
import matplotlib.dates as mdates
from typing import Dict
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体以支持中文显示
import matplotlib.font_manager as fm

# 查找可用的中文字体
available_fonts = []
font_names = ['WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'Droid Sans Fallback', 'DejaVu Sans']
for font_name in font_names:
    try:
        if fm.findfont(fm.FontProperties(family=font_name), fallback_to_default=False):
            available_fonts.append(font_name)
    except:
        continue

# 设置字体
if available_fonts:
    plt.rcParams['font.sans-serif'] = available_fonts
else:
    # 如果没有找到中文字体，使用默认字体并设置字体回退
    plt.rcParams['font.sans-serif'] = ['sans-serif']

plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 设置全局字体属性
plt.rcParams['font.family'] = 'sans-serif'

# 禁用数学模式的默认字体，使用自定义设置
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = available_fonts[0] if available_fonts else 'sans-serif'
plt.rcParams['mathtext.bf'] = available_fonts[0] if available_fonts else 'sans-serif:bold'
plt.rcParams['mathtext.it'] = available_fonts[0] if available_fonts else 'sans-serif:italic'
plt.rcParams['mathtext.cal'] = available_fonts[0] if available_fonts else 'sans-serif'

def plot_investment_growth(backtest_result: Dict, symbol: str = "Stock", ax=None):
    """
    绘制定投增长图表
    
    Args:
        backtest_result: 回测结果
        symbol: 股票代码
        ax: 可选的axes对象，如果提供则在该axes上绘制
    """
    if not backtest_result or 'investment_records' not in backtest_result:
        print("无效的回测结果")
        return
    
    records = backtest_result['investment_records']
    
    # 如果没有提供ax，则创建新的图表
    if ax is None:
        fig, ax1 = plt.subplots(figsize=(12, 8))
    else:
        ax1 = ax
        fig = ax1.figure
    
    # 设置中文字体属性
    chinese_font = fm.FontProperties(family=plt.rcParams['font.sans-serif'][0] if plt.rcParams['font.sans-serif'] else None)
    
    # 绘制累计投资金额和投资价值
    ax1.plot(records['Date'], records['Cumulative_Amount'], 
             label='累计投资金额', color='blue', linewidth=2)
    
    # 计算投资价值
    investment_value = records['Cumulative_Shares'] * records['Price']
    ax1.plot(records['Date'], investment_value, 
             label='投资价值', color='green', linewidth=2)
    
    # 只在创建新图表时设置标签、标题等
    if ax is None:
        ax1.set_xlabel('日期', fontproperties=chinese_font)
        ax1.set_ylabel('金额 ($)', color='blue', fontproperties=chinese_font)
        ax1.tick_params(axis='y', labelcolor='blue')
        
        # 设置刻度标签字体
        for label in ax1.get_xticklabels():
            label.set_fontproperties(chinese_font)
        for label in ax1.get_yticklabels():
            label.set_fontproperties(chinese_font)
        
        # 格式化日期
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, fontproperties=chinese_font)
        
        # 添加图例
        legend = ax1.legend(loc='upper left')
        for text in legend.get_texts():
            text.set_fontproperties(chinese_font)
        
        # 添加标题和网格
        plt.title(f'{symbol} 定投回测结果\n'
                  f'总投入: ${backtest_result["total_investment"]:.2f} | '
                  f'最终价值: ${backtest_result["final_value"]:.2f} | '
                  f'总收益率: {backtest_result["total_return"]:.2f}% | '
                  f'年化收益率: {backtest_result["annual_return"]:.2f}%', 
                  fontproperties=chinese_font)
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
    else:
        # 在提供的axes上设置基本属性
        ax1.set_xlabel('日期', fontproperties=chinese_font)
        ax1.set_ylabel('金额 ($)', color='blue', fontproperties=chinese_font)
        ax1.tick_params(axis='y', labelcolor='blue')
        
        # 添加图例
        legend = ax1.legend(loc='upper left')
        for text in legend.get_texts():
            text.set_fontproperties(chinese_font)
    
    return fig

def plot_price_vs_investment(stock_data: pd.DataFrame, backtest_result: Dict, symbol: str = "Stock", ax=None):
    """
    绘制股价与定投点对比图
    
    Args:
        stock_data: 股票数据
        backtest_result: 回测结果
        symbol: 股票代码
        ax: 可选的axes对象，如果提供则在该axes上绘制
    """
    if not backtest_result or 'investment_records' not in backtest_result:
        print("无效的回测结果")
        return
    
    records = backtest_result['investment_records']
    
    # 如果没有提供ax，则创建新的图表
    if ax is None:
        fig, ax1 = plt.subplots(figsize=(12, 8))
    else:
        ax1 = ax
        fig = ax1.figure
    
    # 设置中文字体属性
    chinese_font = fm.FontProperties(family=plt.rcParams['font.sans-serif'][0] if plt.rcParams['font.sans-serif'] else None)
    
    # 绘制股价
    ax1.plot(stock_data.index, stock_data['Close'], 
             label=f'{symbol} 股价', color='blue', linewidth=1)
    
    # 绘制定投点
    ax1.scatter(records['Date'], records['Price'], 
                color='red', s=50, label='定投点', zorder=5)
    
    # 只在创建新图表时设置标签、标题等
    if ax is None:
        ax1.set_xlabel('日期', fontproperties=chinese_font)
        ax1.set_ylabel('股价 ($)', color='blue', fontproperties=chinese_font)
        ax1.tick_params(axis='y', labelcolor='blue')
        
        # 设置刻度标签字体
        for label in ax1.get_xticklabels():
            label.set_fontproperties(chinese_font)
        for label in ax1.get_yticklabels():
            label.set_fontproperties(chinese_font)
        
        # 格式化日期
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, fontproperties=chinese_font)
        
        # 添加图例
        legend = ax1.legend(loc='upper left')
        for text in legend.get_texts():
            text.set_fontproperties(chinese_font)
        
        # 添加标题和网格
        plt.title(f'{symbol} 股价与定投点对比', 
                  fontproperties=chinese_font)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
    else:
        # 在提供的axes上设置基本属性
        ax1.set_xlabel('日期', fontproperties=chinese_font)
        ax1.set_ylabel('股价 ($)', color='blue', fontproperties=chinese_font)
        ax1.tick_params(axis='y', labelcolor='blue')
        
        # 添加图例
        legend = ax1.legend(loc='upper left')
        for text in legend.get_texts():
            text.set_fontproperties(chinese_font)
    
    return fig
=======
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
>>>>>>> 01d697f523f9ce5ed55ce9a16362a882cf7c3381
