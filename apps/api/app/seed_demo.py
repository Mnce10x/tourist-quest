from datetime import date

from app.db.session import Base, SessionLocal, engine
from app.models.models import Document, ExpenditureRecord, KPIRecord, MediaRecord, Recommendation


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(KPIRecord).first():
        print("Demo data already present")
        return

    db.add_all(
        [
            Document(source_url="https://www.tourism.gov.za/report-q2", object_key="pdf/a.pdf", file_hash="a" * 64, content_type="application/pdf"),
            Document(source_url="https://www.tourism.gov.za/report-q3", object_key="pdf/b.pdf", file_hash="b" * 64, content_type="application/pdf"),
            KPIRecord(report_id="Q2-2024", report_period="FY2024/25 Q2", publish_date=date(2024, 11, 1), programme="Marketing", kpi_name="International Arrivals", kpi_target="2.0m", kpi_actual="1.85m", variance=-7.5, variance_reason="Global air capacity constraints", evidence={"snippets": ["Reduced direct routes impacted arrivals."]}),
            KPIRecord(report_id="Q3-2024", report_period="FY2024/25 Q3", publish_date=date(2025, 2, 1), programme="Marketing", kpi_name="International Arrivals", kpi_target="2.1m", kpi_actual="1.9m", variance=-9.5, variance_reason="Airlift constraints", evidence={"snippets": ["Airlift capacity remained below baseline"]}),
            ExpenditureRecord(report_id="Q3-2024", expenditure_vote="Vote 38", programme="Destination Development", item="Infrastructure grants", planned_budget=250_000_000, actual_spend=231_000_000, variance=-19_000_000, variance_reason="Procurement delays", procurement_notes="Two tenders re-issued", evidence={"snippets": ["Procurement delays affected implementation"]}),
            MediaRecord(media_id="media-1", source="tourism.gov.za", date=date(2025, 1, 15), title="Minister outlines safety plan", body_text="Safety and destination readiness are key priorities.", entities=["Minister", "South Africa"], topics=["safety", "marketing"], sentiment_score=0.1, stance="supportive", key_claims=["Safety plan launched"], risk_flags=[]),
            MediaRecord(media_id="media-2", source="newswire", date=date(2025, 2, 10), title="Infrastructure delays affect visitor confidence", body_text="Delays in key infrastructure projects caused concern among operators.", entities=["Operators"], topics=["infrastructure", "safety"], sentiment_score=-0.4, stance="critical", key_claims=["Project delays persist"], risk_flags=["delivery-risk"], evidence={"snippets": ["caused concern among operators"]}),
            Recommendation(topic="safety", action="Launch myth-busting FAQ with weekly safety metrics by province.", confidence=0.82, rationale="Rising safety mentions correlate with dip in arrivals sentiment.", evidence={"sources": ["media-1", "media-2"], "snippets": ["Safety and destination readiness are key priorities"]}),
        ]
    )
    db.commit()
    print("Seeded demo data")


if __name__ == "__main__":
    run()
