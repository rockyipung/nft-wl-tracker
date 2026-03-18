import os
import shlex
import tempfile
import time
from pathlib import Path
from typing import Optional

import requests

from ocr_app import run


def parse_ocr_command(text: str):
    """Parse `/ocr <image_url> [--lang xxx] [--preprocess]` command."""
    parts = shlex.split(text)
    if not parts or parts[0] != "/ocr":
        raise ValueError("Command harus diawali dengan /ocr")
    if len(parts) < 2:
        raise ValueError("Format: /ocr <image_url> [--lang xxx] [--preprocess]")

    image_url = parts[1]
    lang = "eng"
    preprocess = False

    idx = 2
    while idx < len(parts):
        token = parts[idx]
        if token == "--lang":
            if idx + 1 >= len(parts):
                raise ValueError("Nilai --lang tidak ditemukan")
            lang = parts[idx + 1]
            idx += 2
        elif token == "--preprocess":
            preprocess = True
            idx += 1
        else:
            raise ValueError(f"Argumen tidak dikenali: {token}")

    return image_url, lang, preprocess


def download_image(image_url: str, destination: Path):
    response = requests.get(image_url, timeout=30)
    response.raise_for_status()
    destination.write_bytes(response.content)


def send_message(token: str, chat_id: int, text: str):
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "disable_web_page_preview": True},
        timeout=30,
    ).raise_for_status()


def get_updates(token: str, offset: Optional[int] = None):
    params = {"timeout": 20}
    if offset is not None:
        params["offset"] = offset
    response = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload.get("result", [])


def process_update(token: str, update: dict, allowed_chat_id: Optional[str] = None):
    message = update.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()

    if chat_id is None:
        return

    if allowed_chat_id and str(chat_id) != str(allowed_chat_id):
        send_message(token, chat_id, "Unauthorized chat.")
        return

    if not text.startswith("/ocr"):
        send_message(
            token,
            chat_id,
            "Kirim command: /ocr <image_url> [--lang xxx] [--preprocess]",
        )
        return

    try:
        image_url, lang, preprocess = parse_ocr_command(text)
    except ValueError as err:
        send_message(token, chat_id, f"Format command salah: {err}")
        return

    with tempfile.TemporaryDirectory() as tmp_dir:
        image_path = Path(tmp_dir) / "telegram_input.jpg"
        try:
            download_image(image_url, image_path)
            result = run(image_path=image_path, lang=lang, preprocess=preprocess)
            if not result:
                send_message(token, chat_id, "OCR selesai, tapi tidak ada teks terbaca.")
            else:
                send_message(token, chat_id, f"Hasil OCR:\n\n{result[:3500]}")
        except Exception as err:  # noqa: BLE001
            send_message(token, chat_id, f"Gagal proses OCR: {err}")


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    allowed_chat_id = os.getenv("TELEGRAM_ALLOWED_CHAT_ID")

    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN belum di-set")

    print("Telegram OCR bot started...")
    offset = None
    while True:
        updates = get_updates(token, offset=offset)
        for update in updates:
            offset = update["update_id"] + 1
            process_update(token, update, allowed_chat_id=allowed_chat_id)
        time.sleep(1)


if __name__ == "__main__":
    main()
