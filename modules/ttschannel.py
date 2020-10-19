# Copyright (c) 2020, Rik079, Worthy Alpaca, Zibadian, Micro-T. All rights reserved.

from discord.ext import commands


class TTSchannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(TTSchannel(bot))
