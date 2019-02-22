from .base_controller import BaseController


class CommandController(BaseController):
    def __init__(self, client, body, params):
        super(CommandController, self).__init__(client, body, params)

    def process_command(self, req=None, res=None):
        print("in method")
