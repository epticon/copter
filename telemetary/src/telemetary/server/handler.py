import json
import logging

from ..router.router import Router
from ..exceptions import RouteMissingException

ROUTE = "route"
MESSAGE = "message"


def route_key_exists(payload):
    return ROUTE in payload


def is_error_message(payload):
    return "message" in payload


class MessageHandler:

    """
    Action to perform on any telemetary message recieved.
    """

    @staticmethod
    def process_message(client, payload):
        try:
            MessageHandler.validate(payload)

            # Still confused at why json.loads() has to be done twice.
            data = json.loads(json.loads(payload))
            Router(client).match(route=data[ROUTE], body=data)
        except Exception as err:
            logging.error(str(err))

    @staticmethod
    def validate(payload):
        payload = json.loads(payload)
        error = None

        if is_error_message(payload):
            error = f"Server: {payload[MESSAGE]}"
        elif route_key_exists(payload) == False:
            error = f"Client: {str(RouteMissingException())}"
        else:
            return None

        raise Exception(error)
