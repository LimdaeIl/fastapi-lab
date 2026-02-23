# src/app/common/time.py
from datetime import datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")


def now_kst() -> datetime:
    # tz-aware datetime (KST)
    return datetime.now(tz=KST)
