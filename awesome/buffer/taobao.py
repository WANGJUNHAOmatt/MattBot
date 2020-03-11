from nonebot import on_command, CommandSession


__plugin_name__ = '淘宝优惠券'
__plugin_usage__ = """
获取淘宝优惠券或者积分
使用方法：
输入：\"淘宝\" \"淘宝链接\"
例如：淘宝 abc.efg.xyz\\123456
""".strip()


@on_command('转链', aliases=('淘宝', '天猫', '优惠券'))
async def link(session: CommandSession):
    now_link = session.get('link', prompt='你要转换哪个宝贝的链接呢？')
    new_link = await get_new_link(now_link)
    await session.send(new_link)


@link.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['link'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要转换的链接不能为空呢，请重新输入')

    session.state[session.current_key] = stripped_arg


async def get_new_link(now_link: str) -> str:
    return f'{now_link}成功转换！'
