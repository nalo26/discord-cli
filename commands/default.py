from discord.ext import commands

from main import Client


class Default(commands.Cog):
    """Class of all vanilla commands"""

    def __init__(self, client: Client):
        self.client = client

    @commands.command(aliases=["goto"])
    async def channel(self, ctx, _channel=None):
        """Command to switch channel"""
        self.client.change_channel(ctx, int(_channel))


def setup(client):
    client.add_cog(Default(client))
