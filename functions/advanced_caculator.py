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
            "값을 선택할 삼각비 또는 삼각함수의 종류를 선택하세요.",
            choices=[
                "Cosine",
                "Sine",
                "Tansent",
                "Cosequent",
                "Sequent",
                "Cotangent",
                "Factorial",
                "Log",
            ],
        ),
        first: Option(int, "값을 입력해주세요"),
    ):
        if type == "Cosine":
            equal = str(math.cos(math.pi * (first / 180)))
        elif type == "Sine":
            equal = str(math.sin(math.pi * (first / 180)))
        elif type == "Tansent":
            equal = str(math.tan(math.pi * (first / 180)))
        elif type == "Cosequent":
            equal = str(1.0 / math.cos(first))
        elif type == "Sequent":
            equal = str(1.0 / math.sin(first))
        elif type == "Cotangent":
            equal = str(1.0 / math.tan(first))
            str(1.0 / math.sin(txt))
        elif type == "Factorial":
            equal = str(math.factorial(first))
        elif type == "Log":
            equal = str(math.log(first))
        embed = discord.Embed(
            title="<a:check:824251178493411368> 계산 완료!",
            description=f"{type} {first}의 결과입니다.",
            color=0xFFFFFF,
        ).add_field(name="**결과:**", value=f"```{equal}```", inline=False)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(calcadvance())
