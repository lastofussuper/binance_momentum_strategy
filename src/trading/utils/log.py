from __future__ import annotations
import logging
from pathlib import Path

def set_logger(log_dir: Path)-> logging.Logger:
    logger =logging.getLogger('trading')
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt =logging.Formatter( \
        "%(asctime)s | %(levelname)s | %(message)s")
    
    fh =logging.FileHandler(log_dir, encoding='utf-8')
    fh.setFormatter(fmt)

    sh =logging.StreamHandler()
    sh.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(sh)


    return logger

