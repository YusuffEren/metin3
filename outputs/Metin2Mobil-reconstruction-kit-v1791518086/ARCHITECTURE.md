# Yeniden üretim mimarisi

## Çıkarılan katmanlar

```text
Android Java başlatıcı/güncelleyici (36 dosya)
        |
        v
EterPack kaynak katmanı (96 paket -> 56.666 dosya, 2.177.324.309 bayt)
        |
        +--> Python 2 oyun/UI katmanı (311 .py/.py.bak; 1.979 bağımlılık)
        |         |
        |         +--> 48 native/harici modül, 1.062 kullanılan çağrı
        |
        v
ARM64 C++ istemci motoru (32.151 işlev; 32.146 sözde kod, 5 assembly)
        |
        +--> Ağ/faz/şifreleme
        +--> Karakter, eşya, beceri, lonca, görev, dükkân
        +--> BGFX/Granny/EterPack grafik ve kaynak sistemi
        +--> Android/JNI platform katmanı
```

## Temiz oda yeniden yapımında önerilen sınırlar

1. **Veri katmanı:** `game-data/item_proto.csv` (6.037 eşya), `game-data/mob_proto.csv` (1.347 yaratık/NPC), harita atlası, beceri ve yerelleştirme tabloları.
2. **Python uyumluluk katmanı:** `python/native-api-calls.csv` içindeki API yüzeyini modül modül taklit et. En büyük yüzeyler `player`, `chrmgr`, `wndMgr`, `app`, `item`, `chat` ve `net`.
3. **Dünya/görselleştirme:** Harita RAW/ATR/WTR verileri, DDS/TGA dokular, GR2 modeller ve MSA/MSS hareket betikleri. Özgün motoru yeniden derlemek yerine uyumlu bir dönüştürücü/ithalat katmanı daha güvenli ve sürdürülebilir olur.
4. **Ağ:** Önce handshake/login/select akışı; daha sonra `GamePhase` paketleri. Sunucu her eylemi yetkilendirmeli; istemci Python koduna güvenmemeli.
5. **Sunucu mantığı:** İstemcide bulunmayan hesap, kalıcı dünya, düşürme, ekonomi, görev otoritesi ve hile denetimi temiz oda olarak yeniden yazılmalı veya sahibin özgün sunucu deposundan alınmalı.

## Ne kadar yeniden üretilebilir?

İstemci deneyiminin büyük bölümü yeniden üretilebilir: görseller, sesler, haritalar, UI betikleri, eşya/yaratık tabloları, istemci davranışı ve önemli protokol yapıları mevcut. Ancak bu çıktı özgün C++ kaynak ağacının yerini birebir tutmaz. Derleme dosyaları, yorumlar, özgün tür adlarının bir kısmı, beş çözülemeyen işlev ve özellikle sunucu kaynakları istemci ikilisinde yoktur.

Sonuç: **işlevsel bir temiz-oda yeniden yapım mümkün; özgün oyunun birebir kaynak deposunu yalnızca APK'den geri almak mümkün değil.** Tam sunucu eşdeğerliği için sunucu Git deposu, yedek veya yetkili SSH anahtarı gerekir.

## En kritik eksikler

- Anahtar anlaşması/cipher ve sequence katmanının bit düzeyi uyumluluğu.
- `GamePhase` içindeki tüm S2C/C2S değişken paketlerin şeması.
- GR2 lisanslı biçimi için güvenilir dönüştürme/çalıştırma yolu.
- Sunucu DB şeması, görev state machine'leri, drop/spawn tabloları ve ekonomi kuralları.
- Üretim tarafında admin komutlarının rol denetimi.
