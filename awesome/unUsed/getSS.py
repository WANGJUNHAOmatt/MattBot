import requests
from bs4 import BeautifulSoup
from nonebot import on_command, CommandSession
from GlobalValue import test_user

__plugin_name__ = '最新地址'
__plugin_usage__ = """
获取最新地址
使用方法：
输入：\"地址\" \"ss\" \"最新地址\"
例如： 地址
""".strip()


def now_ss():
    #   目标网站
    url = "https://so.ssfree.ru/"
    selector = "#main > div.content > div:nth-child(5) > code:nth-child(4)"

    response = requests.get(url=url)
    response.encoding = 'utf-8'
    content = response.text

    soup = BeautifulSoup(content, "lxml")
    configuration = soup.select(selector)
    print(configuration)
    address = str(configuration).split("地址")[1].split("端口号")[0].strip()
    port = str(configuration).split("端口号")[1].split("密码")[0].strip()
    password = str(configuration).split("密码")[1].split("加密")[0].strip()
    print(address, port, password)
    return "地址{} 端口{} 密码{}".format(address, port, password)


@on_command('最新地址', aliases=('地址', 'ss'))
async def ss(session: CommandSession):
    if session.ctx['user_id'] in test_user:
        weather_report = await get_now_ss()
        await session.send(weather_report)
    else:
        pass


async def get_now_ss() -> str:
    return now_ss()
