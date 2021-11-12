import re
import discord


def replace_user_mentions(message, client):
    match = [i.group(0) for i in re.finditer(r"<(@!)([0-9]+)>", message.content)]
    if match:
        for mention in match:
            mention_id = int(
                mention.replace("<@", "").replace(">", "").replace("!", "")
            )

            if (result := client.get_user(mention_id)) is not None:
                message.content = message.content.replace(mention, f"@{result}")
    # return content


def replace_roles_mentions(message):
    match = [i.group(0) for i in re.finditer(r"<(@&)([0-9]+)>", message.content)]
    if match:
        for mention in match:
            mention_id = int(
                mention.replace("<@", "").replace(">", "").replace("&", "")
            )

            def check(role):
                return role.id == mention_id

            if (result := discord.utils.find(check, message.guild.roles)) is not None:
                message.content = message.content.replace(mention, f"@{result}")
    # return content


def replace_channel_mentions(message, client):
    match = [i.group(0) for i in re.finditer(r"<#([0-9]+)>", message.content)]
    if match:
        for mention in match:
            mention_id = int(mention.replace("<#", "").replace(">", ""))

            if (result := client.get_channel(mention_id)) is not None:
                message.content = message.content.replace(mention, f"#{result}")
    # return content
