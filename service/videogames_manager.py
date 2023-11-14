import csv
import os
import random
import json
from re import S

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
        self.main_graph = Graph()
        self.genres_graph = Graph()
        self.platforms_graph = Graph()
        self.publishers_graph = Graph()
        self.coincidences_weight = {
            'name': 60,
            'platform': 4,
            'genre': 15,
            'year_of_release': 3,
            'publisher': 10,
            'developer': 5,
            'rating': 3
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

    def getArrayVideoGames(self):
        return list(self.videoGames.values())

    def getVideoGame(self, id):
        return self.videoGames[id]

    def updateVideoGame(self, id, plataform, genre, user_count):
        self.videoGames[id].update(plataform, genre, user_count)

    def getGamesWithMachName(self, name):
        games = []
        for videoGame in self.videoGames.values():
            if name.lower() in videoGame.name.lower():
                games.append(videoGame)
        return games

    # Calculate the weight of the concidences
    def calcularPonderado(self, videoGame, videoGame2):
        ponderado = 0
        for plataform in videoGame.platforms:
            max_platforms = len(videoGame.platforms)
            if plataform in videoGame2.platforms:
                ponderado += self.coincidences_weight['platform'] / max_platforms
        for genre in videoGame.genres:
            if genre in videoGame2.genres:
                ponderado += self.coincidences_weight['genre'] / len(videoGame.genres)
        if videoGame.year_of_release == videoGame2.year_of_release:
            ponderado += self.coincidences_weight['year_of_release']
        if videoGame.publisher == videoGame2.publisher:
            ponderado += self.coincidences_weight['publisher']
        if videoGame.developer == videoGame2.developer:
            ponderado += self.coincidences_weight['developer']
        if videoGame.rating == videoGame2.rating:
            ponderado += self.coincidences_weight['rating']
        for videoGamest in videoGame.name.lower().split(" "):
            if videoGamest in videoGame2.name.lower():
                ponderado += self.coincidences_weight['name'] / len(videoGame.name.split(" "))
        return ponderado

    def loadGames(self):
        path = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.join(path, '../dataset_original.csv')
        with open(relative_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                video_game = VideoGame(row['Name'].replace("/", "-"), row['Platform'], row['Year_of_Release'],
                                       row['Genre'],
                                       row['Publisher'],
                                       row['User_Count'], row['Developer'], row['Rating'],
                                       platforms=None, genres=None, users_platforms=None
                                       )
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
            self.main_graph.add_node(videoGame.id, videoGame.id)

    def addConnections(self):
        for videoGame in self.videoGames.values():
            for videoGame2 in self.videoGames.values():
                if videoGame.id != videoGame2.id:
                    ponderado = self.calcularPonderado(videoGame, videoGame2)
                    if ponderado > RecommendationSearch.MEDIUM.value:
                        self.main_graph.add_edge(videoGame.id, videoGame2.id, ponderado)

    def saveToJson(self):
        jsonArray = []
        for videoGame in self.videoGames.values():
            jsonArray.append(videoGame.getDic())
        with open('original_data.json', 'w') as outfile:
            json.dump(jsonArray, outfile, indent=2)

    def loadFromJson(self):
        with open('original_data.json') as json_file:
            data = json.load(json_file)
            for videoGame in data:
                self.addJsonGame(videoGame)
        self.year_of_releases = list(self.year_of_releases)
        self.publishers = list(self.publishers)
        self.genres = list(self.genres)
        self.plataforms = list(self.plataforms)
        self.year_of_releases.sort()
        self.publishers.sort()
        self.genres.sort()
        self.plataforms.sort()
        
    def get_recommendations_with_filters(self, node_src, gender_filter, platform_filter, year_filter, max_recommendations):
        if node_src not in self.main_graph.nodes:
            return []
        # if gender filter is empty allow all
        # if platform filter is empty allow all
        # if year filter is empty allow all
        

    def addJsonGame(self, videoGameJson):
        self.videoGames[videoGameJson['id']] = VideoGame(videoGameJson['id'], None, videoGameJson['year_of_release'],
                                                         None, videoGameJson['publisher'], None,
                                                         videoGameJson['developer'], videoGameJson['rating'],
                                                         platforms=videoGameJson['platforms'],
                                                         genres=videoGameJson['genres'],
                                                         users_platforms=videoGameJson['users_platforms']
                                                         )
        for platform in videoGameJson['platforms']:
            if len(platform) > 0:
                self.plataforms.add(platform)
        for genre in videoGameJson['genres']:
            if len(genre) > 0:
                self.genres.add(genre)
        for platform in videoGameJson['platforms']:
            if len(platform) > 0:
                self.plataforms.add(platform)
        self.publishers.add(videoGameJson['publisher'])
        self.year_of_releases.add(videoGameJson['year_of_release'])

    def loadGraph(self):
        self.main_graph.loadFromJson('main_graph.json')
        self.genres_graph.loadFromJson('genres_graph.json')
        self.platforms_graph.loadFromJson('platforms_graph.json')
        self.publishers_graph.loadFromJson('publishers_graph.json')
        # self.addGamesToGraph()
        # self.addConnections()
        # self.main_graph.saveGraph('main_graph.json')

    def loadAndSaveAuxGraphs(self):
        for publisher in self.publishers:
            self.publishers_graph.add_node(publisher, publisher)

        for genre in self.genres:
            self.genres_graph.add_node(genre, genre)

        for platform in self.plataforms:
            self.platforms_graph.add_node(platform, platform)

        for videoGame in self.videoGames.values():
            self.publishers_graph.add_edge(videoGame.publisher, videoGame.id, 1)
            for platform in videoGame.platforms:
                self.platforms_graph.add_edge(platform, videoGame.id, 1)
            for genre in videoGame.genres:
                self.genres_graph.add_edge(genre, videoGame.id, 1)

        self.genres_graph.saveGraph('genres_graph.json')
        self.platforms_graph.saveGraph('platforms_graph.json')
        self.publishers_graph.saveGraph('publishers_graph.json')

    def deleteRandomGame(self):
        randomGame = random.choice(list(self.videoGames.keys()))
        del self.videoGames[randomGame]

    def limitGames(self, maxNumberOFGames):
        # Delete random games until the number of games is equal to maxNumberOFGames
        while len(self.videoGames) > maxNumberOFGames:
            self.deleteRandomGame()

    def getRandomGame(self):
        return random.choice(list(self.videoGames.keys()))
