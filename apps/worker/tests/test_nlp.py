from worker.nlp.pipeline import sentiment, topics


def test_sentiment_negative_terms():
    score, evidence = sentiment("There is a delay in procurement. Good recovery plan.")
    assert score < 0
    assert evidence


def test_topics():
    assert "safety" in topics("Safety and security campaign launched")
