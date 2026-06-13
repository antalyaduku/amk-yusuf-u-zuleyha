# AGENTS.md — AMK veri bütünlüğü kuralları

Bu depoda amaç gösterişli bir uygulama geliştirmek değil; küçük, kaynaklı ve
düzeltilebilir tarihî Türkçe verisi üretmektir.

## Kaynakların üstünlüğü

1. `data/*.tsv` dosyaları tek doğruluk kaynağıdır.
2. `exports/*.xlsx` ve `derived/*.jsonl` türetilmiş çıktıdır; bunlar elle
   düzenlenmez.
3. Kaynak PDF'ler telif ve dosya büyüklüğü sebebiyle `sources/` altında
   yerelde tutulur ve varsayılan olarak Git'e eklenmez.

## Zorunlu yöntem

- Her paragrafın kalıcı bir `paragraf_id` değeri bulunur.
- Her kelime ilgili `paragraf_id` ile bağlanır.
- Her sözlük, nüsha veya kullanıcı düzeltmesi `kaynak_id` ile kaydedilir.
- Doğrulanmış bir değer değiştirilecekse eski değer silinmez:
  `data/duzeltmeler.tsv` dosyasına kayıt eklenir.
- Diplomatik çevriyazı ile normalleştirilmiş biçim karıştırılmaz.
  Örnek: diplomatik `soŋ`, normalleştirilmiş `son`.
- Sağır kef `ڭ`, bağlama göre nazal n / ŋ olarak değerlendirilir.
- Arapça kök veya vezin emin olunmadan doldurulmaz. Tahminler
  `doğrulama_durumu=Şüpheli` veya `Kontrol gerekli` olarak işaretlenir.
- Yapay zekâ çıktısı tek başına kaynak değildir.
- Kaynak gösterilmeyen yeni dilbilimsel hüküm doğrulanmış kabul edilmez.
- Boş bilgiyi uydurmak yerine alanı boş bırak ve nota gerekçeyi yaz.

## Yeni kayıt eklerken

- Kimlikleri mevcut en büyük numaradan sonra artır.
- TSV sütun sırasını değiştirme.
- Dosyaları UTF-8 olarak kaydet.
- Çok satırlı hücre kullanma; satır sonlarını boşlukla değiştir.
- Önce veriyi ekle, sonra:
  `python3 scripts/validate_data.py`
- Hata yoksa:
  `python3 scripts/build_jsonl.py`

## Codex görevlerinde beklenen çıktı

Her görev sonunda:
1. Değiştirilen dosyaları listele.
2. Eklenen paragraf/kelime/düzeltme sayılarını yaz.
3. Doğrulama komutunun sonucunu bildir.
4. Şüpheli okumaları ayrıca işaretle.
5. Kullanıcının paleografik düzeltmelerini öncelikli veri olarak işle,
   fakat düzeltme geçmişini koru.
