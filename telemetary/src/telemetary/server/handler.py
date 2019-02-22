import json
import logging
import os

from ..router.router import Router
from utils.route_validation import *
from ..exceptions import RouteMissingException

ROUTES_PATH = os.path.abspath(os.path.dirname(__file__)) + "/../routes.json"


class MessageHandler:
    @staticmethod
    def get_routes():
        with open(ROUTES_PATH) as file:
            return json.load(file)

        return {}

    """
    Action to perform on any telemetary message recieved.
    """

    @staticmethod
    def process_message(client, payload):
        try:
            MessageHandler.validate(payload)
            # Still confused at why json.loads() has to be done twice.
            data = json.loads(json.loads(payload))

            router = Router(client, MessageHandler.get_routes())
            router.match(route=data[ROUTE], body=data)

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
