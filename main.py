import discord
import os
from discord.ext import commands
try:
    import dbkrpy
except ImportError:
    os.system("pip install dbkrpy")
    import dbkrpy
try:
    import koreanbots
except ImportError:
    os.system("pip install koreanbots")
    import koreanbots
from functions import *


bot = commands.Bot(command_prefix='/', help_command=None)
DBKR_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc4Mjc3NzAzNTg5ODYxNzg4NiIsImlhdCI6MTYyNTQwMzg3Mn0.ZLpAckr11OVSbdmpMfvNyYstuYlemDvhyUUZky7iSSWTHITzc2vxHi-Obdg3Q_a3BiS7QzZDTmtHba10JEb0Dso24oaoxWQmUyAQ5ZaQIyAj5lcdo-m_qkyK280pEsV4cYIXd_1PNUwKoO36b78v3gNuQify9BZ7I7nbh2cFNG4'
Bot = koreanbots.Client(bot, DBKR_token)

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("버전 1.3.3! 새로운 명령어가 추가되었어요 - 자세한건 /도움"))
    print("다음으로 로그인합니다 : ")
    print(bot.user.name)


    
for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")


bot.run("NzgyNzc3MDM1ODk4NjE3ODg2.X8RH7A.7D3lcBRv5WiabGpzqruzYaGsv6Y")
