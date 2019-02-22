import aiohttp
import logging
import time
import asyncio
import json
from autobahn.asyncio.websocket import WebSocketClientFactory

from utils.formatting import create_websocket_url
from .protocol import SwarmWebsocketProtocol

try:
    import asyncio
except ImportError:
    import trollius as asyncio


class TelemetaryServer:
    def __init__(self, address, port, path, drone):
        self._drone = drone
        self._address = address
        self._port = port
        self._path = path

        self._factory = WebSocketClientFactory(
            create_websocket_url(address, port, path)
        )
        self._factory.protocol = SwarmWebsocketProtocol

    """
    Performs a fault tolerant connection (re-connects on diconnect).
    """

    def start(self, loop=asyncio.new_event_loop()):
        # This lambda function is defined to enable coercing the drone
        # state changes, before forwarding to the remote server.
        sendTelemetary = lambda vehicle, attr_name, value: self._send_telemetary(
            vehicle, attr_name, value
        )

        while True:
            coro = loop.create_connection(self._factory, self._address, self._port)
            (self._server, self._transport) = loop.run_until_complete(coro)

            try:
                self._drone.register_listeners(sendTelemetary)

                # Another approach that might be possible, is to run_forever
                # on a seperate process. Although, where I feel there might
                # be challenges, is when we need to acces the drone object,
                # which currently is in another process
                loop.run_forever()
            except KeyboardInterrupt:
                break
            except Exception as e:
                logging.error(e)
                print("Attempting to reconnect in 5 seconds.")
                time.sleep(5)
            finally:
                self._drone.unregister_listeners()
                self._server.close()

    """
    Fowards a drone telemetary message to the remote server.
    """

    def _send_telemetary(self, vehicle, attr_name, value):
        payload = {"route": "/telemetary", "data": {attr_name: f"{value}"}}
        self._transport.sendMessage(json.dumps(payload).encode("utf8"))
