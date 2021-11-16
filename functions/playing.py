import discord
import random
from discord.ext import commands
from discord.commands import slash_command

bot = commands.Bot(command_prefix='/', help_command=None)

class playing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='봇과 가위바위보 게임을 합니다.')
    async def rsp(self, ctx, user: str):
        rsp_table = ['가위', '바위', '보']
        if user not in rsp_table:
            embed = discord.Embed(title="WhiteBot 오류", description="가위바위보 기능", color=0xff0000)
            embed.add_field(name="오류 내용:", value="`가위, 바위, 보` 중에 하나를 입력해주세요.", inline=False)
            await ctx.respond(embed=embed)
        else:
            bot = random.choice(rsp_table)
            result = rsp_table.index(user) - rsp_table.index(bot)
            if result == 0:
                forsend = (f'{user} vs {bot}\n비겼네요!')
            elif result == 1 or result == -2:
                forsend = (f'{user} vs {bot}\n{ctx.author.display_name}님이 이겼어요!')
            else:
                forsend = (f'{user} vs {bot}\n봇이 이겼습니다!')
            embed = discord.Embed(title="가위바위보", description=f"봇 vs {ctx.author.display_name}", color=0xffffff)
            embed.add_field(name="**결과:**", value=f"{forsend}", inline=False)
            await ctx.respond(embed=embed)

    @slash_command(description='주사위를 굴립니다.')
    async def dice(self, ctx, firstn: int, secondn: int = None):
        try:
            if firstn < 1:
                embed = discord.Embed(title="WhiteBot 오류", description="주사위 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="자연수 값만 허용됩니다.", inline=False)
                await ctx.respond(embed=embed)
            elif (secondn):
                embed = discord.Embed(title="주사위", description=f"{firstn} ~ {secondn}", color=0xffffff)
                embed.add_field(name="**결과:**", value=f"주사위를 굴렸더니 {random.randint(firstn, secondn)}(이)가 나왔어요!", inline=False)
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="주사위", description=f"1 ~ {firstn}", color=0xffffff)
                embed.add_field(name="**결과:**", value=f"주사위를 굴렸더니 {random.randint(1, firstn)}(이)가 나왔어요!", inline=False)
                await ctx.respond(embed=embed)
        except:
            embed = discord.Embed(title="WhiteBot 오류", description="주사위 기능", color=0xff0000)
            embed.add_field(name="오류 내용:", value="1. 자연수가 아닌 수를 쓰셨는지 확인해주세요.\n2. 첫번째 숫자가 두번째 숫자보다 더 큰지 확인해주세요.\n3. 너무 긴 숫자가 아닌지 확인해주세요.", inline=False)
            await ctx.respond(embed=embed)


    @slash_command(description='여러개의 보기 중 하나를 고릅니다.')
    async def random(self, ctx, *factor):
        if factor:
            randomlists = list(factor)
            choiced = random.choice(randomlists)
            embed = discord.Embed(title="룰렛", description=f'{randomlists}', color=0xffffff)
            embed.add_field(name="**결과:**", value=f'`{choiced}`(이)가 나왔습니다!')
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="WhiteBot 오류", description="랜덤 기능", color=0xff0000)
            embed.add_field(name="오류 내용:", value="올바른 값을 입력해주세요.", inline=False)
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(playing(bot))
