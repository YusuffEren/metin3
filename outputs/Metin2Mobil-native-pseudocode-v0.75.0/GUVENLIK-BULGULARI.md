# Metin2Mobil güvenlik bulguları

İnceleme tarihi: 2026-10-09

Kapsam: Sağlanan APK, manifestten indirilen istemci dosyaları ve APK'nin işaret ettiği `185.169.55.31` güncelleme/oyun altyapısında tahribatsız kontroller.

## Kritik — İmzalanmamış HTTP güncelleme kanalı

`DownloadActivity` manifesti, APK sürüm bilgisini ve bütün oyun dosyalarını düz HTTP üzerinden alıyor. Uygulama manifestinde `android:usesCleartextTraffic="true"` etkin.

Dosyalar ve APK için SHA-1 kontrolü yapılması bu sorunu çözmüyor; beklenen SHA-1 değeri de aynı kimliği doğrulanmamış HTTP kanalından geliyor. Ağ konumundaki bir saldırgan hem dosyayı hem manifestteki özetini değiştirebilir.

Paket içinde çalıştırılan Python dosyaları bu kanaldan indirildiği için bu durum istemci bağlamında kod çalıştırmaya dönüşebilir. APK güncellemesinde Android'in paket imza doğrulaması aynı paket kimliğinin sessizce değiştirilmesini sınırlar; ancak oyun verisi/Python katmanı ayrıca kriptografik olarak imzalanmıyor.

Öneri:

- Güncelleme alanını HTTPS'e taşıyın ve HTTP'yi kapatın/yönlendirin.
- Manifesti çevrimdışı özel anahtarla Ed25519 veya ECDSA kullanarak imzalayın; istemcide yalnızca açık anahtar bulunsun.
- SHA-256 dosya özetleri kullanın. Özet, imzalı manifestin içinde yer almalı.
- İndirilen çalıştırılabilir Python dosyalarını imza doğrulanmadan yüklemeyin.
- `usesCleartextTraffic` değerini kaldırın veya yalnızca zorunlu alanlarla sınırlı network security config kullanın.

## Yüksek — İstemcide balık botu ve GM algılama/kaçınma kodu

`unpacked/root/fishingbot.py` içinde `MultihackDialog`, otomatik balık tutma, otomatik eşya kullanma/satma/atma ve GM fısıltısında çıkış veya oturum kapatma davranışları bulunuyor. `interfacemodule.py` bu dosyayı doğrudan yükleyen `Umut()` metodunu içeriyor.

Bu yalnızca kullanılmayan bir metin değil; ağ paketleri gönderen ve oyun durumunu değiştiren çalışır istemci kodu.

Öneri:

- Dosyayı üretim paketinden çıkarın.
- Balık tutma zamanlaması, eşya kullanımı/satışı ve istek oranlarını sunucuda doğrulayın.
- GM varlığı/fısıltısı üzerinden istemciye ayrıcalıklı sinyal gönderen davranışlara güvenmeyin.
- CI aşamasında `hack`, `bot`, otomatik paket gönderimi ve debug/admin modülleri için yasaklı-dosya kontrolü ekleyin.

## Yüksek — Yönetim arayüzleri ve komut adları istemcide

`uiadminwhisper.py` toplu fısıltı ve `/b`; `uimaintenanceadmin.py` ise `/maintenance`, `/maintenance_text` ve `/maintenance_update` komutlarını gönderiyor. Arayüzler normal istemci paketinde dağıtılıyor.

Komutların varlığı tek başına sunucu açığı değildir. Ancak sunucu yetkiyi yalnızca gizli istemci arayüzüne veya istemciden gelen bir bayrağa dayandırıyorsa herhangi bir değiştirilmiş istemci bunları çağırabilir.

Öneri:

- Her yönetim komutunda sunucu tarafında oturum/rol kontrolü yapın.
- Yönetim protokolünü normal oyun kanalından ayırın veya güçlü yeniden kimlik doğrulama kullanın.
- Normal oyuncu derlemesinden yönetim arayüzlerini kaldırın.
- Başarısız yönetim komutu denemelerini hız sınırlı biçimde kaydedin ve alarm üretin.

## Yüksek — Varlık şifreleme anahtarları istemciden kurtarılabiliyor

EterPack dizin ve veri anahtarları ARM64 kitaplık içinde bulundu ve bütün `96` paket `56.666` dosyaya hatasız açıldı. İstemcinin içindeki simetrik anahtarlar gizli kabul edilemez.

Öneri:

- Varlık şifrelemesini fikrî mülkiyet güvenlik sınırı olarak değerlendirmeyin.
- Bütün güvenlik kararlarını sunucuda verin.
- Hassas sır, yönetim anahtarı veya sunucu güven bilgilerini istemciye koymayın.
- Varlık bütünlüğü gerekiyorsa şifreleme yerine/asıl olarak imzalı manifest kullanın.

## Orta — Eski ve internete açık SSH yüzeyi

TCP `22` internete açık. Banner `OpenSSH_7.8 FreeBSD-20180909`. Parola kimlik doğrulaması sunulmadı; sunucu `publickey,keyboard-interactive` bildirdi ve modern `curve25519-sha256`/Ed25519 kullandı. Banner tek başına yamalanmamış bir açık kanıtı değildir; FreeBSD güvenlik yamaları sürüm dizesini değiştirmeden geri taşınmış olabilir.

Öneri:

- SSH'ı VPN veya yönetim IP allowlist arkasına alın.
- Keyboard-interactive gerekmiyorsa kapatın; yalnızca anahtar kullanın.
- FreeBSD ve OpenSSH yama seviyesini sunucu üzerinde doğrulayın.
- Root girişini kapatın, başarısız denemeleri sınırlayın ve denetim kaydı tutun.

## Orta — Güncelleme altyapısı ve tam dosya listesi herkese açık

`/averos2/` ve `/averos2/manifest.json` kimlik doğrulamasız olarak tam manifesti döndürüyor. Sunucu `darkhttpd/1.17.from.git` ürün bilgisini açıklıyor. `.git`, `.env`, yaygın ZIP yedekleri ve temel traversal denemeleri sırasıyla `404` veya `400` döndürdü; bu kontrollerde doğrudan sunucu kaynak sızıntısı bulunmadı.

Öneri:

- Ürün banner'ını kapatın (`--no-server-id`).
- Güncelleme kökünü yalnızca gerekli dosyalara ayırın ve salt okunur çalıştırın.
- `--chroot`, ayrı düşük yetkili kullanıcı ve `--hide-dotfiles` kullanın.
- Web kökünde kaynak, yedek, anahtar veya yapılandırma bulunmadığını CI/deploy sırasında doğrulayın.

## Düşük/sertleştirme — Android yüzeyi

- `Sancak2Activity` ve `DownloadActivity` dışa açık.
- Uygulama `REQUEST_INSTALL_PACKAGES` izni istiyor.
- APK yalnızca v2 imza şemasıyla imzalı; sertifika RSA-2048.
- `allowBackup=false` olumlu bir ayar.

Öneri:

- Dışa açık olması gerekmeyen activity'leri kapatın veya izinle koruyun.
- Öz-güncelleme zorunlu değilse `REQUEST_INSTALL_PACKAGES` iznini kaldırın.
- Güncel Android imza şemalarını ve Play/App Store kontrollü dağıtımı değerlendirin.

## Tahribatsız dış yüzey sonucu

- Gözlenen açık servisler: TCP `22`, TCP `80`; oyun portları ölçüm anına göre değişken yanıt verdi.
- HTTP: `darkhttpd/1.17.from.git`, yalnızca statik içerik.
- `.git/HEAD`, `.env`, yaygın `server.zip`/`backup.zip`: bulunmadı.
- Dört temel kodlanmış path traversal denemesi: tamamı HTTP `400`.
- SSH kimlik bilgisi denemesi, parola tahmini, hizmet bozma veya veri değiştirme yapılmadı.

## Kaynak koda erişim sonucu

İstemci tarafında ulaşılabilecek sınır pratik olarak tamamlandı: Python ve Java kaynakları, tüm varlıklar, 32.146 fonksiyonluk C-benzeri yerel döküm ve kalan beş fonksiyonun assembly'si mevcut.

Sunucu kaynakları HTTP kökünde yayımlanmıyor ve SSH anahtarı/hesabı olmadan sunucu dosya sistemine meşru erişim yok. Eksiksiz sunucu kodu için kaynak deposu, sunucu yedeği veya yetkili SSH erişimi sağlanması gerekir.
