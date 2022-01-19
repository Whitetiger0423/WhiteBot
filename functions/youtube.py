import asyncio
import discord
import logging
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
from utils.commands import slash_command

bot = commands.Bot(command_prefix='/', help_command=None)
logger = logging.getLogger(__name__)

class youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='유튜브 투게더에 접속할 수 있는 링크를 전송합니다. 음성 채널에 연결되어 있어야 됩니다.')
    async def youtube(self, ctx):
        voice = ctx.author.voice

        if not voice:
            logger.debug("Unable to execute: member is not connected to a voice channel")
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

            embed = discord.Embed(title="유튜브 투게더", description=f"[여기를 클릭해주세요](https://discord.gg/{code})", color=0xffffff)
            embed.set_footer(text="일부 서버에선 작동하지 않는 베타 기능입니다.")
            await ctx.respond(embed=embed)

        except discord.Forbidden as e:
            logger.debug("Forbidden request\n=> Payload: %s\n=> Response: %s", str(payload), e.text)
            embed = discord.Embed(description="봇이 초대할 수 있는 권한이 없습니다.", color=0xff0000)
            await ctx.respond(embed=embed)
        except discord.HTTPException as e:
            logger.error("Discord API has returned %d\n=> Payload: %s\n=> Response: %s", e.code, str(payload), e.text)
            embed = discord.Embed(description="오류가 발생했어요. 잠시 후에 다시 시도해주세요",color=0xff0000)
            await ctx.respond(embed=embed)
        except Exception as e:
            logger.exception("Unexpected exception occurred")
            embed = discord.Embed(description="오류가 발생했어요. 잠시 후에 다시 시도해주세요",color=0xff0000)
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(youtube(bot))
