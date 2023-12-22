from collections import defaultdict


def load(filename: str) -> list[str]:
    return open(filename).read().strip().split(',')


sequence_test = load('test.txt')
sequence = load('input.txt')


def val_hash(s: str) -> int:
    h = 0
    for char in s:
        h += ord(char)
        h *= 17
        h = h % 256
    return h


print(val_hash('qp'))
print(sum(val_hash(s) for s in sequence))


Lens = tuple[str, int]
HashMap = defaultdict[list[Lens]]

def update_hashmap(hashmap: HashMap, command: str) -> HashMap:
    if '-' in command:
        label = command[:-1]
        h = val_hash(label)
        hashmap[h] = [
            (lens_label, lens_val)
            for lens_label, lens_val in hashmap[h]
            if lens_label != label
        ]
        if len(hashmap[h]) == 0:
            del hashmap[h]
    else:
        label, val = command.split('=')
        val = int(val)
        h = val_hash(label)
        if label in set(l for l, v in hashmap[h]):
            hashmap[h] = [
                (lens_label, val if label == lens_label else lens_val)
                for lens_label, lens_val in hashmap[h]
            ]
        else:
            hashmap[h].append((label, val))
    return hashmap


def initialize(sequence: list[str]) -> HashMap:
    hashmap = defaultdict(list)
    for command in sequence:
        hashmap = update_hashmap(hashmap, command)
    return hashmap


def score(hashmap: HashMap) -> int:
    res = 0
    for h, lenses in hashmap.items():
        res += (h + 1) * sum(i * val for i, (_, val) in enumerate(lenses, 1))
    return res


print(
    score(initialize(sequence))
)