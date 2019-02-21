import json
import logging

from .router.router import Router
from .exceptions import RouteMissingException

ROUTE = "route"


def route_key_exists(payload):
    json_payload = json.loads(payload)
    return ROUTE in json_payload


class TelemetaryMessageHandler:

    """
    Action to perform on any telemetary message recieved.
    """

    @staticmethod
    def process_message(client, payload):
        try:
            if route_key_exists(payload) == False:
                raise RouteMissingException

            # still confused at why this has to be done twice
            data = json.loads(json.loads(payload))
            Router(client).match(route=data[ROUTE], body=data)
        except Exception as err:
            logging.error(str(err))
