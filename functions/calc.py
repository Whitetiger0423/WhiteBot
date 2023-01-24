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

from constants import Constants
from utils.commands import slash_command


class Calc(commands.Cog):
    @slash_command(name="연산", description="간단한 연산을 수행합니다.")
    async def calc(
            self,
            ctx: ApplicationContext,
            type: Option(
                str,
                "수행할 연산을 선택하세요.",
                choices=["더하기", "빼기", "곱하기", "나누기"],
            ),
            first: Option(float, "연산할 첫 번째 수를 입력하세요"),
            second: Option(float, "연산할 두 번째 수를 입력하세요"),
    ):
        if type == "더하기":
            equal = first + second
        elif type == "빼기":
            equal = first - second
        elif type == "곱하기":
            equal = first * second
        else:  # type == "나누기":
            equal = first / second

        if equal.is_integer():
            equal = int(equal)

        embed = discord.Embed(
            title=f"{Constants.EMOJI['check']} 계산 완료!",
            description=f"**{type}** 연산의 결과입니다.",
            color=Constants.EMBED_COLOR["default"],
        )
        embed.add_field(name="**결과:**", value=f"```{equal}```", inline=False)
        await ctx.respond(embed=embed)

    @calc.error
    async def calc_error(
            self, ctx: ApplicationContext, error: ApplicationCommandInvokeError
    ):
        if isinstance(error.original, ZeroDivisionError):
            embed = discord.Embed(
                title="WhiteBot 오류", description="연산 기능", color=Constants.EMBED_COLOR["error"]
            )
            embed.add_field(name="오류 내용:", value="나누는 수는 0이 될 수 없습니다", inline=False)
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Calc())
