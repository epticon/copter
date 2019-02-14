import aiohttp
import time
import logging
import sys
import json
import asyncio
import os

from drone import Drone
from services.broadcasting import BroadcastingService, BroadcastEvent
from .exceptions import InvalidIPV4Exception, FailedDroneConnectionException
from .handler import TelemetaryMessageHandler as Handler


class Telemetary:
    def __init__(self, addresses):
        if type(addresses) is not type(list()):
            raise InvalidIPV4Exception

        self._addresses = addresses
        self._vehicle = None
        self._drone = None
        self._broadcaster = None

    async def start(self):
        while True:
            logging.log(1, "Attempting to connect...")

            try:
                (self._drone, self._vehicle) = Telemetary.connect_to_drone()

                self._broadcaster = BroadcastingService(
                    self._addresses, Telemetary.on_message
                )

                await self._broadcaster.start()

                self._drone.register_listener(self._broadcaster.send_telemetary)
            except Exception as e:
                logging.error(e)
                time.sleep(10)

    @staticmethod
    def connect_to_drone():
        vehicle = None

        while vehicle is None:
            try:
                drone = Drone(os.getenv("DRONE_ADDRESS", "tcp:172.17.0.1:5762"))
                vehicle = drone.connect()

                while vehicle.version.major is None:
                    time.sleep(2)

                drone.print_status()

                return (drone, vehicle)
            except Exception as e:
                logging.error(e)
                time.sleep(5)

    """
    Action to perform on any telemetary message recieved.
    """

    @staticmethod
    async def on_message(message, client):
        if message.type == aiohttp.WSMsgType.TEXT:
            return Handler.process_message(message.data)

        elif message.type == aiohttp.WSMsgType.ERROR or message:
            logging.error(message)

        elif message.type == aiohttp.WSMsgType.CLOSED or message:
            return BroadcastEvent.TERMINATE
