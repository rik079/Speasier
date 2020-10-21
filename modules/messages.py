import discord
from discord.ext import commands
from modules import database
from discord.utils import get
from speasier import client
import sqlite3

database = database.database

class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot == True:
            return
        user = ctx.author
        cur = database.cursor()
        #first we check if the bot is inside a voice channel        
        def is_connected(ctx):
            voice_client = get(client.voice_clients, guild=ctx.guild)
            return voice_client and voice_client.is_connected()

        if is_connected(ctx) == None: # disable for testing
            return

        try:
            cur.execute("SELECT * FROM channels WHERE ChannelID = ?", [ctx.channel.id])
            rows = cur.fetchall()
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error coccured: `{er}`")

        if len(rows) != 1:
            return await ctx.send("You need to register this voice channel") # Maybe just return here. Need to test that

        # check if roles are present
        try:
            cur.execute("SELECT * FROM users WHERE DiscordID = ?",
                        [ctx.author.id])
            rows2 = cur.fetchall()
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error coccured: `{er}`")

        if len(rows2) != 1:
            return print("returning")

        data = rows2[0]
        role = discord.utils.get(user.guild.roles, id=int(data[2]))
        
        # from here we need to call the polly API and then send the response into a voice channel


    

def setup(bot):
    bot.add_cog(MessageHandler(bot))
