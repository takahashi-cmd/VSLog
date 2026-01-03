# 統計値取得関数
from __future__ import annotations

def build_stats(total_hours: float, study_days: int):
    total_hours_val = float(total_hours or 0.0)
    days = int(study_days or 0)
    average_per_day = (total_hours_val / days) if days else 0.00

    return {
        'total_day': days,
        'total_hour': round(total_hours_val, 2),
        'avg_hour': round(average_per_day, 2),
    }

