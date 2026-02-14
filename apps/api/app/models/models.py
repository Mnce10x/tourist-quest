from sqlalchemy import JSON, Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_url: Mapped[str] = mapped_column(String(1024), index=True)
    object_key: Mapped[str] = mapped_column(String(255), unique=True)
    file_hash: Mapped[str] = mapped_column(String(64), index=True)
    content_type: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())


class KPIRecord(Base):
    __tablename__ = "kpi_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[str] = mapped_column(String(100), index=True)
    report_period: Mapped[str] = mapped_column(String(32), index=True)
    publish_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    programme: Mapped[str] = mapped_column(String(255), index=True)
    kpi_name: Mapped[str] = mapped_column(String(255))
    kpi_target: Mapped[str | None] = mapped_column(String(100), nullable=True)
    kpi_actual: Mapped[str | None] = mapped_column(String(100), nullable=True)
    variance: Mapped[float | None] = mapped_column(Float, nullable=True)
    variance_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    audit_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)


class ExpenditureRecord(Base):
    __tablename__ = "expenditure_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[str] = mapped_column(String(100), index=True)
    expenditure_vote: Mapped[str] = mapped_column(String(100))
    programme: Mapped[str] = mapped_column(String(255), index=True)
    item: Mapped[str] = mapped_column(String(255))
    planned_budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    actual_spend: Mapped[float | None] = mapped_column(Float, nullable=True)
    variance: Mapped[float | None] = mapped_column(Float, nullable=True)
    variance_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    procurement_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)


class MediaRecord(Base):
    __tablename__ = "media_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    media_id: Mapped[str] = mapped_column(String(100), unique=True)
    source: Mapped[str] = mapped_column(String(255), index=True)
    date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(500))
    body_text: Mapped[str] = mapped_column(Text)
    entities: Mapped[list] = mapped_column(JSON, default=list)
    topics: Mapped[list] = mapped_column(JSON, default=list)
    sentiment_score: Mapped[float] = mapped_column(Float, default=0.0)
    stance: Mapped[str] = mapped_column(String(32), default="neutral")
    key_claims: Mapped[list] = mapped_column(JSON, default=list)
    risk_flags: Mapped[list] = mapped_column(JSON, default=list)
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)


class Recommendation(Base):
    __tablename__ = "recommendations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic: Mapped[str] = mapped_column(String(100), index=True)
    action: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float)
    rationale: Mapped[str] = mapped_column(Text)
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)
