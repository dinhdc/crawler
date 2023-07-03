import requests
from bs4 import BeautifulSoup
import validators

response = requests.get("https://truyenfull.vn")
soup = BeautifulSoup(response.content, "html.parser")
titles = soup.findAll("a")
not_in_titles = [
    "https://truyenfull.vn/",
    "javascript:void(0)",
    "#wrap",
    "http://creativecommons.org/licenses/by/4.0/",
    "https://truyenfull.vn/contact/",
    "https://truyenfull.vn/tos/",
    "https://truyentrz.com/",
    "https://nettruyenfull.com/"
]

for title in titles:
    href = title.attrs["href"].strip()
    if validators.url(href) and href not in not_in_titles:
        print(href)
