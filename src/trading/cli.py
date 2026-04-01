from __future__ import annotations
from pathlib import Path
import yaml
import pandas as pd

from src.trading.utils.time import utc_now_str
from src.trading.utils.log import set_logger
from src.trading.data.binance import fetch_klines_1h
from src.trading.data.clean import clean_bars
from src.trading.data.schema import SCHEMA
from src.trading.features.indicators import add_momentum
from src.trading.strategies.base import StrategyConfigs
from src.trading.strategies.momentum import MomentumStrategy
from src.trading.backtest.engine import run_backtest
from src.trading.backtest.metrics import compute_metrics
from src.trading.reporting.report import write_report

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR =ROOT/'data'
RUNS_DIR =ROOT/'runs'

def load_configs(config_path: Path)->dict:
    return yaml.safe_load(Path(config_path).read_text(encoding=
                                                'utf-8'))

def fetch(cfg: dict)-> pd.DataFrame:
    symbols =cfg['symbols']
    start =cfg['data']['start']
    dfs =[]

    for s in symbols:
        dfs.append(fetch_klines_1h(s,start))
    bars =pd.concat(dfs, ignore_index =True)
    bars =clean_bars(bars)
    DATA_DIR.mkdir(parents =True, exist_ok =True)
    bars.to_parquet(DATA_DIR/'bars_1h.parquet',
                    index =False)
    return bars

def backtest(cfg: dict)->None:
    run_id =utc_now_str()
    run_dir =RUNS_DIR / run_id
    run_dir.mkdir(parents=True,exist_ok =True)
    logger =set_logger(run_dir/'run.log')
    logger.info('loading config...')

    (run_dir/'config_snapshot.yaml').write_text(yaml.safe_dump(cfg,sort_keys=False), encoding ='utf-8')
    
    bars_path =DATA_DIR/'bars_1h.parquet'
    if not bars_path.exists():
        logger.info('no data found. fetching first...')
        bars =fetch(cfg)
    else:
        bars =pd.read_parquet(bars_path)

    strat_cfg =StrategyConfigs(
        lookback_hours =int(cfg['strategy']['lookback_hours']),
        long_only  =bool(cfg['strategy']['long_only'])

    )
    logger.info(f'building features for momentum lookback ={strat_cfg.lookback_hours}h')
    bars_feat = add_momentum(bars,strat_cfg.lookback_hours)
    
    strategy =MomentumStrategy(strat_cfg)
    targets =strategy.target_position(bars_feat)

    logger.info('running backtest...')
    port, trades = run_backtest( data=bars,
                 target_pos=targets,
                 fee_bps=float(cfg['costs']['fee_bps']),
                 slippage_bps=float(cfg['costs']['slippage_bps']),
                 initial_capital=float(cfg['backtest']['initial_capital']),
                 fill=(cfg['backtest']['fill']), )
    
    trades.to_csv(run_dir/'trades.csv',index=False, encoding='utf-8')

    metrics =compute_metrics(port)
    logger.info(f'metrics:{metrics}')

    write_report(run_dir,port,metrics)
    logger.info(f'done. run dir:{run_dir}')


if __name__ =='__main__':
    cfg =load_configs(str(ROOT/'configs'/'default.yaml'))
    backtest(cfg)




