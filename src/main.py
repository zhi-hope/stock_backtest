"""
主程序模块
"""
import pandas as pd
from typing import List, Dict, Optional
import warnings
import sys
import os
warnings.filterwarnings('ignore')

# 将当前目录添加到Python路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import get_stock_data, get_stock_info
from backtest import run_backtest, compare_with_lump_sum
from visualization import plot_investment_growth, plot_price_vs_investment

class StockDripBacktester:
    """美股股票定投回测器"""
    
    def __init__(self):
        self.stock_data = None
        self.symbol = ""
        
    def load_data(self, symbol: str, start_date: str, end_date: str) -> bool:
        """
        加载股票数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            是否成功加载数据
        """
        self.symbol = symbol
        self.stock_data = get_stock_data(symbol, start_date, end_date)
        
        if self.stock_data is None or self.stock_data.empty:
            print(f"未能加载 {symbol} 的数据")
            return False
            
        # 检查是否有可用的股票信息来获取成立日期
        stock_info = get_stock_info(symbol)
        actual_start_date = start_date
        
        # 尝试获取基金的成立日期
        if 'fundInceptionDate' in stock_info and stock_info['fundInceptionDate']:
            # 处理Unix时间戳格式的基金成立日期
            if isinstance(stock_info['fundInceptionDate'], (int, float)):
                fund_start_dt = pd.to_datetime(stock_info['fundInceptionDate'], unit='s')
            else:
                fund_start_dt = pd.to_datetime(stock_info['fundInceptionDate'])
            fund_start = fund_start_dt.strftime('%Y-%m-%d')
            
            # 检查基金成立日期是否晚于用户设置的开始日期
            if fund_start > start_date:
                print(f"注意: {symbol} 成立于 {fund_start}，晚于您设置的开始日期 {start_date}")
                print(f"将自动调整回测开始日期为基金成立日 {fund_start}")
                actual_start_date = fund_start
            else:
                # 基金成立日期早于或等于用户设置的开始日期，使用用户设置的日期
                actual_start_date = start_date
        elif 'startDate' in stock_info and stock_info['startDate']:
            fund_start = pd.to_datetime(stock_info['startDate']).strftime('%Y-%m-%d')
            if fund_start > start_date:
                print(f"注意: {symbol} 数据始于 {fund_start}，晚于您设置的开始日期 {start_date}")
                print(f"将自动调整回测开始日期为数据起始日 {fund_start}")
                actual_start_date = fund_start
        
        # 如果调整了开始日期，重新获取数据
        if actual_start_date != start_date:
            print(f"重新加载 {symbol} 从 {actual_start_date} 到 {end_date} 的数据...")
            self.stock_data = get_stock_data(symbol, actual_start_date, end_date)
            if self.stock_data is None or self.stock_data.empty:
                print(f"重新加载 {symbol} 数据失败")
                return False
        
        print(f"成功加载 {symbol} 从 {actual_start_date} 到 {end_date} 的数据")
        print(f"数据范围: {self.stock_data.index[0].date()} 到 {self.stock_data.index[-1].date()}")
        return True
    
    def run_backtest(self, amount: float, start_date: str, end_date: str, 
                    compare: bool = False, strategy: str = 'weekly', strategy_params: Optional[Dict] = None) -> Optional[Dict]:
        """
        运行定投回测
        
        Args:
            amount: 每期定投金额
            start_date: 回测开始日期
            end_date: 回测结束日期
            compare: 是否与一次性投资比较
            strategy: 定投策略 ('weekly' 或 'monthly')
            strategy_params: 策略参数 (例如 {'day_of_week': 0})

        Returns:
            回测结果
        """
        if self.stock_data is None:
            print("请先加载股票数据")
            return None
            
        # 使用实际数据的起始日期作为回测开始日期
        actual_start_date = self.stock_data.index[0].strftime('%Y-%m-%d')
        print(f"使用实际数据起始日期 {actual_start_date} 进行回测")
        
        if compare:
            result = compare_with_lump_sum(self.stock_data, amount, actual_start_date, end_date, strategy, strategy_params)
        else:
            result = run_backtest(self.stock_data, amount, actual_start_date, end_date, strategy, strategy_params)
            
        return result
    
    def print_results(self, result: Dict, compare: bool = False, strategy: str = 'weekly'):
        """
        打印回测结果
        
        Args:
            result: 回测结果
            compare: 是否包含比较结果
            strategy: 定投策略 ('weekly' 或 'monthly')
        """
        if not result:
            print("回测结果为空")
            return
            
        # 根据策略确定显示的周期单位
        period_unit = "月" if strategy == 'monthly' else "周"
        
        if compare and 'drip_result' in result:
            drip_result = result['drip_result']
            print(f"\n=== {self.symbol} 定投回测结果 ===")
            print(f"定投周期: {drip_result['investment_count']} {period_unit}")
            amount_label = "每月定投金额" if strategy == 'monthly' else "每周定投金额"
            print(f"{amount_label}: ${drip_result['investment_records']['Amount'].iloc[0]:.2f}")
            print(f"总投入金额: ${drip_result['total_investment']:.2f}")
            print(f"最终价值: ${drip_result['final_value']:.2f}")
            print(f"最终股价: ${drip_result['final_price']:.2f}")
            print(f"总收益率: {drip_result['total_return']:.2f}%")
            print(f"年化收益率: {drip_result['annual_return']:.2f}%")
            
            print(f"\n=== 一次性投资比较 ===")
            print(f"一次性投资价值: ${result['lump_sum_value']:.2f}")
            print(f"一次性投资收益率: {result['lump_sum_return']:.2f}%")
            print(f"定投相比一次性投资差异: {result['difference']:.2f}%")
            
            if result['difference'] > 0:
                print("定投策略表现更好")
            else:
                print("一次性投资表现更好")
        elif 'total_investment' in result:
            print(f"\n=== {self.symbol} 定投回测结果 ===")
            print(f"定投周期: {result['investment_count']} {period_unit}")
            amount_label = "每月定投金额" if strategy == 'monthly' else "每周定投金额"
            print(f"{amount_label}: ${result['investment_records']['Amount'].iloc[0]:.2f}")
            print(f"总投入金额: ${result['total_investment']:.2f}")
            print(f"最终价值: ${result['final_value']:.2f}")
            print(f"最终股价: ${result['final_price']:.2f}")
            print(f"总收益率: {result['total_return']:.2f}%")
            print(f"年化收益率: {result['annual_return']:.2f}%")
    
    def plot_results(self, result: Dict):
        """
        绘制回测结果图表
        
        Args:
            result: 回测结果
        """
        if not result:
            print("回测结果为空，无法绘图")
            return
            
        # 导入matplotlib但不显示图表
        import matplotlib
        matplotlib.use('Agg')  # 使用非交互式后端
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'Droid Sans Fallback']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.family'] = 'sans-serif'
        
        # 禁用数学模式的默认字体，使用自定义设置
        plt.rcParams['mathtext.fontset'] = 'custom'
        plt.rcParams['mathtext.rm'] = 'WenQuanYi Zen Hei'
        plt.rcParams['mathtext.bf'] = 'WenQuanYi Zen Hei:bold'
        plt.rcParams['mathtext.it'] = 'WenQuanYi Zen Hei:italic'
        plt.rcParams['mathtext.cal'] = 'WenQuanYi Zen Hei'
        
        try:
            # 绘制定投增长图
            fig1 = plot_investment_growth(result, self.symbol)
            if fig1:
                fig1.savefig(f'{self.symbol}_investment_growth.png', dpi=300, bbox_inches='tight')
                print(f"定投增长图已保存为 {self.symbol}_investment_growth.png")
                plt.close(fig1)
            
            # 绘制股价与定投点对比图
            if 'investment_records' in result:
                fig2 = plot_price_vs_investment(self.stock_data, result, self.symbol)
                if fig2:
                    fig2.savefig(f'{self.symbol}_price_investment.png', dpi=300, bbox_inches='tight')
                    print(f"股价与定投点对比图已保存为 {self.symbol}_price_investment.png")
                    plt.close(fig2)
        except Exception as e:
            print(f"绘图时出错: {e}")

def main():
    """主函数 - 支持用户输入股票代码、时间范围和定投策略"""
    # 创建回测器实例
    backtester = StockDripBacktester()
    
    # 获取用户输入
    print("=== 美股股票定投回测器 ===")
    symbol = input("请输入股票代码 (例如: AAPL): ").strip().upper()
    if not symbol:
        symbol = "AAPL"  # 默认使用苹果公司
    
    start_date = input("请输入开始日期 (YYYY-MM-DD, 例如: 2020-01-01): ").strip()
    if not start_date:
        start_date = "2020-01-01"  # 默认开始日期
    
    end_date = input("请输入结束日期 (YYYY-MM-DD, 例如: 2023-12-31): ").strip()
    if not end_date:
        end_date = "2023-12-31"  # 默认结束日期
    
    # 选择定投策略
    print("\n请选择定投策略:")
    print("1. 每周定投")
    print("2. 每月定投")
    strategy_choice = input("请输入选择 (1 或 2, 默认为 1): ").strip()
    strategy = 'monthly' if strategy_choice == '2' else 'weekly'
    strategy_params = {}

    # 获取策略参数
    if strategy == 'weekly':
        day_map = {"0": "周一", "1": "周二", "2": "周三", "3": "周四", "4": "周五", "5": "周六", "6": "周日"}
        day_of_week_input = input("请输入每周定投的日期 (0-6, 0是周一, 默认为0): ").strip()
        try:
            day_of_week = int(day_of_week_input) if day_of_week_input else 0
            if 0 <= day_of_week <= 6:
                strategy_params['day_of_week'] = day_of_week
                print(f"已选择每周的 {day_map[str(day_of_week)]} 进行定投ảng。")
            else:
                print("输入无效，使用默认的周一进行定投。")
        except ValueError:
            print("输入无效，使用默认的周一进行定投。")

    elif strategy == 'monthly':
        day_of_month_input = input("请输入每月定投的日期 (1-31, 默认为1): ").strip()
        try:
            day_of_month = int(day_of_month_input) if day_of_month_input else 1
            if 1 <= day_of_month <= 31:
                strategy_params['day_of_month'] = day_of_month
                print(f"已选择每月的 {day_of_month} 号进行定投。")
            else:
                print("输入无效，使用默认的1号进行定投。")
        except ValueError:
            print("输入无效，使用默认的1号进行定投。")

    # 获取定投金额
    amount_prompt = "请输入每月定投金额 (美元)" if strategy == 'monthly' else "请输入每周定投金额 (美元)"
    amount_input = input(f"{amount_prompt} (默认为 100.0): ").strip()
    try:
        amount = float(amount_input) if amount_input else 100.0
    except ValueError:
        print("输入无效，使用默认金额 100.0 美元")
        amount = 100.0
    
    print(f"\n正在加载 {symbol} 从 {start_date} 到 {end_date} 的数据...")
    
    # 先尝试加载数据，如果失败则使用模拟数据进行测试
    if backtester.load_data(symbol, start_date, end_date):
        print(f"正在运行{('每月' if strategy == 'monthly' else '每周')}定投回测...")
        backtest_result = backtester.run_backtest(
            amount=amount,
            start_date=start_date,
            end_date=end_date,
            compare=True,  # 与一次性投资比较
            strategy=strategy,
            strategy_params=strategy_params
        )
        
        # 打印结果
        backtester.print_results(backtest_result, compare=True, strategy=strategy)
        
        # 绘制结果图表
        backtester.plot_results(backtest_result['drip_result'] if 'drip_result' in backtest_result else backtest_result)
    else:
        print("无法获取真实股票数据，使用模拟数据进行测试...")
        # 创建模拟数据进行测试
        import numpy as np
        from datetime import datetime, timedelta
        import pandas as pd
        
        # 生成模拟股票数据
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        # 移除周末
        dates = dates[dates.weekday < 5]
        
        # 生成模拟股价数据（从150开始，随机波动）
        prices = [150.0]
        for i in range(1, len(dates)):
            change = np.random.normal(0, 0.02)  # 日收益率均值为0，标准差为2%
            new_price = prices[-1] * (1 + change)
            prices.append(max(new_price, 0.01))  # 确保价格为正
        
        # 创建DataFrame
        backtester.stock_data = pd.DataFrame({
            'Open': prices,
            'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            'Close': prices,
            'Volume': [np.random.randint(1000000, 10000000) for _ in range(len(dates))]
        }, index=dates)
        backtester.symbol = symbol
        
        print("成功创建模拟数据")
        print(f"数据范围: {backtester.stock_data.index[0].date()} 到 {backtester.stock_data.index[-1].date()}")
        
        print(f"正在运行{('每月' if strategy == 'monthly' else '每周')}定投回测...")
        backtest_result = backtester.run_backtest(
            amount=amount,
            start_date=start_date,
            end_date=end_date,
            compare=True,  # 与一次性投资比较
            strategy=strategy,
            strategy_params=strategy_params
        )
        
        # 打印结果
        backtester.print_results(backtest_result, compare=True, strategy=strategy)
        
        # 绘制结果图表
        backtester.plot_results(backtest_result['drip_result'] if 'drip_result' in backtest_result else backtest_result)


if __name__ == "__main__":
    main()