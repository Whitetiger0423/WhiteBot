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
from discord.commands import Option
import base64


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
    async def code(self, ctx, type: Option(str, "암호화 시킬 방식을 선택하세요", choices=["base16", "base32", "base64", "base85" "아스키 코드"]), text):
        if type == "base16":
            string_bytes = text.encode("utf-8")
            base16_bytes = base64.b16encode(string_bytes) 
            data = base16_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base16**을 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed)
        elif type == "base32":
            string_bytes = text.encode("utf-8")
            base32_bytes = base64.b32encode(string_bytes) 
            data = base32_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base32**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed)
        elif type == "base64":
            string_bytes = text.encode("utf-8")
            base64_bytes = base64.b64encode(string_bytes) 
            data = base64_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base64**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed)
        elif type == "base85":
            string_bytes = text.encode("utf-8")
            base85_bytes = base64.b85encode(string_bytes) 
            data = base85_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base85**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed)
        elif type == "아스키 코드":
            data = encrypt(text)
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**아스키 코드**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed)

    @slash_command(description='수신문을 해독합니다.')
    async def decode(self, ctx, type: Option(str, "해독할 암호문의 암호화 방식을 선택하세요", choices=["base16", "base32", "base64", "base85", "아스키 코드"]), text):
        if type == "base16":
            try:
                string_bytes = text.encode("utf-8")
                base16_bytes = base64.b16decode(string_bytes) 
                data = base16_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base16**을 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed)
        elif type == "base32":
            try:
                string_bytes = text.encode("utf-8")
                base32_bytes = base64.b32decode(string_bytes) 
                data = base32_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base32**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed)
        elif type == "base64":
            try:
                string_bytes = text.encode("utf-8")
                base64_bytes = base64.b64decode(string_bytes) 
                data = base64_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base64**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed)
        elif type == "base85":
            try:
                string_bytes = text.encode("utf-8")
                base85_bytes = base64.b85decode(string_bytes) 
                data = base85_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base85**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed)
        elif type == "아스키 코드":
            data = decrypt(text)
            try:
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**아스키 코드**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**해독문:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed)

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

def setup(bot):
    bot.add_cog(etc(bot))
