from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        # Gets voice channel of message author
        channel = ctx.author.voice.channel
        await channel.connect()
        

def setup(bot):
    bot.add_cog(Voice(bot))
