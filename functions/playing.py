import discord
import random
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option


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
    @slash_command(description="워들을 플레이합니다.")
    async def wordle(
        self,
        ctx: ApplicationContext,
        user: Option(str, "단어를 입력하세요, 단어는 영어 5자만 가능합니다")
    ):
        if user.isalpha() and user.islower() and len(user) == 5:#조건 맞음
            word = open("wordle.txt", 'r', encoding='UTF8')
            data = word.readlines()
            LastLine = len(data) + 1
            await ctx.respond(data[random.randint(1, LastLine)])#2316은 파일 줄 수+1로 수정필요 # 완료 - Whitetiger
        else:
            embed = discord.Embed(
                title="WhiteBot 오류", description="워들 기능", color=0xFF0000
            )
            embed.add_field(
                name="오류 내용:",
                value="1. 영어가 아닌 문자를 쓰셨는지 확인해주세요.\n2. 모든 철자가 소문자인지 확인해주세요",
                inline=False,
            )
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(playing())
