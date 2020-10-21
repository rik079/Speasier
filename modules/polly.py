# Copyright (c) 2020, Rik079, Worthy Alpaca, Zibadian, Micro-T. All rights reserved.

import speasier
from discord.ext import commands

polly_client = speasier.polly_client


def synth(voice, text, filename='speech'):
    response = polly_client.synthesize_speech(VoiceId=voice,
                                              OutputFormat='mp3',
                                              Text=text)
    file = open(f'Speasier_audio/{filename}.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()


class Polly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Polly(bot))
