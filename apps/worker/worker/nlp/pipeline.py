from collections import Counter

NEGATIVE_TERMS = {"delay", "risk", "decline", "concern", "shortfall", "problem"}
TOPIC_KEYWORDS = {
    "transformation": ["transformation", "inclusive"],
    "safety": ["safety", "crime", "security"],
    "arrivals": ["arrivals", "visitors", "tourists"],
    "infrastructure": ["infrastructure", "roads", "airlift"],
    "marketing": ["campaign", "brand", "marketing"],
}


def sentiment(text: str) -> tuple[float, list[str]]:
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    evidence = [s for s in sentences if any(t in s.lower() for t in NEGATIVE_TERMS)]
    score = -min(len(evidence) / max(1, len(sentences)), 1.0)
    return score, evidence[:3]


def topics(text: str) -> list[str]:
    lower = text.lower()
    found = [t for t, keys in TOPIC_KEYWORDS.items() if any(k in lower for k in keys)]
    return found or ["general"]


def recommend(media_records: list[dict]) -> list[dict]:
    counts = Counter()
    for m in media_records:
        for t in m.get("topics", []):
            if m.get("sentiment_score", 0) < 0:
                counts[t] += 1
    recs = []
    for topic, c in counts.items():
        recs.append({
            "topic": topic,
            "action": "Publish targeted FAQ + stakeholder briefing and track corrective actions weekly.",
            "confidence": min(0.5 + c * 0.1, 0.95),
            "rationale": f"Negative mentions increased for {topic}",
            "evidence": {"count": c},
        })
    return recs
