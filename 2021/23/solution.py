from types import FunctionType
from typing import *
from math import inf
from functools import lru_cache
import re
from dataclasses import dataclass
from itertools import chain, tee, islice, combinations
from collections import defaultdict, deque
import heapq
from copy import deepcopy
from enum import Enum

Pos = int

class Type(Enum):
    A = 1
    B = 2
    C = 3
    D = 4

with open("template-2.txt") as f:
    template = f.read()

"""
01 02 03 06 07 10 11 14 15 18 19
      04    08    12    16
      05    09    13    17
      20    22    24    26
      21    23    25    27
"""
board = {
    1: [2],
    2: [1, 3],
    3: [2, 4, 6],
    4: [3, 5],
    5: [4, 20],
    6: [3, 7],
    7: [6, 8, 10],
    8: [7, 9],
    9: [8, 22],
    10: [7, 11],
    11: [10, 12, 14],
    12: [11, 13],
    13: [12, 24],
    14: [11, 15],
    15: [14, 16, 18],
    16: [15, 17],
    17: [16, 26],
    18: [15, 19],
    19: [18],
    20: [5, 21],
    21: [20],
    22: [9, 23],
    23: [22],
    24: [13, 25],
    25: [24],
    26: [17, 27],
    27: [26]
}

small_board = {
    1: [2],
    2: [1, 3],
    3: [2, 4, 6],
    4: [3, 5],
    5: [4],
    6: [3, 7],
    7: [6, 8, 10],
    8: [7, 9],
    9: [8],
    10: [7, 11],
    11: [10, 12, 14],
    12: [11, 13],
    13: [12],
    14: [11, 15],
    15: [14, 16, 18],
    16: [15, 17],
    17: [16],
    18: [15, 19],
    19: [18]
}

all_pos = set(board)
remove_from_target = {3, 7, 11, 15}
interm_pos = set([1, 2, 3, 6, 7, 10, 11, 14, 15, 18, 19])

def reach_from(init_pos: Pos, cond:Callable[[Pos], bool] = None, to_remove: Set[Pos]=remove_from_target):
    neighbours = [(p, 1) for p in board[init_pos]]
    visited = {init_pos}
    reach = set()
    if cond is None:
        cond = lambda x: True

    while neighbours:
        next, count = neighbours.pop()
        if cond(next):
            reach.add((next, count))
            visited.add(next)
            not_visited = [(p, count + 1) for p in board[next] if p not in visited]
            neighbours.extend(not_visited)

    return {(p, c) for p, c in reach if p not in to_remove}
    
print(reach_from(9))

rooms = {
    Type.A: [4, 5, 20, 21],
    Type.B: [8, 9, 22, 23],
    Type.C: [12, 13, 24, 25],
    Type.D: [16, 17, 26, 27]
}

def is_room(p):
    return p in chain.from_iterable(rooms.values())

#print(reach_from(9, lambda x: x in interm_pos or x in rooms[Type.B]))

@dataclass
class Pawn:
    type: Type
    pos: Pos
    state: int = 1

    def __lt__(self, other):
        return (self.pos, self.type, self.state) < (other.pos, other.type, other.state)

    def __repr__(self):
        return f'Pawn({self.type}, {self.pos}, {self.state})'
   
def every_n(it: Iterable, n=4):
    for i, e in enumerate(it):
        if i % n == 0:
            yield e

def spaced_val(it: Iterable, space=4):
    l_it = list(tee(it, space))
    for i, it in enumerate(l_it):
        l_it[i] = every_n(islice(it, i, None), 4)

    for vals in l_it:
        yield vals

class GameState:
    def __init__(self, **type_positions):
        self.pawns: list[Pawn] = []
        for type, positions in type_positions.items():
            for pos in positions:
                self.pawns.append(pawn := Pawn(Type[type], pos, 1))

    def move(self, pawn, pos):
        pawn.pos = pos
        pawn.state += 1 
        return

    def get_pawn(self, pos, default=None):
        return next(iter([p for p in self.pawns if p.pos == pos]), default)

    @classmethod
    def from_str(cls, board_ascii: str):
        types = re.findall('[ABCD]', board_ascii)
        pawns = defaultdict(list)
        for (room_type, positions) , pawn_types in zip(rooms.items(), spaced_val(types)):
            for pawn_type, position in zip(pawn_types, positions):
                pawns[pawn_type].append(position)

        return cls(**pawns)


    def valid_move(self, pawn: Pawn) -> List[Tuple[Pos, int]]:
        """list of valid move and their count for pawn with current board

        Args:
            pawn ([Pawn]): pawn to move
        """
        allowed = all_pos - set(p.pos for p in self.pawns)
        reachable_points_and_counts = reach_from(pawn.pos, lambda x: x in allowed)
        reachable_points = {p for p, c in reachable_points_and_counts}
        targets = set(rooms[pawn.type])

        #if pawn cant move
        if not reachable_points_and_counts:
            return []
        
        if not any(p.type != pawn.type for p in self.pawns if (p.pos in targets) and (p.pos > pawn.pos)):
            #if pawn is parked
            if pawn.pos in targets:
                return []
        
        if not any(p.type != pawn.type for p in self.pawns if (p.pos in targets)):
            #if pawn is parked
            #if pawn can park
            if final_pos := max(reachable_points & targets, default=None):
                return [(p, c) for p, c in reachable_points_and_counts if p == final_pos]

        # Pawn can move, is not parked and cannot park directly
        if pawn.state == 1:
            # Check if this move is not blocking
            # ...C.A..... is consider blocking since B needs to go right and A left
            # ..B...A.... is not blocking since B can park and then A 
            # for the moment we dont care
            return [(p, c) for p, c in reachable_points_and_counts if p in (interm_pos - remove_from_target)]

        if pawn.state > 2:
            return []

        return []

    def is_over(self):
        return all(p.pos in rooms[p.type] for p in self.pawns)

    def is_blocked(self):
        pawns_in_hallway = sorted([(p.pos, p.type) for p in self.pawns if p.pos in interm_pos])
        for (p1, p1_type), (p2, p2_type) in combinations(pawns_in_hallway, 2):
            if p1 < p2 and (p2 < rooms[p1_type][0]) and (p1 > rooms[p2_type][0]):
                return True
        return False
       
    def next_states(self):
        next = []
        for pawn in self.pawns:
            for move, count in self.valid_move(pawn):
                g = deepcopy(self)
                g.move(g.get_pawn(pawn.pos), move)
                next.append((pawn.type, count, g))

        return next

    def __lt__(self, other):
        return self.pawns < other.pawns

    def __repr__(self):
        repr = template
        pawns_pos = {p.pos: p.type.name for p in self.pawns}
        for p in all_pos:
            if p in pawns_pos:
                repr = repr.replace(f'{{{p}}}', pawns_pos[p])
            else:
                repr = repr.replace(f'{{{p}}}', '.')
        return repr

with open("input23-2.txt") as f:
    file = f.read()

cost = {
    Type.A: 1,
    Type.B: 10,
    Type.C: 100,
    Type.D: 1000
}

def solve(g):
    if g.is_over():
        return 0
    if g.is_blocked():
        return inf
    next_gamestates = g.next_states()
    if len(next_gamestates) == 0:
        return inf
    else:
        return min(cost[t]*c + solve(n_g) for t, c, n_g in next_gamestates)

def cost_optimistic_finish(g):
    total_cost = 0
    for p in g.pawns:
        path_length = 0
        if p.pos not in rooms[p.type]:
            path_length = list(filter(lambda x: x[0] == rooms[p.type][0], reach_from(p.pos)))[0][1]
        total_cost += path_length * cost[p.type]

    return total_cost

def solve_it(g):
    explore = []
    heapq.heappush(explore, (0, g))

    current_best = inf

    while explore:
        cost_g, g = heapq.heappop(explore)
        cost_g = -cost_g
        if g.is_blocked():
            continue
        if g.is_over():
            if cost_g < current_best:
                current_best = cost_g
                print(cost_g)
                continue
        for t, c, n_g in g.next_states():
            optimistic_cost = cost_optimistic_finish(n_g)
            move_cost = cost[t] * c
            if (cost_g + optimistic_cost + move_cost) < current_best:
                heapq.heappush(explore, (-(cost_g + move_cost), n_g))

    return current_best

g = GameState.from_str(file)
print(solve_it(g))
#print(g.pawns)
print(g)
#print(g.get_pawn(8))
#g.move(g.get_pawn(8) , 7)
#print(g)
#d = deepcopy(g)
g.move(g.get_pawn(12), 10)
print(g)
#print(g.get_pawn(12))
#print(g)
#print(g.valid_move(g.pos_occupant[12]))
for i, n in enumerate(g.next_states()):
    print(i)
    print(n)