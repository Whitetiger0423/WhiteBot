import discord
import os
from discord.ext import commands
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

@bot.command(name="유튜브")
async def youtu1be(ctx): 
    red = 0xFF0000
    blue = 0x00FFFF
    voice = ctx.author.voice

    if not voice:
        embed = discord.Embed(description="이 명령을 사용하려면 사용자가 음성 채널에 있어야합니다...", color=red)
        return await ctx.channel.send(embed=embed)

    r = Route("POST", "/channels/{channel_id}/invites", channel_id=voice.channel.id)

    payload = {
        "max_age": 0,
        "target_type": 2,
        "target_application_id": 755600276941176913,
    }

    try:
        code = (await self.bot.http.request(r, json=payload))["code"]
    except discord.Forbidden:
            embed = discord.Embed(description="봇이 초대할 수 있는 권한이 없습니다...")
            return await ctx.channel.send(embed=embed)

    embed = discord.Embed(title="유튜브 투게더",
            description=f"[여기를 클릭해주세요](https://discord.gg/{code})",
            color=blue,
        )
    await ctx.send(embed=embed)
    
    
for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")


bot.run("NzgyNzc3MDM1ODk4NjE3ODg2.X8RH7A.7D3lcBRv5WiabGpzqruzYaGsv6Y")
