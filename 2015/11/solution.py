from string import ascii_lowercase as letters
from typing import Iterable, Generator, Iterator
from itertools import tee, islice, takewhile

Password = str


def skip_repeat(iterable: Iterable) -> Generator:
    prev = None
    for elem in iterable:
        if elem == prev:
            prev = None
        else:
            prev = elem
            yield elem


def nwise(iterable: Iterable, n: int, overlap: bool = True) -> Iterator:
    iterators = tee(iter(iterable), n)
    result = zip(*[islice(it, i, None) for i, it in enumerate(iterators)])
    if overlap:
        return result
    else:
        return skip_repeat(result)


print(list(nwise(letters, 3)))
print(list(nwise('aaabcd', 2, overlap=False)))
print(list(nwise('aaaabcd', 2, overlap=False)))
print(list(nwise('aaaaabcd', 2, overlap=False)))


def is_valid(p: Password) -> bool:
    if set(nwise(p, 3)).isdisjoint(set(nwise(letters, 3))):
        return False
    if {'i', 'o', 'l'}.intersection(set(p)):
        return False
    if len(set(nwise(p, 2, overlap=False)).intersection({(letter, letter) for letter in letters})) < 2:
        return False
    return True


def next_letter(letter: str) -> str:
    return letters[(letters.index(letter) + 1) % len(letters)]


def next_password(p: Password) -> Password:
    r = []

    carry = True
    for char in reversed(p):
        if carry:
            r.append(next_letter(char))
        else:
            r.append(char)

        if char != 'z':
            carry = False

    return list(reversed(r))

print(next_password('xyz'))
print(next_password('zxyzz'))

def next_valid_password(p: Password) -> Password:
    while not is_valid(p := next_password(p)):
        pass
    return p

print(''.join(next_valid_password('vzbxkghb')))
print(''.join(next_valid_password(next_valid_password('vzbxkghb'))))
