import discord
import os
import aiohttp
import aiofiles
import aiosqlite
import pickle
import asyncio
from discord.ext import commands
import koreanbots
from koreanbots.client import Koreanbots
try:
    import koreanbots
except ImportError:
    os.system("pip install koreanbots")
    import koreanbots
from functions import *



bot = commands.Bot(command_prefix='/', help_command=None)
DBKR_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc4Mjc3NzAzNTg5ODYxNzg4NiIsImlhdCI6MTYzNTM4NzQ2MX0.TRov3uSO4wO0MFQQVhppBL_wYpzjTjwC_FIzV9U7awAVWhqZu9taKTfBH64EAa0q7Tgx0vEy0bcnmex2-tyo_QldVnbzU3ZRjH6vhNoZsOvDOnGshA27iTVMNjicNXew8GeB-KnHckVgMyNcb_7otQRPRtmMkNEpWkMsGBE07NQ'
aiodb = None


@bot.event
async def on_ready():
    ch = bot.guilds
    e = len(ch)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"버전 1.3.11 - {e}개의 서버에서 작동 중"))
    print("다음으로 로그인합니다 : ")
    print(bot.user.name)
    print(f'Be used in {e} guilds.')
    try:
        k = Koreanbots(api_key=DBKR_token)
        await k.guildcount(782777035898617886, servers=len(bot.guilds))
    except:
        print("Error while updating Koreanbots server count")


for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")

try:
    (asyncio.get_event_loop()).run_until_complete(startup())
except KeyboardInterrupt:
    (asyncio.get_event_loop()).run_until_complete(shutdown())


bot.run('NzgyNzc3MDM1ODk4NjE3ODg2.X8RH7A.K1mB4kQKkLtDMf1GFzgliFBC_wg')
