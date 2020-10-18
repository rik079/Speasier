# Copyright(C) 2020 Speasy

import discord
from discord.ext import commands
from modules import database

db = database.database


class UserManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx):
        cur = db.cursor()
        res = cur.execute(f"select Name, voice from users where DiscordID = '{ctx.author.id}'").fetchall()
        username = res[0][0]
        embed = discord.Embed(title=username)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Voice:", value=res[0][1])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UserManagement(bot))
