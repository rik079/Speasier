# Copyright (c) 2020 Rik079, Worthy Alpaca, Zibadian, Micro-T. All rights reserved.

from discord.ext import commands
import config


def is_tech():
    def predicate(ctx):
        if ctx.author.id in config.botadminids:
            return True
        else:
            raise commands.MissingPermissions(missing_perms="Tech")

    return commands.check(predicate)


def is_admin():
    def predicate(ctx):
        if ctx.author.id in config.adminids:
            return True
        else:
            raise commands.NotOwner()

    return commands.check(predicate)
