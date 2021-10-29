import asyncio
import discord
import random
import re
import os, json
import datetime
from discord.ext import commands
import functools
import itertools
import math
from async_timeout import timeout

bot = commands.Bot(command_prefix='/', help_command=None)

class manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ping'])
    async def 핑(self, ctx):
        embed = discord.Embed(title=':ping_pong: 퐁!', color=0xffffff)
        embed.add_field(name='discord API Ping: ', value=f'{round(self.bot.latency * 1000)} ms')
        await ctx.send(embed=embed)

    @commands.command(aliases=['삭제', 'erase', 'delete'])
    async def 청소(self, ctx, count: int):
        try:
            if ctx.author.guild_permissions.administrator:
                if count:
                    await asyncio.sleep(2)
                    await ctx.channel.purge(limit=count + 1)
                    embed=discord.Embed(title="청소 완료!", color=0xffffff)
                    embed.add_field(name="삭제한 메시지의 수:", value=f"{count}", inline=False)
                    erasemsg = await ctx.send(embed=embed)
                    await asyncio.sleep(3)
                    await erasemsg.delete()
                else:
                    embed=discord.Embed(title="오류 발생!", color=0xff0000)
                    embed.add_field(name="값 오류", value="올바른 자연수 값을 입력해주세요.")
            else:
                embed=discord.Embed(title="오류 발생!", color=0xff0000)
                embed.add_field(name="권한 오류", value="권한 확인 후 다시 시도해주세요.", inline=False)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="오류 발생!", color=0xff0000)
            embed.add_field(name="권한 오류", value="권한 확인 후 다시 시도해주세요.", inline=False)
            await ctx.send(embed=embed)

    @commands.command(aliases=['server'])
    async def 서버(self, ctx):
        embed = discord.Embed(title='서버 정보', color=0xffffff)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='서버 이름: ', value=f'{ctx.guild.name}', inline = False)
        embed.add_field(name='서버 ID: ', value=f'`{ctx.guild.id}`', inline = False)
        embed.add_field(name='서버 지역: ', value=f'{ctx.guild.region}', inline = False)
        embed.add_field(name='서버 부스트 레벨: ', value=f'{ctx.guild.premium_tier}레벨', inline = False)
        embed.add_field(name='멤버 수: ', value=f'{ctx.guild.member_count}', inline = False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['user', '유저'])
    async def 내정보(self, ctx):
        embed = discord.Embed(title='유저 정보', color=0xffffff)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name='계정명: ', value=f'{ctx.author.name}', inline = False)
        embed.add_field(name='ID: ', value=f'`{ctx.author.id}`', inline = False)
        embed.add_field(name='이 서버에서의 별명: ', value=f'{ctx.author.display_name}', inline = False)
        embed.add_field(name='멘션: ', value=f'{ctx.author.mention}', inline = False)
        await ctx.send(embed=embed)

    @commands.command(name="announce")
    async def announce(self, ctx, *, 내용):
        adminid = [763422064794796042]
        if ctx.author.id in adminid:
            now = datetime.datetime.now()
            time = f"{str(now.year)}년 {str(now.month)}월 {str(now.day)}일 {str(now.hour)}시 {str(now.minute)}분 {str(now.second)}초"
            embed = discord.Embed(title=":loudspeaker: WhiteBot 공지", description=" ", color=0xffffff)
            embed.add_field(name='공지 내용', value=f'{내용}')
            embed.set_footer(text=f"{str(ctx.author)} - 인증됨\n발송 시간 : {time}", icon_url=ctx.author.avatar_url)
            for guild in bot.guilds:
                senddone = False
                for channel in guild.text_channels:
                    try:
                        await channel.send(embed=embed)
                        print(f'공지 전송 완료')
                        senddone = True
                        break
                    except:
                        print(f'공지 발송 실패')
                        pass
                    if not senddone:
                        print(f'공지 발송 실패')
        else:
            await ctx.send('권한이 부족합니다.')

    @commands.command(aliases=['봇정보', 'botinfo', 'bot'])
    async def 정보(self, ctx):
        ch = self.bot.guilds
        g = len(ch)
        embed = discord.Embed(title='봇 정보', color=0xffffff)
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/782777035898617886/d0ffaea389fce208e560cea5cf082d46.webp?size=1024')
        embed.add_field(name='봇 이름: ', value=f'{self.bot.user.name}', inline = False)
        embed.add_field(name='봇 ID: ', value=f'`{self.bot.user.id}`', inline = False)
        embed.add_field(name='봇 버전: ', value='1.3.8', inline = False)
        embed.add_field(name='봇 참가 서버 수: ', value=f'`{g}`개의 서버', inline = False)
        embed.add_field(name='봇 개발진: ', value='[Team White](<http://team-white.kro.kr/>)', inline = False)
        embed.add_field(name='서포팅 서버: ', value='[초대 링크](<http://server.whitebot.kro.kr/>)', inline = False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['help', '도움말', 'command', '명령어'])
    async def 도움(self, ctx, 종류 = None):
        if (종류 == None):
            embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 명령어 도움말", description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
            embed.add_field(name="/도움", value="이 메시지를 표출합니다.", inline=False)
            embed.add_field(name="/도움 `관리`", value="서버 관리와 관련된 명령어를 표출합니다.", inline=False)
            embed.add_field(name="/도움 `놀이`", value="WhiteBot으로 할 수 있는 놀이 기능과 관련된 명령어를 표출합니다.", inline=False)
            embed.add_field(name="/도움 `기타`", value="기타 다른 명령어를 표출합니다.", inline=False)
            embed.add_field(name="공식 홈페이지", value=":link: [공식 홈페이지](<http://team-white.kro.kr/>)", inline=False)
            embed.add_field(name="공식 서포팅 서버", value=":link: [Team White 공식 서버](<https://discord.gg/aebSVBgzuG>)", inline=False)
            embed.add_field(name="봇 초대 링크", value=":link: [봇 초대하기](<https://discord.com/oauth2/authorize?client_id=782777035898617886&permissions=8&scope=bot>)", inline=False)
            await ctx.send(embed=embed)
        elif 종류 == '관리':
            embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 관리 명령어 도움말",  description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
            embed.add_field(name="/핑", value="봇의 핑을 알려줍니다.", inline=False)
            embed.add_field(name="/청소 `[n]`", value="메시지를 `[n]`의 값 만큼 삭제합니다. 메시지 관리 권한이 필요합니다.", inline=False)
            embed.add_field(name="/서버", value="서버 정보를 전송합니다.", inline=False)
            embed.add_field(name="/내정보", value="유저 정보를 전송합니다.", inline=False)
            await ctx.send(embed=embed)
        elif 종류 == '놀이':
            embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 놀이 명령어 도움말", description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
            embed.add_field(name="/가위바위보 `[가위, 바위, 보]`", value="봇과 가위바위보를 합니다. `/가위바위보 가위` 등의 형식으로 쓰면 됩니다.", inline=False)
            embed.add_field(name="/주사위 `[N]` `(n)`", value="주사위를 굴립니다. `[N]`만 쓰면 1부터 `[N]`까지의 숫자를, `(n)`까지 모두 쓰면 `[N]`부터 `(n)`까지의 숫자를 랜덤으로 표출합니다.", inline=False)
            embed.add_field(name="/룰렛 `[항목들]`", value="`[항목들]` 중에서 하나를 봇이 골라줍니다.", inline=False)
            await ctx.send(embed=embed)
        elif 종류 == '기타':
            embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 기타 명령어 도움말", description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
            embed.add_field(name="/검색 `[항목]`", value="여러 사이트에서 `[항목]`을 검색합니다.", inline=False)
            embed.add_field(name="/전송 `[항목]`", value="`[항목]`을 전송해요!", inline=False)
            embed.add_field(name="/암호 `[수신문]`", value="`[수신문]`을 암호화합니다.", inline=False)
            embed.add_field(name="/해독 `[암호문]`", value="`[암호문]`을 해독합니다.", inline=False)
            embed.add_field(name="/정보", value="봇의 정보를 전송합니다.", inline=False)
            embed.add_field(name="/유튜브", value="들어가 있는 음성 채널에 유튜브 투게더를 활성화 시키는 링크를 보냅니다. 음성 채널에 연결되어 있어야 사용 가능한 명령어입니다.", inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="WhiteBot 오류", description="도움말 기능", color=0xff0000)
            embed.add_field(name="오류 내용:", value="`관리, 놀이, 기타, (공백)` 중 하나를 입력해주세요.", inline=False)
            embed.add_field(name="새로운 명령어를 원하시나요?", value="[Team White 공식 서버](<https://discord.gg/aebSVBgzuG>)에서 의견을 내주세요!", inline=False)
            embed.add_field(name="잘못 들어오셨다고요?", value="`/도움` 으로 다른 명령어들을 알아보세요!", inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(manage(bot))
