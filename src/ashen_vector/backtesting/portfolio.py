"""
Portfolio tracking for backtesting.
"""
from typing import Dict, Any, List
import pandas as pd
from ashen_vector.backtesting.costs import TransactionCosts

class Portfolio:
    """Tracks cash, positions, and history."""
    
    def __init__(self, initial_capital: float = 100000.0, costs: TransactionCosts = None):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, float] = {}
        self.costs = costs or TransactionCosts()
        self.history: List[Dict[str, Any]] = []
        
    def get_total_value(self, current_prices: Dict[str, float]) -> float:
        """Calculate total portfolio value."""
        value = self.cash
        for sym, shares in self.positions.items():
            value += shares * current_prices.get(sym, 0.0)
        return value
        
    def execute_target(self, date: str, symbol: str, target_weight: float, price: float):
        """
        Execute trades to reach target weight (0.0 to 1.0).
        """
        if pd.isna(price) or price <= 0:
            return
            
        current_shares = self.positions.get(symbol, 0.0)
        current_value = self.get_total_value({symbol: price})
        
        target_value = current_value * target_weight
        current_position_value = current_shares * price
        
        value_to_trade = target_value - current_position_value
        
        if abs(value_to_trade) < 1.0:
            return # Ignore tiny rebalances
            
        is_sell = value_to_trade < 0
        cost = self.costs.calculate_cost(abs(value_to_trade), is_sell=is_sell)
        
        shares_to_trade = value_to_trade / price
        
        self.cash -= (value_to_trade + cost)
        self.positions[symbol] = current_shares + shares_to_trade
        
        self.history.append({
            "date": date,
            "symbol": symbol,
            "shares": shares_to_trade,
            "price": price,
            "cost": cost,
            "cash_after": self.cash,
            "position_after": self.positions[symbol]
        })
