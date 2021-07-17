import discord
import os
import aiohttp
import aiofiles
import aiosqlite
import pickle
import asyncio
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
DBKR_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc4Mjc3NzAzNTg5ODYxNzg4NiIsImlhdCI6MTYxNjU5ODI3NSwiZXhwIjoxNjQ4MTU1ODc1fQ.d5e3kEoj3NtTjM56awSfTQHmcFdtwf9fj4NdAPUF2YAqjlJQPsDTqOzkbX0_HMI9OcOQOvPQNm3JOP18IMth9qQmy0Pzhx__JwFoGd5oQEUnqJe54y0utr7vRqstRJ0zlaUHbfkb8IR6CD5T-zieLvq_Cv4q_XmCxaHCn4GiScg'
aiodb = None

dbkrpy.UpdateGuilds(bot,DBKR_token)

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("버전 1.3.3! 새로운 명령어가 추가되었어요 - 자세한건 /도움"))
    print("다음으로 로그인합니다 : ")
    print(bot.user.name)

async def startup():
    global aiodb
    if aiodb is None:
        aiodb = await aiosqlite.connect("database.db")
        # aiocursor = await aiodb.execute("create table user (id int, tos text)")
        # await aiodb.commit()
        # await aiocursor.close()

async def shutdown():
    await aiodb.close()


for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return None
    aiocursor = await aiodb.execute('SELECT * FROM user WHERE id=?', (message.author.id,))
    dbdata = await aiocursor.fetchall()
    await aiocursor.close()
    if str(dbdata) == '[]':
        nosign = True
    else:
        userdat = dbdata[0][1]
        if str(userdat) == "True":
            nosign = False
        else:
            nosign = True
    if nosign and message.content.startswith("/") and bot.get_command(message.content.replace("/", "", 1)) is not None and message.content.replace("/", "", 1) != "가입":
        embed = discord.Embed(title=" 가입",
                              description=f"가입을 하셔야 해요!",
                              color=0xff0000)
        return await message.channel.send(embed=embed, delete_after=120)

    await bot.process_commands(message)

try:
    (asyncio.get_event_loop()).run_until_complete(startup())
except KeyboardInterrupt:
    (asyncio.get_event_loop()).run_until_complete(shutdown())

bot.run("NzgyNzc3MDM1ODk4NjE3ODg2.X8RH7A.7D3lcBRv5WiabGpzqruzYaGsv6Y")
