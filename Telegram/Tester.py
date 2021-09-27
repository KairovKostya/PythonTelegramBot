import unittest
from User import *
from sql import *
import vk_parsing
import os
import requests


class TestUser(unittest.TestCase):
    def test_default(self):
        user = User()
        self.assertEqual(user.id, 0)


class TestVKParser(unittest.TestCase):
    def test_particular_url(self, url):
        works = True
        try:
            if url != 'pass':
                req = requests.get(url)
        except:
            works = False

        self.assertEqual(works, True)

    def test_all_urls(self):
        vk_parser = vk_parsing.Parser()
        posts = vk_parser.take_all_posts()
        vk_parser.file_writer(posts)
        urls = vk_parser.get_all_photos_urls()
        count = 0
        for url in urls:
            try:
                if url != 'pass':
                    req = requests.get(url)
                count += 1
            except:
                pass
        print(len(urls))
        self.assertEqual(len(urls), count)


class TestSQLMethods(unittest.TestCase):
    def test_simple(self):
        sql = SQL('test.db')
        sql.cur.execute('select 1')
        self.assertEqual(sql.cur.fetchone()[0], 1)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
        os.remove(path)

    def test_adding(self):
        sql = SQL('test.db')
        first_user = User(1, "Kostya", "Kairov")
        second_user = User(2, "Kostya", "Myasnikov")
        third_user = User(3, "Timur", "Kharisov")
        self.assertEqual(sql.get_len(), 0)
        sql.add_users(first_user)
        self.assertEqual(sql.get_len(), 1)
        sql.add_users(second_user)
        self.assertEqual(sql.get_len(), 2)
        sql.add_users(third_user)
        self.assertEqual(sql.get_len(), 3)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
        os.remove(path)

    def test_removing(self):
        sql = SQL('test.db')
        first_user = User(1, "Kostya", "Kairov")
        second_user = User(2, "Kostya", "Myasnikov")
        third_user = User(3, "Timur", "Kharisov")
        self.assertEqual(sql.get_len(), 0)
        sql.add_users(first_user)
        self.assertEqual(sql.get_len(), 1)
        sql.add_users(second_user)
        self.assertEqual(sql.get_len(), 2)
        sql.add_users(third_user)
        self.assertEqual(sql.get_len(), 3)
        sql.remove_subscription(3)
        self.assertEqual(sql.get_len(), 2)
        sql.remove_subscription(2)
        self.assertEqual(sql.get_len(), 1)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
        os.remove(path)
