from worker.extractors.pdf_parser import extract_pdf


def test_pdf_golden_regression():
    result = extract_pdf('apps/worker/tests/fixtures/golden_sample.pdf')
    assert len(result.text) > 10
    assert result.strategy_used in {"simple_tables", "layout_text", "heuristic_raw"}
