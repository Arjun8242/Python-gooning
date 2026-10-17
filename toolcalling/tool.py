
# Mock calendar data shared by availability and booking tools
slots = [
    {
        "slot_id": "slot_101",
        "date": "2026-10-19",
        "time": "14:00",
        "duration": 30,
        "booked": False,
    },
    {
        "slot_id": "slot_102",
        "date": "2026-10-19",
        "time": "15:00",
        "duration": 30,
        "booked": False,
    },
]


def get_user_preference():
    """Return the user's appointment preferences."""
    return {
        "timezone": "Asia/Kolkata",
        "preferred_duration": 30,
    }


def find_available_slots(date, duration, timezone):
    """Find slots matching the requested date and duration."""
    available = [
        {
            "slot_id": slot["slot_id"],
            "date": slot["date"],
            "time": slot["time"],
            "duration": slot["duration"],
        }
        for slot in slots
        if slot["date"] == date
        and slot["duration"] == duration
        and not slot["booked"]
    ]

    return {
        "timezone": timezone,
        "available_slots": available,
    }


def book_appointment(slot_id, title):
    """Book a valid, currently available slot."""
    if not isinstance(title, str) or not title.strip():
        return {
            "ok": False,
            "error": "Appointment title is required.",
        }

    slot = next(
        (s for s in slots if s["slot_id"] == slot_id),
        None,
    )

    if slot is None:
        return {
            "ok": False,
            "error": f"Invalid slot ID: {slot_id}",
        }

    if slot["booked"]:
        return {
            "ok": False,
            "error": "This slot is already booked.",
        }

    slot["booked"] = True

    return {
        "ok": True,
        "booking_id": f"booking_{slot_id}",
        "slot_id": slot_id,
        "date": slot["date"],
        "time": slot["time"],
        "duration": slot["duration"],
        "title": title.strip(),
        "status": "confirmed",
    }
