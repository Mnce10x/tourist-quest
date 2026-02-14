import re
from pathlib import Path

import httpx

from worker.config.sources import SAMPLE_PDF, SEED_URLS
from worker.db.persistence import persist_ingestion_payload
from worker.extractors.pdf_parser import extract_pdf
from worker.nlp.pipeline import recommend, sentiment, topics
from worker.pipelines.crawler import discover_and_fetch


def _extract_quarter(text: str) -> str:
    m = re.search(r"FY\s?20\d{2}/\d{2}\s?Q[1-4]", text, flags=re.IGNORECASE)
    return m.group(0).replace(" ", "") if m else "FY2024/25Q3"


def run_ingest(persist: bool = True) -> dict:
    docs = discover_and_fetch(SEED_URLS, crawl_delay=0.2, respect_robots=True)
    with httpx.Client(timeout=30) as client:
        data = client.get(SAMPLE_PDF).content
    path = Path("/tmp/sample_quarterly.pdf")
    path.write_bytes(data)
    pdf = extract_pdf(str(path))
    text = pdf.text[:6000]

    report_period = _extract_quarter(text)
    score, evidence = sentiment(text)
    detected_topics = topics(text)

    media_records = [
        {
            "media_id": "derived-sample-1",
            "topics": detected_topics,
            "sentiment_score": score,
            "risk_flags": ["negative-sentiment"] if score < -0.2 else [],
        }
    ]
    recommendations = recommend(media_records)

    kpi_record = {
        "report_id": "sample-quarterly",
        "report_period": report_period,
        "programme": "Tourism Sector Support",
        "kpi_name": "Sector confidence index",
        "kpi_target": "75",
        "kpi_actual": "71",
        "variance": -4.0,
        "variance_reason": evidence[0] if evidence else "Derived from narrative text",
        "audit_flag": False,
    }

    payload = {
        "documents": docs,
        "pdf_strategy": pdf.strategy_used,
        "kpi_records": [kpi_record],
        "media_records": media_records,
        "recommendations": recommendations,
        "sentiment_evidence": evidence,
    }

    if persist:
        payload["persisted_counts"] = persist_ingestion_payload(payload)

    return payload
