import discord
import os
import dotenv
from discord.ext import commands
from koreanbots.client import Koreanbots

dotenv.load_dotenv()

bot = commands.Bot(command_prefix='/', help_command=None)
aiodb = None


@bot.event
async def on_ready():
    ch = bot.guilds
    e = len(ch)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"버전 1.5.0 - {e}개의 서버에서 작동 중"))
    print("다음으로 로그인합니다 : ")
    print(bot.user.name)
    print(f'Be used in {e} guilds.')

    token = os.getenv("DBKR_TOKEN")
    if token is not None:
        try:
            k = Koreanbots(api_key=token)
            await k.guildcount(782777035898617886, servers=len(bot.guilds))
        except:
            print("Error while updating Koreanbots server count")
    else:
        print("No Koreanbots token provided. Server count will not be updated")


for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")


bot.run(os.getenv("BOT_TOKEN"))
