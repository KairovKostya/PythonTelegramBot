from aiogram_bot import *
from Tester import *
from vk_parsing import *

if __name__ == '__main__':
    half_hour = 1800
    one_day = 86400

    unit_tester = TestUser()
    unit_tester.test_default()
    SQL_tester = TestSQLMethods()
    SQL_tester.test_simple()
    SQL_tester.test_adding()
    SQL_tester.test_removing()
    vk_tester = TestVKParser()
    vk_tester.test_all_urls()

    loop = asyncio.get_event_loop()
    loop.create_task(MyBot.update_data(half_hour))
    loop2 = asyncio.get_event_loop()
    loop.create_task(MyBot.darling(one_day))
    executor.start_polling(MyBot.dp, skip_updates=True)
