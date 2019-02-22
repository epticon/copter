import json
import re


def pascal_to_snake_case(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def parse_assignment(string):
    values = string.strip().split("=")
    return {str(values[0]): float(values[1])}


def parse_logs(path, output_path):
    final_json = []

    with open(path, "r") as log:
        data = json.loads(str(log.read()))

        for log in data:
            readings = log["data"]
            key = list(readings.keys())[0]

            inner_data = str(readings[key])

            if "[" in inner_data and "]" in inner_data:
                # is array value
                string_array = str(inner_data[1:-1]).replace(" ", "").split(",")
                final_json.append({key: list(map(lambda x: float(x), string_array))})

            elif ":" in inner_data:
                # is inner value
                splitted_data = inner_data.split(":")
                key = pascal_to_snake_case(splitted_data[0])
                assigments = splitted_data[1].split(",")
                values = list(map(lambda x: parse_assignment(x), assigments))

                final_json.append({key: values})
            else:
                final_json.append({key: float(inner_data)})

    with open(output_path, "w+") as file:
        file.write(json.dumps(final_json))
