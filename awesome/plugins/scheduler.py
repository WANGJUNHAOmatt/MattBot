from datetime import datetime
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
from test import Birthdays


# @nonebot.scheduler.scheduled_job('interval', seconds=10)
# 每隔10秒发一次


@nonebot.scheduler.scheduled_job('cron', hour='6, 9, 12, 15, 18, 21')
async def drink_water():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_private_msg(user_id=117854373, message=f'现在{now.hour}点啦！\n该去喝水啦！！')
        await bot.send_private_msg(user_id=813499516, message=f'现在{now.hour}点啦！\n已经提醒妈妈喝水了，你也要喝水哦！')

    except CQHttpError:
        pass

# 发送生日信息
@nonebot.scheduler.scheduled_job('cron', hour='6')
async def send_birthday_news():
    bot = nonebot.get_bot()
    birthday = Birthdays()
    for user_id in birthday.birthday_database:
        print(f"给{user_id}发送了早安+生日消息！")
        await bot.send_private_msg(user_id=user_id, message=f'早上好！\n{birthday.get_recent_birthdays(user_id)}')
        await bot.send_private_msg(user_id=813499516, message=f'已经给{user_id}发送了早安+生日消息！')


# ss基本废了
# @nonebot.scheduler.scheduled_job('cron', hour='0, 6, 12, 18', minute='5')
# async def _():
#     bot = nonebot.get_bot()
#     try:
#         await bot.send_private_msg(user_id=113666201, message=f'密码更新啦！\n' + getSS.now_ss())
#         await bot.send_private_msg(user_id=813499516, message=f'密码更新啦，成功通知老爹！\n' + getSS.now_ss())
#     except CQHttpError:
#         pass
