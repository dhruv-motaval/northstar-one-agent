from datetime import datetime
from typing import Dict, List, Any, Optional

def simulate_booking(date: str, time: str) -> dict:
    """
    Unavailable if the requested day is a Sunday, or the requested time is
    outside 10:00-18:00. Otherwise confirmed. Deterministic on purpose, so
    test cases can reliably trigger both the success and failure paths.
    """
    try:
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return {"status": "error", "message": "invalid date/time format"}

    if dt.weekday() == 6 or not (10 <= dt.hour < 18):
        alt1 = dt.replace(hour=11, minute=0)
        alt2 = dt.replace(hour=15, minute=0)
        return {
            "status": "unavailable",
            "alternative_slots": [
                alt1.strftime("%Y-%m-%d %H:%M"),
                alt2.strftime("%Y-%m-%d %H:%M"),
            ],
        }

    return {
        "status": "confirmed",
        "booking_reference": f"NS1-{dt.strftime('%Y%m%d%H%M')}",
    }

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "book_site_visit",
            "description": "Attempt to book a site visit once the customer has confirmed they want to visit and you have their name, phone number, and preferred date and time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Customer's full name"},
                    "phone": {"type": "string", "description": "Customer's phone number"},
                    "date": {"type": "string", "description": "Requested visit date, YYYY-MM-DD"},
                    "time": {"type": "string", "description": "Requested visit time, 24-hour HH:MM"},
                },
                "required": ["name", "phone", "date", "time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": "Flag this conversation for a human sales team member. Use when the customer explicitly asks for a human, has a complex negotiation, or is frustrated.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string", "description": "Short reason for escalation"},
                    "phone": {"type": "string", "description": "Customer's phone number if known"},
                },
                "required": ["reason"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mark_do_not_contact",
            "description": "Call the moment the customer asks to stop being contacted — e.g. 'don't call me again', 'remove my number', 'stop messaging me'.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_followup",
            "description": "Call when the customer is busy or wants to be contacted later, to record when and what to follow up about.",
            "parameters": {
                "type": "object",
                "properties": {
                    "preferred_time": {"type": "string", "description": "When they want to be contacted, in their own words, e.g. 'tomorrow evening'"},
                    "phone": {"type": "string", "description": "Customer's phone number if known"},
                    "note": {"type": "string", "description": "Any extra context for the follow-up"},
                },
                "required": ["preferred_time"],
            },
        },
    },
]
