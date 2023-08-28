import re
import json


def get_data(filename: str) -> str:
    with open(filename) as f:
        return f.read()


data = get_data('input.txt')


def get_numbers(s: str) -> list[int]:
    return list(map(int, re.findall(r'-?\d+', s)))

print(sum(get_numbers(data)))

parsed_data = json.loads(data)


def sum_json(json_data) -> int:
    match json_data:
        case int(a):
            return a
        case list():
            return sum(sum_json(v) for v in json_data)
        case dict():
            if 'red' in json_data.values():
                return 0
            else:
                return sum(sum_json(v) for v in json_data.values())
        case _:
            return 0


print(sum_json(parsed_data))
