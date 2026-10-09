# Metin2Mobil demo tersine mühendislik sonucu

## Elde edilenler

- Güncelleme sunucusundaki `1791518086` sürümü eksiksiz indirildi: 4.900/4.900 dosya, 1.823.292.072 bayt.
- 96/96 EterPack açıldı: 56.666 dosya, 2.177.324.309 bayt.
- Dağıtılan gerçek Python ve Java kaynakları ayrıldı: 396 Python/backup ve 36 Java dosyası.
- ARM64 istemcide 32.151 işlev bulundu; 32.146 işlev Ghidra sözde koduna çevrildi. Beş başarısız işlev assembly olarak saklandı.
- `item_proto` ve `mob_proto` XTEA+LZO katmanı açıldı: 6.037 eşya ile 1.347 yaratık/NPC tam CSV tablosu üretildi.
- Python bağımlılık grafiği ve native API kullanım sözleşmesi çıkarıldı: 1.979 kenar, 1.062 çağrı, 834 sabit.
- Ağ protokolünde 375 aday işlev kataloglandı; 42 çekirdek paket başlık/boyut düzeyinde doğrulandı.
- Localhost eğitim sunucusu/observer ve beş başarılı protokol testi hazırlandı.

## Ana teslimatlar

- `Metin2Mobil-full-v1791518086/`: İndirilen paketler ve bütün açılmış varlıklar.
- `Metin2Mobil-kodlar-v1791518086.zip`: Gerçek Python/Java kodları ve seçilmiş native analiz.
- `Metin2Mobil-native-pseudocode-v0.75.0/`: 61.375.039 baytlık tam native sözde kod ve fallback assembly.
- `Metin2Mobil-reconstruction-kit-v1791518086.zip`: Veri tabloları, protokol, bağımlılık/API haritaları, alanlara ayrılmış native kod ve eğitim sunucusu.
- `Metin2Mobil-demo-v0.75.0-analysis.zip`: İlk APK analiz paketi.

## SHA-256

```text
3F3320B2414AEE3A25F0B10976172BB527F5AC7C48166A70FF7E8F12DE8BF859  Metin2Mobil-demo-v0.75.0-analysis.zip
91FCFE0AA0DDF030F85DC144503BAD4372FD35C361333E6B21949D71DA757146  Metin2Mobil-kodlar-v1791518086.zip
AB3348355538BD481C04CE020784A436C8C5294230D3E8D48CB171493A5E595B  Metin2Mobil-reconstruction-kit-v1791518086.zip
E19963C0909C70524C846BD5D4EBCB05F971CF06208091C55AE2B799419E650B  libsancak2client-complete.c
```

## Kesin sınır

Bu materyal işlevsel bir temiz-oda istemci ve uyumlu sunucu geliştirmek için güçlü bir temel oluşturur. Ancak APK yalnızca istemciyi içerdiğinden özgün sunucu kaynak deposu, DB şeması, görev/spawn/drop otoritesi ve derleme altyapısı istemciden geri çıkarılamaz. Birebir sunucu kodu için proje sahibinin Git deposu, yedeği veya yetkili SSH anahtarı gerekir.
