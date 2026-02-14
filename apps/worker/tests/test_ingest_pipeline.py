from worker.pipelines import ingest


def test_run_ingest_without_persist(monkeypatch):
    monkeypatch.setattr(ingest, 'discover_and_fetch', lambda *args, **kwargs: [{"url": "u", "object_key": "k", "file_hash": "h", "content_type": "text/html"}])

    class _Resp:
        content = b'%PDF-1.4 mock'

    class _Client:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get(self, _):
            return _Resp()

    monkeypatch.setattr(ingest.httpx, 'Client', lambda timeout=30: _Client())

    class _Pdf:
        strategy_used = 'layout_text'
        text = 'FY2024/25 Q3 tourism safety risk has decline in confidence.'

    monkeypatch.setattr(ingest, 'extract_pdf', lambda p: _Pdf())

    result = ingest.run_ingest(persist=False)
    assert result['pdf_strategy'] == 'layout_text'
    assert result['kpi_records']
    assert 'persisted_counts' not in result
