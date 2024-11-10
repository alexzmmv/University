from copy import deepcopy
from random import randrange


def write_file(graph, file_path):
    with open(file_path,"w+") as f:
        vertices=graph.vertices_num()
        edges=graph.edges_num()
        f.write(f"{vertices} {edges}\n")

        for node in graph.vertices_iterator():
            for neighbour in graph.out_neighbours_iterator(node):
                f.write("{0} {1} {2}\n".format(node,neighbour,graph.get_edge_cost(node, neighbour)))

def read_file(file_path):
    with (open(file_path) as f):
        if f is None:
            raise ValueError("File path doesn't exist")
        n, m = map(int, f.readline().split())
        g = Graph(n)
        for _ in range(m):
            vertex1, vertex2, edge_cost = map(int, f.readline().split())
            g.add_edge(vertex1, vertex2, edge_cost)
        return g


def random_graph(vertices_number, edges_number):
    if edges_number > vertices_number * (vertices_number - 1):
        raise ValueError("Too many edges for the number of vertices.")
    g = Graph()

    for i in range(vertices_number):
        g.add_vertex(i)
    for j in range(edges_number):
        vertex1 = randrange(vertices_number)
        vertex2 = randrange(vertices_number)
        while g.is_edge(vertex1, vertex2):
            vertex1 = randrange(vertices_number)
            vertex2 = randrange(vertices_number)
        g.add_edge(vertex1, vertex2, randrange(100))
    return g

class Graph:
    def __init__(self,vertices=0):
        self._vertices = set()
        self._g = dict()
        self._g_inverse = dict()
        self._cost = dict()
        for i in range(vertices):
            self._vertices.add(i)
            self._g[i]=set()
            self._g_inverse[i]=set()

    def vertices_iterator(self):
        for vertex in self._vertices:
            yield vertex

    def out_neighbours_iterator(self,vertex:int):
        if vertex not in self._g:
            raise ValueError("Invalid vertex.")
        for edge in self._g[vertex]:
            yield edge

    def in_neighbours_iterator(self,vertex:int):
        if vertex not in self._g:
            raise ValueError("Invalid vertex.")
        for edge in self._g_inverse[vertex]:
            yield edge

    def edges_iterator(self):
        for key,value in self._cost.items():
            yield key[0],key[1],value

    def is_vertex(self,vertex):
        return vertex in self._vertices

    def is_edge(self,vertex1,vertex2):
        return vertex1 in self._g and vertex2 in self._g[vertex1]

    def vertices_num(self):
        return len(self._vertices)

    def edges_num(self):
        return len(self._cost)

    def out_degree(self,vertex):
        if not self.is_vertex(vertex):
            raise ValueError("Invalid vertex")
        return len(self._g[vertex])

    def in_degree(self,vertex):
        if not self.is_vertex(vertex):
            raise ValueError("Invalid vertex")
        return len(self._g_inverse[vertex])

    def get_edge_cost(self,vertex1,vertex2):
        if (vertex1, vertex2) not in self._cost:
            raise ValueError("The specified edge does not exist.")
        return self._cost[(vertex1, vertex2)]

    def set_edge_cost(self, vertex1, vertex2, new_cost):
        if (vertex1, vertex2) not in self._cost:
            raise ValueError("The specified edge does not exist.")
        self._cost[(vertex1, vertex2)] = new_cost

    def add_edge(self,vertex1,vertex2,edge_cost):
        if self.is_edge(vertex1, vertex2):
            raise ValueError("The specified edge already exists")
        if not self.is_vertex(vertex1) or not self.is_vertex(vertex2):
            raise ValueError("The vertices on the edge do not exist.")
        self._g[vertex1].add(vertex2)
        self._g_inverse[vertex2].add(vertex1)
        self._cost[(vertex1, vertex2)] = edge_cost

    def remove_edge(self,vertex1,vertex2):
        if not self.is_edge(vertex1,vertex2):
            raise ValueError("Edge doesn't exist")
        del self._cost[(vertex1,vertex2)]
        self._g[vertex1].remove(vertex2)
        self._g_inverse[vertex2].remove(vertex1)

    def add_vertex(self,vertex):
        if self.is_vertex(vertex):
            raise ValueError("Invalid vertex")
        self._vertices.add(vertex)
        self._g[vertex] = set()
        self._g_inverse[vertex] = set()

    def remove_vertex(self,vertex):
        if not self.is_vertex(vertex):
            raise ValueError("Cannot remove a vertex which doesn't exist.")

        to_remove = []

        for node in self._g[vertex]:
            to_remove.append(node)

        for node in to_remove:
            self.remove_edge(vertex, node)
        to_remove = []

        for node in self._g_inverse[vertex]:
            to_remove.append(node)

        for node in to_remove:
            self.remove_edge(node, vertex)

        del self._g[vertex]
        del self._g_inverse[vertex]
        self._vertices.remove(vertex)

    def __deepcopy__(self):
        return deepcopy(self)
