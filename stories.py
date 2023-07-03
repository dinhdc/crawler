import csv

import requests
from bs4 import BeautifulSoup

stories = {}


def check_story(url):
    if url in stories:
        return True
    else:
        stories[url] = True
        return False


def get_story(chapter_url):
    try:
        urls = chapter_url.split("/")
        urls = urls[:-2]
        story_url = "/".join(urls)
        if check_story(story_url):
            return None
        response = requests.get(story_url)
        soup = BeautifulSoup(response.content, "html.parser")
        image = soup.select("div.book img[itemprop='image']")[0].attrs["src"]
        author = soup.select("a[itemprop='author']")[0].text
        genres_select = soup.select("div.info a[itemprop='genre']")
        desc = soup.select("div.desc-text[itemprop='description']")[0]
        title = soup.select("h3.title[itemprop='name']")[0].text
        genres = []
        for gen in genres_select:
            genres.append(gen.text)
        return {
            "image": image,
            "author": author,
            "title": title,
            "description": desc,
            "description_text": desc.text,
            "category": genres[0],
            "url": story_url,
            "slug": story_url.split("/")[-1]
        }
    except Exception:
        urls = chapter_url.split("/")
        print(urls)
        return None


def insert_story():
    response = []
    headers = ["image", "author", "title", "description", "description_text", "category", "url", "slug"]
    with open("data.csv", 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            chapter = row[0]
            story = get_story(chapter)
            if story:
                response.append(
                    [story["image"], story["author"], story["title"], story["description"], story["description_text"],
                     story["category"], story["url"], story["slug"]])
    with open("new_stories.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(response)


# https://truyenfull.vn/hop-dao-thich-lo-chuyen-bao-dong
insert_story()
