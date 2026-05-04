from typing import List

import httpx

from app.domains.recommendation.service.search_client_interface import (
    RawPlaceResult,
    SearchClientInterface,
)

_LOCAL_SEARCH_URL = "https://openapi.naver.com/v1/search/local.json"
_TIMEOUT_SECONDS = 3.0


class NaverSearchClient(SearchClientInterface):
    def __init__(self, client_id: str, client_secret: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret

    def search_places(self, query: str, display: int = 5) -> List[RawPlaceResult]:
        try:
            response = httpx.get(
                _LOCAL_SEARCH_URL,
                params={"query": query, "display": display, "sort": "comment"},
                headers={
                    "X-Naver-Client-Id": self._client_id,
                    "X-Naver-Client-Secret": self._client_secret,
                },
                timeout=_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            items = response.json().get("items", [])
            return [
                RawPlaceResult(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    category=item.get("category", ""),
                    description=item.get("description", ""),
                    telephone=item.get("telephone", ""),
                    address=item.get("address", ""),
                    road_address=item.get("roadAddress", ""),
                    mapx=item.get("mapx", ""),
                    mapy=item.get("mapy", ""),
                )
                for item in items
            ]
        except Exception:
            return []
