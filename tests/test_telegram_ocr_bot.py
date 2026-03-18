from pathlib import Path

import pytest

import telegram_ocr_bot


def test_parse_ocr_command_minimal():
    image_url, lang, preprocess = telegram_ocr_bot.parse_ocr_command("/ocr https://img.test/a.png")
    assert image_url == "https://img.test/a.png"
    assert lang == "eng"
    assert preprocess is False


def test_parse_ocr_command_full_options():
    image_url, lang, preprocess = telegram_ocr_bot.parse_ocr_command(
        "/ocr https://img.test/a.png --lang ind --preprocess"
    )
    assert image_url == "https://img.test/a.png"
    assert lang == "ind"
    assert preprocess is True


def test_parse_ocr_command_invalid_prefix():
    with pytest.raises(ValueError):
        telegram_ocr_bot.parse_ocr_command("/start")


def test_process_update_replies_usage_for_non_ocr(monkeypatch):
    sent = []
    monkeypatch.setattr(telegram_ocr_bot, "send_message", lambda _t, _c, text: sent.append(text))

    update = {"message": {"chat": {"id": 123}, "text": "halo"}}
    telegram_ocr_bot.process_update("token", update)

    assert sent
    assert "Kirim command" in sent[0]


def test_process_update_runs_ocr_success(monkeypatch, tmp_path):
    sent = []

    monkeypatch.setattr(telegram_ocr_bot, "send_message", lambda _t, _c, text: sent.append(text))

    def fake_download(_url: str, destination: Path):
        destination.write_bytes(b"dummy")

    monkeypatch.setattr(telegram_ocr_bot, "download_image", fake_download)
    monkeypatch.setattr(telegram_ocr_bot, "run", lambda **_kwargs: "hasil scan")

    update = {"message": {"chat": {"id": 123}, "text": "/ocr https://img.test/a.png"}}
    telegram_ocr_bot.process_update("token", update)

    assert sent == ["Hasil OCR:\n\nhasil scan"]


def test_process_update_rejects_unauthorized(monkeypatch):
    sent = []
    monkeypatch.setattr(telegram_ocr_bot, "send_message", lambda _t, _c, text: sent.append(text))

    update = {"message": {"chat": {"id": 123}, "text": "/ocr https://img.test/a.png"}}
    telegram_ocr_bot.process_update("token", update, allowed_chat_id="999")

    assert sent == ["Unauthorized chat."]
