import asyncio
import discord
import random
import re
import os, json
import datetime
import functools
import itertools
import math
from async_timeout import timeout
from discord.commands import slash_command
from discord.commands import Option

bot = discord.Bot()

class manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='봇의 핑을 전송합니다.')
    async def ping(self, ctx):
        embed = discord.Embed(title=':ping_pong: 퐁!', color=0xffffff)
        embed.add_field(name='discord API Ping: ', value=f'{round(self.bot.latency * 1000)} ms')
        await ctx.respond(embed=embed)

    @slash_command(description='메시지를 일정 개수만큼 지웁니다.')
    async def delete(self, ctx, count: Option(int, "삭제할 메시지의 개수를 입력하세요.")):
        try:
            if ctx.author.guild_permissions.administrator:
                if count:
                    await asyncio.sleep(2)
                    await ctx.channel.purge(limit=count)
                    embed=discord.Embed(title="청소 완료!", color=0xffffff)
                    embed.add_field(name="삭제한 메시지의 수:", value=f"{count}", inline=False)
                    await ctx.respond(embed=embed)
                else:
                    embed=discord.Embed(title="오류 발생!", color=0xff0000)
                    embed.add_field(name="값 오류", value="올바른 자연수 값을 입력해주세요.")
            else:
                embed=discord.Embed(title="오류 발생!", color=0xff0000)
                embed.add_field(name="권한 오류", value="권한 확인 후 다시 시도해주세요.", inline=False)
                await ctx.respond(embed=embed)
        except:
            embed=discord.Embed(title="오류 발생!", color=0xff0000)
            embed.add_field(name="권한 오류", value="권한 확인 후 다시 시도해주세요.", inline=False)
            await ctx.respond(embed=embed)

    @slash_command(description='봇의 정보를 전송합니다.')
    async def bot(self, ctx):
        ch = self.bot.guilds
        g = len(ch)
        embed = discord.Embed(title='봇 정보', color=0xffffff)
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/782777035898617886/d0ffaea389fce208e560cea5cf082d46.webp?size=1024')
        embed.add_field(name='봇 이름: ', value=f'{self.bot.user.name}', inline = False)
        embed.add_field(name='봇 ID: ', value=f'`{self.bot.user.id}`', inline = False)
        embed.add_field(name='봇 버전: ', value='1.3.11', inline = False)
        embed.add_field(name='봇 참가 서버 수: ', value=f'`{g}`개의 서버', inline = False)
        embed.add_field(name='봇 개발진: ', value='[Team White](<https://team-white.kro.kr/>)', inline = False)
        embed.add_field(name='서포팅 서버: ', value='[초대 링크](<http://server.whitebot.kro.kr/>)', inline = False)
        await ctx.respond(embed=embed)

    @slash_command(description='봇의 도움말을 전송합니다.')
    async def help(self, ctx, sorts: Option(str, "도움말의 유형을 선택하세요", choices=["기본", "유틸리티", "놀이", "관리"])):
        firsthelpembed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 명령어 도움말", description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
        firsthelpembed.add_field(name="help 명령어 사용법", value="sorts 변수를 선택하세요.", inline=False)
        firsthelpembed.add_field(name="공식 홈페이지", value=":link: [공식 홈페이지](<https://team-white.kro.kr/>)", inline=False)
        firsthelpembed.add_field(name="개인정보 처리방침", value=":link: [개인정보 처리방침](<https://team-white.kro.kr/privacy>)", inline=False)
        firsthelpembed.add_field(name="공식 서포팅 서버", value=":link: [Team White 공식 서버](<https://discord.gg/aebSVBgzuG>)", inline=False)
        firsthelpembed.add_field(name="봇 초대 링크", value=":link: [봇 초대하기](<https://discord.com/oauth2/authorize?client_id=782777035898617886&permissions=8&scope=bot>)", inline=False)
        
        utilityembed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 유틸리티 명령어 도움말", description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
        utilityembed.add_field(name="/search `[항목]`", value="여러 사이트에서 `[항목]`을 검색합니다.", inline=False)
        utilityembed.add_field(name="/send `[항목]`", value="`[항목]`을 전송해요!", inline=False)
        utilityembed.add_field(name="/code `[수신문]`", value="`[수신문]`을 암호화합니다.", inline=False)
        utilityembed.add_field(name="/decode `[암호문]`", value="`[암호문]`을 해독합니다.", inline=False)
        utilityembed.add_field(name="/bot", value="봇의 정보를 전송합니다.", inline=False)
        utilityembed.add_field(name="/youtube", value="들어가 있는 음성 채널에 유튜브 투게더를 활성화 시키는 링크를 보냅니다. 음성 채널에 연결되어 있어야 사용 가능한 명령어입니다.", inline=False)

        playembed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 놀이 명령어 도움말", description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
        playembed.add_field(name="/rsp `[가위, 바위, 보]`", value="봇과 가위바위보를 합니다. `/가위바위보 가위` 등의 형식으로 쓰면 됩니다.", inline=False)
        playembed.add_field(name="/dice `[N]` `(n)`", value="주사위를 굴립니다. `[N]`만 쓰면 1부터 `[N]`까지의 숫자를, `(n)`까지 모두 쓰면 `[N]`부터 `(n)`까지의 숫자를 랜덤으로 표출합니다.", inline=False)

        manageembed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 관리 명령어 도움말",  description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
        manageembed.add_field(name="/ping", value="봇의 핑을 알려줍니다.", inline=False)
        manageembed.add_field(name="/delete `[n]`", value="메시지를 `[n]`의 값 만큼 삭제합니다. 메시지 관리 권한이 필요합니다.", inline=False)

        if sorts == "유틸리티":
            await ctx.respond(embed=utilityembed)
        elif sorts == "놀이":
            await ctx.respond(embed=playembed)
        elif sorts == "관리":
            await ctx.respond(embed=manageembed)
        elif sorts == "기본":
            await ctx.respond(embed=firsthelpembed)

def setup(bot):
    bot.add_cog(manage(bot))
