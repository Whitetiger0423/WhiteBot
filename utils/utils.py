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

from typing import Callable


def to_querystring(data: dict) -> str:
    """사전을 쿼리스트링 형태의 문자열로 변환합니다.

    | Args:
    |   data (dict): 쿼리스트링으로 변환할 사전

    | Returns:
    |   str: 변환된 쿼리스트링 형태의 문자열
        url body form으로도 사용하기 위해 맨 앞에 ?가 붙어있지 않습니다.
    """
    parts = [f"{key}={value}" for key, value in data.items()]
    return "&".join(parts)


def apply_if_not_none(value, block: Callable):
    if value is not None:
        value = block(value)
    return value


def to_dict(data, get_key: Callable, get_value: Callable = lambda x: x) -> dict:
    items = {}
    for datum in data:
        items[get_key(datum)] = get_value(datum)
    return items
