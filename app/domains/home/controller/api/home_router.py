from fastapi import APIRouter

from app.domains.home.controller.api.request_form.home_event_request_form import HomeEventRequestForm

router = APIRouter(prefix="/home", tags=["home"])


@router.post("/events", status_code=200)
def record_home_event(form: HomeEventRequestForm) -> dict:
    return {"success": True}
