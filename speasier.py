# Copyright (c) 2020 Rik079, Worthy Alpaca, Zibadian, Micro-T. All rights reserved.

import discord
from discord.ext import commands
import discord.ext.commands as errors
import config
from modules import database
import os
import boto3


token = config.token
version = config.__version__
description = """Speasier Discord server text-to-speech bot"""
bot = commands.Bot(command_prefix="?", description=description)

client = discord.Client()

polly_client = boto3.Session(aws_access_key_id=config.aws_id,
                             aws_secret_access_key=config.aws_secret,
                             region_name=config.aws_region).client('polly')

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


if not os.path.exists('Speasier_audio'):
    os.makedirs('Speasier_audio')
if not os.path.exists('Speasier_audio/Soundboard'):
    os.makedirs('Speasier_audio/Soundboard')
database.db_init()
bot.run(token)