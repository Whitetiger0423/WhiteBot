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
import youtube_dl
from async_timeout import timeout
os.system("pip install pynacl")

bot = commands.Bot(command_prefix='/', help_command=None)

class playing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 가위바위보(self, ctx, user: str):
        rps_table = ['가위', '바위', '보']
        bot = random.choice(rps_table)
        result = rps_table.index(user) - rps_table.index(bot)
        if result == 0:
            await ctx.send(
                f'{user} vs {bot}\n{ctx.author.mention} 비겼네요! 다시 한판 하는건 어때요?')
        elif result == 1 or result == -2:
            await ctx.send(
                f'{user} vs {bot}\n{ctx.author.mention}님이 이겼어요! 절 이기시다니 대단해요!'
            )
        else:
            await ctx.send(
                f'{user} vs {bot}\n{ctx.author.mention} 제가 이겼습니다! 한판 더 하실래요?')

    @commands.command()
    async def 주사위(self, ctx, 첫번째숫자: int, 두번째숫자: int = None):
        if (두번째숫자):
            await ctx.send(
                f"{ctx.author.mention} 주사위를 굴렸더니 {random.randint(첫번째숫자, 두번째숫자)}(이)가 나왔어요!"
            )
        else:
            await ctx.send(
                f"{ctx.author.mention} 주사위를 굴렸더니 {random.randint(1, 첫번째숫자)}(이)가 나왔어요!"
            )

def setup(bot):
    bot.add_cog(playing(bot))
