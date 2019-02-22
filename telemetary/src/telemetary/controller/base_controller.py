class BaseController(object):
    def __init__(self, client, body, params):
        self._body = body
        self._params = params
        self._client = client
