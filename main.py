import os

# import json
from argparse import ArgumentParser
import discord
from discord.ext import commands
from termcolor import cprint
import colorama
from aioconsole.stream import ainput

# import requests as rq

from ext.context import Context

parser = ArgumentParser("DiscordCLI", description="A discord client, but from CLI")
parser.add_argument("-t", "--token", help="Your discord account token")
parser.add_argument("-c", "--channel", help="The channel to connect on", type=int)
# parser.add_argument("-e", "--email", help="Your discord email adress")
# parser.add_argument("-p", "--pwd", "--password", help="Your discord password")
args = parser.parse_args()

colorama.init()


class Client(commands.Bot):
    def __init__(self, token):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix="/", intents=intents)
        self.loop.create_task(self.user_input())
        self.channel = None
        self.remove_command("help")

        for command_file in os.listdir("commands"):
            if not command_file.endswith(".py"):
                continue
            self.load_extension(f"commands.{command_file.replace('.py', '')}")

        self._run(token)

    def _run(self, token):
        try:
            super().run(token, bot=False)
        except discord.errors.LoginFailure:
            cprint("Invalid token provided", "red")

    async def on_ready(self):
        self.channel = self.get_channel(args.channel)

        if self.channel is None:
            if args.channel is not None:
                cprint("Invalid channel ID provided.", "red")

            cprint(
                "\n".join(
                    (
                        "Logged in as {0.user} in no specified channel.".format(self),
                        "Send a channel ID to start the program",
                    )
                ),
                "green",
            )
        else:
            cprint("Logged in as {0.user} in #{0.channel}".format(self), "green")

    async def on_message(self, message):
        await self.wait_until_ready()
        if not self.channel:
            return
        if message.author.id == self.user.id:
            return
        if message.channel.id != self.channel.id:
            return

        # fix for the nerf that prevents selfbots to see messages
        hist = await message.channel.history(limit=1).flatten() 
        message = hist[0]
        print("{0.author}: {0.content}".format(message))

    async def user_input(self):
        await self.wait_until_ready()

        while not self.is_closed():
            text = await ainput()
            if not text: continue

            ctx = await self.get_context(text)

            if ctx.channel:
                try:
                    if ctx.command is None:
                        await self.channel.send(text)
                    else:
                        await ctx.command.invoke(ctx)

                except discord.DiscordException as error:
                    cprint(error, "red")

    async def get_context(self, message):
        """Overwrites the default get_context"""

        view = commands.view.StringView(message)
        ctx = Context(view=view, bot=self, message=message)

        prefix = await self.get_prefix(message)
        invoked_prefix = prefix

        if isinstance(prefix, str):
            if not view.skip_string(prefix):
                return ctx
        else:
            invoked_prefix = discord.utils.find(view.skip_string, prefix)
            if invoked_prefix is None:
                return ctx

        invoker = view.get_word()
        ctx.invoked_with = invoker
        ctx.prefix = invoked_prefix
        ctx.command = self.all_commands.get(invoker)
        return ctx

    def change_channel(self, ctx, _channel):
        channel = self._get_channel(_channel)
        if channel is None:
            cprint("Channel not found", "red")
        else:
            self.channel = channel
            if self.channel.type == discord.enums.ChannelType.private:
                cprint(f"Joining DM of {self.channel.recipient}", "green")
            else:
                cprint(f"Joining #{self.channel.name}", "green")

    def _get_channel(self, channel_id):
        channel = self.get_channel(channel_id)
        if channel is not None:
            return channel

        user = self.get_user(channel_id)
        if user is not None:
            return user.dm_channel

        return None


if __name__ == "__main__":
    Client("")
