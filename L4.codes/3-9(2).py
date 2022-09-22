from enum import Enum
import time
from tkinter.tix import TCL_TIMER_EVENTS

class STRATEGY(Enum):
    BFS = 1
    ASTAR = 2

class Node(object):
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __repr__(self):
        return "<Node state:%s parent:%s action:%s path_cost:%s>" % (
            self.state, self.parent, self.action, self.path_cost)

class Problem(object):
    _start_state = [3, 3, 1]
    
    def start_state(self):
        return self._start_state

    def is_goal(self, state):
        return state == [0, 0, 0]

    def heuristic(self, state):
        if state[2] == 1:
            return (state[0] + state[1] + 2) * 2
        if state[2] == 0:
            return (state[0] + state[1]) * 2

    def is_valid_state(self, state):
        if (state[0] != state[1]) and (state[0] != 0 and state[0] != 3):
            return False 
        return True

    def get_successors(self, node: Node, strategy: STRATEGY) -> list:
        successors = []
        state = node.state
        if state[2] == 1:
            if state[0] >= 1:
                successors.append([state[0] - 1, state[1], 0])
            if state[1] >= 1:
                successors.append([state[0], state[1] - 1, 0])
            if state[0] >= 2:
                successors.append([state[0] - 2, state[1], 0])
            if state[1] >= 2:
                successors.append([state[0], state[1] - 2, 0])
            if state[0] >= 1 and state[1] >= 1:
                successors.append([state[0] - 1, state[1] - 1, 0])
        else:
            if state[0] <= 2:
                successors.append([state[0] + 1, state[1], 1])
            if state[1] <= 2:
                successors.append([state[0], state[1] + 1, 1])
            if state[0] <= 1:
                successors.append([state[0] + 2, state[1], 1])
            if state[1] <= 1:
                successors.append([state[0], state[1] + 2, 1])
            if state[0] <= 2 and state[1] <= 2:
                successors.append([state[0] + 1, state[1] + 1, 1])

        # clear states
        candidates = []
        for successor in successors:
            if self.is_valid_state(successor):
                candidates.append(successor)
        successors = candidates

        if strategy == STRATEGY.BFS:
            pass
        elif strategy == STRATEGY.ASTAR:
            min_cost = 100
            candidates = []
            for successor in successors:
                if (node.path_cost + 1) + self.heuristic(successor) <= min_cost:
                    min_cost = node.path_cost + 1 + self.heuristic(successor)
            for successor in successors:
                if (node.path_cost + 1) + self.heuristic(successor) == min_cost:
                    candidates.append(successor)
            successors = candidates
        return successors
    
    
    def solve(self, strategy: STRATEGY, check: bool):
        frontier = [Node(self.start_state(), None, None, 0)]
        explored = []
        nodes_to_be_expanded = 0
        while frontier:
            node = frontier.pop()
            if self.is_goal(node.state):
                return [node, nodes_to_be_expanded]
            explored.append(node.state)
            for successor in self.get_successors(node, strategy):
                nodes_to_be_expanded += 1
                if not check:
                    successor_node = Node(successor, node, None, node.path_cost + 1)
                    if strategy == STRATEGY.BFS:
                        frontier.insert(0, successor_node)
                    if strategy == STRATEGY.ASTAR:
                        frontier.insert(0, successor_node)
                if check and (successor not in explored and successor not in frontier):
                    successor_node = Node(successor, node, None, node.path_cost + 1)
                    if strategy == STRATEGY.BFS:
                        frontier.insert(0, successor_node)
                    if strategy == STRATEGY.ASTAR:
                        frontier.insert(0, successor_node)

        return [None, nodes_to_be_expanded]

mcproblem = Problem()
strategy_inputs = [STRATEGY.BFS, STRATEGY.ASTAR]
check_repeated = [True, False]

for strategy_input in strategy_inputs:
    for check in check_repeated:
        time_start = time.time_ns()
        [node, nodes_to_be_expanded] = mcproblem.solve(strategy_input, check)
        time_end = time.time_ns()
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        path.reverse()
        print("Strategy: %s, Expand: %d times, Check: %s, Time Usage: %s" % (strategy_input, nodes_to_be_expanded, check, time_end - time_start))
        print(path)