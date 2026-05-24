from datetime import datetime

def calculate_hours_worked(closed_shift, open_shift):
    delta = closed_shift - open_shift
    return delta.total_seconds() / 3600

open_shift = datetime(2026, 5, 23, 10, 0)
closed_shift = datetime(2026, 5, 23, 18, 30)

print(calculate_hours_worked(closed_shift, open_shift))