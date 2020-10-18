# Copyright(C) 2020 Speasy

from discord.ext import commands
import sqlite3

database = sqlite3.connect("speasier_db.db")

class UserManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx, cmd):
        cur = database.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE DiscordID = ?", [ctx.author.id])
            rows = cur.fetchall()
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error coccured: {er}")
        
        if len(rows) == 1:
            data = rows[0]
            return await ctx.send(f"You already registered. `Your voice is {data[2]}`")

        try:
            cur.execute("INSERT INTO users(DiscordID, Name, Voice) VALUES(?, ?, ?)", [ctx.author.id, ctx.author.name, cmd])
            database.commit()
        except sqlite3.Error as er:
            return await ctx.send(f"An error coccured: {er}")

        await ctx.send("Successfully registered")


def setup(bot):
    bot.add_cog(UserManagement(bot))
