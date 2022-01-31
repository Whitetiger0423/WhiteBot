import discord
from urllib import parse
from discord.ext import commands
from discord.commands import ApplicationContext, Option
from utils.commands import slash_command

GOOGLE_URL = "https://www.google.com/search?q="
NAVER_URL = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query="
DAUM_URL = "https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&q="
WIKIPEDIA_URL = "https://ko.wikipedia.org/wiki/"
NAVER_TERMS_URL = "https://terms.naver.com/search.naver?query="
NAMU_WIKI_URL = "https://namu.wiki/Search?q="


class etc(commands.Cog):
    @slash_command(description="검색어를 검색합니다.")
    async def search(
        self, ctx: ApplicationContext, *, searching: Option(str, "검색할 문장을 입력하세요.")
    ):
        encoded = parse.quote(searching)

        google = GOOGLE_URL + encoded
        naver = NAVER_URL + encoded
        daum = DAUM_URL + encoded
        wikipedia = WIKIPEDIA_URL + encoded
        termsnaver = NAVER_TERMS_URL + encoded
        namu = NAMU_WIKI_URL + encoded

        embed = discord.Embed(
            title="<a:check:824251178493411368> 검색결과",
            description=f"`{searching}`의 검색 결과입니다.",
            color=0xFFFFFF,
        )
        embed.add_field(
            name="포털 사이트 검색 결과",
            value=(
                f"[**구글**]({google})\n[**네이버**]({naver})\n[다음]({daum})\n[지식백과]({termsnaver})"
            ),
            inline=False,
        )
        embed.add_field(
            name="위키 사이트 검색 결과",
            value=(f"[**위키백과**]({wikipedia})\n[**나무위키**]({namu})"),
            inline=False,
        )
        await ctx.respond(embed=embed)

    @slash_command(description="내용을 전송합니다.")
    async def send(
        self,
        ctx: ApplicationContext,
        *,
        text: Option(str, "전송할 내용을 입력하세요. 줄바꿈은 적용되지 않습니다."),
    ):
        embed = discord.Embed(
            title=f"Sent by {ctx.author.display_name}",
            description=f"{text}",
            color=0xFFFFFF,
        )
        await ctx.respond(embed=embed)

    @slash_command(description="유저의 정보를 표시합니다.")
    async def userinfo(
            self, ctx: ApplicationContext, *, user: Option(discord.User ,"asdf")
    ):
        embed = discord.Embed(colour=0xffffff, title=user.display_name)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="계정명", value=user.name + "#" + user.discriminator)
        embed.add_field(name="닉네임", value=user.display_name)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="최상위 역할", value=user.top_role)
        embed.add_field(name="계정 생성 날짜", value=user.created_at)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(etc())
