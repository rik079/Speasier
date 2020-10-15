# Copyright(C) 2020 Speasy

import discord
from discord.ext import commands
from dadjokes import dadjokes

class DadJokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dadjoke(self, ctx):
        joke = dadjokes.Dadjoke()
        embed = discord.Embed(title=joke.joke,
                              color=discord.Color.red())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DadJokes(bot))