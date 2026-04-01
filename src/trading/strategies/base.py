from __future__ import annotations
import pandas as pd
from dataclasses import dataclass

@dataclass(frozen =True)
class StrategyConfigs:
    lookback_hours: int
    long_only: bool =True


class Strategy:
    name: str ='base'

    def __init__(self, cfg: StrategyConfigs):
        self.cfg =cfg

    def target_position(self, data:pd.DataFrame)->pd.DataFrame:
        raise NotImplementedError 