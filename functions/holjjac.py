import discord
import random
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option

@bot.slash_command(description="홀짝")
async def 홀짝(ctx):
    import random
    dice = random.randint(1, 6)
    embed = discord.Embed(title='홀, 짝중에 하나를 선택해주세요.',
                          description='선택 한 뒤에 어떤 수가 나왔는지 알려드려요.')
    embed.add_field(name='> 주사위의 눈', value='???')
    embed.add_field(name='> 홀수', value='🔴')
    embed.add_field(name='> 짝수', value='🔵')
    msg = await ctx.channel.send(embed=embed)
    await msg.add_reaction('🔴')
    await msg.add_reaction('🔵')
    try:

        def check(reaction, user):
            return str(reaction) in ['🔴', '🔵'] and \
            user == ctx.author and reaction.message.id == msg.id

        reaction, user = await bot.wait_for('reaction_add', check=check)
        if  (str(reaction) == '🔴' and dice % 2 == 1) or \
            (str(reaction) == '🔵' and dice % 2 == 0):
            embed = discord.Embed(title='홀, 짝중에 하나를 선택해주세요.',
                                  description='정답입니다! 계속해서 도전해보세요!')
        else:
            embed = discord.Embed(title='홀, 짝중에 하나를 선택해주세요.',
                                  description='틀렸습니다... 계속해서 도전해보세요!')
        embed.add_field(name='> 주사위의 눈', value=str(dice))
        embed.add_field(name='> 홀수', value='🔴')
        embed.add_field(name='> 짝수', value='🔵')
        await msg.clear_reactions()
        await msg.edit(embed=embed)
    except:
        pass
