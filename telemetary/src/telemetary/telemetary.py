import aiohttp
import time
import logging
import sys
import json
import asyncio
import os

from drone import Drone
from services.broadcasting import BroadcastingService
from .exceptions import InvalidIPV4Exception, FailedDroneConnectionException


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


class Telemetary:
    def __init__(self, addresses):
        if type(addresses) is not type(list()):
            raise InvalidIPV4Exception

        self._addresses = addresses
        self._vehicle = None
        self._drone = None

    def start(self):
        loop = asyncio.get_event_loop()

        while True:
            print("Attempting to connect...")
            self._drone = None
            self._vehicle = None
            try:
                # Start drone
                (self._drone, self._vehicle) = connect_to_drone()

                # Start broadcating server
                BroadcastingService(self._addresses).start(loop)

                # self._drone.register_listener(self._broadcaster.send_telemetary)
            except Exception as e:
                logging.error(e)
                loop.close()
                time.sleep(5)
