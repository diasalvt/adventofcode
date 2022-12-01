from typing import Iterable

def split(it: Iterable):
    buffer = []
    for e in it:
        if e == '':
            yield buffer
            buffer = []
        else:
            buffer.append(int(e))

with open('input.txt') as f:
    raw_calories = f.read().splitlines()
    calories = list(split(raw_calories))

print(max(map(sum, calories)))

print(sum(sorted(map(sum, calories), reverse=True)[:3]))
