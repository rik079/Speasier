# Copyright(C) 2020 Speasy

import discord
from discord.ext import commands
from discord.utils import get
from modules import database
import sqlite3

database = database.database


class UserManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
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

    @commands.command(pass_context=True)
    async def register(self, ctx, voice):
        cur = database.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE DiscordID = ?",
                        [ctx.author.id])
            rows = cur.fetchall()
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error coccured: `{er}`")

        if len(rows) == 1:
            data = rows[0]
            return await ctx.send(f"You already registered. `Your voice is {data[2]}`")

        roleVer = voice.lower() # role to add
        user = ctx.message.author  # user
        role = roleVer  # change the name from roleVer to role
        
        try:
            # add the role
            await user.add_roles(discord.utils.get(user.guild.roles, name=role))
        except:
            # if error
            return await ctx.send('There was an error trying to add the role. Please make sure that the role exists.')

        try:
            cur.execute("INSERT INTO users(DiscordID, Name, Voice) VALUES(?, ?, ?)", [
                        ctx.author.id, ctx.author.name, voice.lower()])
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error coccured: `{er}`")

        
        
        await ctx.send("Successfully registered")

    @commands.command()
    async def unregister(self, ctx):
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

        data = rows[0]
        roleVer = data[2]  # role to add
        user = ctx.message.author  # user
        role = roleVer  # change the name from roleVer to role

        try:
            # add the role
            await user.remove_roles(discord.utils.get(user.guild.roles, name=role))
        except:
            return await ctx.send('There was an error trying to remove the role. Please make sure that the role exists and is completly lowercase.')

        try:
            cur.execute("DELETE FROM users WHERE DiscordID = ?",
                        [ctx.author.id])
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error coccured: `{er}`")

        await ctx.send("Successfully unregistered")

def setup(bot):
    bot.add_cog(UserManagement(bot))
