import aiohttp
import logging


class BroadcastEvent:
    """
    Close a given connection
    """

    CLOSE = "CLOSE"

    """
    Close a given connection, and prevents further iteration over messages recieved.
    """
    CLOSE_AND_STOP_MESSAGE_ITERATION = "CLOSE_AND_STOP_MESSAGE_ITERATION"

    """
    Terminates any further iteration of message for the current message stream.
    """
    STOP_MESSAGE_ITERATION = "STOP_MESSAGE_ITERATION"

    """
    Indicates that a given client connection has been erminated.
    """
    TERMINATE = "TERMINATE"


class BroadcastingService:
    connection_pool = []

    def __init__(self, addresses=[], on_message=None):
        self._on_message = on_message
        self._addresses = addresses

    async def start(self):
        self._connection_pool = await self._map_connection(self._addresses)

    async def _map_connection(self, addresses):
        pool = []

        for address in iter(addresses):
            client = await self._establish_connection(address)

            if client is not None:
                pool.append(client)

        return pool

    async def _establish_connection(self, address):
        client = None

        try:
            connector = aiohttp.TCPConnector(verify_ssl=False, limit=1)

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.ws_connect(address) as client:
                    async for message in client:
                        response = await self._on_message(message, client)

                        if response is BroadcastEvent.STOP_MESSAGE_ITERATION:
                            break
                        elif response is BroadcastEvent.CLOSE:
                            await client.close()
                        elif (
                            response is BroadcastEvent.CLOSE_AND_STOP_MESSAGE_ITERATION
                        ):
                            await client.close()
                        elif (
                            response is BroadcastEvent.CLOSE_AND_STOP_MESSAGE_ITERATION
                        ):
                            break
                        elif response is BroadcastEvent.TERMINATE:
                            self._connection_pool.remove(client)
        except Exception as e:
            logging.error(e)

        return client

    def send_json(self, json):
        map(lambda client: client.send_json(json), self._connection_pool)

    def send_telemetary(self, attr_name, value):
        print(attr_name)
        print(value)
        payload = {"route": "/telemetary", "data": {attr_name: value}}

        self.send_json(payload)
