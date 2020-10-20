# Copyright (c) 2020, Rik079, Worthy Alpaca, Zibadian, Micro-T. All rights reserved.

import discord
from discord.ext import commands
import speasier
from modules import database
import sqlite3

prefix = speasier.bot.command_prefix
client = speasier.client
database = database.database


class TTSchannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def channel(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Channel settings",
                                  color=discord.Color.red())
            embed.add_field(name="Register as a TTS-channel",
                            value=f"{prefix}channel register <voice channel ID> "
                                  f"<Channel name>")
            await ctx.send(embed=embed)

    @channel.command()
    async def register(self, ctx, vchannelid, *, vchannelname):
        # Check if text channel is already registered
        # Note that vchannelname doesn't have to match it's actual name
        try:
            cur = database.cursor()
            res = cur.execute(f"Select * from channels "
                              f"where ChannelID = '{ctx.channel.id}'").fetchall()
        except sqlite3.Error as error:
            return await ctx.send(f"Couldn't reach database, contact a tech: 1 {error}")

        if len(res) != 0:
            embed = discord.Embed(title=f"{res[0][4]} is already registered as TTS for {res[0][3]}",
                                  color=discord.Color.blue())
            return await ctx.send(embed=embed)
        # Now, do the same for the voice channel
        try:
            res = cur.execute(f"Select * from channels "
                              f"where VChannelID = '{vchannelid}'").fetchall()
        except sqlite3.Error as error:
            return await ctx.send(f"Couldn't reach database, contact a tech: 2 {error}")

        if len(res) != 0:
            embed = discord.Embed(title=f"This voice chat already has a TTS channel: {res[0][4]}",
                                  color=discord.Color.blue())
            return await ctx.send(embed=embed)

        try:
            cur.execute(f"insert into channels (GuildID,ChannelID,VChannelID,"
                        f"VChannelName,ChannelName)"
                        f"values('{ctx.guild.id}', '{ctx.channel.id}',"
                        f"'{vchannelid}', '{vchannelname}', '{ctx.channel.name}')")
            database.commit()
            embed = discord.Embed(title="Channel successfully registered",
                                  color=discord.Color.dark_green())
            await ctx.send(embed=embed)
        except sqlite3.Error as error:

            await ctx.send(f"Couldn't register channel, contact a tech: {error}")

    @channel.command()
    async def unregister(self, ctx):
        # Look up if channel is registered
        try:
            cur = database.cursor()
            res = cur.execute(f"select * from channels "
                              f"where ChannelID = {ctx.channel.id}").fetchall()
        except sqlite3.Error as error:
            return await ctx.send(f"Couldn't reach the database, contact a tech: {error}")

        # If channel isn't registered, return
        if len(res) == 0:
            embed = discord.Embed(title=f"Cannot comply: #{ctx.channel.name} isn't registered!",
                                  color=discord.Color.orange())
            return await ctx.send(embed=embed)
        # Else, unregister the channel
        else:
            try:
                cur.execute(f"delete from channels "
                            f"where ChannelID = {ctx.channel.id}")
                database.commit()
                embed = discord.Embed(title="Channel successfully unregistered",
                                      color=discord.Color.dark_red())
                await ctx.send(embed=embed)
            except sqlite3.Error as error:
                return await ctx.send(f"Couldn't unregister channel, contact a tech: {error}")


def setup(bot):
    bot.add_cog(TTSchannel(bot))
