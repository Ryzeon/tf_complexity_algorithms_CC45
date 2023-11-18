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
import networkx as nx
import matplotlib

# Configura Matplotlib para usar el backend 'Agg'
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

load_dotenv()

app = Flask(__name__)


def load_data_and_graph():
    videoGamesManager = VideoGamesManager()  # Singleton
    start = time.time()
    videoGamesManager.loadFromJson()
    # videoGamesManager.saveToJson()
    # Limit games to 2000 games
    # videoGamesManager.loadGames()
    # videoGamesManager.limitGames(5000)
    # videoGamesManager.saveToJson()
    fix_ms = time.time() - start
    fix_ms = round(fix_ms, 4)
    print(f"Total time to load: {fix_ms} ms")
    print(len(videoGamesManager.getVideoGames()))
    print("Loading graph...")
    start = time.time()
    videoGamesManager.loadGraph()
    # videoGamesManager.loadAndSaveAuxGraphs()
    fix_ms = time.time() - start
    fix_ms = round(fix_ms, 4)
    print("Total time to load graphs: " + str(fix_ms) + " ms")
    print(f"Loaded main graph with {len(videoGamesManager.main_graph.nodes)} nodes")
    print(f"Loaded genres graph with {len(videoGamesManager.genres_graph.nodes)} nodes")
    print(
        f"Loaded platforms graph with {len(videoGamesManager.platforms_graph.nodes)} nodes"
    )
    print(
        f"Loaded publishers graph with {len(videoGamesManager.publishers_graph.nodes)} nodes"
    )
    print(
        f"Loaded year of releases graph with {len(videoGamesManager.year_of_releases_graph.nodes)} nodes"
    )
    app.videoGamesManager = videoGamesManager


with app.app_context():
    load_data_and_graph()

# videoGamesManager.grafo.saveGraph("main_graph.json")

# randomGame = videoGamesManager.getGamesWithMachName("pokemon")
# randomGame = random.choice(randomGame).id
#
# print(f'Random game: {randomGame}')
# print(f'Random game: {videoGamesManager.getVideoGame(randomGame).to_string()}')
#
# recommendationSearch = videoGamesManager.main_graph.get_recommendations_invert(
#     randomGame, 10)
#
# for recommendation in recommendationSearch:
#     print("-" * 50)
#     print(f'Conection: {recommendation[0]} - Weight: {recommendation[1]}')
#     print(f'Game: {videoGamesManager.getVideoGame(recommendation[0]).to_string()}')
#     print("-" * 50)


def generate_and_save_graph(game, recomendations):
    plt.clf()
    G = nx.Graph()
    for recommendation in recomendations:
        G.add_edge(
            app.videoGamesManager.getVideoGame(game).id,
            recommendation[0],
            weight=round(int(recommendation[1]), 2),
        )

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 40]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 40]

    pos = nx.spring_layout(
        G, seed=7
    )  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=1000)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(
        G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
    )

    # node labels
    nx.draw_networkx_labels(
        G, pos, font_size=10, font_family="sans-serif", font_color="blue"
    )
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.05)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("static/img/graph.png")
    plt.close()


@app.route("/")
def index():
    page = request.args.get("page", type=int, default=1)
    per_page = 10  # Cantidad de juegos por página
    offset = (page - 1) * per_page
    games = get_games(offset, per_page)

    pagination = Pagination(
        page=page,
        total=len(app.videoGamesManager.videoGames),
        per_page=per_page,
        record_name="games",
    )
    return render_template(
        "index.html",
        video_games=games,
        platforms=app.videoGamesManager.plataforms,
        pagination=pagination,
        genres=app.videoGamesManager.genres,
        years=app.videoGamesManager.year_of_releases,
    )


@app.route("/developers")
def developers():
    return render_template("developers.html")


@app.route("/search-game")
def searchGame():
    game_to_search = request.args.get("search", type=str, default="")
    filter_gender_query = request.args.get("genero", type=str, default="").split(",")
    if "" in filter_gender_query:
        filter_gender_query.remove("")
    filter_platform_query = request.args.get("plataforma", type=str, default="").split(
        ","
    )
    if "" in filter_platform_query: 
        filter_platform_query.remove("")
    filter_year_query = request.args.get("year_of_release", type=str, default="").split(
        ","
    )
    if "" in filter_year_query:
        filter_year_query.remove("")
    amount = request.args.get("amount", type=int, default=10)
    print(filter_year_query)
    print(filter_platform_query)
    print(filter_gender_query)
    game = app.videoGamesManager.getGamesWithMachName(game_to_search)
    if len(game_to_search) > 0:
        if len(game) > 0:
            game = random.choice(game).id
            print("Se encontro el juego")
        else:
            game = app.videoGamesManager.getRandomVideoGame().id
            print("No se encontro el juego")
    else:
        game = app.videoGamesManager.getRandomVideoGame().id
        print("No se encontro el juego")

    print(game)
    related_games = app.videoGamesManager.get_recommendations_with_filters(
        game, filter_gender_query, filter_platform_query, filter_year_query, amount
    )
    # map game and related games in a map int, game
    games = {"➤": app.videoGamesManager.getVideoGame(game)}
    for i in range(len(related_games)):
        games[str(i + 1)] = app.videoGamesManager.getVideoGame(related_games[i][0])

    # threading.Thread(
    #     target=generate_and_save_graph_in_thread, args=(game, related_games)
    # ).start()
    generate_and_save_graph(game, related_games)

    return render_template(
        "search_game.html",
        platforms=app.videoGamesManager.plataforms,
        genres=app.videoGamesManager.genres,
        years=app.videoGamesManager.year_of_releases,
        games=games,
        graph="graph.png",
    )


def get_games(offset=0, per_page=10):
    return app.videoGamesManager.getArrayVideoGames()[offset : offset + per_page]


@app.route("/game/<game_name>")
def game_details(game_name):
    if app.videoGamesManager.exitsInVideoGames(game_name):
        game = app.videoGamesManager.getVideoGame(game_name)
        # image_response = requests.get("https://picsum.photos/400/300")
        game_video = random.choice(get_video_info(game_name + " gameplay", 10))
        print(game_video.embed_url)
        print(game_video.title)
        game_image = random.choice(get_images_from_google_image(game_name, 10))
        return render_template(
            "game_details.html",
            game=game,
            game_image=game_image,
            game_video=game_video.embed_url,
            game_title=game_video.title,
            related_games=app.videoGamesManager.main_graph.get_recommendations_invert(
                game_name, 10
            ),
        )
    else:
        return "Juego no encontrado"


if __name__ == "__main__":
    app.run(debug=True)
