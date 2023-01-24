# Copyright (C) 2022 Team White
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import asyncio
import logging
import os
import re
from datetime import datetime, timedelta
from urllib.parse import quote

import discord
from discord.commands import ApplicationContext, Option, OptionChoice
from discord.ext import commands

from constants import Constants
from utils.commands import slash_command
from utils.whitebot import WhiteBot

PAPAGO_URL = "https://openapi.naver.com/v1/papago/n2mt"
PAPAGO_DETECT_LANG_URL = "https://openapi.naver.com/v1/papago/detectLangs"
PAPAGO_API_ERROR_MSG_REGEX = re.compile(".+ \\((.+)\\)")

logger = logging.getLogger("translate")


class Translate(commands.Cog):
    def __init__(self, bot: WhiteBot):
        self.bot = bot
        self.session = self.bot.aiohttp_session
        self.enabled = True
        _papago_id = os.getenv("PAPAGO_APPID")

        if _papago_id is None:
            logger.warning(
                "Papago API key not provided. Translation feature will be disabled"
            )
            self.enabled = False
            return

        self.papago_id = _papago_id
        self.papago_secret = os.getenv("PAPAGO_SECRET")

        self.is_papago_limited = False

        tomorrow = datetime.today() + timedelta(days=1)
        now = datetime.now()

        self.loop = asyncio.new_event_loop()
        self.loop.call_later((tomorrow - now).total_seconds(), self.day_change)
        logger.info(
            "Papago API limit reset has been scheduled on %s",
            tomorrow.strftime("%b %d %T"),
        )

    @slash_command(name="번역", description="입력한 내용을 번역합니다.")
    async def translate(
            self,
            ctx: ApplicationContext,
            lang: Option(
                str,
                "어느 언어로 변역할지 결정합니다",
                choices=[
                    OptionChoice("영어", "en"),
                    OptionChoice("일본어", "ja"),
                    OptionChoice("중국어", "zh-CN"),
                    OptionChoice("프랑스어", "fr"),
                    OptionChoice("독일어", "de"),
                    OptionChoice("이탈리아어", "it"),
                    OptionChoice("러시아어", "ru"),
                    OptionChoice("스페인어", "es"),
                    OptionChoice("한국어", "ko")
                ],
            ),
            text: str,
    ):
        if not self.enabled:
            embed = discord.Embed(
                title="번역 기능이 비활성화 되어있어요",
                description="관리자에게 문의해주세요\n[Team White 디스코드 서버](https://discord.gg/aebSVBgzuG)",
                color=Constants.EMBED_COLOR["default"],
            )
            return await ctx.respond(embed=embed)

        if self.is_papago_limited:
            embed = discord.Embed(
                title="지금은 번역이 불가해요",
                description="오늘치 번역 기능을 벌써 다 써버렸네요. 내일까지 잠시만 기다려주세요",
                color=Constants.EMBED_COLOR["default"],
            )
            return await ctx.respond(embed=embed)

        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Naver-Client-Id": self.papago_id,
            "X-Naver-Client-Secret": self.papago_secret,
        }
        data = "query=" + text
        async with self.session.post(PAPAGO_DETECT_LANG_URL, data=data.encode("utf-8"), headers=header) as res:
            detected_lang = res.json()["langCode"]
            src_lang = detected_lang
            tar_lang = lang
            embed = self.papago_translate(src_lang, tar_lang, text)
            await ctx.respond(embed=embed)

    def papago_translate(
            self, src_lang: str, tar_lang: str, text: str
    ) -> discord.Embed:
        data = f"source={src_lang}&target={tar_lang}&text={quote(text)}"
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Naver-Client-Id": self.papago_id,
            "X-Naver-Client-Secret": self.papago_secret,
        }
        async with self.session.post(PAPAGO_URL, data=data.encode("utf-8"), headers=header) as res:
            body = res.json()

            if res.status == 200:
                result = body["message"]["result"]
                return discord.Embed(
                    title=f"{Constants.EMOJI['check']} 번역 완료", description=result["translatedText"],
                    color=Constants.EMBED_COLOR["success"]
                ).set_footer(
                    text=f"Papago API: {result['srcLangType']} -> {result['tarLangType']}"
                )
            elif res.status == 500:
                logger.error(
                    "Papago API has returned 500\n=> %s -> %s [%s]\n=> Response: %s",
                    src_lang,
                    tar_lang,
                    text,
                    res.text,
                )
                return discord.Embed(
                    description="파파고 서버에 오류가 발생했어요. 잠시 후에 다시 시도해주세요", color=Constants.EMBED_COLOR["error"]
                )
            else:
                if body["errorCode"] == "010":
                    logger.info("Papago API daily limit exceeded")
                    self.is_papago_limited = True
                    return discord.Embed(
                        title="지금은 번역이 불가해요",
                        description="오늘치 번역 기능을 벌써 다 써버렸네요. 내일까지 잠시만 기다려주세요",
                        color=Constants.EMBED_COLOR["default"],
                    )
                else:
                    logger.info(
                        "Papago API has returned %d\n=> %s -> %s [%s]\n=> Response: %s",
                        res.status_code,
                        src_lang,
                        tar_lang,
                        text,
                        res.text,
                    )
                    err_msg = PAPAGO_API_ERROR_MSG_REGEX.match(body["errorMessage"]).group(
                        1
                    )
                    return discord.Embed(description=err_msg, color=Constants.EMBED_COLOR["error"])

    def day_change(self):
        self.loop.call_later(60 * 60 * 24, self.day_change)
        logger.info("Reset Papago API limit")
        self.is_papago_limited = False


def setup(bot):
    bot.add_cog(Translate(bot))
