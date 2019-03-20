def extract_class_and_method(string):
    parts = string.split(".")
    return (parts[0], parts[1])


def load_class(full_class_string):
    import importlib

    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]
    module = importlib.import_module(module_path)

    # Finally, we retrieve the Class
    return getattr(module, class_str)


def load_method(class_instance, class_method_string):
    return getattr(class_instance, class_method_string)


def instantiate_controller_method(
    module_path, controller_and_method, client, drone, body=None, params=None
):
    def create_method_params(body, params, client):
        return {"req": {"body": body, "params": params}, "res": client}

    (class_string, method_string) = extract_class_and_method(controller_and_method)
    instance = load_class(f"{module_path}.{class_string}")
    method = load_method(instance(client, drone, body, params), method_string)
    return method(**create_method_params(body, params, client))
