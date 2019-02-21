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


def connect_to_drone(address):
    vehicle = None

    while vehicle is None:
        try:
            drone = Drone(address)
            vehicle = drone.connect()

            while vehicle.version.major is None:
                time.sleep(2)

            drone.print_status()
            return (drone, vehicle)

        except Exception as e:
            logging.error(e)
            time.sleep(5)


class Telemetary:
    def __init__(self, **kwargs):
        self._drone_address = kwargs.get("drone_address", "tcp:127.0.0.1:5762")
        self._broadcast_address = kwargs.get("broadcast_address", "127.0.0.1")
        self._broadcast_port = kwargs.get("broadcast_port", 8080)
        self._broadcast_path = kwargs.get("broadcast_path", "/ws")

        # Perform validation of all the above addresses
        self._vehicle = None
        self._drone = None

    def start(self):
        loop = asyncio.get_event_loop()

        while True:
            print("Attempting to connect...")
            self._drone = None
            self._vehicle = None

            try:
                (self._drone, self._vehicle) = connect_to_drone(self._drone_address)

                # Start broadcating server
                broadcast = BroadcastingService(
                    address=self._broadcast_address,
                    port=self._broadcast_port,
                    path=self._broadcast_path,
                )

                broadcast.start(loop)

                # self._drone.register_listener(self._broadcaster.send_telemetary)
            except Exception as e:
                logging.error(e)
                loop.close()
                time.sleep(5)
