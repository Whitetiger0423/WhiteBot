import discord
import math
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option


class AdvancedCalc(commands.Cog):
    @slash_command(name="공학계산", description="공학용 계산기 수준의 연산을 제공합니다.")
    async def calc_eng(
        self,
        ctx: ApplicationContext,
        calc_type: Option(
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
        if calc_type == "사인":
            equal = str(math.sin(math.pi * (first / 180)))
        elif calc_type == "코사인":
            equal = str(math.cos(math.pi * (first / 180)))
        elif calc_type == "탄젠트":
            equal = str(math.tan(math.pi * (first / 180)))
        elif calc_type == "시컨트":
            equal = str(1.0 / math.sin(first))
        elif calc_type == "코시컨트":
            equal = str(1.0 / math.cos(first))
        elif calc_type == "코탄젠트":
            equal = str(1.0 / math.tan(first))
        elif calc_type == "팩토리얼":
            equal = str(math.factorial(first))
        else:  # calc_type == "로그"
            equal = str(math.log(first))
        embed = discord.Embed(
            title="<a:check:824251178493411368> 계산 완료!",
            description=f"{calc_type} {first}의 계산 결과입니다.",
            color=0xFFFFFF,
        ).add_field(name="**계산 결과:**", value=f"```{equal}```", inline=False)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(AdvancedCalc())
