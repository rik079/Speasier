# Copyright(C) 2020 Speasy

import discord
from discord.ext import commands

class DadJokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(DadJokes(bot))