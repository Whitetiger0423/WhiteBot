import discord
from discord.ext import commands
from discord.commands import ApplicationContext, Option
import dotenv
import pymysql
from pytz import timezone
import requests
from WhiteBot.utils.utils import to_querystring
from utils.commands import slash_command
import datetime
import os
import utils.logging
import logging

utils.logging.setup_logging()
logger = logging.getLogger(__name__)

data = ['AED', 'AUD', 'BHD', 'BND', 'CAD', 'CHF', 'CNH', 'DKK', 'EUR', 'GBP', 'HKD', 'IDR', 'JPY', 'KRW', 'KWD', 'MYR', 'NOK', 'NZD', 'SAR', 'SEK', 'SGD', 'THB', 'USD']
class currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("CURRENCY")
        self.db_user = os.getenv("DB_USER")
        self.db_pw = os.getenv("DB_PW")
        self.db_nm = os.getenv("DB_NM")
        
        if self.api_key is None:
            logger.warning("API Key doesn't exist!")

    @slash_command(name="환율", description="현재 시간 기준 환율을 불러옵니다.", guild_ids=[765869720989466635])
    async def currency(
        self,
        ctx: ApplicationContext,
        start: Option(str, "변환할 값(KRW)를 입력하세요. ex) 100000"),
        to: Option(str, "변환될 화폐를 선택해주세요.", choices=list(data))
    ):
        if self.api_key is None:
            err = discord.Embed(
                title="환율 조회 기능이 비활성화 되어있어요",
                description="관리자에게 문의해주세요\n[Team White 디스코드 서버](https://discord.gg/aebSVBgzuG)",
                color=0xFFFFFF
            )
            return await ctx.respond(embed=err)

        await ctx.defer()

        input = format(int(start), ',')

        re = self.select(to)

        now = datetime.datetime.now()
        now = now.astimezone(timezone('Asia/Seoul'))
        if re[f"max({to})"] != None:
            result = re[f"max({to})"] * to
            embed = (
                discord.Embed(
                    title="<a:check:824251178493411368> 변환된 값 정보", description="변환된 값의 정보를 반환함.", color=0xFFFFFF
                    )
                    .add_field(name="입력한 값", value=input, inline=False)
                    .add_field(name="변환된 값", value=result, inline=False)
                
                )
            await ctx.followup.send(embed=embed)

        else:
            err = discord.Embed(
                title="주말/ 공휴일, 또는 밤 11시 이후에는 환율 조회가 불가능해요",
                description="나중에 다시 시도해주세요\n[Team White 디스코드 서버](https://discord.gg/aebSVBgzuG)",
                color=0xFFFFFF)

            await ctx.followup.send(embed=err)

    def db_update():
        dotenv.load_dotenv(verbose=True)
        db_user = os.getenv("DB_USER")
        db_pw = os.getenv("DB_PW")
        db_nm = os.getenv("DB_NM")

        BASE_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?"

        headers = {
                "authkey": os.getenv("CURRENCY"),
                "data": "AP01",
        }

        # a = urlencode(headers)
        req = requests.get(BASE_URL + to_querystring(headers))
        data = req.json()

        db = pymysql.connect(
                user=db_user,
                passwd=db_pw,
                host="127.0.0.1",
                db=db_nm, # 
                charset="utf8",
        )

        cursor = db.cursor(pymysql.cursors.DictCursor)

        delete = "DELETE from testing;"
        cursor.execute(delete)  
        
        for i in data:
                dol = i["bkpr"]
                re = dol.replace(',', '')
                name = i["cur_unit"][:3]
                sql = f"INSERT INTO testing ({name}) VALUES ({re});"
                cursor.execute(sql)
        
        db.commit()
        cursor.close()
        db.close()

    def select(self, to):
        self.db_update()
        db = pymysql.connect(
                user=self.db_user,
                passwd=self.db_pw,
                host="127.0.0.1",
                db=self.db_nm, # 
                charset="utf8",
        )

        cursor = db.cursor(pymysql.cursors.DictCursor)

        sql = f"SELECT max({to}) from testing;"
        cursor.execute(sql)

        result = cursor.fetchone()
        cursor.close()
        db.close()

        return result

def setup(bot):
    bot.add_cog(currency(bot))
            
            
