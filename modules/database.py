# Copyright (c) 2020 Rik079, Worthy Alpaca, Zibadian, Micro-T. All rights reserved.

import sqlite3
from discord.ext import commands
from utils import checks

database = sqlite3.connect("speasier_db.db")


def db_init():
    cur = database.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'users'"
                "('DiscordID' TEXT NOT NULL UNIQUE, 'Name' TEXT, 'Voice' TEXT, PRIMARY "
                "KEY('DiscordID'));")
    cur.execute("CREATE TABLE IF NOT EXISTS 'channels'"
                "('GuildID' TEXT NOT NULL UNIQUE, 'ChannelID'	TEXT NOT NULL,"
                "'VChannelID' TEXT NOT NULL);")
    print("Database initialised and ready to go")


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_tech()
    async def sql(self, ctx, *, query):
        cur = database.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error occurred: `{er}`")
        await ctx.send("Query valid.")
        for row in rows:
            await ctx.send(row)


def setup(bot):
    bot.add_cog(Database(bot))
