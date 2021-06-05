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
os.system("pip install pynacl")

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
            erasemsg = await ctx.send(f'`{count}`건의 메시지를 청소했습니다.')
            await asyncio.sleep(3)
            await erasemsg.delete()
        else:
            await ctx.send(
                f'{ctx.author.mention} 메시지 관리 권한이 필요합니다. 권한 확인 후 다시 실행해주세요.')


    @commands.command()
    async def 킥(self, ctx, member: discord.Member, *, reason):
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


    @commands.command()
    async def 밴(self, ctx, member: discord.Member, *, reason):
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

def setup(bot):
    bot.add_cog(manage(bot))
