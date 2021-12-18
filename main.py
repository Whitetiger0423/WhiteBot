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
        embed = discord.Embed(title="가입 필요", description=f"`/가입` 명령어를 사용하여 WhiteBot의 모든 명령어를 사용해보세요!", color=0xff0000)
        embed.add_field(name='내용:', value='가입을 하신다면 [개인정보 처리방침](http://team-white.kro.kr/privacy)에 동의하는 것으로 간주됩니다.')
        return await message.channel.send(embed=embed, delete_after=120)

    await bot.process_commands(message)

try:
    (asyncio.get_event_loop()).run_until_complete(startup())
except KeyboardInterrupt:
    (asyncio.get_event_loop()).run_until_complete(shutdown())

@app.command(name="load")
async def load_commands(ctx, extension):
    if ctx.author.id == 763422064794796042:
        if extension == 'all':
            for filename in os.listdir("functions"):
                if filename.endswith(".py"):
                    bot.load_extension(f"functions.{filename[:-3]}")
            embed = discord.embed(title="Successfully loaded", description=f"모든 커맨드가 성공적으로 로드되었습니다.", color=0xffffff)
            await ctx.send(embed=embed)
        else:
            app.load_extension(f"functions.{extension}")
            embed = discord.embed(title="Successfully loaded", description=f"{extension} 커맨드가 성공적으로 로드되었습니다.", color=0xffffff)
            await ctx.send(embed=embed)
    else:
        embed = discord.embed(title="Error", description=f"커맨드를 로드할 권한이 없습니다.", color=0xff0000)
        await ctx.send(embed=embed)

@app.command(name="unload")
async def unload_commands(ctx, extension):
    if ctx.author.id == 763422064794796042:
        if extension == 'all':
            for filename in os.listdir("functions"):
                if filename.endswith(".py"):
                    bot.unload_extension(f"functions.{filename[:-3]}")
            embed = discord.embed(title="Successfully unloaded", description=f"모든 커맨드가 성공적으로 언로드되었습니다.", color=0xffffff)
            await ctx.send(embed=embed)
        else:
            app.unload_extension(f"functions.{extension}")
            embed = discord.embed(title="Successfully unloaded", description=f"{extension} 커맨드가 성공적으로 언로드되었습니다.", color=0xffffff)
            await ctx.send(embed=embed)
    else:
        embed = discord.embed(title="Error", description=f"커맨드를 언로드할 권한이 없습니다.", color=0xff0000)
        await ctx.send(embed=embed)

@app.command(name="reload")
async def unload_commands(ctx, extension):
    if ctx.author.id == 763422064794796042:
        if extension == 'all':
            for filename in os.listdir("functions"):
                if filename.endswith(".py"):
                    bot.unload_extension(f"functions.{filename[:-3]}")
                    bot.load_extension(f"functions.{filename[:-3]}")
            embed = discord.embed(title="Successfully reloaded", description=f"모든 커맨드가 성공적으로 리로드되었습니다.", color=0xffffff)
            await ctx.send(embed=embed)
        else:
            app.unload_extension(f"functions.{extension}")
            app.load_extension(f"functions.{extension}")
            embed = discord.embed(title="Successfully reloaded", description=f"{extension} 커맨드가 성공적으로 리로드되었습니다.", color=0xffffff)
            await ctx.send(embed=embed)
    else:
        embed = discord.embed(title="Error", description=f"커맨드를 리로드할 권한이 없습니다.", color=0xff0000)
        await ctx.send(embed=embed)

bot.run('NzgyNzc3MDM1ODk4NjE3ODg2.X8RH7A.K1mB4kQKkLtDMf1GFzgliFBC_wg')
