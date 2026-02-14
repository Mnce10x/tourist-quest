from app.services.analytics import export_csv


def test_export_csv_has_header():
    csv_text = export_csv([{"report_period": "FY2024/25 Q3", "variance": -9.5}])
    assert "report_period" in csv_text
    assert "-9.5" in csv_text
