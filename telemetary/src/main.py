import asyncio
import config.settings
from telemetary import Telemetary
from dotenv import load_dotenv
from dronekit import connect
import os

BROADCAST_ADDRESS = os.getenv("BROADCAST_ADDRESS", "127.0.0.1")
BROADCAST_PORT = os.getenv("BROADCAST_PORT", 8080)
BROADCAST_PATH = os.getenv("BROADCAST_PATH", "/ws")
DRONE_ADDRESS = os.getenv("DRONE_ADDRESS", "tcp:172.17.0.1:5762")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # Improve upon this and use **kwargs
    telemetary = Telemetary(
        drone_address=DRONE_ADDRESS,
        broadcast_address=BROADCAST_ADDRESS,
        broadcast_port=BROADCAST_PORT,
        broadcast_path=BROADCAST_PATH,
    )

    loop.run_until_complete(telemetary.start())
