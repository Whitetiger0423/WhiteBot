import discord
from discord.ext import commands
from discord.commands import ApplicationContext, Option, AutocompleteContext, OptionChoice
from utils.commands import slash_command
from discord.ui import View, Button
import sqlite3
import os
import logging

logger = logging.getLogger(__name__)


class Vote(commands.Cog):
    def __init__(self, bot: discord.Bot):
        db_path = os.getenv("DATABASE_PATH") or ":memory:"
        self.conn = sqlite3.connect(db_path)
        logger.debug("Connected to database: %s", db_path)

        self.create_tables()
        bot.loop.call_soon(self.restore_state, bot)

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS votes(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, state INTEGER, user_id INTEGER, message_id INTEGER, flag INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS vote_choices(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, color INTEGER, emoji TEXT, vote REFERENCES votes)")
        cursor.execute("CREATE TABLE IF NOT EXISTS voters(id INTEGER, vote REFERENCES votes, choice REFERENCES voice_choices)")
        cursor.close()
        self.conn.commit()

    def restore_state(self, bot: discord.Bot):
        logger.info("Restoring previous state")
        cursor = self.conn.execute("SELECT id FROM votes WHERE state=0")
        for (vote_id,) in cursor.fetchall():
            logger.info("Restoring vote #%d", vote_id)
            view = View(timeout=None)
            view.vote_id = vote_id

            param = {"vote_id": vote_id}
            cursor.execute("SELECT id, name FROM vote_choices WHERE vote=:vote_id", param)
            for (choice_id, choice_name) in cursor.fetchall():
                button = Button(style=discord.ButtonStyle.primary, label=choice_name, custom_id=f"vote:{choice_id}")
                button.callback = self.button_callback
                view.add_item(button)

            button = Button(style=discord.ButtonStyle.danger, label="투표 취소", emoji="🔥", custom_id=f"vote:cancel:{vote_id}")
            button.callback = self.cancel_vote
            view.add_item(button)

            bot.add_view(view)

    @slash_command(description="투표를 시작합니다")
    async def vote(
        self,
        ctx: ApplicationContext,
        name: Option(str, description="새로 만들 투표의 이름입니다"),
        choices: Option(str, description="투표의 선택지입니다(쉼표로 구분, 최대 20개)"),
        mv: Option(str, description="중복 투표 가능 여부입니다", choices=["허용"], required=False)
    ):
        await ctx.defer()

        cursor = self.conn.cursor()

        flag = 0
        if mv == "허용":
            flag |= 1

        param = {"name": name, "state": 0, "user_id": ctx.author.id, "flag": flag}
        cursor.execute("INSERT INTO votes (name, state, user_id, flag) VALUES (:name, :state, :user_id, :flag)", param)
        vote_id = cursor.lastrowid
        logger.debug("Created new vote(id=%d, name=%s, user=%d, flag=%d)", vote_id, name, ctx.author.id, flag)

        choices = choices.split(",", 20)
        view = View(timeout=None)
        view.vote_id = vote_id
        for choice in choices:
            choice_name = choice.strip()
            param = {"name": choice_name, "vote": vote_id}
            cursor.execute("INSERT INTO vote_choices (name, vote) VALUES (:name, :vote)", param)
            choice_id = cursor.lastrowid
            logger.debug("Created new vote choice(id=%d, name=%s, vote=%d)", choice_id, choice_name, vote_id)

            button = Button(style=discord.ButtonStyle.primary, label=choice_name, custom_id=f"vote:{choice_id}")
            button.callback = self.button_callback
            view.add_item(button)

        button = Button(style=discord.ButtonStyle.danger, label="투표 취소", emoji="🔥", custom_id=f"vote:cancel:{vote_id}")
        button.callback = self.cancel_vote
        view.add_item(button)

        msg = await ctx.respond(
            embed=discord.Embed(title=f"#{vote_id} {name}", description="아래 버튼을 눌러 투표에 참여해주세요.", color=0xFFFFFF)
            .set_footer(text=f"Started by {ctx.author.display_name}", icon_url=ctx.author.display_avatar),
            view=view
        )
        param = {"message_id": msg.id, "id": vote_id}
        cursor.execute("UPDATE votes SET message_id=:message_id WHERE id=:id", param)
        logger.debug("Updated vote(id=%d, message=%d)", vote_id, msg.id)

        cursor.close()
        self.conn.commit()

    async def button_callback(self, interaction: discord.Interaction):
        cursor = self.conn.cursor()

        user_id = interaction.user.id
        choice_id = int(interaction.data["custom_id"][5:])

        param = {"id": choice_id}
        cursor.execute("SELECT name, vote FROM vote_choices WHERE id=:id", param)
        (choice_name, vote_id) = cursor.fetchone()

        logger.debug("Checking state of vote #%d", vote_id)
        param = {"id": vote_id}
        cursor.execute("SELECT state, flag FROM votes WHERE id=:id", param)
        (vote_state, flag) = cursor.fetchone()
        if vote_state != 0:
            logger.debug("Vote #%d is in non-zero state")
            return await interaction.response.send_message("투표가 이미 종료되었습니다", ephemeral=True)

        if not (flag & 1):
            logger.debug("Checking history of %d", user_id)
            param = {"id": user_id, "vote": vote_id}
            cursor.execute("SELECT * FROM voters WHERE id=:id AND vote=:vote", param)
            if cursor.fetchone() is not None:
                logger.debug("%d has already voted on vote #%d", user_id, vote_id)
                return await interaction.response.send_message("이미 투표하셨습니다", ephemeral=True)

        param = {"id": user_id, "vote": vote_id, "choice": choice_id}
        cursor.execute("INSERT INTO voters (id, vote, choice) VALUES (:id, :vote, :choice)", param)
        logger.debug("Created new voter(id=%d, vote=%d, choice=%d)", user_id, vote_id, choice_id)

        await interaction.response.send_message(f"{choice_name}에 투표하셨습니다.", ephemeral=True)

        cursor.close()
        self.conn.commit()

    async def cancel_vote(self, interaction: discord.Interaction):
        cursor = self.conn.cursor()

        user_id = interaction.user.id
        vote_id = int(interaction.data["custom_id"][12:])

        logger.debug("Checking state of vote #%d", vote_id)
        param = {"id": vote_id}
        cursor.execute("SELECT state FROM votes WHERE id=:id", param)
        (vote_state,) = cursor.fetchone()
        if vote_state != 0:
            logger.debug("Vote #%d is in non-zero state")
            return await interaction.response.send_message("투표가 이미 종료되었습니다", ephemeral=True)

        logger.debug("Checking history of %d", user_id)
        param = {"id": user_id, "vote": vote_id}
        cursor.execute("SELECT id FROM voters WHERE id=:id AND vote=:vote LIMIT 1", param)
        if cursor.fetchone() is None:
            logger.debug("%d has never voted on vote #%d", user_id, vote_id)
            return await interaction.response.send_message("투표하지 않았습니다", ephemeral=True)

        param = {"id": user_id, "vote": vote_id}
        cursor.execute("DELETE FROM voters WHERE id=:id AND vote=:vote", param)
        logger.debug("Deleted voter(id=%d, vote=%d)", user_id, vote_id)

        await interaction.response.send_message("투표 기록이 초기화되었습니다", ephemeral=True)
        cursor.close()
        self.conn.commit()

    async def vote_autocomplete(self, ctx: AutocompleteContext):
        cursor = self.conn.cursor()
        result = []
        value = ctx.value

        logger.debug("Autocompleting %s", value)

        param = {"user_id": ctx.interaction.user.id, "state": 0}
        cursor.execute("SELECT id, name FROM votes WHERE user_id=:user_id AND state=:state", param)
        for (id, name) in cursor:
            format = f"#{id} {name}"
            if value in format:
                result.append(OptionChoice(format, id))

        return result

    @slash_command(description="투표를 종료합니다")
    async def end_vote(self, ctx: ApplicationContext, vote: Option(int, description="종료할 투표를 선택해주세요", autocomplete=vote_autocomplete)):
        cursor = self.conn.cursor()

        param = {"id": vote}
        cursor.execute("SELECT name, state, user_id, message_id FROM votes WHERE id=:id", param)
        (vote_name, state, user_id, message_id) = cursor.fetchone()
        logger.debug("Fetched vote(id=%d, name=%s, state=%d, user=%d, message=%d)", vote, vote_name, state, user_id, message_id)

        if state != 0:
            return await ctx.respond("투표가 이미 종료되었습니다.", ephemeral=True)

        if ctx.author.id != user_id:
            return await ctx.respond("투표는 투표를 시작한 사람만 종료할 수 있습니다.", ephemeral=True)

        param = {"state": 1, "id": vote}
        cursor.execute("UPDATE votes SET state=:state WHERE id=:id", param)
        for view in ctx.bot.persistent_views:
            if hasattr(view, "vote_id") and view.vote_id == vote:
                view.stop()
                logger.debug("View for vote #%d has stopped", vote)
                break

        embed = discord.Embed(title=f"#{vote} {vote_name}", description="투표가 종료되었습니다", color=0xFFFFFF)

        await ctx.channel.get_partial_message(message_id).edit(embed=embed.copy(), view=None)

        param = {"vote": vote}
        cursor.execute("SELECT id, name FROM vote_choices WHERE vote=:vote", param)
        for (choice_id, choice_name) in cursor.fetchall():
            param = {"choice": choice_id}
            cursor.execute("SELECT * FROM voters WHERE choice=:choice", param)
            voter_count = len(cursor.fetchall())
            embed.add_field(name=choice_name, value=voter_count)

        await ctx.respond(embed=embed)
        cursor.close()
        self.conn.commit()


def setup(bot: discord.Bot):
    bot.add_cog(Vote(bot))
