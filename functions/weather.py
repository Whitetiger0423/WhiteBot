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

import discord
from discord.ext import commands
from discord.commands import ApplicationContext, Option
from utils.commands import slash_command
from datetime import date, datetime, timedelta
import requests
import os
from utils.utils import apply_if_not_none, to_querystring, to_dict
import logging

API_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"

place_data = {
    "서울": (60, 127),
    "부산": (98, 76),
    "대구": (89, 90),
    "인천": (55, 124),
    "광주": (58, 74),
    "대전": (67, 100),
    "울산": (102, 84),
    "세종": (66, 103),
    "경기": (60, 120),
    "강원": (73, 134),
    "충북": (69, 107),
    "충남": (68, 100),
    "전북": (63, 89),
    "전남": (51, 67),
    "경북": (89, 91),
    "경남": (91, 77),
    "제주": (52, 38),
}

logger = logging.getLogger(__name__)


class weather(commands.Cog):
    def __init__(self):
        self.service_key = os.getenv("WEATHER_KEY")
        if self.service_key is None:
            logger.warning("Weather API key not provided. Weather feature will be disabled")

    @slash_command(description="현재 날씨를 조회합니다.")
    async def weather(
        self,
        ctx: ApplicationContext,
        place: Option(str, "날씨를 조회할 장소를 선택해주세요.", choices=list(place_data.keys())),
    ):
        if self.service_key is None:
            embed = discord.Embed(
                title="날씨 기능이 비활성화 되어있어요",
                description="관리자에게 문의해주세요\n[Team White 디스코드 서버](https://discord.gg/aebSVBgzuG)",
                color=0xffffff)
            return await ctx.respond(embed=embed)

        await ctx.defer()

        px, py = place_data[place]
        base_date, base_time = get_base_data_time()

        payload = {
            "serviceKey": self.service_key,
            "dataType": "json",
            "base_date": base_date,
            "base_time": base_time,
            "nx": px,
            "ny": py,
        }

        result = requests.get(API_URL + to_querystring(payload))
        data = result.json()["response"]["body"]["items"]["item"]

        data = to_dict(data, lambda k: k["category"], lambda v: v["fcstValue"])

        temperature = apply_if_not_none(data.get("TMP"), lambda x: f"{x}℃")
        wind_speed = apply_if_not_none(data.get("WSD"), lambda x: f"{x}m/s")
        weather_state = apply_if_not_none(data.get("PTY"), self.process_pty)

        if weather_state is None:
            weather_state = apply_if_not_none(data.get("SKY"), self.process_sky)

        embed = (
            discord.Embed(
                title="현재 날씨 정보", description="현재 날씨 정보를 조회했습니다.", color=0xFFFFFF
            )
            .add_field(name="기온", value=temperature or "데이터가 없습니다", inline=True)
            .add_field(name="풍속", value=wind_speed or "데이터가 없습니다", inline=True)
            .add_field(name="날씨", value=weather_state or "데이터가 없습니다", inline=False)
        )

        await ctx.followup.send(embed=embed)

    def process_pty(self, value) -> str:
        if value == "1":
            return "비 내림"
        elif value == "2":
            return "진눈깨비 내림"
        elif value == "3":
            return "눈 내림"
        elif value == "4":
            return "소나기 내림"
        else:
            return None

    def process_sky(self, value) -> str:
        value = int(value)
        if value <= 5:
            return "맑음"
        elif value <= 8:
            return "구름 많음"
        else:
            return "흐림"


def setup(bot):
    bot.add_cog(weather())


def get_base_data_time():
    t = datetime.today()
    t_d = t.strftime("%Y%m%d")
    y = date.today() - timedelta(days=1)
    y_d = y.strftime("%Y%m%d")

    now = datetime.now()

    if now.hour < 2 or (now.hour == 2 and now.minute <= 10):
        base_date = y_d
        base_time = "2300"
    elif now.hour < 5 or (now.hour == 5 and now.minute <= 10):
        base_date = t_d
        base_time = "0200"
    elif now.hour < 8 or (now.hour == 8 and now.minute <= 10):
        base_date = t_d
        base_time = "0500"
    elif now.hour <= 11 or now.minute <= 10:
        base_date = t_d
        base_time = "0800"
    elif now.hour < 14 or (now.hour == 14 and now.minute <= 10):
        base_date = t_d
        base_time = "1100"
    elif now.hour < 17 or (now.hour == 17 and now.minute <= 10):
        base_date = t_d
        base_time = "1400"
    elif now.hour < 20 or (now.hour == 20 and now.minute <= 10):
        base_date = t_d
        base_time = "1700"
    elif now.hour < 23 or (now.hour == 23 and now.minute <= 10):
        base_date = t_d
        base_time = "2000"
    else:
        base_date = t_d
        base_time = "2300"

    return (base_date, base_time)
