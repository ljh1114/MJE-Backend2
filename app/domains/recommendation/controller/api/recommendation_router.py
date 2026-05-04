from fastapi import APIRouter, Depends

from app.domains.recommendation.controller.api.request_form.get_recommendation_request_form import (
    GetRecommendationRequestForm,
)
from app.domains.recommendation.controller.api.response_form.get_recommendation_response_form import (
    GetRecommendationResponseForm,
)
from app.domains.recommendation.service.usecase.get_recommendation_usecase import (
    GetRecommendationUseCase,
)

router = APIRouter(prefix="/courses", tags=["recommendation"])


def _get_recommendation_usecase() -> GetRecommendationUseCase:
    return GetRecommendationUseCase()


@router.post("/recommendations", response_model=GetRecommendationResponseForm)
def get_recommendations(
    form: GetRecommendationRequestForm,
    usecase: GetRecommendationUseCase = Depends(_get_recommendation_usecase),
) -> GetRecommendationResponseForm:
    dto = form.to_request()
    result = usecase.execute(dto)
    return GetRecommendationResponseForm.from_response(result)
