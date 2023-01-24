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

import os
import motor.motor_asyncio


MONGO_URI = os.getenv("MONGO_URI")


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI).WhiteBot


class CurrencyDatabase:
    async def currency_find(country_name: str):
        """

        Args:
            country_name (str): - 필수, 국가 이름 입력

        DB에서 환율 정보를 찾아 반환합니다.
        """
        return await client.currency.find_one()

    async def currency_add(country_name: str, currency: int):
        """

        Args:
            country_unit (str): 국가 명 ex) 짐바브웨 달러 AED
            currency (str): 환율 값 ex) 1,390

        새로운 환율 값을 DB에 저장합니다.
        """
        return await client.currency.insert_one({f"country_{country_name}": currency})

    async def currency_reset():
        """

        새로운 환율 값 저장을 위해 DB 안의 값을 모두 삭제합니다.

        """
        return await client.currency.delete_many({})
