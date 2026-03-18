# OCR Project

Proyek OCR sederhana berbasis Python untuk mengekstrak teks dari gambar menggunakan **Tesseract OCR**.

## Fitur
- OCR dari satu gambar (`.png`, `.jpg`, `.jpeg`, `.webp`, dll)
- Opsi preprocessing (grayscale + threshold) agar hasil pembacaan lebih baik
- Simpan hasil ke file `.txt`
- CLI mudah dipakai

## Struktur
```
.
├── ocr_app.py
├── requirements.txt
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

## Pemakaian
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

## Catatan
- Akurasi OCR tergantung kualitas gambar.
- Untuk dokumen berbahasa Indonesia, gunakan `--lang ind` dan pastikan paket bahasa Tesseract tersedia.
