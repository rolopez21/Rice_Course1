from pathlib import Path
import pandas as pd
import numpy as np
import hvplot.pandas
import panel as pn

def initialize():
    """Initialize the dashboard, data storage, and account balances."""
    return

def build_dashboard(signals_df, portfolio_evaluation_df):
    """Build the dashboard."""
    # Create hvplot visualizations
    price_df = signals_df[["close", "SMA50", "SMA100"]]
    price_chart = price_df.hvplot.line().opts(xaxis=None)


    portfolio_evaluation_table = portfolio_evaluation_df.hvplot.table(
        columns=["index", "Backtest"]
    )

    # Build the dashboard
    dashboard = pn.Column(
        "# Trading Dashboard", price_chart, portfolio_evaluation_table
    )
    return dashboard

def fetch_data():
    """Fetches the latest prices."""

    filepath = Path("../Resources/aapl.csv")
    data_df = pd.read_csv(filepath)

    # print(data_df.head())
    return data_df


def generate_signals(data_df):
    """Generates trading signals for a given dataset."""

    signals_df = data_df.loc[:, ["date", "close"]].copy()
    signals_df.set_index("date", inplace=True, drop=True)

    short_window = 50
    long_window = 100

    signals_df["SMA50"] = signals_df["close"].rolling(window=short_window).mean()
    signals_df["SMA100"] = signals_df["close"].rolling(window=long_window).mean()
    signals_df["Signal"] = 0.0

    signals_df["Signal"][short_window:] = np.where(
        signals_df["SMA50"][short_window:] > signals_df["SMA100"][short_window:],
        1.0,
        0.0
    )

    signals_df["Entry/Exit"] = signals_df["Signal"].diff()


    return signals_df


def execute_backtest(signals_df):
    """Backtests signal data."""
    initial_capital = 100000

    share_size = 500

    signals_df["Position"] = share_size * signals_df["Signal"]
    signals_df["Entry/Exit Position"] = signals_df["Position"].diff()
    
    signals_df["Portfolio Holdings"] = (
        signals_df["close"] * signals_df["Entry/Exit Position"].cumsum()
    )
    
    signals_df["Portfolio Cash"] = (
        initial_capital
        - (signals_df["close"] * signals_df["Entry/Exit Position"]).cumsum()
    )
    signals_df["Portfolio Total"] = (
        signals_df["Portfolio Cash"] + signals_df["Portfolio Holdings"]
    )

    signals_df["Portfolio Daily Returns"] = signals_df["Portfolio Total"].pct_change()


    signals_df["Portfolio Cumulative Returns"] = (
        1 + signals_df["Portfolio Daily Returns"]
    ).cumprod() - 1


    return signals_df


def execute_trade_strategy():
    """Makes a buy/sell/hold decision."""

    return

def evaluate_metrics(historicals_df):
    """Generates evaluation metrics from backtested signal data."""

    # Prepare DataFrame for metrics
    metrics = [
        "Annual Return",
        "Cumulative Returns",
        "Annual Volatility",
        "Sharpe Ratio",
        "Sortino Ratio",
    ]

    columns = ["Backtest"]

    # Initialize the DataFrame with index set to evaluation metrics and column as `Backtest` (just like PyFolio)
    portfolio_evaluation_df = pd.DataFrame(index=metrics, columns=columns)

    # Calculate cumulative return
    portfolio_evaluation_df.loc["Cumulative Returns"] = historicals_df[
        "Portfolio Cumulative Returns"
    ][-1]

    # Calculate annualized return
    portfolio_evaluation_df.loc["Annual Return"] = (
        1 + historicals_df["Portfolio Daily Returns"].mean()
    ) ** 252 - 1

    # Calculate annual volatility
    portfolio_evaluation_df.loc["Annual Volatility"] = (
        1 + historicals_df["Portfolio Daily Returns"].std()
    ) ** 252 - 1

    # Calculate Sharpe Ratio
    portfolio_evaluation_df.loc["Sharpe Ratio"] = (
        historicals_df["Portfolio Daily Returns"].mean() * 252
    ) / (historicals_df["Portfolio Daily Returns"].std() * np.sqrt(252))

    # Calculate Downside Return
    sortino_ratio_df = historicals_df[["Portfolio Daily Returns"]].copy()
    sortino_ratio_df.loc[:, "Downside Returns"] = 0

    target = 0
    mask = sortino_ratio_df["Portfolio Daily Returns"] < target
    sortino_ratio_df.loc[mask, "Downside Returns"] = (
        sortino_ratio_df["Portfolio Daily Returns"] ** 2
    )
    
    # Calculate Sortino Ratio
    down_stdev = np.sqrt(sortino_ratio_df["Downside Returns"].mean())
    expected_return = sortino_ratio_df["Portfolio Daily Returns"].mean()
    sortino_ratio = expected_return / down_stdev

    portfolio_evaluation_df.loc["Sortino Ratio"] = sortino_ratio

    return portfolio_evaluation_df

def update_dashboard():
    """Updates the dashboard."""
    return

def main():
    """Main Event Loop."""
    # initialize()
    raw_data = fetch_data()
    processed_data = generate_signals(raw_data)
    backtest = execute_backtest(processed_data)
    # execute_trade_strategy()
    evaluation_df = evaluate_metrics(backtest)
    dashboard = build_dashboard(backtest,evaluation_df)
    dashboard.servable()
    return

main()