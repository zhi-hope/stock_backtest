# Stock Dollar-Cost Averaging Backtester

This project is a Python-based tool to backtest dollar-cost averaging (DCA) investment strategies on historical stock data. It allows users to simulate regular investments (weekly or monthly) and compares the performance against a lump-sum investment.

## Project Structure

The project follows a standard structure with source code separated from tests:

```
stock_backtest/
├── src/
│   ├── __init__.py
│   ├── backtest.py             # Core backtesting logic
│   ├── data_fetcher.py         # Fetches stock data using yfinance
│   ├── investment_strategy.py  # Defines investment schedules
│   ├── main.py                 # Main entry point for the application
│   └── visualization.py        # Creates plots for the results
├── tests/
│   ├── test_backtest.py
│   └── test_investment_strategy.py
├── .gitignore
├── pytest.ini                  # Pytest configuration
└── README.md
```

## How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Backtester:**
    The main application is interactive and will prompt you for the stock symbol, date range, and investment strategy.
    ```bash
    python -m src.main
    ```

3.  **Run Tests:**
    To run the unit tests, use pytest.
    ```bash
    pytest
    ```
