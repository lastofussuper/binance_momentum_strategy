from __future__ import annotations
from datetime import datetime, timezone
import time
import requests
from .schema import SCHEMA
import pandas as pd
def time_to_ms(time:str)->int:
    dt =datetime.strptime(time,'%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp()*1000
    return int(dt)
    

def fetch_klines_1h(symbol:str,
                 start:str,
                 limit: int=1000,)->pd.DataFrame:
    data =[]
    start_time =time_to_ms(start)
    api_url ='https://api.binance.com/api/v3/klines'
    interval ='1h'
    
    while True:

        params_list ={'symbol':symbol,
                      'interval':interval,
                      'startTime':start_time,
                      'limit':limit}
        
        response = requests.get(api_url,
                params =params_list,timeout=30)
        response.raise_for_status()
        data_snippet =response.json()
        
        if not data_snippet:
            break

        data.extend(data_snippet)

        if len(data_snippet)<limit:
            break

        last_time =data_snippet[-1][0]
        start_time =last_time + 60*60*1000
        
        
        time.sleep(0.3)
        
        
    df =pd.DataFrame(data,
                    columns =['open_time','open','high','low','close','volume',
                            'close_time','quote_asset_volume','number_of_trades',
                            'taker_buy_base_asset_volume','taker_buy_quote_asset_volume','ignore'])
    
    df[SCHEMA.ts]=pd.to_datetime(df['open_time'],unit='ms',utc =True).dt.tz_convert(None)

    df[SCHEMA.symbol]=symbol
    for c in [SCHEMA.open, SCHEMA.high, SCHEMA.low, SCHEMA.close, SCHEMA.volume]:
        df[c] =df[c].astype(float)
        



    return df[[SCHEMA.ts, SCHEMA.symbol, SCHEMA.open, SCHEMA.high, SCHEMA.low, SCHEMA.close, SCHEMA.volume]]
    


