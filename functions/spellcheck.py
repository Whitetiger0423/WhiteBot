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
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
from utils.hanspell import spell_checker
from constants import Constants


class SpellCheck(commands.Cog):
    @slash_command(name="맞춤법", description="맞춤법을 검사합니다.")
    async def spellcheck(self, ctx: ApplicationContext, data: Option(str, "검사할 문장을 입력하세요.", name="내용")):
        result = spell_checker.check(data).as_dict()
        if result["errors"] > 0:
            embed = discord.Embed(title="맞춤법 오류 발견", color=Constants.EMBED_COLOR["error"])
            embed.add_field(name="발견된 오류 개수", value=result["errors"], inline=False)
            embed.add_field(name="수정된 문장", value=result["checked"], inline=False)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title=f"{Constants.EMOJI[0]} 맞춤법 오류 없음", color=Constants.EMBED_COLOR["success"])
            embed.add_field(name="문장", value=result["original"])
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(SpellCheck())
