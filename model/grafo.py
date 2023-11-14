import json


class Graph:
    def __init__(self):
        self.nodes = dict()

    def loadFromJson(self, graph_name):
        with open(graph_name) as json_file:
            self.nodes = json.load(json_file)

    def add_node(self, node_name, node_object):
        if node_name not in self.nodes:
            self.nodes[node_name] = {
                'object': node_object,
                'edges': dict()
            }

    def add_edge(self, node_name1, node_name2, weight):
        if node_name1 in self.nodes and node_name2 in self.nodes:
            self.nodes[node_name1]['edges'][node_name2] = weight
            self.nodes[node_name2]['edges'][node_name1] = weight

    def get_recommendations(self, node_name, max_recomendations, min_weight):
        if node_name in self.nodes:
            recomendations = []
            for edge in self.nodes[node_name]['edges']:
                if self.nodes[node_name]['edges'][edge] >= min_weight:
                    recomendations.append((edge, self.nodes[node_name]['edges'][edge]))
            recomendations.sort(key=lambda x: x[1], reverse=True)
            return recomendations[:max_recomendations]
        return []

    # this is an invert djikstra to get the maxs paths
    # https://www.geeksforgeeks.org/printing-paths-dijkstras-shortest-path-algorithm/
    def get_recommendations_invert(self, node_src, max):
        visited = dict()
        for node in self.nodes:
            visited[node] = False
        path = [node_src]
        self.get_recommendations_invert_util(node_src, visited, path, max)
        return path

    def get_object(self, node_name):
        if node_name in self.nodes:
            return self.nodes[node_name]['object']
        return None

    def get_edges(self, node_name):
        if node_name in self.nodes:
            return self.nodes[node_name]['edges']
        return []

    def saveGraph(self, graph_name):
        with open(graph_name, 'w') as outfile:
            json.dump(self.nodes, outfile, indent=2)

    def get_recommendations_invert_util(self, node_src, visited, path, max):
        if len(path) == max:
            print(path)
            return
        visited[node_src] = True
        for edge in self.nodes[node_src]['edges']:
            if not visited[edge]:
                path.append(edge)
                self.get_recommendations_invert_util(edge, visited, path, max)
                path.pop()
        visited[node_src] = False
