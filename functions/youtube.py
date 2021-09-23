import asyncio
import nextcord
import random
import re
import os, json
import datetime
from nextcord.ext import commands
import functools
import itertools
import math
from async_timeout import timeout
from nextcord.http import Route

bot = commands.Bot(command_prefix='/', help_command=None)

class youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['유튜브투게더', 'youtube'])
    async def 유튜브(self, ctx):
        voice = ctx.author.voice

        if not voice:
            embed = nextcord.Embed(description="이 명령을 사용하려면 사용자가 음성 채널에 있어야합니다.", color=0xff0000)
            return await ctx.channel.send(embed=embed)

        r = Route("POST", "/channels/{channel_id}/invites", channel_id=voice.channel.id)

        payload = {
            "max_age": 0,
            "target_type": 2,
            "target_application_id": 755600276941176913,
        }

        try:
            code = (await self.bot.http.request(r, json=payload))["code"]
        except nextcord.Forbidden:
             embed = nextcord.Embed(description="봇이 초대할 수 있는 권한이 없습니다.", color=0xff0000)
             return await ctx.channel.send(embed=embed)

        embed = nextcord.Embed(title="유튜브 투게더",
                description=f"[여기를 클릭해주세요](https://discord.gg/{code})",
                color=0xffffff,
            )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(youtube(bot))
