import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest

if "cv2" not in sys.modules:
    cv2_stub = types.ModuleType("cv2")
    cv2_stub.COLOR_BGR2GRAY = 6
    cv2_stub.THRESH_BINARY = 0
    cv2_stub.THRESH_OTSU = 0
    cv2_stub.imread = lambda *_args, **_kwargs: object()
    cv2_stub.cvtColor = lambda image, *_args, **_kwargs: image
    cv2_stub.threshold = lambda image, *_args, **_kwargs: (None, image)
    sys.modules["cv2"] = cv2_stub

if "pytesseract" not in sys.modules:
    tess_stub = types.ModuleType("pytesseract")
    tess_stub.image_to_string = lambda *_args, **_kwargs: ""
    sys.modules["pytesseract"] = tess_stub

import ocr_app


def test_parse_args_default_values():
    args = ocr_app.parse_args(["--image", "sample.png"])
    assert args.image == "sample.png"
    assert args.lang == "eng"
    assert args.preprocess is False
    assert args.output is None


def test_parse_args_custom_values():
    args = ocr_app.parse_args(
        ["--image", "sample.png", "--lang", "ind", "--preprocess", "--output", "hasil.txt"]
    )
    assert args.lang == "ind"
    assert args.preprocess is True
    assert args.output == "hasil.txt"


def test_extract_text_without_preprocess(monkeypatch):
    fake_image = object()
    monkeypatch.setattr(ocr_app.cv2, "imread", lambda _: fake_image)
    monkeypatch.setattr(ocr_app.pytesseract, "image_to_string", lambda img, lang: "teks  ")

    result = ocr_app.extract_text(Path("dummy.png"), lang="eng", use_preprocess=False)
    assert result == "teks"


def test_extract_text_with_preprocess(monkeypatch):
    fake_processed = object()
    monkeypatch.setattr(ocr_app, "preprocess_image", lambda _: fake_processed)
    mock_ocr = MagicMock(return_value="hasil")
    monkeypatch.setattr(ocr_app.pytesseract, "image_to_string", mock_ocr)

    result = ocr_app.extract_text(Path("dummy.png"), lang="ind", use_preprocess=True)

    assert result == "hasil"
    mock_ocr.assert_called_once_with(fake_processed, lang="ind")


def test_run_writes_output_file(monkeypatch, tmp_path):
    image_path = tmp_path / "sample.png"
    image_path.write_bytes(b"dummy")
    output_path = tmp_path / "result.txt"

    monkeypatch.setattr(ocr_app, "extract_text", lambda **_: "isi teks")

    result = ocr_app.run(image_path=image_path, output=output_path)

    assert result == "isi teks"
    assert output_path.read_text(encoding="utf-8") == "isi teks\n"


def test_run_raises_if_input_missing(tmp_path):
    missing = tmp_path / "missing.png"
    with pytest.raises(FileNotFoundError):
        ocr_app.run(image_path=missing)
