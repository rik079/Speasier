# Copyright(C) 2020 Speasy

from discord.ext import commands


class UserManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(UserManagement(bot))
