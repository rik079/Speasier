# Copyright (c) 2020 Rik079, Worthy Alpaca, Zibadian, Micro-T. All rights reserved.

import discord
from discord.ext import commands
import os
from utils import checks


class BotAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @checks.is_tech()
    async def debug(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify a valid subcommand.")

    @debug.command()
    async def shutdown(self, ctx):
        await ctx.send("Noo! I urge you to reconsider *dies*")
        await self.bot.close()

    @debug.command()
    async def shell(self, command):
        os.system(command)

    @debug.command()
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!",
                              description=f"Latency: {round(self.bot.latency, 1)} second")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BotAdmin(bot))
