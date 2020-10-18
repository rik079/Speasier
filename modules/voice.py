from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        # Gets voice channel of message author
        print(ctx.author)
        voice_channel = ctx.author.voice
        channel = None
        if voice_channel != None:
            #channel = voice_channel.name
            vc = "683327300288512027"
            await ctx.bot.join_voice_channel(vc)

        else:
            await ctx.send("You are not connected to any voice channel")

def setup(bot):
    bot.add_cog(Voice(bot))
