import argparse
from pathlib import Path

import cv2
import pytesseract


def preprocess_image(image_path: Path):
    """Membaca dan memproses gambar agar OCR lebih akurat."""
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Gagal membaca gambar: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresholded


def extract_text(image_path: Path, lang: str = "eng", use_preprocess: bool = False) -> str:
    """Ekstrak teks dari gambar menggunakan Tesseract."""
    if use_preprocess:
        image = preprocess_image(image_path)
    else:
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Gagal membaca gambar: {image_path}")

    text = pytesseract.image_to_string(image, lang=lang)
    return text.strip()


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="OCR CLI sederhana berbasis Tesseract")
    parser.add_argument("--image", required=True, help="Path ke file gambar")
    parser.add_argument("--lang", default="eng", help="Bahasa OCR (default: eng)")
    parser.add_argument(
        "--preprocess",
        action="store_true",
        help="Aktifkan preprocessing gambar (grayscale + threshold)",
    )
    parser.add_argument("--output", help="Path output file txt (opsional)")
    return parser.parse_args(argv)


def run(image_path: Path, lang: str = "eng", preprocess: bool = False, output: Path | None = None) -> str:
    if not image_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {image_path}")

    result = extract_text(image_path=image_path, lang=lang, use_preprocess=preprocess)

    if output:
        output.write_text(result + "\n", encoding="utf-8")

    return result


def main(argv=None):
    args = parse_args(argv)
    image_path = Path(args.image)
    output_path = Path(args.output) if args.output else None

    result = run(image_path=image_path, lang=args.lang, preprocess=args.preprocess, output=output_path)

    if output_path:
        print(f"Hasil OCR disimpan ke: {output_path}")
    else:
        print("=== HASIL OCR ===")
        print(result)


if __name__ == "__main__":
    main()
