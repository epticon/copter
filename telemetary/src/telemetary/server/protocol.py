from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory

from .handler import MessageHandler


class SwarmWebsocketProtocol(WebSocketClientProtocol):
    def drone(self):
        return self.factory.drone

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    async def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary is not True:
            MessageHandler.process_message(
                client=self, drone=self.drone(), payload=str(payload.decode("utf8"))
            )

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
