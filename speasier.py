# Copyright(C) 2020 Speasy

import discord
from discord.ext import commands
import discord.ext.commands as errors
import config
from modules import database
import os


token = config.token
version = config.__version__
description = """Speasier Discord server text-to-speech bot"""
bot = commands.Bot(command_prefix="?", description=description)

client = discord.Client()


for filename in os.listdir(config.modulepath):
    if filename.endswith('.py'):
        bot.load_extension(f'modules.{filename[:-3]}')


@bot.event
async def on_ready():     
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("speaking slave for you"))
    print(f"The bot is logged in as {bot.user.name} now! have a wonderful day!")

# Error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, errors.CommandNotFound):
        return await ctx.send(error)
    if isinstance(error, errors.RoleNotFound):
        return await ctx.send(error)
    if isinstance(error, errors.BadArgument):
        return await ctx.send(error)

database.db_init()
bot.run(token)