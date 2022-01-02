import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from datetime import date, datetime, timedelta
import requests


class weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='현재 날씨를 조회합니다.')
    async def weather(self, ctx, place: Option(str, "날씨를 조회할 장소를 선택해주세요.", choices=["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"])):
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

        result = requests.get("http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?" + payload)

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
    bot.add_cog(weather(bot))