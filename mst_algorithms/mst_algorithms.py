import heapq
import time
import sys
from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []
        self.adj = [[] for _ in range(vertices)]
    
    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

# Prim's Algorithm
def prim(graph):
    start_time = time.time()
    
    V = graph.V
    key = [sys.maxsize] * V
    parent = [None] * V
    key[0] = 0
    mst_set = [False] * V
    
    for _ in range(V):
        min_key = sys.maxsize
        u = 0
        for v in range(V):
            if key[v] < min_key and not mst_set[v]:
                min_key = key[v]
                u = v
        
        mst_set[u] = True
        
        for v, w in graph.adj[u]:
            if not mst_set[v] and w < key[v]:
                key[v] = w
                parent[v] = u
    
    end_time = time.time()
    
    mst = []
    total_weight = 0
    for i in range(1, V):
        mst.append((parent[i], i, key[i]))
        total_weight += key[i]
    
    return {
        'mst': mst,
        'total_weight': total_weight,
        'time': end_time - start_time
    }

# Kruskal's Algorithm
def kruskal(graph):
    start_time = time.time()
    
    result = []
    i = 0
    e = 0
    
    graph.graph = sorted(graph.graph, key=lambda item: item[2])
    
    parent = []
    rank = []
    
    for node in range(graph.V):
        parent.append(node)
        rank.append(0)
    
    while e < graph.V - 1:
        u, v, w = graph.graph[i]
        i += 1
        x = find(parent, u)
        y = find(parent, v)
        
        if x != y:
            e += 1
            result.append((u, v, w))
            union(parent, rank, x, y)
    
    end_time = time.time()
    
    total_weight = sum(edge[2] for edge in result)
    
    return {
        'mst': result,
        'total_weight': total_weight,
        'time': end_time - start_time
    }

# Helper functions for Kruskal's Algorithm
def find(parent, i):
    if parent[i] != i:
        parent[i] = find(parent, parent[i])
    return parent[i]

def union(parent, rank, x, y):
    x_root = find(parent, x)
    y_root = find(parent, y)
    
    if rank[x_root] < rank[y_root]:
        parent[x_root] = y_root
    elif rank[x_root] > rank[y_root]:
        parent[y_root] = x_root
    else:
        parent[y_root] = x_root
        rank[x_root] += 1

# Borůvka's Algorithm
def boruvka(graph):
    start_time = time.time()
    
    parent = list(range(graph.V))
    mst = []
    num_trees = graph.V
    
    while num_trees > 1:
        cheapest = [-1] * graph.V
        
        for u, v, w in graph.graph:
            set1 = find(parent, u)
            set2 = find(parent, v)
            
            if set1 != set2:
                if cheapest[set1] == -1 or cheapest[set1][2] > w:
                    cheapest[set1] = (u, v, w)
                if cheapest[set2] == -1 or cheapest[set2][2] > w:
                    cheapest[set2] = (u, v, w)
        
        for i in range(graph.V):
            if cheapest[i] != -1:
                u, v, w = cheapest[i]
                set1 = find(parent, u)
                set2 = find(parent, v)
                
                if set1 != set2:
                    mst.append((u, v, w))
                    union(parent, [0]*graph.V, set1, set2)
                    num_trees -= 1
    
    end_time = time.time()
    
    total_weight = sum(edge[2] for edge in mst)
    
    return {
        'mst': mst,
        'total_weight': total_weight,
        'time': end_time - start_time
    }

# Heap-based Prim's Algorithm for comparison
def prim_heap(graph):
    start_time = time.time()
    
    V = graph.V
    key = [sys.maxsize] * V
    parent = [None] * V
    mst_set = [False] * V
    
    heap = []
    heapq.heappush(heap, (0, 0))
    key[0] = 0
    
    while heap:
        current_key, u = heapq.heappop(heap)
        
        if mst_set[u]:
            continue
        
        mst_set[u] = True
        
        for v, w in graph.adj[u]:
            if not mst_set[v] and w < key[v]:
                key[v] = w
                parent[v] = u
                heapq.heappush(heap, (w, v))
    
    end_time = time.time()
    
    mst = []
    total_weight = 0
    for i in range(1, V):
        mst.append((parent[i], i, key[i]))
        total_weight += key[i]
    
    return {
        'mst': mst,
        'total_weight': total_weight,
        'time': end_time - start_time
    }

# Example usage and complexity analysis
def main():
    # Create a sample graph
    g = Graph(5)
    g.add_edge(0, 1, 2)
    g.add_edge(0, 3, 6)
    g.add_edge(1, 2, 3)
    g.add_edge(1, 3, 8)
    g.add_edge(1, 4, 5)
    g.add_edge(2, 4, 7)
    g.add_edge(3, 4, 9)
    
    print("=== Minimum Spanning Tree Algorithms ===")
    print()
    
    # Run Prim's Algorithm
    prim_result = prim(g)
    print("1. Prim's Algorithm:")
    print(f"   MST: {prim_result['mst']}")
    print(f"   Total Weight: {prim_result['total_weight']}")
    print(f"   Execution Time: {prim_result['time']:.10f} seconds")
    print(f"   Time Complexity: O(V^2)")
    print(f"   Space Complexity: O(V)")
    print()
    
    # Run Heap-based Prim's Algorithm
    prim_heap_result = prim_heap(g)
    print("2. Heap-based Prim's Algorithm:")
    print(f"   MST: {prim_heap_result['mst']}")
    print(f"   Total Weight: {prim_heap_result['total_weight']}")
    print(f"   Execution Time: {prim_heap_result['time']:.10f} seconds")
    print(f"   Time Complexity: O(E log V)")
    print(f"   Space Complexity: O(V + E)")
    print()
    
    # Run Kruskal's Algorithm
    kruskal_result = kruskal(g)
    print("3. Kruskal's Algorithm:")
    print(f"   MST: {kruskal_result['mst']}")
    print(f"   Total Weight: {kruskal_result['total_weight']}")
    print(f"   Execution Time: {kruskal_result['time']:.10f} seconds")
    print(f"   Time Complexity: O(E log E)")
    print(f"   Space Complexity: O(E)")
    print()
    
    # Run Borůvka's Algorithm
    boruvka_result = boruvka(g)
    print("4. Borůvka's Algorithm:")
    print(f"   MST: {boruvka_result['mst']}")
    print(f"   Total Weight: {boruvka_result['total_weight']}")
    print(f"   Execution Time: {boruvka_result['time']:.10f} seconds")
    print(f"   Time Complexity: O(E log V)")
    print(f"   Space Complexity: O(V + E)")
    print()
    
    print("=== Complexity Comparison ===")
    print("\nAlgorithm | Time Complexity | Space Complexity")
    print("--------------------------------------------")
    print("Prim (Array) | O(V²) | O(V)")
    print("Prim (Heap) | O(E log V) | O(V + E)")
    print("Kruskal | O(E log E) | O(E)")
    print("Borůvka | O(E log V) | O(V + E)")
    print()
    
    print("=== Performance Comparison on Sample Graph ===")
    print("\nAlgorithm | Execution Time (seconds)")
    print("----------------------------------------")
    print(f"Prim (Array) | {prim_result['time']:.10f}")
    print(f"Prim (Heap) | {prim_heap_result['time']:.10f}")
    print(f"Kruskal | {kruskal_result['time']:.10f}")
    print(f"Borůvka | {boruvka_result['time']:.10f}")

if __name__ == "__main__":
    main()