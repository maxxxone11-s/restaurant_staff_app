def calculate_hours_worked(closed_shift, open_shift):
    delta = closed_shift - open_shift
    return delta.total_seconds() / 3600

def create_shift_response_list(shifts_user):
    response = []

    for shift in shifts_user:
        hours_worked = None
        if shift.closed_shift is not None:
            hours_worked = calculate_hours_worked(shift.closed_shift, shift.open_shift)

        response.append({
            "id": shift.id,
            "user_id": shift.user_id,
            "open_shift": shift.open_shift,
            "closed_shift": shift.closed_shift,
            "revenue": shift.revenue,
            "hours_worked": hours_worked
        })

    return response