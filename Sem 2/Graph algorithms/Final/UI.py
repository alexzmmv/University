from Graph import *


class UI:
    def __init__(self,graph=None):
        if graph is None:
            graph=Graph()
            self.__graph_name="Empty graph with 10 vertices."
        self.__graph=graph
        self.__graph_name="Default graph."

    def graph_menu(self):
        def print_menu():
            print("1. Add vertex.")
            print("2. Add edge.")
            print("3. Remove vertex.")
            print("4. Remove edge.")
            print("5. Update cost.")
            print("6. Print graph.")
            print("7. Print graph to file.")
            print("8. Get the number of vertices.")
            print("9. Get the number of edges.")
            print("10. Check if there is an edge between two vertices.")
            print("11. Get the in degree of a vertex.")
            print("12. Get the out degree of a vertex.")
            print("13. Get the in neighbours of a vertex.")
            print("14. Get the out neighbours of a vertex.")
            print("15. Get the cost of an edge.")

            print("0. Exit/Switch graph.")


        def add_vertex():
            try:
                vertex=int(input("Give vertex: "))
            except ValueError:
                print("Invalid input.")
                return
            try:
                self.__graph.add_vertex(vertex)
            except ValueError as z:
                print(z)

        def add_edge():
            try:
                vertex1=int(input("Give first vertex: "))
                vertex2=int(input("Give second vertex: "))
                cost=int(input("Give cost: "))
            except ValueError:
                print("Invalid input.")
                return
            try:
                self.__graph.add_edge(vertex1,vertex2,cost)
            except ValueError as zv:
                print(zv)

        def remove_vertex():
            try:
                vertex=int(input("Give vertex: "))
            except ValueError:
                print("Invalid input.")
                return
            try:
                self.__graph.remove_vertex(vertex)
            except ValueError as zx:
                print(zx)

        def remove_edge():
            try:
                vertex1=int(input("Give first vertex: "))
                vertex2=int(input("Give second vertex: "))
            except ValueError:
                print("Invalid input.")
                return
            try:
                self.__graph.remove_edge(vertex1,vertex2)
            except ValueError as zv:
                print(zv)

        def update_cost():
            try:
                vertex1=int(input("Give first vertex: "))
                vertex2=int(input("Give second vertex: "))
                cost=int(input("Give new cost: "))
            except ValueError:
                print("Invalid input.")
                return
            try:
                self.__graph.update_cost(vertex1,vertex2,cost)
            except ValueError as zv:
                print(zv)

        def print_graph():
            print("Vertices: ")
            for vertex in self.__graph.vertices_iterator():
                print(vertex)
            print("Edges: ")
            for edge in self.__graph.edges_iterator():
                print(edge[0],edge[1],edge[2])

            for edge in self.__graph.edges_iterator():
                print(edge[0],edge[1],edge[2])

        def print_graph_to_file():
            file_name=input("Give file path: ")
            try:
                write_file(self.__graph,file_name)
            except ValueError as zv:
                print(zv)
        def get_vertices_num():
            print(self.__graph.vertices_num())
        def get_edges_num():
            print(self.__graph.edges_num())
        def check_edge():
            try:
                vertex1=int(input("Give first vertex: "))
                vertex2=int(input("Give second vertex: "))
            except ValueError:
                print("Invalid input.")
                return
            print(self.__graph.is_edge(vertex1,vertex2))
        def get_in_degree():
            try:
                vertex=int(input("Give vertex: "))
            except ValueError:
                print("Invalid input.")
                return
            print(self.__graph.in_degree(vertex))
        def get_out_degree():
            try:
                vertex=int(input("Give vertex: "))
            except ValueError:
                print("Invalid input.")
                return
            print(self.__graph.out_degree(vertex))
        def get_in_neighbours():
            try:
                vertex=int(input("Give vertex: "))
            except ValueError:
                print("Invalid input.")
                return
            for neighbour in self.__graph.in_neighbours_iterator(vertex):
                print(neighbour)
        def get_out_neighbours():
            try:
                vertex=int(input("Give vertex: "))
            except ValueError:
                print("Invalid input.")
                return
            for neighbour in self.__graph.out_neighbours_iterator(vertex):
                print(neighbour)
        def get_edge_cost():
            try:
                vertex1=int(input("Give first vertex: "))
                vertex2=int(input("Give second vertex: "))
            except ValueError:
                print("Invalid input.")
                return
            print(self.__graph.get_edge_cost(vertex1,vertex2))

        while True:
            print_menu()
            try:
                command=input("Give command: ")
                if command=="1":
                    add_vertex()
                elif command=="2":
                    add_edge()
                elif command=="3":
                    remove_vertex()
                elif command=="4":
                    remove_edge()
                elif command=="5":
                    update_cost()
                elif command=="6":
                    print_graph()
                elif command=="7":
                    print_graph_to_file()
                elif command=="8":
                    get_vertices_num()
                elif command=="9":
                    get_edges_num()
                elif command=="10":
                    check_edge()
                elif command=="11":
                    get_in_degree()
                elif command=="12":
                    get_out_degree()
                elif command=="13":
                    get_in_neighbours()
                elif command=="14":
                    get_out_neighbours()
                elif command=="15":
                    get_edge_cost()
                elif command=="0":
                    break
                else:
                    print("Invalid command.")
            except ValueError as ve:
                print(ve)
            except Exception as e:
                print(e)
    def run(self):
        def switch_graph_menu():
            print("1. Empty graph with n vertices.")
            print("2. Predefined graph.")
            print("3. Graph from file.")
            print("4. Modify graph menu.")
            print("0. Exit.")

        def predefined_graph_menu():
            print("1. Graph 1k:")
            print("2. Graph 10k:")
            print("3. Graph 100k:")
            print("4. Graph 1M:")
            print("5. Random graph.")
            print("0. Exit.")

        def predefined_graph():
            while True:
                predefined_graph_menu()
                inp=input("Give command: ")
                if inp=="1":
                    self.__graph=read_file("./PreDefGraph/graph1k.txt")
                    self.__graph_name="Graph 1k."
                elif inp=="2":
                    self.__graph=read_file("./PreDefGraph/graph10k.txt")
                    self.__graph_name="Graph 10k."
                elif inp=="3":
                    self.__graph=read_file("./PreDefGraph/graph100k.txt")
                    self.__graph_name="Graph 100k."
                elif inp=="4":
                    self.__graph=read_file("./PreDefGraph/graph1M.txt")
                    self.__graph_name="Graph 1M."
                elif inp=="5":
                    vertices_num=int(input("Give number of vertices: "))
                    edges_num=int(input("Give number of edges: "))
                    try:
                        self.__graph=random_graph(vertices_num,edges_num)
                        self.__graph_name="Random graph."
                    except ValueError as zv:
                        print(zv)
                elif inp=="0":
                    return
                else:
                    print("Invalid command.")
                print(f"Current graph: {self.__graph_name}")

        while True:
            switch_graph_menu()
            print(f"Current graph: {self.__graph_name}")
            command=input("Give command: ")
            if command=="1":
                vertices_num=int(input("Give number of vertices: "))
                self.__graph=Graph(vertices_num)
                gr_name=input("Give your graph a name: ")
                self.__graph_name=gr_name
            elif command=="2":
                predefined_graph()
            elif command=="3":
                file_path=input("Give file path: ")
                try:
                    self.__graph=read_file(file_path)
                except ValueError as ve:
                    print(ve)
            elif command=="4":
                self.graph_menu()
            elif command=="0":
                return
            else:
                print("Invalid command.")
