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
import youtube_dl
from async_timeout import timeout

bot = commands.Bot(command_prefix='/', help_command=None)

class manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 핑(self, ctx):
        embed = discord.Embed(title=':ping_pong: 퐁!', color=0xFEFEFE)
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/782777035898617886/d16ab665b8db020f4b62313cb260b2f1.webp?size=1024')
        embed.add_field(name='Discord API Ping: ',
                    value=f'{round(self.bot.latency * 1000)} ms')
        await ctx.send(embed=embed)


    @commands.command()
    async def 청소(self, ctx, count: int):
        if ctx.author.guild_permissions.administrator:
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=count + 1)
            embed=discord.Embed(title="청소 완료!", color=0xffffff)
            embed.add_field(name="삭제한 메시지의 수:", value="{count}", inline=False)
            erasemsg = await ctx.send(embed=embed)
            await asyncio.sleep(3)
            await erasemsg.delete()
        else:
            embed=discord.Embed(title="오류 발생!", color=0xffffff)
            embed.add_field(name="메시지 관리 권한이 필요합니다.", value="권한 확인 후 다시 시도해주세요.", inline=False)
            await ctx.send(embed=embed)


    @commands.command()
    async def 킥(self, ctx, member: discord.Member, *, reason = None):
        if ctx.author.guild_permissions.administrator:
            if reason == None:
                reason = 'None'
            if not member.guild_permissions.administrator:
                await ctx.send(
                    f'{member.name}#{member.discriminator} 서버원을 추방하였습니다.')
                await member.send(
                    f"{ctx.message.guild.name} 서버에서 추방당했습니다! 이유는 다음과 같습니다: ```{reason}``` 서버에 다시 참가할 수 있습니다! \n {await ctx.message.guild.invites()[0]}"
                )
                await member.kick(reason=reason)
            else:
                await ctx.send(
                    f'{ctx.author.mention} 관리자는 추방할 수 없습니다. 관리자 권한을 해제하고 다시 시도해주세요.'
                )
        else:
            await ctx.send(
                f'{ctx.author.mention} 관리자 권한이 필요합니다. 권한 확인 후 다시 실행해주세요.')


    @commands.command()
    async def 밴(self, ctx, member: discord.Member, *, reason = None):
        if ctx.author.guild_permissions.administrator:
            if reason == None:
                reason = 'None'
            if not member.guild_permissions.administrator:
                await ctx.send(f'{member.name}#{member.discriminator} 서버원을 밴했습니다.')
                await member.send(
                f"{ctx.message.guild.name} 서버에서 차단당했습니다! 이유는 다음과 같습니다: ```{reason}``` 차단이 풀리기 전까지 서버에 다시 참가할 수 없습니다!"
            )
                await member.ban(reason=reason)
            else:
                await ctx.send(
                    f'{ctx.author.mention} 관리자는 밴할 수 없습니다. 관리자 권한을 해제하고 다시 시도해주세요.'
            )
        else:
            await ctx.send(
                f'{ctx.author.mention} 관리자 권한이 필요합니다. 권한 확인 후 다시 실행해주세요.')


    @commands.command()
    async def 언밴(self, ctx, *, member):
        if ctx.author.guild_permissions.administrator:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name,
                                                   member_discriminator):
                    await ctx.send('서버원을 언밴했습니다. 이 서버에 다시 들어올 수 있습니다.')
                    await ctx.guild.unban(user)
        else:
            await ctx.send(
                f'{ctx.author.mention} 관리자 권한이 필요합니다. 권한 확인 후 다시 실행해주세요.')

    @commands.command()
    async def 서버(self, ctx):
        embed = discord.Embed(title='서버 정보', color=0xFEFEFE)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='서버 이름: ',
                    value=f'{ctx.guild.name}', inline = False)
        embed.add_field(name='서버 ID: ',
                    value=f'{ctx.guild.id}', inline = False)
        embed.add_field(name='서버 지역: ',
                    value=f'{ctx.guild.region}', inline = False)
        embed.add_field(name='서버 부스트 레벨: ',
                    value=f'{ctx.guild.premium_tier}레벨', inline = False)
        embed.add_field(name='멤버 수: ',
                    value=f'{ctx.guild.member_count}', inline = False)
        await ctx.send(embed=embed)

    @commands.command()
    async def 내정보(self, ctx):
        embed = discord.Embed(title='유저 정보', color=0xFEFEFE)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name='계정명: ',
                    value=f'{ctx.author.name}', inline = False)
        embed.add_field(name='ID: ',
                    value=f'{ctx.author.id}', inline = False)
        embed.add_field(name='이 서버에서의 별명: ',
                    value=f'{ctx.author.display_name}', inline = False)
        embed.add_field(name='멘션: ',
                    value=f'{ctx.author.mention}', inline = False)
        await ctx.send(embed=embed)

    @commands.command(name="announce")
    async def announce(self, ctx, *, 내용):
        adminid = [763422064794796042]
        if ctx.author.id in adminid:
            now = datetime.datetime.now()
            time = f"{str(now.year)}년 {str(now.month)}월 {str(now.day)}일 {str(now.hour)}시 {str(now.minute)}분 {str(now.second)}초"
            embed = discord.Embed(color=0x00FFFF)
            embed = discord.Embed(title=":loudspeaker: WhiteBot 공지",
                              description=" ",
                              colour=0x00ff00,
                              inline=False)
            embed.add_field(name='공지 내용', value=f'{내용}')
            embed.set_footer(text=f"{str(ctx.author)} - 인증됨\n발송 시간 : {time}",
                         icon_url=ctx.author.avatar_url)
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

    @commands.command(name="정보")
    async def 정보(self, ctx):
        ch = self.bot.guilds
        g = len(ch)
        embed = discord.Embed(title='봇 정보', color=0xFEFEFE)
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/782777035898617886/d16ab665b8db020f4b62313cb260b2f1.webp?size=1024')
        embed.add_field(name='봇 이름: ',
                    value=f'{self.bot.user.name}', inline = False)
        embed.add_field(name='봇 ID: ',
                    value=f'{self.bot.user.id}', inline = False)
        embed.add_field(name='봇 버전: ',
                    value='1.3.3', inline = False)
        embed.add_field(name='봇 참가 서버 수: ',
                    value=f'{g}개의 서버', inline = False)
        embed.add_field(name='봇 개발진: ',
                    value='[White_team](<http://whiteteam.kro.kr/>)', inline = False)
        embed.add_field(name='서포팅 서버: ',
                    value='[초대 링크](<http://server.whitebot.kro.kr/>)', inline = False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['help', '도움말'])
    async def 도움(self, ctx, 종류 = None):
        if (종류 == None):
            embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 명령어 도움말",
                          description="WhiteBot의 명령어에 대해서 소개합니다.",
                          color=0xFEFEFE)
            embed.add_field(name="/도움", value="이 메시지를 표출합니다.", inline=False)
            embed.add_field(name="/도움 관리", value="서버 관리와 관련된 명령어를 표출합니다.", inline=False)
            embed.add_field(name="/도움 놀이",
                    value="WhiteBot으로 할 수 있는 놀이 기능과 관련된 명령어를 표출합니다.",
                    inline=False)
            embed.add_field(name="/도움 음악",
                    value="음악 기능과 관련된 명령어를 표출합니다.",
                    inline=False)
            embed.add_field(name="/도움 기타",
                    value="기타 다른 명령어를 표출합니다.",
                    inline=False)
            embed.add_field(name="공식 홈페이지",
                    value=":link: [공식 홈페이지](<http://whiteteam.kro.kr/>)",
                    inline=False)
            embed.add_field(
            name="공식 서포팅 서버",
            value=":link: [White_team 공식 서버](<https://discord.gg/aebSVBgzuG>)",
            inline=False)
            embed.add_field(
            name="봇 초대 링크",
            value=
            ":link: [봇 초대하기](<https://discord.com/oauth2/authorize?client_id=782777035898617886&permissions=8&scope=bot>)",
            inline=False)
            await ctx.send(embed=embed)
        elif 종류 == '관리':
            embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 관리 명령어 도움말",
                          description="WhiteBot의 명령어에 대해서 소개합니다.",
                          color=0xFEFEFE)
            embed.add_field(name="/핑", value="핑을 알려줍니다.", inline=False)
            embed.add_field(name="/청소 `n`",
                    value="메시지를 `n`의 값 만큼 삭제합니다. 메시지 관리 권한이 필요합니다.",
                    inline=False)
            embed.add_field(
            name="/킥 (@서버원) [이유]",
            value="`@서버원`을 추방합니다. `이유`는 추방된 유저의 DM으로 발송됩니다. 관리자 권한이 필요합니다.",
            inline=False)
            embed.add_field(
            name="/밴 (@서버원) [이유]",
            value="`@서버원`을 추방 및 차단합니다. `이유`는 차단된 유저의 DM으로 발송됩니다. 관리자 권한이 필요합니다.",
            inline=False)
            embed.add_field(name="/언밴 (@서버원)",
                    value="`@서버원`의 추방을 해제합니다. 관리자 권한이 필요합니다.",
                    inline=False)
            await ctx.send(embed=embed)
        elif 종류 == '놀이':
            embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 놀이 명령어 도움말",
                          description="WhiteBot의 명령어에 대해서 소개합니다.",
                          color=0xFEFEFE)
            embed.add_field(name="/가위바위보 `(가위, 바위, 보)`",
                    value="봇과 가위바위보를 합니다. `/가위바위보 가위` 등의 형식으로 쓰면 됩니다.",
                    inline=False)
            embed.add_field(
            name="/주사위 (N) [n]",
            value=
            "주사위를 굴립니다. `N`만 쓰면 1부터 `N`까지의 숫자를, `n`까지 모두 쓰면 `N`부터 `n`까지의 숫자를 랜덤으로 표출합니다.",
            inline=False)
            await ctx.send(embed=embed)
            '''
        elif 종류 == '경제':
            embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 경제 명령어 도움말",
                          description="WhiteBot의 명령어에 대해서 소개합니다.",
                          color=0xFEFEFE)
            embed.add_field(name="/뽑기 (/뽑, /ㅃ)",
                    value="1000원에서 5000원 사이의 돈을 무작위로 얻습니다.",
                    inline=False)
            embed.add_field(name="/돈확인 [멤버] (/ㄷㅎㅇ [멤버])",
                    value="자신의 돈이나 [멤버]의 돈을 확인합니다.",
                    inline=False)
            embed.add_field(name="/돈비교 (멤버1) [멤버2] (/ㄷㅂㄱ (멤버1) [멤버2])",
                    value="자신의 돈과 (멤버1)의 돈을 비교하거나, (멤버1)과 [멤버2]의 돈을 비교합니다.",
                    inline=False)
            embed.add_field(name="/도박 (걸돈) (늘릴 배수) (/ㄷㅂ (걸돈) (늘릴 배수)",
                    value="(걸돈)만큼을 도박에 겁니다. 만약 성공한다면 (늘릴 배수)만큼 돈이 늡니다! 하지만 실패할 경우엔 건 돈이 모두 없어집니다. 1000원 이상만 걸 수 있습니다.",
                    inline=False)
            await ctx.send(embed=embed)
            '''
        elif 종류 == '음악':
            embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 음악 명령어 도움말",
                          description="WhiteBot의 명령어에 대해서 소개합니다.",
                          color=0xFEFEFE)
            embed.add_field(name="/참가",
                    value="봇을 음성채널에 참가시킵니다.",
                    inline=False)
            embed.add_field(name="/재생 (제목)",
                    value="노래를 재생합니다.",
                    inline=False)
            embed.add_field(name="/진행",
                    value="재생중인 곡을 표시합니다.",
                    inline=False)
            embed.add_field(name="/재생목록",
                    value="대기열을 표시합니다.",
                    inline=False)
            embed.add_field(name="/셔플",
                    value="대기열의 순서와 상관 없이 랜덤으로 음악을 플레이 합니다.",
                    inline=False)
            embed.add_field(name="/삭제 (N)",
                    value="대기열의 N번 곡을 대기열에서 지웁니다.",
                    inline=False)
            embed.add_field(name="/반복",
                    value="나오고 있는 곡을 반복해서 재생합니다.",
                    inline=False)
            embed.add_field(name="/스킵",
                    value="노래를 건너뜁니다. 만약 나오고 있는 노래가 스킵 명령어를 쓴 사람이 재생한 노래가 아니라면 투표를 통해 건너뛰어집니다.",
                    inline=False)
            embed.add_field(name="/방출",
                    value="음성채널에서 봇을 방출시킵니다.",
                    inline=False)
            await ctx.send(embed=embed)
        elif 종류 == '기타':
            embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 기타 명령어 도움말",
                          description="WhiteBot의 명령어에 대해서 소개합니다.",
                          color=0xFEFEFE)
            embed.add_field(name="/검색 (항목)",
                    value="여러 사이트에서 (항목)을 검색합니다.",
                    inline=False)
            embed.add_field(name="/전송 (항목)", value="(항목)을 전송해요!", inline=False)
            embed.add_field(name="/암호 (수신문)", value="(수신문)을 암호화합니다.", inline=False)
            embed.add_field(name="/해독 (암호문)", value="(암호문)을 해독합니다.", inline=False)
            embed.add_field(name="/서버", value="서버 정보를 전송합니다.", inline=False)
            embed.add_field(name="/내정보", value="유저 정보를 전송합니다.", inline=False)
            embed.add_field(name="/정보", value="봇의 정보를 전송합니다.", inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 명령어 도움말 오류",
                          description="무슨 명령어가 궁금하신가요?",
                          color=0xFEFEFE)
            embed.add_field(name="새로운 명령어를 원하시나요?",
                    value="[White_team 공식 서버](<https://discord.gg/aebSVBgzuG>)에서 의견을 내주세요!",
                    inline=False)
            embed.add_field(name="잘못 들어오셨다고요?", value="`/도움` 으로 다른 명령어들을 알아보세요!", inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(manage(bot))
