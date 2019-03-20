from functools import partial
from .base_controller import BaseController
from drone.commands import DroneCommand
from utils.mavlink_mission_parser import MavlinkMissionParser


def to_dict(args):
    if isinstance(args, str):
        return dict()
    return dict(args)


def get_key(value):
    if isinstance(value, str) == False:
        return list(value)[0]
    return value


def upload_mission(cmd, drone):
    drone.upload_mission(MavlinkMissionParser.from_string(cmd))


def execute_single_command(cmd, drone):
    key = get_key(cmd)
    args = to_dict(cmd).get(key, {})
    switch = {
        "land": partial(drone.land),
        "auto_mode": partial(drone.auto_mode),
        "guided_mode": partial(drone.guided_mode),
        "set_home": partial(drone.set_home, **args),
        "clear_command": partial(drone.clear_command),
        "navigate_to": partial(drone.navigate_to, **args),
        "return_home": partial(drone.return_home, **args),
        "set_flight_height": partial(drone.set_flight_height, **args),
    }

    switch.get(key, lambda: None)()


class CommandController(BaseController):
    def __init__(self, client, drone, body, args):
        super(CommandController, self).__init__(client, drone, body, args)

    def process_command(self, req, res):
        try:
            switch = {
                "mission": partial(upload_mission),
                "single": partial(execute_single_command),
            }

            instruction = req["body"]["instruction"]
            key = get_key(instruction)
            args = {"cmd": instruction[key], "drone": self._drone}
            switch.get(key, lambda x, y: None)(**args)

        except (IndexError):
            print("No value for instruction was provided.")
