from typing import List


# WA: 0, NT: 1, Q: 2, NSW: 3, V: 4, SA: 5, T: 6
australia_map = [
    [0, 1, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

solutions = []

def is_valid(australia_map: List[List], solution: List, index: int, color: int):
    for i in range(len(australia_map)):
        if len(solution) < i:
            break
        if australia_map[index][i] == 1 and solution[i] == color:
            return False
    return True

def backtrack(australia_map: List[List], Colors: List, solution: List, index:int):
    if index == len(australia_map):
        one_solution = solution.copy()
        solutions.append(one_solution)
        return
    for color in Colors:
        if is_valid(australia_map, solution, index, color):
            solution.append(color)
            backtrack(australia_map, Colors, solution, index + 1)
            solution.pop()

colors_list = [[1, 2, 3], [1, 2, 3, 4], [1, 2]]
for colors in colors_list:
    solutions = []
    backtrack(australia_map, colors, [], 0)
    print("Available Solutions with "+ str(len(colors)) + " colors: " + str(len(solutions)))
    for solution in solutions:
        print(solution)
