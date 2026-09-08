"""LiveKit entrypoint for the Sarran AI Solutions booking assistant."""

import os
import json
from datetime import datetime

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession, inference

from sarran_prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from sarran_tools import (
    book_sarran_appointment,
    find_available_times,
    search_company_knowledge,
)

load_dotenv(".env")

REBECCA_AVATAR_URL = "https://d8j0ntlcm91z4.cloudfront.net/user_3Eq04W7OgDWTPBa4nFYo1PJl4y7/hf_20260908_121947_e84f74de-73a9-4381-a3e9-2c1241da1d9f.png"


class SarranBookingAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            stt=inference.STT(model="deepgram/nova-3", language="multi"),
            llm=inference.LLM(
                model=os.getenv("SARRAN_LLM_MODEL", "google/gemma-4-31b-it")
            ),
            tts=inference.TTS(model="inworld/inworld-tts-2", voice="Victoria"),
            tools=[
                search_company_knowledge,
                find_available_times,
                book_sarran_appointment,
            ],
        )


server = AgentServer()


@server.rtc_session(agent_name=os.getenv("SARRAN_AGENT_NAME", "sarran-booking-agent"))
async def sarran_agent(ctx: agents.JobContext):
    session = AgentSession()
    await session.start(
        room=ctx.room,
        agent=SarranBookingAgent(),
    )
    await ctx.connect()
    await ctx.room.local_participant.set_name("Rebecca")
    await ctx.room.local_participant.set_metadata(
        json.dumps(
            {"avatar_url": REBECCA_AVATAR_URL, "role": "Sarran AI booking assistant"}
        )
    )
    now = datetime.now().astimezone().isoformat()
    await session.generate_reply(
        instructions=f"{SESSION_INSTRUCTION}\nCurrent local time: {now}"
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
