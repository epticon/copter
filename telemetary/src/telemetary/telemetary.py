import aiohttp
import time
import logging
import sys

from drone import Drone
from services.broadcasting_service import *
from .exceptions import InvalidIPV4Exception


class Telemetary:
    def __init__(self, addresses=[]):
        self.drone = Drone()

        if type(addresses) is not type(list()):
            raise InvalidIPV4Exception

        try:
            while self.drone.connect() is False:
                time.sleep(10)  # utilize exponential backoff algo
                self.broadcast_connection = BroadcastingService(addresses)
                self.drone.register_listener(self.broadcast_telemetary)
        except (Exception):
            pass
            # logging.error(sys.exc_info()[0])

    def broadcast_telemetary(self, attr_name, value):
        payload = {attr_name: value}
        self.broadcast_connection.send_json(payload)

    """
    Action to perform on any telemetary message recieved.
    """

    async def on_message(self, message, client):
        if message.type == aiohttp.WSMsgType.TEXT:
            if message.data == "close cmd":
                return BroadcastEvent.CLOSE_AND_STOP_MESSAGE_ITERATION
            else:
                await client.send_str(message.data + '/answer')

        elif message.type == aiohttp.WSMsgType.ERROR or message:
            logging.error(message)

        elif message.type == aiohttp.WSMsgType.CLOSED or message:
            return BroadcastEvent.TERMINATE
