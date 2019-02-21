class RouteMissingException(Exception):
    def __str__(self):
        return "The specified route is missing"
