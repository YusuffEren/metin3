# Metin2Mobil demo v0.75.0 — statik analiz raporu

## Sonuç

APK başarıyla parçalandı. Java/Dalvik katmanındaki 36 sınıfın tamamı Java benzeri kaynak koda geri üretildi. APK'nin asıl oyun mantığının önemli bir kısmı uygulamanın ilk açılışta eriştiği güncelleme sunucusunda ayrı `.py` dosyaları halinde bulunuyor. Manifestte listelenen 100 Python kaynak dosyasının tamamı indirildi; boyutları ve SHA-1 değerleri tek tek doğrulandı.

Bu inceleme statiktir. APK çalıştırılmadı, oyun sunucusuna giriş yapılmadı ve 1,82 GB'lık varlık paketi indirilmedi.

## APK kimliği

- Dosya: `Metin2Mobil-demo-v0.75.0.apk`
- Paket: `com.averos2.mobile`
- Sürüm: `0.75.0` / versionCode `75`
- APK boyutu: `15.372.895` bayt
- APK SHA-256: `89cbe8e5d7fc7b41b6b42b39d0f402b5042f84e325eaa4c26d40dabc551992f5`
- Minimum / hedef SDK: `26` / `35`
- Ana aktivite: `com.sancak2.client.DownloadActivity`
- İmza sertifikası: `CN=Metin2 Mobile, OU=Mobilserverler, O=Mobilserverler.com, L=Istanbul, C=TR`
- Sertifika SHA-256: `0df4b0cc29bc86e9e3c13e59815559a058f34395f9a68116b12944a5e579373f`

## Mimari

1. `DownloadActivity` açılır ve `http://185.169.55.31/averos2/` taban adresini kullanır.
2. `apk/version.json` üzerinden APK güncellemesini kontrol eder.
3. `manifest.json` içindeki dosya envanterini yerel `bundle_manifest.json` ile karşılaştırır.
4. Eksik/değişmiş dosyaları `data/<manifest-path>` yolundan indirir; boyut ve SHA-1 kontrolü yapar.
5. İndirme bittikten sonra `Sancak2Activity` başlatılır.
6. `Sancak2Activity`, `libsancak2client.so` native kütüphanesini yükler.
7. Native çekirdek, indirilen `pack/`, `lib/`, `mobile_root/` ve diğer oyun verilerini çalıştırır.

## Erişilen kaynak kod

### Android / Java katmanı

`sources/` altında 36 sınıf bulunuyor. Önemli sınıflar:

- `DownloadActivity.java`: güncelleme, indirme, SHA-1 doğrulama ve oyunu başlatma.
- `Sancak2Activity.java`: native istemciyi yükleme, Android yaşam döngüsü, dokunma/klavye köprüsü ve bildirimler.
- `M2WebBrowser.java`: oyun içi WebView/popup köprüsü.
- `KeepAliveService.java`: oyun arka plandayken bağlantıyı canlı tutan foreground service.
- `ApkProvider.java`: indirilen APK güncellemesini Android paket yükleyicisine sunan provider.

Bu dosyalar decompiler çıktısıdır; orijinal değişken adları ve bazı kontrol akışları kaybolmuştur.

### Python oyun/UI katmanı

`remote-python-sources/mobile_root/` altında 100 doğrulanmış gerçek `.py` dosyası, toplam `2.822.901` bayt:

- Temel akış: `game.py`, `interfacemodule.py`, `intrologin.py`, `introcreate.py`, `introselect.py`, `introloading.py`.
- Sunucu yapılandırması: `serverinfo.py`.
- Envanter ve ticaret: `uiinventory.py`, `uishop.py`, `uishopsearch.py`, `uiofflineshop.py`, `ui_offline.py`, `uiexchange.py`, `uisafebox.py`.
- Mobil arayüz: `uimobilehud.py`, `uimobilelayout.py`, `uimobilelogin.py`, `uimobilestatus.py`.
- Oyun sistemleri: `uiauto.py`, `fishingbot.py`, `uicards.py`, `uicark.py`, `uiejder.py`, `uietkinlik.py`, `uichestdrop.py`, `uizindangiris.py`.
- Doğrulama sonuçları: `remote-python-sources/download-verification.json`.

### Native katman

- Dosya: `lib/arm64-v8a/libsancak2client.so`
- Mimari: ARM64 Android ELF
- Boyut: `13.630.224` bayt
- SHA-256: `8af3b18520e5acd0ef1f5e384b147e1cefe3c4faca20b0cd1df774ff7dbeb6f1`
- Çıkarılan yazdırılabilir dize sayısı: `53.029`

Native dosyada çok sayıda anlamlı C++ sembolü kalmış durumda. Bunlar arasında `CPythonNetworkStream`, `CAccountConnector`, `CPythonPlayer`, `CPythonApplication`, `CServerStateChecker` ve JNI köprüleri yer alıyor. Kütüphane ayrıca gömülü Python 2 çalışma zamanı, Crypto++, ses/görüntü bileşenleri ve klasik Metin2 istemci sınıflarını içeriyor. `native-strings/` dizini sonraki Ghidra/IDA çalışması için arama envanteri sağlar; bu rapor native makine kodunu C++ kaynağına çevirdiğini iddia etmez.

## Sunucu ve kanal bilgileri

`serverinfo.py` içindeki yapılandırma:

- Sunucu adı: `Averos2`
- Ana ad: `oyun.averos2.com`
- Sabit yedek IP: `185.169.55.31`
- Kimlik doğrulama portu: `11002`
- Kanal portları: `12002`, `12102`, `12202`, `12302`, `12402`, `12502`
- Mark portu: `12002`

İnceleme anındaki uzak manifest:

- Manifest sürümü: `1791518086`
- Dosya sayısı: `4.900`
- Toplam oyun verisi: `1.823.292.072` bayt (yaklaşık `1,70 GiB`)
- Sunucudaki APK sürümü: `0.78.0` / versionCode `78`
- Uzak APK boyutu: `15.606.651` bayt
- Uzak APK SHA-1: `56ffb55ca00dfc4a2eb8f3ba5e2d31478b79942a`

## Güvenlik açısından dikkat çekenler

- Manifestte `android:usesCleartextTraffic="true"` var ve güncelleme adresi düz HTTP kullanıyor.
- Oyun verileri SHA-1 ile doğrulanıyor, fakat hem manifest hem dosyalar aynı şifrelenmemiş kanaldan geliyor. Ağ üzerindeki bir saldırgan manifesti ve Python dosyalarını birlikte değiştirebilirse SHA-1 kontrolü bunu engellemez. İndirilen `.py` dosyaları istemci tarafından yürütüldüğü için bu ciddi bir tedarik zinciri riski oluşturur.
- APK kendi güncellemesini indirebiliyor ve `REQUEST_INSTALL_PACKAGES` izni istiyor. Android imza doğrulaması mevcut uygulamanın üzerine farklı imzalı paket kurulmasını sınırlar; yine de aktarımın HTTPS ve imzalı metadata ile korunması gerekir.
- `DownloadActivity` ve `Sancak2Activity` dışarıya açık (`exported=true`); provider ve keep-alive service dışarıya kapalıdır.
- `bundle_url.txt` taban adresi geçersiz kılma mekanizması bulunuyor. Dosya uygulamanın özel veri alanında olsa da debug/root/başka bir uygulama açığı senaryosunda indirme kaynağını değiştirebilir.

## Önerilen sonraki çalışma

1. Python kaynaklarını modül ve özellik bazında haritalandırmak.
2. `libsancak2client.so` dosyasını Ghidra ile ARM64 olarak açıp kalan C++ sembollerinden fonksiyon ağacı üretmek.
3. Güncelleme zincirini HTTPS, SHA-256 ve imzalı manifest ile güçlendirmek.
4. Kontrollü bir Android emülatöründe ağ trafiğini ve çalışma zamanı davranışını gözlemlemek.

## Çıktı dizini

- `sources/`: decompile edilmiş Java katmanı
- `remote-python-sources/`: sunucudan alınmış ve doğrulanmış Python kaynakları
- `AndroidManifest.decoded.xml`: çözülmüş manifest
- `metadata.json`: APK envanteri, hash'ler ve imza bilgisi
- `remote-manifest.json`: uzak oyun dosyası manifesti
- `remote-apk-version.json`: uzak APK sürüm kaydı
- `dex-strings.txt`: DEX dize sabitleri
- `native-strings/`: native kütüphane dize envanteri
- `raw/`: APK arşivinin ham içeriği
