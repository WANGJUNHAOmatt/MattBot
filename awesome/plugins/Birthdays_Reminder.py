from nonebot import on_command, CommandSession
import nonebot
from test import Birthdays
import datetime


__plugin_name__ = '好友生日提醒'
__plugin_usage__ = """
生日列表可以记录、提醒您朋友的生日。
1.输入'生日'获取接下来14天中您朋友的生日
2.输入'生日列表'获取您朋友的生日列表
3.输入'添加生日'可添加您朋友的生日到生日列表
4.输入'删除生日'可删除生日列表中的生日
""".strip()


# 获取接下来14天的生日
# TODO 使用户可以自定义时长
@on_command('生日', aliases=('Birthday', 'Birthdays', 'birthday'))
async def next_birthdays(session: CommandSession):
    birthdays = Birthdays()
    user_id = session.ctx['user_id']
    await session.send(birthdays.get_recent_birthdays(user_id))


# 获取生日列表
@on_command('生日列表', aliases=('list', 'birthdayList'))
async def birthdays_list(session: CommandSession):
    birthdays = Birthdays()
    user_id = session.ctx['user_id']
    await session.send(birthdays.get_birthday_list(user_id))


def valuable_date(date: str) -> bool:
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        return False
    return True


# 添加生日
@on_command('添加生日', aliases=('addBirthday', 'AddBirthday'))
async def add_birthday(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    user_id = session.ctx['user_id']
    date = session.get('date', prompt='请输入"YYYY-MM-DD"格式的日期，例：2000-11-22')
    if not valuable_date(date):
        session.state.pop('date')
        session.pause('错误的格式，请输入正确的格式!')
    name = session.get('name', prompt='请输入在那天过生日的人的姓名，例：张三')
    birthday = datetime.date.fromisoformat(date)
    check = session.get('check', prompt=f'{birthday.isoformat(), name}，您确认添加吗？（Y/N）')
    if check == 'Y':
        birthdays = Birthdays()
        birthdays.add_birthday(user_id, birthday, name)
        await session.send('已添加该条记录！')
    else:
        await session.send('已取消添加！')
    print("add_birthday", user_id, birthday, name, check)
    await session.send('完成！')


# 删除生日
@on_command('delBirthday', aliases=('删除生日', 'DelBirthday'))
async def del_birthday(session: CommandSession):
    user_id = session.ctx['user_id']
    date = session.get('date', prompt='请输入"YYYY-MM-DD"格式的日期，例：2000-11-22')
    if not valuable_date(date):
        session.state.pop('date')
        session.pause('错误的格式，请输入正确的格式!')
    name = session.get('name', prompt='请输入在那天过生日的人的姓名，例：张三')
    birthday = datetime.date.fromisoformat(date)
    check = session.get('check', prompt=f'{birthday.isoformat(), name}，您确认吗？（Y/N）')
    if check == 'Y':
        birthdays = Birthdays()
        await session.send(birthdays.del_birthday(user_id, birthday, name))
    else:
        await session.send('已取消删除！')
    print("del_birthday", user_id, birthday, name, check)
    await session.send('完成！')


@on_command('database', aliases=('数据库', '用户信息'))
async def get_database(session: CommandSession):
    birthdays = Birthdays()
    user_id = session.ctx['user_id']
    if user_id == 813499516:
        await session.send(birthdays.print_database())


@on_command('send_notice', aliases=('发送消息', '发送通知'))
async def send_notice(session: CommandSession):
    birthdays = Birthdays()
    if session.ctx['user_id'] != 813499516:
        return
    msg = session.get('msg', prompt='请输入想要广播的信息')
    check = session.get('check', prompt=f'"{str(msg)}"，您确认吗？（Y/N）')
    bot = nonebot.get_bot()
    if check == 'Y':
        for user in list(birthdays.birthday_database.keys()):
            await bot.send_private_msg(user_id=user, message=msg)
            await bot.send_private_msg(user_id=813499516, message=f'已经给{user}发送了通知！')
        await session.send("成功发送")
    else:
        await session.send("已取消发送")
