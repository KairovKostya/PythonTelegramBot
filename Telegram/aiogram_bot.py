import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import User
from quotes_parsing import *
import random
from vk_parsing import *

import time
from sql import *
from User import *


class MyBot:
    """This class controls all messages and subscriptions"""
    my_vk_parser = Parser()
    my_quote_parser = QuoteParser()
    my_bot = Bot(token=config.API_TOKEN)
    dp = Dispatcher(my_bot)
    posts = my_vk_parser.take_all_posts()
    amount_of_posts = 0
    my_vk_parser.file_writer(posts)
    my_sql = SQL('subscribers.db')

    @staticmethod
    async def send_message(id, message):
        try:
            await MyBot.my_bot.send_message(id, message)
        except:
            pass

    @staticmethod
    async def send_photo(chat_id, photo, caption=""):
        try:
            await MyBot.my_bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
        except:
            pass

    @staticmethod
    def update_data():
        now = int(time.time())
        all_posts = MyBot.my_vk_parser.take_all_posts()
        MyBot.my_vk_parser.file_writer(all_posts)
        MyBot.my_quote_parser.set_quotes()
        MyBot.time_of_last_updating = now

    @staticmethod
    @dp.message_handler(commands=['start'])
    async def welcome(message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = KeyboardButton("Пацанский пост")
        item2 = KeyboardButton("Топ 5 постов по кол-ву лайков")
        item3 = KeyboardButton("Топ 5 постов по кол-ву просмотров")

        markup.add(item1, item2, item3)
        try:
            await MyBot.my_bot.send_message(message.chat.id,
                                                "Добро пожаловать, {0.first_name}!".format(
                                                    message.from_user, await MyBot.my_bot.get_me()),
                            parse_mode='html', reply_markup=markup)
        except:
            pass

    @staticmethod
    @dp.message_handler(commands=['help'])
    async def help(message):
        await MyBot.send_message(message.chat.id, config.long_message1 +
                                 str(MyBot.my_sql.get_len()) + config.long_message2)

    @staticmethod
    @dp.message_handler(commands=['subscribe'])
    async def subscribe(message):
        if not MyBot.my_sql.subscriber_exists(message.from_user.id):
            current_user = User(str(message.from_user.id), str(message.from_user.first_name),
                                str(message.from_user.last_name))
            if current_user.last_name == 'None':
                current_user.last_name = ""
            MyBot.my_sql.add_users(current_user)
            await MyBot.send_message(message.chat.id, "Вы успешно подписаны")
        else:
            await MyBot.send_message(message.chat.id, "Вы и так подписаны")

    @staticmethod
    @dp.message_handler(commands=['unsubscribe'])
    async def unsubscribe(message):
        if not MyBot.my_sql.subscriber_exists(str(message.chat.id)):
            await MyBot.send_message(message.chat.id, "Вы и не были подписаны")
        else:
            MyBot.my_sql.remove_subscription(str(message.chat.id))
            await MyBot.send_message(message.chat.id, "Вы успешно отписаны")


    @staticmethod
    @dp.message_handler(content_types=['text'])
    async def boy_post(message):
        if message.text == "Пацанский пост":
            urls = MyBot.my_vk_parser.get_all_photos_urls()
            rand_pic = random.randint(1, len(urls) - 2)
            await MyBot.send_photo(chat_id=message.chat.id, photo=urls[rand_pic],
                                          caption=MyBot.my_quote_parser.get_random_quote())
        else:
            await MyBot.most_liked(message)

    @staticmethod
    @dp.message_handler(content_types=['text'])
    async def most_liked(message):
        if message.text == "Топ 5 постов по кол-ву лайков":
            a = MyBot.my_vk_parser.get_5_best_posts(0)
            for i in range(5):
                await MyBot.send_message(message.chat.id,
                                                "Место " + str(i + 1) + ", количество лайков: " + str(a[i].likes))
                if a[i].photo_url != 'pass':
                    await MyBot.send_photo(chat_id=message.chat.id, photo=a[i].photo_url,
                                                  caption=a[i].message)
                else:
                    await MyBot.send_message(message.chat.id, a[i].message)

        else:
            await MyBot.most_viewed(message)

    @staticmethod
    @dp.message_handler(content_types=['text'])
    async def most_viewed(message):
        if message.text == "Топ 5 постов по кол-ву просмотров":
            a = MyBot.my_vk_parser.get_5_best_posts(3)
            for i in range(5):
                await MyBot.send_message(message.chat.id,
                                                "Место " + str(i + 1) + ", количество просмотров: " + str(a[i].views))
                if a[i].photo_url != 'pass':
                    await MyBot.send_photo(chat_id=message.chat.id, photo=a[i].photo_url,
                                                      caption=a[i].message)
                else:
                    await MyBot.send_message(message.chat.id, a[i].message)
        else:
            await MyBot.send_message(message.chat.id, "Костя не знает такой команды")

    @staticmethod
    async def darling(wait_for):
        """darling chooses one of subscribers and sends him a message every 'wait_for' seconds"""
        while True:
            length = MyBot.my_sql.get_len()
            if length == 0:
                await asyncio.sleep(wait_for)
                continue
            x = random.randint(0, length-1)
            count = 0
            users = MyBot.my_sql.get_subscriptions()
            name = ""
            last_name = ""
            for s in users:
                if count == x:
                    name = str(s[1])
                    last_name = str(s[2])
                count += 1
            count = 0
            users = MyBot.my_sql.get_subscriptions()
            for s in users:
                if count == x:
                    await MyBot.send_message(s[0], "Ты любимчик Кости Мясникова на этот день, "
                                                    + str(s[1]) + " " + last_name +"!")
                    await MyBot.send_photo(chat_id=s[0],
                                                photo='https://i.ytimg.com/vi/JOd2FzJXW78/maxresdefault.jpg',
                                                caption="Darling! Say Ahh.")

                else:
                    await MyBot.send_message(s[0], name + " " + last_name +
                                                    " сегодня любимчик Кости! Поздравим его(её) с этим")
                count += 1
            await asyncio.sleep(wait_for)


    @staticmethod
    async def update_data(wait_for):
        while True:
            all_posts = MyBot.my_vk_parser.take_all_posts()
            MyBot.my_vk_parser.file_writer(all_posts)
            MyBot.my_quote_parser.set_quotes()
            if MyBot.amount_of_posts == 0:
                MyBot.amount_of_posts = len(all_posts)
            if MyBot.amount_of_posts < len(all_posts):
                users = MyBot.my_sql.get_subscriptions()
                x = len(all_posts) - MyBot.amount_of_posts
                a = MyBot.my_vk_parser.get_x_last_posts(x)
                for s in users:
                    for i in range(x):
                        if a[i].photo_url != 'pass':
                            await MyBot.send_message(s[0], "В нашем сообществе вышел новый пост! Быстрее беги туда, чтобы увидеть полную версию поста!!!\nPreview:")
                            await MyBot.send_photo(chat_id=s[0], photo=a[i].photo_url, caption=a[i].message)
                        else:
                            await MyBot.send_message(s[0], a[i].message +
                                                        "\n*Здесь должна быть картинка, но её съел Костя*")
                MyBot.amount_of_posts = len(all_posts)
            await asyncio.sleep(wait_for)