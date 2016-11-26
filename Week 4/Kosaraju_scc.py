import logging
import sys
from collections import deque, defaultdict


class Kosaraju:
    def __init__(self, graph, rev_graph):
        self.__graph, self.__rev_graph = graph, rev_graph
        self.__current_leader = None
        self.__leaders = defaultdict(set)
        self.__done, self.__explored = set(), set()
        self.__order = deque()

    def __dfs(self, graph, node):
        # stack realization
        stack = deque([node])
        while stack:
            vertex = stack.pop()
            if vertex not in self.__explored:
                self.__explored.add(vertex)
                # on the first pass __current_leader == None
                if self.__current_leader is not None:
                    self.__leaders[self.__current_leader].add(vertex)
                # vertex will be popped after all its adjacent vertices
                stack.append(vertex)
                to_add = graph[vertex] - self.__explored if vertex in graph else set()
                if len(to_add) > 0:
                    stack.extend(to_add)
            # it's the second time we pop vertex from stack
            else:
                if vertex not in self.__done:
                    self.__done.add(vertex)
                    self.__order.appendleft(vertex)

    def __calculate_magic_numbers(self):
        for node in self.__rev_graph.keys():
            if node not in self.__explored:
                self.__dfs(self.__rev_graph, node)

    def __calculate_leaders(self):
        self.__calculate_magic_numbers()
        logger.info('Magic times calculated')
        self.__explored = set()
        for node in self.__order:
            if node not in self.__explored:
                self.__current_leader = node
                self.__dfs(self.__graph, node)

    @property
    def leaders(self):
        self.__calculate_leaders()
        return self.__leaders


def load_graphs(file_name):
    graph, rev_graph = defaultdict(set), defaultdict(set)
    # the size of the file is reasonable for this problem, can speed things up by loading the whole file
    with open(file_name) as data:
        file_contents = data.read()
    # build both graph and reversed graph in one go
    for line in file_contents.split('\n'):
        spl = line.split()
        head, tail = map(int, spl)
        graph[head].add(tail)
        rev_graph[tail].add(head)
    return graph, rev_graph

if __name__ == '__main__':
    # initialize logging to console
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(levelname)s [%(funcName)s] %(message)s',
                                  datefmt='%Y-%m-%d\t%H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # actual start
    logger.info('Program started')
    g1, g2 = load_graphs('SCC.txt')
    logger.info('Data loaded from file')
    # initialize our Kosaraju object
    kosaraju = Kosaraju(g1, g2)
    logger.info('Kosaraju initialized')
    # calculate leaders
    leaders_dict = kosaraju.leaders
    logger.info('Calculated SCC leaders')
    for i in sorted(leaders_dict, key=lambda k: len(leaders_dict[k]), reverse=True)[:5]:
        print(len(leaders_dict[i]))
    logger.info('Done')
