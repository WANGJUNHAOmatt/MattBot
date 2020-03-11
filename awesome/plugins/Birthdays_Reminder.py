from nonebot import on_command, CommandSession
from GlobalValue import normal_user
from test import Birthdays
import datetime


__plugin_name__ = '生日列表'
__plugin_usage__ = """
开启生日提醒，提醒您未来两周您朋友的生日。
""".strip()


# 获取接下来14天的生日
# TODO 使用户可以自定义时长
@on_command('生日', aliases=('Birthday', 'Birthdays', 'birthday'))
async def next_birthdays(session: CommandSession):
    birthdays = Birthdays()
    user_id = session.ctx['user_id']
    await session.send(birthdays.get_next_birthdays(user_id))


# 获取生日列表
@on_command('生日列表', aliases=('list', 'birthdayList'))
async def birthdays_list(session: CommandSession):
    birthdays = Birthdays()
    user_id = session.ctx['user_id']
    await session.send(birthdays.get_birthday_list(user_id))

# 添加生日
@on_command('addBirthday', aliases=('添加生日', 'AddBirthday'))
async def add_birthday(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    user_id = session.ctx['user_id']
    date = session.get('date', prompt='请输入"YYYY-MM-DD"格式的日期，例：2000-11-22')
    name = session.get('name', prompt='请输入在那天过生日的人的姓名，例：张三')
    birthday = datetime.date.fromisoformat(date)
    check = session.get('check', prompt=f'{birthday, name}，您确认吗？（Y/N）')
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
    name = session.get('name', prompt='请输入在那天过生日的人的姓名，例：张三')
    birthday = datetime.date.fromisoformat(date)
    check = session.get('check', prompt=f'{birthday, name}，您确认吗？（Y/N）')
    if check == 'Y':
        birthdays = Birthdays()
        await session.send(birthdays.del_birthday(user_id, birthday, name))
    else:
        await session.send('已取消删除！')
    print("del_birthday", user_id, birthday, name, check)
    await session.send('完成！')
