import nextcord
import random
from nextcord.ext import commands

bot = commands.Bot(command_prefix='/', help_command=None)

class playing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 가위바위보(self, ctx, user: str):
        rps_table = ['가위', '바위', '보']
        if user not in rps_table:
            embed = nextcord.Embed(title="WhiteBot 오류", description="가위바위보 기능", color=0xff0000)
            embed.add_field(name="오류 내용:", value="`가위, 바위, 보` 중에 하나를 입력해주세요.", inline=False)
            await ctx.send(embed=embed)
        else:
            bot = random.choice(rps_table)
            result = rps_table.index(user) - rps_table.index(bot)
            if result == 0:
                forsend = (f'{user} vs {bot}\n비겼네요!')
            elif result == 1 or result == -2:
                forsend = (f'{user} vs {bot}\n{ctx.author.display_name}님이 이겼어요!')
            else:
                forsend = (f'{user} vs {bot}\n봇이 이겼습니다!')
            embed = nextcord.Embed(title="가위바위보", description=f"봇 vs {ctx.author.display_name}", color=0xffffff)
            embed.add_field(name="**결과:**", value=f"{forsend}", inline=False)
            await ctx.send(embed=embed)

    @commands.command(aliases=['roll', 'dice'])
    async def 주사위(self, ctx, 첫번째숫자: int, 두번째숫자: int = None):
        try:
            if 첫번째숫자 < 1:
                embed = nextcord.Embed(title="WhiteBot 오류", description="주사위 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="자연수 값만 허용됩니다.", inline=False)
                await ctx.send(embed=embed)
            elif (두번째숫자):
                embed = nextcord.Embed(title="주사위", description=f"{첫번째숫자} ~ {두번째숫자}", color=0xffffff)
                embed.add_field(name="**결과:**", value=f"주사위를 굴렸더니 {random.randint(첫번째숫자, 두번째숫자)}(이)가 나왔어요!", inline=False)
                await ctx.send(embed=embed)
            else:
                embed = nextcord.Embed(title="주사위", description=f"1 ~ {첫번째숫자}", color=0xffffff)
                embed.add_field(name="**결과:**", value=f"주사위를 굴렸더니 {random.randint(1, 첫번째숫자)}(이)가 나왔어요!", inline=False)
                await ctx.send(embed=embed)
        except:
            embed = nextcord.Embed(title="WhiteBot 오류", description="주사위 기능", color=0xff0000)
            embed.add_field(name="오류 내용:", value="1. 자연수가 아닌 수를 쓰셨는지 확인해주세요.\n2. 첫번째 숫자가 두번째 숫자보다 더 큰지 확인해주세요.\n3. 너무 긴 숫자가 아닌지 확인해주세요.", inline=False)
            await ctx.send(embed=embed)


    @commands.command(aliases=['룰렛', 'random', '뭐먹지'])
    async def 랜덤(self, ctx, *args):
        if args:
            randomlists = list(args)
            random.choice(randomlists)
            embed = nextcord.Embed(title="랜덤 뽑기", description=f'{args}', color=0xffffff)
            embed.add_field(name="**결과:**", value=f'`{randomlists}`가 나왔습니다!')
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(title="WhiteBot 오류", description="랜덤 기능", color=0xff0000)
            embed.add_field(name="오류 내용:", value="올바른 값을 입력해주세요.", inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(playing(bot))
