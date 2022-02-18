import discord
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option

basic_commands = (
    discord.Embed(
        title="<a:check:824251178493411368> WhiteBot 명령어 도움말",
        description="WhiteBot의 명령어에 대해서 소개합니다.",
        color=0xFFFFFF,
    )
    .add_field(name="help 명령어 사용법", value="sorts 변수를 선택하세요.", inline=False)
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
        title="<a:check:824251178493411368> WhiteBot 유틸리티 명령어 도움말",
        description="WhiteBot의 명령어에 대해서 소개합니다.",
        color=0xFFFFFF,
    )
    .add_field(name="/search `[항목]`", value="여러 사이트에서 `[항목]`을 검색합니다.", inline=False)
    .add_field(name="/send `[항목]`", value="`[항목]`을 전송해요!", inline=False)
    .add_field(name="/code `[수신문]`", value="`[수신문]`을 암호화합니다.", inline=False)
    .add_field(name="/decode `[암호문]`", value="`[암호문]`을 해독합니다.", inline=False)
    .add_field(name="/bot", value="봇의 정보를 전송합니다.", inline=False)
    .add_field(
        name="/youtube",
        value="들어가 있는 음성 채널에 유튜브 투게더를 활성화 시키는 링크를 보냅니다. 음성 채널에 연결되어 있어야 사용 가능하며, 일부 서버에선 작동하지 않습니다.",
        inline=False,
    )
    .add_field(name="/weather `[지역]`", value="`[지역]`의 현재 날씨를 조회합니다.")
    .add_field(name="/translate `[언어]` `[텍스트]`", value="`[텍스트]`를 번역합니다.", inline=False)
)

playing_commands = (
    discord.Embed(
        title="<a:check:824251178493411368> WhiteBot 놀이 명령어 도움말",
        description="WhiteBot의 명령어에 대해서 소개합니다.",
        color=0xFFFFFF,
    )
    .add_field(
        name="/rsp `[가위, 바위, 보]`",
        value="봇과 가위바위보를 합니다. `/가위바위보 가위` 등의 형식으로 쓰면 됩니다.",
        inline=False,
    )
    .add_field(
        name="/dice `[N]` `(n)`",
        value="주사위를 굴립니다. `[N]`만 쓰면 1부터 `[N]`까지의 숫자를, `(n)`까지 모두 쓰면 `[N]`부터 `(n)`까지의 숫자를 랜덤으로 표출합니다.",
        inline=False,
    )
    .add_field(
        name="holjjac", value="홀짝 게임을 시작합니다. 직접 반응을 눌러서 홀짝을 맞춰보세요.", inline=False
    )
)

manage_commands = (
    discord.Embed(
        title="<a:check:824251178493411368> WhiteBot 관리 명령어 도움말",
        description="WhiteBot의 명령어에 대해서 소개합니다.",
        color=0xFFFFFF,
    )
    .add_field(name="/ping", value="봇의 핑을 알려줍니다.", inline=False)
    .add_field(
        name="/delete `[n]`",
        value="메시지를 `[n]`의 값 만큼 삭제합니다. 메시지 관리 권한이 필요합니다.",
        inline=False,
    )
)


class help(commands.Cog):
    @slash_command(description="봇의 도움말을 전송합니다.")
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
        elif sorts == "기본":
            await ctx.respond(embed=basic_commands)


def setup(bot):
    bot.add_cog(help())
