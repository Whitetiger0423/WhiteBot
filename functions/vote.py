import discord
from discord.ext import commands
from discord.commands import ApplicationContext, Option
from utils.commands import slash_command
from discord.ui import View, Button
import sqlite3
import os
import re
import logging

logger = logging.getLogger(__name__)

class vote(commands.Cog):
    VOTE_ID_REGEX = re.compile("#?(\\d+)")

    def __init__(self):
        db_path = os.getenv("DATABASE_PATH") or ":memory:"
        self.service = vote_service(db_path)
        self.service.create_tables()

    @slash_command(description="투표를 시작합니다")
    async def vote(
        self,
        ctx: ApplicationContext,
        name: Option(str, description="투표 이름"),
        choices: Option(str, description="선택지(쉼표로 구분, 최대 25개)")
    ):
        await ctx.defer()

        vote_id = self.service.create_vote(name, ctx.author.id, ctx.interaction.token)
        logger.info(f"vote entity created(id: {vote_id}, name: {name})")

        choices = choices.split(",", 25)
        view = View()
        for choice in choices:
            choice_name = choice.strip()
            choice_id = self.service.create_vote_choice(choice_name, vote_id)
            logger.info(f"vote choice entity created(id: {choice_id}, name: {choice_name}, vote: {vote_id})")

            button = Button(style = discord.ButtonStyle.primary, label = choice_name, custom_id = str(choice_id))
            button.callback = self.button_callback
            view.add_item(button)

        await ctx.respond(
            embed=discord.Embed(title=f"#{vote_id} {name}", description="아래 버튼을 눌러 투표에 참여해주세요.", color=0xFFFFFF)
                .set_footer(text=f"Started by {ctx.author.display_name}", icon_url=ctx.author.display_avatar),
            view=view
        )

    async def button_callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        choice_id = interaction.data["custom_id"]
        vote_id = self.service.get_choice(choice_id)[3]

        if self.service.get_vote(vote_id)[2] != 0:
            return await interaction.response.send_message("투표가 종료되었습니다", ephemeral=True)

        self.service.create_voter(user_id, choice_id)
        logger.info(f"voter entity created(id: {user_id}, choice: {choice_id})")

    @slash_command(description="투표를 끝냅니다")
    async def end_vote(self, ctx: ApplicationContext, _vote_id: Option(str, description="투표 아이디(미입력시 가장 최근에 시작한 투표)", required = False)):
        await ctx.defer()

        if _vote_id is None:
            vote_id = self.service.get_latest_vote(ctx.user.id)
        else:
            regex_match = self.VOTE_ID_REGEX.match(_vote_id)
            if regex_match is None:
                return await ctx.respond("투표 아이디가 올바르지 않습니다", ephemeral=True)
            vote_id = regex_match.group(1)

        self.service.set_vote_state(1, vote_id)

        vote = self.service.get_vote(vote_id)
        embed = discord.Embed(title="투표 결과", description=f"#{vote_id} {vote[1]}\n투표가 종료되었습니다", color=0xFFFFFF)

        for choice in self.service.get_choices(vote_id):
            embed.add_field(name=choice[1], value=self.service.get_voter_count(choice[0]))

        ctx.respond(embed=embed)


class vote_service():
    CREATE_TABLES = [
        "CREATE TABLE IF NOT EXISTS votes(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, state INTEGER, user_id INTEGER, interaction_token TEXT)",
        "CREATE TABLE IF NOT EXISTS vote_choices(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, value INTEGER, vote REFERENCES votes)",
        "CREATE TABLE IF NOT EXISTS voters(id INTEGER PRIMARY KEY, choice REFERENCES voice_choices)"
    ]
    CREATE_VOTE = "INSERT INTO votes (name, state, user_id, interaction_token) VALUES (?, 0, ?, ?)"
    CREATE_VOTE_CHOICE = "INSERT INTO vote_choices (name, value, vote) VALUES (?, 0, ?)"
    CREATE_VOTER = "INSERT INTO voters (id, choice) VALUES (?, ?)"

    GET_LATEST_VOTE = "SELECT * FROM votes WHERE user_id=? ORDER BY id DESC LIMIT 1"
    GET_VOTE = "SELECT * FROM votes WHERE id=?"
    GET_CHOICE = "SELECT * FROM choices WHERE id=?"
    GET_CHOICES = "SELECT * FROM choices WHERE vote=?"
    GET_VOTER_COUNT = "SELECT * FROM voters WHERE choice=?"

    SET_VOTE_STATE = "UPDATE votes SET state=? WHERE id=?"

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)

    def create_tables(self):
        cursor = self.conn.cursor()
        for smt in self.CREATE_TABLES:
            cursor.execute(smt)

    def create_vote(self, name, user_id, interaction_token) -> int:
        cursor = self.conn.execute(self.CREATE_VOTE, (name, user_id, interaction_token))
        return cursor.lastrowid

    def create_vote_choice(self, name, vote) -> int:
        cursor = self.conn.execute(self.CREATE_VOTE_CHOICE, (name, vote))
        return cursor.lastrowid

    def create_voter(self, id, choice) -> int:
        cursor = self.conn.execute(self.CREATE_VOTER, (id, choice))
        return cursor.lastrowid

    def get_latest_vote(self, user_id) -> int:
        cursor = self.conn.execute(self.GET_LATEST_VOTE, (user_id))
        return cursor.lastrowid

    def get_vote(self, vote_id) -> tuple:
        cursor = self.conn.execute(self.GET_VOTE, (vote_id))
        return cursor.fetchone()

    def get_choice(self, choice_id) -> tuple:
        cursor = self.conn.execute(self.GET_CHOICE, (choice_id))
        return cursor.fetchone()

    def get_choices(self, vote_id) -> list[tuple]:
        cursor = self.conn.execute(self.GET_CHOICES, (vote_id))
        return cursor.fetchall()

    def get_voter_count(self, choice_id) -> int:
        cursor = self.conn.execute(self.GET_VOTER_COUNT, (choice_id))
        return cursor.rowcount

    def set_vote_state(self, state, vote_id) -> None:
        self.conn.execute(self.SET_VOTE_STATE, (state, vote_id))


def setup(bot: discord.Bot):
    bot.add_cog(vote())
