# 美股股票定投回测程序

这是一个用于回测美股股票定投策略效果的Python程序。该程序可以加载股票历史数据，模拟每周或每月定投策略，并与一次性投资进行比较。

## 功能特点

- 获取美股历史股价数据 (使用yfinance库)
- 模拟每周或每月定投策略 (可自定义日期)
- 计算定投收益率和年化收益率
- 与一次性投资策略进行比较
- 可视化定投结果和股价走势
- 支持命令行交互式使用和编程方式调用
- 提供图形用户界面(GUI)进行可视化操作
- 包含自动化测试套件 (pytest)

## 安装依赖

```bash
pip install -r requirements.txt
```

依赖包括：
- numpy
- pandas
- yfinance
- matplotlib
- PyQt6
- pytest

## 运行测试

项目包含一套自动化测试，用于验证核心计算逻辑的准确性。安装依赖后，运行以下命令：

```bash
python3 -m pytest
```

## 使用方式

### 1. 图形界面使用 (推荐)

程序提供了一个直观的图形用户界面，可以通过以下命令启动：

```bash
python gui.py
```

GUI功能：
- 直观的参数输入界面
- 实时结果显示
- 图表可视化
- 结果导出功能

### 2. 命令行交互式使用

直接运行主程序，根据提示输入股票代码、时间范围、定投策略和金额：

```bash
python main.py
```

### 3. 编程方式使用

```python
from main import StockDripBacktester

# 创建回测器实例
backtester = StockDripBacktester()

# 加载股票数据
symbol = "AAPL"  # 苹果公司
start_date = "2020-01-01"
end_date = "2023-12-31"

if backtester.load_data(symbol, start_date, end_date):
    # 运行每周定投回测 (每周定投100美元)
    backtest_result = backtester.run_backtest(
        amount=100.0,
        start_date=start_date,
        end_date=end_date,
        compare=True,  # 与一次性投资比较
        strategy='weekly'  # 定投策略: 'weekly' 或 'monthly'
    )
    
    # 打印结果
    backtester.print_results(backtest_result, compare=True, strategy='weekly')
    
    # 绘制结果图表
    backtester.plot_results(backtest_result['drip_result'] if 'drip_result' in backtest_result else backtest_result)
```

## 代码架构

项目采用模块化设计，组织如下：

1. `main.py` - 主程序模块，包含StockDripBacktester类和用户交互
2. `data_fetcher.py` - 数据获取模块，使用yfinance库获取股票数据
3. `investment_strategy.py` - 定投策略模块，生成投资日期和计算股份数量
4. `backtest.py` - 回测计算模块，执行定投回测和比较分析
5. `visualization.py` - 可视化模块，生成图表
6. `gui.py` - 图形用户界面模块
7. `__init__.py` - 包初始化文件

## 核心类和函数

### StockDripBacktester (main.py)
- `load_data(symbol, start_date, end_date)` - 加载股票数据
- `run_backtest(amount, start_date, end_date, compare, strategy, strategy_params)` - 运行定投回测
- `print_results(result, compare, strategy)` - 打印回测结果
- `plot_results(result)` - 生成和保存图表

### 数据获取 (data_fetcher.py)
- `get_stock_data(symbol, start_date, end_date)` - 获取股票历史数据
- `get_stock_info(symbol)` - 获取股票信息

### 投资策略 (investment_strategy.py)
- `weekly_investment_dates(start_date, end_date, day_of_week)` - 生成每周投资日期
- `monthly_investment_dates(start_date, end_date, day_of_month)` - 生成每月投资日期
- `calculate_investment_shares(stock_data, investment_dates, weekly_amount)` - 计算每次投资的股份数量

### 回测 (backtest.py)
- `run_backtest(stock_data, amount, start_date, end_date, strategy, strategy_params)` - 执行定投回测
- `compare_with_lump_sum(stock_data, amount, start_date, end_date, strategy, strategy_params)` - 与一次性投资比较

### 可视化 (visualization.py)
- `plot_investment_growth(backtest_result, symbol, ax=None)` - 绘制定投增长图表
- `plot_price_vs_investment(stock_data, backtest_result, symbol, ax=None)` - 绘制股价与投资点对比图表

## 注意事项

1. 该程序仅供学习和研究使用
2. 股票投资存在风险，历史回测结果不保证未来收益
3. 程序使用yfinance库获取数据，需要网络连接
4. GUI程序需要图形环境支持，如果在无头服务器上运行可能需要配置X11转发