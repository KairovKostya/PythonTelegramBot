import requests
import time
import csv
from config import *
import Tester
from Post import *


class Parser:
    """This class parses all posts from vk-page"""
    __token = VK_TOKEN
    __version = 5.95
    __owner_id = -198620269
    wrong_url = []

    def get_all_photos_urls(self):
        with open("my_posts.csv", encoding='utf-8') as r_file:
            all_photos = []
            file_reader = csv.reader(r_file, delimiter=",")
            count = -1
            for row in file_reader:
                count += 1
                if count == 0:
                    continue
                all_photos.append(row[2])
            return all_photos

    def take_all_posts(self):
        offset = 0
        all_posts = []
        count = 100
        while (offset < 1000):
            response = requests.get('https://api.vk.com/method/wall.get',
                                    params={
                                        'access_token': self.__token,
                                        'v': self.__version,
                                        'owner_id': self.__owner_id,
                                        'count': count,
                                        'offset': offset
                                    }
                                    )
            data = response.json()['response']['items']
            all_posts.extend(data)
            offset += 100
            time.sleep(0.1)
        return all_posts

    def file_writer(self, posts):
        with open('my_posts.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(('likes', 'body', 'url', 'views'))

            for post in posts:
                img_url = 'pass'
                try:
                    if post['attachments'][0]['type'] == "photo":
                        max = 0
                        for x in post['attachments'][0]['photo']['sizes']:
                            if x['height'] * x['width'] > max:
                                max = x['height'] * x['width']
                                img_url = x['url']
                    url_tester = Tester.TestVKParser()
                    try:
                        url_tester.test_particular_url(img_url)
                    except:
                        img_url = 'pass'
                except:
                    pass
                writer.writerow((post['likes']['count'], post['text'], img_url, post['views']['count']))

    def get_5_best_posts(self, par):
        with open("my_posts.csv", encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            sortedlist = sorted(file_reader, key=lambda row: row[par], reverse=True)
            count = -1
            ans = []
            for row in sortedlist:
                count += 1
                if count == 0:
                    continue
                if count > 5:
                    break
                ans.append(Post(message=row[1], photo_url=row[2], likes=row[par], views=row[par]))
            return ans

    def get_x_last_posts(self, x):
        with open("my_posts.csv", encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            count = -1
            ans = []
            for row in file_reader:
                count += 1
                if count == 0 or count ==1:
                    continue
                if count > x + 1:
                    break
                ans.append(Post(message=row[1], photo_url=row[2]))
            return ans
