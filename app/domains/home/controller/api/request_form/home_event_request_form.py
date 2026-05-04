from typing import Any, Dict, Optional

from pydantic import BaseModel


class HomeEventRequestForm(BaseModel):
    event_type: str
    data: Optional[Dict[str, Any]] = None
