from collections import deque


class Graph:
    def __init__(self):
        self.nodes = dict()

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
    
    def get_object(self, node_name):
        if node_name in self.nodes:
            return self.nodes[node_name]['object']
        return None

    def get_edges(self, node_name):
        if node_name in self.nodes:
            return self.nodes[node_name]['edges']
        return []
