import hashlib
from itertools import count
from typing import Generator, Tuple, Callable

with open('input.txt') as f:
    token = f.readline().replace('\n', '')
    
print(token)

def md5(s: str) -> str:
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def default_rule(s: str, *, size: int = 5) -> bool:
    return s.startswith('0'*size)

def valid_hash(token: str, rule: Callable) -> Generator[Tuple[int, str], None, None]:
    for i in count():
        if rule(md5(hash := f'{token}{i}')):
            yield (i, hash)

def find_hash(token: str, rule: Callable = default_rule) -> Tuple[int, str]:
    return next(valid_hash(token, rule))
    

def test_find_hash():
    assert find_hash('abcdef')[0] == 609043

result = find_hash(token)
print(result)

def r2(s: str) -> bool:
    return default_rule(s, size = 6)

result = find_hash(token, r2)
print(result)

