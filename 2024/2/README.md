# Day 2

Bruteforce because lists are very small.

[solution](https://www.reddit.com/r/adventofcode/comments/1h4ncyr/comment/m00dpfi/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)
```python
data = [[*map(int, l.split())] for l in open('data.txt')]

def good(d, s=0):
    for i in range(len(d)-1):
        if not 1 <= d[i]-d[i+1] <= 3:
            return s and any(good(d[j-1:j] + d[j+1:]) for j in (i,i+1))
    return True

for s in 0, 1: print(sum(good(d, s) or good(d[::-1], s) for d in data))
```

- We can just focus on one case: increasing. Having the main function checking only one case makes it 
simpler. In part 2, gecause of the error tolerance we would need more observations to know if this should be increasing or decreasing.
- Short circuit the recursive call when we cannot have error anymore.


I would usually go with a similar recursive function but I thought this time that there 
should be a more 'direct' solution. Also avoiding to iterate twice (for increasing case only) on the list. When we face an error, the
recursive solution will test the rest in two different settings `(i, i+1)`.


```python
def is_valid_except_one(rep: Report) -> bool:
    def _is_valid(x, y):
        if (x is None) or (y is None):
            return True
        return (1 <= (y - x) <= 3)

    def _increasing(rep: Report, can_skip: int = 1) -> bool:
        rep_with_sentinels = list(chain([None], rep, [None]))
        window = sliding_window(rep_with_sentinels, 4)
        is_valid_interval = sliding_window(
            starmap(_is_valid, pairwise(rep_with_sentinels)),
            3
        )

        for w, is_valid_increase in zip(window, is_valid_interval):
            a1, a2, a3, a4 = w

            match is_valid_increase:
                case True, False, False:
                    if not _is_valid(a2, a4):
                        return False
                    can_skip -= 1
                case True, False, True:
                    if not (_is_valid(a1, a3) or _is_valid(a2, a4)):
                        return False
                    can_skip -= 1
                case False, False, False:
                    return False
        return can_skip >= 0

    return (_increasing(rep) or _increasing(rep[::-1]))
```

This solution implements an algorithm similar to how a human would solve the challenge:
Find a spot with error, see if there is a possible fix. If yes continue otherwise return False.

