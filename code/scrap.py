import requests
from bs4 import BeautifulSoup as bs, element
from pprint import pprint
import re
from rich.progress import Progress
import pathlib
from pathlib import Path
import json

SCRAP_SITE = "https://books.toscrape.com/"
response = requests.get(SCRAP_SITE)
soup = bs(response.text, "lxml")

class Scrap():
    def __init__(self) -> None:
        self.categories()

    def _categories_title(self) -> list[str]:               # Return a list the title of all categories of book in the site
        # Take a list of all link element ( a ) whose contain the titles
        title_list_container = soup.find("aside", class_="sidebar col-sm-4 col-md-3")
        title_list_container_list = title_list_container.find_all('a')

        # Retrieve all text inside each link ( a ) element and add them to a list
        title_list = []
        for title in title_list_container_list:
            # text = re.sub(r"[\s]*", "", title.text)
            title_list.append(re.sub(r"([a-z])([A-Z])", r"\1 \2", re.sub(r"[\s]*", "", title.text)))
                

                    
        return title_list

    def _categories_link(self) -> list[str]:                # Return a list of all categories link
        # Take a list of all link element ( a ) whose contain the titles
        title_list_container = soup.find("aside", class_="sidebar col-sm-4 col-md-3")
        title_list_container_list = title_list_container.find_all('a')

        # Retrieve all link inside each link ( a ) element and add them to a list
        link_list = []
        for link in title_list_container_list:
            link_list.append(SCRAP_SITE + link.attrs['href'])

        return link_list

    def _fetching_categories_urls(self) -> list[element.Tag]:          # Create a beautifulsoup variable of each category url
        urls = self._categories_link()
        sou_list = []
        SOUP_DIR = Path(__file__).parent / "scrap" / "categories_links_soup"
        SOUP_DIR.mkdir(exist_ok=True)
        SOUP_FILE = SOUP_DIR / "soup.json"

        if not SOUP_FILE.exists():
            with Progress() as progress:
                task = progress.add_task("Fetching the html files...", total=51)

                for i in range(len(urls)):
                    url = self._categories_link()[i]
                    res = requests.get(url)
                    sou = bs(res.text, 'lxml')
                    sou_list.append(sou)
                    progress.update(task, advance=1)

            with open(SOUP_FILE, 'w', encoding='utf-8') as file:
                # file.write(str(sou_list))
                json.dump(str(sou_list), file, indent=4)
        else:
            with open(SOUP_FILE, 'r', encoding='utf-8') as file:
                # sou_list = file.read()
                sou_list = json.load(file)

        return sou_list

    def imgs_urls(self) -> dict:                            # Fetch all image url along with their categories
        sou_list: list[element.Tag] = self._fetching_categories_urls()
        main_dict = {}

        for i, sou in enumerate(sou_list):
            img_container = sou.find('ol', class_="row")
            imgs_container = img_container.find_all('li')
            imgs_list = []
            for item in imgs_container:
                img = item.find('img').attrs['src']
                imgs_list.append(fr"{SCRAP_SITE + img}")
            main_dict[self._categories_title()[i]] = imgs_list

        return main_dict

    def save_img(self) -> None:                             # save images in a file
            
            IMG_DIR = Path(__file__).parent / "scrap" / "img_save_dir"
            IMG_DIR.mkdir(exist_ok=True)
            main_dict = self.imgs_urls()

            with Progress() as progress:
                task = progress.add_task("saving images...", total=len(self._categories_title()))

                for j, i in zip(range(len(main_dict)), range(len(self._categories_title()))):
                
                    IMG_DIR = Path(__file__).parent / "scrap" / "img_save_dir"
                    IMG_DIR: pathlib.WindowsPath = IMG_DIR / f"{ str(i).zfill(3) }_{ self._categories_title()[i] }"
                    IMG_DIR.mkdir(exist_ok=True)

                    for k in range(len(main_dict[self._categories_title()[j]])):
                        file_path = IMG_DIR / f"{ str(k).zfill(3) }.jpg"
                        with open(file_path, 'wb') as file:
                            url = main_dict[self._categories_title()[j]][k]
                            res = requests.get(url)
                            file.write(res.content)
                    progress.update(task, advance=1)

    def des_title(self):
        soup_list: list[element.Tag] = self._fetching_categories_urls()
        imgs_title_dict = {}
        BOOK_TITLE_DIR = Path(__file__).parent / "scrap" / "title_save_dir"
        BOOK_TITLE_DIR.mkdir(exist_ok=True)

        with Progress() as progress:
            task = progress.add_task("Saving soup elements...", total=len(self._categories_title()))

            for sou, i in zip(soup_list, range(len(self._categories_title()))):
                img_container = sou.find('ol', class_="row")
                imgs_container = img_container.find_all('li')
                imgs_title_list = []
                for item in imgs_container:
                    img_title = item.find('h3').find('a')['title']
                    imgs_title_list.append(img_title)
                imgs_title_dict[self._categories_title()[i]] = imgs_title_list
                progress.update(task, advance=1)

            with open(BOOK_TITLE_DIR / "book_titles.json", 'w') as file:
                json.dump(imgs_title_dict, file, indent=5)

        return imgs_title_dict

    def categories(self) -> dict:                           # Return a dictionary of all categories and their link
        title = self._categories_title()
        link = self._categories_link()

        categories = {}
        for i in range(len(title)):
            categories[title[i]] = link[i]

        return categories

    def book_price(self) -> list:
        soup_list: list[element.Tag] = self._fetching_categories_urls()
        titles = self.des_title()
        price_list = {}
        BOOK_PRICE_DIR = Path(__file__).parent / "scrap" / "price_save_dir"
        BOOK_PRICE_DIR.mkdir(exist_ok=True)

        for soup, i in zip(soup_list, range(len(self._categories_title()))):
            book_price_container = soup.find('ol', class_="row")
            book_prices_container = book_price_container.find_all('li')
            book_price_list = {}
            for item, j in zip(book_prices_container, range(len(titles[self._categories_title()[i]]))):
                book_price = item.find('div', class_='product_price').find('p', class_='price_color').get_text()
                book_price_list[titles[self._categories_title()[i]][j]] = re.sub(r"[Â]*", "", book_price)
            price_list[self._categories_title()[i]] = book_price_list
            
        with open(BOOK_PRICE_DIR / "book_price.json", 'w', encoding='utf-8') as file:
            json.dump(price_list, file,ensure_ascii=True , indent=5)

        return price_list

    def book_info_urls(self):
        soup: list[element.Tag] = self._fetching_categories_urls()
        
        return soup

    def book_description(self):
        pass


if __name__ == "__main__":
    scrap = Scrap()
    pprint(scrap._fetching_categories_urls())