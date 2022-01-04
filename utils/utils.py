def to_querystring(data: dict) -> str:
    """사전을 쿼리스트링 형태의 문자열로 변환합니다.

    | Args:
    |   data (dict): 쿼리스트링으로 변환할 사전

    | Returns:
    |   str: 변환된 쿼리스트링 형태의 문자열
        url body form으로도 사용하기 위해 맨 앞에 ?가 붙어있지 않습니다.
    """
    parts = [f"{key}={value}" for key, value in data.items()]
    return '&'.join(parts)
