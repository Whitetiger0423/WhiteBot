import discord
import random
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
import logging

logger = logging.getLogger(__name__)


class playing(commands.Cog):
    @slash_command(description="봇과 가위바위보 게임을 합니다.")
    async def rsp(
        self,
        ctx: ApplicationContext,
        user: Option(str, "낼 것을 선택하세요", choices=["가위", "바위", "보"]),
    ):
        rsp_table = ["가위", "바위", "보"]
        if user not in rsp_table:
            embed = discord.Embed(
                title="WhiteBot 오류", description="가위바위보 기능", color=0xFF0000
            )
            embed.add_field(
                name="오류 내용:", value="`가위, 바위, 보` 중에 하나를 입력해주세요.", inline=False
            )
            await ctx.respond(embed=embed)
        else:
            bot = random.choice(rsp_table)
            result = rsp_table.index(user) - rsp_table.index(bot)
            if result == 0:
                forsend = f"{user} vs {bot}\n비겼네요!"
            elif result == 1 or result == -2:
                forsend = f"{user} vs {bot}\n{ctx.author.display_name}님이 이겼어요!"
            else:
                forsend = f"{user} vs {bot}\n봇이 이겼습니다!"
            embed = discord.Embed(
                title="가위바위보",
                description=f"봇 vs {ctx.author.display_name}",
                color=0xFFFFFF,
            )
            embed.add_field(name="**결과:**", value=f"{forsend}", inline=False)
            await ctx.respond(embed=embed)

    @slash_command(description="주사위를 굴립니다.")
    async def dice(
        self,
        ctx: ApplicationContext,
        firstn: Option(int, "첫번째 숫자를 정하세요. 두번째 숫자가 없을 경우 범위는 0 ~ firstn으로 결정됩니다."),
        secondn: Option(
            int, "두번째 숫자가 있을 경우 범위는 firstn ~ secondn으로 결정됩니다. ", required=False
        ),
    ):
        try:
            if firstn < 1:
                embed = discord.Embed(
                    title="WhiteBot 오류", description="주사위 기능", color=0xFF0000
                )
                embed.add_field(name="오류 내용:", value="자연수 값만 허용됩니다.", inline=False)
                await ctx.respond(embed=embed)
            elif secondn:
                embed = discord.Embed(
                    title="주사위", description=f"{firstn} ~ {secondn}", color=0xFFFFFF
                )
                embed.add_field(
                    name="**결과:**",
                    value=f"주사위를 굴렸더니 {random.randint(firstn, secondn)}(이)가 나왔어요!",
                    inline=False,
                )
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(
                    title="주사위", description=f"1 ~ {firstn}", color=0xFFFFFF
                )
                embed.add_field(
                    name="**결과:**",
                    value=f"주사위를 굴렸더니 {random.randint(1, firstn)}(이)가 나왔어요!",
                    inline=False,
                )
                await ctx.respond(embed=embed)
        except:
            embed = discord.Embed(
                title="WhiteBot 오류", description="주사위 기능", color=0xFF0000
            )
            embed.add_field(
                name="오류 내용:",
                value="1. 자연수가 아닌 수를 쓰셨는지 확인해주세요.\n2. 첫번째 숫자가 두번째 숫자보다 더 큰지 확인해주세요.",
                inline=False,
            )
            await ctx.respond(embed=embed)

    @slash_command(description="홀짝 게임을 시작합니다.")
    async def holjjac(self, ctx: ApplicationContext):
        dice = random.randint(1, 6)
        embed = discord.Embed(
            title="홀짝 게임",
            description="1부터 6까지 나오는 주사위의 수가 짝수일지, 홀수일지 아래의 반응을 눌러 예측해보세요!",
            color=0xFFFFFF,
        )
        embed.add_field(name="> 주사위의 눈", value="?", inline=False)
        embed.add_field(name="> 선택지", value="홀수: 🔴\n짝수: 🔵", inline=True)
        interaction = await ctx.interaction.response.send_message(embed=embed)
        msg = await interaction.original_message()
        await msg.add_reaction("🔴")
        await msg.add_reaction("🔵")
        try:

            def check(reaction, user):
                return (
                    str(reaction) in ["🔴", "🔵"]
                    and user == ctx.author
                    and reaction.message.id == msg.id
                )

            reaction, user = await ctx.bot.wait_for("reaction_add", check=check)
            if (str(reaction) == "🔴" and dice % 2 == 1) or (
                str(reaction) == "🔵" and dice % 2 == 0
            ):
                embed = discord.Embed(
                    title="홀짝 게임", description=f"정답입니다!", color=0xFFFFFF
                )
                embed.add_field(name="> 주사위의 눈", value=f"{dice}")
                embed.add_field(name="> 당신의 선택", value=f"{str(reaction)}", inline=False)
            else:
                embed = discord.Embed(
                    title="홀짝 게임", description=f"틀렸습니다..", color=0xFFFFFF
                )
                embed.add_field(name="> 주사위의 눈", value=f"{dice}")
                embed.add_field(name="> 당신의 선택", value=f"{str(reaction)}", inline=False)
            await msg.edit(embed=embed)
        except:
            logger.exception("Unexpected exception from holjjac")

            embed = discord.Embed(
                title="오류가 발생했어요", description="잠시 후에 다시 시도해주세요", color=0xFF0000
            )
            await msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(playing())
