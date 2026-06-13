# Çalışma akışı

1. Kaynak sayfadan yalnızca bir paragraf seçilir.
2. Osmanlı harfli metin ve diplomatik çevriyazı hazırlanır.
3. Normalleştirilmiş okuma ve günümüz Türkçesi ayrı tutulur.
4. Açıklanacak kelimeler `kelimeler.tsv` dosyasına eklenir.
5. Kök, vezin ve anlam için kullanılan kaynak `kaynak_id` ile bağlanır.
6. Kullanıcı bir okumayı düzeltirse:
   - esas kayıt güncellenir,
   - `duzeltmeler.tsv` dosyasına eski/yeni değer ve gerekçe eklenir.
7. Veri denetimi çalıştırılır.
8. JSONL çıktısı yeniden oluşturulur.
9. Yeni sürüm adı verilir.

## Otomatikleştirilen işler

- Kimlik biçimi ve benzersizlik denetimi
- Paragraf–kelime ve kelime–kaynak bağlantıları
- Eksik zorunlu alan uyarıları
- Düzeltme kaydı bağlantısı
- JSONL/RAG çıktısı
- GitHub üzerinde her değişiklikte otomatik test

## İnsan denetiminde kalan işler

- Osmanlıca okuma
- Sağır kef ve benzeri paleografik ayrıntılar
- Arapça kök ve vezin
- Bağlam anlamı
- Metnin günümüz Türkçesine aktarımı
