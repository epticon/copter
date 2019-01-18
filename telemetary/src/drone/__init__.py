from dronekit import Vehicle, connect
from .listeners import attributes_listeners


class Drone:
    def __init__(self, address='127.0.0.1:14550'):
        self.address = address

    """
        Attempts to connect to drone with previously given address
    """

    def connect(self):
        vh = connect(self.address, wait_ready=True)
        self.vehicle = vh

    """
        Sends a given MAVLINK command to the given drone.
    """

    def send_mavlink_command(self, command):
        self.vehicle.send_mavlink(command)

    """
        Sends a given In-built command to the given drone.
    """

    def send_raw_command(self, mavlink_command):
        self.vehicle.send_mavlink(mavlink_command)

    def register_listener(self, listener=None):
        if listener is not None:
            for events in attributes_listeners:
                self.vehicle.add_attribute_listener(events, listener)
