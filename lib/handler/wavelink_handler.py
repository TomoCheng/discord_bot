import re
import discord
import wavelink
from discord.ext import commands
from bot import join_voice_channel

YOUTUBE_PLAYLIST_REGEX = re.compile(r"(?:list=)([a-zA-Z0-9_-]+)")


class WavelinkHandler:
    """WavelinkHandler"""

    def __init__(self, client: discord.Client):
        self.client = client
        self.pool: wavelink.Pool = wavelink.Pool()

    async def connect(self):
        node = wavelink.Node(
            uri="http://host.docker.internal:2333",
            password="youshallnotpass",
        )
        await self.pool.connect(client=self.client, nodes=[node])

        for node_id, node in self.pool.nodes.items():
            print(f"✅ Node: {node_id} | Object: {node}")

    async def joinChannel(
        self, client: discord.Client, voice_channel: discord.VoiceChannel
    ):
        player: wavelink.Player = await join_voice_channel(
            client, voice_channel, cls=wavelink.Player
        )
        player.autoplay = wavelink.AutoPlayMode.enabled

    async def playMusic(self, ctx: commands.Context, youtube_url: str):

        player: wavelink.Player = ctx.voice_client
        is_playlist = bool(YOUTUBE_PLAYLIST_REGEX.search(youtube_url))

        if is_playlist:  ##清單
            return

        tracks: wavelink.Search = await wavelink.Playable.search(youtube_url)
        ##print("searching:", youtube_url)
        ##results = await wavelink.Playable.search(youtube_url)
        print("results:", tracks)

        if not tracks:
            return await ctx.channel.send("❌ 找不到音樂！")

        track = tracks[0]
        await player.play(track, volume=50)
        await ctx.channel.send(f"🎶 現在播放：{track.title}")
