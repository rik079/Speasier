from discord.ext import commands
from speasier import client

global VCchannel
class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        # Gets voice channel of message author
        if ctx.author.voice == None:
            return await ctx.send("You need to join the voice channel before you can do that")
        channel = ctx.author.voice.channel
        VCchannel = await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client == None:
            return await ctx.send("You need to join the voice channel before you can do that")
        await ctx.voice_client.disconnect()

def setup(bot):
    bot.add_cog(Voice(bot))
