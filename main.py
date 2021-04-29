import asyncio
import discord
import random
import re
import os, json
import datetime
from hostbot import keep_alive
from discord.ext import commands
from replit import db
try:
		from discord_slash import SlashContext, SlashCommand
except ImportError:
		os.system("pip install -U discord-py-slash-command")
import functools
import itertools
import math
import youtube_dl
from async_timeout import timeout
try:
        import pynacl
except:
        os.system("pip install pynacl")
try:
    import dbkrpy
except ImportError:
    os.system("pip install dbkrpy")
    import dbkrpy


bot = commands.Bot(command_prefix='/', help_command=None)
DBKR_token = os.getenv('DBKR_token')


dab = db["dab"]


def getdb():
    dab = db["dab"]


def savedb():
    db["dab"] = dab


getdb()
savedb()

dbkrpy.UpdateGuilds(bot,DBKR_token)

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("버전 1.3.1! 도움말이 대폭 개선되었어요 - 자세한건 /도움"))
    print("다음으로 로그인합니다 : ")
    print(bot.user.name)


@bot.command(aliases=['help', '도움말'])
async def 도움(ctx, 종류 = None):
    if (종류 == None):
        embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 명령어 도움말",
                          description="WhiteBot의 명령어에 대해서 소개합니다.",
                          color=0xFEFEFE)
        embed.add_field(name="/도움", value="이 메시지를 표출합니다.", inline=False)
        embed.add_field(name="/도움 관리", value="서버 관리와 관련된 명령어를 표출합니다.", inline=False)
        embed.add_field(name="/도움 놀이",
                    value="WhiteBot으로 할 수 있는 놀이 기능과 관련된 명령어를 표출합니다.",
                    inline=False)
        embed.add_field(name="/도움 경제",
                    value="WhiteBot의 경제 시스템과 관련된 명령어를 표출합니다.",
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
        ":link: [봇 초대하기](<https://discord.com/api/oauth2/authorize?client_id=819776362067656724&permissions=8&scope=bot%20applications.commands>)",
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
        name="/킥 `@서버원` `이유`",
        value="`@서버원`을 추방합니다. `이유`는 추방된 유저의 DM으로 발송됩니다. 관리자 권한이 필요합니다.",
        inline=False)
        embed.add_field(
        name="/밴",
        value="`@서버원`을 추방 및 차단합니다. `이유`는 차단된 유저의 DM으로 발송됩니다. 관리자 권한이 필요합니다.",
        inline=False)
        embed.add_field(name="/언밴",
                    value="`@서버원`의 추방을 해제합니다. 관리자 권한이 필요합니다.",
                    inline=False)
        await ctx.send(embed=embed)
    elif 종류 == '놀이':
        embed = discord.Embed(title="<a:check:824251178493411368> WhiteBot 놀이 명령어 도움말",
                          description="WhiteBot의 명령어에 대해서 소개합니다.",
                          color=0xFEFEFE)
        embed.add_field(name="/가위바위보 `(가위, 바위, 보)`",
                    value="봇과 가위바위보를 합니다. `/가위바위보 가위` 등의 형식으로 쓰면 됩니다.\n가위바위보에서 이기면 WhiteBot의 경제 시스템에서 쓸 수 있는 7500원을 얻어요!",
                    inline=False)
        embed.add_field(
        name="/주사위 `N` `n`",
        value=
        "주사위를 굴립니다. `N`만 쓰면 1부터 `N`까지의 숫자를, `n`까지 모두 쓰면 `N`부터 `n`까지의 숫자를 랜덤으로 표출합니다.",
        inline=False)
        await ctx.send(embed=embed)
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


@bot.command()
async def 핑(ctx):
    embed = discord.Embed(title=':ping_pong: 퐁!', color=0xFEFEFE)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name='Discord API Ping: ',
                    value=f'{round(bot.latency * 1000)} ms')
    await ctx.send(embed=embed)


@bot.command()
async def 청소(ctx, count: int):
    if ctx.author.guild_permissions.administrator:
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=count + 1)
        erasemsg = await ctx.send(f'`{count}`건의 메시지를 청소했습니다.')
        await asyncio.sleep(3)
        await erasemsg.delete()
    else:
        await ctx.send(
            f'{ctx.author.mention} 메시지 관리 권한이 필요합니다. 권한 확인 후 다시 실행해주세요.')


@bot.command()
async def 킥(ctx, member: discord.Member, *, reason):
    if ctx.author.guild_permissions.administrator:
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


@bot.command()
async def 밴(ctx, member: discord.Member, *, reason):
    if ctx.author.guild_permissions.administrator:
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


@bot.command()
async def 언밴(ctx, *, member):
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


@bot.command()
async def 가위바위보(ctx, user: str):
    rps_table = ['가위', '바위', '보']
    bot = random.choice(rps_table)
    result = rps_table.index(user) - rps_table.index(bot)
    if result == 0:
        await ctx.send(
            f'{user} vs {bot}\n{ctx.author.mention} 비겼네요! 다시 한판 하는건 어때요?')
    elif result == 1 or result == -2:
        await ctx.send(
            f'{user} vs {bot}\n{ctx.author.mention}님이 이겼어요! 절 이기시다니 대단해요!'
        )
        try:
            dab[str(ctx.author.id)]["money"] += 7500
            savedb()
            b = dab[str(ctx.author.id)]["money"]
            await ctx.send(f'가위바위보를 이겨 ' + str(7500) +
                           f'원을 얻었어요! 현재 가진 돈은 {str(b)}원이에요!')
        except KeyError:
            dab[str(ctx.author.id)] = {}
            dab[str(ctx.author.id)]["money"] = 7500
            savedb()
            b = dab[str(ctx.author.id)]["money"]
            await ctx.send(f'가위바위보를 이겨 ' + str(7500) +
                           f'원을 얻었어요! 현재 가진 돈은 {str(b)}원이에요!')
    else:
        await ctx.send(
            f'{user} vs {bot}\n{ctx.author.mention} 제가 이겼습니다! 한판 더 하실래요?')


@bot.command()
async def 검색(ctx, *, 검색어):
    embed = discord.Embed(title="<a:check:824251178493411368> 검색결과",
                          description="여러 사이트에서 검색한 결과입니다.",
                          color=0xfefefe)
    embed.add_field(name="구글 검색결과",
                    value=('https://www.google.com/search?q=' +
                           검색어.replace(" ", "%20")),
                    inline=False)
    embed.add_field(name="네이버 검색결과",
                    value=('https://search.naver.com/search.naver?query=' +
                           검색어.replace(" ", "%20")),
                    inline=False)
    embed.add_field(name="다음 검색결과",
                    value=('https://search.daum.net/search?w=tot&q=' +
                           검색어.replace(" ", "%20")),
                    inline=False)
    embed.add_field(name="위키백과 검색결과",
                    value=('https://ko.wikipedia.org/wiki/특수:검색/' +
                           검색어.replace(" ", "_")),
                    inline=False)
    embed.add_field(name="지식백과 검색결과",
                    value=('https://terms.naver.com/search.naver?query=' +
                           검색어.replace(" ", "_")),
                    inline=False)
    embed.add_field(name="나무위키 검색결과",
                    value=('https://namu.wiki/Search?q=' +
                           검색어.replace(" ", "%20")),
                    inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def 주사위(ctx, 첫번째숫자: int, 두번째숫자: int = None):
    if (두번째숫자):
        await ctx.send(
            f"{ctx.author.mention} 주사위를 굴렸더니 {random.randint(첫번째숫자, 두번째숫자)}(이)가 나왔어요!"
        )
    else:
        await ctx.send(
            f"{ctx.author.mention} 주사위를 굴렸더니 {random.randint(1, 첫번째숫자)}(이)가 나왔어요!"
        )


@bot.command()
async def 전송(ctx, *, 내용):
        await ctx.send(내용)


@bot.command(aliases=['뽑', 'ㅃ'])
async def 뽑기(ctx):
    random_coin = random.randint(1000, 5000)
    getdb()
    try:
        dab[str(ctx.author.id)]["money"] += random_coin
        savedb()
        b = dab[str(ctx.author.id)]["money"]
        await ctx.send(f'{ctx.author.mention} ' + str(random_coin) +
                       f'원을 얻었어요! 현재 가진 돈은 {str(b)}원이에요!')
    except KeyError:
        dab[str(ctx.author.id)] = {}
        dab[str(ctx.author.id)]["money"] = random_coin
        savedb()
        b = dab[str(ctx.author.id)]["money"]
        await ctx.send(f'{ctx.author.mention} ' + str(random_coin) +
                       f'원을 얻었어요! 현재 가진 돈은 {str(b)}원이에요!')


@bot.command(aliases=['ㄷㅂㄱ'])
async def 돈비교(ctx, 멤버1: discord.Member, 멤버2: discord.Member = None):
    getdb()
    if 멤버2 == None:
        멤버2 = ctx.author
    m1yn = 0
    m2yn = 0
    try:
        m1money = dab[str(멤버1.id)]["money"]
        m1yn = 1
        m2money = dab[str(멤버2.id)]["money"]
        m2yn = 1

        if (m1money > m2money):
            await ctx.send(
                f'{ctx.author.mention} {멤버1.name}#{멤버1.discriminator}님이 {멤버2.name}#{멤버2.discriminator}님보다 {m1money - m2money}원 더 많아요!'
            )
        elif (m1money < m2money):
            await ctx.send(
                f'{ctx.author.mention} {멤버2.name}#{멤버2.discriminator}님이 {멤버1.name}#{멤버1.discriminator}님보다 {m2money - m1money}원 더 많아요!'
            )
        else:
            await ctx.send(
                f'{ctx.author.mention} {멤버1.name}#{멤버1.discriminator}님과 {멤버2.name}#{멤버2.discriminator}님이 가지고 있는 돈이 똑같아요!'
            )
    except KeyError:
        if (m1yn):
            m1money = dab[str(멤버1.id)]["money"]
            dab[str(멤버2.id)] = {}
            dab[str(멤버2.id)]["money"] = 0
            m2money = dab[str(멤버2.id)]["money"]
        else:
            try:
                dab[str(멤버1.id)] = {}
                dab[str(멤버1.id)]["money"] = 0
                m1money = dab[str(멤버1.id)]["money"]
                m2money = dab[str(멤버2.id)]["money"]
            except KeyError:
                dab[str(멤버2.id)] = {}
                dab[str(멤버2.id)]["money"] = 0
                m2money = dab[str(멤버2.id)]["money"]
                if (m1money > m2money):
                    await ctx.send(
                        f'{ctx.author.mention} {멤버1.name}#{멤버1.discriminator}님이 {멤버2.name}#{멤버2.discriminator}님보다 {m1money - m2money}원 더 많아요!'
                    )
                elif (m1money < m2money):
                    await ctx.send(
                        f'{ctx.author.mention} {멤버2.name}#{멤버2.discriminator}님이 {멤버1.name}#{멤버1.discriminator}님보다 {m2money - m1money}원 더 많아요!'
                    )
                else:
                    await ctx.send(
                        f'{ctx.author.mention} {멤버1.name}#{멤버1.discriminator}님과 {멤버2.name}#{멤버2.discriminator}님이 가지고 있는 돈이 똑같아요!'
                    )
        dab[str(ctx.author.id)] = {}
        dab[str(ctx.author.id)]["money"] = 0
        savedb()
        if (m1money > m2money):
            await ctx.send(
                f'{ctx.author.mention} {멤버1.name}#{멤버1.discriminator}님이 {멤버2.name}#{멤버2.discriminator}님보다 {m1money - m2money}원 더 많아요!'
            )
        elif (m1money < m2money):
            await ctx.send(
                f'{ctx.author.mention} {멤버2.name}#{멤버2.discriminator}님이 {멤버1.name}#{멤버1.discriminator}님보다 {m2money - m1money}원 더 많아요!'
            )
        else:
            await ctx.send(
                f'{ctx.author.mention} {멤버1.name}#{멤버1.discriminator}님과 {멤버2.name}#{멤버2.discriminator}님이 가지고 있는 돈이 똑같아요!'
            )

@bot.command()
async def 압류(ctx, 멤버: discord.Member, 수량: int):
    adminid = [
        509990516570718208, 763422064794796042,
        770025636148150302
    ]
    getdb()
    if ctx.author.id in adminid:
        dab[str(멤버.id)]["money"] -= 수량
        savedb()
        z = dab[str(멤버.id)]["money"]
        await ctx.send(
            f"{ctx.author.mention} {멤버}의 재산 중 {수량}원을 압류하였습니다. 현재 {멤버}에게는 {z}원이 남았습니다.")
    else:
        await ctx.send('권한이 없습니다.')

@bot.command()
async def 지급(ctx, 멤버: discord.Member, 수량: int):
    adminid = [
        509990516570718208, 763422064794796042,
        770025636148150302
    ]
    getdb()
    if ctx.author.id in adminid:
        dab[str(멤버.id)]["money"] += 수량
        savedb()
        z = dab[str(멤버.id)]["money"]
        await ctx.send(
            f"{ctx.author.mention} {멤버}에게 {수량}원을 지급하였습니다. 현재 {멤버}에게는 {z}원이 남았습니다.")
    else:
        await ctx.send('권한이 없습니다.')

@bot.command()
async def 초기화(ctx, 멤버: discord.Member):
    adminid = [
        509990516570718208, 763422064794796042,
        770025636148150302
    ]
    getdb()
    if ctx.author.id in adminid:
        dab[str(멤버.id)]["money"] = 0
        savedb()
        z = dab[str(멤버.id)]["money"]
        await ctx.send(
            f"{ctx.author.mention} {멤버}의 재산을 모두 압류하였습니다. 현재 {멤버}에게는 {z}원이 남았습니다.")
    else:
        await ctx.send('권한이 없습니다.')

@bot.command(aliases=['ㄷㅂ'])
async def 도박(ctx, 걸돈: int, 늘릴_배수: int):
    last = 늘릴_배수 * 10
    try:
        if (걸돈 > dab[str(ctx.author.id)]["money"]):
            await ctx.send(f"{ctx.author.mention} 걸려는 돈이 가진 돈보다 많아요!")
            return
    except KeyError:
        await ctx.send(f"{ctx.author.mention} 걸려는 돈이 가진 돈보다 많아요!")
    if 늘릴_배수 < 2:
        await ctx.send(f"{ctx.author.mention} 최소한 2배여야죠! 설마 버그를 찾으려고 하신건가요?")
        return
    if 걸돈 < 999:
        await ctx.send(f"{ctx.author.mention} 1000원 이상만 걸 수 있어요!")
        return
    getdb()
    adminid = [
        509990516570718208,
        770025636148150302
    ]
    if ctx.author.id in adminid:
        dab[str(ctx.author.id)]["money"] -= 걸돈
        dab[str(ctx.author.id)]["money"] += 걸돈 * 늘릴_배수
        savedb()
        b = dab[str(ctx.author.id)]["money"]
        await ctx.send(
            f"{ctx.author.mention} 도박에 성공하여 {걸돈}원이 {걸돈 * 늘릴_배수}원으로 늘어났어요! 현재 가진 돈은 {b}원이에요!")
    elif 늘릴_배수 == 0:
        dab[str(ctx.author.id)]["money"] -= 걸돈
        dab[str(ctx.author.id)]["money"] += 걸돈 * 늘릴_배수
        savedb()
        b = dab[str(ctx.author.id)]["money"]
        await ctx.send(
            f"{ctx.author.mention} 건 돈 {걸돈}원이 모두 없어졌어요.. 현재 가진 돈은 {b}원이에요.")
    elif (random.randint(1, last) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
        dab[str(ctx.author.id)]["money"] -= 걸돈
        dab[str(ctx.author.id)]["money"] += 걸돈 * 늘릴_배수
        savedb()
        b = dab[str(ctx.author.id)]["money"]
        await ctx.send(
            f"{ctx.author.mention} 도박에 성공하여 {걸돈}원이 {걸돈 * 늘릴_배수}원으로 늘어났어요! 현재 가진 돈은 {b}원이에요!")
    else:
        dab[str(ctx.author.id)]["money"] -= 걸돈
        savedb()
        c = dab[str(ctx.author.id)]["money"]
        await ctx.send(
            f"{ctx.author.mention} 도박에서 돈을 따였어요... {걸돈}원이 모두 없어져서 현재 가진 돈은 {c}원이에요.")



@bot.command(aliases=['ㄷㅎㅇ'])
async def 돈확인(ctx, 멤버: discord.Member = None):
    if (멤버 == None):
        try:
            getdb()
            b = dab[str(ctx.author.id)]["money"]
            await ctx.send(f'{ctx.author.mention} 현재 가진 돈은 {str(b)}원이에요!')
        except KeyError:
            getdb()
            dab[str(ctx.author.id)] = {}
            dab[str(ctx.author.id)]["money"] = 0
            b = dab[str(ctx.author.id)]["money"]
            await ctx.send(f'{ctx.author.mention} 현재 가진 돈은 {str(b)}원이에요!')
    else:
        try:
            getdb()
            b = dab[str(멤버.id)]["money"]
            await ctx.send(f'{ctx.author.mention} {멤버.name}님이 현재 가진 돈은 {str(b)}원이에요!')
        except KeyError:
            getdb()
            dab[str(멤버.id)] = {}
            dab[str(멤버.id)]["money"] = 0
            b = dab[str(멤버.id)]["money"]
            await ctx.send(f'{ctx.author.mention} {멤버.name}님이 현재 가진 돈은 {str(b)}원이에요!')



youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.uploader}**의 **{0.title}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('요청하신 노래를 찾을 수가 없어요. `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('요청하신 `{}`을 찾을 수가 없어요.'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('요청하신 `{}`을 찾을 수가 없어요.'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('요청하신 `{}`을 찾을 수가 없어요.'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{}일'.format(days))
        if hours > 0:
            duration.append('{}시간'.format(hours))
        if minutes > 0:
            duration.append('{}분'.format(minutes))
        if seconds > 0:
            duration.append('{}초'.format(seconds))

        return ' '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='재생 중...',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='재생 시간', value=self.source.duration)
                 .add_field(name='요청자', value=self.requester.mention)
                 .add_field(name='영상 업로더', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[바로가기]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 5 seconds.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(5):  # 5 seconds
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('개인 메세지로는 사용할 수 없는 기능이에요! 서버에서 진행해주세요.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('에러 발생: {}'.format(str(error)))

    @commands.command(name='참가', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='정지')
    async def _stop(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('음성 채널에 연결되어있지 않습니다.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='진행', aliases=['playing'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='스킵')
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('재생 중인 곡이 없어요!')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('투표를 하시려면 `/스킵` 명령어를 사용해주세요!')
                await ctx.send('투표가 접수되었습니다! 현재 **{}/3** 표가 집계되었어요.'.format(total_votes))

        else:
            await ctx.send('이미 투표 하셨는걸요..?')

    @commands.command(name='재생목록')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('대기열이 비어있어요.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='{} 페이지 중에서 {} 페이지를 보고 계세요!'.format(pages, page)))
        await ctx.send(embed=embed)

    @commands.command(name='셔플')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('대기열이 비어있어요.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='삭제')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('대기열이 비어있어요.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='반복')
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('재생 중인 곡이 없어요!')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')
        await ctx.send('반복 여부를 변경하시려려면 한번 더 명령어를 입력해주세요!')

    @commands.command(name='재생')
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('오류 발생: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('대기열에 {}가 추가되었어요!'.format(str(source)))


    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('음성 채널에 연결해주세요!')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('봇이 이미 음성 채널에 연결되어있어요.')


bot.add_cog(Music(bot))

keep_alive()

bot.run(os.getenv("TOKEN"))
