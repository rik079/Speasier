# Copyright (c) 2020 Rik079, Worthy Alpaca, Zibadian, Micro-T. All rights reserved.

import discord
from discord.ext import commands
from modules import database
import sqlite3

database = database.database


class UserManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Get info about your TTS status")
    async def profile(self, ctx):
        cur = database.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE DiscordID = ?",
                        [ctx.author.id])
            rows = cur.fetchall()
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error coccured: `{er}`")

        if len(rows) != 1:
            return await ctx.send("You don't have a registered voice!")        
        
        username = rows[0][1]
        embed = discord.Embed(title=username)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Voice:", value=rows[0][2])
        await ctx.send(embed=embed)

    @commands.command(description="Register a TTS voice", usage="[voice]")
    async def register(self, ctx, voice):
        cur = database.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE DiscordID = ?",
                        [ctx.author.id])
            rows = cur.fetchall()
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error occurred: `{er}`")

        if len(rows) == 1:
            data = rows[0]
            return await ctx.send(f"You already registered. `Your voice is {data[2]}`")

        try:
            cur.execute("INSERT INTO users(DiscordID, Name, Voice) VALUES(?, ?, ?)", [
                        ctx.author.id, ctx.author.name, voice])
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error occurred: `{er}`")

        await ctx.send("Successfully registered")

    @commands.command(description="Unregister yourself from Speasier TTS")
    async def unregister(self, ctx):
        cur = database.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE DiscordID = ?",
                        [ctx.author.id])
            rows = cur.fetchall()
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error occurred: `{er}`")

        if len(rows) != 1:
            return await ctx.send("You don't have a registered voice!")

        try:
            cur.execute("DELETE FROM users WHERE DiscordID = ?",
                        [ctx.author.id])
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error occurred: `{er}`")

        await ctx.send("Successfully unregistered")


def setup(bot):
    bot.add_cog(UserManagement(bot))
