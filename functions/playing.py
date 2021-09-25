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

bot = commands.Bot(command_prefix='/', help_command=None)

class playing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 가위바위보(self, ctx, user: str):
        rps_table = ['가위', '바위', '보']
        if user not in rps_table:
            embed = nextcord.Embed(title="WhiteBot 오류", description="가위바위보 기능", color=0xff0000)
            embed.add_field(name="오류 내용:", value="`가위, 바위, 보` 중에 하나를 입력해주세요.", inline=False)
            await ctx.send(embed=embed)
        else:
            bot = random.choice(rps_table)
            result = rps_table.index(user) - rps_table.index(bot)
            if result == 0:
                forsend = (f'{user} vs {bot}\n비겼네요!')
            elif result == 1 or result == -2:
                forsend = (f'{user} vs {bot}\n{ctx.author.display_name}님이 이겼어요!')
            else:
                forsend = (f'{user} vs {bot}\n봇이 이겼습니다!')
            embed = nextcord.Embed(title="가위바위보", description=f"봇 vs {ctx.author.display_name}", color=0xffffff)
            embed.add_field(name="**결과:**", value=f"{forsend}", inline=False)
            await ctx.send(embed=embed)

    @commands.command(aliases=['roll', 'dice'])
    async def 주사위(self, ctx, 첫번째숫자: int, 두번째숫자: int = None):
        try:
            if 첫번째숫자 < 1:
                embed = nextcord.Embed(title="WhiteBot 오류", description="주사위 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="자연수 값만 허용됩니다.", inline=False)
                await ctx.send(embed=embed)
            else:
                if (두번째숫자):
                    embed = nextcord.Embed(title="주사위", description=f"{첫번째숫자} ~ {두번째숫자}", color=0xffffff)
                    embed.add_field(name="**결과:**", value=f"주사위를 굴렸더니 {random.randint(첫번째숫자, 두번째숫자)}(이)가 나왔어요!", inline=False)
                    await ctx.send(embed=embed)
                else:
                    embed = nextcord.Embed(title="주사위", description=f"1 ~ {첫번째숫자}", color=0xffffff)
                    embed.add_field(name="**결과:**", value=f"주사위를 굴렸더니 {random.randint(1, 첫번째숫자)}(이)가 나왔어요!", inline=False)
                    await ctx.send(embed=embed)
        except:
            embed = nextcord.Embed(title="WhiteBot 오류", description="주사위 기능", color=0xff0000)
            embed.add_field(name="오류 내용:", value="자연수 값만 허용됩니다.", inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(playing(bot))
