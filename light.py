from dotenv import load_dotenv

from pywizlight import wizlight, PilotBuilder

import asyncio
import os

load_dotenv()

LIGHT_IP = os.getenv('LIGHT_IP')
LIGHT_PORT = os.getenv('LIGHT_PORT')
SKIP_LIGHT = os.getenv('SKIP_LIGHT')

async def async_turn_on_light():
    if SKIP_LIGHT == 'true' or SKIP_LIGHT == '1':
        return

    if LIGHT_IP is None:
        raise ValueError("LIGHT_IP environment variable not set")
    if LIGHT_PORT is None:
        raise ValueError("LIGHT_PORT environment variable not set")

    light = wizlight(LIGHT_IP, port=int(LIGHT_PORT))

    await light.turn_on(PilotBuilder(
        brightness=255,
        rgb=(100, 0, 0)
    ))

def sync_turn_on_light() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_turn_on_light())
