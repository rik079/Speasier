# Copyright(C) 2020 Speasy

import sqlite3
from discord.ext import commands
from utils import checks

database = sqlite3.connect("speasier_db.db")


def db_init():
    cur = database.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'users'"
                "('DiscordID' TEXT NOT NULL UNIQUE, 'Name' TEXT, 'Voice' TEXT, PRIMARY "
                "KEY('DiscordID'));")
    print("Database initialised and ready to go")


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_tech()
    async def sql(self, ctx, *, query):
        cur = database.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        database.commit()
        for row in rows:
            await ctx.send(row)


def setup(bot):
    bot.add_cog(Database(bot))
