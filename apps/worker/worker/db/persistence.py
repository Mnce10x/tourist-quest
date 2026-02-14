import json
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from worker.config.settings import settings


class _Base:
    pass


def get_session():
    engine = create_engine(settings.database_url, future=True)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return session_factory()


def persist_ingestion_payload(payload: dict) -> dict:
    """
    Persist normalized ingestion payload into existing API tables.
    Uses SQLAlchemy text statements to avoid hard-coupling worker to API ORM imports.
    """
    from sqlalchemy import text

    inserted = {"documents": 0, "kpi_records": 0, "media_records": 0, "recommendations": 0}
    with get_session() as db:
        for doc in payload.get("documents", []):
            if not isinstance(doc, dict):
                continue
            db.execute(
                text(
                    """
                    INSERT INTO documents (source_url, object_key, file_hash, content_type)
                    VALUES (:source_url, :object_key, :file_hash, :content_type)
                    """
                ),
                {
                    "source_url": doc.get("url", ""),
                    "object_key": doc.get("object_key", ""),
                    "file_hash": doc.get("file_hash", ""),
                    "content_type": doc.get("content_type", "application/octet-stream"),
                },
            )
            inserted["documents"] += 1

        for kpi in payload.get("kpi_records", []):
            db.execute(
                text(
                    """
                    INSERT INTO kpi_records
                    (report_id, report_period, publish_date, programme, kpi_name, kpi_target, kpi_actual, variance, variance_reason, audit_flag, evidence)
                    VALUES (:report_id, :report_period, :publish_date, :programme, :kpi_name, :kpi_target, :kpi_actual, :variance, :variance_reason, :audit_flag, :evidence)
                    """
                ),
                {
                    "report_id": kpi.get("report_id", "unknown"),
                    "report_period": kpi.get("report_period", "unknown"),
                    "publish_date": date.today(),
                    "programme": kpi.get("programme", "unknown"),
                    "kpi_name": kpi.get("kpi_name", "unknown"),
                    "kpi_target": str(kpi.get("kpi_target", "")),
                    "kpi_actual": str(kpi.get("kpi_actual", "")),
                    "variance": float(kpi.get("variance", 0) or 0),
                    "variance_reason": kpi.get("variance_reason"),
                    "audit_flag": bool(kpi.get("audit_flag", False)),
                    "evidence": json.dumps({"source": "worker_ingest"}),
                },
            )
            inserted["kpi_records"] += 1

        for media in payload.get("media_records", []):
            db.execute(
                text(
                    """
                    INSERT INTO media_records
                    (media_id, source, date, title, body_text, entities, topics, sentiment_score, stance, key_claims, risk_flags, evidence)
                    VALUES (:media_id, :source, :date, :title, :body_text, :entities, :topics, :sentiment_score, :stance, :key_claims, :risk_flags, :evidence)
                    """
                ),
                {
                    "media_id": media.get("media_id", f"media-{date.today().isoformat()}"),
                    "source": "derived_ingest",
                    "date": date.today(),
                    "title": "Derived media narrative",
                    "body_text": "Auto-generated from quarterly source document",
                    "entities": json.dumps(media.get("entities", [])),
                    "topics": json.dumps(media.get("topics", [])),
                    "sentiment_score": float(media.get("sentiment_score", 0)),
                    "stance": media.get("stance", "neutral"),
                    "key_claims": json.dumps(media.get("key_claims", [])),
                    "risk_flags": json.dumps(media.get("risk_flags", [])),
                    "evidence": json.dumps({"source": "worker_ingest"}),
                },
            )
            inserted["media_records"] += 1

        for rec in payload.get("recommendations", []):
            db.execute(
                text(
                    """
                    INSERT INTO recommendations (topic, action, confidence, rationale, evidence)
                    VALUES (:topic, :action, :confidence, :rationale, :evidence)
                    """
                ),
                {
                    "topic": rec.get("topic", "general"),
                    "action": rec.get("action", "Monitor"),
                    "confidence": float(rec.get("confidence", 0.5)),
                    "rationale": rec.get("rationale", "Auto-generated"),
                    "evidence": json.dumps(rec.get("evidence", {})),
                },
            )
            inserted["recommendations"] += 1

        db.commit()
    return inserted
