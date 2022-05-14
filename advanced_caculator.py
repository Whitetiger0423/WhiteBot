import asyncio
import discord
import math
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option


class calcadvance(commands.Cog):
    @slash_command(description="단순 연산이 아닌 공학용 계산기 수준의 값을 제공합니다.")
    async def calcadvance(
        self,
        ctx: ApplicationContext,
        type: Option(
            str,
            "값을 선택할 삼각비 또는 삼각함수의 종류를 선택하세요.",
            choices=["Cosine", "Sine", "Tansent", "Cosequent", "Sequent", "Cotansent", "Factorial", "Log"],
        ),
        first: Option(str, "각도를 입력해주세요"),
    ):
        if type == "Cosine":
            equal = str(math.cos(math.pi * (first / 180)))
        if type == "Sine":
            equal = str(math.sin(math.pi * (first / 180)))
        if type == "Tansent":
            equal = str(math.tan(math.pi * (first / 180)))
        if type == "Cosequent":
            equal = str(1.0 / math.cos(first))
        if type == "Sequent":
            equal = str(1.0 / math.sin(first))
        if type == "Cotansent":
            equal = str(1.0 / math.tan(first))
            str(1.0 / math.sin(txt))
        if type == "Factorial"
            equal = str(math.factorial(first))
        elif type == "Log":
            equal = str(math.log(first))
        embed = discord.Embed(
            title="<a:check:824251178493411368> 계산 완료!",
            description=f"{type}의 **{choises}**결과입니다.",
            color=0xFFFFFF,
        ).add_field(name="**결과:**", value=f"```{equal}```", inline=False)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(calcadvance())
