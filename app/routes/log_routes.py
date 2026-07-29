from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.database.database import get_db
from app.models.log_model import Log
from app.schemas.log_schema import LogCreate

from app.services.email_service import send_alert_email


router = APIRouter()


@router.post("/logs")
def create_log(
    log: LogCreate,
    db: Session = Depends(get_db)
):

    new_log = Log(
        service_name=log.service_name,
        log_level=log.log_level,
        message=log.message,
        source=log.source
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return {
        "message": "Log created successfully",
        "data": new_log.id
    }


@router.get("/logs")
def get_logs(
    log_level: str = None,
    service_name: str = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(Log)

    if log_level:
        query = query.filter(
            Log.log_level == log_level
        )

    if service_name:
        query = query.filter(
            Log.service_name == service_name
        )

    if start_date:
        query = query.filter(
            Log.timestamp >= datetime.fromisoformat(start_date)
        )

    if end_date:
        query = query.filter(
            Log.timestamp <= datetime.fromisoformat(end_date)
        )

    return query.all()


@router.get("/log-stats")
def get_log_stats(
    db: Session = Depends(get_db)
):

    return {
        "total_logs": db.query(Log).count(),
        "error_logs":
        db.query(Log)
        .filter(Log.log_level == "ERROR")
        .count(),

        "info_logs":
        db.query(Log)
        .filter(Log.log_level == "INFO")
        .count(),

        "warning_logs":
        db.query(Log)
        .filter(Log.log_level == "WARNING")
        .count()
    }


@router.get("/recurring-errors")
def recurring_errors(
    db: Session = Depends(get_db)
):

    logs = db.query(Log).filter(
        Log.log_level == "ERROR"
    ).all()

    error_count = {}

    for log in logs:

        if log.message in error_count:
            error_count[log.message] += 1
        else:
            error_count[log.message] = 1


    recurring = []

    for message, count in error_count.items():

        if count >= 2:

            recurring.append({
                "message": message,
                "count": count
            })

    return {
        "recurring_errors": recurring
    }


@router.get("/dashboard-summary")
def dashboard_summary(
    db: Session = Depends(get_db)
):

    top_services = (

        db.query(
            Log.service_name,
            func.count(Log.id)
        )

        .group_by(Log.service_name)

        .order_by(
            func.count(Log.id).desc()
        )

        .limit(5)

        .all()
    )

    return {

        "total_logs":
        db.query(Log).count(),

        "total_errors":
        db.query(Log)
        .filter(Log.log_level == "ERROR")
        .count(),

        "total_warnings":
        db.query(Log)
        .filter(Log.log_level == "WARNING")
        .count(),

        "total_info":
        db.query(Log)
        .filter(Log.log_level == "INFO")
        .count(),

        "top_services": [

            {
                "service": service,
                "count": count
            }

            for service, count in top_services
        ]
    }

@router.get("/alerts")
def get_alerts(
    db: Session = Depends(get_db)
):

    error_services = (

        db.query(
            Log.service_name,
            func.count(Log.id)
        )

        .filter(
            Log.log_level == "ERROR"
        )

        .group_by(
            Log.service_name
        )

        .all()
    )

    alerts = []

    for service, count in error_services:

        severity = None

        if count >= 5:
            severity = "HIGH"

        elif count >= 3:
            severity = "MEDIUM"

        elif count >= 2:
            severity = "LOW"


        if severity:

            send_alert_email(
                service,
                severity,
                count
            )

            alerts.append({

                "service": service,
                "error_count": count,
                "severity": severity,
                "message": "High error rate detected",
                "email_sent": True

            })

    return {
        "alerts": alerts
    }