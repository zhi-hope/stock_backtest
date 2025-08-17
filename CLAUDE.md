# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python program for backtesting US stock dollar-cost averaging (DCA) investment strategies. The program can load historical stock data, simulate weekly or monthly DCA strategies, and compare them with lump-sum investing.

## Code Architecture

The project is organized into several modules:

1. `main.py` - Main program module with the StockDripBacktester class and user interaction
2. `data_fetcher.py` - Data retrieval module using yfinance library
3. `investment_strategy.py` - DCA strategy module for generating investment dates and calculating shares
4. `backtest.py` - Backtesting calculation module
5. `visualization.py` - Visualization module for generating charts
6. `__init__.py` - Package initialization and exports

## Common Development Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

Requirements include:
- numpy
- pandas
- yfinance
- matplotlib

### Run the Program
```bash
python main.py
```

### Programmatic Usage
```python
from main import StockDripBacktester

# Create backtester instance
backtester = StockDripBacktester()

# Load stock data
symbol = "AAPL"
start_date = "2020-01-01"
end_date = "2023-12-31"

if backtester.load_data(symbol, start_date, end_date):
    # Run weekly DCA backtest (invest $100 each week)
    backtest_result = backtester.run_backtest(
        amount=100.0,
        start_date=start_date,
        end_date=end_date,
        compare=True,  # Compare with lump-sum investing
        strategy='weekly'  # DCA strategy: 'weekly' or 'monthly'
    )
    
    # Print results
    backtester.print_results(backtest_result, compare=True, strategy='weekly')
    
    # Plot results
    backtester.plot_results(backtest_result['drip_result'] if 'drip_result' in backtest_result else backtest_result)
```

## Key Classes and Functions

### StockDripBacktester (main.py)
- `load_data(symbol, start_date, end_date)` - Load stock data
- `run_backtest(amount, start_date, end_date, compare, strategy)` - Run DCA backtest
- `print_results(result, compare, strategy)` - Print backtest results
- `plot_results(result)` - Generate and save charts

### Data Fetching (data_fetcher.py)
- `get_stock_data(symbol, start_date, end_date)` - Retrieve stock historical data
- `get_stock_info(symbol)` - Get stock information

### Investment Strategy (investment_strategy.py)
- `weekly_investment_dates(start_date, end_date)` - Generate weekly investment dates
- `monthly_investment_dates(start_date, end_date)` - Generate monthly investment dates
- `calculate_investment_shares(stock_data, investment_dates, weekly_amount)` - Calculate shares for each investment

### Backtesting (backtest.py)
- `run_backtest(stock_data, amount, start_date, end_date, strategy)` - Execute DCA backtest
- `compare_with_lump_sum(stock_data, amount, start_date, end_date, strategy)` - Compare DCA with lump-sum investing

### Visualization (visualization.py)
- `plot_investment_growth(backtest_result, symbol)` - Plot investment growth chart
- `plot_price_vs_investment(stock_data, backtest_result, symbol)` - Plot price vs investment points chart