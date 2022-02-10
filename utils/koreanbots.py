import logging
from typing import Optional

logger = logging.getLogger(__name__)


async def update_guild_count(token: Optional[str], bot_id: int, guild_count: int):
    if token is None:
        logger.warning("No Koreanbots token provided")
        logger.warning("Server count will not be updated")
        return

    try:
        from koreanbots.client import Koreanbots
        client = Koreanbots(api_key=token)
        await client.guildcount(bot_id, servers=guild_count)
    except ImportError:
        logger.warning("Koreanbots module is not installed")
        logger.warning("Server count will not be updated")
    except Exception:
        logger.exception("Error while updating Koreanbots server count")
