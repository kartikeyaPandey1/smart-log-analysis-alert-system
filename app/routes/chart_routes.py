from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func,case

from app.database.database import get_db
from app.models.log_model import Log

router = APIRouter()


@router.get("/charts/log-levels")
def log_level_chart(db: Session = Depends(get_db)):

    data = (
        db.query(
            Log.log_level,
            func.count(Log.id)
        )
        .group_by(Log.log_level)
        .all()
    )

    return {
        "chart_data": [
            {
                "label": level,
                "count": count
            }
            for level, count in data
        ]
    }


@router.get("/charts/services")
def service_chart(db: Session = Depends(get_db)):

    data = (
        db.query(
            Log.service_name,
            func.count(Log.id)
        )
        .group_by(Log.service_name)
        .all()
    )

    return {
        "chart_data": [
            {
                "service": service,
                "count": count
            }
            for service, count in data
        ]
    }

@router.get("/charts/service-health")
def service_health(db: Session =Depends(get_db)):

    data = (

        db.query(

            Log.service_name,

            (
                100
                -
                (
                    func.sum(
                        case(
                            (Log.log_level == "ERROR", 25),
                            else_=0
                        )
                    )
                )
            ).label("health")

        )

        .group_by(Log.service_name)

        .all()

    )

    health_data = []

    for service, health in data:

        # Prevent negative health
        health = max(0, health)

        if health >= 90:
            status = "Healthy"

        elif health >= 70:
            status = "Stable"

        elif health >= 40:
            status = "Warning"

        else:
            status = "Critical"

        health_data.append(
            {
                "service": service,
                "health": health,
                "status": status
            }
        )

    return {
        "chart_data": health_data
    }