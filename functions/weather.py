from utils.commands import slash_command
from discord.ext import commands
from discord.commands import Option
import requests
from bs4 import BeautifulSoup
from constants import Constants
import discord


weather_selectors = Constants.WEATHER_SELECTORS


class Weather(commands.Cog):
    @slash_command(name="날씨", description="특정 지역의 날씨를 출력합니다.")
    async def weather(self, ctx, place: Option(str, "검색할 지역을 입력하세요.")):
        response = requests.get(f"https://search.naver.com/search.naver?where=nexearch&ie=utf8&query={place}+날씨")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            temp = self.select(soup, "temp")[5:-1]
            sens_temp = self.select(soup, "sens_temp")[:-1]
            weather = self.select(soup, "weather")
            humidity = self.select(soup, "humidity")
            wind_type = self.select(soup, "wind_type")
            wind_speed = self.select(soup, "wind_speed")
            micro_dust = self.select(soup, "micro_dust")
            ultramicro_dust = self.select(soup, "ultramicro_dust")
            uv = self.select(soup, "uv")
            embed = (
                discord.Embed(
                    title=f"{place} 날씨 정보", description="현재 날씨 정보를 조회했습니다.", color=Constants.EMBED_COLOR["default"]
                )
                .add_field(name=f"{self.temp_emoji(temp)} 기온", value=f"{temp}℃", inline=True)
                .add_field(name=f"{self.temp_emoji(sens_temp)} 체감온도", value=f"{sens_temp}℃", inline=True)
                .add_field(name=f"{self.weather_emoji(weather)} 날씨", value=weather, inline=True)
                .add_field(name="습도", value=humidity, inline=True)
                .add_field(name=wind_type, value=wind_speed, inline=True)
                .add_field(name="미세먼지", value=micro_dust, inline=True)
                .add_field(name="초미세먼지", value=ultramicro_dust, inline=True)
                .add_field(name="자외선", value=uv, inline=True)
            )
            await ctx.respond(embed=embed)
        except AttributeError:
            embed = discord.Embed(
                title="WhiteBot 오류",
                description=f"`{place}`는 올바른 지역명이 아닙니다.",
                color=Constants.EMBED_COLOR["error"],
            )
            await ctx.respond(embed=embed)

    def select(self, soup, value: str) -> str:
        return soup.select_one(weather_selectors[value]).get_text()

    def weather_emoji(self, value) -> str:
        if value == "비":
            return ":cloud_rain:"
        # elif value == "진눈깨비 내림":
            # return Constants.EMOJI["sleet"]
        # elif value == "소나기 내림":
            # return ":white_sun_rain_cloud:"
        elif value == "눈":
            return ":cloud_snow:"
        elif value == "맑음":
            return ":sunny:"
        elif value == "구름많음":
            return ":white_sun_cloud:"
        elif value == "흐림":
            return ":cloud:"
        else:
            return None

    def temp_emoji(self, value) -> str:
        if float(value) >= 33:
            return ":hot_face:"
        elif float(value) > 5:
            return ":grinning:"
        else:
            return ":cold_face:"


def setup(bot):
    bot.add_cog(Weather())
