import os
from discord.commands import slash_command
from utils.utils import apply_if_not_none

TEST_GUILD_ID = apply_if_not_none(os.getenv("TEST_GUILD_ID"), lambda x : int(x))

def slash_command(**kwargs):
    if TEST_GUILD_ID is not None:
        kwargs['guild_ids'] = [TEST_GUILD_ID]

    return slash_command(**kwargs)
