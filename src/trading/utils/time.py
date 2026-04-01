from __future__  import annotations
import datetime as dt


def utc_now_str()->str:
    return dt.datetime.now(dt.timezone.utc).strftime( \
        '%Y-%m-%d_%H-%M-%S')
