"""Module providing discord messaging function."""

import platform
import asyncio
import discord
from discord.ext import commands
from config import discord as discord_config

class Bot(commands.AutoShardedBot):
    """Class representing a discord bot"""
    def __init__(self, folder_id) -> None:
        self.folder_id = folder_id
        intents: discord.Intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self) -> None:
        """Function send message when the bot is connected."""
        print(f'logged in to discord as {self.user}')
        channel = self.get_channel(discord_config["channel_id"])

        await channel.send(
            "A new folder has been uploaded: \n" +
            "https://drive.google.com/drive/u/3/folders/" + self.folder_id + "\n" +
            "Todo:",
            suppress_embeds=True
        )

        for link in discord_config["links"]:
            await channel.send(
                f"Upload to [{link['label']}]({link['url']})",
                suppress_embeds=True
            )

        await channel.send("Please delete the done Todos")

        await self.close()


def send_message(folder_id):
    """Function sending messages to a discord server."""
    if platform.system().lower() == 'windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if not discord_config["token"]:
        print("no discord token provided")
        return
    if not discord_config["channel_id"]:
        print("no discord channel id provided")
        return

    bot = Bot(folder_id)
    bot.run(discord_config["token"], log_handler=None)
