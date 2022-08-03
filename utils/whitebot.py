# Copyright (C) 2022 Team White
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from discord.ext import commands, tasks
import discord
from utils.logging import setup_logging
import logging
from time import time
import os
from utils.koreanbots import update_guild_count
from traceback import format_exception
import sys


class WhiteBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", help_command=None)
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.start_time = time()
        for filename in os.listdir("functions"):
            if filename.endswith(".py"):
                self.load_extension(f"functions.{filename[:-3]}")

    async def on_ready(self):
        guild_count = len(self.guilds)
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"Be used in {guild_count} guilds.")

        dbkr_token = os.getenv("DBKR_TOKEN")
        await update_guild_count(dbkr_token, self.user.id, guild_count)

        self.change_status.start()

    @tasks.loop(seconds=5)
    async def change_status(self):
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"버전 1.10.0 - {len(self.guilds)}개의 서버에서 작동 중"),
        )

    def run(self):
        super().run(os.getenv("BOT_TOKEN"))

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        text = "".join(format_exception(type(error), error, error.__traceback__))
        self.logger.error(text)
        await ctx.send(
            embed=discord.Embed(
                title=f"오류 발생: {error.__class__.__name__}",
                description=f"```{text}```",
                color=0xff0000
            )
        )

    async def on_error(self, event, *args, **kwargs):
        error = sys.exc_info()
        text = f"{error[0].__name__}: {error[1]}"
        embed = discord.Embed(title=f'오류 발생: {error[0].__name__}', color=0xff0000, description=f"```{text}```")
        await args[0].channel.send(embed=embed)
        text = text.replace("\n", " | ")
        self.logger.error(text)
