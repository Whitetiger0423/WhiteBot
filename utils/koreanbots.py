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
