import json
from argparse import ArgumentParser
import discord
from discord.ext import commands
from termcolor import cprint
import colorama
import requests as rq

parser = ArgumentParser("DiscordCLI", description="A discord client, but from CLI")
parser.add_argument("-t", "--token", help="Your discord account token")
parser.add_argument("-e", "--email", help="Your discord email adress")
parser.add_argument("-p", "--pwd", "--password", help="Your discord password")
args = parser.parse_args()

colorama.init()


class Client(commands.Bot):
    """Ceci est la doc"""
    pass


if __name__ == "__main__":
    Client()
