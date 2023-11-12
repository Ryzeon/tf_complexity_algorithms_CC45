import random
import time

# import requests
from flask import Flask, render_template, request
from flask_paginate import Pagination

from service.videogames_manager import VideoGamesManager
from service.videogames_manager import RecommendationSearch
from utils.utils import get_video_info
from utils.utils import get_images_from_google_image
from dotenv import load_dotenv

load_dotenv()

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


# recommendationSearch = videoGamesManager.grafo.get_recommendations(
#     randomGame, 10, RecommendationSearch.LOW.value)
# for recommendation in recommendationSearch:
#     print('------------------')
#     print(
#         f'Recommendation: {videoGamesManager.getVideoGame(recommendation[0]).to_string()}')
#     print(f'Weight: {recommendation[1]}')
#     print('------------------')

x = get_video_info(randomGame, 10)
#
# y = get_images_from_google_image(randomGame, 10)
# print(x)
# print(y)


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
def index():
    page = request.args.get('page', type=int, default=1)
    per_page = 10  # Cantidad de juegos por página
    offset = (page - 1) * per_page
    games = get_games(offset, per_page)

    pagination = Pagination(page=page, total=len(
        videoGamesManager.videoGames), per_page=per_page, record_name='games')
    return render_template('index.html',
                           video_games=games,
                           platforms=videoGamesManager.plataforms,
                           pagination=pagination,
                           genres=videoGamesManager.genres,
                           years=videoGamesManager.year_of_releases,
                           )


@app.route("/developers")
def developers():
    return render_template("developers.html")


@app.route("/search-game")
def searchGame():
    return render_template("search_game.html")


def get_games(offset=0, per_page=10):
    return videoGamesManager.getArrayVideoGames()[offset: offset + per_page]


@app.route('/game/<game_name>')
def game_details(game_name):
    if videoGamesManager.exitsInVideoGames(game_name):
        game = videoGamesManager.getVideoGame(game_name)
        # image_response = requests.get("https://picsum.photos/400/300")
        game_video = random.choice(get_video_info(game_name, 10))
        print(game_video.embed_url)
        print(game_video.title)
        game_image = random.choice(get_images_from_google_image(game_name, 10))
        return render_template('game_details.html',
                               game=game,
                               game_image=game_image,
                               game_video=game_video.embed_url,
                               game_title=game_video.title,
                               related_games=videoGamesManager.grafo.get_recommendations(game_name, 10,
                                                                                         RecommendationSearch.LOW.value))
    else:
        return "Juego no encontrado"


if __name__ == '__main__':
    app.run(debug=True)
