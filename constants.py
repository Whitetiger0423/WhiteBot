class Constants:
    VERSION = "1.11.0"
    EMOJI = {
        "check": "<a:check:824251178493411368>",
        "sleet": "<:sleet:1018802491665678346>"
    }
    EMBED_COLOR = {
        "default": 0xffffff,
        "success": 0x00FFC6,
        "error": 0xFF0000
    }
    COVID_SELECTORS = {
        "death": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_graph > table > tbody > tr:nth-child(1) > td:nth-child(2) > span",
        "confirmed": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_graph > table > tbody > tr:nth-child(1) > td:nth-child(5) > span",
        "total_death": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_num > div:nth-child(1)",
        "total_confirmed": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_num > div:nth-child(2)"
    }
