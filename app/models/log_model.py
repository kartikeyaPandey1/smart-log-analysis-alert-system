from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.models.base import Base


class Log(Base):

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    service_name = Column(String, nullable=False)

    log_level = Column(String, nullable=False)

    message = Column(String, nullable=False)

    source = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )