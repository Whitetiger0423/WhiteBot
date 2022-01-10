import asyncio
import discord
import os
import requests
from requests.utils import quote
from datetime import datetime, timedelta
import re
import json
import logging
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option, OptionChoice

PAPAGO_URL = "https://openapi.naver.com/v1/papago/n2mt"
GOOGLE_URL = "https://translation.googleapis.com/language/translate/v2"
REGEX = re.compile(".+ \\((.+)\\)")

logger = logging.getLogger("translate")

class translate(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.papago_id = os.getenv("PAPAGO_APPID")
        self.papago_secret = os.getenv("PAPAGO_SECRET")
        self.google_secret = os.getenv("GOOGLE_SECRET")

        self.is_papago_limited = False

        tomorrow = datetime.today() + timedelta(days=1)
        now = datetime.now()

        self.loop = asyncio.new_event_loop()
        self.loop.call_later((tomorrow - now).total_seconds(), self.day_change)
        logger.debug("Papago API limit reset has been scheduled on %s", tomorrow.strftime("%b %d %T"))

    @slash_command(description='입력한 내용을 번역합니다.')
    async def translate(
        self,
        ctx: ApplicationContext,
        lang: Option(str, "어느 언어에서 어느 언어로 변역할지 결정합니다", choices=[
            OptionChoice("한국어 -> 영어", "ko:en"),
            OptionChoice("영어 -> 한국어", "en:ko"),
            OptionChoice("한국어 -> 일본어", "ko:ja"),
            OptionChoice("일본어 -> 한국어", "ja:ko"),
            OptionChoice("한국어 -> 중국어", "ko:zh-CN"),
            OptionChoice("중국어 -> 한국어", "zh-CN:ko")
        ]),
        text: str
    ):
        src_lang, tar_lang = lang.split(':')
        if self.is_papago_limited:
            # embed = self.google_translate(src_lang, tar_lang, text)
            embed = discord.Embed(title="지금은 번역이 불가해요",
                                  description="오늘치 번역 기능을 벌써 다 써버렸네요. 내일 다시 하실 수 있어요",
                                  color=0xffffff)
        else:
            embed = self.papago_translate(src_lang, tar_lang, text)
        await ctx.respond(embed=embed)

    def papago_translate(self, src_lang: str, tar_lang: str, text: str) -> discord.Embed:
        data = f"source={src_lang}&target={tar_lang}&text={quote(text)}"
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Naver-Client-Id": self.papago_id,
            "X-Naver-Client-Secret": self.papago_secret
        }
        res = requests.post(PAPAGO_URL, data=data, headers=header)
        body = res.json()

        if res.status_code == 200:
            result = body['message']['result']
            return discord.Embed(title="번역 완료",
                                 description=result['translatedText'],
                                 color=0x00ffc6) \
                .set_footer(text=f"Papago API: {result['srcLangType']} -> {result['tarLangType']}")
        elif res.status_code == 500:
            logger.warning("Papago API has returned 500(Internal Server Error)")
            logger.info("User input: %s -> %s [%s]", src_lang, tar_lang, text)
            logger.info("Data from Papago API: %s", res.text)
            return discord.Embed(title="오류 발생",
                                 description="파파고 내부 서버에서 오류가 발생했어요. 잠시 후에 다시 시도해주세요",
                                 color=0xff0000)
        else:
            if body['errorCode'] == '010':
                logger.info("Papago API daily limit exceeded")
                self.is_papago_limited = True
                return self.google_translate(src_lang, tar_lang, text)
            else:
                logger.debug("Request toward Papago API failed for user error")
                logger.debug("User input: %s -> %s [%s]", src_lang, tar_lang, text)
                logger.debug("Data from Papago API: %s", res.text)
                err_msg = REGEX.match(body['errorMessage']).group(1)
                return discord.Embed(title="오류 발생",
                                     description=err_msg,
                                     color=0xff0000)

    def google_translate(self, src_lang: str, tar_lang: str, text: str) -> discord.Embed:
        data = json.dumps({
            "q": text,
            "source": src_lang,
            "target": tar_lang,
            "format": "text"
        })
        header = {
            "Authorization": "Bearer " + self.google_secret,
            "Content-Type": "application / json"
        }

        res = requests.post(GOOGLE_URL, data=data, headers=header)
        body = res.json()

        if res.ok:
            result = body['data']['translations'][0]['translatedText']
            return discord.Embed(title="번역 완료",
                                 description=result,
                                 color=0x00ffc6) \
                .set_footer(text=f"Google API: {src_lang} -> {tar_lang}")
        else:
            logger.warning("Google API request failed with code %s", res.status_code)
            logger.info("Data from Google API: %s", res.text)
            return discord.Embed(title="오류 발생",
                                 description="오류가 발생했어요. 잠시 후에 다시 시도해주세요",
                                 color=0xff0000)

    def day_change(self):
        self.loop.call_later(60 * 60 * 24, self.day_change)
        logger.debug("Reset Papago API limit")
        self.is_papago_limited = False


def setup(bot: discord.Bot):
    bot.add_cog(translate(bot))
