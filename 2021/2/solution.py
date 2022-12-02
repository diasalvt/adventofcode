from itertools import islice
from collections import defaultdict

def sol1():
    with open("input2.txt") as f:
        values = (row for row in f)
        move_size = map(lambda x: x.split(), values)

        total_moves = defaultdict(int)
        for move, size in move_size:
            total_moves[move] += int(size)

        print(total_moves)
        result = (total_moves['down'] - total_moves['up']) * total_moves['forward'] 
        print(result)

def sol2():
    with open("input2.txt") as f:
        values = (row for row in f)
        move_size = map(lambda x: x.split(), values)
        
        tracked_values = {
            'aim': 0,
            'horizontal': 0,
            'depth': 0
        }

        for move, size in move_size:
            size = int(size)
            if move == 'up':
                tracked_values['aim'] -= size
            elif move == 'down':
                tracked_values['aim'] += size
            elif move == 'forward':
                tracked_values['horizontal'] += size
                tracked_values['depth'] += tracked_values['aim'] * size
            
        print(tracked_values)
        result = tracked_values['horizontal'] * tracked_values['depth']
        print(result)

sol2()