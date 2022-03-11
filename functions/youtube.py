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
import logging
from discord.ext import commands
from discord.http import Route
from discord.commands import ApplicationContext
from utils.commands import slash_command

logger = logging.getLogger(__name__)


class youtube(commands.Cog):
    @slash_command(description="유튜브 투게더에 접속할 수 있는 링크를 전송합니다. 음성 채널에 연결되어 있어야 됩니다.")
    async def 유튜브(self, ctx: ApplicationContext):
        voice = ctx.author.voice

        if voice is not discord.VoiceState:
            logger.debug(
                "Unable to execute: member is not connected to a voice channel"
            )
            embed = discord.Embed(
                description="이 명령을 사용하려면 사용자가 음성 채널에 있어야합니다.", color=0xFF0000
            )
            return await ctx.respond(embed=embed)

        r = Route("POST", "/channels/{channel_id}/invites", channel_id=voice.channel.id)

        payload = {
            "max_age": 0,
            "target_type": 2,
            "target_application_id": 755600276941176913,
        }

        try:
            code = (await self.bot.http.request(r, json=payload))["code"]

            embed = discord.Embed(
                title="유튜브 투게더",
                description=f"[여기를 클릭해주세요](https://discord.gg/{code})",
                color=0xFFFFFF,
            )
            embed.set_footer(text="일부 서버에선 작동하지 않는 베타 기능입니다.")
            await ctx.respond(embed=embed)

        except discord.Forbidden as e:
            logger.debug(
                "Forbidden request\n=> Payload: %s\n=> Response: %s",
                str(payload),
                e.text,
            )
            embed = discord.Embed(description="초대 코드 생성 권한이 없습니다.", color=0xFF0000)
            await ctx.respond(embed=embed)
        except discord.HTTPException as e:
            logger.error(
                "Discord API has returned %d\n=> Payload: %s\n=> Response: %s",
                e.code,
                str(payload),
                e.text,
            )
            embed = discord.Embed(
                description="오류가 발생했어요. 잠시 후에 다시 시도해주세요", color=0xFF0000
            )
            await ctx.respond(embed=embed)
        except Exception:
            logger.exception("Unexpected exception occurred")
            embed = discord.Embed(
                description="오류가 발생했어요. 잠시 후에 다시 시도해주세요", color=0xFF0000
            )
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(youtube())
