# AMK — Yusuf u Züleyha veri çalışması

Bu depo, *Yusuf u Züleyha* metnini paragraf paragraf işleyen küçük ve
denetlenebilir bir tarihî Türkçe veri çalışmasıdır.

## Temel karar

**Asıl veri `data/*.tsv` dosyalarıdır.** Excel dosyası yalnızca insan
tarafından rahat görüntüleme için üretilmiş dışa aktarımdır.

## Yapı

- `data/paragraflar.tsv`: Her paragraf bir satır.
- `data/kelimeler.tsv`: Her çözümlenen kelime veya kalıp bir satır.
- `data/duzeltmeler.tsv`: Eski okuma, yeni okuma ve gerekçe.
- `data/kaynaklar.tsv`: Nüsha, sözlük, makale ve kullanıcı düzeltmeleri.
- `scripts/validate_data.py`: Kimlikleri ve tablolar arası bağlantıları denetler.
- `scripts/build_jsonl.py`: Paragraf ve kelimeleri yapay zekâ/RAG için JSONL'e dönüştürür.
- `AGENTS.md`: Codex'in uyması gereken proje kuralları.
- `docs/`: Veri modeli ve çalışma yöntemi.
- `exports/`: Excel gibi türetilmiş dosyalar.
- `sources/`: Kaynak PDF'ler yerelde tutulur; varsayılan olarak Git'e eklenmez.

## Denetim

Terminalde proje klasöründe:

```bash
python3 scripts/validate_data.py
python3 scripts/build_jsonl.py
```

Doğrulama başarısızsa yeni veri sürümü yayımlanmaz.

## Sürümleme

- Yeni paragraf veya küçük düzeltme: `v0.1 → v0.2`
- Veri şeması değişikliği: daha büyük sürüm artışı
- Doğrulanmış bir okuma sessizce değiştirilmez; `duzeltmeler.tsv` kaydı zorunludur.
