class InvalidIPV4Exception(Exception):
    pass


class FailedDroneConnectionException(Exception):
    pass


class RouteMissingException(Exception):
    def __str__(self):
        return "The specified route is missing"
