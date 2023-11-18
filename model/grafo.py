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
        if node_name1 in self.nodes:
            self.nodes[node_name1]['edges'][node_name2] = weight
        if node_name2 in self.nodes:
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

    def get_recommendations_invert(self, node_src, max_recommendations):
        if node_src not in self.nodes:
            print("nada")
            return []

        visited = set()
        queue = [(0, node_src)]  # Initialize the priority queue with node_src
        recommendations = []

        while queue and len(recommendations) < max_recommendations:
            _, current_node = queue.pop(0)

            if current_node in visited:
                continue

            visited.add(current_node)

            for neighbor, weight in self.get_edges(current_node).items():
                if neighbor not in visited:
                    queue.append((weight, neighbor))

            sorted_neighbors = sorted(queue, key=lambda x: x[0], reverse=True)
            for neighbor in sorted_neighbors:
                recommendations.append((neighbor[1], neighbor[0]))
        return recommendations[:max_recommendations]

    def get_object(self, node_name):
        if node_name in self.nodes:
            return self.nodes[node_name]['object']
        return None

    def get_edges(self, node_name):
        if node_name in self.nodes:
            return self.nodes[node_name]['edges']
        return {}

    def saveGraph(self, graph_name):
        with open(graph_name, 'w') as outfile:
            json.dump(self.nodes, outfile, indent=2)
