from fastapi import APIRouter, Depends

from app.domains.courses.controller.api.request_form.course_event_request_form import (
    CourseEventRequestForm,
)
from app.domains.courses.controller.api.request_form.create_recommendation_request_form import (
    CreateRecommendationRequestForm,
)
from app.domains.courses.controller.api.response_form.create_recommendation_response_form import (
    CreateRecommendationResponseForm,
)
from app.domains.courses.controller.api.response_form.get_course_detail_response_form import (
    GetCourseDetailResponseForm,
)
from app.domains.courses.repository.course_repository_interface import CourseRepositoryInterface
from app.domains.courses.repository.in_memory_course_repository import get_course_repository
from app.domains.courses.service.usecase.create_course_recommendations_usecase import (
    CreateCourseRecommendationsUseCase,
)
from app.domains.courses.service.usecase.get_course_detail_usecase import GetCourseDetailUseCase

router = APIRouter(prefix="/courses", tags=["courses"])


def _get_create_recommendations_usecase(
    repository: CourseRepositoryInterface = Depends(get_course_repository),
) -> CreateCourseRecommendationsUseCase:
    return CreateCourseRecommendationsUseCase(repository)


def _get_course_detail_usecase(
    repository: CourseRepositoryInterface = Depends(get_course_repository),
) -> GetCourseDetailUseCase:
    return GetCourseDetailUseCase(repository)


@router.post("/events", status_code=200)
def record_course_event(form: CourseEventRequestForm) -> dict:
    return {"success": True}


@router.post("/recommendations", response_model=CreateRecommendationResponseForm)
def create_recommendations(
    form: CreateRecommendationRequestForm,
    usecase: CreateCourseRecommendationsUseCase = Depends(_get_create_recommendations_usecase),
) -> CreateRecommendationResponseForm:
    dto = form.to_request()
    result = usecase.execute(dto)
    return CreateRecommendationResponseForm.from_response(result)


@router.get("/{course_id}", response_model=GetCourseDetailResponseForm)
def get_course_detail(
    course_id: str,
    usecase: GetCourseDetailUseCase = Depends(_get_course_detail_usecase),
) -> GetCourseDetailResponseForm:
    result = usecase.execute(course_id)
    return GetCourseDetailResponseForm.from_response(result)
