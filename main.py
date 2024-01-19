import discord
import random
import os
from lib.bot.music_bot import MusicBot
from discord.ext import commands
from lib.utils.logger import log
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
dc_client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)


@dc_client.event
async def on_ready():
    print('目前登入身份：', dc_client.user)
    custom_activity = discord.CustomActivity('喵喵')
    await dc_client.change_presence(
        status=discord.Status.idle, activity=custom_activity
    )


@dc_client.event
async def on_message(message: discord.Message):
    if message.author == dc_client.user:
        return
    if message.content == '你好':
        await message.channel.send('摳泥漆挖')
    if message.content == '擲骰子':
        await message.channel.send(f'KIKI骰出了{random.randint(1, 6)}!')
    if message.content.lower() == 'kiki來':
        await message.channel.send('喵')
        await join_voice_channel(message.author.voice.channel)
    if message.content.lower() == 'kiki進來':
        await message.channel.send('喵')
        await join_voice_channel(message.author.voice.channel)
    if message.content.lower() == 'kiki滾':
        await message.channel.send('幹')
        await leave_voice_channel(message.author.voice.channel)
    if message.content.startswith('找影片'):
        message_split = message.content.split(" ", 1)
        log(message_split)
    if message.content.lower().startswith('kiki放音樂'):
        titles = music_bot.add_queue(message.content.split(" ", 1)[1])

        if titles:
            for title in titles:
                await message.channel.send(f"[music_bot] add queue: {title}")
        await join_voice_channel(message.author.voice.channel)
        await music_bot.play_music(message.channel)
    if message.content.lower() == 'kiki切歌':
        music_bot.stop_music()


async def join_voice_channel(voice_channel: discord.VoiceChannel):
    for voice_client in dc_client.voice_clients:
        if voice_client.channel == voice_channel:
            return voice_client
    return await voice_channel.connect()


async def leave_voice_channel(voice_channel: discord.VoiceChannel):
    for voice_client in dc_client.voice_clients:
        if voice_client.channel == voice_channel:
            return await voice_client.disconnect()


music_bot = MusicBot(dc_client)

if __name__ == '__main__':

    bot_token = os.environ.get("discord_bot_token")
    dc_client.run(bot_token)
