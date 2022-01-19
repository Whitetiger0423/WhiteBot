import discord
import os
import dotenv
import logging
from discord.ext import commands
from koreanbots.client import Koreanbots

dotenv.load_dotenv()

loggingLevel = logging.INFO \
    if os.getenv("TEST_GUILD_ID") is None else logging.DEBUG
logging.basicConfig(level=loggingLevel)

bot = commands.Bot(command_prefix="/", help_command=None)
logger = logging.getLogger('main')


@bot.event
async def on_ready():
    guild_count = len(bot.guilds)

    logger.info(f"Logged in as {bot.user.name}")
    logger.info(f'Be used in {guild_count} guilds.')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"버전 1.5.0 - {guild_count}개의 서버에서 작동 중"))

    token = os.getenv("DBKR_TOKEN")
    if token is not None:
        try:
            k = Koreanbots(api_key=token)
            await k.guildcount(782777035898617886, servers=guild_count)
        except:
            logger.error("Error while updating Koreanbots server count")
    else:
        logger.warning("No Koreanbots token provided. Server count will not be updated")


for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")


bot.run(os.getenv("BOT_TOKEN"))
