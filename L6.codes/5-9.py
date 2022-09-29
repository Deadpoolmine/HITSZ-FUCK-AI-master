from time import sleep
from typing import List
from treelib import Tree, Node
import json
 
tree = Tree()
DRAW_LEVEL = 2
tree.create_node(str([]), str([]))

def print_board(tic_tac_toe_board: List):
    # print("-------------")
    # for i in range(3):
    #     print("|", tic_tac_toe_board[3*i], "|", tic_tac_toe_board[3*i + 1], "|", tic_tac_toe_board[3*i + 2], "|")
    #     print("-------------")
    # sleep(1)
    return 
    # print(tic_tac_toe_board)

solution = []
solutions = []

def apply_solution(solution: List):
    tic_tac_toe_board = ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N']
    for i in range(len(solution)):
        if i % 2 == 0:
            tic_tac_toe_board[solution[i]] = 'X'
        else:
            tic_tac_toe_board[solution[i]] = 'O'
    return tic_tac_toe_board

def check_winner(solution: List):
    tic_tac_toe_board = apply_solution(solution)
    winner = 'N'
    winner_cnt = 0
    # check row
    for i in range(3):
        if tic_tac_toe_board[3*i] == tic_tac_toe_board[3*i + 1] == tic_tac_toe_board[3*i + 2] != 'N':
            winner = tic_tac_toe_board[3*i]
            winner_cnt += 1
    # check column
    for i in range(3):
        if tic_tac_toe_board[i] == tic_tac_toe_board[i + 3] == tic_tac_toe_board[i + 6] != 'N':
            winner = tic_tac_toe_board[i]
            winner_cnt += 1
    
    # check diagonal
    if tic_tac_toe_board[0] == tic_tac_toe_board[4] == tic_tac_toe_board[8] != 'N':
        winner = tic_tac_toe_board[0]
        winner_cnt += 1

    if tic_tac_toe_board[2] == tic_tac_toe_board[4] == tic_tac_toe_board[6] != 'N':
        winner = tic_tac_toe_board[2]
        winner_cnt += 1

    return winner, winner_cnt

def check_terminal(solution: List):
        
    tic_tac_toe_board = apply_solution(solution)
    winner = 'N'
    
    # check row
    for i in range(3):
        if tic_tac_toe_board[3*i] == tic_tac_toe_board[3*i + 1] == tic_tac_toe_board[3*i + 2] != 'N':
            if winner == 'N':
                winner = tic_tac_toe_board[3*i]
            else:
                return False
            print_board(tic_tac_toe_board)

    # check column
    for i in range(3):
        if tic_tac_toe_board[i] == tic_tac_toe_board[i + 3] == tic_tac_toe_board[i + 6] != 'N':
            if winner == 'N':
                winner = tic_tac_toe_board[i]
            else:
                return False
            print_board(tic_tac_toe_board)
    
    # check diagonal
    if tic_tac_toe_board[0] == tic_tac_toe_board[4] == tic_tac_toe_board[8] != 'N':
        if winner == 'N':
            winner = tic_tac_toe_board[0]
        else:
            return False
        print_board(tic_tac_toe_board)

    if tic_tac_toe_board[2] == tic_tac_toe_board[4] == tic_tac_toe_board[6] != 'N':
        if winner == 'N':
            winner = tic_tac_toe_board[2]
        else:
            return False
        print_board(tic_tac_toe_board)

    if winner != 'N':
        if winner == 'O' and len(solution) % 2 != 0:
            return False
        return True
    if winner == 'N':
        if len(solution) == 9:
            return True
    return False

def check_duplicate(solution: List):
    tic_tac_toe_board = apply_solution(solution)
    for _solution in solutions:
        if len(_solution) != len(solution):
            continue
        _tic_tac_toe_board = apply_solution(_solution)
        is_same = True
        for i, state in enumerate(_tic_tac_toe_board):
            if _tic_tac_toe_board[i] != tic_tac_toe_board[i]:
                is_same = False
                break
        if is_same:
            return True
    return False


def evaluate(solution: List):
    def _evaluate(solution: List, n: int, symbol: str):
        _score = 0
        tic_tac_toe_board = apply_solution(solution)
        # check row
        for i in range(3):
            row = [tic_tac_toe_board[3*i], tic_tac_toe_board[3*i + 1], tic_tac_toe_board[3*i + 2]]
            if row.count(symbol) == n:
                if row.count(symbol) + row.count('N') == 3:
                    _score += 1
        # check col
        for i in range(3):
            col = [tic_tac_toe_board[i], tic_tac_toe_board[i + 3], tic_tac_toe_board[i + 6]]
            if col.count(symbol) == n:
                if col.count(symbol) + col.count('N') == 3:
                    _score += 1

        # check diagonal
        diag = [tic_tac_toe_board[0], tic_tac_toe_board[4], tic_tac_toe_board[8]]
        if diag.count(symbol) == n:
            if diag.count(symbol) + diag.count('N') == 3:
                _score += 1

        diag = [tic_tac_toe_board[2], tic_tac_toe_board[4], tic_tac_toe_board[6]]
        if diag.count(symbol) == n:
            if diag.count(symbol) + diag.count('N') == 3:
                _score += 1
        return _score

    return 3*(_evaluate(solution, 2, 'X') - _evaluate(solution, 2, 'O')) + _evaluate(solution, 1, 'X') - _evaluate(solution, 1, 'O')

def dfs_search(solution: List, traverse_only=False):
    if not traverse_only:
        if check_terminal(solution):
            if not check_duplicate(solution):
                _solution = solution.copy()
                solutions.append(_solution)
        
    for i in range(9):
        if i not in solution:
            solution.append(i)
            if len(solution) <= DRAW_LEVEL:
                tree.create_node(str(solution.copy()), str(solution), 
                                 parent=str(solution[:len(solution) - 1]), 
                                 data = evaluate(solution))
            dfs_search(solution, traverse_only)
            solution.pop()

dfs_search(solution, True)

print(len(solutions))
x_winner = 0
o_winner = 0
lens_map = [0, 0, 0, 0, 0, 0, 0, 0, 0]

for _solution in solutions:
    lens_map[len(_solution) - 1] += 1
    winner, winner_cnt = check_winner(_solution)
    if winner == 'X':
        x_winner += 1
    elif winner == 'O':
        o_winner += 1
    # print(_solution)
    # print(winner_cnt)
print(x_winner, o_winner)
print(lens_map)

with open("tree.json", 'w') as f:
    obj = json.loads(tree.to_json(with_data=True))
    f.write(json.dumps(obj, indent=4))
