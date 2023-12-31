import platform
import asyncio
import discord
from discord.ext import commands
from config import discord_token, discord_channel_id

class Bot(commands.AutoShardedBot):
    def __init__(self, folder_id) -> None:
        self.folder_id = folder_id
        intents: discord.Intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self) -> None:
        print(f'logged in to discord as {self.user}')
        channel = self.get_channel(discord_channel_id)

        await channel.send(
            "A new folder has been uploaded: \n" +
            "https://drive.google.com/drive/u/3/folders/" + self.folder_id + "\n" +
            "Todo:"
        )

        await channel.send(
            "Upload to [YT](https://studio.youtube.com/channel/UCFyJy3JBtBLFJHUe9hGxqbA)"
        )
        await channel.send(
            "Upload to [TikTok](https://www.tiktok.com/creator-center/upload?from=upload)"
        )
        await channel.send(
            "Upload to [Instagram](https://www.instagram.com/)"
        )

        await channel.send("Please delete the done Todos")

        await self.close()


def send_message(folder_id):
    if platform.system().lower() == 'windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    bot = Bot(folder_id)
    bot.run(discord_token, log_handler=None)
