## python func executes and returns data ##
def get_user_preference():
    """Return the user's appointment preferences."""

    return {
        "timezone": "Asia/kolkata",
        "preferred_duration": 30 
    }

def find_available_slots(date, duration, timezone):
    """Find available appointment slots."""

    slots = [
        {
            "slot_id": "slot_101",
            "date": "2026-10-19",
            "time": "14:00",
            "duration": 30
        },
        {
            "slot_id": "slot_102",
            "date": "2026-10-19",
            "time": "15:00",
            "duration": 30
        }
    ]

    available = [
        slot for slot in slots
        if slot["date"] == date and slot["duration"] == duration
    ]

    return {
        "timezone": timezone,
        "available_slots": available
    }


def book_appointment(slot_id, title):
    """Book an appointment in calendar"""

    return {
        "booking_id": "booking_001",
        "slot_id": slot_id,
        "title": title,
        "status": "confirmed"
    }
