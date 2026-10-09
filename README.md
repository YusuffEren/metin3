# Metin3 / Metin2Mobil yeniden oluşturma çalışması

Bu depo, `Metin2Mobil-demo-v0.75.0.apk` istemcisinin proje sahibinin izniyle yapılan eğitim ve güvenlik odaklı tersine mühendislik çalışmasını içerir. Hedef, dağıtılan istemcideki veriyi ve davranışı belgelemek, açıkları görmek ve temiz-oda yöntemiyle yeniden üretilebilir bir teknik temel hazırlamaktır.

Önemli ayrım: Depoda gerçek dağıtılmış Python/Java dosyaları ve oyun varlıkları bulunur. `libsancak2client` için üretilen C dosyaları ise özgün C++ kaynak kodu değil, ARM64 ikiliden Ghidra ile oluşturulmuş sözde koddur.

## Neler bulundu?

- Güncelleme sürümü `1791518086` için manifestteki 4.900 dosyanın tamamı indirildi: 1.823.292.072 bayt.
- 96 EterPack paketinin tamamı açıldı: 56.666 oyun dosyası, 2.177.324.309 bayt.
- Varlıklar arasında 8.961 GR2 model, 8.276 DDS doku, 6.408 MSA animasyon, 5.116 MSS hareket betiği, 1.602 WAV ses ve bütün harita RAW/ATR/WTR katmanları var.
- Dağıtılmış istemci kodundan 396 Python/backup ve 36 Java dosyası ayrıldı.
- ARM64 istemcide 32.151 çalıştırılabilir işlev bulundu. 32.146 işlev sözde koda çevrildi; çözülemeyen beş işlev assembly olarak saklandı.
- Native sözde kod ağ, Python API, oynanış/karakter, grafik/kaynak ve Android platform alanlarına ayrıldı.
- Python katmanında 311 dosya, 1.979 bağımlılık kenarı, 48 native/harici modül, kullanılan 1.062 native çağrı ve 834 sabit kataloglandı.
- `item_proto` ve `mob_proto` içindeki ikinci XTEA+LZO katmanı açıldı.
  - 6.037 eşyanın 156 baytlık kayıtları tam CSV’ye çevrildi.
  - 1.347 yaratık/NPC’nin 255 baytlık kayıtları tam CSV’ye çevrildi.
- Ağ tarafında 375 gönderme/alma işlevi aday olarak çıkarıldı; 42 çekirdek paket başlık, yön ve boyut düzeyinde doğrulandı.
- Handshake, faz geçişi, login, karakter seçimi/oluşturma ve bazı oyun paketleri için yeniden oluşturulmuş C başlığı bulunuyor.
- Yalnızca localhost üzerinde çalışan gözlemci/minimal login eğitim sunucusu ve beş protokol testi eklendi.

## Mevcut bilginin yüzdesi

Aşağıdaki oranlar iki farklı şeyi ayırır: dosyaya sahip olma oranı ve davranışı doğru anlama/yeniden uygulama oranı. Bunlar mühendislik tahminidir; özgün kaynak deposuyla karşılaştırma yapılmadığı için matematiksel doğruluk iddiası taşımaz.

- Kamuya açık güncelleme manifestindeki dosyalar: **%100** — 4.900/4.900 doğrulandı.
- EterPack paketlerinin açılması: **%100** — 96/96 paket, sıfır çıkarma hatası.
- Dağıtılan Python ve Java istemci kodu: **yaklaşık %100** — paketlerde bulunan kaynakların tamamı alındı.
- Native işlev kapsaması: **%99,98 sayısal kapsama** — 32.146/32.151 sözde kod; fakat derlenebilir ve anlamlandırılmış özgün C++ eşdeğerliği tahmini **%70–80**.
- İstemci oyun verileri ve görsel/ses içerik: **%95–98** — istemcinin ihtiyaç duyduğu büyük bölüm mevcut; sunucuya özel spawn/drop/quest kayıtları eksik.
- Eşya ve mob tabloları: **%100 kayıt kapsaması** — istemcideki tüm kayıtlar çıkarıldı.
- Python-native API yüzeyi: **%80–90** — kullanılan çağrılar ve sabitler biliniyor; bazı native yan etkiler henüz modellenmedi.
- Ağ protokolü: **%40–55** — çekirdek fazlar ve birçok sabit paket biliniyor; tam GamePhase, sequence ve cipher ayrıntıları tamamlanmalı.
- Özgün sunucu kaynak kodu: **%0 doğrudan kaynak** — APK’de bulunmuyor. İstemciden çıkarılabilen sunucu davranış sözleşmesi tahmini **%20–30**.
- İşlevsel temiz-oda istemciyi yeniden üretme yeterliliği: **%80–90**.
- İstemci + kalıcı MMO sunucusu dahil özgün oyunun tamamını birebir yeniden üretme yeterliliği: **yaklaşık %55–65**.

Özgün sunucu Git deposu, veritabanı şeması ve görev/drop/spawn dosyaları sağlanırsa tam oyun kapsamının **%90+** seviyesine çıkması beklenir.

## Oyunu nasıl yeniden yaparız?

### 1. Veriyi sabitleme

Önce `item_proto.csv`, `mob_proto.csv`, harita atlası, yerelleştirme, eşya listesi ve beceri tabloları tek bir sürümlü veri şemasına alınmalı. VNUM ilişkileri için doğrulayıcı testler yazılmalı.

### 2. Varlık dönüştürme hattı

- DDS/TGA/PNG dokuları seçilen motorun biçimine dönüştür.
- GR2 modeller için lisans ve biçim uyumlu bir içe aktarıcı kullan veya modelleri açık bir ara biçime dönüştür.
- MSA/MSM/MSS hareket ve karakter tanımlarını yeni animasyon sistemine aktar.
- RAW/ATR/WTR harita katmanlarından arazi, çarpışma, su ve minimap üret.

### 3. İstemci mimarisi

İki uygulanabilir yol var:

- Mevcut davranışa en yakın yol: C++/BGFX tabanlı yeni istemci ve Python 2 betikleri için uyumluluk katmanı.
- Daha sürdürülebilir yol: Godot, Unreal veya Unity üzerinde yeni istemci; Python UI/oyun davranışını aşamalı olarak modern dile taşıma.

Her iki yolda da `python/native-api-calls.csv`, `app`, `net`, `player`, `chrmgr`, `wndMgr`, `item`, `chat`, `background` gibi modüller için uygulanacak API sözleşmesidir.

### 4. İlk oynanabilir dikey dilim

İlk hedef tam MMO olmamalı. Şu sırayla ilerlemek daha güvenilir:

1. Bir haritayı yükle ve kamera/karakter hareketini çalıştır.
2. Bir karakter modeli, temel animasyonlar ve çarpışmayı bağla.
3. Eşya envanteri ile `item_proto.csv` verisini göster.
4. Bir mobu `mob_proto.csv` değerleriyle üret ve yerel savaş döngüsünü çalıştır.
5. Python UI ekranlarını veya yeni eşdeğerlerini ekle.
6. Bundan sonra ağlı login/select/game akışına geç.

### 5. Sunucu

Temiz-oda sunucu en az şu servisleri ayırmalı:

- Auth/account servisi.
- Karakter seçimi ve kalıcı kayıt servisi.
- Kanal/world servisi.
- Harita, spawn ve AI döngüsü.
- Envanter, ekonomi, ticaret ve dükkân otoritesi.
- Görev/event state machine’i.
- Lonca, parti, mesajlaşma ve offline-shop servisleri.

İstemciden gelen hiçbir admin komutu veya eşya/para kararı güvenilir kabul edilmemeli. Yetki ve doğrulama her zaman sunucuda yapılmalı.

### 6. Ağ uyumluluğu

Önce `FF` handshake, `FD` faz, login ve karakter seçim paketleri tamamlanmalı. Ardından `FB/FA` anahtar anlaşması, cipher aktivasyonu ve `SendSequence` durumu yeniden uygulanmalı. Son aşamada `GamePhase` içindeki değişken uzunluklu paketler kataloglanmalı.

### 7. Güvenlik düzeltmeleri

- Güncelleme kanalı HTTPS ve imzalı manifest kullanmalı.
- Paket hash’i ile manifest aynı güvensiz kanaldan alınmamalı.
- Python betikleri imzalanmalı veya güvenilir paket içinde doğrulanmalı.
- Admin/maintenance komutları sunucu tarafında rol kontrolüne tabi olmalı.
- Dağıtım istemcisinden fishing-bot/multihack kodu çıkarılmalı.
- Varlık şifreleme anahtarlarının istemcide bulunmasının gizlilik sağlamadığı kabul edilmeli.

## Depo içeriği

- `outputs/Metin2Mobil-demo-v0.75.0-analysis/`: APK analizi.
- `outputs/Metin2Mobil-kodlar-v1791518086/`: Gerçek Python/Java kodları ve seçilmiş native çıktı.
- `outputs/Metin2Mobil-native-pseudocode-v0.75.0/`: Tam native sözde kod ve assembly fallback.
- `outputs/Metin2Mobil-reconstruction-kit-v1791518086/`: Yeniden yapım verileri, protokol ve eğitim sunucusu.
- `outputs/repository-bundles/`: Tam 3,9 GB indirilmiş/açılmış varlık dizininin bölünmüş TAR arşivi.
- `outputs/METIN2MOBIL-SONUC.md`: Kısa sonuç ve hash özeti.

## Tam varlık paketini geri açma

`outputs/repository-bundles` altındaki bütün `Metin2Mobil-full-v1791518086.tar.part-*` dosyalarını ikili sırayla birleştirip TAR’ı açın.

Git Bash/Linux/macOS:

```bash
cat outputs/repository-bundles/Metin2Mobil-full-v1791518086.tar.part-* > Metin2Mobil-full-v1791518086.tar
tar -xf Metin2Mobil-full-v1791518086.tar
```

Windows PowerShell içinde `cmd` kullanarak:

```powershell
cmd /c copy /b "outputs\repository-bundles\Metin2Mobil-full-v1791518086.tar.part-*" "Metin2Mobil-full-v1791518086.tar"
tar -xf .\Metin2Mobil-full-v1791518086.tar
```

Parça hash’leri `outputs/repository-bundles/SHA256SUMS.txt` içinde bulunur.
Birleştirilmiş TAR dosyasının SHA-256 değeri `7F38C47DECACF6548F79EA4ACC9D3684412816371749E7BA6D153FC6E8E7E9F0` olmalıdır.

## Bilinen kesin sınır

APK’den özgün sunucu deposu, geliştirici yorumları, özgün build sistemi veya istemcide hiç bulunmayan servis kodu geri alınamaz. Bunların birebir sürümü için proje sahibinin sunucu Git deposu, yedeği veya yetkili SSH erişimi gereklidir. Bu depo buna karşılık, temiz-oda yeniden uygulama için istemciden elde edilebilecek en kapsamlı teknik tabanı sunar.
