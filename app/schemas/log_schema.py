from pydantic import BaseModel
from typing import Optional


class LogCreate(BaseModel):

    service_name: str

    log_level: str

    message: str

    source: Optional[str] = None