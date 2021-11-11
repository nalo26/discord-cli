import json
# from argparse import ArgumentParser
import discord
from discord.ext import commands
from termcolor import cprint
import colorama
from aioconsole.stream import ainput
import requests as rq

# parser = ArgumentParser("DiscordCLI", description="A discord client, but from CLI")
# parser.add_argument("-t", "--token", help="Your discord account token")
# parser.add_argument("-e", "--email", help="Your discord email adress")
# parser.add_argument("-p", "--pwd", "--password", help="Your discord password")
# args = parser.parse_args()

colorama.init()

class Client(commands.Bot):

    def __init__(self, token):
        super().__init__(command_prefix='/')
        self.loop.create_task(self.user_input())
        self.channel = None
        self.remove_command("help")
        self._run(token)

    def _run(self, token):
        try:
            super().run(token, bot=False)
        except discord.errors.LoginFailure:
            cprint("Invalid token provided", "red")

    async def on_ready(self):
        cprint(f"Logged in as {self.user.name}#{self.user.discriminator}", "green")

    async def on_message(self, message):
        await self.wait_until_ready()
        if not self.channel: return
        if message.channel.id != self.channel: return
        print(f"{message.author}: {message.content}")

    async def user_input(self):
        await self.wait_until_ready()
        while not self.is_closed():
            text = await ainput()



if __name__ == "__main__":
    Client("")
