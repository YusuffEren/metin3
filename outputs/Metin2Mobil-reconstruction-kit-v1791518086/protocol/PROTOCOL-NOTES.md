# Metin2 Mobile ağ protokolü — yeniden oluşturma notları

Bu belge, `libsancak2client.so` ARM64 istemcisinin Ghidra sözde kodundan çıkarılmıştır. Özgün sunucu başlığı veya özgün kaynak kod değildir.

## Taşıma ve çerçeveleme

- Kimlik doğrulama ve oyun kanalı TCP kullanıyor. İstemcide görülen varsayılan hedef portlar sırasıyla `11002` ve `12002`.
- Paket başlığı ilk bayt. Yorumlama aktif faza bağlı: aynı başlık farklı fazlarda başka anlama gelebiliyor.
- Faz paketi `FD <phase>`; değerler: `0=offline`, `1=handshake`, `2=login`, `3=select`, `4=loading`, `5=game`.
- Handshake paketi 13 bayt: `FF + u32 token + u32 server_time_ms + i32 delta`.
- Ping `2C`, istemci cevabı `FE`.
- İstemci gönderimlerinin çoğu `SendSequence()` çağrısıyla bitiyor. Bu, oyun sunucusunun ağ katmanında doğruladığı ek sıra/güvenlik durumudur; katalogdaki yapı boylarına dahil değildir.

## Şifreleme durumu

İstemci `FB` başlıklı 261 baytlık anahtar anlaşması paketiyle `CNetworkStream::Prepare/Activate` çağrılarını kullanıyor. `FA` anahtar anlaşmasının tamamlandığını bildiriyor ve ardından `ActivateCipher()` çalışıyor. `98` ve `99` hibrit şifre anahtarı/SDB paketleri ayrıca işleniyor.

Dolayısıyla yalnızca paket yapılarını bilmek tam üretim oturumu kurmaya yetmez. Tam uyumluluk için aşağıdakilerin de yeniden uygulanması gerekir:

1. `Prepare`, `Activate` ve `ActivateCipher` algoritmaları ile oturum anahtarı üretimi.
2. `SendSequence` durum tablosu ve sunucu doğrulaması.
3. `GamePhase` içindeki değişken uzunluklu paketlerin tüm uzunluk kuralları.
4. Login-success içindeki karakter kayıtlarının kesin alan adları ve oyun sunucusu yönlendirmesi.

## Kanıt düzeyleri

- `packet-catalog.csv`: İstemcide doğrudan sabit başlık ve `Send/Recv` boyu görülerek doğrulanmış çekirdek paketler.
- `packet-function-candidates.csv`: 375 gönderme/alma işlevi için otomatik tarama sonucu. Boyut ve sabit sütunları araştırma ipucudur; doğrudan protokol sözleşmesi sayılmamalı.
- `native/network-protocol.c`: Bu bulguların dayandığı 1.019 ağ/şifreleme işlevinin sözde kodu.

## Eğitim sunucusunun kapsamı

`emulator/server.py` varsayılan olarak sadece `127.0.0.1` üzerinde pasif gözlemci olarak çalışır. `--mode login-failure` seçeneği handshake, login fazı ve kontrollü login-hatası cevabını üretir. Bu yol istemcinin ilk ağ akışını sınamak içindir; hesap veritabanı, karakter seçimi veya oyun dünyası sunucusu değildir.

Üretim IP'sine bağlanma, parola deneme veya sunucuya veri yazma işlemi yapmaz.
