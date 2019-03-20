import time
from .commands import DroneCommand
from .listeners import attributes_listeners
from .custom_commands import CustomCommand
from dronekit import Vehicle, connect, VehicleMode


class Drone(DroneCommand):
    def __init__(self, address="tcp:172.17.0.1:5762"):
        self._address = address
        self._listener = None
        self._vehicle = None
        super(Drone, self).__init__(self._vehicle)

    """
    Arms the motors of the drone.
    """

    def arm_motors(self):
        # Performs a basic pre-arm check on drone.
        while not self._vehicle.is_armable:
            print("Waiting for vehicle to initialise...")
            time.sleep(1)

        print("Arming motors")
        self._vehicle.guided_mode()  # Copter should arm in GUIDED mode
        self._vehicle.armed = True
        self._vehicle.auto_mode()

    """
    Attempts to connect to drone with previously given address.
    """

    def connect(self):
        self._vehicle = connect(self._address, wait_ready=True)
        self.arm_motors()
        return self._vehicle

    """
    Sends a given MAVLINK command to the given drone.
    """

    def send_mavlink(self, mavlink_command):
        self._vehicle.send_mavlink(mavlink_command)

    def upload_mission(self, missions):
        """
        Uploads a given mission list to the drone. Also supports custom mission commands.
        """
        cmds = self._vehicle.commands
        for cmd in missions:
            if isinstance(cmd, CustomCommand):  # custom command
                cmd.exec(cmds)  # This is passed by reference.
            else:
                cmds.add(cmd)
        self._vehicle.commands.upload()

    """
    Subscribe to all of the drones attribute changes. The provided listener
    gets called on change.
    """

    def register_listeners(self, listener=None):
        self._listener = listener

        if listener is not None:
            for events in attributes_listeners:
                self._vehicle.add_attribute_listener(events, self._listener)

    """
    Unsubscribe to all of the drones attribute changes.
    """

    def unregister_listeners(self):
        if self._listener is not None:
            for event in attributes_listeners:
                self._vehicle.remove_attribute_listener(event, self._listener)

    """
    Print basic status of the drone to stdout.
    """

    def print_status(self):
        print("Get all vehicle attribute values:")
        print("Autopilot Firmware version: %s" % self._vehicle.version)
        print("Major version number: %s" % self._vehicle.version.major)
        print("Minor version number: %s" % self._vehicle.version.minor)
        print("Patch version number: %s" % self._vehicle.version.patch)
        print("Release type: %s" % self._vehicle.version.release_type())
        print("Release version: %s" % self._vehicle.version.release_version())
        print("Stable release?: %s" % self._vehicle.version.is_stable())

    """
    Close any existing connection with the drone.
    """

    def close(self):
        self._vehicle.close()
