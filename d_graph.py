# Course: CS261 - Data Structures
# Author: Kent Chau
# Assignment: 6
# Description: Graphs

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        add vertice to the directed graph
        """
        self.v_count += 1
        self.adj_matrix.append([0]*self.v_count)
        for i in range(self.v_count -1):
            self.adj_matrix[i].append(0)
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        add edge to direct graph with two vertices
        """
        if src >= self.v_count:
            return
        if dst >= self.v_count:
            return
        if weight <= 0:
            return
        if src == dst:
            return
        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        remove edge from directed graph
        """
        if src >= self.v_count:
            return
        if dst >= self.v_count:
            return
        if src < 0 or dst < 0:
            return

        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        return list of vertices in direct graph
        """
        v = []
        count = 0
        for i in range(self.v_count):
            v.append(i)
            count += 1
        return v

    def get_edges(self) -> []:
        """
        return list of edges
        """
        vert = []
        for i in range(self.v_count):
            for j in range(self.v_count):
                if self.adj_matrix[i][j] != 0:
                    vert.append((i, j, self.adj_matrix[i][j]))
        return vert

    def is_valid_path(self, path: []) -> bool:
        """
        return boolean value to see if path is valid or not
        """
        if path == []:
            return True
        check = []
        lista = self.get_edges()
        que = deque([])
        for j in lista:
            que.appendleft(j)
        lista.clear()
        while len(que) > 0:
            pop = que.pop()
            x, y, weight = pop
            lista.append((x, y))
        for i in range(1,len(path)):
            temp = (path[i-1], path[i])
            if temp in lista:
                check.append(True)
            else:
                check.append(False)
        if False in check:
            return False
        else:
            return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        depth first search for given vertex, return list
        """
        visited = []
        stack = []
        stack.append(v_start)
        while len(stack) > 0:
            pop = stack.pop()
            if pop not in visited:
                visited.append(pop)
            for i in range(self.v_count -1, -1, -1):
                if self.adj_matrix[pop][i] != 0:
                    if i not in visited:
                        stack.append(i)
        return visited


    def bfs(self, v_start, v_end=None) -> []:
        """
        breadth first search of given vertex, returns list
        """
        visited = []
        que = deque([])
        que.append(v_start)
        while len(que) > 0:
            pop = que.pop()
            if pop not in visited:
                visited.append(pop)
            for i in range(0, self.v_count):
                if self.adj_matrix[pop][i] !=0:
                    if i not in visited:
                        que.appendleft(i)
        return visited

    def double_spiderman(self):
        """assist has cycle function in checking if there are two
        vertices that are directed at each other creating a cycle"""
        list1 = []
        list2 = []
        for i in range(self.v_count):
            for j in range(self.v_count):
                if self.adj_matrix[i][j] != 0:
                    list1.append((i, j))
        for k in list1:
            x, y = k
            if (y, x) in list1:
                return True
        return False

    def has_cycle(self, vert=None):
        """
        boolean for finding if a given directed graph has a cycle
        """
        st = []
        check = []
        child = []
        if self.double_spiderman():
            return True

        counter = 0
        temp = []
        for i in range(self.v_count):
            temp.append(sorted(self.dfs(i)))
        for i in range(self.v_count):
            check.append(i)
        for ii in range(self.v_count):
            counter += 1
            child.append(-1)

        for m in temp:
            st.append(m)
        while len(st) > 1:
            pop = st.pop()
            temp.pop()
            for n in temp:
                if pop == n:
                    return True
        return False
    #     # ----------------------------
    #     visited = []
    #     st = []
    #     check = []
    #     if self.double_spiderman():
    #         return True
    #     if vert is None:
    #         for i in range(self.v_count):
    #             for j in range(self.v_count):
    #                 if self.adj_matrix[i][j] != 0:
    #                     check.append((i, j))
    #     else:
    #         check = vert
    #     # ------------------------
    #     while len(check) > 0:
    #         g = check.pop(0)
    #         st.append(g)
    #         while len(st) > 0:
    #             pop = st.pop()
    #             curr, next = pop
    #             stlen1 = len(st)
    #             for i in range(self.v_count):
    #                 if self.adj_matrix[next][i] != 0:
    #                     if i != curr:
    #                         st.append((next, i))
    #                         # if curr not in visited:
    #                         #     visited.append(curr)
    #                     if i in visited:
    #                         st.clear()
    #                         check.clear()
    #                         visited.clear()
    #                         return True
    #             if curr not in visited:
    #                 visited.append(curr)
    #             stlen2 = len(st)
    #             # if stlen1 == stlen2 and stlen2 > 0:
    #             #     #visited.pop(len(visited)-1)
    #             #     st.pop()
    #         visited.clear()
    #     # ------------------------------------
    #     return False
    #
    # # ------third way--------------
    # visited = []
    # st = []
    # check = []
    # if self.double_spiderman():
    #     return True
    # # if vert is None:
    # #     for i in range(self.v_count):
    # #         for j in range(self.v_count):
    # #             if self.adj_matrix[i][j] != 0:
    # #                 check.append((i, j))
    #
    # for i in range(self.v_count):
    #     check.append(i)
    # # ------------------------
    # while len(check) > 0:
    #     g = check.pop(0)
    #     st.append(g)
    #     while len(st) > 0:
    #         pop = st.pop()
    #         if pop in check:
    #             check.remove(pop)
    #         # curr, next = pop
    #         # stlen1 = len(st)
    #         for i in range(self.v_count):
    #             if self.adj_matrix[pop][i] != 0:
    #                 # maybe use list in list in place of tuples?
    #                 if i != pop:
    #                     st.append(i)
    #                 if i in visited:
    #                     return True
    #         if pop not in visited:
    #             visited.append(pop)
    # # ------------------------------------
    # return False

    def findMinDistanceNode(self, distanceArray, visited):
        """assist dijkstra in finding minimum distance"""
        minDistance = float('inf')
        minIndex = -1
        for i in range(self.v_count):
            if distanceArray[i] < minDistance and visited[i] == False:
                minDistance = distanceArray[i]
                minIndex = i

        return minIndex

    def dijkstra(self, src: int) -> []:
        """
        return list of shortest paths from one node to another
        """
        distanceArray = [float('inf')] * self.v_count
        visited = [False]*self.v_count

        distanceArray[src] = 0

        for vertexCount in range(self.v_count):
            minDistanceNodeIndex = self.findMinDistanceNode(distanceArray, visited)

            visited[minDistanceNodeIndex] = True

            for jj in range(self.v_count):
                if self.adj_matrix[minDistanceNodeIndex][jj] != 0:
                    if visited[jj] == False:
                        if (distanceArray[minDistanceNodeIndex] + self.adj_matrix[minDistanceNodeIndex][jj]) < distanceArray[jj]:
                            distanceArray[jj] = distanceArray[minDistanceNodeIndex] + self.adj_matrix[minDistanceNodeIndex][jj]

        return distanceArray


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # edges = [(0,2, 5), (3,0, 1), (5,2, 2), (5, 10, 3), (7, 5, 4), (7, 9, 5), (9, 0, 6),
    #          (9, 12, 7), (10, 1, 8), (10, 5, 9), (10, 9, 10), (10, 12, 11), (11, 5, 12), (12, 7, 13)]
    # edges = [(0, 12, 1), (1, 0, 2), (2, 11, 3), (3 ,7, 4), (3, 12, 5), (4, 7, 6), (9, 10, 7),
    #          (6, 10, 8), (7, 11, 9), (8, 11, 10), (9, 8, 11), (9, 10, 12), (10, 5, 13),
    #          (11, 9, 14)]
    # edges = [(0, 12, 1), (4, 12, 2), (5, 9, 3), (6, 3, 4), (7, 5, 5), (7, 8, 6), (8, 3, 7),
    #          (8, 10, 8), (10, 0, 9), (10, 7, 10), (11, 3, 11), (12, 6 ,12)]
    # edges = [(0, 10, 1), (1, 4, 2), (1, 7, 3), (4, 3, 4), (4, 10, 5), (5, 4, 6),
    #          (6, 7, 7), (7, 5, 8), (8, 0, 9), (8, 7, 10), (12, 3, 11), (12, 11, 12)] #false
    # edges = [(2, 8, 1), (2, 12, 2), (5, 6, 3), (6, 7, 4), (6, 11, 5), (7, 4, 6), (7, 8, 7),
    #          (8, 12, 8), (9, 0, 9), (9, 3, 10), (9, 4, 11), (10, 2, 12), (10, 5, 13), (12, 3, 14)] #false
    # edges = [(0, 10, 1), (1, 5, 2), (2, 11, 3), (6, 7, 4), (6, 12, 5), (7, 3, 6),
    #          (7, 12, 7), (8, 1, 8), (11, 0, 9), (11, 6, 10), (12, 0, 11)] #false##
    # edges = [(1, 5, 1), (1, 8, 2), (1, 9, 3), (2, 4, 4), (3, 11, 5),
    #          (3, 8, 6), (6, 8, 7), (7, 1, 9), (8, 11, 1), (11, 7, 2), (11, 9, 3),
    #          (12, 4, 6)] #true


    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0, 99)]
    for src, dst, *weight in edges_to_add:
        g.add_edge(src, dst, *weight)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    # print(g.has_cycle())
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
