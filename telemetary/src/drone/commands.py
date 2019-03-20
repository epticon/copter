from dronekit import mavutil, VehicleMode, LocationGlobal, Command


class DroneCommand(object):
    def __init__(self, vehicle=None):
        self._vehicle = vehicle

    def auto_mode(self):
        self._vehicle.mode = VehicleMode("AUTO")

    def guided_mode(self):
        self._vehicle.mode = VehicleMode("GUIDED")

    def return_home(self, airspeed=None, groundspeed=None):
        self._vehicle.mode = VehicleMode("RTL")

    def set_home(self, lng, lat, alt=None):
        self._vehicle.home_location = LocationGlobal(lat, lng, alt)

    def land(self):
        self._vehicle.mode = VehicleMode("LAND")

    def navigate_to(self, lng, lat, altitude):
        self._vehicle.simple_goto(LocationGlobal(int(lng), int(lat), int(altitude)))

    def set_flight_height(self, altitude):
        self._vehicle.simple_takeoff(altitude)

    def clear_command(self):
        cmds = self._vehicle.commands
        cmds.clear()
        cmds.upload()
