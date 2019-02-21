def create_websocket_url(address, port, path):
    path = str(path)

    if len(path) > 0 and path.startswith("/") == False:
        path = f"/{path}"

    return f"ws://{address}:{port}{path}"
