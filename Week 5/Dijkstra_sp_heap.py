import heapq
import math


class Heap:
    """
    heap data structure with removing based on
    https://docs.python.org/3.5/library/heapq.html#priority-queue-implementation-notes
    need to mark deleted -1, otherwise when comparing [math.inf, '<removed-task>'], [math.inf, 4]
    Python will error out:
    http://stackoverflow.com/questions/16373809/python-huffman-coding-exception-unorderable-types
    """

    def __init__(self, graph, source):
        # create a list to serve as heap, assign the source vertex the score of 0, infinity for the rest
        heap = [[0 if node == source else math.inf, node] for node in graph.keys()]
        heapq.heapify(heap)
        self.heap = heap  # list of entries arranged in a heap
        self.entry_finder = {i[-1]: i for i in heap}  # mapping of nodes to entries (score, node)
        self.REMOVED = -1  # placeholder for a removed node

    def add_node(self, node, score=0):
        """Add a new node or update the Dijkstra score of an existing node"""
        if node in self.entry_finder:
            self.remove_node(node)
        entry = [score, node]
        self.entry_finder[node] = entry
        heapq.heappush(self.heap, entry)

    def remove_node(self, node):
        """Mark an existing node as REMOVED.  Raise KeyError if not found."""
        entry = self.entry_finder.pop(node)
        entry[-1] = self.REMOVED

    def get_score(self, node):
        """Get node's old score in O(1) time before updating it"""
        return self.entry_finder[node][0]

    def pop_node(self):
        """Remove and return the node with the lowest Dijkstra score. Raise KeyError if empty."""
        while self.heap:
            score, node = heapq.heappop(self.heap)
            if node is not self.REMOVED:
                del self.entry_finder[node]
                return score, node
        raise KeyError('pop from an empty priority queue')


def calculate_dijkstra_sp(edges_dict, heap):
    length = len(edges_dict)  # the number of vertices n
    explored = set()
    unexplored = set(node for node in edges_dict.keys())
    shortest_paths = {}
    while len(explored) < length:
        new_score, new_vertex = heap.pop_node()  # we pop next vertex w
        explored.add(new_vertex)
        unexplored.remove(new_vertex)
        shortest_paths[new_vertex] = new_score
        for node, edge_length in edges_dict[new_vertex]:  # for each v of edges (w, v)
            if node in unexplored:  # if it's a crossing edge
                current_score = heap.get_score(node)  # set its score to the min{(its current score), (A[w] + L(w, v))}
                heap.remove_node(node)
                score = min(current_score, new_score + edge_length)
                heap.add_node(node, score)
    return shortest_paths


def load_graph_from_file(file_name):
    """Read the file line by line, process the vertices, edges and weights
    return a graph in a form of dictionary: {tail: [(head, length), (head, length)...}"""
    graph = {}
    with open(file_name) as data:
        for line in data:
            spl = line.split()
            if spl:
                tail = int(spl.pop(0))
                graph[tail] = [tuple(map(int, i.split(','))) for i in spl]
    return graph


def provide_answer():
    gr = load_graph_from_file('SP.txt')
    heap = Heap(gr, 1)
    sp = calculate_dijkstra_sp(gr, heap)
    vertices = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    for vertex in vertices:
        print(sp[vertex])


if __name__ == '__main__':
    provide_answer()
