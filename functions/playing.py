import discord
import random
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
from typing import List


class playing(commands.Cog):
    @slash_command(description="봇과 가위바위보 게임을 합니다.")
    async def rsp(
        self,
        ctx: ApplicationContext,
        user: Option(str, "낼 것을 선택하세요", choices=["가위", "바위", "보"]),
    ):
        rsp_table = ["가위", "바위", "보"]
        if user not in rsp_table:
            embed = discord.Embed(
                title="WhiteBot 오류", description="가위바위보 기능", color=0xFF0000
            )
            embed.add_field(
                name="오류 내용:", value="`가위, 바위, 보` 중에 하나를 입력해주세요.", inline=False
            )
            await ctx.respond(embed=embed)
        else:
            bot = random.choice(rsp_table)
            result = rsp_table.index(user) - rsp_table.index(bot)
            if result == 0:
                forsend = f"{user} vs {bot}\n비겼네요!"
            elif result == 1 or result == -2:
                forsend = f"{user} vs {bot}\n{ctx.author.display_name}님이 이겼어요!"
            else:
                forsend = f"{user} vs {bot}\n봇이 이겼습니다!"
            embed = discord.Embed(
                title="가위바위보",
                description=f"봇 vs {ctx.author.display_name}",
                color=0xFFFFFF,
            )
            embed.add_field(name="**결과:**", value=f"{forsend}", inline=False)
            await ctx.respond(embed=embed)

    @slash_command(description="주사위를 굴립니다.")
    async def dice(
        self,
        ctx: ApplicationContext,
        firstn: Option(int, "첫번째 숫자를 정하세요. 두번째 숫자가 없을 경우 범위는 0 ~ firstn으로 결정됩니다."),
        secondn: Option(
            int, "두번째 숫자가 있을 경우 범위는 firstn ~ secondn으로 결정됩니다. ", required=False
        ),
    ):
        try:
            if firstn < 1:
                embed = discord.Embed(
                    title="WhiteBot 오류", description="주사위 기능", color=0xFF0000
                )
                embed.add_field(name="오류 내용:", value="자연수 값만 허용됩니다.", inline=False)
                await ctx.respond(embed=embed)
            elif secondn:
                embed = discord.Embed(
                    title="주사위", description=f"{firstn} ~ {secondn}", color=0xFFFFFF
                )
                embed.add_field(
                    name="**결과:**",
                    value=f"주사위를 굴렸더니 {random.randint(firstn, secondn)}(이)가 나왔어요!",
                    inline=False,
                )
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(
                    title="주사위", description=f"1 ~ {firstn}", color=0xFFFFFF
                )
                embed.add_field(
                    name="**결과:**",
                    value=f"주사위를 굴렸더니 {random.randint(1, firstn)}(이)가 나왔어요!",
                    inline=False,
                )
                await ctx.respond(embed=embed)
        except:
            embed = discord.Embed(
                title="WhiteBot 오류", description="주사위 기능", color=0xFF0000
            )
            embed.add_field(
                name="오류 내용:",
                value="1. 자연수가 아닌 수를 쓰셨는지 확인해주세요.\n2. 첫번째 숫자가 두번째 숫자보다 더 큰지 확인해주세요.",
                inline=False,
            )
            await ctx.respond(embed=embed)

    @slash_command(description="틱택토(삼목) 게임을 진행합니다.")
    async def tictactoe(self, ctx: ApplicationContext, rival: Option(discord.User, description="같이 게임을 할 유저를 선택하세요")):
        if rival.bot:
            embed = discord.Embed(
                    title="WhiteBot 오류", description="틱택토 기능", color=0xFF0000
                )
            embed.add_field(name="오류 내용:", value="봇과는 대결할 수 없습니다.", inline=False)
            await ctx.respond(embed=embed)
        else:await ctx.respond("틱택토(삼목) 게임을 시작합니다. X부터 시작해요!", view=TicTacToe(ctx.user.id, rival.id))


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            if interaction.user.id != view.x_member_id:
                return
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "O의 차례입니다!"
        else:
            if interaction.user.id != view.o_member_id:
                return
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "X의 차례입니다!"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X 승리!"
            elif winner == view.O:
                content = "O 승리!"
            else:
                content = "비겼습니다."

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, player_id: discord.Member, rival_id: discord.Member):
        super().__init__()

        self.x_member_id = player_id
        self.o_member_id = rival_id

        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


def setup(bot):
    bot.add_cog(playing())
