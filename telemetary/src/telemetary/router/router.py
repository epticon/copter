import logging
import json
from .endpoints import EXECUTE_COMMAND

routes = {"/command": "get_user"}


class Router:
    def __init__(self, client):
        self._client = client

    def match(self, route=None, body=None, params=None):
        try:
            eval("self.{}({}, {})".format(routes[route], body, params))
        except IndexError:
            logging.error("Invalid route specified: {}".format(route))
        except Exception as err:
            logging.error(err)

    def get_user(self, body=None, params=None):
        print("sending message from `get_user`")
        try:
            self._client.sendMessage("response")
        except Exception as err:
            logging.error(err)
