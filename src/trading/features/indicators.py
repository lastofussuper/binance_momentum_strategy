from __future__ import annotations
import pandas as pd
from src.trading.data.schema import SCHEMA

def add_returns(df:pd.DataFrame)-> pd.DataFrame:
    df['returns'] =df.goupby(SCHEMA.symbol)[SCHEMA.close].pct_change()
    return df

def add_momentum(df:pd.DataFrame,
                 lookback_hours:int)->pd.DataFrame:
    df[f'ret_{lookback_hours}h'] = df.groupby(SCHEMA.symbol)[SCHEMA.close].pct_change(periods=lookback_hours)

    return df
