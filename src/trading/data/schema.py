from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen =True)

class KlineSchema:
    ts: str ='timestamp'
    symbol: str ='symbol'
    open: str ='open'
    high: str ='high'
    low: str ='low'
    close: str ='close'
    volume: str ='volume'

SCHEMA = KlineSchema()
