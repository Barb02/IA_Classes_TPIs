#STUDENT NAME: Bárbara Nóbrega Galiza
#STUDENT NUMBER: 105937

#DISCUSSED TPI-1 WITH: (names and numbers):
# José Gameiro 108840
# João Miguel Dias Andrade 107969
# Tomás Victal 109018
# Pedro Daniel Pinho 109986

from tree_search import *
import math

class OrderDelivery(SearchDomain):

    def __init__(self,connections, coordinates):
        self.connections = connections
        self.coordinates = coordinates

    def actions(self,state):
        city = state[0]
        actlist = []
        for (C1,C2,D) in self.connections:
            if (C1==city):
                actlist += [(C1,C2)]
            elif (C2==city):
               actlist += [(C2,C1)]
        return actlist 

    def result(self,state,action):
        (city, already_visited) = state
        (C1,C2) = action
        if C1==city:
            if C1 not in already_visited:
                already_visited.append(C1)
            return (C2, already_visited.copy())

    def satisfies(self, state, goal):
        (city, already_visited) = state
        (goal_city, target_cities) = goal
        if city in target_cities and city not in already_visited:
            already_visited.append(city)
        return (all(x in already_visited for x in target_cities) and city == goal_city)

    def cost(self, state, action):
        city = state[0]
        C1, C2 = action
        if C1==city:
            for (x1, x2, d) in self.connections:
                if (x1, x2) == action or (x2, x1) == action:
                    return d

    def heuristic(self, state, goal):
        (city, already_visited) = state
        (goal_city, target_cities) = goal
        missing_cities = [city for city in target_cities if city not in already_visited]
        if missing_cities == []:
            return math.dist(self.coordinates[city], self.coordinates[goal_city])
        total = 0
        for mc in missing_cities:
            total += math.dist(self.coordinates[city], self.coordinates[goal_city])
        return total
 
class MyNode(SearchNode):

    def __init__(self, state, parent, depth=None, cost=None, heuristic=None, eval=None):
        super().__init__(state,parent)
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.eval = eval
        self.marked_for_del = False
        self.children = []

class MyTree(SearchTree):

    def __init__(self, problem, strategy='breadth', maxsize=None):
        super().__init__(problem,strategy)
        root = MyNode(problem.initial, None, 0, 0, problem.domain.heuristic(problem.initial, problem.goal), problem.domain.heuristic(problem.initial, problem.goal))
        self.open_nodes = [root]
        self.solution = None
        self.non_terminals = 0
        self.terminals = 1
        self.maxsize = maxsize
    
    def astar_add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key = lambda x : (x.eval, x.state))
        
    def search2(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            self.terminals -= 1
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals += 1
                return self.get_path(node)
            self.non_terminals += 1
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    cost = node.cost + self.problem.domain.cost(node.state , a)
                    heuristic = self.problem.domain.heuristic(newstate, self.problem.goal)
                    newnode = MyNode(newstate, node, node.depth + 1, cost, heuristic, cost + heuristic)
                    node.children.append(newnode)
                    lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)
            self.terminals += len(lnewnodes)
            if self.strategy == "A*" and self.maxsize != None: 
                while self.terminals + self.non_terminals > self.maxsize:
                    self.manage_memory()
        return None

    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'A*':
            self.astar_add_to_open(lnewnodes)

    def manage_memory(self):
        rev_nodes = self.open_nodes[::-1]
        for node in rev_nodes:
            if not node.marked_for_del and node.parent != None:
                node.marked_for_del = True
                sibilings = [c for c in node.parent.children]
                marked_sibilings = [s for s in sibilings if s.marked_for_del]
                if sibilings == marked_sibilings:
                    min_eval = node.eval
                    for s in sibilings:
                        self.open_nodes.remove(s)
                        self.terminals -= 1
                        node.parent.children.remove(s)
                        if s.eval < min_eval:
                            min_eval = s.eval
                    node.parent.eval = min_eval
                    self.add_to_open([node.parent])
                    self.non_terminals -= 1
                    self.terminals += 1
                break

def orderdelivery_search(domain, city, targetcities, strategy='breadth', maxsize=None):
    p = SearchProblem(domain, (city, []), (city, targetcities))
    t = MyTree(p, strategy, maxsize)
    path = t.search2()
    cities = [s[0] for s in path]
    return (t, cities)