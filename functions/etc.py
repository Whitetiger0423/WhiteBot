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
import aiohttp
import aiofiles
import aiosqlite
import pickle
import main
from urllib import parse
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option
import base64
import requests
import datetime
from datetime import date, datetime, timedelta




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
    async def code(self, ctx, type: Option(str, "암호화 시킬 방식을 선택하세요", choices=["base16", "base32", "base64", "base85", "아스키 코드"]), text: Option(str, "암호화 시킬 문장을 입력하세요.")):
        if type == "base16":
            string_bytes = text.encode("utf-8")
            base16_bytes = base64.b16encode(string_bytes) 
            data = base16_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base16**을 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**원문:**", value=f"```{text}```", inline=False)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base32":
            string_bytes = text.encode("utf-8")
            base32_bytes = base64.b32encode(string_bytes) 
            data = base32_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base32**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**원문:**", value=f"```{text}```", inline=False)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base64":
            string_bytes = text.encode("utf-8")
            base64_bytes = base64.b64encode(string_bytes) 
            data = base64_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base64**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**원문:**", value=f"```{text}```", inline=False)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base85":
            string_bytes = text.encode("utf-8")
            base85_bytes = base64.b85encode(string_bytes) 
            data = base85_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base85**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**원문:**", value=f"```{text}```", inline=False)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)
        elif type == "아스키 코드":
            data = encrypt(text)
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**아스키 코드**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**원문:**", value=f"```{text}```", inline=False)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(description='수신문을 해독합니다.')
    async def decode(self, ctx, type: Option(str, "해독할 암호문의 암호화 방식을 선택하세요", choices=["base16", "base32", "base64", "base85", "아스키 코드"]), text: Option(str, "해독할 암호문을 입력하세요.")):
        if type == "base16":
            try:
                string_bytes = text.encode("utf-8")
                base16_bytes = base64.b16decode(string_bytes) 
                data = base16_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base16**을 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**암호문:**", value=f"```{text}```", inline=False)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base32":
            try:
                string_bytes = text.encode("utf-8")
                base32_bytes = base64.b32decode(string_bytes) 
                data = base32_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base32**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**암호문:**", value=f"```{text}```", inline=False)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base64":
            try:
                string_bytes = text.encode("utf-8")
                base64_bytes = base64.b64decode(string_bytes) 
                data = base64_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base64**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**암호문:**", value=f"```{text}```", inline=False)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base85":
            try:
                string_bytes = text.encode("utf-8")
                base85_bytes = base64.b85decode(string_bytes) 
                data = base85_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base85**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**암호문:**", value=f"```{text}```", inline=False)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
        elif type == "아스키 코드":
            data = decrypt(text)
            try:
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**아스키 코드**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**암호문:**", value=f"```{text}```", inline=False)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(description='검색어를 검색합니다.')
    async def search(self, ctx, *, searching: Option(str, "검색할 문장을 입력하세요.")):
        google = 'https://www.google.com/search?q=' + parse.quote(searching)
        naver = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' + parse.quote(searching)
        daum = 'https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&q=' + parse.quote(searching)
        wikipedia = 'https://ko.wikipedia.org/wiki/' + parse.quote(searching)
        termsnaver = 'https://terms.naver.com/search.naver?query=' + parse.quote(searching)
        namu = 'https://namu.wiki/Search?q=' + parse.quote(searching)
        embed = discord.Embed(title="<a:check:824251178493411368> 검색결과", description=f"`{searching}`의 검색 결과입니다.", color=0xffffff)
        embed.add_field(name="포털 사이트 검색 결과", value=(f'[**구글**]({google})\n[**네이버**]({naver})\n[다음]({daum})\n[지식백과]({termsnaver})'), inline=False)
        embed.add_field(name="위키 사이트 검색 결과",  value=(f'[**위키백과**]({wikipedia})\n[**나무위키**]({namu})'), inline=False)
        await ctx.respond(embed=embed)

    @slash_command(description='내용을 전송합니다.')
    async def send(self, ctx, *, text: Option(str, "전송할 내용을 입력하세요. 줄바꿈은 적용되지 않습니다.")):
        embed = discord.Embed(title=f"Sent by {ctx.author.display_name}", description=f"{text}", color=0xffffff)
        await ctx.respond(embed=embed)

    @slash_command(description='현재 날씨를 조회합니다.')
    async def weather(self, ctx, place: Option(str, "날씨를 조회할 장소를 선택해주세요.", choices=["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"])):
        px, py = 0
        if place == "서울":
            px = 60
            py = 127
        elif place == "부산":
            px = 98
            py = 76
        elif place == "대구":
            px = 89
            py = 90
        elif place == "인천":
            px = 55
            py = 124
        elif place == "광주":
            px = 58
            py = 74
        elif place == "대전":
            px = 67
            py = 100
        elif place == "울산":
            px = 102
            py = 84
        elif place == "세종":
            px = 66
            py = 103
        elif place == "경기":
            px = 60
            py = 120
        elif place == "강원":
            px = 73
            py = 134
        elif place == "충북":
            px = 69
            py = 107
        elif place == "충남":
            px = 68
            py = 100
        elif place == "전북":
            px = 63
            py = 89
        elif place == "전남":
            px = 51
            py = 67
        elif place == "경북":
            px = 89
            py = 91
        elif place == "경남":
            px = 91
            py = 77
        elif place == "제주":
            px = 52
            py = 38

        t = datetime.today()
        t_d = t.strftime("%Y%m%d")
        y = date.today() - timedelta(days=1)
        y_d = y.strftime("%Y%m%d")
        now = datetime.now()

        base_date, base_time = "0"
        if now.hour<2 or (now.hour==2 and now.minute<=10):
            base_date=y_d 
            base_time="2300"
        elif now.hour<5 or (now.hour==5 and now.minute<=10): 
            base_date=t_d
            base_time="0200"
        elif now.hour<8 or (now.hour==8 and now.minute<=10):
            base_date=t_d
            base_time="0500"
        elif now.hour<=11 or now.minute<=10:
            base_date=t_d
            base_time="0800"
        elif now.hour<14 or (now.hour==14 and now.minute<=10): 
            base_date=t_d
            base_time="1100"
        elif now.hour<17 or (now.hour==17 and now.minute<=10):
            base_date=t_d
            base_time="1400"
        elif now.hour<20 or (now.hour==20 and now.minute<=10):
            base_date=t_d
            base_time="1700" 
        elif now.hour<23 or (now.hour==23 and now.minute<=10):
            base_date=t_d
            base_time="2000"
        else: 
            base_date=t_d
            base_time="2300"
        
        payload = "serviceKey=" + "4yqCoXlfJ9i35%2Fn69zg7LQjUfnOJzHRSthsdNyJWACmg2TK8QRlmwe%2FlcamLJiCJ%2FiXEB4dxQ9KjDF2iwJyK7g%3D%3D" + "&" +\
            "dataType=json" + "&" +\
            "base_date=" + base_date + "&" +\
            "base_time=" + base_time + "&" +\
            "nx=" + px + "&" +\
            "ny=" + py

        result = requests.get("http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?" + payload)

        items = result.json().get('response').get('body').get('items')

        data = dict()
        data['date'] = base_date

        weather_data = dict()
        for item in items['item']:
            if item['category'] == 'T3H':
                weather_data['tmp'] = item['fcstValue']
            
            if item['category'] == 'PTY':
                weather_code = item['fcstValue']
                weather_state = ''

                if weather_code == '1':
                    weather_state = '비 내림'
                elif weather_code == '2':
                    weather_state = '진눈깨비 내림'
                elif weather_code == '3':
                    weather_state = '눈 내림'
                elif weather_code == '4':
                    weather_state = '소나기 내림'
                else:
                    weather_state = '내리지 않음'

                weather_data['code'] = weather_code
                weather_data['state'] = weather_state

        data['weather'] = weather_data
        
        embed = discord.Embed(title=f"현재 날씨 정보", description=f"현재 날씨 정보를 조회했습니다.", color=0xffffff)
        embed.add_field(name="기온", value=f"{data['weather']['tmp']}℃", inline=False)
        embed.add_field(name="날씨", value=data['weather']['state'], inline=True)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(etc(bot))
