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
try:
    import dbkrpy
except ImportError:
    os.system("pip install dbkrpy")
    import dbkrpy
from functions import *


bot = commands.Bot(command_prefix='/', help_command=None)
DBKR_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc4Mjc3NzAzNTg5ODYxNzg4NiIsImlhdCI6MTYxNjU5ODI3NSwiZXhwIjoxNjQ4MTU1ODc1fQ.d5e3kEoj3NtTjM56awSfTQHmcFdtwf9fj4NdAPUF2YAqjlJQPsDTqOzkbX0_HMI9OcOQOvPQNm3JOP18IMth9qQmy0Pzhx__JwFoGd5oQEUnqJe54y0utr7vRqstRJ0zlaUHbfkb8IR6CD5T-zieLvq_Cv4q_XmCxaHCn4GiScg'


dbkrpy.UpdateGuilds(bot,DBKR_token)

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("버전 1.3.3! 새로운 명령어가 추가되었어요 - 자세한건 /도움"))
    print("다음으로 로그인합니다 : ")
    print(bot.user.name)

@bot.command()
async def 정보(ctx):
    ch = bot.guilds
    g = len(ch)
    embed = discord.Embed(title='봇 정보', color=0xFEFEFE)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name='봇 이름: ',
                    value=f'{bot.user.name}', inline = False)
    embed.add_field(name='봇 ID: ',
                    value=f'{bot.user.id}', inline = False)
    embed.add_field(name='봇 버전: ',
                    value='1.3.3', inline = False)
    embed.add_field(name='봇 참가 서버 수: ',
                    value=f'{g}개의 서버', inline = False)
    embed.add_field(name='봇 개발진: ',
                    value='[White_team](<http://whiteteam.kro.kr/>)', inline = False)
    embed.add_field(name='서포팅 서버: ',
                    value='[초대 링크](<http://server.whitebot.kro.kr/>)', inline = False)
    await ctx.send(embed=embed)

@bot.command(name="announce")
async def announce(ctx, *, 내용):
    adminid = [763422064794796042]
    if ctx.author.id in adminid:
        now = datetime.datetime.now()
        time = f"{str(now.year)}년 {str(now.month)}월 {str(now.day)}일 {str(now.hour)}시 {str(now.minute)}분 {str(now.second)}초"
        embed = discord.Embed(color=0x00FFFF)
        embed = discord.Embed(title=":loudspeaker: WhiteBot 공지",
                              description=" ",
                              colour=0x00ff00,
                              inline=False)
        embed.add_field(name='공지 내용', value=f'{내용}')
        embed.set_footer(text=f"{str(ctx.author)} - 인증됨\n발송 시간 : {time}",
                         icon_url=ctx.author.avatar_url)
        for guild in bot.guilds:
            senddone = False
            for channel in guild.text_channels:
                try:
                    await channel.send(embed=embed)
                    print(f'공지 전송 완료')
                    senddone = True
                    break
                except:
                    print(f'공지 발송 실패')
                    pass
                if not senddone:
                    print(f'공지 발송 실패')
    else:
        await ctx.send('권한이 부족합니다.')

for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")


bot.run("NzgyNzc3MDM1ODk4NjE3ODg2.X8RH7A.FDYS2PwpH-7SNUPaDezszyBiN3U")
