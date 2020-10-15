# Copyright(C) 2020 Speasy

import discord
from discord.ext import commands
from dadjokes import dadjokes

class DadJokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dadjoke(self, ctx, search=''):
        if search != '':
            #TODO put the actual search function here
            joke = dadjokes.Dadjoke()
            embed = discord.Embed(title=joke.joke,
                                  colour=discord.Color.blue())
            embed.set_footer(text="Unfortunately, the dad joke search function "
                                  "doesn't work yet :( here's a random joke for now!")
            await ctx.send(embed=embed)
        else:
            joke = dadjokes.Dadjoke()
            embed = discord.Embed(title=joke.joke,
                                  colour=discord.Color.red())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DadJokes(bot))