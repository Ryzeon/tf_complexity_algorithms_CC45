import time

from flask import Flask

from service.videogames_manager import VideoGamesManager

app = Flask(__name__)

videoGamesManager = VideoGamesManager()  # Singleton
# Calcualte ms to load
start = time.time()
videoGamesManager.loadGames()

for k,v in videoGamesManager.getVideoGames():
    print(v.to_string())
    print()
    print()
    print()

fix_ms = time.time() - start
fix_ms = round(fix_ms, 4)
print(f'Total time to load: {fix_ms} ms')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello sWorld!'


if __name__ == '__main__':
    app.run()
