# 導入 Discord.py
import asyncio
import discord
import random
import os
import re
from lib.handler.youtube_handler import YoutubeHandler
from pytube import YouTube
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
dc_bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)
youtube_handler = YoutubeHandler()


# 調用 event 函式庫
@dc_bot.event
# 當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', dc_bot.user)
    custom_activity = discord.CustomActivity('喵喵')
    # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await dc_bot.change_presence(
        status=discord.Status.idle, activity=custom_activity
    )


@dc_bot.event
# 當有訊息時
async def on_message(message):
    # 排除自己的訊息，避免陷入無限循環
    if message.author == dc_bot.user:
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
        print(message_split)
    if message.content.lower().startswith('kiki放音樂'):
        await music_bot.play_music(message)
    if message.content.lower() == 'kiki切歌':
        music_bot.stop_music()


def is_valid_url(url):
    pattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'
    return bool(re.match(pattern, url))


async def join_voice_channel(voice_channel):
    for voice_client in dc_bot.voice_clients:
        if voice_client.channel == voice_channel:
            return voice_client
    return await voice_channel.connect()


async def leave_voice_channel(voice_channel):
    for voice_client in dc_bot.voice_clients:
        if voice_client.channel == voice_channel:
            return await voice_client.disconnect()


class MusicBot:
    def __init__(self):
        self.voice = discord.VoiceProtocol
        self.audio = discord.FFmpegPCMAudio
        self.voice_channel = discord.VoiceChannel
        self.text_channel = discord.TextChannel
        self.file_name = "song.mp4"

    async def play_music(self, message):
        await join_voice_channel(message.author.voice.channel)
        self.voice_channel = message.author.voice.channel
        self.text_channel = message.channel
        message_split = message.content.split(" ", 1)

        is_yt_url = False
        try:
            YouTube(message_split[1])
            is_yt_url = True
        except:
            is_yt_url = False

        video_url = ""
        if is_yt_url:
            video_url = message_split[1]
        else:
            search = message
            video_url = youtube_handler.search_youtube_video(search)

        yt = YouTube(video_url)
        video_name = yt.title

        self.voice = discord.utils.get(dc_bot.voice_clients)

        if self.voice.is_playing():
            play_list_name.append(video_name)
            play_list_url.append(video_url)
            print(f'{video_name} 已加入播放清單 : {play_list_name}')
            await self.text_channel.send(
                f'{video_name} 已加入播放清單 : {play_list_name}'
            )
            return

        song_there = os.path.isfile("song.mp4")

        try:
            if song_there:
                os.remove("song.mp4")
        except PermissionError:
            print("Is song.mp4 playing")

        # 找尋輸入的Youtube連結, 將目標影片下載下來備用

        yt.streams.first().download()
        # 將目標影片改名, 方便找到它
        for file in os.listdir("./"):
            if file.endswith(".mp4"):
                os.rename(file, "song.mp4")
        self.audio = discord.FFmpegPCMAudio(
            executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",
            source=self.file_name,
            options="-af \"volume=0.1\"",
        )
        # 找尋要播放的音樂並播放, 結束後依照after部分的程式進行後續步驟
        self.voice.play(
            self.audio,
            after=lambda x: asyncio.run_coroutine_threadsafe(
                self.on_music_end(),
                dc_bot.loop,
            ),
        )
        await self.text_channel.send(f'正在撥放: {video_name}')

    async def on_music_end(self):
        # 播放完後的步驟, 進行前一首歌刪除, 抓取一首清單內的歌進行播放
        os.remove(self.file_name)
        if len(play_list_url) != 0:
            video_name = play_list_name[0]
            video_url = play_list_url[0]
            del play_list_name[0]
            del play_list_url[0]

            yt = YouTube(video_url)
            yt.streams.first().download()
            # 將目標影片改名, 方便找到它
            for file in os.listdir("./"):
                if file.endswith(".mp4"):
                    os.rename(file, "song.mp4")
            self.audio = discord.FFmpegPCMAudio(
                executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",
                source=self.file_name,
                options="-af \"volume=0.1\"",
            )
            # 找尋要播放的音樂並播放, 結束後依照after部分的程式進行後續步驟
            self.voice.play(
                self.audio,
                after=lambda x: asyncio.run_coroutine_threadsafe(
                    self.on_music_end(),
                    dc_bot.loop,
                ),
            )
            await self.text_channel.send(f'接著播放: {video_name}')
        else:
            await self.text_channel.send('播完ㄌ 掰掰')
            await leave_voice_channel(self.voice_channel)

    def stop_music(self):
        if self.voice.is_playing():
            self.audio.cleanup()


play_list_name = []
play_list_url = []
music_bot = MusicBot()

if __name__ == '__main__':

    bot_token = os.environ.get("discord_bot_token")

    dc_bot.run(bot_token)
