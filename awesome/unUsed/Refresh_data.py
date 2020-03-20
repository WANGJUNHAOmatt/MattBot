from datetime import datetime
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
import requests
from bs4 import BeautifulSoup


def now_ss():
    #   目标网站
    url = "https://on.ssfree.ru/"
    selector = "#main > div.content > div:nth-child(5) > code:nth-child(4)"

    response = requests.get(url=url)
    response.encoding = 'utf-8'
    content = response.text

    soup = BeautifulSoup(content, "lxml")
    configuration = soup.select(selector)
    # print(configuration)
    address = str(configuration).split("地址")[1].split("端口号")[0].strip()
    port = str(configuration).split("端口号")[1].split("密码")[0].strip()
    password = str(configuration).split("密码")[1].split("加密")[0].strip()
    # print(address, port, password)
    return "地址{} 端口{} 密码{}".format(address, port, password)


@nonebot.scheduler.scheduled_job('cron', hour='0, 6, 12, 18', minute='5, 30')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=849871859,
                                 message=f'现在{now.hour}点{now.minute}分啦！\n'+now_ss())
    except CQHttpError:
        pass
