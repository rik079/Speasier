# Copyright(C) 2020 Rik079, Micro-T

import discord
from discord.ext import commands

import config


token = config.token

version = config.__version__

description = """Speasier Discord server text-to-speech bot"""

bot = commands.Bot(command_prefix="?", description=description)

client = discord.Client()

@bot.event
async def on_ready():
    print(f"The bot is logged in as {bot.user.name} now! have a wonderful day!")

@bot.command()
async def falconlaunch(ctx):
    await ctx.send("https://www.youtube.com/watch?v=sB_nEtZxPog")


bot.run(token)
