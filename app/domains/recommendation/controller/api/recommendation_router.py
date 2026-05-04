from fastapi import APIRouter, Depends

from app.domains.recommendation.controller.api.request_form.get_recommendation_request_form import (
    GetRecommendationRequestForm,
)
from app.domains.recommendation.controller.api.response_form.get_course_detail_response_form import (
    GetCourseDetailResponseForm,
)
from app.domains.recommendation.controller.api.response_form.get_recommendation_response_form import (
    GetRecommendationResponseForm,
)
from app.domains.recommendation.repository.in_memory_recommendation_session_repository import (
    get_recommendation_session_repository,
    InMemoryRecommendationSessionRepository,
)
from app.domains.recommendation.repository.recommendation_session_repository_interface import (
    RecommendationSessionRepositoryInterface,
)
from app.domains.recommendation.service.dto.request.get_course_detail_request_dto import (
    GetCourseDetailRequestDto,
)
from app.domains.recommendation.service.usecase.get_course_detail_usecase import GetCourseDetailUseCase
from app.domains.recommendation.service.usecase.get_recommendation_usecase import (
    GetRecommendationUseCase,
)

router = APIRouter(prefix="/courses", tags=["recommendation"])


def _get_session_repository(
    repository: InMemoryRecommendationSessionRepository = Depends(get_recommendation_session_repository),
) -> RecommendationSessionRepositoryInterface:
    return repository


def _get_recommendation_usecase(
    repository: RecommendationSessionRepositoryInterface = Depends(_get_session_repository),
) -> GetRecommendationUseCase:
    return GetRecommendationUseCase(session_repository=repository)


def _get_course_detail_usecase(
    repository: RecommendationSessionRepositoryInterface = Depends(_get_session_repository),
) -> GetCourseDetailUseCase:
    return GetCourseDetailUseCase(repository=repository)


@router.post("/recommendations", response_model=GetRecommendationResponseForm)
def get_recommendations(
    form: GetRecommendationRequestForm,
    usecase: GetRecommendationUseCase = Depends(_get_recommendation_usecase),
) -> GetRecommendationResponseForm:
    dto = form.to_request()
    result = usecase.execute(dto)
    return GetRecommendationResponseForm.from_response(result)


@router.get("/recommendations/{course_id}", response_model=GetCourseDetailResponseForm)
def get_course_detail(
    course_id: str,
    usecase: GetCourseDetailUseCase = Depends(_get_course_detail_usecase),
) -> GetCourseDetailResponseForm:
    dto = GetCourseDetailRequestDto(course_id=course_id)
    result = usecase.execute(dto)
    return GetCourseDetailResponseForm.from_response(result)
