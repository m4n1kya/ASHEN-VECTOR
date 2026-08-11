"""
Transaction costs model for backtesting.
"""

class TransactionCosts:
    """Models commission, slippage, and bid-ask spread."""
    
    def __init__(
        self,
        commission_rate: float = 0.001,  # 0.1% per trade
        slippage_rate: float = 0.0005,   # 0.05% slippage
        tax_rate: float = 0.0            # Stamp duty, etc.
    ):
        self.commission_rate = commission_rate
        self.slippage_rate = slippage_rate
        self.tax_rate = tax_rate
        
    def calculate_cost(self, trade_value: float, is_sell: bool = False) -> float:
        """Calculate total transaction costs for a trade."""
        cost = trade_value * (self.commission_rate + self.slippage_rate)
        if is_sell:
            cost += trade_value * self.tax_rate
        return cost
