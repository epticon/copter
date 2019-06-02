from dronekit import mavutil, VehicleMode, LocationGlobal, Command
import time


class DroneCommand(object):
    def __init__(self, vehicle=None):
        self._vehicle = vehicle

    @property
    def is_armed(self):
        return self._vehicle.armed

    def _change_mode(self, mode, trials=3):
        # Todo: Add support for checking if mode exists
        print("Changing to mode: {0} from mode: {1}".format(mode, self.current_mode()))

        counter = 1
        self._vehicle.mode = VehicleMode(mode)
        while self.current_mode() != mode:
            if counter == trials:
                break
            else:
                counter += 1
                print("Changing mode failed. Trying again in 1 second.")
                time.sleep(1)
        print("Change mode succeeded")

    def current_mode(self):
        return self._vehicle.mode.name

    def auto_mode(self):
        self._change_mode("AUTO")

    def loiter_mode(self):
        self._change_mode("LOITER")

    def guided_mode(self):
        self._change_mode("GUIDED")

    def return_home(self, airspeed=None, groundspeed=None):
        self._change_mode("RTL")

    def land(self):
        self._change_mode("LAND")

    def set_home(self, lng, lat, alt=None):
        self._vehicle.home_location = LocationGlobal(lat, lng, alt)

    def navigate_to(self, lng, lat, altitude):
        self._vehicle.simple_goto(LocationGlobal(int(lng), int(lat), int(altitude)))

    def set_flight_height(self, altitude):
        self._vehicle.simple_takeoff(altitude)

    def arm_motors(self):
        """
        Arms the motors of the drone.
        """
        if self.is_armed == True:
            return

        while not self._vehicle.is_armable:
            print("Pre-arm checks still running; Waiting for vehicle to initialise.")
            time.sleep(1)

        print("Arming motors")
        self._vehicle.mode = VehicleMode("GUIDED")
        self._vehicle.armed = True

        while not self._vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

    def start_mission(self):
        msg = self._vehicle.message_factory.command_long_encode(
            0, 0, mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0, 0, 0, 0
        )
        self._vehicle.send_mavlink(msg)

    def take_off(self, altitude):
        self._vehicle.simple_takeoff(altitude)

        while True:
            print("Altitude: ", self._vehicle.location.global_relative_frame.alt)
            if self._vehicle.location.global_relative_frame.alt >= altitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)

    def download_commands(self):
        cmds_handler = self._vehicle.commands
        cmds_handler.download()
        cmds_handler.wait_ready()
        return cmds_handler

    def clear_all_commands(self):
        cmds = self.download_commands()
        cmds.clear()
        cmds.upload()
