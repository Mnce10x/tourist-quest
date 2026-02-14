from datetime import date
from pydantic import BaseModel


class ExecutiveOverview(BaseModel):
    kpi_count: int
    media_items: int
    avg_sentiment: float
    alerts: list[str]


class RecommendationOut(BaseModel):
    id: int
    topic: str
    action: str
    confidence: float
    rationale: str
    evidence: dict


class KPITrendPoint(BaseModel):
    report_period: str
    programme: str
    kpi_name: str
    variance: float | None


class VarianceOutlier(BaseModel):
    record_type: str
    identifier: str
    variance: float
    reason: str | None


class ExplainRecord(BaseModel):
    metric_type: str
    metric_id: int
    evidence: dict


class DataQualitySummary(BaseModel):
    total_documents: int
    total_kpis: int
    total_expenditure: int
    total_media: int
    extraction_success_rate: float
    anomalies: list[str]


class MediaLifecyclePoint(BaseModel):
    date: date | None
    topic: str
    count: int
    avg_sentiment: float
