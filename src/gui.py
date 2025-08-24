"""
GUI界面模块
"""
import sys
import os
from datetime import datetime
# 在导入PyQt6之前设置环境变量以避免X11连接问题
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QRadioButton, QButtonGroup, QCheckBox, QTextEdit, 
                            QTabWidget, QFileDialog, QMessageBox, QDateEdit, 
                            QGroupBox, QFormLayout)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont, QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import StockDripBacktester

class StockBacktestGUI(QMainWindow):
    """股票定投回测GUI界面"""
    
    def __init__(self):
        super().__init__()
        self.backtester = StockDripBacktester()
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('美股股票定投回测器')
        self.setGeometry(100, 100, 1000, 800)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 创建输入区域
        self.create_input_section(main_layout)
        
        # 创建控制按钮区域
        self.create_control_section(main_layout)
        
        # 创建结果显示区域
        self.create_results_section(main_layout)
        
        # 创建状态栏
        self.statusBar().showMessage('就绪')
        
    def create_input_section(self, parent_layout):
        """创建输入区域"""
        # 创建输入组框
        input_group = QGroupBox("输入参数")
        input_layout = QVBoxLayout()
        
        # 股票信息行
        stock_layout = QHBoxLayout()
        stock_layout.addWidget(QLabel("股票代码:"))
        self.symbol_input = QLineEdit("AAPL")
        stock_layout.addWidget(self.symbol_input)
        
        stock_layout.addWidget(QLabel("开始日期:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate(2020, 1, 1))
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        stock_layout.addWidget(self.start_date)
        
        stock_layout.addWidget(QLabel("结束日期:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate(2023, 12, 31))
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        stock_layout.addWidget(self.end_date)
        
        input_layout.addLayout(stock_layout)
        
        # 投资策略行
        strategy_layout = QHBoxLayout()
        
        # 策略选择
        strategy_group = QGroupBox("投资策略")
        strategy_vbox = QVBoxLayout()
        self.weekly_radio = QRadioButton("每周定投")
        self.monthly_radio = QRadioButton("每月定投")
        self.weekly_radio.setChecked(True)
        
        strategy_radio_group = QButtonGroup()
        strategy_radio_group.addButton(self.weekly_radio)
        strategy_radio_group.addButton(self.monthly_radio)
        
        strategy_vbox.addWidget(self.weekly_radio)
        strategy_vbox.addWidget(self.monthly_radio)
        strategy_group.setLayout(strategy_vbox)
        strategy_layout.addWidget(strategy_group)
        
        # 投资金额
        amount_layout = QVBoxLayout()
        amount_layout.addWidget(QLabel("投资金额 ($):"))
        self.amount_input = QLineEdit("100.0")
        amount_layout.addWidget(self.amount_input)
        strategy_layout.addLayout(amount_layout)
        
        # 比较选项
        compare_layout = QVBoxLayout()
        self.compare_checkbox = QCheckBox("与一次性投资比较")
        self.compare_checkbox.setChecked(True)
        compare_layout.addWidget(self.compare_checkbox)
        strategy_layout.addLayout(compare_layout)
        
        strategy_layout.addStretch()  # 添加弹性空间
        input_layout.addLayout(strategy_layout)
        
        input_group.setLayout(input_layout)
        parent_layout.addWidget(input_group)
        
    def create_control_section(self, parent_layout):
        """创建控制按钮区域"""
        control_layout = QHBoxLayout()
        
        # 运行按钮
        self.run_button = QPushButton("运行回测")
        self.run_button.clicked.connect(self.run_backtest)
        self.run_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        control_layout.addWidget(self.run_button)
        
        # 重置按钮
        self.reset_button = QPushButton("重置")
        self.reset_button.clicked.connect(self.reset_inputs)
        control_layout.addWidget(self.reset_button)
        
        # 导出按钮
        self.export_button = QPushButton("导出结果")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setEnabled(False)
        control_layout.addWidget(self.export_button)
        
        control_layout.addStretch()
        parent_layout.addLayout(control_layout)
        
    def create_results_section(self, parent_layout):
        """创建结果显示区域"""
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        
        # 文本结果标签页
        self.text_results = QTextEdit()
        self.text_results.setReadOnly(True)
        self.text_results.setFont(QFont("Courier", 10))
        self.tab_widget.addTab(self.text_results, "文本结果")
        
        # 图表标签页
        self.chart_tab = QWidget()
        chart_layout = QVBoxLayout()
        
        # 创建图表标签页
        self.chart_tabs = QTabWidget()
        
        # 投资增长图
        self.growth_chart_widget = QWidget()
        growth_layout = QVBoxLayout()
        self.growth_figure = Figure(figsize=(10, 6))
        self.growth_canvas = FigureCanvas(self.growth_figure)
        growth_layout.addWidget(self.growth_canvas)
        self.growth_chart_widget.setLayout(growth_layout)
        self.chart_tabs.addTab(self.growth_chart_widget, "投资增长图")
        
        # 价格与投资点对比图
        self.price_chart_widget = QWidget()
        price_layout = QVBoxLayout()
        self.price_figure = Figure(figsize=(10, 6))
        self.price_canvas = FigureCanvas(self.price_figure)
        price_layout.addWidget(self.price_canvas)
        self.price_chart_widget.setLayout(price_layout)
        self.chart_tabs.addTab(self.price_chart_widget, "价格与投资点对比图")
        
        chart_layout.addWidget(self.chart_tabs)
        self.chart_tab.setLayout(chart_layout)
        self.tab_widget.addTab(self.chart_tab, "图表结果")
        
        parent_layout.addWidget(self.tab_widget)
        
    def run_backtest(self):
        """运行回测"""
        try:
            # 获取输入参数
            symbol = self.symbol_input.text().strip().upper()
            if not symbol:
                QMessageBox.warning(self, "输入错误", "请输入股票代码")
                return
                
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            if start_date >= end_date:
                QMessageBox.warning(self, "输入错误", "开始日期必须早于结束日期")
                return
            
            # 获取投资策略
            strategy = 'monthly' if self.monthly_radio.isChecked() else 'weekly'
            
            # 获取投资金额
            try:
                amount = float(self.amount_input.text())
                if amount <= 0:
                    QMessageBox.warning(self, "输入错误", "投资金额必须大于0")
                    return
            except ValueError:
                QMessageBox.warning(self, "输入错误", "请输入有效的投资金额")
                return
            
            # 获取比较选项
            compare = self.compare_checkbox.isChecked()
            
            # 更新状态栏
            self.statusBar().showMessage(f'正在加载 {symbol} 数据...')
            self.run_button.setEnabled(False)
            QApplication.processEvents()
            
            # 加载数据
            if not self.backtester.load_data(symbol, start_date, end_date):
                QMessageBox.warning(self, "数据加载失败", f"无法加载 {symbol} 的数据，将使用模拟数据进行测试")
                # 创建模拟数据
                self.create_mock_data(symbol, start_date, end_date)
            
            # 运行回测
            self.statusBar().showMessage('正在运行回测...')
            QApplication.processEvents()
            
            backtest_result = self.backtester.run_backtest(
                amount=amount,
                start_date=start_date,
                end_date=end_date,
                compare=compare,
                strategy=strategy
            )
            
            if backtest_result:
                # 显示结果
                self.display_results(backtest_result, compare, strategy)
                self.export_button.setEnabled(True)
                self.statusBar().showMessage('回测完成')
            else:
                QMessageBox.warning(self, "回测失败", "回测过程出现错误")
                self.statusBar().showMessage('回测失败')
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"运行回测时发生错误: {str(e)}")
            self.statusBar().showMessage('回测出错')
        finally:
            self.run_button.setEnabled(True)
            
    def create_mock_data(self, symbol, start_date, end_date):
        """创建模拟数据"""
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
        self.backtester.stock_data = pd.DataFrame({
            'Open': prices,
            'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            'Close': prices,
            'Volume': [np.random.randint(1000000, 10000000) for _ in range(len(dates))]
        }, index=dates)
        self.backtester.symbol = symbol
        
    def display_results(self, result, compare, strategy):
        """显示回测结果"""
        # 显示文本结果
        self.display_text_results(result, compare, strategy)
        
        # 显示图表结果
        self.display_chart_results(result)
        
    def display_text_results(self, result, compare, strategy):
        """显示文本结果"""
        if not result:
            self.text_results.setPlainText("回测结果为空")
            return
            
        # 根据策略确定显示的周期单位
        period_unit = "月" if strategy == 'monthly' else "周"
        
        # 构建结果文本
        output = []
        output.append("=" * 50)
        output.append(f"股票代码: {self.backtester.symbol}")
        output.append(f"数据范围: {self.backtester.stock_data.index[0].date()} 到 {self.backtester.stock_data.index[-1].date()}")
        output.append("=" * 50)
        
        if compare and 'drip_result' in result:
            drip_result = result['drip_result']
            output.append(f"\n=== 定投回测结果 ===")
            output.append(f"定投周期: {drip_result['investment_count']} {period_unit}")
            amount_label = "每月定投金额" if strategy == 'monthly' else "每周定投金额"
            output.append(f"{amount_label}: ${drip_result['investment_records']['Amount'].iloc[0]:.2f}")
            output.append(f"总投入金额: ${drip_result['total_investment']:.2f}")
            output.append(f"最终价值: ${drip_result['final_value']:.2f}")
            output.append(f"最终股价: ${drip_result['final_price']:.2f}")
            output.append(f"总收益率: {drip_result['total_return']:.2f}%")
            output.append(f"年化收益率: {drip_result['annual_return']:.2f}%")
            
            output.append(f"\n=== 一次性投资比较 ===")
            output.append(f"一次性投资价值: ${result['lump_sum_value']:.2f}")
            output.append(f"一次性投资收益率: {result['lump_sum_return']:.2f}%")
            output.append(f"定投相比一次性投资差异: {result['difference']:.2f}%")
            
            if result['difference'] > 0:
                output.append("定投策略表现更好")
            else:
                output.append("一次性投资表现更好")
        elif 'total_investment' in result:
            output.append(f"\n=== 定投回测结果 ===")
            output.append(f"定投周期: {result['investment_count']} {period_unit}")
            amount_label = "每月定投金额" if strategy == 'monthly' else "每周定投金额"
            output.append(f"{amount_label}: ${result['investment_records']['Amount'].iloc[0]:.2f}")
            output.append(f"总投入金额: ${result['total_investment']:.2f}")
            output.append(f"最终价值: ${result['final_value']:.2f}")
            output.append(f"最终股价: ${result['final_price']:.2f}")
            output.append(f"总收益率: {result['total_return']:.2f}%")
            output.append(f"年化收益率: {result['annual_return']:.2f}%")
            
        self.text_results.setPlainText("\n".join(output))
        
    def display_chart_results(self, result):
        """显示图表结果"""
        if not result:
            return
            
        # 清除之前的图表
        self.growth_figure.clear()
        self.price_figure.clear()
        
        # 绘制投资增长图
        try:
            # 获取结果数据
            if 'drip_result' in result:
                drip_result = result['drip_result']
            else:
                drip_result = result
                
            # 使用可视化模块中的函数绘制图表
            from visualization import plot_investment_growth, plot_price_vs_investment
            
            # 绘制投资增长图
            ax1 = self.growth_figure.add_subplot(111)
            plot_investment_growth(drip_result, self.backtester.symbol, ax1)
            self.growth_canvas.draw()
                
        except Exception as e:
            # 如果图表绘制失败，显示错误信息
            ax1 = self.growth_figure.add_subplot(111)
            ax1.text(0.5, 0.5, f'图表绘制错误: {str(e)}', ha='center', va='center', 
                    transform=ax1.transAxes, fontsize=12, color='red')
            self.growth_canvas.draw()
        
        # 绘制价格与投资点对比图
        try:
            if 'drip_result' in result:
                drip_result = result['drip_result']
            else:
                drip_result = result
                
            # 使用可视化模块中的函数绘制图表
            ax2 = self.price_figure.add_subplot(111)
            plot_price_vs_investment(self.backtester.stock_data, drip_result, self.backtester.symbol, ax2)
            self.price_canvas.draw()
                
        except Exception as e:
            # 如果图表绘制失败，显示错误信息
            ax2 = self.price_figure.add_subplot(111)
            ax2.text(0.5, 0.5, f'图表绘制错误: {str(e)}', ha='center', va='center', 
                    transform=ax2.transAxes, fontsize=12, color='red')
            self.price_canvas.draw()
        
    def reset_inputs(self):
        """重置输入"""
        self.symbol_input.setText("AAPL")
        self.start_date.setDate(QDate(2020, 1, 1))
        self.end_date.setDate(QDate(2023, 12, 31))
        self.weekly_radio.setChecked(True)
        self.amount_input.setText("100.0")
        self.compare_checkbox.setChecked(True)
        self.text_results.clear()
        self.export_button.setEnabled(False)
        
        # 清除图表
        self.growth_figure.clear()
        self.price_figure.clear()
        self.growth_canvas.draw()
        self.price_canvas.draw()
        
        self.statusBar().showMessage('已重置')
        
    def export_results(self):
        """导出结果"""
        try:
            # 获取保存文件路径
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "导出结果", 
                f"{self.backtester.symbol}_backtest_results.txt", 
                "文本文件 (*.txt);;所有文件 (*)"
            )
            
            if file_path:
                # 保存文本结果
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_results.toPlainText())
                QMessageBox.information(self, "导出成功", f"结果已导出到: {file_path}")
                self.statusBar().showMessage(f'结果已导出到: {file_path}')
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出结果时发生错误: {str(e)}")

def main():
    """主函数"""
    try:
        app = QApplication(sys.argv)
        gui = StockBacktestGUI()
        gui.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"无法启动GUI界面: {str(e)}")
        print("这可能是因为没有图形环境导致的。")
        print("请确保您在支持图形界面的环境中运行此程序，例如:")
        print("1. 本地桌面环境")
        print("2. 通过SSH连接时使用X11转发 (ssh -X user@host)")
        print("3. 在WSL2中使用WSLg")
        print("4. 在Docker中运行时启用图形支持")
        sys.exit(1)

if __name__ == "__main__":
    main()