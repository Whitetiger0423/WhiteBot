import logging
import os
import discord
from discord.commands import SlashCommand, ApplicationContext, application_command
from utils.utils import apply_if_not_none
from typing import Callable, Optional

TEST_GUILD_ID = apply_if_not_none(os.getenv("TEST_GUILD_ID"), lambda x: int(x))

logger = logging.getLogger(__name__)

class ErrorHandlingSlashCommand(SlashCommand):
    def __init__(self, func: Callable, *args, **kwargs) -> None:
        super().__init__(func, *args, **kwargs)
        logger.info(f"{self.name} command registered")

        self._callback = func
        self.callback = self.error_handler

    def error_handler(self, ctx: ApplicationContext, **kwargs):
        try:
            self._callback(ctx, kwargs)
        except WhiteBotException as e:
            ctx.respond(embed=discord.Embed(
                title=e.title or "오류가 발생했어요",
                description=e.description,
                color=0xFF0000
            ))
        except Exception as e:
            logger.exception(f"Exception from {self.name}")
            ctx.respond(embed=discord.Embed(
                title="알 수 없는 오류가 발생했어요",
                description="잠시 후에 다시 시도해주세요",
                color=0xFF0000
            ))

class WhiteBotException(RuntimeError):
    def __init__(self, description: str, title: Optional[str] = None):
        self.description = description
        self.title = title

def slash_command(**kwargs):
    if TEST_GUILD_ID is not None:
        kwargs["guild_ids"] = [TEST_GUILD_ID]

    return application_command(cls=ErrorHandlingSlashCommand, **kwargs)
