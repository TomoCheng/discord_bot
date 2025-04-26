import asyncio
import discord
from discord.ext import commands
from pytube import YouTube
from lib.handler.youtube_handler import (
    YoutubeHandler,
    get_playlist_id,
    get_video_id,
)
from pathlib import Path
from lib.utils.file_path import ASSET_PATH
from lib.utils.logger import log
from discord.ext import commands

class MusicBot:
    def __init__(self,
                 client:discord.Client = None,
                 audio:discord.FFmpegPCMAudio = None,
                 voice_channel:discord.VoiceChannel = None,):
        self.client = client
        self.audio = audio
        self.voice_channel = voice_channel
        self.playlist = {}
        self.current_music_title = ''

    def add_queue(self, ctx:commands.Context, url:str):

        yt_handler = YoutubeHandler()

        playlist_id = get_playlist_id(url)
        video_id = get_video_id(url)

        titles = []

        if playlist_id:
            if video_id:
                title = yt_handler.get_video_title(video_id)
                log(f"[music_bot] add queue: {title}")

                if title:
                    self.playlist[ctx] = {
                        "video_id": video_id,
                        "title": title,
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                    }
                    titles.append(title)

            for video_id in yt_handler.get_playlist_ids(playlist_id):

                title = yt_handler.get_video_title(video_id)
                log(f"[music_bot] add queue: {title}")
                if title:
                    self.playlist[ctx] = {
                        "video_id": video_id,
                        "title": title,
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                    }
                    titles.append(title)

        elif video_id:
            title = yt_handler.get_video_title(video_id)
            log(f"[music_bot] add queue: {title}")
            if title:
                self.playlist[ctx] = {
                    "video_id": video_id,
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                }
                titles.append(title)

        else:
            log("[music_bot] add queue: url error")

        return titles

    async def play_music(self, song_path=None, next=False):
        if not self.playlist:
            return

        if len(self.playlist) == 0:
            self.current_music_title = ''
            return

        self.voice_channel = discord.utils.get(self.client.voice_clients)
            
        if not self.voice_channel:
            return

        if self.voice_channel.is_playing() and not next:
            return

        ctx = list(self.playlist.keys())[0]
        video_id = self.playlist[ctx]["video_id"]
        video_url = self.playlist[ctx]["url"]
        title = self.playlist[ctx]["title"]
        del self.playlist[ctx]

        log(f"[music_bot] play music: {title}")
        await ctx.reply(f"播放音樂: {title} \n {video_url}")

        yt = YouTube(video_url)
        song_path = Path(
            yt.streams.first().download(
                output_path=ASSET_PATH, filename=video_id + ".mp4"
            )
        )

        self.audio = discord.FFmpegOpusAudio(
            executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",
            source=song_path,
            options="-af \"volume=0.1\"",)
        self.voice_channel.play(
            self.audio,
            after=lambda x: asyncio.run_coroutine_threadsafe(
                self.play_music(song_path, next=True),
                self.client.loop,
            ),
        )
        self.current_music_title = title

    def stop_music(self):
        if self.voice_channel.is_playing():
            self.audio.cleanup()
        return self.current_music_title
