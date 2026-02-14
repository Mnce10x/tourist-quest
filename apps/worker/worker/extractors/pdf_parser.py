from dataclasses import dataclass
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


@dataclass
class PDFExtractionResult:
    text: str
    tables: list[list[list[str]]]
    strategy_used: str


def extract_pdf(path: str) -> PDFExtractionResult:
    # Strategy 1: simple table extraction
    try:
        tables = []
        with pdfplumber.open(path) as pdf:
            text = "\n".join((p.extract_text() or "") for p in pdf.pages)
            for p in pdf.pages:
                t = p.extract_tables() or []
                tables.extend(t)
        if tables:
            return PDFExtractionResult(text=text, tables=tables, strategy_used="simple_tables")
    except Exception:
        pass

    # Strategy 2: layout extraction fallback (placeholder hook)
    try:
        reader = PdfReader(path)
        text = "\n".join((p.extract_text() or "") for p in reader.pages)
        if text:
            return PDFExtractionResult(text=text, tables=[], strategy_used="layout_text")
    except Exception:
        pass

    # Strategy 3: plain bytes heuristic
    raw = Path(path).read_bytes().decode(errors="ignore")
    return PDFExtractionResult(text=raw[:20000], tables=[], strategy_used="heuristic_raw")
