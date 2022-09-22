from ctypes import Union
import os
from xmlrpc.client import MAXINT

class Node(object):
    def __init__(self, state, parent, action, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __repr__(self):
        ret = ""
        for i in self.state:
            if i != self.state[-1]:
                ret += chr(ord('a') + i) + "->"
            else:
                ret += chr(ord('a') + i)
        return ret

class TSP():
    __dis = []
    __num_cities = 0
    __start_state = [0]

    def __init__(self, o):
        if type(o) == str:
            if os.access(o, os.R_OK):
                self.__read_file(o)
        if type(o) == list[list]:
            self.__dis = o

    def __read_file(self, filename):
        with open(filename, 'r') as f:
            self.__num_cities = int(f.readline())
            for i in range(self.__num_cities):
                self.__dis.append([int(x) for x in f.readline().split()])
    
    def __heristic_mst(self, partial):
        # prim
        V = []
        U = []
        MST = []
        for v in range(self.__num_cities):
            if v not in partial:
                V.append(v)
        if len(V) == 0:
            return 0
        s = V[0]
        U.append(s)
        cost = 0
        while len(U) != len(V):
            min_dis = 100000000
            min_v = None
            min_u = None
            for u in U:
                for v in V:
                    if v not in U and self.__dis[u][v] != 0 and self.__dis[u][v] < min_dis:
                        min_dis = self.__dis[u][v]
                        min_v = v
                        min_u = u
            if min_v != None and min_u != None:
                U.append(min_v)
                MST.append((min_u, min_v))
                cost += min_dis
            else: 
                return 100000000
        # print(MST)
        return cost
    
    def __get_successors(self, node: Node) -> list[Node]:
        def calc_gh(node: Node, next_node: Node):
            to_be_chosen_state = node.state + [next_node]
            _min_cost = 100000000
            for s in node.state:
                if self.__dis[s][next_node] != 0 and self.__dis[s][next_node] < _min_cost:
                    _min_cost = self.__dis[s][next_node]
            g = _min_cost + node.cost
            h = self.__heristic_mst(to_be_chosen_state)
            return g, h
            
        successors = []
        min_cost = 100000000
        for i in range(self.__num_cities):
            if i not in node.state:
                g, h = calc_gh(node, i)
                if g + h <= min_cost:
                    min_cost = g + h
        
        for i in range(self.__num_cities):
            if i not in node.state:
                g, h = calc_gh(node, i)
                if g + h == min_cost:
                    successors.append(Node(node.state + [i], node, i, g))
        return successors
        
    def is_goal(self, state):
        return len(state) == self.__num_cities
    
    def start_state(self):
        return self.__start_state

    def solve(self):
        frontier = [Node(self.start_state(), None, None, 0)]
        explored = []
        nodes_to_be_expanded = 0
        while frontier:
            node = frontier.pop()
            if self.is_goal(node.state):
                return [node, nodes_to_be_expanded]
            explored.append(node.state)
            for successor in self.__get_successors(node):
                frontier.insert(0, successor)
                nodes_to_be_expanded += 1
        return [None, nodes_to_be_expanded]

tsp = TSP("tsp.map")
[node, nodes_to_be_expanded] = tsp.solve()
print(node.state)
print(node)
print("Expand: " + str(nodes_to_be_expanded))
