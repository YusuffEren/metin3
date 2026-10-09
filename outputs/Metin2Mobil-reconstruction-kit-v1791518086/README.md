# Metin2Mobil yeniden oluşturma kiti — v1791518086

Bu paket, demo istemcisinden çıkarılan materyali yeniden yapım çalışmalarına dönüştürür. Özgün kaynak depo değildir; Python/Java dosyaları gerçek dağıtılan dosyalardır, native `.c` dosyaları Ghidra sözde kodudur.

## Sonuç özeti

- Tam güncelleme kümesi: 4.900/4.900 dosya, 1.823.292.072 bayt.
- EterPack açılımı: 96/96 paket, 56.666 dosya, 2.177.324.309 bayt.
- Native analiz: 32.151 işlev; 32.146 sözde kod, 5 assembly fallback.
- Bu kitte indekslenen seçilmiş native işlev: 7.978.
- Python: 311 dosya, 1.979 bağımlılık kenarı, 1.062 kullanılan native API çağrısı, 834 native sabit.
- Oyun tabloları: 6.037 eşya ve 1.347 yaratık/NPC, XTEA+LZO katmanından doğrulanarak CSV'ye çıkarıldı.
- Ağ: 375 otomatik paket işlevi adayı; 42 çekirdek paket elle doğrulanmış katalogda.

## Dizinler

- `assets/`: uzantı/dizin envanteri, kritik dosya hash'leri ve harita atlası.
- `game-data/`: çözülmüş `item_proto.csv`, `mob_proto.csv` ve ham kayıt blokları.
- `python/`: bağımlılık grafiği, native modül listesi, kullanılan API çağrıları ve sabitler.
- `native/`: ağ, Python API, oynanış, grafik/kaynak ve Android alanlarına ayrılmış sözde kod.
- `protocol/`: doğrulanmış paket kataloğu, otomatik adaylar, C başlığı ve araştırma notları.
- `emulator/`: localhost eğitim sunucusu, paket çözücü ve testler.
- `tools/`: kiti tekrar üretmek için kullanılan betikler.

Tam 61 MB native döküm ve 2,17 GB varlık ağacı ayrı çıktılardadır; kit onları çoğaltmaz.

## Eğitim sunucusunu çalıştırma

```powershell
cd emulator
python -m unittest -v
python server.py --mode observe
```

İlk handshake/login UI akışını kontrollü hata cevabıyla denemek için:

```powershell
python server.py --mode login-failure
```

Her iki mod da varsayılan olarak yalnızca `127.0.0.1:11002` ve `127.0.0.1:12002` üzerinde dinler.

## İlgili ana çıktılar

- Tam varlıklar: `../Metin2Mobil-full-v1791518086/unpacked/`
- Gerçek Python/Java kod paketi: `../Metin2Mobil-kodlar-v1791518086/`
- Tam native sözde kod: `../Metin2Mobil-native-pseudocode-v0.75.0/libsancak2client-complete.c`

## Sınır

İstemci içinde bulunmayan özgün sunucu kaynak kodu tersine mühendislikle “çıkarılamaz”. Bu kit, görülebilen protokol ve veri sözleşmesinden uyumlu bir sunucu yazmaya temel sağlar. Birebir sunucu için sahibin özgün repo/yedek erişimi gerekir.
