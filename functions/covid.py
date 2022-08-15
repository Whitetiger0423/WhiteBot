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
from discord import ApplicationContext
from utils.commands import slash_command
import requests
from bs4 import BeautifulSoup
import discord

covid_selectors = {
    "death": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_graph > table > tbody > tr:nth-child(1) > td:nth-child(2) > span",
    "confirmed": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_graph > table > tbody > tr:nth-child(1) > td:nth-child(5) > span",
    "total_death": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_num > div:nth-child(1)",
    "total_confirmed": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_num > div:nth-child(2)"
}


class Covid(commands.Cog):
    @slash_command(name="코로나", description="코로나 관련 정보를 출력합니다.")
    async def get_covid(self, ctx: ApplicationContext):
        response = requests.get("http://ncov.mohw.go.kr/")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        death = soup.select_one(covid_selectors["death"]).get_text()
        confirmed = soup.select_one(covid_selectors["confirmed"]).get_text()
        total_death = soup.select_one(covid_selectors["total_death"]).get_text()[6:]
        total_confirmed = soup.select_one(covid_selectors["total_confirmed"]).get_text()[6:-4]
        embed = discord.Embed(title="코로나 현황", color=0xFFFFFF)
        embed.add_field(name="오늘 사망자", value=f"{death}명")
        embed.add_field(name="오늘 확진자", value=f"{confirmed}명")
        embed.add_field(name="누적 사망자", value=f"{total_death}명")
        embed.add_field(name="누적 확진자", value=f"{total_confirmed}명")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Covid())
