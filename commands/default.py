from discord.ext import commands
from termcolor import cprint

from main import Client

SHORTCUTS = {
    'shrug': r'¯\\\_(ツ)\_/¯',
    'tableflip': '(╯°□°）╯︵ ┻━┻',
    'unflip': '┬─┬ ノ( ゜-゜ノ)',
    'lenny': '( ͡° ͜ʖ ͡°)'
}


class Default(commands.Cog):
    """Class of all vanilla commands"""

    def __init__(self, client: Client):
        self.client = client

    @commands.command(aliases=["goto"])
    async def channel(self, ctx, _channel=None):
        """Command to switch channel"""
        self.client.change_channel(ctx, int(_channel))

    @commands.command(aliases=list(SHORTCUTS))
    async def _shortcut(self, ctx, *message):
        await ctx.send(f"{' '.join(message)} {SHORTCUTS[ctx.invoked_with]}")

    @commands.command()
    async def me(self, ctx, *message):
        await ctx.send(f"*{' '.join(message)}*")

    @commands.command()
    async def spoiler(self, ctx, *message):
        await ctx.send(f"||{' '.join(message)}||")

    @commands.command()
    async def nick(self, ctx, *name):
        if len(name) == 0:
            await ctx.guild.me.edit(nick=None) # reset nick
            cprint(f"Nickname of guild \"{ctx.guild}\" removed.", "blue")
        else:
            nick = " ".join(name)
            await ctx.guild.me.edit(nick=nick)
            cprint(f"Nickname of guild \"{ctx.guild}\" changed to \"{nick}\".", "blue")

    @commands.command()
    async def thread(self, ctx, name, *message):
        pass # TODO



def setup(client):
    client.add_cog(Default(client))
