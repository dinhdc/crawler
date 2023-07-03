import requests
from bs4 import BeautifulSoup
import validators
import csv


def handle_one_chapter(url):
    link_req = requests.get(url)
    index = url.split("/")[-2].split("-")[-1]
    link_soup = BeautifulSoup(link_req.content, "html.parser")
    content = link_soup.select("#chapter-c")
    title = link_soup.select(".truyen-title")[0].text
    chapter_title = link_soup.select(".chapter-title")[0].text
    return {
        "content": content[0].text,
        "title": title,
        "chapter": chapter_title,
        "index": index
    }


def get_list_story(url):
    list_response = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    list_url = soup.select("div[class='list list-truyen col-xs-12']")
    children = list_url[0].select("div.row")
    for child in children:
        list_response.append(child.select("a")[0].attrs["href"])
    return list_response


def handle_one_page(url):
    try:
        list_chapter = []
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        chapters = soup.select(".list-chapter")
        list_pages = soup.select(".sr-only")
        next_page_url = None
        for page in list_pages:
            if page.text == "Trang tiếp":
                next_page = page.parent
                next_page_url = next_page.attrs["href"]
        for ul in chapters:
            li_list = ul.findChildren("li")
            for li in li_list:
                a_tag = li.findChildren("a")[0]
                list_chapter.append(a_tag.attrs["href"])
        return list_chapter, next_page_url
    except Exception:
        return [], None


def handle_detail_story(url):
    list_chapter, next_page_url = handle_one_page(url)
    while next_page_url is not None:
        temp, temp_url = handle_one_page(next_page_url)
        list_chapter.extend(temp)
        next_page_url = temp_url
    return list_chapter


def check_page(url):
    urls = url.split("/")
    if "danh-sach" in url or "the-loai" in url:
        return "category"
    elif "chuong" in urls[-2] or "#list-chapter" == urls[-1]:
        return "chapter"
    else:
        return "description"


def get_content_page():
    with open("new_stories.csv", 'r') as csvfile:
        datareader = csv.reader(csvfile)
        header = next(datareader)
        with open('new_list_chapter.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(["url", "crawled"])
        for row in datareader:
            href = row[6]
            type_page = check_page(href)
            if type_page == "description":
                chapters = handle_detail_story(href)
                # list_chapters.extend(chapters)
                with open('new_list_chapter.csv', 'a', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    for chapter in chapters:
                        writer.writerow([chapter, False])
            elif type_page == "category":
                list_story = get_list_story(href)
                for story in list_story:
                    chapters = handle_detail_story(story)
                    with open('new_list_chapter.csv', 'a', encoding='UTF8') as f:
                        writer = csv.writer(f)
                        for chapter in chapters:
                            writer.writerow([chapter, False])
            else:
                # list_chapters.extend(handle_detail_story(href))
                with open('new_list_chapter.csv', 'a', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    # write the header
                    writer.writerow([href, False])


# get_content_page("https://truyenfull.vn/tieu-hoc-tra-om-yeu/")
# print(get_list_story("https://truyenfull.vn/danh-sach/truyen-moi/"))
# res = (handle_detail_story("https://truyenfull.vn/tieu-hoc-tra-om-yeu/"))
# print(handle_one_chapter(res[0]))
get_content_page()
