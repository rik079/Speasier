# Copyright(C) 2020 Speasy

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import config
from modules import database


token = config.token
version = config.__version__
description = """Speasier Discord server text-to-speech bot"""
bot = commands.Bot(command_prefix="?", description=description)

client = discord.Client()


@bot.event
async def on_ready():
    for cog in config.extensions:
        bot.load_extension(cog)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("speaking slave for you"))
    print(f"The bot is logged in as {bot.user.name} now! have a wonderful day!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return await ctx.send(error)

@bot.command()
async def falconlaunch(ctx):
    await ctx.send("https://www.youtube.com/watch?v=sB_nEtZxPog")


@bot.command()
async def ping(ctx):
    await ctx.message.add_reaction('\U0001F3D3')

database.db_init()
bot.run(token)
