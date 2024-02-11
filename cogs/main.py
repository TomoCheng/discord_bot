import discord
from discord.ext import commands
from bot import join_voice_channel, leave_voice_channel

class Main(commands.Cog):

    def __init__(self, client=discord.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Command Bot 登入身分: {self.client.user}')
        custom_activity = discord.CustomActivity('喵喵')
        await self.client.change_presence(
            status=discord.Status.idle, activity=custom_activity
        )
        try:
            synced = await self.client.tree.sync()
            print(f"Synced {synced} commands")
        except Exception as e:
            print("An error occurred while syncing: ", e)

    @commands.hybrid_command(name='kiki', help='kiki會跟你打招呼')
    async def kiki(self, ctx:commands.Context):
        await ctx.reply('喵喵喵')

    @commands.hybrid_command(name='kiki來', help='可以叫kiki進頻道')
    async def kiki_come(self, ctx:commands.Context):
        await join_voice_channel(self.client, ctx.author.voice.channel)
        await ctx.reply('喵')

    @commands.hybrid_command(name='kiki滾', help='無情ㄉ趕走kiki')
    async def kiki_fuck_off(self, ctx:commands.Context):
        ctx.defer()
        await leave_voice_channel(self.client, ctx.author.voice.channel)
        await ctx.reply('幹')

async def setup(command_bot:commands.Bot):
   await command_bot.add_cog(Main(command_bot))
