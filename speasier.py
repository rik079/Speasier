# Copyright(C) 2020 Rik079, Micro-T

import discord
from discord.ext import commands

import config


token = config.token

version = config.__version__

description = """Speasier Discord server text-to-speech bot"""

bot = commands.Bot(command_prefix="!", description=description)

client = discord.Client()

@bot.event
async def on_ready():
    print(f"The bot is logged in as {bot.user.name} now! have a wonderful day!")


extensions = ["cogs.events", "cogs.moderation", "cogs.error", "cogs.admin", "cogs.channel_management"]


bot.run(token)