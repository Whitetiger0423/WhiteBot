import asyncio
import discord
import math
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option


class calcadvance(commands.Cog):
    @slash_command(description="공학용 계산기 수준의 값을 제공합니다.")
    async def 공학연산(
        self,
        ctx: ApplicationContext,
        type: Option(
            str,
            "수행할 연산을 선택하세요.",
            choices=[
                "사인",
                "코사인",
                "탄젠트",
                "시컨트",
                "코시컨트",
                "코탄젠트",
                "팩토리얼",
                "로그",
            ],
        ),
        first: Option(int, "값을 입력해주세요"),
    ):
        if type == "사인":
            equal = str(math.sin(math.pi * (first / 180)))
        elif type == "코사인":
            equal = str(math.cos(math.pi * (first / 180)))
        elif type == "탄젠트":
            equal = str(math.tan(math.pi * (first / 180)))
        elif type == "시컨트":
            equal = str(1.0 / math.sin(first))
        elif type == "코시컨트":
            equal = str(1.0 / math.cos(first))
        elif type == "코탄젠트":
            equal = str(1.0 / math.tan(first))
        elif type == "팩토리얼":
            equal = str(math.factorial(first))
        elif type == "로그":
            equal = str(math.log(first))
        embed = discord.Embed(
            title="<a:check:824251178493411368> 계산 완료!",
            description=f"{type} {first}의 계산 결과입니다.",
            color=0xFFFFFF,
        ).add_field(name="**계산 결과:**", value=f"```{equal}```", inline=False)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(calcadvance())
