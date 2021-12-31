import asyncio
import discord
import random
import re
import os, json
import datetime
from discord.ext import commands
import functools
import itertools
import math
from async_timeout import timeout
from discord.http import Route
from discord.commands import slash_command

bot = commands.Bot(command_prefix='/', help_command=None)

class youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='유튜브 투게더에 접속할 수 있는 링크를 전송합니다. 음성 채널에 연결되어 있어야 됩니다.')
    async def youtube(self, ctx):
        voice = ctx.author.voice

        if not voice:
            embed = discord.Embed(description="이 명령을 사용하려면 사용자가 음성 채널에 있어야합니다.", color=0xff0000)
            return await ctx.respond(embed=embed)

        r = Route("POST", "/channels/{channel_id}/invites", channel_id=voice.channel.id)

        payload = {
            "max_age": 0,
            "target_type": 2,
            "target_application_id": 755600276941176913,
        }

        try:
            code = (await self.bot.http.request(r, json=payload))["code"]
        except discord.Forbidden:
            embed = discord.Embed(description="봇이 초대할 수 있는 권한이 없습니다.", color=0xff0000)
            return await ctx.respond(embed=embed)

        embed = discord.Embed(title="유튜브 투게더", description=f"[여기를 클릭해주세요](https://discord.gg/{code})", color=0xffffff)
        embed.set_footer(text="일부 서버에선 작동하지 않는 베타 기능입니다.")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(youtube(bot))
