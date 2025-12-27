# 統計値取得関数
from __future__ import annotations
from decimal import Decimal

def build_stats(total_hours: float, study_days: str):
    total_hours_val = float(total_hours or 0.0)
    days = int(study_days or 0)
    average_per_day = total_hours / days if days else 0.00

    return {
        'total_hours': f'{total_hours_val:.2f}' if total_hours_val else 0.00,
        'study_days': days,
        'average_per_day': f'{average_per_day:.2f}',
    }

