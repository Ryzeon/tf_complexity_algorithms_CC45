import csv
import os
import random

from model.videogame import VideoGame
from model.grafo import Graph
from enum import Enum


class RecommendationSearch(Enum):
    HIGH = 90
    MEDIUM = 40
    LOW = 20


class VideoGamesManager:
    def __init__(self):
        self.videoGames = dict()
        self.plataforms = set()
        self.genres = set()
        self.year_of_releases = set()
        self.publishers = set()
        self.grafo = Graph()
        self.conciendes_weight = {
            'platform': 30,
            'genre': 35,
            'year_of_release': 10,
            'publisher': 10,
            'developer': 5,
            'rating': 10
        }

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

    # Calculate the weight of the concidences
    def calcularPonderado(self, videoGame, videoGame2):
        # el ponderador debe sumar 100
        ponderado = 0
        for plataform in videoGame.platforms:
            max_platforms = len(videoGame.platforms)
            if plataform in videoGame2.platforms:
                ponderado += self.conciendes_weight['platform'] / max_platforms
        for genre in videoGame.genres:
            if genre in videoGame2.genres:
                ponderado += self.conciendes_weight['genre'] / len(videoGame.genres)
        if videoGame.year_of_release == videoGame2.year_of_release:
            ponderado += self.conciendes_weight['year_of_release']
        if videoGame.publisher == videoGame2.publisher:
            ponderado += self.conciendes_weight['publisher']
        if videoGame.developer == videoGame2.developer:
            ponderado += self.conciendes_weight['developer']
        if videoGame.rating == videoGame2.rating:
            ponderado += self.conciendes_weight['rating']
        return ponderado

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

    def addGamesToGraph(self):
        for videoGame in self.videoGames.values():
            self.grafo.add_node(videoGame.id, videoGame)

    def addConnections(self):
        for videoGame in self.videoGames.values():
            for videoGame2 in self.videoGames.values():
                if videoGame.id != videoGame2.id:
                    ponderado = self.calcularPonderado(videoGame, videoGame2)
                    self.grafo.add_edge(videoGame.id, videoGame2.id, ponderado)

    def loadGraph(self):
        self.addGamesToGraph()
        self.addConnections()

    def deleteRandomGame(self):
        randomGame = random.choice(list(self.videoGames.keys()))
        del self.videoGames[randomGame]

    def limitGames(self, maxNumberOFGames):
        # Delete random games until the number of games is equal to maxNumberOFGames
        while len(self.videoGames) > maxNumberOFGames:
            self.deleteRandomGame()

    def getRandomGame(self):
        return random.choice(list(self.videoGames.keys()))
