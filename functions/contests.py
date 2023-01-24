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

from datetime import datetime

import discord
from discord.commands import ApplicationContext
from discord.ext import commands

from constants import Constants
from utils.commands import slash_command
from utils.whitebot import WhiteBot


class Contests(commands.Cog):
    def __init__(self, bot: WhiteBot):
        self.bot = bot
        self.session = self.bot.aiohttp_session

    @slash_command(name="코드포스", description="코드포스 콘테스트 상황을 출력합니다")
    async def codeforces(self, ctx: ApplicationContext):
        async with self.session.get("https://codeforces.com/api/contest.list") as response:
            json = await response.json()
            contests = json["result"]
            contest_status = contests[0]["phase"]
            i = 0
            while contest_status == "BEFORE":
                i += 1
                contest_status = contests[i]["phase"]
            active_contests = list(reversed(contests[:i]))
            embed = discord.Embed(title="Codeforces 콘테스트", color=Constants.EMBED_COLOR["default"])
            for contest in active_contests:
                start_time = contest["startTimeSeconds"]
                start_time_formatted = datetime.fromtimestamp(start_time).strftime("%Y/%m/%d %H:%M:%S")
                embed.add_field(name=contest["name"],
                                value=f"[{start_time_formatted}](https://codeforces.com/contests/{contest['id']}) (<t:{start_time}:R>)",
                                inline=False)
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Contests(bot))
