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
from urllib import parse
from discord.ext import commands
from discord.commands import ApplicationContext, Option
from utils.commands import slash_command
from constants import Constants


GOOGLE_URL = "https://www.google.com/search?q="
NAVER_URL = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query="
DAUM_URL = (
    "https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&q="
)
WIKIPEDIA_URL = "https://ko.wikipedia.org/wiki/"
NAVER_TERMS_URL = "https://terms.naver.com/search.naver?query="
NAMU_WIKI_URL = "https://namu.wiki/Search?q="


class Etc(commands.Cog):
    @slash_command(name="검색", description="검색어를 검색합니다.")
    async def search(
        self, ctx: ApplicationContext, *, searching: Option(str, "검색할 문장을 입력하세요.")
    ):
        encoded = parse.quote(searching)

        google = GOOGLE_URL + encoded
        naver = NAVER_URL + encoded
        daum = DAUM_URL + encoded
        wikipedia = WIKIPEDIA_URL + encoded
        termsnaver = NAVER_TERMS_URL + encoded
        namu = NAMU_WIKI_URL + encoded

        embed = discord.Embed(
            title="<a:check:824251178493411368> 검색결과",
            description=f"`{searching}`의 검색 결과입니다.",
            color=Constants.EMBED_COLOR["default"],
        )
        embed.add_field(
            name="포털 사이트 검색 결과",
            value=(
                f"[**구글**]({google})\n[**네이버**]({naver})\n[다음]({daum})\n[지식백과]({termsnaver})"
            ),
            inline=False,
        )
        embed.add_field(
            name="위키 사이트 검색 결과",
            value=(f"[**위키백과**]({wikipedia})\n[**나무위키**]({namu})"),
            inline=False,
        )
        await ctx.respond(embed=embed)

    @slash_command(name="전송", description="내용을 전송합니다.")
    async def send(
        self,
        ctx: ApplicationContext,
        *,
        text: Option(str, "전송할 내용을 입력하세요. 줄바꿈은 적용되지 않습니다."),
    ):
        embed = discord.Embed(
            title=f"Sent by {ctx.author.display_name}",
            description=f"{text}",
            color=Constants.EMBED_COLOR["default"],
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Etc())
