import time
from .commands import DroneCommand
from .listeners import attributes_listeners
from .custom_commands import CustomCommand
from dronekit import Vehicle, connect, VehicleMode, Command, mavutil

INITIAL_TAKEOFF_HEIGHT = 20


class Drone(DroneCommand):
    def __init__(self, address="tcp:172.17.0.1:5762"):
        self._address = address
        self._listener = None
        self._vehicle = None
        super(Drone, self).__init__(self._vehicle)

    @property
    def altitude(self):
        return self._vehicle.location.global_relative_frame.alt

    @property
    def no_of_commands(self):
        """
        Total number of mission commands currently on the drone

        Returns:
            int -- No of commands in drone's CommandSequence
        """
        cmds = self.download_commands()
        return cmds.count

    @property
    def mission_completed(self):
        """Checks if a drone has completed all of its mission commands

        Returns:
            Boolean -- Has completed all mission commands
        """
        return self._vehicle.commands.next == 0

    def connect(self):
        """
        Attempts to connect to drone with previously given address.
        """
        self._vehicle = connect(self._address, wait_ready=True)
        self._prepare_for_mission()
        return self._vehicle

    def _prepare_for_mission(self):
        """
        Prepare drone for mission mode on connecting to the drone.
        """
        if self.no_of_commands == 0:
            # Add a takeoff command
            takeoff = mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
            frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
            cmd = Command(
                0, 0, 0, frame, takeoff, 0, 0, 0, 0, 0, 0, 0, 0, INITIAL_TAKEOFF_HEIGHT
            )
            self.upload_mission([cmd], continue_flight=False)

        self.arm_motors()
        if self.altitude < 1:
            self.take_off(INITIAL_TAKEOFF_HEIGHT)
        self.auto_mode()

    def send_mavlink(self, mavlink_command):
        """
        Sends a given MAVLINK command to the given drone.
        """
        self._vehicle.send_mavlink(mavlink_command)

    def upload_mission(self, missions, continue_flight=True):
        """
        Uploads a given mission list to the drone. Also supports custom mission commands.
        """
        if len(missions) == 0:
            return

        cmds_handler = self.download_commands()
        for cmd in missions:
            if isinstance(cmd, CustomCommand):  # custom command
                cmd.exec(cmds_handler)  # This is passed by reference.
            else:
                cmds_handler.add(cmd)
        cmds_handler.upload()

        if continue_flight == True:
            self.continue_mission(next=self._vehicle.commands.next)

    def continue_mission(self, next=0):
        """
        Proceeds with mission execution, i.e. continues mission from `next`.

        Keyword Arguments:
            next {int} -- Index of mission command to execute in the CommandSequence (default: {0})
        """
        self.guided_mode()
        if self.mission_completed == True:
            self._vehicle.commands.next = next
        self.auto_mode()

    def register_listeners(self, listener=None):
        """
        Subscribe to all of the drones attribute changes. The provided listener
        gets called on change.
        """
        self._listener = listener
        if listener is not None:
            for events in attributes_listeners:
                self._vehicle.add_attribute_listener(events, self._listener)

    def unregister_listeners(self):
        """
        Unsubscribe to all of the drones attribute changes.
        """
        if self._listener is not None:
            for event in attributes_listeners:
                self._vehicle.remove_attribute_listener(event, self._listener)

    def print_status(self):
        """
        Print basic status of the drone to stdout.
        """
        print("Get all vehicle attribute values:")
        print("Autopilot Firmware version: %s" % self._vehicle.version)
        print("Major version number: %s" % self._vehicle.version.major)
        print("Minor version number: %s" % self._vehicle.version.minor)
        print("Patch version number: %s" % self._vehicle.version.patch)
        print("Release type: %s" % self._vehicle.version.release_type())
        print("Release version: %s" % self._vehicle.version.release_version())
        print("Stable release?: %s" % self._vehicle.version.is_stable())

    def close(self):
        """
        Close any existing connection with the drone.
        """
        self._vehicle.close()
