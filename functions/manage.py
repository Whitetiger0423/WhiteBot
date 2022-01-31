import asyncio
import discord
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
import time


class manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="봇의 핑을 전송합니다.")
    async def ping(self, ctx: ApplicationContext):
        embed = discord.Embed(title=":ping_pong: 퐁!", color=0xFFFFFF)
        embed.add_field(
            name="discord API Ping: ", value=f"{round(ctx.bot.latency * 1000)} ms"
        )
        await ctx.respond(embed=embed)

    @slash_command(description="메시지를 일정 개수만큼 지웁니다.")
    async def delete(
        self, ctx: ApplicationContext, count: Option(int, "삭제할 메시지의 개수를 입력하세요.")
    ):
        try:
            if ctx.author.guild_permissions.administrator:
                if count:
                    await asyncio.sleep(2)
                    await ctx.channel.purge(limit=count)
                    embed = discord.Embed(title="청소 완료!", color=0xFFFFFF)
                    embed.add_field(name="삭제한 메시지의 수:", value=f"{count}", inline=False)
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(title="오류 발생!", color=0xFF0000)
                    embed.add_field(name="값 오류", value="올바른 자연수 값을 입력해주세요.")
            else:
                embed = discord.Embed(title="오류 발생!", color=0xFF0000)
                embed.add_field(name="권한 오류", value="권한 확인 후 다시 시도해주세요.", inline=False)
                await ctx.respond(embed=embed)
        except:
            embed = discord.Embed(title="오류 발생!", color=0xFF0000)
            embed.add_field(name="권한 오류", value="권한 확인 후 다시 시도해주세요.", inline=False)
            await ctx.respond(embed=embed)

    @slash_command(description="봇의 정보를 전송합니다.")
    async def bot(self, ctx: ApplicationContext):
        nowtime = time.time()
        S = round(nowtime - self.bot.start_time)
        D = 0
        H = 0
        M = 0
        while S >= 86400:
            S = S - 86400
            D += 1
        while S >= 3600:
            S = S - 3600
            H += 1
        while S >= 60:
            S = S - 60
            M += 1

        embed = discord.Embed(title="봇 정보", color=0xFFFFFF)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/782777035898617886/d0ffaea389fce208e560cea5cf082d46.webp?size=1024")
        embed.add_field(name="봇 이름: ", value=f"{ctx.bot.user.name}", inline=True)
        embed.add_field(name="봇 ID: ", value=f"`{ctx.bot.user.id}`", inline=True)
        embed.add_field(name="봇 버전: ", value="1.5.0", inline=True)
        embed.add_field(name="업타임: ", value="{0} 일 {1} 시간 {2} 분 {3} 초".format(D, H, M, S), inline=True)
        embed.add_field(name="봇 참가 서버 수: ", value=f"`{len(ctx.bot.guilds)}`개의 서버", inline=True)
        embed.add_field(name="봇 개발진: ", value="[Team White](<https://team-white.kro.kr/>)", inline=True)
        embed.add_field(name="서포팅 서버: ", value="[초대 링크](<http://server.whitebot.kro.kr/>)", inline=True)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(manage(bot))
