from dataclasses import dataclass, field
from typing import List

from app.domains.recommendation.service.dto.response.get_recommendation_response_dto import (
    RecommendationCourseItemDto,
)


@dataclass
class RecommendationSessionDto:
    area: str
    start_time: str
    transport: str
    courses: List[RecommendationCourseItemDto] = field(default_factory=list)
