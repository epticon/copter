import logging
import json

from .endpoints import EXECUTE_COMMAND
from utils import loaders


"""
Dynamically load a class from a string.
"""


class Router:
    def __init__(self, client, routes, controller_path="telemetary.controller"):
        self._client = client
        self._routes = routes
        self._controller_path = controller_path

    def match(self, route, body=None, params=None):
        try:
            return loaders.instantiate_controller_method(
                module_path=self._controller_path,
                controller_and_method=self._routes[route],
                client=self._client,
                body=body,
                params=params,
            )

        except IndexError:
            logging.error("Invalid route specified: {}".format(route))
        except Exception as err:
            logging.error(err)
