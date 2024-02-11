from discord.ext import commands
from lib.bot.music_bot import MusicBot
from bot import join_voice_channel
from lib.bot.music_bot import MusicBot

class Music(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.music_bot = MusicBot(self.client)

    @commands.hybrid_command(name='kiki放音樂', help='kiki會幫你放音樂')
    async def play_music(self, ctx:commands.Context, youtube_url:str):
        await join_voice_channel(self.client, ctx.author.voice.channel)
        titles = self.music_bot.add_queue(ctx, youtube_url)
        if titles:
            for title in titles:
                await ctx.reply(f"加入清單: {title}")
        await self.music_bot.play_music()
        
    @commands.hybrid_command(name='kiki切歌', help='kiki會幫你切歌')
    async def stop_music(self, ctx:commands.Context):
        current_music_title = self.music_bot.stop_music()
        await ctx.reply(f'***kiki把[{current_music_title}]切掉了***')

async def setup(command_bot:commands.Bot):
   await command_bot.add_cog(Music(command_bot))
