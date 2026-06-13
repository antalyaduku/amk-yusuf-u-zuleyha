# Veri modeli

## `paragraflar.tsv`

Bir satır bir paragrafı temsil eder.

- `paragraf_id`: Kalıcı kimlik (`PAR-YZ-0001`)
- `eser_id`: Eser kısa kodu
- `pdf_sayfa`: PDF görüntü sıra numarası
- `matbu_sayfa`: Basılı eserde görünen sayfa
- `Osmanlıca_metin`: Kaynak harfli metin
- `diplomatik_çevriyazı`: Tarihî biçimleri mümkün olduğunca korur
- `normalleştirilmiş_okuma`: Okumayı bugünkü biçime yaklaştırır
- `günümüz_Türkçesi`: Anlam aktarımı
- `durum`: Doğrulama düzeyi
- `not`: Okuma ve sayfa notları

## `kelimeler.tsv`

Bir satır bir kelimeyi veya kalıplaşmış ifadeyi temsil eder.

`lemma`, `kaynak_dil`, `Arapça_kök`, `vezin`, Türkçe ek çözümlemesi,
temel anlam ve bağlam anlamı ayrı alanlarda tutulur.

## `duzeltmeler.tsv`

Doğrulanmış veya yayımlanmış kayıtların değişiklik geçmişidir.
Eski ve yeni değer birlikte tutulur. Düzeltme kaydı olmadan sessiz değişiklik
yapılmaz.

## `kaynaklar.tsv`

Her veri hükmünün bağlanabileceği nüsha, sözlük, makale veya alan uzmanı
düzeltmesi burada tanımlanır.

## Doğrulama durumları

- `Ham`
- `Ön okuma`
- `Kontrol gerekli`
- `Kullanıcı doğruladı`
- `Sözlükle doğrulandı`
- `Uzman doğruladı`
- `Şüpheli`
