from __future__ import annotations
from typing import *
from math import ceil
from functools import reduce

tree_1 = [[[1, 2],2], [2, 4]]
tree_2 = [[[[[9,8],1],2],3],4]
tree_3 = [7,[6,[5,[4,[3,2]]]]]
tree_4 = [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
l_tree = [
    [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
    [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
    [7,[5,[[3,8],[1,4]]]],
    [[2,[2,2]],[8,[8,1]]],
    [2,9],
    [1,[[[9,3],9],[[9,0],[0,7]]]],
    [[[5,[7,4]],7],1],
    [[[[4,2],2],6],[8,7]]
]

Direction = Literal['L'] | Literal['R']
Directions = list[Direction]
Leaf = int
BinaryTree =  Leaf | List['BinaryTree']
Trail = List[Tuple[Direction, BinaryTree]]
FocusedTree = Tuple[BinaryTree, Trail]

def tree_to_f_tree(tree: BinaryTree):
    return (tree, [])

def f_tree_to_tree(f_tree: FocusedTree):
    match f_tree:
        case (tree, []):
            return tree
        case (tree, [('L', discarded_tree), *b]):
            return f_tree_to_tree(([tree, discarded_tree], b))
        case (tree, [('R', discarded_tree), *b]):
            return f_tree_to_tree(([discarded_tree, tree], b))

def step(tree: FocusedTree, d: Direction) -> Optional[FocusedTree]:
    match tree:
        case ([], _):
            return None
        case (int(a), _):
            return None
        case ([a, b], trail):
            if d == 'L':
                return (a, [('L', b)] + trail)
            else:
                return (b, [('R', a)] + trail)

def search_left_first_depth(tree: BinaryTree) -> Optional[FocusedTree]:
    condition = lambda x: x >= 4
    def r_search_left_first(f_tree: FocusedTree, depth=0):
        match f_tree:
            case (int(a), _):
                return None
            case ([int(a), int(b)], _):
                if condition(depth):
                    return f_tree
                else:
                    return None
            case ([a, b], t):
                if search := r_search_left_first(step(f_tree, 'L'), depth + 1):
                    return search
                else:
                    return r_search_left_first(step(f_tree, 'R'), depth + 1)

    return r_search_left_first(tree_to_f_tree(tree))

def search_left_first_greater(tree: BinaryTree) -> Optional[FocusedTree]:
    condition = lambda x: x >= 10
    def r_search_left_first(f_tree: FocusedTree):
        match f_tree:
            case (int(a), _):
                if condition(a):
                    return f_tree
                else:
                    return None
            case ([a, b], t):
                if search := r_search_left_first(step(f_tree, 'L')):
                    return search
                else:
                    return r_search_left_first(step(f_tree, 'R'))

    return r_search_left_first(tree_to_f_tree(tree))

def add_most_left(tree: BinaryTree, value: int) -> BinaryTree:
    match tree:
        case int(a):
            return a + value
        case [a, b]:
            return [add_most_left(a, value), b]

def add_most_right(tree: BinaryTree, value: int) -> BinaryTree:
    match tree:
        case int(a):
            return a + value
        case [a, b]:
            return [a, add_most_right(b, value)]

def explode(f_tree: FocusedTree):
    (a, b), trail = f_tree

    def modify(direction: Direction, trail: Trail, op: Callable[[BinaryTree], BinaryTree]) -> Trail:
        match trail:
            case []:
                return []
            case [(d, discarded_tree), *tail]:
                if d != direction:
                    return [(d, op(discarded_tree)), *tail]
                else:
                    return [(d, discarded_tree), *modify(direction, tail, op)]

    add_a = lambda x: add_most_right(x, a)
    add_b = lambda x: add_most_left(x, b)
    new_f_tree = (0, modify('R', modify('L', trail, add_a), add_b))
    return f_tree_to_tree(new_f_tree)

def split(f_tree: FocusedTree):
    val, trail = f_tree
    return f_tree_to_tree(([int(val / 2), ceil(val / 2)], trail))

def simplify(tree: BinaryTree):
    def p_step(tree: BinaryTree):
        has_changed = False
        while f_tree := search_left_first_depth(tree):
            tree = explode(f_tree)
            has_changed = True
        if f_tree := search_left_first_greater(tree):
            tree = split(f_tree)
            has_changed = True

        return tree, has_changed

    has_changed = True
    while has_changed:
        tree, has_changed = p_step(tree)

    return tree

def magnitude(tree):
    match tree:
        case int(a):
            return a
        case [a, b]:
            return 3*magnitude(a) + 2*magnitude(b)

def process(l_tree: List[BinaryTree]) -> int:
    full_tree = l_tree[0]
    for t in l_tree[1:]:
        full_tree = simplify([full_tree, t])

    return magnitude(full_tree)

def load_input(f_name: str):
    with open(f_name) as f:
        return [eval(row) for row in f]

trees = load_input("input18.txt")
print(process(trees))