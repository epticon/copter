import aiohttp
import logging
import time
import asyncio
import json
from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory

from telemetary.handler import TelemetaryMessageHandler as Handler

try:
    import asyncio
except ImportError:
    import trollius as asyncio


class RemoteSwarmProtocol(WebSocketClientProtocol):
    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    async def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary is not True:
            Handler.process_message(self, str(payload.decode("utf8")))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


class BroadcastingService:
    def __init__(self, addresses=[]):
        self._factory = WebSocketClientFactory(addresses[0])
        self._factory.protocol = RemoteSwarmProtocol

    """
    Performs a fault tolerant connection (re-connects on diconnect).
    """

    def start(self, loop=asyncio.get_event_loop()):
        while True:
            coro = loop.create_connection(self._factory, "172.17.0.1", 9090)
            (server, _) = loop.run_until_complete(coro)

            try:
                loop.run_forever()
            except KeyboardInterrupt:
                break
            except Exception as e:
                logging.error(e)
                print("Attempting to reconnect in 5 seconds.")
                time.sleep(5)
            finally:
                server.close()

    def send_telemetary(self, attr_name, value):
        def send_json(json):
            pass

        print(attr_name)
        print(value)
        payload = {"route": "/telemetary", "data": {attr_name: value}}

        send_json(payload)
