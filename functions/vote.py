import discord
from discord.ext import commands
from discord.commands import ApplicationContext, Option
from utils.commands import slash_command
from discord.ui import View, Button
import sqlite3
import os
import logging

logger = logging.getLogger(__name__)


class vote(commands.Cog):
    def __init__(self):
        db_path = os.getenv("DATABASE_PATH") or ":memory:"
        self.conn = sqlite3.connect(db_path)

        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS votes(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, state INTEGER, user_id INTEGER, interaction_token TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS vote_choices(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, vote REFERENCES votes)")
        cursor.execute("CREATE TABLE IF NOT EXISTS voters(id INTEGER, choice REFERENCES voice_choices)")
        cursor.close()

    @slash_command(description="투표를 시작합니다")
    async def vote(
        self,
        ctx: ApplicationContext,
        name: Option(str, description="새로 만들 투표의 이름입니다"),
        choices: Option(str, description="투표의 선택지입니다(쉼표로 구분, 최대 25개)")
    ):
        await ctx.defer()

        cursor = self.conn.cursor()

        cursor.execute(f"INSERT INTO votes (name, state, user_id, interaction_token) VALUES ('{name}', 0, {ctx.author.id}, '{ctx.interaction.token}')")
        vote_id = cursor.lastrowid

        choices = choices.split(",", 25)
        view = View()
        for choice in choices:
            choice_name = choice.strip()
            cursor.execute(f"INSERT INTO vote_choices (name, vote) VALUES ('{choice_name}', {vote_id})")
            choice_id = cursor.lastrowid

            button = Button(style=discord.ButtonStyle.primary, label=choice_name, custom_id=str(choice_id))
            button.callback = self.button_callback
            view.add_item(button)

        await ctx.respond(
            embed=discord.Embed(title=f"#{vote_id} {name}", description="아래 버튼을 눌러 투표에 참여해주세요.", color=0xFFFFFF)
            .set_footer(text=f"Started by {ctx.author.display_name}", icon_url=ctx.author.display_avatar),
            view=view
        )
        cursor.close()
        self.conn.commit()

    async def button_callback(self, interaction: discord.Interaction):
        cursor = self.conn.cursor()

        user_id = interaction.user.id
        choice_id = interaction.data["custom_id"]

        cursor.execute(f"SELECT vote FROM vote_choices WHERE id={choice_id}")
        (vote_id,) = cursor.fetchone()

        cursor.execute(f"SELECT state FROM votes WHERE id={vote_id}")
        (vote_state,) = cursor.fetchone()
        if vote_state != 0:
            return await interaction.response.send_message("투표가 종료되었습니다", ephemeral=True)

        cursor.execute(f"INSERT INTO voters (id, choice) VALUES ({user_id}, {choice_id})")

        cursor.close()
        self.conn.commit()

    @slash_command(description="투표를 종료합니다")
    async def end_vote(self, ctx: ApplicationContext, vote_id: Option(int, description="종료할 투표 아이디입니다")):
        await ctx.defer()

        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE votes SET state=1 WHERE id={vote_id}")

        cursor.execute(f"SELECT name FROM votes WHERE id={vote_id}")
        (vote_name,) = cursor.fetchone()
        embed = discord.Embed(title=f"#{vote_id} {vote_name}", description="투표가 종료되었습니다", color=0xFFFFFF)

        cursor.execute(f"SELECT id, name FROM vote_choices WHERE vote={vote_id}")
        for (choice_id, choice_name) in cursor.fetchall():
            cursor.execute(f"SELECT * FROM voters WHERE choice={choice_id}")
            voter_count = len(cursor.fetchall())
            embed.add_field(name=choice_name, value=voter_count)

        await ctx.respond(embed=embed)
        cursor.close()
        self.conn.commit()


def setup(bot: discord.Bot):
    bot.add_cog(vote())
