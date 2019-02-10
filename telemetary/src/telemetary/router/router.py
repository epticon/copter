import logging
import json

from endpoints import *


class TelemetaryRouter:
    routes = {
        EXECUTE_COMMAND: 'get_user'
    }

    def match(self, route, body=None, params=None):
        invalidRoute = "Invalid"
        event = TelemetaryRouter.routes.get(route, invalidRoute)
        if event is invalidRoute:
            raise invalidRoute

        try:
            # Executes the given function name.
            return eval('self.{}({}, {})'.format(event, body, params))
        except:
            logging.error("Invalid route action: {}".format(event))

    async def get_user(self, client, body=None, params=None,):
        await client.send_str(body + '/answer')