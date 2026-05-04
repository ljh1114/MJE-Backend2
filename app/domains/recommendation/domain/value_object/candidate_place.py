from dataclasses import dataclass

from app.domains.recommendation.domain.value_object.place_type import PlaceType


@dataclass(frozen=True)
class CandidatePlace:
    id: int
    name: str
    category: str
    road_address: str
    address: str
    mapx: str
    mapy: str
    link: str
    telephone: str
    keyword: str
    collected_at: str
    place_type: PlaceType
