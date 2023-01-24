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

import logging
import os

import discord
import requests
from discord.commands import ApplicationContext, Option
from discord.ext import commands

from constants import Constants
from utils.commands import slash_command
from utils.database import CurrencyDatabase
from utils.utils import to_querystring

logger = logging.getLogger(__name__)

units = {
    "아랍에미리트 디르함": "AED",
    "오스트레일리아 달러": "AUD",
    "바레인 디나르": "BHD",
    "브루나이 달러": "BND",
    "캐나다 달러": "CAD",
    "스위스 프랑": "CHF",
    "위안화": "CNH",
    "덴마크 크로네": "DKK",
    "유로": "EUR",
    "파운드 스털링": "GBP",
    "홍콩 달러": "HKD",
    "인도네시아 루피아": "IDR(100)",
    "일본 엔": "JPY(100)",
    "쿠웨이트 디나르": "KWD",
    "말레이시아 링깃": "MYR",
    "노르웨이 크로네": "NOK",
    "뉴질랜드 달러": "NZD",
    "사우디아라비아 리얄": "SAR",
    "스웨덴 크로나": "SEK",
    "싱가포르 달러": "SGD",
    "태국 밧": "THB",
    "미국 달러": "USD",
}

choice = [
    "AED 아랍에미리트 디르함",
    "AUD 오스트레일리아 달러",
    "BHD 바레인 디나르",
    "BND 브루나이 달러",
    "CAD 캐나다 달러",
    "CHF 스위스 프랑",
    "CNH 위안화",
    "DKK 덴마크 크로네",
    "EUR 유로",
    "GBP 파운드 스털링",
    "HKD 홍콩 달러",
    "IDR 인도네시아 루피아",
    "JPY 일본 엔",
    "KWD 쿠웨이트 디나르",
    "MYR 말레이시아 링깃",
    "NOK 노르웨이 크로네",
    "NZD 뉴질랜드 달러",
    "SAR 사우디아라비아 리얄",
    "SEK 스웨덴 크로나",
    "SGD 싱가포르 달러",
    "THB 태국 밧",
    "USD 미국 달러",
]


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("CURRENCY")

        if self.api_key is None:
            logger.warning("API Key가 없습니다")

    @slash_command(
        name="환율",
        description="현재 시간 기준 환율로 환전합니다.",
    )
    async def currency(
            self,
            ctx: ApplicationContext,
            start: Option(int, "변환할 값(KRW)를 입력하세요. ex) 100000"),
            to: Option(str, "변환할 통화를 선택해주세요. ex)USD", choices=choice),
    ):
        if self.api_key is None:
            err = discord.Embed(
                title="환율 조회 기능이 비활성화 되어있어요",
                description="관리자에게 문의해주세요\n[Team White 디스코드 서버](https://discord.gg/aebSVBgzuG)",
                color=Constants.EMBED_COLOR["default"],
            )
            return await ctx.respond(embed=err)

        await ctx.defer()
        unit = units[to[4:]]
        db_unit = units.get(to[4:])
        await self.db_update(unit)

        if await CurrencyDatabase.currency_find(db_unit):
            found = await CurrencyDatabase.currency_find(db_unit)

            end = int(found[f"country_{db_unit}"])
            result = start / end
            if unit == "IDR(100)" or unit == "JPY(100)":
                unit = unit[:3]
            embed = (
                discord.Embed(
                    title=f"{Constants.EMOJI['check']} 변환된 값 정보",
                    description="변환된 값의 정보를 반환했어요",
                    color=Constants.EMBED_COLOR["default"],
                )
                .add_field(name="입력한 값", value=f"`{start:,}`원", inline=False)
                .add_field(name="변환된 값", value=f"`{result:.2f}` `{unit}`", inline=False)
            )
            return await ctx.followup.send(embed=embed)

        else:
            err = discord.Embed(
                title="주말/ 공휴일, 또는 밤 11시 이후에는 환율 조회가 불가능해요",
                description="나중에 다시 시도해주세요\n[Team White 디스코드 서버](https://discord.gg/aebSVBgzuG)",
                color=Constants.EMBED_COLOR["default"],
            )

            return await ctx.followup.send(embed=err)

    async def db_update(self, unit):
        base_url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?"

        headers = {"authkey": os.getenv("CURRENCY"), "data": "AP01", "cur_unit": unit}

        req = requests.get(base_url + to_querystring(headers))
        data = req.json()

        await CurrencyDatabase.currency_reset()
        for i in data:
            dol = i["bkpr"]
            re = dol.replace(",", "")
            name = i["cur_unit"]
            await CurrencyDatabase.currency_add(name, re)


def setup(bot):
    bot.add_cog(Currency(bot))
