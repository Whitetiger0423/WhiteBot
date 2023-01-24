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

import os
from discord.commands import SlashCommand, application_command
from utils.utils import apply_if_not_none

TEST_GUILD_ID = apply_if_not_none(os.getenv("TEST_GUILD_ID"), lambda x: int(x))


def slash_command(**kwargs):
    if TEST_GUILD_ID is not None:
        kwargs["guild_ids"] = [TEST_GUILD_ID]

    return application_command(cls=SlashCommand, **kwargs)
