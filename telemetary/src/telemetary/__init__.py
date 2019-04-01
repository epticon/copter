import aiohttp
import time
import logging
import sys
import json
import asyncio
import os

from drone import Drone
from .server import TelemetaryServer
from . import controller


def connect_to_drone(address):
    vehicle = None

    while vehicle is None:
        try:
            drone = Drone(address)
            vehicle = drone.connect()

            while vehicle.version.major is None:
                time.sleep(2)

            drone.print_status()
            return drone

        except Exception as e:
            logging.error(e)


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
        while True:
            print("Attempting to connect...")
            self._drone = None

            try:
                self._drone = connect_to_drone(self._drone_address)
                server = TelemetaryServer(
                    address=self._broadcast_address,
                    port=self._broadcast_port,
                    path=self._broadcast_path,
                    drone=self._drone,
                )

                server.start(asyncio.get_event_loop())

            except Exception as e:
                self._drone.close()
                logging.error(e)
                time.sleep(5)
