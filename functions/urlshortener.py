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

import discord
from discord import ApplicationContext, Option
from discord.ext import commands
from utils.commands import slash_command
import requests
from bs4 import BeautifulSoup
from constants import Constants


class UrlShorten(commands.Cog):
    @slash_command(name="주소단축", description="URL을 단축합니다.")
    async def url_shorten(
        self,
        ctx: ApplicationContext,
        url: Option(str, "단축할 URL을 입력하세요.")
    ):
        request_url = f"https://is.gd/create.php?format=simple&url={url}"
        # Url shorting service is provided by is.gd - not responsible for the use of the service
        embed = discord.Embed(
            title="요청 중",
            description="URL 단축 서버에 단축된 URL을 요청하고 있습니다.",
            color=Constants.EMBED_COLOR["default"],
        ).add_field(name="**단축된 URL:**", value="요청 중...", inline=False)
        embed.set_footer(text="Provided by is.gd")
        message = await ctx.respond(embed=embed)
        response = requests.get(request_url)
        html = response.text
        shorten_url = BeautifulSoup(html, 'html.parser')
        if response.status_code == 200:  # Succeeded

            embed = discord.Embed(
                title=f"{Constants.EMOJI[0]} 단축 완료!",
                description=f"`{url}` 에 대해 단축된 URL입니다.",
                color=Constants.EMBED_COLOR["default"],
            ).add_field(name="**단축된 URL:**", value=f"```{shorten_url}```", inline=False)
            embed.set_footer(text="Provided by is.gd")

        else:  # Failed
            embed = discord.Embed(
                title="단축 실패",
                description="서버 측 오류로 URL 단축에 실패하였습니다.",
                color=Constants.EMBED_COLOR["error"],
            ).add_field(name="아래 정보를 포함하여 개발자에게 문의하십시오:", value=f"```Status: {response.status_code}```", inline=False)
            embed.set_footer(text="Provided by is.gd")
        await message.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(UrlShorten())
