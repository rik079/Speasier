import discord
from discord.ext import commands
from modules import database
from discord.utils import get
from speasier import client
import sqlite3
from modules import polly

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

        #first we check if the member is inside a voice channel 
        if ctx.author.voice == None:
            return
            
        # check if the channel is registered
        try:
            cur.execute("SELECT * FROM channels WHERE ChannelID = ?", [ctx.channel.id])
            rows = cur.fetchall()
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error coccured: `{er}`")

        if len(rows) != 1:
            return
            
        # check if roles are registered
        try:
            cur.execute("SELECT * FROM users WHERE DiscordID = ?",
                        [ctx.author.id])
            rows2 = cur.fetchall()
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error coccured: `{er}`")

        
        if len(rows2) != 1:
            role = None
        else:
            data = rows2[0]
            role = discord.utils.get(user.guild.roles, id=int(data[2]))
        
        # from here we need to call the polly API and then send the response into a voice channel
        # the role will be either a name or None
        # not sure what you need to make polly use the standard voice
        


    

def setup(bot):
    bot.add_cog(MessageHandler(bot))
