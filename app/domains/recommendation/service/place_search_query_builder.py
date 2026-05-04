from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.domains.recommendation.domain.value_object.activity_type import ActivityKind
from app.domains.recommendation.domain.value_object.place_type import PlaceType

_RESTAURANT_TEMPLATES = [
    ("{area} 맛집",       "맛집"),
    ("{area} 식당",       "식당"),
    ("{area} 데이트 식당", "데이트 식당"),
    ("{area} 점심",       "점심"),
    ("{area} 저녁",       "저녁"),
]

_CAFE_TEMPLATES = [
    ("{area} 카페",      "카페"),
    ("{area} 디저트 카페", "디저트 카페"),
    ("{area} 감성 카페",  "감성 카페"),
]

_ACTIVITY_TEMPLATES: Dict[str, List[str]] = {
    ActivityKind.EXHIBITION.value:  ["{area} 전시",       "{area} 미술관"],
    ActivityKind.WALK.value:        ["{area} 산책",       "{area} 공원"],
    ActivityKind.SHOPPING.value:    ["{area} 쇼핑",       "{area} 소품샵"],
    ActivityKind.POPUP.value:       ["{area} 팝업스토어"],
    ActivityKind.WORKSHOP.value:    ["{area} 공방",       "{area} 체험"],
    ActivityKind.INDOOR_PLAY.value: ["{area} 보드게임",   "{area} 방탈출"],
    ActivityKind.MOVIE.value:       ["{area} 영화관"],
    ActivityKind.KARAOKE.value:     ["{area} 노래방"],
    ActivityKind.BAR.value:         ["{area} 술집",       "{area} 와인바"],
    ActivityKind.NIGHT_VIEW.value:  ["{area} 야경"],
    ActivityKind.SPORTS.value:      ["{area} 볼링",       "{area} 스포츠"],
    ActivityKind.LATE_NIGHT.value:  ["{area} 심야데이트"],
}


@dataclass
class PlaceSearchQuery:
    query: str
    keyword_label: str
    place_type: PlaceType
    activity_kind: Optional[ActivityKind] = field(default=None)


class PlaceSearchQueryBuilder:
    def build_restaurant_queries(self, area: str) -> List[PlaceSearchQuery]:
        return [
            PlaceSearchQuery(
                query=tmpl.format(area=area),
                keyword_label=label,
                place_type=PlaceType.RESTAURANT,
            )
            for tmpl, label in _RESTAURANT_TEMPLATES
        ]

    def build_cafe_queries(self, area: str) -> List[PlaceSearchQuery]:
        return [
            PlaceSearchQuery(
                query=tmpl.format(area=area),
                keyword_label=label,
                place_type=PlaceType.CAFE,
            )
            for tmpl, label in _CAFE_TEMPLATES
        ]

    def build_activity_queries(self, area: str) -> List[PlaceSearchQuery]:
        queries: List[PlaceSearchQuery] = []
        for kind_value, templates in _ACTIVITY_TEMPLATES.items():
            activity_kind = ActivityKind(kind_value)
            for tmpl in templates:
                query = tmpl.format(area=area)
                queries.append(PlaceSearchQuery(
                    query=query,
                    keyword_label=query,
                    place_type=PlaceType.ACTIVITY,
                    activity_kind=activity_kind,
                ))
        return queries
