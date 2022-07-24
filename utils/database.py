import os
import motor.motor_asyncio
import dotenv

dotenv.load_dotenv("./token.env", verbose=True)

MONGO_URI = os.getenv("MONGO_URI")


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI).WhiteBot


class CURRENCY_DATABASE:
    async def currency_find(country_name: str):
        """

        Args:
            country_name (str): - 필수, 국가 이름 입력

        DB에서 환율 정보를 찾아 반환합니다.
        """
        return await client.currency.find_one(f"country_{country_name}")

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
