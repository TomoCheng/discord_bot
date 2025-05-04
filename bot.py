import discord
import os
import asyncio
from discord.ext import commands
from lib.utils.logger import log
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
command_bot = commands.Bot(command_prefix='!', intents=intents)


async def join_voice_channel(
    client: discord.Client, voice_channel: discord.VoiceChannel, cls=None
) -> discord.VoiceProtocol:
    if client.voice_clients is not None:
        for voice_client in client.voice_clients:
            if voice_client.channel == voice_channel:
                return voice_client
    if cls:
        return await voice_channel.connect(cls=cls)
    else:
        return await voice_channel.connect()


async def leave_voice_channel(
    client: discord.Client, voice_channel: discord.VoiceChannel
):
    for voice_client in client.voice_clients:
        if voice_client.channel == voice_channel:
            return await voice_client.disconnect()


async def init_load_all_cog():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await command_bot.load_extension(f'cogs.{filename[:-3]}')


if __name__ == '__main__':
    asyncio.run(init_load_all_cog())
    bot_token = os.environ.get("discord_bot_token")
    command_bot.run(bot_token)
