# Copyright(C) 2020 Speasy

import discord
from discord.ext import commands
import os
from utils import checks


class BotAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_tech()
    async def debug(self, ctx, cmd, *, info=''):
        if cmd == 'tts':
            await ctx.send(f"!tts This is a Speasier test. 1. 2. 3. 4. 5. Test completed")
        elif cmd == 'shutdown':
            await ctx.send("Noo! I urge you to reconsider *dies*")
            await self.bot.close()
        elif cmd == 'shell':
            os.system(f"{info}")
        elif cmd == 'ping':
            embed = discord.Embed(title="Pong!",
                                  description=f"Latency: {round(self.bot.latency, 1)} second")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BotAdmin(bot))
