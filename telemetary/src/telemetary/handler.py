import json

from .router.router import TelemetaryRouter as Router
from services.broadcasting import BroadcastEvent
from .exceptions import RouteMissingException


class TelemetaryMessageHandler:
    @staticmethod
    def process_message(message):
        try:
            request = TelemetaryMessageHandler.validate_message(message)
            return Router().match(route=request.route, body=request)
        except RouteMissingException as e:
            print("Route is missing.")
            pass

    @staticmethod
    def validate_message(message):
        json_message = json.loads(message)

        if "route" not in json_message:
            print("not in")
            raise RouteMissingException
        else:
            print(json_message)

        return json_message

    @staticmethod
    def handle_drone_command(client):
        # Pilot sends a command to be executed on the drone
        return BroadcastEvent.CLOSE_AND_STOP_MESSAGE_ITERATION
