from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.core.security import admin_only, require_role
from app.db.session import get_db
from app.models.models import ExpenditureRecord, KPIRecord, MediaRecord, Recommendation
from app.schemas.api import (
    DataQualitySummary,
    ExecutiveOverview,
    ExplainRecord,
    KPITrendPoint,
    MediaLifecyclePoint,
    RecommendationOut,
    VarianceOutlier,
)
from app.services.analytics import (
    data_quality,
    executive_overview,
    explain_metric,
    export_csv,
    kpi_trends,
    media_lifecycle,
    variance_outliers,
)

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/overview", response_model=ExecutiveOverview)
def overview(db: Session = Depends(get_db), _role: str = Depends(require_role)):
    return executive_overview(db)


@router.get("/kpis")
def list_kpis(db: Session = Depends(get_db), _role: str = Depends(require_role)):
    return db.query(KPIRecord).limit(200).all()


@router.get("/kpi-trends", response_model=list[KPITrendPoint])
def list_kpi_trends(db: Session = Depends(get_db), _role: str = Depends(require_role)):
    return kpi_trends(db)


@router.get("/expenditure")
def list_expenditure(db: Session = Depends(get_db), _role: str = Depends(require_role)):
    return db.query(ExpenditureRecord).limit(200).all()


@router.get("/media")
def list_media(db: Session = Depends(get_db), _role: str = Depends(require_role)):
    return db.query(MediaRecord).limit(300).all()


@router.get("/media-lifecycle", response_model=list[MediaLifecyclePoint])
def list_media_lifecycle(db: Session = Depends(get_db), _role: str = Depends(require_role)):
    return media_lifecycle(db)


@router.get("/recommendations", response_model=list[RecommendationOut])
def list_recommendations(db: Session = Depends(get_db), _role: str = Depends(require_role)):
    return db.query(Recommendation).order_by(Recommendation.confidence.desc()).all()


@router.get("/outliers", response_model=list[VarianceOutlier])
def list_outliers(db: Session = Depends(get_db), _role: str = Depends(require_role)):
    return variance_outliers(db)


@router.get("/explain", response_model=ExplainRecord)
def explain(
    metric_type: str = Query(..., pattern="^(kpi|expenditure|media|recommendation)$"),
    metric_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
    _role: str = Depends(require_role),
):
    return explain_metric(db, metric_type, metric_id)


@router.get("/data-quality", response_model=DataQualitySummary)
def get_data_quality(db: Session = Depends(get_db), _role: str = Depends(admin_only)):
    return data_quality(db)


@router.get("/export/{dataset}", response_class=PlainTextResponse)
def export_dataset(dataset: str, db: Session = Depends(get_db), _role: str = Depends(require_role)):
    dataset = dataset.lower().strip()
    if dataset == "kpi":
        rows = kpi_trends(db)
    elif dataset == "outliers":
        rows = variance_outliers(db)
    elif dataset == "media_lifecycle":
        rows = media_lifecycle(db)
    else:
        rows = []
    return export_csv(rows)
