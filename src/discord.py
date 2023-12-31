import platform
import asyncio
import discord
from config import discordToken, discordChannelId

from discord.ext import commands

class TestBot(commands.AutoShardedBot):
    def __init__(self, folderId) -> None:
        self.folderId = folderId
        intents: discord.Intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self) -> None:
        print(f'logged in to discord as {self.user}')
        channel = self.get_channel(discordChannelId)
        
        await channel.send(
            "A new folder has been uploaded: \n" +
            "https://drive.google.com/drive/u/3/folders/" + self.folderId + "\n" +
            "Todo:"
        )

        await channel.send("Upload to [YT](https://studio.youtube.com/channel/UCFyJy3JBtBLFJHUe9hGxqbA)")
        await channel.send("Upload to [TikTok](https://www.tiktok.com/creator-center/upload?from=upload)")
        await channel.send("Upload to [Instagram](https://www.instagram.com/)")

        await channel.send("Please delete the done Todos")

        await self.close()


def sendMessage(folderId):
    if platform.system().lower() == 'windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    bot = TestBot(folderId)
    bot.run(discordToken, log_handler=None)