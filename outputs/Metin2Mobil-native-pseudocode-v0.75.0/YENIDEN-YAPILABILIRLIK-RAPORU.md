# Metin2Mobil yeniden yapılabilirlik raporu

İnceleme tarihi: 2026-10-09

## Kısa cevap

Mevcut materyalle oyunun istemci tarafı ve aynı varlıkları kullanan benzer bir oyun büyük ölçüde yeniden yapılabilir. Ancak yalnızca bu dosyalarla özgün oyunun birebir, üretime hazır ve aynı sunucu davranışlarına sahip kopyası derlenemez.

Bunun nedeni iki ayrı ürün bulunmasıdır:

1. **İstemci:** Android kabuğu, Python arayüz/oyun mantığı, ARM64 C++ motoru ve varlıklar.
2. **Sunucu:** Hesap, karakter, dünya durumu, savaş doğrulaması, eşya ekonomisi, görevler, veritabanı ve yönetim servisleri.

İstemci tarafının büyük bölümü elde edildi. Özgün sunucu programı ve veritabanı şeması istemci dağıtımında bulunmuyor.

## Elde edilen kaynak düzeyi

- `296` açılmış paket içi Python dosyası.
- Kod paketinde tekrarlar/dışarıdan yayımlananlarla birlikte `396` Python dosyası.
- DEX'ten decompile edilmiş `36` Java sınıfı.
- ARM64 kitaplıkta `15.401` adlandırılmış dinamik fonksiyon.
- Ghidra'nın yürütülebilir bellekte tanımladığı `32.151` fonksiyon.
- C-benzeri sözde koda çevrilen `32.146` fonksiyon; kalan `5` fonksiyonun ARM64 assembly dökümü ayrıca çıkarıldı.
- Tam sözde kod çıktısı yaklaşık `1.619.537` satır ve `61,4 MB`.
- `597` ağ/protokol, `555` oynanış, `868` aktör/karakter ve `216` paket/kaynak kategorili adlandırılmış yerel fonksiyon.
- `56.666` çıkarılmış varlık dosyası.

`libsancak2client-complete.c` özgün C++ değildir. Derleyicinin ürettiği ARM64 makine kodundan yeniden oluşturulmuş sözde koddur; değişken adları, yorumlar, özgün sınıf tanımları, şablon türleri ve derleme sistemi geri gelmez.

## Yeniden kullanılabilir bölümler

- Arayüzler, pencereler ve istemci oyun akışı: yüksek oranda yeniden kurulabilir.
- Modeller, animasyonlar, haritalar, efektler, sesler ve dokular: elde edildi.
- Sunucu adresi ve kanal yapılandırması: elde edildi.
- Paket biçimi ve şifreli varlıkların açılması: çözüldü.
- Android etkinliği, dokunmatik/klavye köprüsü: Java ve yerel semboller üzerinden incelenebilir.
- Ağ protokolü: gönderme/alma fonksiyonlarından ve paket işleyicilerinden yeniden belgelenebilir.
- Yerel karakter, grafik, kaynak ve oyun sistemleri: sözde koddan bağımsız olarak yeniden uygulanabilir.

## Eksik kalan özgün parçalar

- Sunucu yürütülebilirleri ve sunucu C/C++ kaynakları.
- Veritabanı şeması ve canlı veriler.
- Sunucu görev betikleri; paketlerde `.lua` veya `.sql` dosyası bulunmadı.
- Özgün C++ başlıkları ve kaynakları; paketlerde `.cpp`, `.cc`, `.cxx`, `.h` veya `.hpp` bulunmadı.
- Derleme sistemi, özgün bağımlılık sürümleri ve geliştirici ortamı.
- Sunucunun hile önleme ve doğrulama kurallarının tam davranışı.

## Gerçekçi yeniden yapım yolları

### Bağımsız yeniden uygulama

En güvenli ve teknik olarak en temiz yol budur. Mevcut varlık/Python davranışları referans alınır; istemci motoru Unity, Godot veya yeni bir C++ katmanında yeniden yazılır. Sunucu ise belgelenen paket akışına göre sıfırdan oluşturulur. Bu yöntem özgün kaynak gerektirmez fakat önemli mühendislik ister.

### Mevcut ARM64 istemcisini kullanmak

İstemci korunur, ağ protokolü belgelenerek uyumlu bir eğitim sunucusu yazılır. Ağ fonksiyon adları ve sözde kod bunun için yeterli başlangıç sağlar. Yine de karakter, savaş, eşya, dünya ve veritabanı davranışlarının sunucu tarafında yeniden tasarlanması gerekir.

### Birebir özgün kaynak kod

İstemci paketinden buna ulaşmak mümkün değildir. Özgün sunucu kaynakları yalnızca geliştiricinin kaynak deposu, yedekleri veya yasal olarak sağladığı sunucu dağıtımında bulunabilir. Çalışan uzak sunucuya izinsiz erişim veya güvenlik açığı kullanımı bu analizin kapsamına alınmamıştır.

## Dosyalar

- `libsancak2client-complete.c`: Yürütülebilir bellekteki bütün tanımlı fonksiyonların sözde kodu.
- `libsancak2client-selected.c`: Oyuna ilişkin seçilmiş fonksiyonların daha küçük sözde kod dökümü.
- `decompile-failures-arm64.asm`: C-benzeri çıktısı üretilemeyen beş fonksiyonun assembly dökümü.
- `native-function-symbols.tsv`: Adres, boyut, kategori ve sembol adları.
- `native-symbol-summary.json`: Sembol kategori özeti.
- Tam Python/Java kod paketi: `../Metin2Mobil-kodlar-v1791518086.zip`.
- Tam varlıklar: `../Metin2Mobil-full-v1791518086/unpacked/`.

## Son değerlendirme

Bir ekip bu materyalle oyunu **yeniden geliştirebilir**, fakat bu işlem “kaynakları açıp derlemek” değildir. İstemci tarafı güçlü biçimde belgelenmiş ve büyük ölçüde görünür durumdadır; sunucu tarafı ise protokol ve gözlenen istemci beklentileri temel alınarak yeniden yazılmalıdır.
