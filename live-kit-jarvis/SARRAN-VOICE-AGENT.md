# Sarran voice agent

Run the booking-only agent with:

```powershell
python sarran_agent.py dev
```

The existing `agent.py` Jarvis entrypoint is unchanged. The Sarran agent exposes only approved
knowledge lookup, calendar availability, and confirmed booking tools.

## Configuration

Add these values to `.env` as needed:

```text
SARRAN_KNOWLEDGE_DIR=C:\Users\rober\claude-websites\sarran-ai
SARRAN_CALENDAR_ID=primary
SARRAN_AGENT_NAME=sarran-booking-agent
SARRAN_LLM_MODEL=gemma3:4b
SARRAN_OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
```

The local Sarran agent uses Ollama's OpenAI-compatible endpoint. Install the model once with
`ollama pull gemma3:4b`; no paid LLM API key is required for local inference.

The existing Google OAuth setup must be completed with `python google_auth_setup.py`. The OAuth
token is local-only and must never be committed. The current Google scope includes Gmail because
the legacy Jarvis agent uses it; a production Sarran deployment should use a separate OAuth client
with Calendar-only scope if the provider supports it.

## Booking behavior

- 30-minute discovery calls are checked against Google Calendar availability.
- The caller must provide name, email, and reason for calling.
- The agent repeats the slot and requires explicit confirmation before creating an event.
- Events are created on `SARRAN_CALENDAR_ID` and invite the caller by email.
- The agent cannot read email, delete events, cancel bookings, take payment, or invent answers.

Telephony, SIP routing, WhatsApp notifications, and website CTAs are intentionally separate from
this first agent slice and should be added only after private call testing succeeds.