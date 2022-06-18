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


def fromtolang(selectedlang: str) -> str:
    if lang == "ko":
        choices = [
            OptionChoice("영어", "ko:en"),
            OptionChoice("일본어", "ko:ja"),
            OptionChoice("중국어", "ko:zh-CN"),
            OptionChoice("프랑스어", "ko:fr"),
            OptionChoice("베트남어", "ko:vi"),
            OptionChoice("인도네시아어", "ko:id"),
            OptionChoice("독일어", "ko:de"),
            OptionChoice("태국어", "ko:th"),
            OptionChoice("러시아어", "ko:ru"),
            OptionChoice("스페인어", "ko:es"),
            OptionChoice("인도어", "ko:it"),
        ]
    elif lang == "en":
        choices = [
            OptionChoice("한국어", "en:ko"),
            OptionChoice("일본어", "en:ja"),
            OptionChoice("중국어", "en:zh-CN"),
            OptionChoice("프랑스어", "en:fr"),
        ]
    elif lang == "ja":
        choices = [
            OptionChoice("한국어", "ja:ko"),
            OptionChoice("영어", "ja:en"),
            OptionChoice("중국어", "ja:zh-CN"),
        ]
    elif lang == "zh-CN":
        choices = [
            OptionChoice("한국어", "zh-CN:ko"),
            OptionChoice("영어", "zh-CN:en"),
            OptionChoice("일본어", "zh-CN:ja"),
        ]
    elif lang == "fr":
        choices = [OptionChoice("한국어", "fr:ko"), OptionChoice("영어", "fr:en")]
    elif lang == "vi":
        choices = [OptionChoice("한국어", "vi:ko")]
    elif lang == "id":
        choices = [OptionChoice("한국어", "id:ko")]
    elif lang == "th":
        choices = [OptionChoice("한국어", "th:ko")]
    elif lang == "de":
        choices = [OptionChoice("한국어", "de:ko")]
    elif lang == "ru":
        choices = [OptionChoice("한국어", "ru:ko")]
    elif lang == "es":
        choices = [OptionChoice("한국어", "es:ko")]
    elif lang == "it":
        choices = [OptionChoice("한국어", "it:ko")]
    return choices
