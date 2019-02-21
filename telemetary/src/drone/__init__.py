from dronekit import Vehicle, connect
from .listeners import attributes_listeners


class Drone:
    def __init__(self, address="tcp:172.17.0.1:5762"):
        self._address = address
        self._listener = None

    """
        Attempts to connect to drone with previously given address
    """

    def connect(self):
        self._vehicle = connect(self._address, wait_ready=True)

        return self._vehicle

    """
        Sends a given MAVLINK command to the given drone.
    """

    def send_mavlink_command(self, command):
        self._vehicle.send_mavlink(command)

    """
        Sends a given In-built command to the given drone.
    """

    def send_raw_command(self, mavlink_command):
        self._vehicle.send_mavlink(mavlink_command)

    def register_listeners(self, listener=None):
        self._listener = listener

        if listener is not None:
            for events in attributes_listeners:
                self._vehicle.add_attribute_listener(events, self._listener)

    def unregister_listeners(self):
        if self._listener is not None:
            for event in attributes_listeners:
                self._vehicle.remove_attribute_listener(event, self._listener)

    def print_status(self):
        print("Get all vehicle attribute values:")
        print("Autopilot Firmware version: %s" % self._vehicle.version)
        print("Major version number: %s" % self._vehicle.version.major)
        print("Minor version number: %s" % self._vehicle.version.minor)
        print("Patch version number: %s" % self._vehicle.version.patch)
        print("Release type: %s" % self._vehicle.version.release_type())
        print("Release version: %s" % self._vehicle.version.release_version())
        print("Stable release?: %s" % self._vehicle.version.is_stable())
