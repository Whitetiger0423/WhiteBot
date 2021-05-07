import asyncio
import discord
import random
import re
import os, json
import datetime
from discord.ext import commands
from replit import db
import functools
import itertools
import math
import youtube_dl
from async_timeout import timeout
try:
        import pynacl
except:
        os.system("pip install pynacl")

bot = commands.Bot(command_prefix='/', help_command=None)

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
async def 서버(ctx):
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