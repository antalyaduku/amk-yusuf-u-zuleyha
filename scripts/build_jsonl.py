#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "derived" / "paragraphs_with_words.jsonl"

def read_tsv(name: str):
    with (DATA / name).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

def main() -> int:
    paragraphs = read_tsv("paragraflar.tsv")
    words = read_tsv("kelimeler.tsv")
    corrections = read_tsv("duzeltmeler.tsv")
    sources = {r["kaynak_id"]: r for r in read_tsv("kaynaklar.tsv")}

    words_by_paragraph = {}
    for word in words:
        record = dict(word)
        sid = record.get("kaynak_id", "")
        record["kaynak"] = sources.get(sid)
        words_by_paragraph.setdefault(record["paragraf_id"], []).append(record)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for paragraph in paragraphs:
            pid = paragraph["paragraf_id"]
            record = {
                **paragraph,
                "kelimeler": words_by_paragraph.get(pid, []),
                "duzeltmeler": [
                    c for c in corrections if pid in c.get("kayıt_id", "")
                ],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Oluşturuldu: {OUT.relative_to(ROOT)}")
    print(f"Paragraf: {len(paragraphs)} | Kelime: {len(words)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
