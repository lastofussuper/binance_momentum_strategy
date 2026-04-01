from __future__ import annotations
import pandas as pd
from .schema import SCHEMA

def clean_bars(df: pd.DataFrame)-> pd.DataFrame:
    df =df.drop_duplicates(subset=[SCHEMA.ts, 
                                    SCHEMA.symbol]) \
                                        .sort_values(by=[SCHEMA.ts, SCHEMA.symbol])
    
    assert df[SCHEMA.ts].notna().all(), 'timestamp contains null values'
    assert (df[[SCHEMA.open, SCHEMA.high, SCHEMA.low,
                SCHEMA.close, SCHEMA.volume]].notna().all().all()),'price or volum contains null values'
    
    return df.reset_index(drop=True)

