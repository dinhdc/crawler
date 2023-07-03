import requests
from bs4 import BeautifulSoup

response = requests.get("https://truyenfull.vn/thap-nien-80-nhat-ky-nghich-tap-cua-nu-phu-ac-doc/chuong-30/")
soup = BeautifulSoup(response.content, "html.parser")
titles = soup.select("div#chapter-c p")
for title in titles:
    print(title.text)
