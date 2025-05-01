import discord
from discord.ext import commands
from lib.handler.wavelink_handler import WavelinkHandler
from bot import join_voice_channel


class Music(commands.Cog):

    def __init__(self, client=discord.Client):
        self.client = client
        self.wavelink_handler = WavelinkHandler(self.client)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.wavelink_handler.connect()

    @commands.hybrid_command(name='kiki放音樂', help='kiki會幫你放音樂')
    async def play_music(self, ctx: commands.Context, youtube_url: str):
        await self.wavelink_handler.joinChannel(
            client=self.client, voice_channel=ctx.author.voice.channel
        )
        await ctx.channel.send('***kiki來放音樂了***')
        await self.wavelink_handler.playMusic(ctx, youtube_url)
        ##titles = self.music_bot.add_queue(ctx, youtube_url)
        ##if titles:
        ##    for title in titles:
        ##        await ctx.reply(f"加入清單: {title}")
        ##await self.music_bot.play_music()

    @commands.hybrid_command(name='kiki切歌', help='kiki會幫你切歌')
    async def stop_music(self, ctx: commands.Context):
        ##current_music_title = self.music_bot.stop_music()
        ##await ctx.reply(f'***kiki把[{current_music_title}]切掉了***')
        await ctx.channel.send('test')


async def setup(command_bot: commands.Bot):
    await command_bot.add_cog(Music(command_bot))
