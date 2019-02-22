ROUTE = "route"
MESSAGE = "message"


def route_key_exists(payload):
    return ROUTE in payload


def is_error_message(payload):
    return MESSAGE in payload
