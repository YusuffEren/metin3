# -*- coding: utf-8 -*-
# MOBIL - mobile_root/uigrafik.py: GRAF\xddK AYARLARI paneli (Ayarlar penceresi: "Sistem Se\xe7enekleri" ile "Oyun Se\xe7enekleri"
# aras\xfdndaki "Grafik Ayarlar\xfd" d\xfc\xf0mesi -> uisystem.py).
# \xdcRET\xddL\xddR: tools/grafik/uigrafik_kaynak.py (UTF-8) -> tools/grafik/gen_uigrafik.py -> bu dosya (cp1254 ka\xe7\xfd\xfel\xfd ASCII).
# Sahte motor testi + \xe7izim: tools/grafik/test_sahte.py (eski APK / yeni APK, kal\xfdc\xfdl\xfdk, d\xf6\xfeeme denetimi).
#
# KULLANICI (2026-10-07): prototip Desktop/Averos2-Grafik-Prototip/index.html ONAYLANDI -> birebir oyun penceresi.
#  - \xdcst \xfeerit: cihaz s\xfdn\xfdf\xfd + RAM, anl\xfdk FPS (app.GetPerfStats / GetRenderFPS / kendi saya\xe7), Ak\xfdc\xfdl\xfdk + Is\xfdnma/Pil
#    \xf6l\xe7erleri (prototipin yuk() form\xfcl\xfc aynen).
#  - 5 kademe (Otomatik/D\xfc\xfe\xfck/Orta/Y\xfcksek/Ultra; elle de\xf0i\xfeince "ozel" -> hi\xe7bir kademe se\xe7ili g\xf6r\xfcnmez, prototip gibi).
#  - 10 ayar: FPS, \xc7\xf6z\xfcn\xfcrl\xfck, Doku, G\xf6lgeler, Efektler, G\xf6r\xfc\xfe Mesafesi, Ayr\xfdnt\xfdl\xfd Oyuncu, Di\xf0erlerinin Efektleri,
#    \xddsim Etiketleri, Pil Koruma. Varsay\xfdlan (paneli Otomatik'e d\xf6nd\xfcr\xfcr) / Uygula (uygular + kaydeder).
#
# MOTOR S\xd6ZLE\xdeMES\xdd (v76 I paketi, YEN\xdd APK): app.SetFPSLimit / SetRenderScale / SetTextureQuality / SetEffectLevel /
#   SetDetailedCharacterLimit / SetOthersEffectsVisible / SetBatterySaver / GetGraphicsDefaults / GetDeviceRamMB /
#   GetPerfStats. HER \xe7a\xf0r\xfd getattr ile: eski APK'da yoksa sessizce atlan\xfdr (panel yine a\xe7\xfdl\xfdr, yaln\xfdz mevcut olanlar etkili).
# OYUNUN MEVCUT AYARLARI (eski APK'da da var): g\xf6lge = systemSetting.SetShadowLevel (Kapal\xfd: 1 + background.SHADOW_NONE,
#   her harita y\xfckleni\xfeinde game.py Open -> OyunAcildi yeniden uygular; motor Warp'ta sistem seviyesine d\xf6nd\xfcr\xfcr),
#   g\xf6r\xfc\xfe mesafesi = constInfo.SET_FOG_LEVEL_INDEX (Sistem Se\xe7enekleri'ndeki "Sis" sat\xfdr\xfdyla AYNI de\xf0er),
#   isim etiketleri = systemSetting.SetAlwaysShowNameFlag (Oyun Se\xe7enekleri'ndeki sat\xfdrla AYNI de\xf0er).
#   \xddki yerden de\xf0i\xfeen ayar TUTARLI: di\xf0er pencereden de\xf0i\xfeince buraya "ozel" olarak yaz\xfdl\xfdr (_IzleKur), o pencereler
#   her a\xe7\xfdl\xfd\xfeta g\xfcncel de\xf0eri g\xf6sterir (_DiyalogSenkron).
# \xddS\xddM ET\xddKETLER\xdd (koordinat\xf6r 2026-10-07, telefonda bulunan hata: "Yak\xfdndakiler" isimleri H\xdd\xc7 g\xf6stermiyordu - mobilde
#   fare/hover yok): H\xdd\xc7B\xddR kademe "isimleri her zaman g\xf6ster"i KAPATMAZ. Yak\xfdndakiler = A\xc7IK + app.SetNameTagRange(1500)
#   (~15 m; kendi karakter + hedef hep g\xf6r\xfcn\xfcr), Her zaman = A\xc7IK + SetNameTagRange(0) (ger\xe7ek 3500). Eski APK'da
#   (SetNameTagRange yok) Yak\xfdndakiler de A\xc7IK (tam mesafe). Bayrak yaln\xfdz panelde Uygula'da (ve yeni kurulumun ilk
#   a\xe7\xfdl\xfd\xfe\xfdnda) A\xc7ILIR; a\xe7\xfdl\xfd\xfeta kay\xfdttan uygulan\xfdrken yaln\xfdz mesafe verilir -> Oyun Se\xe7enekleri'nden "kapal\xfd" se\xe7en
#   oyuncunun tercihi EZ\xddLMEZ (panel o durumda yaln\xfdz G\xd6STER\xddM olarak "Yak\xfdndakiler" g\xf6sterir; kay\xfdt de\xf0i\xfemez). Kay\xfdt
#   yoksa (mevcut oyuncu) mesafe de verilmez (motor varsay\xfdlan\xfd birebir). Oyun Se\xe7enekleri'nden "a\xe7\xfdk" yap\xfdl\xfdnca kay\xfdttaki
#   se\xe7im motorun o anki mesafesinden okunur. Bu hatayla kapanm\xfd\xfe kay\xfdtlar (surum<2, isim=yakinda) bir kez onar\xfdl\xfdr
#   (A\xc7IK + surum=2).
# OTOMAT\xddK YEN\xddDEN BA\xdeLATMA (v76 J): Uygula'da doku kalitesi a\xe7\xfdl\xfd\xfeta y\xfcklenenden farkl\xfdysa ve app.RestartApp varsa
#   (Android + PC yeni APK; iOS'ta YOK - Apple izin vermez) kay\xfdt diske yaz\xfdld\xfdktan SONRA "Oyun yeniden ba\xfelat\xfdl\xfdyor..."
#   g\xf6sterilir, 1.5 sn sonra app.RestartApp() (oyunun normal \xe7\xfdk\xfd\xfe yolu + yeni s\xfcre\xe7). D\xfcelloda (\xe7\xfdk\xfd\xfe yasak) ya da
#   kay\xfdt yaz\xfdlamazsa eski not ("oyunu yeniden ba\xfelat") kal\xfdr. Zamanlay\xfdc\xfd panelden ba\xf0\xfdms\xfdz (panel kapansa da \xe7al\xfd\xfe\xfdr).
# KALICILIK: pack/grafik.cfg ("anahtar=de\xf0er" sat\xfdrlar\xfd; \xf6nce .tmp yaz\xfdl\xfdr, sonra yeniden adland\xfdr\xfdl\xfdr). YALNIZ panelde
#   Uygula'ya bas\xfdnca yaz\xfdl\xfdr (a\xe7\xfdl\xfd\xfeta asla); ba\xfeka pencere isim/sis de\xf0i\xfetirirse kay\xfdt VARSA g\xfcncellenir.
# UYGULAMA ZAMANI: ui.py sonunda Erken() -> app.Create sar\xfdl\xfdr; Create d\xf6ner d\xf6nmez (dokular y\xfcklenmeden: imle\xe7, logo,
#   giri\xfe ekran\xfd ondan sonra) uygulan\xfdr. Kanca ka\xe7arsa ilk oyun a\xe7\xfdl\xfd\xfe\xfdnda (OyunAcildi) uygulan\xfdr.
# MEVCUT OYUNCU KORUMASI (koordinat\xf6r 2026-10-07: "ilk a\xe7\xfdl\xfd\xfeta mevcut oyuncular\xfdn ayarlar\xfd de\xf0i\xfemesin"):
#   - ESK\xdd APK (app.GRAFIK_V76 yok): grafik.cfg yoksa a\xe7\xfdl\xfd\xfeta H\xdd\xc7B\xddR \xdeEY uygulanmaz; yaln\xfdz panelde Uygula. (Kay\xfdt varsa
#     = oyuncu daha \xf6nce kendisi Uygula'ya basm\xfd\xfe -> onun se\xe7imi geri y\xfcklenir.)
#   - YEN\xdd APK, kay\xfdt yok, MEVCUT kurulum (hesap / dil / bayrak dosyas\xfd var; metin2.cfg ilk indirmede de geldi\xf0i i\xe7in \xf6l\xe7\xfct
#     de\xf0il): g\xf6lge / isim / g\xf6r\xfc\xfe mesafesi oyunun \xdeU ANK\xdd de\xf0erinden; yaln\xfdz motorun yeni ayarlar\xfd (FPS, \xe7\xf6z\xfcn\xfcrl\xfck, doku,
#     efekt, ayr\xfdnt\xfdl\xfd oyuncu, di\xf0erlerinin efektleri, pil) Otomatik kademeden. Hepsi Otomatik'le ayn\xfdysa "oto", de\xf0ilse "ozel".
#     \xddST\xddSNA: RAM kademesi D\xdc\xde\xdcK cihazda g\xf6lge + g\xf6r\xfc\xfe mesafesi de Otomatik (d\xfc\xfe\xfck) kademeden (oyunun a\xe7\xfdlabilmesi \xf6nce).
#   - YEN\xdd APK, ger\xe7ekten YEN\xdd kurulum: tam Otomatik kademe.
# \xddK\xdd D\xddL: t\xfcm yaz\xfdlar YAZI[tr/en] (dil.Mevcut()).
import os
import math
import app
import ui
import wndMgr
import dil

DOSYA = "pack/grafik.cfg"
PT = "d:/ymir work/ui/pattern/"
PUB = "d:/ymir work/ui/public/"
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")
TASMA = 0.02

# ------------------------------------------------------------------ ayarlar (prototip AYAR / KADEME / OTO birebir)
ANAHTAR = ("fps", "coz", "doku", "golge", "efekt", "mesafe", "oyuncu", "digerEf", "isim", "pil")
AYAR = (
	("fps", "sec", ("30", "45", "60")),
	("coz", "kaydir", None),
	("doku", "sec", ("dusuk", "orta", "yuksek")),
	("golge", "sec", ("kapali", "ben", "herkes")),
	("efekt", "sec", ("az", "normal", "tam")),
	("mesafe", "sec", ("yakin", "orta", "uzak")),
	("oyuncu", "sec", ("20", "40", "70")),
	("digerEf", "anahtar", None),
	("isim", "sec", ("yakinda", "hep")),
	("pil", "anahtar", None),
)
SAYI = ("fps", "oyuncu")		# se\xe7enek yaz\xfds\xfd de\xf0erin kendisi
COZ_MIN, COZ_MAX, COZ_ADIM = 50, 100, 5
KADEME = {
	"dusuk": {"fps": "30", "coz": 60, "doku": "dusuk", "golge": "kapali", "efekt": "az", "mesafe": "yakin", "oyuncu": "20", "digerEf": False, "isim": "yakinda", "pil": True},
	"orta": {"fps": "30", "coz": 75, "doku": "orta", "golge": "ben", "efekt": "normal", "mesafe": "orta", "oyuncu": "40", "digerEf": True, "isim": "yakinda", "pil": True},
	"yuksek": {"fps": "60", "coz": 90, "doku": "yuksek", "golge": "ben", "efekt": "tam", "mesafe": "uzak", "oyuncu": "70", "digerEf": True, "isim": "hep", "pil": True},
	"ultra": {"fps": "60", "coz": 100, "doku": "yuksek", "golge": "herkes", "efekt": "tam", "mesafe": "uzak", "oyuncu": "70", "digerEf": True, "isim": "hep", "pil": False},
}
KADEMELER = ("oto", "dusuk", "orta", "yuksek", "ultra")
OTO = {"dusuk": "dusuk", "orta": "orta", "yuksek": "yuksek"}
GUC = {"dusuk": 2.6, "orta": 4.5, "yuksek": 9.0}		# telefon gucu katsayisi (11 GB Dimensity 7200 ayarlarda 61 FPS: eski 5.8 "Dusuk" gosteriyordu)
# motor e\xfelemeleri
DOKU = {"dusuk": 0, "orta": 1, "yuksek": 2}
EFEKT = {"az": 0, "normal": 1, "tam": 2}
GOLGE = {"kapali": 1, "ben": 2, "herkes": 3}		# systemSetting seviyesi (SHADOW_GROUND / _AND_SOLO / _ALL); 0'\xfd kabul etmez
MESAFE = {"yakin": 0, "orta": 1, "uzak": 2}		# constInfo FOG_LEVEL_LIST indeksi (4800 / 9600 / 12800)
ISIM_MESAFE = {"yakinda": 1500, "hep": 0}		# app.SetNameTagRange (oyun birimi; 0 = ger\xe7ek 3500)
SURUM = 2				# grafik.cfg bi\xe7imi: 2 = isim etiketi onar\xfdm\xfd yap\xfdld\xfd
YENIDEN_GECIKME = 1.5		# Uygula -> app.RestartApp (sn)

YAZI = {
	"tr": {"bas": "Grafik Ayarlar\xfd", "cihaz": "Telefonunuz", "anlik": "Anl\xfdk", "akicilik": "Ak\xfdc\xfdl\xfdk", "isinma": "Is\xfdnma / Pil",
		"sinif": {"dusuk": "D\xfc\xfe\xfck seviye", "orta": "Orta seviye", "yuksek": "Y\xfcksek seviye"}, "ram": "RAM",
		"kademe": {"oto": "Otomatik", "dusuk": "D\xfc\xfe\xfck", "orta": "Orta", "yuksek": "Y\xfcksek", "ultra": "Ultra", "ozel": "\xd6zel"},
		"kademeAlt": {"oto": "telefona g\xf6re", "dusuk": "en ak\xfdc\xfd", "orta": "dengeli", "yuksek": "g\xfczel", "ultra": "en g\xfczel"},
		"seviye": ("\xc7ok d\xfc\xfe\xfck", "D\xfc\xfe\xfck", "Orta", "Y\xfcksek", "\xc7ok y\xfcksek"),
		"not": "D\xfc\xfe\xfck ayarlar donmay\xfd, \xfds\xfdnmay\xfd ve pil t\xfcketimini azalt\xfdr. Otomatik, telefonunuza en uygun ayar\xfd se\xe7er.",
		"yeniden": "Doku kalitesinin tam etkisi i\xe7in oyunu yeniden ba\xfelat.",
		"baslatiliyor": "Oyun yeniden ba\xfelat\xfdl\xfdyor...",
		"vars": "Varsay\xfdlan", "uyg": "Uygula", "uygulandi": "Grafik ayarlar\xfd uyguland\xfd",
		"a": {"fps": ("FPS S\xfdn\xfdr\xfd", "30 = serin ve uzun pil"), "coz": ("\xc7\xf6z\xfcn\xfcrl\xfck", "d\xfc\xfe\xfck = \xe7ok daha h\xfdzl\xfd"),
			"doku": ("Doku Kalitesi", "bellek kullan\xfdm\xfd"), "golge": ("G\xf6lgeler", ""), "efekt": ("Efektler", "beceri ve par\xe7ac\xfdklar"),
			"mesafe": ("G\xf6r\xfc\xfe Mesafesi", ""), "oyuncu": ("Ayr\xfdnt\xfdl\xfd Oyuncu", "tam \xe7izilen ki\xfei say\xfds\xfd"),
			"digerEf": ("Di\xf0erlerinin Efektleri", "kalabal\xfdkta"), "isim": ("\xddsim Etiketleri", ""), "pil": ("Pil Koruma", "\xfds\xfdn\xfdnca otomatik d\xfc\xfe\xfcr")},
		"s": {"dusuk": "D\xfc\xfe\xfck", "orta": "Orta", "yuksek": "Y\xfcksek", "kapali": "Kapal\xfd", "ben": "Ben", "herkes": "Herkes", "az": "Az",
			"normal": "Normal", "tam": "Tam", "yakin": "Yak\xfdn", "uzak": "Uzak", "hep": "Her zaman", "yakinda": "Yak\xfdndakiler"}},
	"en": {"bas": "Graphics Settings", "cihaz": "Your phone", "anlik": "Live", "akicilik": "Smoothness", "isinma": "Heat / Battery",
		"sinif": {"dusuk": "Low-end", "orta": "Mid-range", "yuksek": "High-end"}, "ram": "RAM",
		"kademe": {"oto": "Auto", "dusuk": "Low", "orta": "Medium", "yuksek": "High", "ultra": "Ultra", "ozel": "Custom"},
		"kademeAlt": {"oto": "fits your phone", "dusuk": "smoothest", "orta": "balanced", "yuksek": "pretty", "ultra": "prettiest"},
		"seviye": ("Very low", "Low", "Medium", "High", "Very high"),
		"not": "Lower settings reduce stutter, heat and battery use. Auto picks the best settings for your phone.",
		"yeniden": "Restart the game for the full texture quality effect.",
		"baslatiliyor": "Restarting the game...",
		"vars": "Default", "uyg": "Apply", "uygulandi": "Graphics settings applied",
		"a": {"fps": ("FPS Limit", "30 = cooler, longer battery"), "coz": ("Resolution", "lower = much faster"),
			"doku": ("Texture Quality", "memory use"), "golge": ("Shadows", ""), "efekt": ("Effects", "skills and particles"),
			"mesafe": ("View Distance", ""), "oyuncu": ("Detailed Players", "fully drawn characters"),
			"digerEf": ("Others' Effects", "in crowds"), "isim": ("Name Tags", ""), "pil": ("Battery Saver", "lower when hot")},
		"s": {"dusuk": "Low", "orta": "Med", "yuksek": "High", "kapali": "Off", "ben": "Me", "herkes": "All", "az": "Few",
			"normal": "Normal", "tam": "Full", "yakin": "Near", "uzak": "Far", "hep": "Always", "yakinda": "Nearby"}},
}


def Y():
	try:
		return YAZI.get(dil.Mevcut(), YAZI["en"])
	except:
		return YAZI["en"]


# ------------------------------------------------------------------ durum
_D = {"kademe": "oto", "deger": None, "cihaz": None, "ram": 0, "ramKademe": None, "yuklendi": False, "uygulandi": False,
	"dokuAcilis": None, "kaynak": None, "sistemUygula": True, "isimAc": False, "isimMesafe": True, "onar": False}
# kaynak: "kayit" (grafik.cfg) | "yeni" (yeni kurulum, tam Otomatik) | "mevcut" (kay\xfdt yok, mevcut oyuncu: g\xf6lge/isim/sis \xfeu anki)
# sistemUygula: oyunun mevcut ayarlar\xfd (g\xf6lge/isim/sis) a\xe7\xfdl\xfd\xfeta + harita y\xfckleni\xfeinde uygulan\xfdr m\xfd
# isimAc: a\xe7\xfdl\xfd\xfeta "isimleri her zaman g\xf6ster" A\xc7ILIR m\xfd (yaln\xfdz yeni kurulum + hatal\xfd eski kay\xfdt onar\xfdm\xfd; kay\xfdttan
#   a\xe7\xfdl\xfd\xfeta oyuncunun Oyun Se\xe7enekleri tercihi ezilmez - yaln\xfdz mesafe verilir)
# isimMesafe: a\xe7\xfdl\xfd\xfeta motor isim mesafesi (SetNameTagRange) verilir mi - mevcut oyuncuda (kay\xfdt yok) HAYIR: motor
#   varsay\xfdlan\xfd (ger\xe7ek 3500) aynen kal\xfdr; panelde "kapal\xfd" -> "Yak\xfdndakiler" yaln\xfdz G\xd6STER\xddMD\xddR
# onar: eski (surum<2) kay\xfdt "Yak\xfdndakiler" hatas\xfdyla isimleri kapatm\xfd\xfe olabilir -> a\xe7\xfdl\xfd\xfeta bir kez A\xc7 + surum=2 yaz
_YB = {"zaman": 0.0, "saat": None, "hata": False}		# bekleyen otomatik yeniden ba\xfelatma (app.GetTime zaman\xfd; 0 = yok)
SISTEM = ("golge", "isim", "mesafe")
HESAP_DOSYALARI = ("pack/mobile_login.cfg", "pack/hesap1.cfg", "pack/hesap2.cfg", "pack/hesap3.cfg", "pack/hesap4.cfg",
	"pack/dil.cfg", "pack/bayrak_hesap.cfg", "interface.cfg")		# yaln\xfdz oyun i\xe7inde olu\xfeur (indirme paketinde YOK)
_SON = {}				# motor \xe7a\xf0r\xfds\xfd -> son verilen arg\xfcmanlar (ayn\xfd de\xf0er tekrar g\xf6nderilmez)
_ICERDE = [False]		# kendi systemSetting / constInfo \xe7a\xf0r\xfdlar\xfdm\xfdz (izleyici "d\xfd\xfear\xfddan" saymas\xfdn)
_PEN = [None]


def _Hata(ne):
	try:
		import dbg
		import traceback
		dbg.TraceError("uigrafik %s: %s" % (ne, traceback.format_exc()))
	except:
		pass


def Cihaz():
	"""cihaz s\xfdn\xfdf\xfd ("dusuk"/"orta"/"yuksek"): app.GetGraphicsDefaults()["kademe"]; yoksa RAM e\xfei\xf0i
	(<= 3300 MB d\xfc\xfe\xfck, <= 4600 orta, \xfcst\xfc y\xfcksek); o da yoksa orta. Bir kez hesaplan\xfdr."""
	if _D["cihaz"]:
		return _D["cihaz"]
	k = None
	ram = 0
	f = getattr(app, "GetGraphicsDefaults", None)
	if f:
		try:
			d = f()
			k = d.get("kademe")
			ram = int(d.get("ram_mb", 0) or 0)
			if d.get("ram_kademe") is not None:
				_D["ramKademe"] = int(d.get("ram_kademe"))		# 0 d\xfc\xfe\xfck, 1 orta, 2 y\xfcksek (yaln\xfdz RAM)
		except:
			k = None
			_Hata("GetGraphicsDefaults")
	if ram <= 0:
		g = getattr(app, "GetDeviceRamMB", None)
		if g:
			try:
				ram = int(g())
			except:
				ram = 0
	if k not in OTO:
		if ram > 0:
			k = "dusuk" if ram <= 3300 else ("orta" if ram <= 4600 else "yuksek")
		else:
			k = "orta"
	_D["cihaz"] = k
	_D["ram"] = max(0, ram)
	return k


def KademeDeger(k):
	return dict(KADEME[OTO[Cihaz()]] if k == "oto" else KADEME[k])


def V76():
	"""yeni APK motor API'leri var m\xfd"""
	return bool(getattr(app, "GRAFIK_V76", 0))


def DusukRam():
	"""RAM kademesi d\xfc\xfe\xfck m\xfc (GetGraphicsDefaults "ram_kademe"; yoksa <= 3300 MB; bilinmiyorsa hay\xfdr)"""
	Cihaz()
	if _D["ramKademe"] is not None:
		return _D["ramKademe"] <= 0
	return 0 < _D["ram"] <= 3300


def YeniKurulum():
	"""hi\xe7 oynanmam\xfd\xfe kurulum: hesap / dil / bayrak dosyas\xfd yok (metin2.cfg ilk indirmede de geldi\xf0i i\xe7in say\xfdlmaz)"""
	for p in HESAP_DOSYALARI:
		if os.path.exists(p):
			return False
	return True


def IsimAcik():
	"""oyunun "isimleri her zaman g\xf6ster" ayar\xfd (Oyun Se\xe7enekleri); okunamazsa True (g\xf6sterim ezilmesin)"""
	try:
		import systemSetting
		return bool(systemSetting.IsAlwaysShowName())
	except:
		return True


def IsimSecimi():
	"""oyunun \xfeu anki isim etiketi durumu -> panel se\xe7imi: "her zaman g\xf6ster" KAPALI ise "yakinda" (panel bunu g\xf6sterir,
	oyuncunun tercihi de\xf0i\xfemez); A\xc7IK ise motor mesafesi 0 (ger\xe7ek 3500; eski APK hep) "hep", daralt\xfdlm\xfd\xfesa "yakinda"."""
	if not IsimAcik():
		return "yakinda"
	g = getattr(app, "GetNameTagRange", None)
	if g:
		try:
			if int(g()) > 0:
				return "yakinda"
		except:
			pass
	return "hep"


def MevcutSistem():
	"""oyunun \xdeU ANK\xdd g\xf6lge / isim / g\xf6r\xfc\xfe mesafesi de\xf0eri (eski APK'da da var)"""
	d = {}
	try:
		import systemSetting
		lvl = int(systemSetting.GetShadowLevel())
		d["golge"] = "kapali" if lvl <= 1 else ("ben" if lvl == 2 else "herkes")
	except:
		pass
	d["isim"] = IsimSecimi()
	try:
		import constInfo
		i = constInfo.GET_FOG_LEVEL_INDEX()
		for (ad, j) in MESAFE.items():
			if i == j:
				d["mesafe"] = ad
	except:
		pass
	return d


def _Dogrula(k, v):
	"""dosyadan okunan de\xf0er -> ge\xe7erli de\xf0er ya da None"""
	try:
		if k == "coz":
			n = int(v)
			n = max(COZ_MIN, min(COZ_MAX, n))
			return COZ_MIN + int(round((n - COZ_MIN) / float(COZ_ADIM))) * COZ_ADIM
		if k in ("digerEf", "pil"):
			if v in ("1", "0"):
				return v == "1"
			return None
		for (a, tur, sec) in AYAR:
			if a == k:
				return v if v in sec else None
	except:
		pass
	return None


def _Oku():
	"""-> (kademe, de\xf0erler, s\xfcr\xfcm); dosya yoksa (None, {}, 0)"""
	kademe = None
	d = {}
	surum = 0
	try:
		f = open(DOSYA, "r")
		metin = f.read()
		f.close()
	except:
		return (None, d, 0)
	for satir in metin.replace("\r", "").split("\n"):
		satir = satir.strip()
		if not satir or satir.startswith("#") or "=" not in satir:
			continue
		(k, v) = satir.split("=", 1)
		(k, v) = (k.strip(), v.strip())
		if k == "kademe":
			if v in KADEMELER or v == "ozel":
				kademe = v
		elif k == "surum":
			try:
				surum = int(v)
			except:
				surum = 0
		elif k in ANAHTAR:
			x = _Dogrula(k, v)
			if x is not None:
				d[k] = x
	return (kademe, d, surum)


def Yukle():
	"""kay\xfdt (pack/grafik.cfg) -> _D. Kay\xfdt yoksa: yeni kurulum (yeni APK) tam Otomatik; mevcut oyuncu (ya da eski APK)
	g\xf6lge/isim/sis \xfeu anki de\xf0erinden, motorun yeni ayarlar\xfd Otomatik'ten (d\xfc\xfe\xfck RAM: g\xf6lge + sis de Otomatik'ten)."""
	if _D["yuklendi"]:
		return
	(k, d, surum) = _Oku()
	sistem = True
	isimAc = False
	onar = False
	if k in KADEMELER:
		deger = KademeDeger(k)
		kaynak = "kayit"
	elif k == "ozel":
		deger = KademeDeger("oto")
		deger.update(d)
		kaynak = "kayit"
	elif V76() and YeniKurulum():
		k = "oto"
		deger = KademeDeger("oto")
		kaynak = "yeni"
		isimAc = True		# yeni kurulum: oyuncu tercihi hen\xfcz yok -> isimler A\xc7IK (Yak\xfdndakiler = 15 m)
	else:
		oto = KademeDeger("oto")
		deger = dict(oto)
		m = MevcutSistem()
		dusuk = V76() and DusukRam()
		for a in SISTEM:
			if dusuk and a in ("golge", "mesafe"):
				continue		# d\xfc\xfe\xfck RAM: Otomatik (d\xfc\xfe\xfck) kademeden -> a\xe7\xfdl\xfd\xfeta uygulan\xfdr
			if m.get(a):
				deger[a] = m[a]
		k = "oto" if deger == oto else "ozel"
		kaynak = "mevcut"
		sistem = dusuk		# isim zaten \xfeu anki de\xf0er (de\xf0i\xfemez); g\xf6lge/sis yaln\xfdz d\xfc\xfe\xfck RAM'de de\xf0i\xfeir
	if kaynak == "kayit" and surum < SURUM:
		## surum 1 kayd\xfd: eski panel "Yak\xfdndakiler"de "her zaman g\xf6ster"i KAPATIYORDU (mobilde isimler hi\xe7 g\xf6r\xfcnmez) ->
		## bir kez A\xc7; kay\xfdt surum=2 ile yeniden yaz\xfdl\xfdr (sonraki a\xe7\xfdl\xfd\xfelarda oyuncunun tercihi aynen kal\xfdr)
		onar = True
		isimAc = (deger.get("isim") == "yakinda")
	_D["kademe"] = k
	_D["deger"] = deger
	_D["kaynak"] = kaynak
	_D["sistemUygula"] = sistem
	_D["isimAc"] = isimAc
	_D["isimMesafe"] = (kaynak != "mevcut")
	_D["onar"] = onar
	_D["yuklendi"] = True


def _Kaydet():
	v = _D["deger"]
	if not v:
		return False
	satirlar = ["# Averos2 grafik ayarlari (uigrafik.py) - oyun icinden degistirilir", "surum=%d" % SURUM, "kademe=%s" % _D["kademe"]]
	for k in ANAHTAR:
		x = v[k]
		if k in ("digerEf", "pil"):
			x = "1" if x else "0"
		satirlar.append("%s=%s" % (k, x))
	try:
		veri = ("\n".join(satirlar) + "\n").encode("ascii")		# \xd6NCE kodla: hata olursa dosya hi\xe7 a\xe7\xfdlmaz
	except:
		_Hata("kaydet kodlama")
		return False
	gecici = DOSYA + ".tmp"
	try:
		f = open(gecici, "wb")
		f.write(veri)
		f.flush()
		try:
			os.fsync(f.fileno())
		except:
			pass
		f.close()
		try:
			os.rename(gecici, DOSYA)		# Android/POSIX: atomik de\xf0i\xfetirme
		except OSError:
			try:
				os.remove(DOSYA)		# Windows: hedef varsa rename olmaz
			except OSError:
				pass
			os.rename(gecici, DOSYA)
		return True
	except:
		_Hata("kaydet")
		return False


# ------------------------------------------------------------------ uygulama
def _Cagir(ad, arg, zorla):
	"""yeni APK motor \xe7a\xf0r\xfds\xfd: yoksa sessizce atla; ayn\xfd de\xf0er tekrar g\xf6nderilmez (zorla hari\xe7)"""
	f = getattr(app, ad, None)
	if not f:
		return False
	if not zorla and _SON.get(ad) == arg:
		return True
	try:
		f(*arg)
		_SON[ad] = arg
		return True
	except:
		_Hata(ad)
		return False


def _GolgeArkaPlan(v):
	"""G\xf6lgeler Kapal\xfd: systemSetting 0'\xfd kabul etmez (ger\xe7ek istemci) -> seviye 1 + arka plan\xfd SHADOW_NONE yap.
	Harita y\xfckl\xfc de\xf0ilse motor yok sayar; her harita y\xfckleni\xfeinde OyunAcildi yeniden \xe7a\xf0\xfdr\xfdr."""
	if v.get("golge") != "kapali":
		return
	try:
		import background
		background.SetShadowLevel(getattr(background, "SHADOW_NONE", 0))
	except:
		pass


def _Sistem(v, isimAc):
	"""oyunun mevcut ayarlar\xfd (eski APK'da da var): isim etiketi, g\xf6lge seviyesi, g\xf6r\xfc\xfe mesafesi (sis).
	\xddsim: "her zaman g\xf6ster" ASLA kapat\xfdlmaz; isimAc ise (panelde Uygula / yeni kurulum / hatal\xfd kay\xfdt onar\xfdm\xfd) A\xc7ILIR.
	Yak\xfdndakiler / Her zaman fark\xfd yaln\xfdz motor mesafesidir (SetNameTagRange, _Uygula)."""
	_ICERDE[0] = True
	try:
		import systemSetting
		if isimAc:
			try:
				if not systemSetting.IsAlwaysShowName():
					systemSetting.SetAlwaysShowNameFlag(True)
			except:
				_Hata("isim")
		try:
			lvl = GOLGE[v["golge"]]
			if int(systemSetting.GetShadowLevel()) != lvl:
				systemSetting.SetShadowLevel(lvl)
		except:
			_Hata("golge")
		_GolgeArkaPlan(v)
		try:
			import constInfo
			i = MESAFE[v["mesafe"]]
			try:
				simdi = constInfo.GET_FOG_LEVEL_INDEX()
			except:
				simdi = -1
			if simdi != i:
				constInfo.SET_FOG_LEVEL_INDEX(i)
		except:
			_Hata("mesafe")
	finally:
		_ICERDE[0] = False


def _Uygula(zorla, sistem=True, isimAc=True, isimMesafe=True):
	v = _D["deger"]
	_Cagir("SetTextureQuality", (DOKU[v["doku"]],), zorla)		# ilk: dokular y\xfcklenmeden
	_Cagir("SetFPSLimit", (int(v["fps"]),), zorla)
	_Cagir("SetRenderScale", (v["coz"] / 100.0,), zorla)
	_Cagir("SetEffectLevel", (EFEKT[v["efekt"]],), zorla)
	_Cagir("SetDetailedCharacterLimit", (int(v["oyuncu"]),), zorla)
	_Cagir("SetOthersEffectsVisible", (bool(v["digerEf"]),), zorla)
	_Cagir("SetBatterySaver", (bool(v["pil"]),), zorla)
	if isimMesafe:
		_Cagir("SetNameTagRange", (ISIM_MESAFE[v["isim"]],), zorla)		# yeni APK: Yak\xfdndakiler 15 m; eski APK: tam mesafe
	if sistem:
		_Sistem(v, isimAc)


def AcilistaUygula(yedek=False):
	"""kay\xfdtl\xfd ayarlar\xfd uygula (app.Create sonras\xfd; kanca ka\xe7t\xfdysa ilk oyun a\xe7\xfdl\xfd\xfe\xfdnda yedek=True)"""
	try:
		if not V76() and not os.path.exists(DOSYA):
			return		# eski APK + oyuncu hi\xe7 Uygula'ya basmam\xfd\xfe: H\xdd\xc7B\xddR \xdeEY de\xf0i\xfemez
		Yukle()
		if yedek:
			## kanca \xe7al\xfd\xfemad\xfd: dokular motorun kendi kalitesiyle y\xfcklendi -> yeniden ba\xfelatma notu ona g\xf6re
			g = getattr(app, "GetTextureQuality", None)
			q = None
			if g:
				try:
					q = {0: "dusuk", 1: "orta", 2: "yuksek"}.get(int(g()))
				except:
					q = None
			_D["dokuAcilis"] = q or _D["deger"]["doku"]
		else:
			_D["dokuAcilis"] = _D["deger"]["doku"]
		_Uygula(True, _D["sistemUygula"], _D["isimAc"], _D["isimMesafe"])
		_D["uygulandi"] = True
		if _D["onar"]:
			_D["onar"] = False
			_Kaydet()		# surum=2: onar\xfdm bir kez (kay\xfdt zaten vard\xfd - oyuncu Uygula'ya basm\xfd\xfet\xfd)
	except:
		_Hata("AcilistaUygula")


def Uygula(kademe, deger):
	"""panelin Uygula d\xfc\xf0mesi: de\xf0erleri uygula + kaydet (isimler A\xc7ILIR: oyuncu panelden a\xe7\xfdk\xe7a se\xe7ti).
	D\xf6n\xfc\xfe: kay\xfdt diske yaz\xfdld\xfd m\xfd (otomatik yeniden ba\xfelatma yaln\xfdz o zaman)."""
	Yukle()
	_D["kademe"] = kademe
	_D["deger"] = dict(deger)
	_D["kaynak"] = "kayit"
	_D["sistemUygula"] = True
	_D["isimMesafe"] = True
	_D["onar"] = False
	_Uygula(False, True, True, True)
	_D["uygulandi"] = True
	return _Kaydet()


def DokuBekliyor(doku):
	"""se\xe7ilen doku kalitesi a\xe7\xfdl\xfd\xfeta y\xfcklenenden farkl\xfd m\xfd (yaln\xfdz yeni APK: SetTextureQuality varsa)"""
	if not getattr(app, "SetTextureQuality", None):
		return False
	a = _D["dokuAcilis"]
	return bool(a) and a != doku


# ------------------------------------------------------------------ otomatik yeniden ba\xfelatma (v76 J)
def YenidenBaslatabilir():
	"""app.RestartApp var m\xfd (Android + PC yeni APK; iOS'ta YOK) ve oyuncu d\xfcelloda de\xf0il mi (oyunun \xc7\xfdk\xfd\xfe d\xfc\xf0mesi de
	d\xfcelloda kapatmaz - uisystem.Yes)"""
	if not getattr(app, "RestartApp", None):
		return False
	try:
		import player
		if player.IsPVPInstance():
			return False
	except:
		pass
	return True


def YenidenBekliyor():
	return _YB["zaman"] > 0


class _Saat(ui.Window):
	"""panelden ba\xf0\xfdms\xfdz g\xf6r\xfcnmez zamanlay\xfdc\xfd: panel kapansa da bekleyen yeniden ba\xfelatma zaman\xfdnda \xe7al\xfd\xfe\xfdr"""

	def __init__(self):
		ui.Window.__init__(self, "TOP_MOST")
		self.AddFlag("not_pick")
		self.SetSize(1, 1)
		self.SetPosition(0, 0)

	def __del__(self):
		ui.Window.__del__(self)

	def OnUpdate(self):
		_YenidenDenetle()


def YenidenBaslatPlanla():
	"""kay\xfdt diske yaz\xfdld\xfdktan SONRA: YENIDEN_GECIKME sn sonra app.RestartApp() (oyunun normal \xe7\xfdk\xfd\xfe yolu + yeni s\xfcre\xe7)"""
	_YB["zaman"] = app.GetTime() + YENIDEN_GECIKME
	_YB["hata"] = False
	if not _YB["saat"]:
		_YB["saat"] = _Saat()
	_YB["saat"].Show()


def _YenidenDenetle():
	z = _YB["zaman"]
	if not z or app.GetTime() < z:
		return
	_YB["zaman"] = 0.0
	try:
		_YB["saat"].Hide()
	except:
		pass
	try:
		app.RestartApp()
	except:
		_YB["hata"] = True		# panel eski nota d\xf6ner (oyuncu elle yeniden ba\xfelat\xfdr)
		_Hata("RestartApp")


# ------------------------------------------------------------------ iki yerden de\xf0i\xfeen ayarlar (tutarl\xfdl\xfdk)
def _Disaridan(k, v):
	"""Oyun Se\xe7enekleri (isim) / Sistem Se\xe7enekleri (sis) de\xf0i\xfetirdi -> kayda "ozel" olarak i\xfele"""
	if _ICERDE[0] or not _D["yuklendi"] or not _D["deger"]:
		return
	if _D["deger"].get(k) == v:
		return
	_D["deger"][k] = v
	_D["kademe"] = "ozel"
	if os.path.exists(DOSYA):		# kay\xfdt yaln\xfdz oyuncu Uygula'ya bast\xfdysa var; yoksa burada da yaz\xfdlmaz
		_Kaydet()


def _IzleKur():
	"""systemSetting.SetAlwaysShowNameFlag + constInfo.SET_FOG_LEVEL_INDEX sar\xfdl\xfdr (ui.py'nin SaveConfig sarmal\xfdn\xfdn
	\xfcst\xfcne): ba\xfeka pencere de\xf0i\xfetirirse grafik kayd\xfd g\xfcncellenir."""
	try:
		import systemSetting
		f = getattr(systemSetting, "SetAlwaysShowNameFlag", None)
		if f and not getattr(f, "_grafik", False):
			def SetAlwaysShowNameFlag(flag, *a):
				r = f(flag, *a)
				try:
					## "a\xe7\xfdk": kay\xfdttaki se\xe7im motorun \xdeU ANK\xdd mesafesinden (0 -> Her zaman, daralt\xfdlm\xfd\xfe -> Yak\xfdndakiler).
					## "kapal\xfd": kay\xfdt DE\xd0\xdd\xdeMEZ (mesafe se\xe7imi korunur); panel a\xe7\xfdl\xfdnca yaln\xfdz "Yak\xfdndakiler" G\xd6STER\xddR.
					if flag:
						_Disaridan("isim", IsimSecimi())
				except:
					pass
				return r
			SetAlwaysShowNameFlag._grafik = True
			systemSetting.SetAlwaysShowNameFlag = SetAlwaysShowNameFlag
	except:
		_Hata("izle isim")
	try:
		import constInfo
		g = getattr(constInfo, "SET_FOG_LEVEL_INDEX", None)
		if g and not getattr(g, "_grafik", False):
			def SET_FOG_LEVEL_INDEX(index, *a):
				r = g(index, *a)
				try:
					for (ad, i) in MESAFE.items():
						if i == index:
							_Disaridan("mesafe", ad)
				except:
					pass
				return r
			SET_FOG_LEVEL_INDEX._grafik = True
			constInfo.SET_FOG_LEVEL_INDEX = SET_FOG_LEVEL_INDEX
	except:
		_Hata("izle sis")


def Senkron():
	"""panel a\xe7\xfdl\xfdrken: oyunun canl\xfd isim / sis de\xf0eri kay\xfdttan farkl\xfdysa (\xf6r. ba\xfeka pencere) kayda al"""
	if not _D["yuklendi"]:
		return
	if IsimAcik():
		_Disaridan("isim", IsimSecimi())		# kapal\xfdyken kay\xfdt aynen; panel "Yak\xfdndakiler" G\xd6STER\xddR (GrafikPaneli)
	try:
		import constInfo
		i = constInfo.GET_FOG_LEVEL_INDEX()
		for (ad, j) in MESAFE.items():
			if i == j:
				_Disaridan("mesafe", ad)
	except:
		pass


def _DiyalogSenkron():
	"""Oyun Se\xe7enekleri / Sistem Se\xe7enekleri pencereleri d\xfc\xf0me durumunu yaln\xfdz kurulurken okur; her Show'da g\xfcncel
	de\xf0eri g\xf6stersinler (grafik panelinden de\xf0i\xfeince eski durum g\xf6r\xfcnmesin). S\xfdn\xfdf d\xfczeyinde bir kez."""
	try:
		import uiGameOption
		C = uiGameOption.OptionDialog
		if not getattr(C, "_grafikSenkron", False):
			eski = C.Show

			def Show(self, *a):
				try:
					self.RefreshAlwaysShowName()
				except:
					pass
				return eski(self, *a)
			C.Show = Show
			C._grafikSenkron = True
	except:
		_Hata("senkron oyun secenekleri")
	try:
		import uiSystemOption
		C = uiSystemOption.OptionDialog
		if not getattr(C, "_grafikSenkron", False):
			eski2 = C.Show

			def Show2(self, *a):
				try:
					import constInfo
					self._OptionDialog__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
				except:
					pass
				return eski2(self, *a)
			C.Show = Show2
			C._grafikSenkron = True
	except:
		_Hata("senkron sistem secenekleri")


# ------------------------------------------------------------------ kancalar
def Erken():
	"""ui.py sonunda (app.Create'den \xd6NCE): app.Create sar\xfdl\xfdr -> Create d\xf6ner d\xf6nmez ayarlar uygulan\xfdr
	(cihaz sorgusu ve motor \xe7a\xf0r\xfdlar\xfd cihaz kurulduktan sonra; dokular hen\xfcz y\xfcklenmemi\xfe). \xddzleyiciler kurulur."""
	try:
		asil = getattr(app, "Create", None)
		if asil and not getattr(asil, "_grafik", False):
			def Create(*a, **k):
				r = asil(*a, **k)
				AcilistaUygula()
				return r
			Create._grafik = True
			app.Create = Create
	except:
		_Hata("Erken")
	_IzleKur()


def OyunAcildi():
	"""game.py GameWindow.Open (her harita y\xfckleni\xfei): kanca ka\xe7t\xfdysa ayarlar\xfd uygula; G\xf6lgeler Kapal\xfd ise yeni haritada
	arka plan\xfd yeniden kapat; di\xf0er se\xe7enek pencereleri senkron."""
	try:
		if not _D["uygulandi"]:
			AcilistaUygula(True)
		elif _D["deger"] and _D["sistemUygula"]:
			_GolgeArkaPlan(_D["deger"])
		_DiyalogSenkron()
	except:
		_Hata("OyunAcildi")


# ------------------------------------------------------------------ pencere yerle\xfeimi (prototip .pen 800x590, mant\xfdksal px)
W, H = 800, 590
C_KREM = 0xfff1e6c0
C_ALTIN = 0xffe8d08a
C_ALT = 0xffc9b88f
C_SARI = 0xfff2c94c
C_KENAR = 0xff6b5a3e
C_CIZGI = 0xff3d342a
C_YESIL = 0xff8fd16a
C_TURUNCU = 0xfff0a24a
C_KIRMIZI = 0xffe0705a
C_SOLUK = 0xff8f8470
C_NOT = 0xffa99c80
C_BASLIK = 0xfffeedc6
# yaz\xfd boylar\xfd: telefonda pencere ~1.7x g\xf6r\xfcn\xfcr -> en az 14 px (prototipin 11-12 px'leri 14'e \xe7\xfdkt\xfd); <= 20 (font 32 px pi\xfeer)
F_BASLIK, F_AD, F_KUCUK, F_SEC, F_FPS, F_DUGME = 19, 15, 14, 14, 20, 15

INFO_X, INFO_Y, INFO_W, INFO_H = 22, 52, 756, 62
SUT1, SUT2, SUT3, SUT_SON = 37, 284, 492, 763		# grid 1.2fr 1fr 1.4fr (i\xe7 726, ara 14)
OLC_ETIKET, OLC_DEGER = 88, 72
KAD_Y, KAD_H, KAD_ARA = 124, 46, 8
LISTE_Y, SATIR_H, SATIR_ARA, SUTUN_W, SUTUN_ARA = 182, 48, 6, 371, 14
NOT_Y = 518
ALT_Y, ALT_W, ALT_H = 536, 150, 34
BILDIRIM_Y = 610


def _Otur(D, w, tex, s, rrs, z):
	t = w / float(s) - tex
	n = int(t + 0.01) if t >= 0 else -int(-t + 0.01)
	if tex + n < 1:
		n = 1 - tex
	if rrs:
		oran = 0.0 if n == 0 else (n + (0.5 if n > 0 else -0.5)) / float(tex)
		return ((D + TASMA) / float(tex + n), oran)
	e = int(round(D - tex * s * z))
	oran = 0.0 if e == 0 else (e + (0.5 if e > 0 else -0.5)) / float(tex)
	return ((D + TASMA - e) / float(tex), oran)


def _R(v):
	return int(round(v))


class _Kok(ui.Window):
	def __init__(self):
		ui.Window.__init__(self, "TOP_MOST")
		self.guncelle = None
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		return True		# panel modal: d\xfd\xfear\xfd dokunu\xfe oyuna ge\xe7mez

	def OnMouseLeftButtonUp(self):
		return True

	def OnUpdate(self):
		if self.guncelle:
			self.guncelle()


class _Hit(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.onUp = None
		self.onDown = None

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		if self.onDown:
			self.onDown()
		return True

	def OnMouseLeftButtonUp(self):
		if self.onUp:
			self.onUp()
		return True


class _Parca(object):
	"""ortak \xe7izim yard\xfdmc\xfdlar\xfd (uibayrak ile ayn\xfd d\xf6\xfeeme kural\xfd: _Otur)"""

	def _Win(self, parent, x, y, w, h):
		p = ui.Window()
		p.SetParent(parent)
		p.SetPosition(_R(x), _R(y))
		p.SetSize(max(1, _R(w)), max(1, _R(h)))
		p.Show()
		self.keep.append(p)
		return p

	def _Img(self, parent, path, x, y, sx=1.0, sy=1.0):
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(path)
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		w.SetScale(sx, sy)
		w.SetPosition(_R(x), _R(y))
		w.Show()
		self.keep.append(w)
		return w

	def _Tile(self, parent, path, x, y, w, h, tw, th, sx=1.0, sy=1.0):
		img = self._Img(parent, path, x, y, sx, sy)
		(zx, r) = _Otur(_R(x + w) - _R(x), w, tw, sx, HAS_RRS, 1.0)
		(zy, b) = _Otur(_R(y + h) - _R(y), h, th, sy, HAS_RRS, 1.0)
		img.SetScale(zx, zy)
		img.SetRenderingRect(0.0, 0.0, r, b)
		return img

	def _Rect(self, parent, x, y, w, h, color, fill=True):
		b = ui.Bar() if fill else ui.Box()
		b.SetParent(parent)
		b.AddFlag("not_pick")
		b.SetColor(color)
		b.SetPosition(_R(x), _R(y))
		b.SetSize(max(1, _R(x + w) - _R(x)), max(1, _R(y + h) - _R(y)))
		b.Show()
		self.keep.append(b)
		return b

	def _Daire(self, parent, cx, cy, d, color):
		"""OPAK dolu daire: \xfcst \xfcste binen 3-4 dikd\xf6rtgen (az pencere; kademeli daire)"""
		n = 3 if d <= 10 else 4
		out = []
		for i in xrange(n):
			a = (i + 0.5) / n * (math.pi / 2)
			w = d * math.cos(a)
			h = d * math.sin(a)
			out.append(self._Rect(parent, cx - w / 2.0, cy - h / 2.0, w, h, color))
		return out

	def _Hale(self, parent, cx, cy, d, color, adim=2):
		"""YARI SAYDAM daire (par\xfdlt\xfd): \xfcst \xfcste binmeyen yatay \xfeeritler -> saydaml\xfdk d\xfczg\xfcn"""
		r = d / 2.0
		out = []
		for i in xrange(0, int(d), adim):
			yy = i + adim / 2.0 - r
			yarim = (max(0.0, r * r - yy * yy)) ** 0.5
			if yarim < 0.6:
				continue
			out.append(self._Rect(parent, cx - yarim, cy - r + i, 2 * yarim, adim, color))
		return out

	def _Txt(self, parent, size, color, x, y, align="left", outline=True):
		t = ui.TextLine()
		t.SetParent(parent)
		t.AddFlag("not_pick")
		t.SetFontName("Tahoma:%d" % size)
		if outline:
			t.SetOutline()
		if align == "center":
			t.SetHorizontalAlignCenter()
		elif align == "right":
			t.SetHorizontalAlignRight()
		t.SetVerticalAlignCenter()
		t.SetPackedFontColor(color)
		t.SetPosition(_R(x), _R(y))
		t.Show()
		self.keep.append(t)
		return t

	def _Dokun(self, parent, x, y, w, h, up=None, down=None):
		hb = _Hit()
		hb.SetParent(parent)
		hb.SetPosition(_R(x), _R(y))
		hb.SetSize(max(1, _R(w)), max(1, _R(h)))
		hb.onUp = up
		hb.onDown = down
		hb.Show()
		self.keep.append(hb)
		return hb

	def _Dugme(self, parent, x, y, w, h, olay):
		b = ui.Button()
		b.SetParent(parent)
		b.SetUpVisual(PUB + "middle_button_01.sub")
		b.SetOverVisual(PUB + "middle_button_02.sub")
		b.SetDownVisual(PUB + "middle_button_03.sub")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, w / 61.0, h / 21.0)
		b.SetPosition(_R(x), _R(y))
		b.SetEvent(olay)
		b.Show()
		self.keep.append(b)
		return b

	def _Board(self, p, W, H):
		self._Tile(p, PT + "board_base.tga", 32, 32, W - 64, H - 64, 128, 128)
		self._Tile(p, PT + "board_line_top.tga", 32, 0, W - 64, 32, 128, 32)
		self._Tile(p, PT + "board_line_bottom.tga", 32, H - 32, W - 64, 32, 128, 32)
		self._Tile(p, PT + "board_line_left.tga", 0, 32, 32, H - 64, 32, 128)
		self._Tile(p, PT + "board_line_right.tga", W - 32, 32, 32, H - 64, 32, 128)
		for (n, cx, cy) in (("lefttop", 0, 0), ("righttop", W - 32, 0), ("leftbottom", 0, H - 32), ("rightbottom", W - 32, H - 32)):
			self._Tile(p, PT + "board_corner_%s.tga" % n, cx, cy, 32, 32, 32, 32)

	def _Baslik(self, p, W, yazi, kapat):
		"""prototip .tb (8,7, W-16 x 37: tb_sol 51 + tb_orta) + ortal\xfd ba\xfel\xfdk + kare \xe7arp\xfd (sa\xf0 14, \xfcst 10, 30x30)"""
		x, y, w = 8, 7, W - 16
		bh = 23 * 1.6
		bw = 32 * 1.6
		self._Tile(p, PT + "titlebar_left.tga", x, y, bw, bh, 32, 32, 1.6, 1.6)
		self._Tile(p, PT + "titlebar_center.tga", x + bw, y, w - bw, bh, 32, 32, 1.6, 1.6)
		t = self._Txt(p, F_BASLIK, C_BASLIK, W / 2.0, y + bh / 2.0, "center")
		t.SetText(yazi)
		c = 30
		cx, cy = W - 14 - c, 10
		cb = ui.Button()
		cb.SetParent(p)
		cb.SetUpVisual("mobile/ui/minimap/btn_close_sq.png")
		cb.SetOverVisual("mobile/ui/minimap/btn_close_sq.png")
		cb.SetDownVisual("mobile/ui/minimap/btn_close_sq_down.png")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(cb.hWnd, c / 64.0, c / 64.0)
		cb.SetPosition(cx, cy)
		cb.SetEvent(kapat)
		cb.Show()
		self.keep.append(cb)
		self._Dokun(p, cx - 12, 0, c + 24, 50, kapat)		# g\xf6r\xfcnmez geni\xfe dokunma alan\xfd
		return t


def _Genislik(t, metin):
	"""TextLine yaz\xfd geni\xfeli\xf0i (eski APK dar \xf6l\xe7er: harf ba\xfe\xfdna +1 px pay\xfd ile)"""
	try:
		w = t.GetTextSize()[0]
		if w > 0:
			return w + (0 if getattr(app, "GRAFIK_V76", 0) else len(metin) // 2)
	except:
		pass
	return len(metin) * 7


# ------------------------------------------------------------------ panel
class GrafikPaneli(_Parca):

	def __init__(self):
		self.keep = []
		Yukle()
		Senkron()
		self.kademe = _D["kademe"]
		self.deger = dict(_D["deger"])
		if not IsimAcik() and self.deger["isim"] != "yakinda":
			## Oyun Se\xe7enekleri'nde "her zaman g\xf6ster" kapal\xfd: panel "Yak\xfdndakiler" G\xd6STER\xddR (kay\xfdt/tercih de\xf0i\xfemez;
			## Uygula'ya bas\xfdl\xfdrsa isimler bu se\xe7imle A\xc7ILIR)
			self.deger["isim"] = "yakinda"
			self.kademe = "ozel"
			for k in KADEMELER:
				if KademeDeger(k) == self.deger:
					self.kademe = k
					break
		self.cihaz = Cihaz()
		self.surukle = False
		self.yenidenGosterildi = YenidenBekliyor()
		self.bildirimSon = 0.0
		self.fpsSon = 0.0
		self.sayac = [0, app.GetTime()]
		self.fpsSayac = 0
		self.sw = float(wndMgr.GetScreenWidth())
		self.sh = float(wndMgr.GetScreenHeight())
		self.__Kur()
		self.__Ciz()
		self.__Fps(True)

	# ---------------- kurulum
	def __Kur(self):
		y = Y()
		kok = _Kok()
		kok.SetSize(_R(self.sw), _R(self.sh))
		kok.SetPosition(0, 0)
		kok.Show()
		self.keep.append(kok)
		self.kok = kok
		self._Rect(kok, 0, 0, self.sw, self.sh, 0x80000000)		# prototip .perde rgba(0,0,0,.5)
		p = self._Win(kok, (self.sw - W) / 2.0, max(0.0, (self.sh - H) / 2.0), W, H)
		self.pen = p
		self._Board(p, W, H)
		self._Baslik(p, W, y["bas"], ui.__mem_func__(self.Kapat))
		self.__KurBilgi(y)
		self.__KurKademe(y)
		self.__KurListe(y)
		self.notT = self._Txt(p, F_KUCUK, C_NOT, W / 2.0, NOT_Y, "center")
		bx = W / 2.0 - 8 - ALT_W
		self._Dugme(p, bx, ALT_Y, ALT_W, ALT_H, ui.__mem_func__(self.__Varsayilan))
		self._Txt(p, F_DUGME, C_BASLIK, bx + ALT_W / 2.0, ALT_Y + ALT_H / 2.0, "center").SetText(y["vars"])
		bx = W / 2.0 + 8
		self._Dugme(p, bx, ALT_Y, ALT_W, ALT_H, ui.__mem_func__(self.__Uygula))
		self._Txt(p, F_DUGME, C_SARI, bx + ALT_W / 2.0, ALT_Y + ALT_H / 2.0, "center").SetText(y["uyg"])
		## bildirim (prototip .bildirim: pencerenin alt\xfdnda, 1.6 sn)
		bw = 300
		self.bilWin = self._Win(p, (W - bw) / 2.0, BILDIRIM_Y, bw, 34)
		self.bilWin.AddFlag("not_pick")
		self.bilZemin = self._Rect(self.bilWin, 0, 0, bw, 34, 0xbf000000)
		self.bilCizgi = self._Rect(self.bilWin, 0, 0, bw, 34, C_KENAR, False)
		self.bilT = self._Txt(self.bilWin, F_KUCUK, C_SARI, bw / 2.0, 17, "center")
		self.bilWin.Hide()
		kok.guncelle = ui.__mem_func__(self.__Guncelle)

	def __KurBilgi(self, y):
		p = self.pen
		self._Rect(p, INFO_X, INFO_Y, INFO_W, INFO_H, 0x8c000000)
		self._Rect(p, INFO_X, INFO_Y, INFO_W, INFO_H, C_CIZGI, False)
		## 1. s\xfctun: cihaz s\xfdn\xfdf\xfd + RAM
		self._Txt(p, F_KUCUK, C_SOLUK, SUT1, 70).SetText(y["cihaz"])
		renk = C_TURUNCU if self.cihaz == "dusuk" else C_YESIL
		parlak = (renk & 0x00ffffff) | 0x30000000
		self._Hale(p, SUT1 + 5, 92.5, 16, parlak)		# box-shadow 0 0 6px
		self._Daire(p, SUT1 + 5, 92.5, 10, renk)
		ram = _D["ram"]
		metin = y["sinif"][self.cihaz]
		if ram > 0:
			gb = max(1, int(math.ceil(ram / 1024.0 - 0.15)))		# telefonun g\xf6sterdi\xf0i 3.6 GB -> "4 GB"
			metin += " \xb7 %d GB %s" % (gb, y["ram"])
		self._Txt(p, F_AD, C_KREM, SUT1 + 16, 92).SetText(metin)
		## 2. s\xfctun: anl\xfdk FPS
		self._Txt(p, F_KUCUK, C_SOLUK, SUT2, 65).SetText(y["anlik"])
		self.fpsT = self._Txt(p, F_FPS, C_SARI, SUT2, 92)
		self.fpsEk = self._Txt(p, F_KUCUK, C_ALT, SUT2 + 30, 95)
		self.fpsEk.SetText("FPS")
		## 3. s\xfctun: \xf6l\xe7erler
		self.olcer = []
		for (i, ad) in enumerate(("akicilik", "isinma")):
			cy = 73 + i * 20
			self._Txt(p, F_KUCUK, C_ALT, SUT3, cy).SetText(y[ad])
			x0 = SUT3 + OLC_ETIKET + 8
			x1 = SUT_SON - OLC_DEGER - 8
			self._Rect(p, x0, cy - 4, x1 - x0, 8, 0xff1a1510)
			self._Rect(p, x0, cy - 4, x1 - x0, 8, C_CIZGI, False)
			dolu = self._Rect(p, x0 + 1, cy - 3, 1, 6, C_YESIL)
			t = self._Txt(p, F_KUCUK, C_ALT, SUT_SON, cy, "right")
			self.olcer.append((dolu, t, x0 + 1, x1 - x0 - 2))

	def __KurKademe(self, y):
		p = self.pen
		self.kd = {}
		kw = (INFO_W - 4 * KAD_ARA) / 5.0
		for (i, ad) in enumerate(KADEMELER):
			x = INFO_X + i * (kw + KAD_ARA)
			o = {"seritler": [], "x": x}
			n = 4
			for j in xrange(n):		# linear-gradient: 4 \xfeerit (renk fark\xfd k\xfc\xe7\xfck, kademe g\xf6r\xfcnmez)
				y0 = KAD_Y + 1 + (KAD_H - 2) * j / float(n)
				y1 = KAD_Y + 1 + (KAD_H - 2) * (j + 1) / float(n)
				o["seritler"].append(self._Rect(p, x + 1, y0, kw - 2, y1 - y0, 0xff000000))
			o["cizgi"] = self._Rect(p, x, KAD_Y, kw, KAD_H, C_KENAR, False)
			o["ad"] = self._Txt(p, F_AD, C_KREM, x + kw / 2.0, KAD_Y + 15, "center")
			o["ad"].SetText(y["kademe"][ad])
			o["alt"] = self._Txt(p, F_KUCUK, C_SOLUK, x + kw / 2.0, KAD_Y + 33, "center")
			o["alt"].SetText(y["kademeAlt"][ad])
			self.kd[ad] = o
		## se\xe7ili kademenin i\xe7 par\xfdlt\xfds\xfd (box-shadow inset 0 0 12px): TEK tak\xfdm, se\xe7ili d\xfc\xf0meye ta\xfe\xfdn\xfdr
		self.kdKw = kw
		self.kdParla = [self._Rect(p, 0, KAD_Y + k, kw - 2 * k, KAD_H - 2 * k, a, False)
			for (k, a) in ((1, 0x45f2c94c), (2, 0x2df2c94c), (3, 0x18f2c94c), (4, 0x0cf2c94c))]
		for ad in KADEMELER:
			x = self.kd[ad]["x"]
			self._Dokun(p, x, KAD_Y, kw, KAD_H, (lambda a=ad: self.__Kademe(a)))

	def __KurListe(self, y):
		p = self.pen
		self.satir = {}
		for (i, (k, tur, sec)) in enumerate(AYAR):
			rx = INFO_X + (i % 2) * (SUTUN_W + SUTUN_ARA)
			ry = LISTE_Y + (i // 2) * (SATIR_H + SATIR_ARA)
			self._Rect(p, rx, ry, SUTUN_W, SATIR_H, 0x73000000)
			self._Rect(p, rx, ry, SUTUN_W, SATIR_H, C_CIZGI, False)
			(ad, alt) = y["a"][k]
			if alt:
				self._Txt(p, F_AD, C_KREM, rx + 13, ry + 15).SetText(ad)
				self._Txt(p, F_KUCUK, C_SOLUK, rx + 13, ry + 33).SetText(alt)
			else:
				self._Txt(p, F_AD, C_KREM, rx + 13, ry + 24).SetText(ad)
			sag = rx + SUTUN_W - 11		# padding sa\xf0 10 + kenar 1
			o = {"tur": tur}
			if tur == "sec":
				self.__KurSec(o, k, sec, sag, ry, y)
			elif tur == "kaydir":
				self.__KurKaydir(o, k, sag, ry)
			else:
				self.__KurAnahtar(o, k, sag, ry)
			self.satir[k] = o

	def __KurSec(self, o, k, sec, sag, ry, y):
		p = self.pen
		yazilar = [(v if k in SAYI else y["s"][v]) for v in sec]
		olcum = []
		olcer = ui.TextLine()		# yaln\xfdz \xf6l\xe7\xfcm (g\xf6sterilmez)
		olcer.SetFontName("Tahoma:%d" % F_SEC)
		for metin in yazilar:
			olcer.SetText(metin)
			olcum.append((metin, max(46, _Genislik(olcer, metin) + 16)))
		gw = 2 + sum([w for (m, w) in olcum]) + len(olcum) - 1
		gx = sag - gw
		gy = ry + 9
		self._Rect(p, gx, gy, gw, 30, C_KENAR, False)
		o["sec"] = []
		x = gx + 1
		for (j, (metin, bw)) in enumerate(olcum):
			if j:
				self._Rect(p, x, gy + 1, 1, 28, C_CIZGI)
				x += 1
			zemin = self._Rect(p, x, gy + 1, bw, 28, 0xff120e09)
			t = self._Txt(p, F_SEC, C_ALT, x + bw / 2.0, gy + 15, "center", False)		# zeminden SONRA: \xfcstte
			t.SetText(metin)
			v = sec[j]
			self._Dokun(p, x - (1 if j else 0), ry + 1, bw + (1 if j else 0), SATIR_H - 2, (lambda a=k, b=v: self.__Sec(a, b)))
			o["sec"].append((v, zemin, t))
			x += bw

	def __KurKaydir(self, o, k, sag, ry):
		p = self.pen
		x0 = sag - 40 - 8 - 120
		cy = ry + 24
		self._Rect(p, x0, cy - 4, 120, 8, 0xff3b3b3b)
		self._Rect(p, x0, cy - 4, 120, 8, 0xff767676, False)
		o["dolu"] = self._Rect(p, x0, cy - 4, 1, 8, C_SARI)
		top = ui.Window()
		top.SetParent(p)
		top.AddFlag("not_pick")
		top.SetSize(16, 16)
		top.Show()
		self.keep.append(top)
		self._Daire(top, 8, 8, 16, C_SARI)
		o["topuz"] = top
		o["x0"] = x0
		o["cy"] = cy
		o["deger"] = self._Txt(p, F_AD, C_SARI, sag, cy, "right")
		o["hit"] = self._Dokun(p, x0 - 8, ry + 1, 120 + 16, SATIR_H - 2, None, ui.__mem_func__(self.__KaydirBasla))

	def __KurAnahtar(self, o, k, sag, ry):
		p = self.pen
		x = sag - 52
		yy = ry + 11
		o["zemin"] = self._Rect(p, x, yy, 52, 26, 0xff120e09)
		o["cizgi"] = self._Rect(p, x, yy, 52, 26, C_KENAR, False)
		o["topuz"] = self._Rect(p, x + 4, yy + 4, 18, 18, 0xff5d5240)
		o["x"] = x
		o["y"] = yy
		self._Dokun(p, x - 14, ry + 1, 52 + 14 + 10, SATIR_H - 2, (lambda a=k: self.__Anahtar(a)))

	# ---------------- \xe7izim (durum -> g\xf6r\xfcn\xfcm)
	def __Ciz(self):
		self.__CizKademe()
		for (k, tur, sec) in AYAR:
			o = self.satir[k]
			v = self.deger[k]
			if tur == "sec":
				for (d, zemin, t) in o["sec"]:
					on = (str(v) == d)
					zemin.SetColor(0xff4a3a1e if on else 0xff120e09)
					t.SetPackedFontColor(C_SARI if on else C_ALT)
			elif tur == "kaydir":
				self.__CizKaydir()
			else:
				on = bool(v)
				o["zemin"].SetColor(0xff3a2f1f if on else 0xff120e09)
				o["cizgi"].SetColor(C_SARI if on else C_KENAR)
				o["topuz"].SetColor(C_SARI if on else 0xff5d5240)
				o["topuz"].SetPosition(o["x"] + (30 if on else 4), o["y"] + 4)
		self.__Olc()
		self.__CizNot()

	def __CizKademe(self):
		for ad in KADEMELER:
			o = self.kd[ad]
			on = (self.kademe == ad)
			(a, b) = ((0x4a, 0x3a, 0x1e), (0x2a, 0x20, 0x10)) if on else ((0x2a, 0x22, 0x16), (0x17, 0x12, 0x0c))
			n = len(o["seritler"])
			for (j, s) in enumerate(o["seritler"]):
				f = (j + 0.5) / n
				c = [int(round(a[i] + (b[i] - a[i]) * f)) for i in (0, 1, 2)]
				s.SetColor(0xff000000 | (c[0] << 16) | (c[1] << 8) | c[2])
			o["cizgi"].SetColor(C_SARI if on else C_KENAR)
			o["ad"].SetPackedFontColor(C_SARI if on else C_KREM)
			o["alt"].SetPackedFontColor(C_ALTIN if on else C_SOLUK)
		sec = self.kd.get(self.kademe)		# "ozel": hi\xe7bir kademe se\xe7ili de\xf0il -> par\xfdlt\xfd gizli
		for (k, g) in enumerate(self.kdParla):
			if sec:
				g.SetPosition(_R(sec["x"]) + k + 1, KAD_Y + k + 1)
				g.SetSize(max(1, _R(sec["x"] + self.kdKw) - _R(sec["x"]) - 2 * (k + 1)), KAD_H - 2 * (k + 1))
				g.Show()
			else:
				g.Hide()

	def __CizKaydir(self):
		o = self.satir["coz"]
		v = self.deger["coz"]
		f = (v - COZ_MIN) / float(COZ_MAX - COZ_MIN)
		cx = o["x0"] + 8 + f * (120 - 16)
		o["dolu"].SetSize(max(1, _R(cx) - _R(o["x0"])), 8)
		o["topuz"].SetPosition(_R(cx - 8), _R(o["cy"] - 8))
		o["deger"].SetText("%d%%" % v)

	def __CizNot(self):
		y = Y()
		if YenidenBekliyor():		# panel geri say\xfdm s\xfdras\xfdnda yeniden a\xe7\xfdld\xfdysa da
			self.notT.SetText(y["baslatiliyor"])
			self.notT.SetPackedFontColor(C_SARI)
		elif DokuBekliyor(self.deger["doku"]):
			self.notT.SetText(y["yeniden"])
			self.notT.SetPackedFontColor(C_TURUNCU)
		else:
			self.notT.SetText(y["not"])
			self.notT.SetPackedFontColor(C_NOT)

	def Yuk(self):
		"""tahmini y\xfck (0..1): prototip yuk() BIREBIR - her ayar\xfdn g\xf6reli maliyeti, cihaz g\xfcc\xfcne b\xf6l\xfcn\xfcr"""
		v = self.deger
		m = {"dusuk": 0, "orta": .5, "yuksek": 1, "kapali": 0, "ben": .4, "herkes": 1, "az": 0, "normal": .5, "tam": 1,
			"yakin": 0, "uzak": 1, "yakinda": 0, "hep": 1}
		l = 0.0
		l += (int(v["fps"]) - 30) / 30.0 * .9
		l += ((v["coz"] / 100.0) ** 2) * 1.6
		l += m[v["doku"]] * .35 + m[v["golge"]] * .6 + m[v["efekt"]] * .5 + m[v["mesafe"]] * .45 + (int(v["oyuncu"]) - 20) / 50.0 * .55
		l += (.3 if v["digerEf"] else 0) + m[v["isim"]] * .15
		return min(1.0, l / GUC[self.cihaz])

	def __Olc(self):
		l = self.Yuk()
		ak = max(.05, 1 - l * .9)
		isi = min(1.0, l * (.85 if self.deger["pil"] else 1))
		sev = Y()["seviye"]

		def renk(x):
			return C_KIRMIZI if x > .66 else (C_TURUNCU if x > .4 else C_YESIL)
		for (i, (x, kotu)) in enumerate(((ak, 1 - ak), (isi, isi))):
			(dolu, t, x0, w) = self.olcer[i]
			dolu.SetSize(max(1, _R(x * w)), 6)
			dolu.SetColor(renk(kotu))
			t.SetText(sev[min(4, int(x * 5))])

	# ---------------- olaylar (yeniden ba\xfelatma beklerken se\xe7imler kilitli: kaydedilen de\xf0er de\xf0i\xfemesin)
	def __Kademe(self, ad):
		if YenidenBekliyor():
			return
		self.kademe = ad
		self.deger = KademeDeger(ad)
		self.__Ciz()

	def __Ozel(self):
		self.kademe = "ozel"		# prototip ozel(): elle de\xf0i\xfeince hi\xe7bir kademe se\xe7ili de\xf0il

	def __Sec(self, k, v):
		if YenidenBekliyor():
			return
		self.deger[k] = v
		self.__Ozel()
		self.__Ciz()

	def __Anahtar(self, k):
		if YenidenBekliyor():
			return
		self.deger[k] = not self.deger[k]
		self.__Ozel()
		self.__Ciz()

	def __KaydirBasla(self):
		if YenidenBekliyor():
			return
		self.surukle = True
		self.__KaydirGuncelle()

	def __KaydirGuncelle(self):
		o = self.satir["coz"]
		try:
			(mx, my) = wndMgr.GetMousePosition()
			(gx, gy) = o["hit"].GetGlobalPosition()
		except:
			return
		lx = mx - gx - 8		# hit alan\xfd izden 8 px solda ba\xfelar
		f = max(0.0, min(1.0, (lx - 8) / float(120 - 16)))
		v = COZ_MIN + int(round(f * (COZ_MAX - COZ_MIN) / float(COZ_ADIM))) * COZ_ADIM
		if v != self.deger["coz"]:
			self.deger["coz"] = v
			self.__Ozel()
			self.__CizKademe()
			self.__CizKaydir()
			self.__Olc()

	def __Varsayilan(self):
		if YenidenBekliyor():
			return
		self.kademe = "oto"
		self.deger = KademeDeger("oto")
		self.__Ciz()

	def __Uygula(self):
		"""uygula + kaydet; doku kalitesi a\xe7\xfdl\xfd\xfeta y\xfcklenenden farkl\xfdysa ve m\xfcmk\xfcnse (app.RestartApp, d\xfcello de\xf0il, kay\xfdt
		D\xddSKE YAZILDI) 1.5 sn sonra oyun kendili\xf0inden yeniden ba\xfelar; de\xf0ilse eski not (elle yeniden ba\xfelat)"""
		if YenidenBekliyor():
			return
		y = Y()
		yazildi = Uygula(self.kademe, self.deger)
		if yazildi and DokuBekliyor(self.deger["doku"]) and YenidenBaslatabilir():
			YenidenBaslatPlanla()
			self.yenidenGosterildi = True
			self.__CizNot()
			self.__Bildirim(y["baslatiliyor"], 0)		# yeniden ba\xfelayana kadar a\xe7\xfdk kal\xfdr
			return
		self.__CizNot()
		self.__Bildirim(y["uygulandi"])

	def __Bildirim(self, metin, sure=1.6):
		t = self.bilT
		t.SetText(metin)
		bw = _Genislik(t, metin) + 34
		self.bilWin.SetPosition(_R((W - bw) / 2.0), BILDIRIM_Y)
		self.bilWin.SetSize(_R(bw), 34)
		self.bilZemin.SetSize(_R(bw), 34)
		self.bilCizgi.SetSize(_R(bw), 34)
		t.SetPosition(_R(bw / 2.0), 17)
		self.bilWin.Show()
		self.bilWin.SetTop()
		self.bildirimSon = (app.GetTime() + sure) if sure else 0.0		# 0: kendili\xf0inden kapanmaz

	def __Fps(self, simdi=False):
		"""anl\xfdk FPS: yeni APK GetPerfStats()[0]; eski APK GetRenderFPS(); o da 0 ise panelin kendi kare sayac\xfd"""
		fps = 0
		f = getattr(app, "GetPerfStats", None)
		if f:
			try:
				fps = int(f()[0])
			except:
				fps = 0
		if fps <= 0:
			g = getattr(app, "GetRenderFPS", None)
			if g:
				try:
					fps = int(g())
				except:
					fps = 0
		if fps <= 0:
			fps = self.fpsSayac
		if fps > 0 or simdi:
			metin = ("%d" % fps) if fps > 0 else "--"		# kare sayac\xfd ilk saniyede hen\xfcz yok
			self.fpsT.SetText(metin)
			self.fpsEk.SetPosition(_R(SUT2 + _Genislik(self.fpsT, metin) + 4), 95)

	def __Guncelle(self):
		t = app.GetTime()
		self.sayac[0] += 1
		if t - self.sayac[1] >= 1.0:
			self.fpsSayac = int(round(self.sayac[0] / (t - self.sayac[1])))
			self.sayac = [0, t]
		if self.surukle:
			if getattr(wndMgr, "IsLeftButtonDown", None) and wndMgr.IsLeftButtonDown():
				self.__KaydirGuncelle()
			else:
				self.surukle = False
		if t >= self.fpsSon:
			self.fpsSon = t + 0.25		# prototip: 250 ms
			self.__Fps()
		if self.bildirimSon and t >= self.bildirimSon:
			self.bildirimSon = 0.0
			self.bilWin.Hide()
		if self.yenidenGosterildi and not YenidenBekliyor() and _YB["hata"]:
			## app.RestartApp ba\xfear\xfds\xfdz: eski nota d\xf6n (oyuncu elle yeniden ba\xfelat\xfdr)
			self.yenidenGosterildi = False
			self.bilWin.Hide()
			self.__CizNot()

	def Kapat(self):
		try:
			self.kok.guncelle = None
			self.kok.Hide()
		except:
			pass
		self.keep = []
		self.satir = {}
		self.kd = {}
		self.olcer = []
		if _PEN[0] is self:
			_PEN[0] = None


def Ac():
	"""Ayarlar penceresi (uisystem.py) "Grafik Ayarlar\xfd" d\xfc\xf0mesi"""
	try:
		Kapat()
		_PEN[0] = GrafikPaneli()
	except:
		_Hata("Ac")


def Kapat():
	w = _PEN[0]
	_PEN[0] = None
	if w:
		w.Kapat()


def AcikMi():
	return _PEN[0] is not None
