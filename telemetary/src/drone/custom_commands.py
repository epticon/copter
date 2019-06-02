CUSTOM_WAYPOINTS_CLEAR = 701


class CustomCommand(object):
    def __init__(self, code):
        self._code = int(code)

    def exec(self, cmds):
        if self._code == CUSTOM_WAYPOINTS_CLEAR:
            cmds.clear()
