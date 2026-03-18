# OCR Project

Proyek OCR sederhana berbasis Python untuk mengekstrak teks dari gambar menggunakan **Tesseract OCR**.

## Fitur
- OCR dari satu gambar (`.png`, `.jpg`, `.jpeg`, `.webp`, dll)
- Opsi preprocessing (grayscale + threshold) agar hasil pembacaan lebih baik
- Simpan hasil ke file `.txt`
- CLI mudah dipakai
- Trigger OCR via Telegram bot (input command dari Telegram, output hasil OCR ke Telegram)

## Struktur
```
.
├── ocr_app.py
├── telegram_ocr_bot.py
├── requirements.txt
├── tests/
└── README.md
```

## Instalasi
1. Buat virtual environment (opsional tapi direkomendasikan):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependency Python:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Tesseract di sistem:
   - Ubuntu/Debian:
     ```bash
     sudo apt-get update && sudo apt-get install -y tesseract-ocr
     ```
   - macOS (Homebrew):
     ```bash
     brew install tesseract
     ```
   - Windows:
     Install dari installer resmi Tesseract, lalu pastikan path executable masuk ke `PATH`.

## Pemakaian CLI
OCR dasar:
```bash
python ocr_app.py --image path/ke/gambar.png
```

OCR dengan bahasa Indonesia + preprocessing:
```bash
python ocr_app.py --image path/ke/gambar.jpg --lang ind --preprocess
```

Simpan ke file:
```bash
python ocr_app.py --image path/ke/gambar.jpg --output hasil.txt
```

## Trigger Input/Output Telegram
Bot Telegram menerima command OCR dari chat, lalu mengirim hasil OCR kembali ke chat yang sama.

### 1) Set environment variable
```bash
export TELEGRAM_BOT_TOKEN="<token_bot_telegram>"
export TELEGRAM_ALLOWED_CHAT_ID="<chat_id_anda>"  # opsional, untuk whitelist chat
```

### 2) Jalankan bot
```bash
python telegram_ocr_bot.py
```

### 3) Kirim command dari Telegram
Format command:
```text
/ocr <image_url> [--lang xxx] [--preprocess]
```

Contoh:
```text
/ocr https://example.com/nota.jpg --lang ind --preprocess
```

Bot akan membalas dengan teks hasil OCR.

## Catatan
- Akurasi OCR tergantung kualitas gambar.
- Untuk dokumen berbahasa Indonesia, gunakan `--lang ind` dan pastikan paket bahasa Tesseract tersedia.
- Panjang pesan Telegram terbatas; hasil OCR panjang akan dipotong.
