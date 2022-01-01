import discord
import os
import requests
from requests.utils import quote
import re
from discord.ext import commands
from discord.commands import slash_command, ApplicationContext, Option, OptionChoice

PAPAGO_URL = "https://openapi.naver.com/v1/papago/n2mt"
REGEX = re.compile(".+ \\((.+)\\)")


class translate(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Naver-Client-Id": os.getenv("PAPAGO_APPID"),
            "X-Naver-Client-Secret": os.getenv("PAPAGO_SECRET")
        }

    @slash_command(description='입력한 내용을 한글에서 영어로 번역합니다. 파파고 API를 사용합니다.')
    async def translate(
        self,
        ctx: ApplicationContext,
        lang: Option(str, "어느 언어에서 어느 언어로 변역할지 결정합니다", choices=[
            OptionChoice("한국어 -> 영어", "en:ko"),
            OptionChoice("영어 -> 한국어", "ko:en"),
            OptionChoice("한국어 -> 일본어", "ko:ja"),
            OptionChoice("일본어 -> 한국어", "ja:ko"),
            OptionChoice("한국어 -> 중국어", "ko:zh-CN"),
            OptionChoice("중국어 -> 한국어", "zh-CN:ko")
        ]),
        text: str
    ):
        src_lang, tar_lang = lang.split(':')
        data = f"source={src_lang}&target={tar_lang}&text={quote(text)}"

        res = requests.post(PAPAGO_URL, data=data, headers=self.header)
        body = res.json()

        if res.status_code == 200:
            result = body['message']['result']
            embed = discord.Embed(title="<a:check:837221276065464370> 번역 완료",
                                  description=result['translatedText'],
                                  color=0x00ffc6) \
                .set_footer(text=f"Papago API: {result['srcLangType']} -> {result['tarLangType']}")
        elif res.status_code == 500:
            print("Papago API has returned 500(Internal Server Error)")
            print("Request:", res.request.method, res.request.url, res.request.headers)
            print("Response:", res.text)
            embed = discord.Embed(title="오류 발생",
                                  description="파파고 내부 서버에서 오류가 발생했어요. 잠시 후에 다시 시도해주세요",
                                  color=0xff0000)
        else:
            err_msg = REGEX.match(body['errorMessage']).group(1)
            embed = discord.Embed(title="오류 발생",
                                  description=err_msg,
                                  color=0xff0000)
        await ctx.respond(embed=embed)


def setup(bot: discord.Bot):
    bot.add_cog(translate(bot))
