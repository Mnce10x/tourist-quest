import csv
import io
from collections import defaultdict

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import Document, ExpenditureRecord, KPIRecord, MediaRecord, Recommendation


def executive_overview(db: Session):
    kpi_count = db.query(func.count(KPIRecord.id)).scalar() or 0
    media_items = db.query(func.count(MediaRecord.id)).scalar() or 0
    avg_sentiment = db.query(func.avg(MediaRecord.sentiment_score)).scalar() or 0
    alerts = []
    if avg_sentiment < -0.15:
        alerts.append("Sentiment is trending negative")
    high_variance = db.query(func.count(KPIRecord.id)).filter(func.abs(KPIRecord.variance) > 20).scalar() or 0
    if high_variance:
        alerts.append(f"{high_variance} KPI records show high variance")
    return {
        "kpi_count": kpi_count,
        "media_items": media_items,
        "avg_sentiment": round(float(avg_sentiment), 3),
        "alerts": alerts,
    }


def kpi_trends(db: Session) -> list[dict]:
    rows = db.query(KPIRecord).order_by(KPIRecord.report_period.asc()).all()
    return [
        {
            "report_period": r.report_period,
            "programme": r.programme,
            "kpi_name": r.kpi_name,
            "variance": r.variance,
        }
        for r in rows
    ]


def variance_outliers(db: Session) -> list[dict]:
    outliers: list[dict] = []
    for r in db.query(KPIRecord).filter(func.abs(KPIRecord.variance) >= 10).all():
        outliers.append(
            {
                "record_type": "kpi",
                "identifier": f"{r.report_id}:{r.kpi_name}",
                "variance": float(r.variance or 0),
                "reason": r.variance_reason,
            }
        )
    for r in db.query(ExpenditureRecord).filter(func.abs(ExpenditureRecord.variance) >= 10_000_000).all():
        outliers.append(
            {
                "record_type": "expenditure",
                "identifier": f"{r.report_id}:{r.item}",
                "variance": float(r.variance or 0),
                "reason": r.variance_reason,
            }
        )
    return outliers


def explain_metric(db: Session, metric_type: str, metric_id: int) -> dict:
    if metric_type == "kpi":
        record = db.get(KPIRecord, metric_id)
    elif metric_type == "expenditure":
        record = db.get(ExpenditureRecord, metric_id)
    elif metric_type == "media":
        record = db.get(MediaRecord, metric_id)
    elif metric_type == "recommendation":
        record = db.get(Recommendation, metric_id)
    else:
        return {"metric_type": metric_type, "metric_id": metric_id, "evidence": {"error": "unsupported type"}}
    return {"metric_type": metric_type, "metric_id": metric_id, "evidence": getattr(record, "evidence", {}) if record else {}}


def data_quality(db: Session) -> dict:
    total_documents = db.query(func.count(Document.id)).scalar() or 0
    total_kpis = db.query(func.count(KPIRecord.id)).scalar() or 0
    total_expenditure = db.query(func.count(ExpenditureRecord.id)).scalar() or 0
    total_media = db.query(func.count(MediaRecord.id)).scalar() or 0
    denom = max(1, total_documents)
    extraction_success_rate = min(1.0, (total_kpis + total_expenditure + total_media) / denom)
    anomalies = []
    if total_documents == 0:
        anomalies.append("No ingested documents detected")
    if total_media and db.query(func.avg(MediaRecord.sentiment_score)).scalar() is None:
        anomalies.append("Media rows found without sentiment scores")
    return {
        "total_documents": total_documents,
        "total_kpis": total_kpis,
        "total_expenditure": total_expenditure,
        "total_media": total_media,
        "extraction_success_rate": round(float(extraction_success_rate), 3),
        "anomalies": anomalies,
    }


def media_lifecycle(db: Session) -> list[dict]:
    rows = db.query(MediaRecord).all()
    grouped: dict[tuple, list[float]] = defaultdict(list)
    counts: dict[tuple, int] = defaultdict(int)
    for r in rows:
        topics = r.topics or ["general"]
        for t in topics:
            key = (r.date, t)
            counts[key] += 1
            grouped[key].append(float(r.sentiment_score or 0))
    payload = []
    for (dt, topic), count in counts.items():
        avg = sum(grouped[(dt, topic)]) / max(1, len(grouped[(dt, topic)]))
        payload.append({"date": dt, "topic": topic, "count": count, "avg_sentiment": round(avg, 3)})
    return sorted(payload, key=lambda x: (str(x["date"]), x["topic"]))


def export_csv(rows: list[dict]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()
