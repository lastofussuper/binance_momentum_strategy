from __future__ import annotations
from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd
from src.trading.data.schema import SCHEMA

def write_report(run_dir: Path,
                 port: pd.DataFrame,
                 metrics: dict,)->None:
    run_dir.mkdir(parents=True,
                  exist_ok=True)

    (run_dir/'metrics.json').write_text(json.dumps(metrics, indent =2), encoding ='utf-8')

    port.to_parquet(run_dir/'port.parquet', index =False)

    plt.figure()
    plt.plot(port[SCHEMA.ts],port['equity'])
    plt.xticks(rotation =30)
    plt.tight_layout()
    plt.savefig(run_dir/'equity.png',dpi=150)
    plt.close()