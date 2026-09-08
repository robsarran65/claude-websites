from dotenv import load_dotenv

from livekit import agents
from livekit.agents import (
    AgentServer,
    AgentSession,
    Agent,
    inference,
    room_io,
    TurnHandlingOptions,
    ChatContext,
)
from livekit.plugins import google
from livekit.plugins.noise_cancellation import NC
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import (
    get_weather,
    search_web,
    send_email,
    list_emails,
    read_email,
    list_calendar_events,
    create_calendar_event,
    delete_calendar_event,
    power_off,
)
from mem0 import AsyncMemoryClient
from datetime import datetime
import json
import logging

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self, chat_ctx=None) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            stt=inference.STT(model="deepgram/nova-3", language="multi"),
            llm=inference.LLM(model="google/gemma-4-31b-it"),
            tts=inference.TTS(
                model="inworld/inworld-tts-2",
                voice="Victoria",
            ),
            turn_handling=TurnHandlingOptions(
                turn_detection=inference.TurnDetector(),
            ),
            tools=[
                get_weather,
                search_web,
                send_email,
                list_emails,
                read_email,
                list_calendar_events,
                create_calendar_event,
                delete_calendar_event,
                power_off,
            ],
            chat_ctx=chat_ctx,
        )


server = AgentServer()


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: agents.JobContext):
    session = AgentSession()

    mem0 = AsyncMemoryClient()
    user_name = "Robert"

    response = await mem0.get_all(filters={"user_id": user_name})
    results = response.get("results", [])
    initial_ctx = ChatContext()
    memory_str = ""

    if results:
        memories = [
            {"memory": result["memory"], "updated_at": result["updated_at"]}
            for result in results
        ]
        memory_str = json.dumps(memories)
        logging.info(f"Memories: {memory_str}")
        initial_ctx.add_message(
            role="assistant",
            content=f"The user's name is {user_name}, and this is relevant context about him: {memory_str}",
        )

    await session.start(
        room=ctx.room,
        agent=Assistant(chat_ctx=initial_ctx),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=NC(),
            ),
            video_input=True,
        ),
    )

    await ctx.connect()

    current_time = datetime.now().astimezone().isoformat()
    await session.generate_reply(
        instructions=f"{SESSION_INSTRUCTION}\n\nThe current date and time is {current_time}. "
        "Use it to resolve relative dates like 'tomorrow' or 'next Friday' into exact "
        "ISO 8601 timestamps when creating calendar events.",
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
