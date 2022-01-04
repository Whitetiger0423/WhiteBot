import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from datetime import date, datetime, timedelta
import requests
import os
from utils.utils import to_querystring

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
    "제주": (52, 38)
}


class weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service_key = os.getenv("WEATHER_KEY")

    @slash_command(description='현재 날씨를 조회합니다.')
    async def weather(self, ctx, place: Option(str, "날씨를 조회할 장소를 선택해주세요.", choices=list(place_data.keys()))):
        px, py = place_data[place]
        base_date, base_time = get_base_data_time()

        payload = {
            "serviceKey": self.service_key,
            "dataType": "json",
            "base_date": base_date,
            "base_time": base_time,
            "nx": px,
            "ny": py
        }

        result = requests.get(API_URL + to_querystring(payload))
        items = result.json()['response']['body']['items']

        data = dict()
        data['date'] = base_date

        weather_data = dict()
        for item in items['item']:
            if item['category'] == 'TMP':
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

        embed = discord.Embed(
            title=f"현재 날씨 정보", description=f"현재 날씨 정보를 조회했습니다.", color=0xffffff)
        embed.add_field(
            name="기온", value=f"{data['weather']['tmp']}℃", inline=False)
        embed.add_field(name="날씨", value=data['weather']['state'], inline=True)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(weather(bot))


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
