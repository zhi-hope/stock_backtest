# 美股股票定投回测程序

这是一个用于回测美股股票定投策略效果的Python程序。该程序可以加载股票历史数据，模拟每周或每月定投策略，并与一次性投资进行比较。

## 功能特点

- 获取美股历史股价数据 (使用yfinance库)
- 模拟每周或每月定投策略
- 计算定投收益率和年化收益率
- 与一次性投资策略进行比较
- 可视化定投结果和股价走势
- 支持用户交互输入股票代码、时间范围和定投策略

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用示例

### 1. 编程方式使用

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

### 2. 交互式使用

直接运行主程序，根据提示输入股票代码、时间范围、定投策略和金额：

```bash
python main.py
```

## 模块说明

- `data_fetcher.py`: 数据获取模块，用于获取股票历史数据
- `investment_strategy.py`: 定投策略模块，生成定投日期和计算股份数量
- `backtest.py`: 回测计算模块，执行定投回测和比较分析
- `visualization.py`: 可视化模块，生成图表
- `main.py`: 主程序模块，包含StockDripBacktester类和使用示例

## 注意事项

1. 该程序仅供学习和研究使用
2. 股票投资存在风险，历史回测结果不保证未来收益
3. 程序使用yfinance库获取数据，需要网络连接
