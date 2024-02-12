# 導入 Discord.py
import asyncio
import os

import discord
from pytube import YouTube

from lib.handler.youtube_handler import (
    YoutubeHandler,
    get_playlist_id,
    get_video_id,
)
from pathlib import Path
from lib.utils.file_path import ASSET_PATH
from lib.utils.logger import log


class MusicBot:
    def __init__(self, dc_client):
        self.dc_client = dc_client
        self.voice = discord.VoiceProtocol
        self.audio = discord.FFmpegPCMAudio
        self.voice_channel = discord.VoiceChannel
        self.text_channel = discord.TextChannel
        self.playlist = {}

    def add_queue(self, url):

        yt_handler = YoutubeHandler()

        playlist_id = get_playlist_id(url)
        video_id = get_video_id(url)

        titles = []

        if playlist_id:
            if video_id:
                title = yt_handler.get_video_title(video_id)
                log(f"[music_bot] add queue: {title}")

                if title:
                    self.playlist[video_id] = {
                        "title": title,
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                    }
                    titles.append(title)

            for video_id in yt_handler.get_playlist_ids(playlist_id):

                title = yt_handler.get_video_title(video_id)
                log(f"[music_bot] add queue: {title}")
                if title:
                    self.playlist[video_id] = {
                        "title": title,
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                    }
                    titles.append(title)

        elif video_id:
            title = yt_handler.get_video_title(video_id)
            log(f"[music_bot] add queue: {title}")
            if title:
                self.playlist[video_id] = {
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                }
                titles.append(title)

        else:
            log("[music_bot] add queue: url error")

        return titles

    async def play_music(self, channel, song_path=None, next=False):
        if not self.playlist:
            return

        if len(self.playlist) == 0:
            return

        if not self.voice_channel:
            return

        self.voice_channel = discord.utils.get(self.dc_client.voice_clients)

        if self.voice_channel.is_playing() and not next:
            return

        video_id = list(self.playlist.keys())[0]
        video_url = self.playlist[video_id]["url"]
        title = self.playlist[video_id]["title"]

        del self.playlist[video_id]

        log(f"[music_bot] play music: {title}")
        await channel.send(f"[umsic_bot] play music: {title}")

        yt = YouTube(video_url)
        song_path = Path(
            yt.streams.first().download(
                output_path=ASSET_PATH, filename=video_id + ".mp4"
            )
        )

        self.voice_channel.play(
            self.audio(
                executable="D:/ffmpeg/bin/ffmpeg.exe",
                source=song_path,
                options="-af \"volume=0.1\"",
            ),
            after=lambda x: asyncio.run_coroutine_threadsafe(
                self.play_music(channel, song_path, next=True),
                self.dc_client.loop,
            ),
        )

    def stop_music(self):
        if self.voice_channel.is_playing():
            self.audio.cleanup()
