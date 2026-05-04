import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Set, Tuple

from app.domains.recommendation.domain.value_object.candidate_place import CandidatePlace
from app.domains.recommendation.service.place_search_query_builder import (
    PlaceSearchQuery,
    PlaceSearchQueryBuilder,
)
from app.domains.recommendation.service.search_client_interface import SearchClientInterface

_MIN_REQUIRED = 5
_DISPLAY_PER_QUERY = 5
_HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


def _strip_html(text: str) -> str:
    return _HTML_TAG_PATTERN.sub("", text).strip()


def _place_id(name: str, address: str) -> int:
    return abs(hash((name, address))) % (10**9)


@dataclass
class PlaceCandidateCollection:
    restaurants: List[CandidatePlace]
    cafes: List[CandidatePlace]
    activities: List[CandidatePlace]
    shortage_reasons: List[str]


class PlaceCandidateCollector:
    def __init__(self, client: SearchClientInterface) -> None:
        self._client = client
        self._query_builder = PlaceSearchQueryBuilder()

    def collect(self, area: str) -> PlaceCandidateCollection:
        restaurants = self._collect_by_queries(self._query_builder.build_restaurant_queries(area))
        cafes = self._collect_by_queries(self._query_builder.build_cafe_queries(area))
        activities = self._collect_by_queries(self._query_builder.build_activity_queries(area))

        shortage_reasons: List[str] = []
        if len(restaurants) < _MIN_REQUIRED:
            shortage_reasons.append(
                f"레스토랑 후보 부족 (수집: {len(restaurants)}개, 최소: {_MIN_REQUIRED}개)"
            )
        if len(cafes) < _MIN_REQUIRED:
            shortage_reasons.append(
                f"카페 후보 부족 (수집: {len(cafes)}개, 최소: {_MIN_REQUIRED}개)"
            )
        if len(activities) < _MIN_REQUIRED:
            shortage_reasons.append(
                f"액티비티 후보 부족 (수집: {len(activities)}개, 최소: {_MIN_REQUIRED}개)"
            )

        return PlaceCandidateCollection(
            restaurants=restaurants,
            cafes=cafes,
            activities=activities,
            shortage_reasons=shortage_reasons,
        )

    def _collect_by_queries(self, queries: List[PlaceSearchQuery]) -> List[CandidatePlace]:
        seen: Set[Tuple[str, str]] = set()
        results: List[CandidatePlace] = []
        collected_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        for search_query in queries:
            try:
                raw_items = self._client.search_places(search_query.query, _DISPLAY_PER_QUERY)
            except Exception:
                continue

            for raw in raw_items:
                address = raw.road_address or raw.address
                if not address:
                    continue

                name = _strip_html(raw.title)
                dedup_key = (name, address)
                if dedup_key in seen:
                    continue
                seen.add(dedup_key)

                results.append(CandidatePlace(
                    id=_place_id(name, address),
                    name=name,
                    category=raw.category,
                    road_address=raw.road_address,
                    address=raw.address,
                    mapx=raw.mapx,
                    mapy=raw.mapy,
                    link=raw.link,
                    telephone=raw.telephone,
                    keyword=search_query.keyword_label,
                    collected_at=collected_at,
                    place_type=search_query.place_type,
                    activity_kind=search_query.activity_kind,
                ))

        return results
