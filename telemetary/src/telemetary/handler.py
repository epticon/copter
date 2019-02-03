import json

from .router.router import TelemetaryRouter as Router
from services.broadcasting import BroadcastEvent


class TelemetaryMessageHandler:
    @staticmethod
    def handle_message(message):
        request_info = TelemetaryMessageHandler.parse_drone_command(
            message.data
        )

        return Router().match(request_info["route"])

    @staticmethod
    def parse_drone_command(message_data):
        message_parts = message_data.split(' ')

        if len(message_parts) is 0 or \
                len(message_parts[0]) is 0 or \
                message_parts[0][0] is not '/':
            raise 'Route missing'

        route = message_parts[0]
        if message_parts > 1:
            return {"route": route, "data": json.load(message_parts[1])}

        return {"route": route}

    @staticmethod
    def __handle_drone_command(client):
        # Pilot sends a command to be executed on the drone
        return BroadcastEvent.CLOSE_AND_STOP_MESSAGE_ITERATION
