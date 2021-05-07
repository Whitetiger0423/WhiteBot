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
        770025636148150302, 674569768811888641
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
        770025636148150302, 674569768811888641
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
        770025636148150302, 674569768811888641
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
    if (random.randint(1, last) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
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
