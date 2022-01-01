import discord
import base64
from discord.ext import commands
from discord.commands import slash_command, Option

def encrypt(plain: str):
    parsed: list = list(plain)
    encrypted: list = [str(ord(x)) for x in parsed]
    return ' '.join(encrypted).strip()

def decrypt(encrypted: str):
    parsed: list = [int(x) for x in encrypted.split(' ')]
    decrypted: list = [chr(x) for x in parsed]
    return ''.join(decrypted)


class code(commands.Cogs):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='수신문을 암호화합니다.')
    async def code(self, ctx, type: Option(str, "암호화 시킬 방식을 선택하세요", choices=["base16", "base32", "base64", "base85", "아스키 코드"]), text: Option(str, "암호화 시킬 문장을 입력하세요.")):
        if type == "base16":
            string_bytes = text.encode("utf-8")
            base16_bytes = base64.b16encode(string_bytes) 
            data = base16_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base16**을 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**원문:**", value=f"```{text}```", inline=False)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base32":
            string_bytes = text.encode("utf-8")
            base32_bytes = base64.b32encode(string_bytes) 
            data = base32_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base32**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**원문:**", value=f"```{text}```", inline=False)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base64":
            string_bytes = text.encode("utf-8")
            base64_bytes = base64.b64encode(string_bytes) 
            data = base64_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base64**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**원문:**", value=f"```{text}```", inline=False)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base85":
            string_bytes = text.encode("utf-8")
            base85_bytes = base64.b85encode(string_bytes) 
            data = base85_bytes.decode("utf-8") 
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**base85**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**원문:**", value=f"```{text}```", inline=False)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)
        elif type == "아스키 코드":
            data = encrypt(text)
            embed = discord.Embed(title="<a:check:824251178493411368> 암호화 완료!", description="**아스키 코드**를 기반으로 한 암호문입니다.", color=0xffffff)
            embed.add_field(name="**원문:**", value=f"```{text}```", inline=False)
            embed.add_field(name="**암호문:**", value=f"```{data}```", inline=False)
            await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(description='수신문을 해독합니다.')
    async def decode(self, ctx, type: Option(str, "해독할 암호문의 암호화 방식을 선택하세요", choices=["base16", "base32", "base64", "base85", "아스키 코드"]), text: Option(str, "해독할 암호문을 입력하세요.")):
        if type == "base16":
            try:
                string_bytes = text.encode("utf-8")
                base16_bytes = base64.b16decode(string_bytes) 
                data = base16_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base16**을 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**암호문:**", value=f"```{text}```", inline=False)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base32":
            try:
                string_bytes = text.encode("utf-8")
                base32_bytes = base64.b32decode(string_bytes) 
                data = base32_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base32**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**암호문:**", value=f"```{text}```", inline=False)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base64":
            try:
                string_bytes = text.encode("utf-8")
                base64_bytes = base64.b64decode(string_bytes) 
                data = base64_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base64**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**암호문:**", value=f"```{text}```", inline=False)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
        elif type == "base85":
            try:
                string_bytes = text.encode("utf-8")
                base85_bytes = base64.b85decode(string_bytes) 
                data = base85_bytes.decode("utf-8")
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**base85**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**암호문:**", value=f"```{text}```", inline=False)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
        elif type == "아스키 코드":
            data = decrypt(text)
            try:
                embed = discord.Embed(title="<a:check:824251178493411368> 해독 완료!", description="**아스키 코드**를 기반으로 한 암호문을 해독하였습니다.\n해독이 잘못되었다면 [서포팅 서버](<https://discord.gg/aebSVBgzuG>)에서 제보해주세요!", color=0xffffff)
                embed.add_field(name="**암호문:**", value=f"```{text}```", inline=False)
                embed.add_field(name="**해독 결과:**", value=f"```{data}```", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)
            except:
                embed = discord.Embed(title="WhiteBot 오류", description="해독 기능", color=0xff0000)
                embed.add_field(name="오류 내용:", value="올바르지 않은 암호문입니다. 암호의 종류가 맞는지 확인해주시고, 올바른 암호문을 입력해주세요.", inline=False)
                await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(code(bot))
