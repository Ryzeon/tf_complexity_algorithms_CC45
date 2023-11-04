class VideoGame:
    def __init__(self, name, platform, year_of_release, genre, publisher, user_count, developer, rating):
        self.id = name
        self.name = name
        self.platforms = set()
        self.users_platforms = {}
        self.genres = set()
        self.year_of_release = year_of_release
        self.publisher = publisher
        self.developer = developer
        self.rating = rating

        self.add_platform(platform)
        self.add_genre(genre)
        self.users_platforms[platform] = user_count

    def update(self, platform, genre, user_count):
        self.add_platform(platform)
        self.add_genre(genre)
        self.users_platforms[platform] = user_count

    def add_platform(self, platform):
        self.platforms.add(platform)

    def add_genre(self, genre):
        self.genres.add(genre)

    def to_string(self):
        return f'{self.name} {self.platforms} {self.year_of_release} {self.genres} {self.publisher} {self.users_platforms} {self.developer} {self.rating}'