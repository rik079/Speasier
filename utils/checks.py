# Copyright(C) 2020 Speasy

import discord
from discord.ext import commands
import config

def is_tech():
    def predicate(ctx):
        if ctx.author.id not in config.botadminids:
            raise commands.MissingPermissions(missing_perms="Tech")
        else:
            return True

    return commands.check(predicate)

def is_admin():
    def predicate(ctx):
        if ctx.author.id not in config.adminids:
            raise commands.NotOwner()
        else:
            return True

    return commands.check(predicate)
