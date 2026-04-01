from __future__ import annotations
import numpy as np
import pandas as pd

def max_drawdown(equity: pd.Series)->float:
    peak = equity.cummax()
    draw_down =(equity/peak)-1.0

    return float(draw_down.min())

def sharpe_hourly(pnl_pct: pd.Series)->float:
    ann =365*24
    mu =pnl_pct.mean()
    sig =pnl_pct.std()
    if sig ==0 or np.isnan(sig):
        return 0.0
    return float(mu/sig*np.sqrt(ann))

def compute_metrics(port:pd.DataFrame)->dict:
    equity =port['equity']
    pnl =port['pnl_pct']
    total_return =float(equity.iloc[-1]/equity.iloc[0]-1.0)
    
    mdd =max_drawdown(equity)
    shp =sharpe_hourly(pnl)
    return {
        "total_return": total_return,
        "max_drawdown": mdd,
        "sharpe_ratio": shp,
        "final_equity": float(equity.iloc[-1])
    }