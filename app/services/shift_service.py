def calculate_hours_worked(shifts_user):
    response = []

    for shift in shifts_user:
        hours_worked = None
        
        if shift.closed_shift is not None:
            delta = shift.closed_shift - shift.open_shift
            hours_worked = delta.total_seconds() / 3600

        response.append({
            "id": shift.id,
            "user_id": shift.user_id,
            "open_shift": shift.open_shift,
            "closed_shift": shift.closed_shift,
            "revenue": shift.revenue,
            "hours_worked": hours_worked
        })

    return response