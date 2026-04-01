from __future__ import annotations
import pandas as pd
from src.trading.data.schema import SCHEMA
from .cost import bps_to_rate


def run_backtest(data:pd.DataFrame,
                 target_pos:pd.DataFrame,
                 fee_bps:float,
                 slippage_bps:float,
                 initial_capital:float,
                 fill:str='next_open', )-> tuple[ pd.DataFrame, pd.DataFrame]:
    
    df =pd.merge(data,target_pos, on=[SCHEMA.ts, SCHEMA.symbol],
                 how='left')
    df['target_pos'] = df['target_pos'].fillna(0)
    df =df.sort_values(by=[SCHEMA.ts, SCHEMA.symbol])
   
    df['ret'] =df.groupby(SCHEMA.symbol)[SCHEMA.close].pct_change().fillna(0)

    if fill =='next_open':
        df['pos']=df.groupby(SCHEMA.symbol)['target_pos'].shift(1).fillna(0)
    else:
        df['pos'] =df['target_pos']
    
    df['pos_prev'] =df.groupby(SCHEMA.symbol)['pos'].shift(1).fillna(0)
    df['turnover'] = (df['pos'] - df['pos_prev']).abs()

    cost_rate = bps_to_rate(fee_bps + slippage_bps)
    df['cost'] = df['turnover'] * cost_rate

    df['pnl_pct'] =df['pos']* df['ret'] - df['cost']

    port = df['pnl_pct'].groupby(df[SCHEMA.ts]).mean().to_frame('pnl_pct')
    port['equity'] =(1.0 + port['pnl_pct']).cumprod() * initial_capital 
    port =port.reset_index()

    trades = df.loc[df['turnover']>0,[SCHEMA.ts, SCHEMA.symbol, 'pos', 'turnover', 'cost']]

    return port, trades