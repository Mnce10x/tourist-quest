from datetime import date
from pydantic import BaseModel, Field


class Provenance(BaseModel):
    source_url: str
    object_key: str
    file_hash: str
    evidence_snippets: list[str] = Field(default_factory=list)


class KPIRecord(BaseModel):
    report_id: str
    report_period: str
    publish_date: date | None = None
    programme: str
    kpi_name: str
    kpi_target: float | str | None = None
    kpi_actual: float | str | None = None
    variance: float | None = None
    variance_reason: str | None = None
    audit_flag: bool = False
    provenance: Provenance


class ExpenditureRecord(BaseModel):
    report_id: str
    expenditure_vote: str
    programme: str
    item: str
    planned_budget: float | None = None
    actual_spend: float | None = None
    variance: float | None = None
    variance_reason: str | None = None
    procurement_notes: str | None = None
    provenance: Provenance


class MediaRecord(BaseModel):
    media_id: str
    source: str
    date: date | None = None
    author: str | None = None
    title: str
    body_text: str
    entities: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)
    sentiment_score: float = 0.0
    stance: str = "neutral"
    key_claims: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    provenance: Provenance
