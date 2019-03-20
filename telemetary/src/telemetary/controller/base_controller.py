class BaseController(object):
    def __init__(self, client, drone, body, params):
        self._body = body
        self._params = params
        self._client = client
        self._drone = drone
