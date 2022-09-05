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
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
from constants import Constants

basic_commands = (
    discord.Embed(
        title=f"{Constants.EMOJI[0]} WhiteBot 명령어 도움말",
        description="WhiteBot의 명령어에 대해서 소개합니다.",
        color=Constants.EMBED_COLOR["default"],
    )
    .add_field(name="도움말 명령어 사용법", value="sorts 변수를 선택하세요.", inline=False)
    .add_field(
        name="공식 홈페이지",
        value=":link: [공식 홈페이지](<https://team-white.kro.kr/>)",
        inline=False,
    )
    .add_field(
        name="개인정보 처리방침",
        value=":link: [개인정보 처리방침](<https://team-white.kro.kr/privacy>)",
        inline=False,
    )
    .add_field(
        name="공식 서포팅 서버",
        value=":link: [Team White 공식 서버](<https://discord.gg/aebSVBgzuG>)",
        inline=False,
    )
    .add_field(
        name="봇 초대 링크",
        value=":link: [봇 초대하기](<https://discord.com/oauth2/authorize?client_id=782777035898617886&permissions=8&scope=bot>)",
        inline=False,
    )
)

utility_commands = (
    discord.Embed(
        title=f"{Constants.EMOJI[0]} WhiteBot 유틸리티 명령어 도움말",
        description="WhiteBot의 명령어에 대해서 소개합니다.",
        color=Constants.EMBED_COLOR["default"],
    )
    .add_field(name="/검색 `[항목]`", value="여러 사이트에서 `[항목]`을 검색합니다.", inline=False)
    .add_field(name="/전송 `[항목]`", value="`[항목]`을 전송해요!", inline=False)
    .add_field(name="/암호 `[수신문]`", value="`[수신문]`을 암호화합니다.", inline=False)
    .add_field(name="/해독 `[암호문]`", value="`[암호문]`을 해독합니다.", inline=False)
    .add_field(name="/날씨 `[지역]`", value="`[지역]`의 현재 날씨를 조회합니다.")
    .add_field(name="/번역 `[언어]` `[텍스트]`", value="`[텍스트]`를 번역합니다.", inline=False)
    .add_field(
        name="/투표 `[제목]` `[선택지]`", value="`[선택지]`를 대상으로 한 투표를 진행합니다.", inline=False
    )
    .add_field(name="/개표 `[투표]`", value="`[투표]`를 종료하고, 결과를 확인합니다.", inline=False)
    .add_field(
        name="/연산 `[종류]` `[A]` `[B]`",
        value="`[A]`와 `[B]`를 `[종류]`로 받은 사칙 연산을 실행합니다. `[A]`와 `[B]`는 정수, 소수 모두 가능합니다.",
        inline=False,
    )
    .add_field(name="/공학계산 `[종류]` `[값]`", value="`[값]`을 `[종류]`로 계산합니다.", inline=False)
    .add_field(name="/맞춤법 `[내용]`", value="`[내용]`의 맞춤법을 검사합니다.", inline=False)
    .add_field(name="/주소단축 `[URL]`", value="`[URL]`을 짧은 주소로 단축해줍니다.", inline=False)
    .add_field(name="/코로나", value="코로나 관련 정보를 출력합니다.", inline=False)
    .add_field(name="/환율 `[원화]` `[종류]`", value="`[원화]`원을 `[종류]`로 얼마인지 출력합니다.", inline=False)
)

playing_commands = (
    discord.Embed(
        title=f"{Constants.EMOJI[0]} WhiteBot 놀이 명령어 도움말",
        description="WhiteBot의 명령어에 대해서 소개합니다.",
        color=Constants.EMBED_COLOR["default"],
    )
    .add_field(
        name="/가위바위보 `[가위, 바위, 보]`",
        value="봇과 가위바위보를 합니다. `/가위바위보 가위` 등의 형식으로 쓰면 됩니다.",
        inline=False,
    )
    .add_field(
        name="/주사위 `[A]` `(B)`",
        value="주사위를 굴립니다. `[A]`만 쓰면 1부터 `[A]`까지의 숫자를, `(B)`까지 모두 쓰면 `[A]`부터 `(B)`까지의 숫자를 랜덤으로 표출합니다.",
        inline=False,
    )
    .add_field(
        name="/틱택토 `[상대]`",
        value="`[상대]`와 틱택토(삼목) 게임을 진행합니다. 스스로를 상대로 지정할 경우 혼자서 조종합니다.",
        inline=False,
    )
    .add_field(name="/홀짝", value="홀짝 게임을 시작합니다. 직접 반응을 눌러서 홀짝을 맞춰보세요.", inline=False)
)

manage_commands = (
    discord.Embed(
        title=f"{Constants.EMOJI[0]} WhiteBot 관리 명령어 도움말",
        description="WhiteBot의 명령어에 대해서 소개합니다.",
        color=Constants.EMBED_COLOR["default"],
    )
    .add_field(name="/도움말", value="봇의 도움말을 전송합니다.", inline=False)
    .add_field(name="/봇", value="봇의 정보를 전송합니다. 봇의 버전, 업타임 등이 같이 표시됩니다.", inline=False)
    .add_field(name="/핑", value="봇의 핑을 전송합니다.", inline=False)
    .add_field(
        name="/청소 `[n]`",
        value="메시지를 `[n]`의 값 만큼 삭제합니다. 메시지 관리 권한이 필요합니다.",
        inline=False,
    )
)


class Help(commands.Cog):
    @slash_command(name="도움말", description="봇의 도움말을 전송합니다.")
    async def help(
        self,
        ctx: ApplicationContext,
        sorts: Option(str, "도움말의 유형을 선택하세요", choices=["기본", "유틸리티", "놀이", "관리"]),
    ):
        if sorts == "유틸리티":
            await ctx.respond(embed=utility_commands)
        elif sorts == "놀이":
            await ctx.respond(embed=playing_commands)
        elif sorts == "관리":
            await ctx.respond(embed=manage_commands)
        else:  # sorts == "기본":
            await ctx.respond(embed=basic_commands)


def setup(bot):
    bot.add_cog(Help())
