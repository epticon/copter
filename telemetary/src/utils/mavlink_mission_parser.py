from dronekit import Command
from drone.custom_commands import CustomCommand
from dronekit.mavlink import mavutil


class MavlinkMissionParser(object):
    @staticmethod
    def from_string(cmds):
        """
        Parses a given string of values into equivalent mavlink
        commands or recognized custom commands.
        """

        if len(cmds) == 0:
            return []

        missionlist = []
        for line in cmds:
            linearray = line.split("\t")
            if len(linearray) == 1:
                cmd = int(linearray[0])
                if cmd >= 700 and cmd <= 800:  # is custom command
                    missionlist.append(CustomCommand(cmd))
                continue

            ln_frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
            ln_currentwp = 0
            ln_autocontinue = 0
            ln_command = int(linearray[0])
            # if ln_command == 13:
            #     ln_command = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
            ln_param1 = float(linearray[1])
            ln_param2 = float(linearray[2])
            ln_param3 = float(linearray[3])
            ln_param4 = float(linearray[4])
            ln_param5 = float(linearray[5])
            ln_param6 = float(linearray[6])
            ln_param7 = float(linearray[7].strip())
            cmd = Command(
                0,
                0,
                0,
                ln_frame,
                ln_command,
                ln_currentwp,
                ln_autocontinue,
                ln_param1,
                ln_param2,
                ln_param3,
                ln_param4,
                ln_param5,
                ln_param6,
                ln_param7,
            )
            missionlist.append(cmd)
        return missionlist
