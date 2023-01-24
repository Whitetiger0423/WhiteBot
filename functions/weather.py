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

from json import loads
from os import getenv

import requests
from discord import Embed
from discord.commands import Option
from discord.ext import commands

from constants import Constants
from utils.commands import slash_command


class Weather(commands.Cog):
    @slash_command(name="날씨", description="특정 지역의 날씨를 출력합니다.")
    async def weather(self, ctx, place: Option(str, "검색할 지역을 입력하세요.", name="장소")):
        url = f"https://api.openweathermap.org/geo/1.0/direct?q={place}&limit=5&appid={getenv('WEATHER_KEY')}"
        response = requests.get(url)
        json = loads(response.text)
        if len(json):
            location = json[0]
            name = location["local_names"]["ko"] if "ko" in location["local_names"].keys() else location["name"]
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={getenv('WEATHER_KEY')}&lang=kr&units=metric"
            response = requests.get(url)
            json = loads(response.text)
            weather = json["weather"][0]
            embed = Embed(title=f"{name} 날씨 ({json['coord']['lon']}° {json['coord']['lat']}°)",
                          color=Constants.EMBED_COLOR["default"], description="일출/일몰은 사용자의 타임존으로 출력됩니다.")
            embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png")
            embed.add_field(name="날씨", value=weather["description"])
            embed.add_field(name="온도 실제/체감", value=f"{json['main']['temp']}°C / {json['main']['feels_like']}°C")
            embed.add_field(name="온도 최대/최저", value=f"{json['main']['temp_max']}°C / {json['main']['temp_min']}°C")
            embed.add_field(name="습도", value=f"{json['main']['humidity']}%")
            embed.add_field(name="기압", value=f"{json['main']['pressure']} hPa")
            embed.add_field(name="풍속", value=f"{json['wind']['speed']}m/s")
            embed.add_field(name="일출", value=f"<t:{json['sys']['sunrise']}>")
            embed.add_field(name="일몰", value=f"<t:{json['sys']['sunset']}>")
            await ctx.respond(embed=embed)
        else:
            embed = Embed(title="오류", description="검색 결과가 없습니다.", color=Constants.EMBED_COLOR["error"])
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Weather())
