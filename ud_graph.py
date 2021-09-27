# Course: 261 data structures
# Author: Kent Chau
# Assignment: 6
# Description: Graphs

import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        dict = self.adj_list
        if v not in dict:
            dict[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return
        if u not in self.adj_list:
            self.add_vertex(u)
            self.add_edge(u, v)
        if v not in self.adj_list:
            self.add_vertex(v)
            self.add_edge(u, v)
        if u in self.adj_list:
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
        if v in self.adj_list:
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        for i in self.adj_list.keys():
            if i == v:
                if u in self.adj_list[i]:
                    self.adj_list[i].remove(u)
        for j in self.adj_list.keys():
            if j == u:
                if v in self.adj_list[j]:
                    self.adj_list[u].remove(v)


    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """

        if v in self.adj_list:
            self.adj_list.pop(v)
        for aa in self.adj_list.values():
            if v in aa:
                aa.remove(v)


    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        vert2 = []
        for a in self.adj_list.keys():
            if a not in vert2:
                vert2.append(a)
        return vert2

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edges = []
        for j in self.adj_list.keys():
            for k in self.adj_list[j]:
                tup = (j, k)
                tup2 = (k, j)
                if tup not in edges and tup2 not in edges:
                    edges.append(tup)
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        check = []
        if path == []:
            return True
        if len(path) == 1 and path[0] not in self.adj_list.keys():
            return False
        for i in range(1, len(path)):
            if path[i] in self.adj_list[path[i-1]]:
                check.append(True)
            else:
                check.append(False)
        if False in check and len(check) > 0:
            return False
        else:
            return True

    def sortThis(self, arr):
        """sort a given array then reverse the order"""
        for index in range(1, len(arr)):
            v = arr[index]
            p = index -1
            while p >= 0 and arr[p] > v:
                arr[p +1] = arr[p]
                p -= 1
            arr[p +1] = v
        arr.reverse()

    def sortThisOrdered(self, arr):
        """sort a given array then reverse the order"""
        for index in range(1, len(arr)):
            v = arr[index]
            p = index -1
            while p >= 0 and arr[p] > v:
                arr[p +1] = arr[p]
                p -= 1
            arr[p +1] = v

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """

        visited = []
        stack1 = []
        stack1.append(v_start)
        if v_start not in self.adj_list.keys():
            return visited
        while len(stack1) > 0:
            pop = stack1.pop()
            if pop not in visited:
                visited.append(pop)
            if pop == v_end:
                break
            self.sortThis(self.adj_list[pop])
            for i in self.adj_list[pop]:
                if i not in visited:
                    stack1.append(i)
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        visited = []
        que = deque([])
        que.append(v_start)
        if v_start not in self.adj_list.keys():
            return visited
        while len(que) > 0:
            pop = que.pop()
            if pop not in visited:
                visited.append(pop)
            self.sortThisOrdered(self.adj_list[pop])
            for i in self.adj_list[pop]:
                if i not in visited:
                    que.appendleft(i)
            if visited[len(visited) -1] == v_end:
                break
        return visited


    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        counter = 0
        vertices = []
        for keys in self.adj_list.keys():
            vertices.append(keys)
        while len(vertices) > 0:
            for i in vertices:
                counter += 1
                temp = self.dfs(i)
                for j in temp:
                    if j in vertices:
                        vertices.remove(j)

        return counter

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        ll = []
        return self.has_cycleHelper(ll)

    def has_cycleHelper(self, lis, k=None):
        """assistive recursive function for checking for cycle"""
        visited = []
        st = []
        a = None
        b = None
        lista = []
        if lis == []:
            for keys in self.adj_list.keys():
                lista.append(keys)
        else:
            lista = lis
        for keys in self.adj_list.keys():
            if self.adj_list[keys] != []:
                a = keys
                break
        if k is not None:
            st.append(k)
            a = k
        else:
            st.append(a)
        parent = None
        while len(st) > 0:
            pop = st.pop()
            if type(pop) is tuple:
                a, b = pop

            for i in self.adj_list[a]:
                if i != b:
                    st.append((i,a))
                if i in visited and i != b:
                    return True
            if a not in visited:
                if a in lista:
                    lista.remove(a)
                visited.append(a)
        if len(lista) > 1:
            return self.has_cycleHelper(lista, lista[0])
        return False

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', 'FG', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    g.remove_edge('D', 'G')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    #
    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    #edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    edges = ['EC', 'CE', 'CB','JG', 'JI', 'GJ', 'FA', 'FH', 'AF', 'AH', 'HA', 'HF', 'BK', 'BC', 'BI', 'KB', 'IJ', 'IB']
    g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
    #     'add FG', 'remove GE')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print('{:<10}'.format(case), g.has_cycle())
    g.has_cycle()
    print(g.has_cycle())