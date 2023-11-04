import time

from flask import Flask

from service.videogames_manager import VideoGamesManager
from service.videogames_manager import RecommendationSearch

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
    print(f'Recommendation: {videoGamesManager.getVideoGame(recommendation[0]).to_string()}')
    print(f'Weight: {recommendation[1]}')
    print('------------------')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
