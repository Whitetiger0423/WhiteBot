import discord
from discord.ext import commands
from discord.commands import ApplicationContext, Option
from utils.commands import slash_command
from discord.ui import View, Button
import sqlite3
import os
import re

CREATE_TABLES = [
    "CREATE TABLE IF NOT EXISTS votes(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, state INTEGER, user_id INTEGER, interaction_token TEXT)",
    "CREATE TABLE IF NOT EXISTS vote_choices(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, value INTEGER, vote REFERENCES votes)",
    "CREATE TABLE IF NOT EXISTS voters(id INTEGER PRIMARY KEY, vote REFERENSES votes)"
]
CREATE_VOTE = "INSERT INTO votes (name, state, user_id, interaction_token) VALUES (?, 0, ?, ?)"
CREATE_VOTE_CHOICE = "INSERT INTO vote_choices (name, value, vote) VALUES (?, 0, ?)"

VOTE_ID_REGEX = re.compile("#?(\\d+)")

class vote(commands.Cog):
    def __init__(self):
        self.db = sqlite3.connect(os.getenv("DATABASE_FILE"))
        cursor = self.db.cursor()

        for smt in CREATE_TABLES:
            cursor.execute(smt)

    @slash_command(description="투표를 시작합니다")
    async def vote(
        self,
        ctx: ApplicationContext,
        name: Option(str, description="투표 이름"),
        choices: Option(str, description="선택지(쉼표로 구분, 최대 25개)")
    ):
        await ctx.defer()

        cursor = self.db.cursor()
        cursor.execute(CREATE_VOTE, [name, ctx.author.id, ctx.interaction.token])
        vote_id = cursor.lastrowid

        choices = choices.split(",", 25)
        view = View()
        for choice in choices:
            cursor.execute(CREATE_VOTE_CHOICE, [choice.strip(), vote_id])
            choice_id = cursor.lastrowid

            button = Button(style = discord.ButtonStyle.primary, label = choice, custom_id = str(choice_id))
            view.add_item(button)

        self.db.commit()

        await ctx.respond(
            embed=discord.Embed(title=name, description="아래 버튼을 눌러 투표에 참여해주세요.", color=0xFF0000)
                .set_footer(text=f"Started by {ctx.author.display_name}", icon_url=ctx.author.display_avatar),
            view=view
        )

def setup(bot: discord.Bot):
    bot.add_cog(vote())
