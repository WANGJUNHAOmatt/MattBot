import nonebot
from nonebot import on_command, CommandSession


@on_command('usage', aliases=['使用帮助', '帮助', 'help'])
async def usage(session: CommandSession):
    # 获取设置了名称的插件列表
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))
    arg = session.current_arg_text.strip().lower()
    if not arg:
        # 如果用户没有发送参数，则发送功能列表
        await session.send(
            '我现在支持的功能有：\n' + '\n'.join(p.name for p in plugins) +
            '\n输入‘使用方法’根据指引获得具体使用方式')
        return

    # 如果发了参数则发送相应命令的使用帮助
    for p in plugins:
        if p.name.lower() == arg:
            await session.send(p.usage)


@on_command('使用方法', aliases=('man', 'manuals'))
async def manuals(session: CommandSession):
    app = session.get('app', prompt="请输入要了解的名称（输入usage或帮助获取应用名称）")
    for plugin in nonebot.get_loaded_plugins():
        if plugin.name == app:
            await session.send(plugin.usage)
            return
    await session.send("错误的输入")
