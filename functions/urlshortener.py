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
from discord import ApplicationContext, Option, ApplicationCommandInvokeError
from discord.ext import commands
from utils.commands import slash_command
import urllib

class urlshorten(commands.Cog):
    @slash_command(name="주소단축", description="URL을 단축합니다.")
    async def 주소단축(
        self,
        ctx: ApplicationContext,
        url: Option(str, "단축할 URL을 입력하세요.")
    ):
        requestUrl=f"https://is.gd/create.php?format=simple&url={urllib.parse.quote(url)}"
        # Url shorting service is provided by is.gd - not responsible for the use of the service
        
        requested = urllib.request.urlopen(requestUrl)
        if requested.status == 200: # Succeeded
            shortenedUrl=str(requested.read()) # Store URL

            embed = discord.Embed(
                title="<a:check:824251178493411368> 단축 완료!",
                description=f"`{url}` 에 대해 단축된 URL입니다.",
                color=0xFFFFFF,
            ).add_field(name="**단축된 URL:**", value=f"```{shortenedUrl}```", inline=False)
            embed.set_footer(text="Provided by is.gd")
            
        else: # Failed
            0xFF0000
            embed = discord.Embed(
                title="단축 실패",
                description=f"서버 측 오류로 URL 단축에 실패하였습니다.",
                color=0xFFFFFF,
            ).add_field(name="아래 정보를 포함하여 개발자에게 문의하십시오:", value=f"```Status: {requested.status}```", inline=False)
            embed.set_footer(text="Provided by is.gd")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(urlshorten())
