import random
class Node(object):
    def __init__(self, value):
        self.neighbors = set()
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Node): return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return "|Node " + str(self.value) + ": " + str(self.neighbors) + "|\n"


def make_graph(relations):
    graph = dict() # list of nodes
    for val in relations:
        neighbors = relations[val]
        if val not in graph:
            node = Node(val)
            graph[val] = node
        else:
            node = graph[val]

        for neighbor in neighbors:
            node.neighbors.add(neighbor)

            if neighbor not in graph:
                neighbor_node = Node(neighbor)
                graph[neighbor] = neighbor_node

            graph[neighbor].neighbors.add(val)

    return graph


def dfs(graph, start_node, seen = None):
    if seen == None: seen = set()

    if start_node in seen: return seen

    seen.add(start_node)

    neighbors = graph[start_node].neighbors
    for neighbor in neighbors:
        seen = dfs(graph, neighbor, seen)

    return seen


def createAlliances(relations):
    graph = make_graph(relations)

    result = dict()

    while (len(graph) > 0):
        start_node = random.choice(list(graph.keys()))
        seen = dfs(graph, start_node)

        result[start_node] = seen

        for elem in seen:
            del graph[elem]

    return result



# d = {0: set(),
#      1: {2, 4, 5, 6, 7},
#      2: {3, 4},
#      3: set(),
#      4: {5, 6},
#      5: {6, 7},
#      6: {7},
#      7: set()}
# print(createAlliances(d))

