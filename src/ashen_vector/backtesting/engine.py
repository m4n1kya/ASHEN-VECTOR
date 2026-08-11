"""
Backtesting engine for evaluating trading strategies and models.
"""

import pandas as pd
from ashen_vector.backtesting.portfolio import Portfolio
from ashen_vector.backtesting.costs import TransactionCosts

class BacktestEngine:
    """Iterates through historical data applying signals."""
    
    def __init__(self, initial_capital: float = 100000.0, costs: TransactionCosts = None):
        self.initial_capital = initial_capital
        self.costs = costs or TransactionCosts()
        
    def run(self, symbol: str, prices: pd.Series, signals: pd.Series) -> pd.DataFrame:
        """
        Run backtest on a single asset.
        prices: Close prices indexed by date.
        signals: Target position (1.0 for long, 0.0 for flat, -1.0 for short).
        Returns a DataFrame with the equity curve.
        """
        portfolio = Portfolio(self.initial_capital, self.costs)
        equity_curve = []
        
        # Ensure alignment
        dates = sorted(list(set(prices.index).intersection(signals.index)))
        
        for date in dates:
            price = float(prices[date])
            target_pos = float(signals[date])
            
            # Execute target weight
            portfolio.execute_target(date, symbol, target_pos, price)
            
            total_value = portfolio.get_total_value({symbol: price})
            current_shares = portfolio.positions.get(symbol, 0.0)
            
            equity_curve.append({
                "date": date,
                "portfolio_value": total_value,
                "position": current_shares,
                "signal": target_pos,
                "price": price
            })
            
        df = pd.DataFrame(equity_curve)
        if not df.empty:
            df = df.set_index("date")
            df["daily_return"] = df["portfolio_value"].pct_change().fillna(0.0)
            df["cumulative_return"] = (df["portfolio_value"] / self.initial_capital) - 1.0
            
            # Drawdown
            peak = df["portfolio_value"].cummax()
            df["drawdown"] = (df["portfolio_value"] - peak) / peak
            
        return df
