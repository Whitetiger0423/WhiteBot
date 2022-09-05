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

from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext
import requests
from bs4 import BeautifulSoup
from json import loads
import discord
from datetime import datetime, timedelta
from constants import Constants


class Contests(commands.Cog):
    @slash_command(name="코드포스", description="코드포스 콘테스트 상황을 출력합니다")
    async def codeforces(self, ctx: ApplicationContext):
        raw_data = str(BeautifulSoup(requests.get("https://codeforces.com/api/contest.list").text, 'html.parser'))
        contests = loads(raw_data)["result"]
        contest_status = contests[0]["phase"]
        i = 0
        while contest_status == "BEFORE":
            i += 1
            contest_status = contests[i]["phase"]
        active_contests = list(reversed(contests[:i]))
        embed = discord.Embed(title="Codeforces 콘테스트", color=Constants.EMBED_COLOR["default"])
        for contest in active_contests:
            startTime = (datetime.fromtimestamp(contest["startTimeSeconds"])).strftime('%Y/%m/%d %H:%M')
            td = str(timedelta(seconds=int(contest["relativeTimeSeconds"] * -1))).replace(" days", "일").replace(" day", "일").split(":")
            beforeStart = f"{td[0]}시간 {td[1]}분 {td[2]}초"
            embed.add_field(name=contest["name"], value=f"{beforeStart} 후({startTime})", inline=False)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Contests())
