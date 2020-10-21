# Copyright (c) 2020 Rik079, Worthy Alpaca, Zibadian, Micro-T. All rights reserved.

import sqlite3
from discord.ext import commands
from utils import checks

database = sqlite3.connect("speasier_db.db")


def db_init():
    cur = database.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'users'"
                "('DiscordID' TEXT NOT NULL UNIQUE, 'Name' TEXT, 'VoiceID' TEXT, PRIMARY "
                "KEY('DiscordID'));")
    cur.execute("CREATE TABLE IF NOT EXISTS 'channels'"
                "('GuildID' TEXT NOT NULL, 'ChannelID' TEXT NOT NULL UNIQUE,"
                "'VChannelID' TEXT NOT NULL,"
                "'Soundboard' TEXT);")
    print("Database initialised and ready to go")


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Run an SQL query on the database",
                      usage="[query]")
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
