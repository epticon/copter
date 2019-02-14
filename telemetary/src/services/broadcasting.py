import aiohttp


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
