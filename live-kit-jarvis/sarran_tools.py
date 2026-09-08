"""Restricted tools for the Sarran AI booking agent."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, time, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo

from google_services import calendar_service
from livekit.agents import RunContext, function_tool

from sarran_knowledge import search_knowledge

EASTERN = ZoneInfo("America/New_York")
BUSINESS_START = time(9, 0)
BUSINESS_END = time(18, 0)


def _calendar_id() -> str:
    return os.getenv("SARRAN_CALENDAR_ID", "primary")


def _eastern(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=EASTERN)
    return value.astimezone(EASTERN)


def _round_up_half_hour(value: datetime) -> datetime:
    value = value.replace(second=0, microsecond=0)
    minutes = value.minute
    increment = 30 - (minutes % 30)
    if increment == 30:
        return value
    return value + timedelta(minutes=increment)


@function_tool
async def search_company_knowledge(
    context: RunContext,  # type: ignore
    query: str,
) -> str:
    """Search approved Sarran AI website and company material for an answer."""
    return search_knowledge(query)


@function_tool
async def find_available_times(
    context: RunContext,  # type: ignore
    start_time: str,
    end_time: str,
    duration_minutes: int = 30,
) -> str:
    """Find open time slots in the Sarran booking calendar within an ISO range."""
    try:
        start = _eastern(datetime.fromisoformat(start_time))
        end = _eastern(datetime.fromisoformat(end_time))
        if end <= start or duration_minutes <= 0:
            return "Please provide a valid availability range and appointment duration."
        service = calendar_service()
        busy_response = (
            service.freebusy()
            .query(
                body={
                    "timeMin": start.astimezone(timezone.utc).isoformat(),
                    "timeMax": end.astimezone(timezone.utc).isoformat(),
                    "items": [{"id": _calendar_id()}],
                }
            )
            .execute()
        )
        busy = busy_response["calendars"].get(_calendar_id(), {}).get("busy", [])
        busy_ranges = [
            (
                _eastern(datetime.fromisoformat(item["start"])),
                _eastern(datetime.fromisoformat(item["end"])),
            )
            for item in busy
        ]
        slots = []
        current_day = start.date()
        while current_day <= end.date() and len(slots) < 8:
            if current_day.weekday() >= 5:
                current_day += timedelta(days=1)
                continue
            day_start = datetime.combine(current_day, BUSINESS_START, EASTERN)
            day_end = datetime.combine(current_day, BUSINESS_END, EASTERN)
            cursor = _round_up_half_hour(max(start, day_start))
            latest_end = min(end, day_end)
            while (
                cursor + timedelta(minutes=duration_minutes) <= latest_end
                and len(slots) < 8
            ):
                slot_end = cursor + timedelta(minutes=duration_minutes)
                if not any(
                    cursor < busy_end and slot_end > busy_start
                    for busy_start, busy_end in busy_ranges
                ):
                    slots.append(
                        {
                            "start": cursor.isoformat(),
                            "end": slot_end.isoformat(),
                            "timezone": "America/New_York",
                        }
                    )
                cursor += timedelta(minutes=30)
            current_day += timedelta(days=1)
        return json.dumps({"timezone": "America/New_York", "slots": slots})
    except Exception as exc:
        logging.exception("Availability lookup failed")
        return f"Availability is temporarily unavailable: {exc}"


@function_tool
async def book_sarran_appointment(
    context: RunContext,  # type: ignore
    caller_name: str,
    caller_email: str,
    start_time: str,
    end_time: str,
    reason: str,
) -> str:
    """Create one confirmed booking on the Sarran calendar."""
    try:
        start = _eastern(datetime.fromisoformat(start_time))
        end = _eastern(datetime.fromisoformat(end_time))
        if (
            start.date() != end.date()
            or start.weekday() >= 5
            or start.time() < BUSINESS_START
            or end.time() > BUSINESS_END
            or end <= start
        ):
            return "Bookings are available only Monday through Friday from 9:00 AM to 6:00 PM Eastern."

        service = calendar_service()
        event = {
            "summary": f"Sarran AI discovery call - {caller_name}",
            "description": (
                f"Booked by the Sarran AI voice agent.\nCaller reason: {reason}"
            ),
            "start": {"dateTime": start.isoformat()},
            "end": {"dateTime": end.isoformat()},
            "attendees": [{"email": caller_email}],
        }
        created = (
            service.events()
            .insert(calendarId=_calendar_id(), body=event, sendUpdates="all")
            .execute()
        )
        return json.dumps(
            {
                "status": "booked",
                "event_id": created["id"],
                "start": start.isoformat(),
                "timezone": "America/New_York",
            }
        )
    except Exception as exc:
        logging.exception("Booking creation failed")
        return f"The booking could not be created: {exc}"
