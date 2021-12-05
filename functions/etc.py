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
import os
import aiohttp
import aiofiles
import aiosqlite
import pickle
import main
from discord.ext import commands
from discord.commands import slash_command


bot = commands.Bot(command_prefix='/', help_command=None)

def encrypt(plain: str):
    parsed: list = list(plain)
    encrypted: list = [str(ord(x)) for x in parsed]
    return ' '.join(encrypted).strip()

def decrypt(encrypted: str):
    parsed: list = [int(x) for x in encrypted.split(' ')]
    decrypted: list = [chr(x) for x in parsed]
    return ''.join(decrypted)

class etc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='수신문을 암호화합니다.')
    async def code(self, ctx, text):
        data = encrypt(text)
        embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="아스키 코드를 기반으로 한 암호문입니다.\n해독할 때 띄어쓰기는 인식되지 않으니 `_`나 `-`등의 문자를 넣는것을 추천해요!", color=0xffffff)
        embed.add_field(name="**원문:**", value=f"```{text}```", inline=False)
        embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
        await ctx.respond(embed=embed)

    @slash_command(description='수신문을 해독합니다.')
    async def decode(self, ctx, text):
        data = decrypt(text)
        try:
            embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="아스키 코드를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
            embed.add_field(name="**암호문:**", value=f"```{text}```", inline=False)
            embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed)
        except:
            await ctx.respond('올바른 암호문을 입력해주세요.')

    @slash_command(description='검색어를 검색합니다.')
    async def search(self, ctx, *, 검색어):
        google = 'https://www.google.com/search?q=' + 검색어.replace(' ', '%20')
        naver = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' + 검색어.replace(' ', '%20')
        daum = 'https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&q=' + 검색어.replace(' ', '%20')
        wikipedia = 'https://ko.wikipedia.org/wiki/' + 검색어.replace(' ', '_')
        termsnaver = 'https://terms.naver.com/search.naver?query=' + 검색어.replace(" ", "%20")
        namu = 'https://namu.wiki/Search?q=' + 검색어.replace(" ", "%20")
        embed = discord.Embed(title="<a:check:824251178493411368> 검색결과", description=f"`{검색어}`의 검색 결과입니다.", color=0xffffff)
        embed.add_field(name="포털 사이트 검색 결과", value=(f'[**구글**]({google})\n[**네이버**]({naver})\n[다음]({daum})\n[지식백과]({termsnaver})'), inline=False)
        embed.add_field(name="위키 사이트 검색 결과",  value=(f'[**위키백과**]({wikipedia})\n[**나무위키**]({namu})'), inline=False)
        await ctx.respond(embed=embed)

    @slash_command(description='내용을 전송합니다.')
    async def send(self, ctx, *, 내용):
        embed = discord.Embed(title=f"Sent by {ctx.author.display_name}", description=f"{내용}", color=0xffffff)
        await ctx.respond(embed=embed)

    @slash_command(description='WhiteBot 시스템에 가입합니다.')
    async def register(self, ctx):
        aiocursor = await main.aiodb.execute("select * from user where id=?", (ctx.author.id,))
        dbdata = await aiocursor.fetchall()
        await aiocursor.close()
        if str(dbdata) == '[]':
            insertdb = True
        else:
            insertdb = False
        if insertdb:
            aiocursor = await main.aiodb.execute("insert into user (id, tos) values (?, ?)", (ctx.author.id, "True"))
            await main.aiodb.commit()
            await aiocursor.close()
            await ctx.respond(embed=discord.Embed(title="가입 완료", description=f"{ctx.author.mention}\n가입이 완료됐습니다. 이제 봇의 모든 명령어를 사용하실 수 있습니다.", color=0xffffff))
            return
        else:
            aiocursor = await main.aiodb.execute("UPDATE user SET tos = ? WHERE id=?", ("True", ctx.author.id))
            await main.aiodb.commit()
            await aiocursor.close()
            await ctx.respond(embed=discord.Embed(title="가입 완료", description=f"{ctx.author.mention}\n가입이 완료됐습니다. 이제 봇의 모든 명령어를 사용하실 수 있습니다.", color=0xffffff))
            return

def setup(bot):
    bot.add_cog(etc(bot))
