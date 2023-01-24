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

import base64

import discord
from discord.commands import ApplicationContext, Option
from discord.ext import commands

from constants import Constants
from utils.commands import slash_command


class Code(commands.Cog):
    @slash_command(name="암호", description="수신문을 암호화합니다.")
    async def encrypt(
            self,
            ctx: ApplicationContext,
            type: Option(
                str,
                "암호화 시킬 방식을 선택하세요",
                choices=["base16", "base32", "base64", "base85", "아스키 코드"],
            ),
            text: Option(str, "암호화 시킬 문장을 입력하세요."),
    ):
        if type == "base16":
            data = base16_encrypt(text)
        elif type == "base32":
            data = base32_encrypt(text)
        elif type == "base64":
            data = base64_encrypt(text)
        elif type == "base85":
            data = base85_encrypt(text)
        else:  # type == "아스키 코드":
            data = ascii_encrypt(text)

        embed = discord.Embed(
            title=f"{Constants.EMOJI['check']} 암호화 완료!",
            description=f"**{type}**를 기반으로 한 암호문입니다.",
            color=Constants.EMBED_COLOR["default"],
        ).add_field(name="**암호문:**", value=f"```{data}```", inline=False)

        await ctx.respond(embed=embed)

    @slash_command(name="해독", description="수신문을 해독합니다.")
    async def decrypt(
            self,
            ctx: ApplicationContext,
            type: Option(
                str,
                "해독할 암호문의 암호화 방식을 선택하세요",
                choices=["base16", "base32", "base64", "base85", "아스키 코드"],
            ),
            text: Option(str, "해독할 암호문을 입력하세요."),
    ):
        try:
            if type == "base16":
                data = base16_decrypt(text)
            elif type == "base32":
                data = base32_decrypt(text)
            elif type == "base64":
                data = base64_decrypt(text)
            elif type == "base85":
                data = base85_decrypt(text)
            else:  # type == "아스키 코드":
                data = ascii_decrypt(text)

            embed = discord.Embed(
                title="<a:check:824251178493411368> 해독 완료!",
                description=(
                        f"**{type}**를 기반으로 한 암호문을 해독하였습니다.\n"
                        + "해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!"
                ),
                color=Constants.EMBED_COLOR["default"]
            ).add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
        except Exception:
            embed = discord.Embed(
                title="WhiteBot 오류", description="해독 기능", color=Constants.EMBED_COLOR["error"]
            ).add_field(
                name="오류 내용:",
                value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.",
                inline=False,
            )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Code())


# ---------------------------
#        Encrypt
# ---------------------------


def ascii_encrypt(plain: str):
    parsed = list(plain)
    encrypted = [str(ord(x)) for x in parsed]
    return " ".join(encrypted).strip()


def base16_encrypt(plain: str):
    string_bytes = plain.encode("utf-8")
    base16_bytes = base64.b16encode(string_bytes)
    return base16_bytes.decode("utf-8")


def base32_encrypt(plain: str):
    string_bytes = plain.encode("utf-8")
    base32_bytes = base64.b32encode(string_bytes)
    return base32_bytes.decode("utf-8")


def base64_encrypt(plain: str):
    string_bytes = plain.encode("utf-8")
    base64_bytes = base64.b64encode(string_bytes)
    return base64_bytes.decode("utf-8")


def base85_encrypt(plain: str):
    string_bytes = plain.encode("utf-8")
    base85_bytes = base64.b85encode(string_bytes)
    return base85_bytes.decode("utf-8")


# ---------------------------
#          Decrypt
# ---------------------------


def ascii_decrypt(code: str):
    parsed = [int(x) for x in code.split(" ")]
    decrypted = [chr(x) for x in parsed]
    return "".join(decrypted)


def base16_decrypt(code: str):
    string_bytes = code.encode("utf-8")
    base16_bytes = base64.b16decode(string_bytes)
    return base16_bytes.decode("utf-8")


def base32_decrypt(code: str):
    string_bytes = code.encode("utf-8")
    base32_bytes = base64.b32decode(string_bytes)
    return base32_bytes.decode("utf-8")


def base64_decrypt(code: str):
    string_bytes = code.encode("utf-8")
    base64_bytes = base64.b64decode(string_bytes)
    return base64_bytes.decode("utf-8")


def base85_decrypt(code: str):
    string_bytes = code.encode("utf-8")
    base85_bytes = base64.b85decode(string_bytes)
    return base85_bytes.decode("utf-8")
