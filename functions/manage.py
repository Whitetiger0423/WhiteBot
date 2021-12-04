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
from discord.commands import slash_command

bot = commands.Bot(command_prefix='/', help_command=None)

class HelpDropdown(discord.ui.Select):
    def __init__(self):

        manageembed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 관리 명령어 도움말",  description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
        manageembed.add_field(name="/ping", value="봇의 핑을 알려줍니다.", inline=False)
        manageembed.add_field(name="/delete `[n]`", value="메시지를 `[n]`의 값 만큼 삭제합니다. 메시지 관리 권한이 필요합니다.", inline=False)
        manageembed.add_field(name="/server", value="서버 정보를 전송합니다.", inline=False)
        manageembed.add_field(name="/user", value="유저 정보를 전송합니다.", inline=False)

        playembed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 놀이 명령어 도움말", description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
        playembed.add_field(name="/rsp `[가위, 바위, 보]`", value="봇과 가위바위보를 합니다. `/가위바위보 가위` 등의 형식으로 쓰면 됩니다.", inline=False)
        playembed.add_field(name="/dice `[N]` `(n)`", value="주사위를 굴립니다. `[N]`만 쓰면 1부터 `[N]`까지의 숫자를, `(n)`까지 모두 쓰면 `[N]`부터 `(n)`까지의 숫자를 랜덤으로 표출합니다.", inline=False)
        playembed.add_field(name="/random `[항목들]`", value="`[항목들]` 중에서 하나를 봇이 골라줍니다.", inline=False)

        utilityembed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 유틸리티 명령어 도움말", description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
        utilityembed.add_field(name="/search `[항목]`", value="여러 사이트에서 `[항목]`을 검색합니다.", inline=False)
        utilityembed.add_field(name="/send `[항목]`", value="`[항목]`을 전송해요!", inline=False)
        utilityembed.add_field(name="/code `[수신문]`", value="`[수신문]`을 암호화합니다.", inline=False)
        utilityembed.add_field(name="/decode `[암호문]`", value="`[암호문]`을 해독합니다.", inline=False)
        utilityembed.add_field(name="/bot", value="봇의 정보를 전송합니다.", inline=False)
        utilityembed.add_field(name="/youtube", value="들어가 있는 음성 채널에 유튜브 투게더를 활성화 시키는 링크를 보냅니다. 음성 채널에 연결되어 있어야 사용 가능한 명령어입니다.", inline=False)

        options = [
            discord.SelectOption(
                label="관리", description="관리와 관련된 명령어들을 소개합니다.", value = f'{manageembed}'
            ),
            discord.SelectOption(
                label="놀이", description="혼자, 또는 같이 놀때 필요한 여러 편의기능들을 소개합니다.", value = f'{playembed}'
            ),
            discord.SelectOption(
                label="유틸리티", description="암호화, 유튜브 투게더 등 여러 유틸리티 기능들을 소개합니다.", value = f'{utilityembed}'
            ),
        ]

        super().__init__(
            placeholder="보고 싶은 명령어 도움말을 선택하세요!",
            min_values=1,
            max_values=1,
            options=options,
        )
        

    async def callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.send_message(
            f'{select.values[0]}'
        )

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(HelpDropdown())

class manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @slash_command(description='봇의 핑을 전송합니다.')
    async def ping(self, ctx):
        embed = discord.Embed(title=':ping_pong: 퐁!', color=0xffffff)
        embed.add_field(name='discord API Ping: ', value=f'{round(self.bot.latency * 1000)} ms')
        await ctx.respond(embed=embed)

    @slash_command(description='메시지를 일정 개수만큼 지웁니다.')
    async def delete(self, ctx, count: int):
        try:
            if ctx.author.guild_permissions.administrator:
                if count:
                    await asyncio.sleep(2)
                    await ctx.channel.purge(limit=count + 1)
                    embed=discord.Embed(title="청소 완료!", color=0xffffff)
                    embed.add_field(name="삭제한 메시지의 수:", value=f"{count}", inline=False)
                    erasemsg = await ctx.respond(embed=embed)
                    await asyncio.sleep(3)
                    await erasemsg.delete()
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

    @slash_command(description='서버 정보를 전송합니다.')
    async def server(self, ctx):
        embed = discord.Embed(title='서버 정보', color=0xffffff)
        embed.set_thumbnail(url=discord.guild.icon_url)
        embed.add_field(name='서버 이름: ', value=f'{discord.guild.name}', inline = False)
        embed.add_field(name='서버 ID: ', value=f'`{discord.guild.id}`', inline = False)
        embed.add_field(name='서버 지역: ', value=f'{discord.guild.region}', inline = False)
        embed.add_field(name='서버 부스트 레벨: ', value=f'{discord.guild.premium_tier}레벨', inline = False)
        embed.add_field(name='멤버 수: ', value=f'{discord.guild.member_count}', inline = False)
        await ctx.respond(embed=embed)

    @slash_command(description='유저의 정보를 전송합니다.')
    async def user(self, ctx):
        embed = discord.Embed(title='유저 정보', color=0xffffff)
        embed.set_thumbnail(url=discord.author.avatar_url)
        embed.add_field(name='계정명: ', value=f'{discord.author.name}', inline = False)
        embed.add_field(name='ID: ', value=f'`{discord.author.id}`', inline = False)
        embed.add_field(name='이 서버에서의 별명: ', value=f'{discord.author.display_name}', inline = False)
        embed.add_field(name='멘션: ', value=f'{discord.author.mention}', inline = False)
        await ctx.respond(embed=embed)

    @slash_command(description='봇의 정보를 전송합니다.')
    async def bot(self, ctx):
        ch = self.bot.guilds
        g = len(ch)
        embed = discord.Embed(title='봇 정보', color=0xffffff)
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/782777035898617886/d0ffaea389fce208e560cea5cf082d46.webp?size=1024')
        embed.add_field(name='봇 이름: ', value=f'{self.bot.user.name}', inline = False)
        embed.add_field(name='봇 ID: ', value=f'`{self.bot.user.id}`', inline = False)
        embed.add_field(name='봇 버전: ', value='1.3.9', inline = False)
        embed.add_field(name='봇 참가 서버 수: ', value=f'`{g}`개의 서버', inline = False)
        embed.add_field(name='봇 개발진: ', value='[Team White](<http://team-white.kro.kr/>)', inline = False)
        embed.add_field(name='서포팅 서버: ', value='[초대 링크](<http://server.whitebot.kro.kr/>)', inline = False)
        await ctx.respond(embed=embed)

    @slash_command(description='봇의 도움말을 전송합니다.')
    async def help(self, ctx):
        view = DropdownView()
        embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 명령어 도움말", description="WhiteBot의 명령어에 대해서 소개합니다.", color=0xffffff)
        embed.add_field(name="/help", value="이 메시지를 표출합니다.", inline=False)
        embed.add_field(name="공식 홈페이지", value=":link: [공식 홈페이지](<http://team-white.kro.kr/>)", inline=False)
        embed.add_field(name="공식 서포팅 서버", value=":link: [Team White 공식 서버](<https://discord.gg/aebSVBgzuG>)", inline=False)
        embed.add_field(name="봇 초대 링크", value=":link: [봇 초대하기](<https://discord.com/oauth2/authorize?client_id=782777035898617886&permissions=8&scope=bot>)", inline=False)
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(manage(bot))
