# APK statik analiz özeti

Detaylı Türkçe inceleme için `ANALIZ-RAPORU.md` dosyasına bakın.

- Paket: `com.averos2.mobile`
- Sürüm: `0.75.0` (`75`)
- Ana aktivite: `com.sancak2.client.DownloadActivity`
- SDK: min `26`, hedef `35`
- SHA-256: `89cbe8e5d7fc7b41b6b42b39d0f402b5042f84e325eaa4c26d40dabc551992f5`
- DEX / sınıf: `1` / `36`
- Native kütüphane: `1`

## İzinler

- `android.permission.VIBRATE`
- `android.permission.INTERNET`
- `android.permission.FOREGROUND_SERVICE`
- `android.permission.POST_NOTIFICATIONS`
- `android.permission.WAKE_LOCK`
- `android.permission.ACCESS_NETWORK_STATE`
- `android.permission.REQUEST_INSTALL_PACKAGES`
- `android.permission.FOREGROUND_SERVICE_SPECIAL_USE`

## Bileşenler

- Aktivite: `com.sancak2.client.DownloadActivity`
- Aktivite: `com.sancak2.client.Sancak2Activity`
- Servis: `com.sancak2.client.KeepAliveService`
- Sağlayıcı: `com.sancak2.client.ApkProvider`

## Çıktılar

- `sources/`: DEX'ten geri üretilen Java benzeri kaynaklar
- `AndroidManifest.decoded.xml`: okunabilir manifest
- `dex-strings.txt`: DEX sabit dizeleri
- `native-strings/`: `.so` içindeki yazdırılabilir dizeler
- `raw/`: APK arşivinin ham içeriği
- `metadata.json`: makinece okunabilir envanter ve hash'ler

> Not: Decompile çıktısı orijinal kaynak kod değildir; değişken adları ve bazı kontrol akışları kaybolabilir.
