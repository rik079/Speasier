# Copyright(C) 2020 Rik079

import discord
from discord.ext import commands


class ErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.on_command_error = self._on_command_error
        self.client = None

    async def _on_command_error(self, ctx, error, bypass=False):
        if (
            hasattr(ctx.command, "on_error")
            or (ctx.command and hasattr(ctx.cog, f"_{ctx.command.cog_name}__error"))
            and not bypass
        ):
            return
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(
                embed=discord.Embed(
                    title="Command not available",
                    description="This can't be used in a DM.",
                    colour=discord.Colour.red(),
                )
            )
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(
                embed=discord.Embed(
                    title="Command not available",
                    description="This can only be used ina  DM",
                    colour=discord.Colour.red(),
                )
            )
        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Wrong parameters",
                description=f"Poke Rik079 or Micro-T if this keeps happening",
                colour=discord.Colour.red(),
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            await ctx.send(
                embed=discord.Embed(
                    title="Access denied.",
                    description=f":SockFiddler *slaps {ctx.message.author} around a bit with a large trout*",
                    colour=discord.Colour.red(),
                )
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    title="Access denied.",
                    description=f"Rik079 *slaps {ctx.message.author} around a bit with a large trout*",
                    colour=discord.Colour.red(),
                )
            )
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    title="Bot Missing Permissions",
                    description="Bot is missing permissions to perform that action. The following permissions are"
                    f" needed: {', '.join([self.bot.tools.perm_format(p) for p in error.missing_perms])}",
                    colour=discord.Colour.red(),
                )
            )
        elif isinstance(error, discord.HTTPException):
            await ctx.send(
                embed=discord.Embed(
                    title="Unknown HTTP Exception",
                    description=f"Please report this to Rik079 or Micro-T.\n```{error.text}````",
                    colour=discord.Colour.red(),
                )
            )
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Unknown Error",
                    description=f"Please report this to Rik079 or Micro T.\n```{error.original.__class__.__name__}: "
                    f"{error.original}```",
                    colour=discord.Colour.red(),
                )
            )


def setup(bot):
    bot.add_cog(ErrorCog(bot))