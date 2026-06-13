#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "reports" / "validation_report.md"

FILES = {
    "paragraflar": DATA / "paragraflar.tsv",
    "kelimeler": DATA / "kelimeler.tsv",
    "duzeltmeler": DATA / "duzeltmeler.tsv",
    "kaynaklar": DATA / "kaynaklar.tsv",
}

REQUIRED_HEADERS = {
    "paragraflar": [
        "paragraf_id", "eser_id", "eser_adı", "pdf_sayfa", "matbu_sayfa",
        "Osmanlıca_metin", "diplomatik_çevriyazı", "normalleştirilmiş_okuma",
        "günümüz_Türkçesi", "durum", "not"
    ],
    "kelimeler": [
        "kelime_id", "paragraf_id", "sıra", "Osmanlıca_biçim",
        "diplomatik_biçim", "normalleştirilmiş_biçim", "lemma", "kaynak_dil",
        "Arapça_kök", "vezin", "Türkçe_ek_çözümlemesi", "temel_anlam",
        "bağlam_anlamı", "kaynak_id", "doğrulama_durumu", "not"
    ],
    "duzeltmeler": [
        "düzeltme_id", "tarih", "kayıt_türü", "kayıt_id", "alan",
        "eski_değer", "yeni_değer", "gerekçe", "düzelten", "durum"
    ],
    "kaynaklar": [
        "kaynak_id", "kısa_ad", "kaynak_türü", "tam_künye/açıklama",
        "konum", "erişim_tarihi", "not"
    ],
}

ID_PATTERNS = {
    "paragraflar": re.compile(r"^PAR-YZ-\d{4}$"),
    "kelimeler": re.compile(r"^KEL-YZ-\d{4}$"),
    "duzeltmeler": re.compile(r"^DUZ-YZ-\d{4}$"),
    "kaynaklar": re.compile(r"^KAY-\d{4}$"),
}

ID_COLUMNS = {
    "paragraflar": "paragraf_id",
    "kelimeler": "kelime_id",
    "duzeltmeler": "düzeltme_id",
    "kaynaklar": "kaynak_id",
}

def read_tsv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return reader.fieldnames or [], list(reader)

def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    tables = {}

    for name, path in FILES.items():
        if not path.exists():
            errors.append(f"Eksik dosya: {path.relative_to(ROOT)}")
            continue
        headers, rows = read_tsv(path)
        tables[name] = rows
        if headers != REQUIRED_HEADERS[name]:
            errors.append(
                f"{path.name}: sütunlar beklenen sırada değil.\n"
                f"Beklenen: {REQUIRED_HEADERS[name]}\nBulunan: {headers}"
            )

        id_col = ID_COLUMNS[name]
        ids = []
        for line_no, row in enumerate(rows, start=2):
            value = (row.get(id_col) or "").strip()
            ids.append(value)
            if not ID_PATTERNS[name].match(value):
                errors.append(f"{path.name}:{line_no} geçersiz {id_col}: {value!r}")
            for key, cell in row.items():
                if cell and ("\n" in cell or "\r" in cell):
                    errors.append(f"{path.name}:{line_no} çok satırlı hücre: {key}")
        dupes = sorted({x for x in ids if ids.count(x) > 1})
        for value in dupes:
            errors.append(f"{path.name}: yinelenen kimlik: {value}")

    if errors and not tables:
        return write_report(errors, warnings, tables)

    paragraphs = {r["paragraf_id"] for r in tables.get("paragraflar", [])}
    words = {r["kelime_id"] for r in tables.get("kelimeler", [])}
    sources = {r["kaynak_id"] for r in tables.get("kaynaklar", [])}

    for line_no, row in enumerate(tables.get("kelimeler", []), start=2):
        pid = row["paragraf_id"].strip()
        sid = row["kaynak_id"].strip()
        if pid not in paragraphs:
            errors.append(f"kelimeler.tsv:{line_no} bilinmeyen paragraf_id: {pid}")
        if sid and sid not in sources:
            errors.append(f"kelimeler.tsv:{line_no} bilinmeyen kaynak_id: {sid}")
        if not row["lemma"].strip():
            warnings.append(f"kelimeler.tsv:{line_no} lemma boş")
        if row["kaynak_dil"].startswith("Arapça") and row["kaynak_dil"] != "Arapça kalıp":
            if not row["Arapça_kök"].strip():
                warnings.append(f"kelimeler.tsv:{line_no} Arapça kelimede kök boş")
            if not row["vezin"].strip():
                warnings.append(f"kelimeler.tsv:{line_no} Arapça kelimede vezin boş")

    known_ids = paragraphs | words | sources
    id_re = re.compile(r"(?:PAR-YZ|KEL-YZ)-\d{4}|KAY-\d{4}")
    for line_no, row in enumerate(tables.get("duzeltmeler", []), start=2):
        refs = id_re.findall(row["kayıt_id"])
        if not refs:
            warnings.append(f"duzeltmeler.tsv:{line_no} kayıt_id içinde tanınan kimlik yok")
        for ref in refs:
            if ref not in known_ids:
                errors.append(f"duzeltmeler.tsv:{line_no} bilinmeyen kayıt kimliği: {ref}")
        if not row["eski_değer"].strip() or not row["yeni_değer"].strip():
            errors.append(f"duzeltmeler.tsv:{line_no} eski/yeni değer boş bırakılamaz")
        if not row["gerekçe"].strip():
            errors.append(f"duzeltmeler.tsv:{line_no} gerekçe zorunludur")

    return write_report(errors, warnings, tables)

def write_report(errors, warnings, tables) -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    counts = {name: len(rows) for name, rows in tables.items()}
    status = "BAŞARILI" if not errors else "BAŞARISIZ"
    lines = [
        "# AMK veri doğrulama raporu",
        "",
        f"**Sonuç:** {status}",
        "",
        "## Kayıt sayıları",
        "",
    ]
    for name in ["paragraflar", "kelimeler", "duzeltmeler", "kaynaklar"]:
        lines.append(f"- {name}: {counts.get(name, 0)}")
    lines += ["", "## Hatalar", ""]
    lines += [f"- {e}" for e in errors] or ["- Yok"]
    lines += ["", "## Uyarılar", ""]
    lines += [f"- {w}" for w in warnings] or ["- Yok"]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"AMK doğrulama: {status}")
    print(f"Hata: {len(errors)} | Uyarı: {len(warnings)}")
    print(f"Rapor: {REPORT.relative_to(ROOT)}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
