from collections import Counter, defaultdict
from itertools import tee

test = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

with open("input14.txt") as f:
    input = [row.strip() for row in f]

#input = test.split('\n')

## Parse
def sol1():
    template, _, *rules = input
    rules = [rule.split(' -> ') for rule in rules]
    rules_for_sub = [(p0 + p1, f'{p0}@{replacement}@{p1}') for (p0, p1), replacement in rules]


    def step(template, rules):
        for lhs, rhs in rules:
            while lhs in template:
                template = template.replace(lhs, rhs)
        return template.replace('@' , '')

    for i in range(10):
        template = step(template, rules_for_sub)

    (_, most), *_, (_, least) = Counter(template).most_common()
    res = most - least
    print(res)


def sol2():

    template, _, *rules = input
    rules = [rule.split(' -> ') for rule in rules]

    rules_for_dict = {(p0 + p1): (p0 + replacement, replacement + p1) for (p0, p1), replacement in rules}
    count_digram = defaultdict(int)
    count_gram = defaultdict(int)

    for (p0, p1) in pairwise(template):
        count_digram[(p0 + p1)] += 1
    for gram in template:
        count_gram[gram] += 1

    def step(count_digram, count_gram, rules):
        count_digram_next = count_digram.copy()
        for lhs, (rhs_1, rhs_2) in rules.items():
            if lhs in count_digram:
                c = count_digram[lhs]
                count_digram_next[rhs_1] += c
                count_digram_next[rhs_2] += c
                count_digram_next[lhs] -= c
                count_gram[rhs_2[0]] += c

        return count_digram_next, count_gram
    
    for i in range(40):
        count_digram, count_gram = step(count_digram, count_gram, rules_for_dict)
    
    sorted_letters, sorted_counts = zip(*sorted(count_gram.items(), key=lambda x: x[1], reverse=True))
    print(sorted_counts[0] - sorted_counts[-1])

sol2()