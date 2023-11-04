import csv
import os

from model.videogame import VideoGame


class VideoGamesManager:
    def __init__(self):
        self.videoGames = dict()
        self.plataforms = set()
        self.genres = set()
        self.year_of_releases = set()
        self.publishers = set()

    def exitsInVideoGames(self, id):
        if id in self.videoGames:
            return True
        return False

    def add_videoGame(self, videogame):
        if not self.exitsInVideoGames(videogame.id):
            self.videoGames[videogame.id] = videogame
        else:
            self.updateVideoGame(videogame.id, videogame)

    def getVideoGames(self):
        return self.videoGames.items()

    def getVideoGame(self, id):
        return self.videoGames[id]

    def updateVideoGame(self, id, plataform, genre, user_count):
        self.videoGames[id].update(plataform, genre, user_count)

    def loadGames(self):
        path = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.join(path, '../dataset_original.csv')
        with open(relative_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                video_game = VideoGame(row['Name'], row['Platform'], row['Year_of_Release'], row['Genre'],
                                       row['Publisher'],
                                       row['User_Count'], row['Developer'], row['Rating'])
                if self.exitsInVideoGames(video_game.id):
                    self.updateVideoGame(video_game.id, row['Platform'], row['Genre'], row['User_Count'])
                else:
                    self.add_videoGame(video_game)
                self.plataforms.add(row['Platform'])
                self.genres.add(row['Genre'])
                self.year_of_releases.add(row['Year_of_Release'])
                self.publishers.add(row['Publisher'])