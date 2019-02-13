import asyncio
import config.settings
from telemetary import Telemetary
from dotenv import load_dotenv
from dronekit import connect
import os

BROADCAST_ADDRESSES = os.getenv("TELEMETARY_BROADCAST_SERVERS", "").split(",")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    telemetary = Telemetary(BROADCAST_ADDRESSES)
    loop.run_until_complete(telemetary.start())
