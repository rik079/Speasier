# Copyright (c) 2020 Rik079, Worthy Alpaca, Zibadian, Micro-T. All rights reserved.

import discord
from discord.ext import commands
import os
from utils import checks
from modules import polly


class BotAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(description="Secret stuff", usage="[subcommand] <arguments>")
    @checks.is_tech()
    async def debug(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify a valid subcommand.")

    @debug.command(description="Shut down the bot")
    async def shutdown(self, ctx):
        await ctx.send("Noo! I urge you to reconsider *dies*")
        await self.bot.close()

    @debug.command(description="Run a shell command", usage="[command]")
    async def shell(self, command):
        os.system(command)

    @debug.command(description="Ping for Awesome People(TM)")
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!",
                              description=f"Latency: {round(self.bot.latency, 1)} second")
        await ctx.send(embed=embed)

    @debug.command(description="Manually create TTS file", usage="[voice] [text]")
    async def tts(self, ctx, voice, *, text):
        try:
            polly.synth(voice, text)
            await ctx.send("Manual file creation completed.")
        except:
            return await ctx.send("Unable to create synth file.")

def setup(bot):
    bot.add_cog(BotAdmin(bot))
