from nonebot import on_command, CommandSession
from Schedule import get_schedule, get_full_schedule
from GlobalValue import normal_user


__plugin_name__ = '获取课程表'
__plugin_usage__ = """
获取当日或完整课程表。
发送'课表'或'kb'获取当日课表,
发送'完整课表'或'fkb'获取完整课程表。
""".strip()


@on_command('课程表', aliases=('课表', 'kb'))
async def schedule(session: CommandSession):
    user_id = session.ctx['user_id']
    if user_id in normal_user:
        await session.send(session.ctx['sender']['nickname']+","+get_schedule(user_id))
    else:
        pass


@on_command('完整课程表', aliases=('fkb', '完整课表'))
async def schedule(session: CommandSession):
    user_id = session.ctx['user_id']
    if user_id in normal_user:
        await session.send(session.ctx['sender']['nickname']+","+get_full_schedule(user_id))
    else:
        pass
