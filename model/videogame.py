class VideoGame:
    def __init__(self, name, platform, year_of_release, genre, publisher, user_count, developer, rating,
                 platforms=None, genres=None, users_platforms=None
                 ):
        if users_platforms is None:
            users_platforms = dict()
            users_platforms[platform] = user_count
        if genres is None:
            genres = list()
            self.add_genre(genre)
        if platforms is None:
            platforms = list()
            self.add_platform(platform)
        self.id = name
        self.name = name
        self.platforms = platforms
        self.genres = genres
        self.year_of_release = year_of_release
        self.publisher = publisher
        self.developer = developer
        self.users_platforms = users_platforms
        self.rating = rating

    def update(self, platform, genre, user_count):
        self.add_platform(platform)
        self.add_genre(genre)
        self.users_platforms[platform] = user_count

    def add_platform(self, platform):
        if platform not in self.platforms:
            self.platforms.append(platform)

    def add_genre(self, genre):
        if genre not in self.genres:
            self.genres.append(genre)

    def to_string(self):
        return f'{self.name} {self.platforms} {self.year_of_release} {self.genres} {self.publisher} {self.users_platforms} {self.developer} {self.rating}'

    def getDic(self):
        return {
            'id': self.id,
            'name': self.name,
            'platforms': self.platforms,
            'genres': self.genres,
            'year_of_release': self.year_of_release,
            'publisher': self.publisher,
            'users_platforms': self.users_platforms,
            'developer': self.developer,
            'rating': self.rating
        }
