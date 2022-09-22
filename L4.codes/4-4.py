from enum import Enum
from random import randint, seed, shuffle
from re import L

ITERATION = 1000

class STRATEGY(Enum):
    HILL_CLIMB_STEEP_ASCENT = 0
    HILL_CLIMB_FIRST_CHOICE = 1
    HILL_CLIMB_RANDOM_RESTART = 2
    SIMULATED_ANNEALING = 3

class Node(object):
    def __init__(self, state, parent, action, cost):
        self.state: list = state
        self.parent = parent
        self.action = action
        self.cost = cost

class Problem(object):
    start_state = None
    goal_state = None
    max_tries = 900
    cur_tries = 0
    cur_cost = 0
    
    def __init__(self, goal_state) -> None:
        self.goal_state = goal_state

    def generate_start_state(self):
        raise NotImplementedError

    def get_successors(self, node: Node, strategy: STRATEGY) -> list[Node]:
        raise NotImplementedError

    def heuristic(self, state, strategy: STRATEGY):
        raise NotImplementedError
    
    def get_start_state(self):
        return self.start_state

    def reset_problem_counter(self, state = None):
        self.cur_tries = 0
        self.cur_cost = 0
        if state != None:
            self.start_state = state
    
    def get_cur_cost(self):
        return self.cur_cost
    
    def get_cur_tries(self):
        return self.cur_tries

    def solve(self, strategy, run_test = False):
        self.cur_tries += 1
        if strategy != STRATEGY.HILL_CLIMB_RANDOM_RESTART:
            self.cur_cost = 0

        current = Node(self.get_start_state(), None, None, self.heuristic(self.get_start_state(), strategy))
        if strategy != STRATEGY.SIMULATED_ANNEALING:
            while True:
                neighbors = self.get_successors(current, strategy)

                if len(neighbors) == 0:
                    if current.cost != 0:
                        if not run_test:
                            print("Hit local maximum, Exit")
                        break
                    return current
                
                neighbor = neighbors[0]
                
                if neighbor.cost >= current.cost:
                    if current.cost != 0:
                        if not run_test:
                            print("Hit local maximum, Exit")
                        break
                    return current

                current = neighbor
                self.cur_cost += 1

            if strategy == STRATEGY.HILL_CLIMB_RANDOM_RESTART:
                if self.cur_tries == self.max_tries:
                    if not run_test:
                        print("Random Restart Hit max tries, Exit")
                    return current
                if not run_test:
                    print("Random Restart, Try: " + str(self.cur_tries))
                self.generate_start_state()
                return self.solve(strategy, run_test)
            else: 
                return current
        else:
            MAX_T = 1000
            t = 0
            while True:
                if current.cost == 0:
                    return current
                
                T = MAX_T - t
                if T == 0:
                    if current.cost != 0:
                        if not run_test:
                            print("Simulated Annealing Hit Temperature goes Zero, Exit")
                    return current
                neighbors = self.get_successors(current, strategy)
                neighbor = neighbors[0]
                delta = current.cost - neighbor.cost
                if delta > 0:
                    current = neighbor
                else:
                    p = 2.71828 ** (delta / T)
                    if p > randint(0, 100) / 100:
                        current = neighbor
                t += 1
                self.cur_cost += 1
    
class EightPuzzle(Problem):
    def __init__(self, goal_state) -> None:
        super().__init__(goal_state)

    def generate_start_state(self):
        state = self.goal_state.copy()
        actions = ['up', 'down', 'left', 'right']
        for i in range(100):
            action = actions[randint(0, 3)]
            self.__try_move(state, action)
        self.start_state = state

    def heuristic(self, state, strategy: STRATEGY):
        ret = 0
        for ith, s in enumerate(state):
            if s != 0:
                _x, _y = divmod(ith, 3)
                x, y = divmod(self.goal_state.index(s), 3)
                ret += abs(_x - x) + abs(_y - y)
        return ret

    def __try_move(self, state, action):
        zero_index = state.index(0)
        if action == 'up':
            if zero_index not in [0, 1, 2]:
                state[zero_index] = state[zero_index - 3]
                state[zero_index - 3] = 0
                return True
        if action == 'down':
            if zero_index not in [6, 7, 8]:
                state[zero_index] = state[zero_index + 3]
                state[zero_index + 3] = 0
                return True
        if action == 'left':
            if zero_index not in [0, 3, 6]:
                state[zero_index] = state[zero_index - 1]
                state[zero_index - 1] = 0
                return True
        if action == 'right':
            if zero_index not in [2, 5, 8]:
                state[zero_index] = state[zero_index + 1]
                state[zero_index + 1] = 0
                return True
        return False

    def get_successors(self, node: Node, strategy: STRATEGY) -> list[Node]:
        successors: list[Node] = []
        state = node.state

        actions = ['up', 'down', 'left', 'right']
        for action in actions:
            successor = state.copy()
            ret = self.__try_move(successor, action)
            if ret:
                successors.append(Node(successor, node, action, self.heuristic(successor, strategy)))
        
        candidates = []

        if strategy == STRATEGY.HILL_CLIMB_STEEP_ASCENT:
            min_cost = 100000000
            for successor in successors:
                if successor.cost < min_cost:
                    min_cost = successor.cost
            
            for successor in successors:
                if successor.cost == min_cost:
                    candidates.append(successor)
        
        if strategy == STRATEGY.HILL_CLIMB_FIRST_CHOICE:
            for successor in successors:
                if successor.cost <= node.cost:
                    candidates.append(successor)
            shuffle(candidates)

        if strategy == STRATEGY.HILL_CLIMB_RANDOM_RESTART:
            for successor in successors:
                candidates.append(successor)

        if strategy == STRATEGY.SIMULATED_ANNEALING:
            for successor in successors:
                candidates.append(successor)
            shuffle(candidates)

        return candidates

class EightQueens(Problem):
    N = 8
    
    def __init__(self, goal_state) -> None:
        super().__init__(goal_state)

    def generate_start_state(self):
        self.start_state = []
        for i in range(self.N):
            self.start_state.append(randint(0, self.N))
        # self.start_state = [2, 1, 2, 1]
        
    def heuristic(self, state, strategy: STRATEGY):
        # collisions between queens
        ret = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] == state[j]:
                    ret += 1
                if abs(state[i] - state[j]) == abs(i - j):
                    ret += 1
        return ret
        
    def __try_move(self, state, action, queen, step):
        if action == 'up':
            if state[queen] - step >= 0:
                state[queen] -= step
                return True
        if action == 'down':
            if state[queen] + step < self.N:
                state[queen] += step
                return True
        return False

    def get_successors(self, node: Node, strategy: STRATEGY) -> list[Node]:
        successors: list[Node] = []
        state = node.state

        actions = ['up', 'down']
        max_steps = self.N
        for step in range(1, max_steps + 1):
            for queen in range(len(state)):
                for action in actions:
                    successor = state.copy()
                    ret = self.__try_move(successor, action, queen, step)
                    if ret:
                        successors.append(Node(successor, node, action, self.heuristic(successor, strategy)))

        candidates = []

        if strategy == STRATEGY.HILL_CLIMB_STEEP_ASCENT:
            min_cost = 100000000
            for successor in successors:
                if successor.cost < min_cost:
                    min_cost = successor.cost
            
            for successor in successors:
                if successor.cost == min_cost:
                    candidates.append(successor)
        
        if strategy == STRATEGY.HILL_CLIMB_FIRST_CHOICE:
            for successor in successors:
                if successor.cost <= node.cost:
                    candidates.append(successor)
            shuffle(candidates)

        if strategy == STRATEGY.HILL_CLIMB_RANDOM_RESTART:
            for successor in successors:
                candidates.append(successor)

        if strategy == STRATEGY.SIMULATED_ANNEALING:
            for successor in successors:
                candidates.append(successor)
            shuffle(candidates)

        return candidates

ep = EightPuzzle([0, 1, 2, 3, 4, 5, 6, 7, 8])
ep.generate_start_state()
start_state = ep.get_start_state()

# ep = EightQueens(None)
# ep.generate_start_state()
# start_state = ep.get_start_state()

def run_test(p: Problem, start_state):
    results = []
    for strategy in STRATEGY:
        total = ITERATION
        success = 0
        total_search_cost = 0
        avg_search_cost = 0
        max_search_cost = -1
        min_search_cost = 100000000

        for i in range(ITERATION):
            p.reset_problem_counter(start_state)
            node = p.solve(strategy, True)
            success += 1 if node.cost == 0 else 0
            cur_cost = p.get_cur_cost()
            total_search_cost += cur_cost
            if cur_cost > max_search_cost:
                max_search_cost = cur_cost
            if cur_cost < min_search_cost:
                min_search_cost = cur_cost
        avg_search_cost = total_search_cost / total
        
        res = ""
        res += ("Strategy: " + str(strategy)) + ("\n")
        res += ("Success: " + str(success) + "/" + str(total)) + ("\n")
        res += ("Total Search Cost: " + str(total_search_cost)) + ("\n")
        res += ("Average Search Cost: " + str(avg_search_cost)) + ("\n")
        res += ("Max Search Cost: " + str(max_search_cost)) + ("\n")
        res += ("Min Search Cost: " + str(min_search_cost)) + ("\n")
        res += ("\n")
        results.append(res)

    results.insert(0, "\nStart State: " + str(start_state) + "\n")
    for result in results:
        print(result)

run_test(ep, start_state)