from collections import defaultdict

def deterministic_die():
    i = 1
    while True:
        yield i
        i += 1

deter = deterministic_die()

def roll():
    return next(deter)

def run():
    players_pos = {1: 9, 2: 4}
    total_score = defaultdict(int)
    max_score = 0
    while True:
        for player in sorted(players_pos):
            pos = players_pos[player]
            rolls = roll() + roll() + roll()
            players_pos[player] = ((pos + rolls - 1) % 10) + 1
            total_score[player] += players_pos[player]
            max_score = max(total_score.values())
            if max_score >= 1000:
                return total_score

res = min(run().values())
print(res*(roll()-1))

from itertools import product
from collections import Counter

possibilities = []
for i in range(1, 11):
    possibilities.append(Counter([(i + r1 + r2 + r3 - 1) % 10 + 1 for r1, r2, r3 in product(*[range(1, 4)]*3)]))
    
def run(n):
    pos = [9, 4]
    def update_scores(old_scores, possibilities):
        new_scores = defaultdict(lambda: defaultdict(int))
        for pos, scores in old_scores.items():
            for next_pos, next_count in possibilities[pos - 1].items():
                for prev_score, count in scores.items():
                    if prev_score < 21:
                        new_scores[next_pos][prev_score + next_pos] += count*next_count
        return new_scores
                
    players_scores = [{v: {0: 1}} for v in pos]
    win = [0, 0]
    for i in range(n):
        for player in range(2):
            players_scores[player] = (r := update_scores(players_scores[player], possibilities))
            r_o = players_scores[0 if player else 1]

            win_score_counts = sum(c for v in r.values() for score, c in v.items() if score >= 21)
            lost_score_counts = sum(c for v in r_o.values() for score, c in v.items() if score < 21)
            win[player] += win_score_counts * lost_score_counts
                    
    return players_scores, win

_, win = run(15)
print(max(win))
    

