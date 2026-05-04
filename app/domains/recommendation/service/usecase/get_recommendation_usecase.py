import uuid
from datetime import datetime

from app.domains.recommendation.domain.value_object.recommendation_place import RecommendationPlace
from app.domains.recommendation.repository.recommendation_session_repository_interface import (
    RecommendationSessionRepositoryInterface,
)
from app.domains.recommendation.service.dto.recommendation_session_dto import RecommendationSessionDto
from app.domains.recommendation.service.dto.request.get_recommendation_request_dto import (
    GetRecommendationRequestDto,
)
from app.domains.recommendation.service.dto.response.get_recommendation_response_dto import (
    GetRecommendationResponseDto,
    RecommendationCourseItemDto,
    RecommendationPlaceDto,
)

_MOCK_TEMPLATES = [
    {
        "grade": "best",
        "restaurant": {"name": "한우 명가", "category": "음식점 > 한식 > 소고기,돼지고기", "keyword": "한우 맛집 데이트"},
        "cafe": {"name": "루프탑 카페", "category": "카페 > 커피전문점", "keyword": "루프탑 데이트 카페"},
        "activity": {"name": "VR 체험관", "category": "레저 > 오락 > VR체험", "keyword": "커플 VR 체험"},
    },
    {
        "grade": "optional",
        "restaurant": {"name": "스시 오마카세", "category": "음식점 > 일식 > 초밥,롤", "keyword": "오마카세 데이트"},
        "cafe": {"name": "브런치 카페", "category": "카페 > 브런치", "keyword": "분위기 좋은 카페"},
        "activity": {"name": "볼링장", "category": "레저 > 스포츠 > 볼링장", "keyword": "커플 볼링"},
    },
    {
        "grade": "optional",
        "restaurant": {"name": "이탈리안 레스토랑", "category": "음식점 > 양식 > 이탈리안", "keyword": "파스타 데이트"},
        "cafe": {"name": "디저트 카페", "category": "카페 > 디저트", "keyword": "케이크 카페"},
        "activity": {"name": "방탈출 카페", "category": "레저 > 오락 > 방탈출카페", "keyword": "커플 방탈출"},
    },
]


class GetRecommendationUseCase:
    def __init__(self, session_repository: RecommendationSessionRepositoryInterface) -> None:
        self._session_repository = session_repository

    def execute(self, dto: GetRecommendationRequestDto) -> GetRecommendationResponseDto:
        collected_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        courses = []

        for idx, template in enumerate(_MOCK_TEMPLATES):
            course_id = str(uuid.uuid4())
            base_id = (idx + 1) * 100

            restaurant = self._build_place(base_id + 1, dto.area, template["restaurant"], collected_at)
            cafe = self._build_place(base_id + 2, dto.area, template["cafe"], collected_at)
            activity = self._build_place(base_id + 3, dto.area, template["activity"], collected_at)

            courses.append(
                RecommendationCourseItemDto(
                    course_id=course_id,
                    grade=template["grade"],
                    restaurant=self._to_dto(restaurant),
                    cafe=self._to_dto(cafe),
                    activity=self._to_dto(activity),
                )
            )

        response = GetRecommendationResponseDto(courses=courses, shortage_reasons=[])

        self._session_repository.save(
            RecommendationSessionDto(
                area=dto.area,
                start_time=dto.start_time,
                transport=dto.transport,
                courses=courses,
            )
        )

        return response

    def _build_place(self, place_id: int, area: str, template: dict, collected_at: str) -> RecommendationPlace:
        return RecommendationPlace(
            id=place_id,
            name=f"{area} {template['name']}",
            category=template["category"],
            road_address=f"서울 {area} 테헤란로 {place_id}길 {place_id}",
            address=f"서울 {area}",
            mapx="127.0276",
            mapy="37.4979",
            link="",
            telephone="02-1234-5678",
            keyword=template["keyword"],
            collected_at=collected_at,
        )

    def _to_dto(self, place: RecommendationPlace) -> RecommendationPlaceDto:
        return RecommendationPlaceDto(
            id=place.id,
            name=place.name,
            category=place.category,
            road_address=place.road_address,
            address=place.address,
            mapx=place.mapx,
            mapy=place.mapy,
            link=place.link,
            telephone=place.telephone,
            keyword=place.keyword,
            collected_at=place.collected_at,
        )
