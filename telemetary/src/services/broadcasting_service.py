import aiohttp


class BroadcastEvent:
    CLOSE = "CLOSE"
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

    async def __init__(self, server_addresses=[], on_message=None):
        self.__session = aiohttp.ClientSession()
        self.__on_message = on_message
        self.__server_addresses = server_addresses

    def start(self):
        self.connection_pool = list(
            filter(
                lambda x: x is not None,
                map(self.__establish_connection, self.__server_addresses)
            )
        )

    async def __establish_connection(self, address):
        client = None

        try:
            client = self.__session.ws_connect(address)

            for message in client:
                response = self.__on_message(message, client)

                if response is BroadcastEvent.STOP_MESSAGE_ITERATION:
                    break
                elif response is BroadcastEvent.CLOSE:
                    await client.close()
                elif response is BroadcastEvent.CLOSE_AND_STOP_MESSAGE_ITERATION:
                    await client.close()
                    break
                elif response is BroadcastEvent.TERMINATE:
                    self.connection_pool.remove(client)
        except:
            self.connection_pool.remove(client)

    async def send_json(self, json):
        await map(lambda client: client.send_json(json), self.connection_pool)
