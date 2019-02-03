import aiohttp
import time
import logging
import sys
import json

from drone import Drone
from services.broadcasting import BroadcastingService, BroadcastEvent
from .exceptions import InvalidIPV4Exception
from .handler import TelemetaryMessageHandler


class Telemetary:
    def __init__(self, addresses=[]):
        self.drone = Drone()

        if type(addresses) is not type(list()):
            raise InvalidIPV4Exception

        try:
            while self.drone.connect() is False:
                time.sleep(10)  # utilize exponential backoff algo
                self.broadcast_connection = BroadcastingService(
                    addresses, self.on_message
                )
                self.drone.register_listener(self.broadcast_telemetary)
        except (Exception):
            pass
            # logging.error(sys.exc_info()[0])

    def broadcast_telemetary(self, attr_name, value):
        # post to /telemetary path here i.e. add it to the json
        payload = {attr_name: value}
        self.broadcast_connection.send_json(payload)

    """
    Action to perform on any telemetary message recieved.
    """
    async def on_message(self, message, client):
        if message.type == aiohttp.WSMsgType.TEXT:
            return TelemetaryMessageHandler.handle_message(message.data)

        elif message.type == aiohttp.WSMsgType.ERROR or message:
            logging.error(message)

        elif message.type == aiohttp.WSMsgType.CLOSED or message:
            return BroadcastEvent.TERMINATE
