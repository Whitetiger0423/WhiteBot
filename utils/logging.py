import logging

RESET = "\033[0m"
CYAN = "\033[1;36m"
COLORS = {
    "DEBUG": "\033[1;37m", # WHITE
    "INFO": "\033[1;34m",  # BLUE
    "WARNING": "\033[1;33m", # YELLO
    "ERROR": "\033[1;35m", # MAGENTA
    "CRITICAL": "\033[1;31m" # RED
}

class HighlightingFormatter(logging.Formatter):
    def __init__(self, format, datefmt, style):
        super().__init__(format, datefmt, style)

    def format(self, record: logging.LogRecord):
        space = 8-len(record.levelname)
        levelname_color = COLORS[record.levelname] + record.levelname + RESET + " " * space
        record.levelname = levelname_color

        space = 15-len(record.name)
        if (space < 0): space = 0
        record.name = CYAN + record.name + RESET + " " * space

        return super().format(record)

def setup_logging():
    formatter = HighlightingFormatter("{asctime} {levelname} {name}: {message}", "%Y-%m-%d %H:%M:%S", "{")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.basicConfig(handlers=[handler], level=logging.INFO)
