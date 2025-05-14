# volatility_targeting/core.py

import pandas as pd
import numpy as np

class VolatilityTargeting:
    def __init__(self, lookback=25, target_vol_pct=0.01, rebalance_buffer=0.1):
        self.lookback = lookback
        self.target_vol_pct = target_vol_pct
        self.rebalance_buffer = rebalance_buffer

    def annualized_volatility(self, prices):
        daily_returns = prices.pct_change()
        rolling_vol = daily_returns.rolling(self.lookback).std()
        return rolling_vol * np.sqrt(252)

    def compute_weights(self, price_df, allocated_equity=1_000_000, max_positions=None):
        vol_df = price_df.pct_change().rolling(self.lookback).std() * np.sqrt(252)
        uncapped_weights = self.target_vol_pct / vol_df
        weight_sum = uncapped_weights.sum(axis=1)
        norm_weights = uncapped_weights.div(weight_sum, axis=0)

        if max_positions is None:
            max_positions = price_df.shape[1]
        cap_per_asset = allocated_equity / max_positions

        position_sizes = norm_weights.mul(allocated_equity, axis=0)
        capped_positions = position_sizes.clip(upper=cap_per_asset)
        return capped_positions

    def rebalance_needed(self, current_weights, new_weights):
        weight_diff = (new_weights - current_weights).abs()
        return (weight_diff > self.rebalance_buffer * current_weights).any()
