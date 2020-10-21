# Copyright (c) 2020 Rik079, Worthy Alpaca, Zibadian, Micro-T. All rights reserved.

import discord
from discord.ext import commands
import dadjokes
import random


class DadJokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Get a dadjoke")
    async def dadjoke(self, ctx, search=''):
        if search != '':
            jokes = list(iter(dadjokes.DadjokeSearch(search)))
            if len(jokes) == 0:
                joke = dadjokes.Dadjoke()
                embed = discord.Embed(title=joke.joke,
                                      colour=discord.Color.red())
                embed.set_footer(text="We couldn't find a joke for \"" + search +
                                      "\" so here's a random joke instead")
                await ctx.send(embed=embed)
            else:
                joke = jokes[random.randint(0, len(jokes) - 1)]
                embed = discord.Embed(title=joke.joke,
                                      colour=discord.Color.blue())
                await ctx.send(embed=embed)
        else:
            joke = dadjokes.Dadjoke()
            embed = discord.Embed(title=joke.joke,
                                  colour=discord.Color.red())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DadJokes(bot))
