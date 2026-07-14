import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.document_service import DocumentService


def test_document_service_imports():
    assert DocumentService is not None
