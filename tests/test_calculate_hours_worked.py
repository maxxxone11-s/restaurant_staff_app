from app.services.shift_service import calculate_hours_worked
from datetime import datetime

def test_calculate_hours_worked():
    open_shift = datetime(2026, 5, 23, 10, 0)
    closed_shift = datetime(2026, 5, 23, 18, 30)
    hors_worked = calculate_hours_worked(closed_shift, open_shift)

    assert hors_worked == 8.5