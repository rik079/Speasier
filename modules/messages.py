import discord
from discord.ext import commands
from modules import database


class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        print(ctx)


    

def setup(bot):
    bot.add_cog(MessageHandler(bot))