from functools import reduce
from operator import add
from itertools import islice, dropwhile, accumulate

with open('input.txt') as f:
    instruction = f.readline()
    
# instruction = ')())()'
result = sum(
    map(lambda x: 1 if x == '(' else -1, instruction)
)

print(result)

result = next(
    dropwhile(
        lambda x: x[1] > -1,
        enumerate(accumulate(map(lambda x: 1 if x == '(' else -1, instruction), add))
    )
)

print(result + 1)
