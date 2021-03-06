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

    @commands.group(description="Set channel settings", usage="[subcommand] <arguments>")
    async def channel(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Channel settings",
                                  color=discord.Color.red())
            embed.add_field(name="Register as a TTS-channel",
                            value=f"{prefix}channel register [voice chat name]")
            embed.add_field(name="Unregister a channel",
                            value=f"{prefix}channel unregister")
            embed.add_field(name="Enable/disable soundboard",
                            value=f"{prefix}channel soundboard")
            embed.add_field(name="Change the voice chat for this channel",
                            value=f"{prefix}channel [new voice chat]")
            await ctx.send(embed=embed)

    @channel.command(description="Register a channel", usage="[voice channel name]")
    async def register(self, ctx, *, vchannelname):
        channel = discord.utils.get(ctx.guild.channels, name=vchannelname)
        # Check if text channel is already registered
        try:
            cur = database.cursor()
            res = cur.execute(f"SELECT * FROM channels "
                              f"WHERE ChannelID = '{ctx.channel.id}'").fetchall()
        except sqlite3.Error as error:
            return await ctx.send(f"Couldn't reach database, contact a tech: 1 {error}")

        # Return if already registered
        if len(res) != 0:            
            vchnlname = discord.utils.get(ctx.guild.channels, id=int(res[0][2]))            
            chnlname = discord.utils.get(ctx.guild.channels, id=int(res[0][1]))            
            embed = discord.Embed(title=f"{chnlname.name} is already registered as TTS for {vchnlname.name}",
                                  color=discord.Color.blue())
            return await ctx.send(embed=embed)
        # Now, do the same for the voice channel
        try:
            res = cur.execute(f"SELECT * FROM channels "
                              f"WHERE VChannelID = '{channel.id}'").fetchall()
        except sqlite3.Error as error:
            return await ctx.send(f"Couldn't reach database, contact a tech: 2 {error}")

        if len(res) != 0:
            chnlname = discord.utils.get(ctx.guild.channels, id=int(res[0][1]))
            embed = discord.Embed(title=f"This voice chat already has a TTS channel: {chnlname.name}",
                                  color=discord.Color.blue())
            return await ctx.send(embed=embed)
        # Check if voice channel exists
        if channel is None:
            embed = discord.Embed(title="Voice channel doesn't exist",
                                  color=discord.Color.dark_red())
            embed.set_footer(text="Make sure to type in the excact name of the channel")
            return await ctx.send(embed=embed)
        # Check if channel is a voice channel
        if channel.type != discord.ChannelType.voice:
            return await ctx.send(embed=discord.Embed(title="That's not a voice channel!",
                                                      color=discord.Color.dark_red()))
        # If all is okay, register the channel
        try:
            cur.execute(f"INSERT INTO channels (GuildID,ChannelID,VChannelID,Soundboard)"
                        f"VALUES('{ctx.guild.id}', '{ctx.channel.id}',"
                        f"'{channel.id}', 'On')")
            database.commit()
            embed = discord.Embed(title="Channel successfully registered",
                                  color=discord.Color.dark_green())
            await ctx.send(embed=embed)
        except sqlite3.Error as error:

            await ctx.send(f"Couldn't register channel, contact a tech: {error}")

    @channel.command(description="Unregister channel")
    async def unregister(self, ctx):
        # Look up if channel is registered
        try:
            cur = database.cursor()
            res = cur.execute(f"SELECT * FROM channels "
                              f"WHERE ChannelID = {ctx.channel.id}").fetchall()
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
                cur.execute(f"DELETE FROM channels "
                            f"WHERE ChannelID = {ctx.channel.id}")
                database.commit()
                embed = discord.Embed(title="Channel successfully unregistered",
                                      color=discord.Color.dark_red())
                await ctx.send(embed=embed)
            except sqlite3.Error as error:
                return await ctx.send(f"Couldn't unregister channel, contact a tech: {error}")

    @channel.command(description="Get info about this channel")
    async def profile(self, ctx):
        # Check if channel is registered
        try:
            cur = database.cursor()
            res = cur.execute(f"SELECT * FROM channels "
                              f"WHERE ChannelID = {ctx.channel.id}").fetchall()
        except sqlite3.Error as error:
            return await ctx.send(f"Couldn't reach the database, contact a tech: {error}")

        # If channel isn't registered, return
        if len(res) == 0:
            channel_name = ctx.channel.name
            embed = discord.Embed(title=f"#{channel_name}",
                                  color=discord.Color.blue(),
                                  description="This channel is not registered. "
                                              "To register it, use "
                                              "`?channel register <voice channel>`")
            embed.set_author(name="TTS Channel profile")
            return await ctx.send(embed=embed)

        # Else, display profile info
        channel_name = discord.utils.get(ctx.guild.channels, id=(int(res[0][1])))
        vchannel_name = discord.utils.get(ctx.guild.channels, id=(int(res[0][2])))
        soundboard_setting = res[0][3]
        embed = discord.Embed(title=f"#{channel_name}",
                              color=discord.Color.blue())
        embed.add_field(name="Voice channel", value=vchannel_name)
        embed.add_field(name="Soundboard", value=soundboard_setting)
        embed.set_author(name="TTS Channel profile")
        await ctx.send(embed=embed)

    @channel.command(description="Enable/disable soundboard, toggles on/off")
    async def soundboard(self, ctx):
        # Get current setting
        try:
            cur = database.cursor()
            res = cur.execute(f"SELECT Soundboard FROM channels "
                              f"WHERE ChannelID = {ctx.channel.id}").fetchall()
        except sqlite3.Error as error:
            return await ctx.send(f"Couldn't reach the database, contact a tech: {error}")
        # If it's off, turn it on
        if res[0][0] == "Off":
            action = "On"
        # And if it's on, turn it Off
        elif res[0][0] == "On":
            action = "Off"
        # Else, error
        else:
            return await ctx.send("Oh noes! setting is not registered in the database correctly. "
                                  "Contact a tech!")
        # Commit action to the database now
        try:
            cur.execute(f"UPDATE channels "
                        f"SET Soundboard = '{action}' "
                        f"WHERE ChannelID = {ctx.channel.id}")
            database.commit()
            await ctx.send(embed=discord.Embed(title=f"Soundboard in this channel is now {action}"))
        except sqlite3.Error as error:
            return await ctx.send(f"Couldn't update setting! contact a tech! {error}")

    @channel.command(description="Change the voice chat this channel belongs to", usage="[new voice chat]")
    async def change_voicechat(self, ctx, *, newvc):
        # Convert newvc to ID
        voicechat = discord.utils.get(ctx.guild.channels, name=newvc)
        # Return if channel doesn't exist...
        if voicechat is None:
            embed = discord.Embed(title="Voice channel doesn't exist",
                                  color=discord.Color.dark_red())
            embed.set_footer(text="Make sure to type in the excact name of the channel")
            return await ctx.send(embed=embed)
        # ... or of it isn't a voice channel.
        if voicechat.type != discord.ChannelType.voice:
            return await ctx.send(embed=discord.Embed(title="That's not a voice channel!",
                                                      color=discord.Color.dark_red()))
        # Get info about the current channel
        try:
            cur = database.cursor()
            res = cur.execute(f"SELECT * FROM channels "
                              f"WHERE ChannelID = {ctx.channel.id}").fetchall()
        except sqlite3.Error as error:
            return await ctx.send(f"Couldn't reach database! contact a tech: {error}")
        # Check if new channel is the same as the old one. If they are return:
        if int(res[0][2]) == voicechat.id:
            embed = discord.Embed(title=f"Cannot comply: {voicechat.name} is already this "
                                        f"channel's voice room!")
            return await ctx.send(embed=embed)
        # Else, continue
        else:
            try:
                cur.execute(f"UPDATE channels "
                            f"SET VChannelID = {voicechat.id} "
                            f"WHERE ChannelID = {ctx.channel.id}")
                database.commit()
                await ctx.send(embed=discord.Embed(title=f"Voice chat of this channel is now {newvc}"))
            except sqlite3.Error as error:
                return await ctx.send(f"Cannot update voice channel! contact a tech: {error}")


def setup(bot):
    bot.add_cog(TTSchannel(bot))
