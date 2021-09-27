import config
import requests
from bs4 import BeautifulSoup
import random


class QuoteParser:
    """This class parses quotes for boy posts"""
    __url = "https://citatnica.ru/citaty/krutye-tsitaty-dlya-patsanov-400-tsitat"
    __headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
    }
    __req = requests.get(__url  , headers=__headers)
    __src = __req.text

    def set_quotes(self):
        with open("index.html", "w") as file:
            self.__req = requests.get(self.__url, headers=self.__headers)
            self.__src = self.__req.text
            file.write(self.__src)

    def get_quotes(self):
        with open("index.html") as file:
            self.__src = file.read()

        soup = BeautifulSoup(self.__src, "lxml")
        all_quote_hrefs = soup.find_all(class_="su-note-inner su-u-clearfix su-u-trim")
        quotes = []
        for item in all_quote_hrefs:
            quotes.append(item.text)
        return quotes

    def get_random_quote(self):
        rand = random.randint(2, 399)
        return self.get_quotes()[rand]



