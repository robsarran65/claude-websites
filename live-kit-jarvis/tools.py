import asyncio
import base64
import json
import logging
import os
import smtplib
import sys
from datetime import datetime, timezone
from ssl import create_default_context
from typing import Optional

from livekit.agents import function_tool, RunContext
import requests
from duckduckgo_search import DDGS

from google_services import gmail_service, calendar_service


@function_tool
async def get_weather(
    context: RunContext,  # type: ignore
    city: str,
) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            return response.text.strip()
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}."


@function_tool
async def search_web(
    context: RunContext,  # type: ignore
    query: str,
) -> str:
    """
    Search the web using DuckDuckGo.
    """
    try:
        results = DDGS().text(query, max_results=5)
        return "\n".join(r["body"] for r in results)
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."


@function_tool
async def send_email(
    context: RunContext,  # type: ignore
    to_email: str,
    subject: str,
    message: str,
    cc_email: Optional[str] = None,
) -> str:
    """
    Send an email through Gmail SMTP.

    Args:
        to_email: Recipient email address
        subject: Email subject line
        message: Email body content
        cc_email: Optional CC email address
    """
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Get credentials from environment variables
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv(
            "GMAIL_APP_PASSWORD"
        )  # Use App Password, not regular password

        if not gmail_user or not gmail_password:
            return "Gmail credentials not configured. Set GMAIL_USER and GMAIL_APP_PASSWORD."

        # Create SSL context
        ssl_context = create_default_context()

        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=ssl_context)
            server.login(gmail_user, gmail_password)

            # Build email
            email_body = f"Subject: {subject}\n\n{message}"
            recipients = [to_email]
            if cc_email:
                recipients.append(cc_email)

            server.sendmail(gmail_user, recipients, email_body)

        logging.info(f"Email sent to {to_email} with subject: {subject}")
        return f"Email sent successfully to {to_email}"

    except Exception as e:
        logging.error(f"Error sending email to {to_email}: {e}")
        return f"An error occurred while sending email to {to_email}: {e}"


@function_tool
async def list_emails(
    context: RunContext,  # type: ignore
    max_results: int = 5,
) -> str:
    """
    List the most recent emails in the inbox, with sender, subject, and a short snippet.
    Use the "id" of an email from this list with read_email to read its full content.
    """
    try:
        service = gmail_service()
        listing = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX"], maxResults=max_results)
            .execute()
        )
        emails = []
        for item in listing.get("messages", []):
            msg = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=item["id"],
                    format="metadata",
                    metadataHeaders=["From", "Subject"],
                )
                .execute()
            )
            headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
            emails.append(
                {
                    "id": item["id"],
                    "from": headers.get("From", "Unknown"),
                    "subject": headers.get("Subject", "(no subject)"),
                    "snippet": msg.get("snippet", ""),
                }
            )
        return json.dumps(emails)
    except Exception as e:
        logging.error(f"Error listing emails: {e}")
        return "An error occurred while listing emails."


def _extract_email_body(payload) -> str:
    """Recursively find the first text/plain part of a Gmail message payload."""
    if payload.get("mimeType") == "text/plain" and payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode(
            "utf-8", errors="replace"
        )
    for part in payload.get("parts", []) or []:
        found = _extract_email_body(part)
        if found:
            return found
    return ""


@function_tool
async def read_email(
    context: RunContext,  # type: ignore
    email_id: str,
) -> str:
    """
    Read the full sender, subject, and body text of one email, given its id from list_emails.
    """
    try:
        service = gmail_service()
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=email_id, format="full")
            .execute()
        )
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        body = _extract_email_body(msg["payload"]) or msg.get("snippet", "")
        return f"From: {headers.get('From')}\nSubject: {headers.get('Subject')}\n\n{body}"
    except Exception as e:
        logging.error(f"Error reading email {email_id}: {e}")
        return "An error occurred while reading that email."


@function_tool
async def list_calendar_events(
    context: RunContext,  # type: ignore
    max_results: int = 10,
) -> str:
    """
    List upcoming calendar events, soonest first.
    Use the "id" of an event from this list with delete_calendar_event to cancel it.
    """
    try:
        service = calendar_service()
        now = datetime.now(timezone.utc).isoformat()
        events = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
            .get("items", [])
        )
        result = [
            {
                "id": e["id"],
                "summary": e.get("summary", "(no title)"),
                "start": e["start"].get("dateTime", e["start"].get("date")),
                "end": e["end"].get("dateTime", e["end"].get("date")),
            }
            for e in events
        ]
        return json.dumps(result)
    except Exception as e:
        logging.error(f"Error listing calendar events: {e}")
        return "An error occurred while listing calendar events."


@function_tool
async def create_calendar_event(
    context: RunContext,  # type: ignore
    summary: str,
    start_time: str,
    end_time: str,
    description: Optional[str] = None,
    location: Optional[str] = None,
) -> str:
    """
    Create a calendar event.

    Args:
        summary: Title of the event
        start_time: ISO 8601 start datetime, e.g. 2026-09-10T15:00:00-04:00
        end_time: ISO 8601 end datetime, e.g. 2026-09-10T16:00:00-04:00
        description: Optional event description
        location: Optional event location
    """
    try:
        service = calendar_service()
        event = {
            "summary": summary,
            "start": {"dateTime": start_time},
            "end": {"dateTime": end_time},
        }
        if description:
            event["description"] = description
        if location:
            event["location"] = location

        service.events().insert(calendarId="primary", body=event).execute()
        return f"Event '{summary}' created for {start_time}."
    except Exception as e:
        logging.error(f"Error creating calendar event: {e}")
        return "An error occurred while creating the calendar event."


@function_tool
async def delete_calendar_event(
    context: RunContext,  # type: ignore
    event_id: str,
) -> str:
    """Delete/cancel a calendar event, given its id from list_calendar_events."""
    try:
        service = calendar_service()
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return "Event deleted successfully."
    except Exception as e:
        logging.error(f"Error deleting calendar event {event_id}: {e}")
        return "An error occurred while deleting the calendar event."


@function_tool
async def power_off(
    context: RunContext,  # type: ignore
) -> str:
    """
    Shut down the Jarvis agent server process.
    Use when the user says "power off", "go rest", "sleep", or similar.
    """

    async def _shutdown():
        await asyncio.sleep(5)
        logging.info("Powering off Jarvis agent server.")
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(0)

    asyncio.create_task(_shutdown())
    return "Powering off now. Goodbye, sir."
