import random

import requests
from bs4 import BeautifulSoup
import os


class Video:
    def __init__(self, title, url, embed_url):
        self.title = title
        self.url = url
        self.embed_url = embed_url


def get_video_info(query, limit=10):
    API_KEY = getRandomAPIKey()
    url = f"https://www.googleapis.com/youtube/v3/search"
    data = {
        "key": API_KEY,
        "part": "id,snippet",
        "q": query,
        "max_results": limit
    }
    r = requests.get(url, params=data)
    if r.status_code == 403:
        print("API KEY EXPIRED", API_KEY)
        return get_video_info(query, limit)
    j = r.json()
    items = j["items"]
    videos = []
    for item in items:
        if item["id"]["kind"] == "youtube#video":
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            embed = f"https://www.youtube.com/embed/{video_id}"
            video = Video(title, url, embed)
            videos.append(video)
    return videos


def getRandomAPIKey():
    random_num = random.randint(1, 5)
    return os.getenv(f"GOOGLE_API_{random_num}")


def get_random_video_info(query):
    return random.choice(get_video_info(query, 10))


def get_images_from_google_image(query, limit=10):
    url = "https://www.google.com/search?q=" + query + "&tbm=isch"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return extract_image_links(soup)[:limit]


def extract_image_links(soup):
    image_links = []
    for img in soup.find_all("img"):
        if img.get("src"):
            if img.get("src").startswith("http"):
                image_links.append(img["src"])
    return image_links
