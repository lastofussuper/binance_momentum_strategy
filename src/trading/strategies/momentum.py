from __future__ import annotations
import pandas as pd
from .base import Strategy, StrategyConfigs
from src.trading.data.schema import SCHEMA

class MomentumStrategy(Strategy):
    name: str ='momentum'

    def target_position(self, data: pd.DataFrame)-> pd.DataFrame:
        lb =self.cfg.lookback_hours
        col =f'ret_{lb}h'
        sig =(data[col]>0).astype(float)
        if not self.cfg.long_only:
            sig =2*sig -1
        out =data[[SCHEMA.ts,SCHEMA.symbol]].copy()
        out['target_pos'] =sig.fillna(0)

        return out