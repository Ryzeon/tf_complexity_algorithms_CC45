import time

from flask import Flask

from service.videogames_manager import VideoGamesManager
from service.videogames_manager import RecommendationSearch
import networkx as nx
import matplotlib.pyplot as plt

app = Flask(__name__)

videoGamesManager = VideoGamesManager()  # Singleton
# Calcualte ms to load
start = time.time()
videoGamesManager.loadGames()
# Limit games to 2000 games
videoGamesManager.limitGames(2000)
print(len(videoGamesManager.getVideoGames()))
videoGamesManager.loadGraph()
fix_ms = time.time() - start
fix_ms = round(fix_ms, 4)
print(f'Total time to load: {fix_ms} ms')

randomGame = videoGamesManager.getRandomGame()

print(f'Random game: {randomGame}')
print(f'Random game: {videoGamesManager.getVideoGame(randomGame).to_string()}')
recommendationSearch = videoGamesManager.grafo.get_recommendations(randomGame, 10, RecommendationSearch.LOW.value)
for recommendation in recommendationSearch:
    print('------------------')
    print(f'Recommendation: {videoGamesManager.getVideoGame(recommendation[0]).to_string()}')
    print(f'Weight: {recommendation[1]}')
    print('------------------')

# d_graph = nx.Graph()
# d_graph.add_node(videoGamesManager.getVideoGame(randomGame).id)
# for recommendation in recommendationSearch:
#     d_graph.add_node(recommendation[0])
#     d_graph.add_edge(videoGamesManager.getVideoGame(randomGame).id, recommendation[0], weight=recommendation[1])
# pos = nx.spring_layout(d_graph)
# nx.draw(d_graph, pos, with_labels=True, node_size=10, font_color="black", font_size=1)
# etiquetas_aristas = nx.get_edge_attributes(d_graph, "weight")
# nx.draw_networkx_edge_labels(d_graph, pos, edge_labels=etiquetas_aristas)
# plt.show()
#
# print("Done")


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
