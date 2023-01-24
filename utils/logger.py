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

RESET = "\033[0m"
CYAN = "\033[1;36m"
COLORS = {
    "DEBUG": "\033[1;37m",    # WHITE
    "INFO": "\033[1;34m",     # BLUE
    "WARNING": "\033[1;33m",  # YELLOW
    "ERROR": "\033[1;35m",    # MAGENTA
    "CRITICAL": "\033[1;31m"  # RED
}


class HighlightingFormatter(logging.Formatter):
    def __init__(self, format_str, datefmt, style):
        super().__init__(format_str, datefmt, style)

    def format(self, record: logging.LogRecord):
        space = 8 - len(record.levelname)
        levelname_color = COLORS[record.levelname] + record.levelname + RESET + " " * space
        record.levelname = levelname_color

        space = 15 - len(record.name)
        if (space < 0):
            space = 0
        record.name = CYAN + record.name + RESET + " " * space

        return super().format(record)


def setup_logging():
    formatter = HighlightingFormatter("{asctime} {levelname} {name}: {message}", "%Y-%m-%d %H:%M:%S", "{")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.basicConfig(handlers=[handler], level=logging.INFO)
