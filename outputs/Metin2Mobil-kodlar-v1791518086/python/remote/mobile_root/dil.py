# MOBIL - dil.py: oyuncunun DIL SECIMI (KULLANICI 2026-10-06: "once Ingilizce, ilk giriste hangi dili istiyorsun diye sor,
# ortak dil Ingilizce olsun - global"). Tek sunucu, herkes kendi dilini gorur; ceviriler ISTEMCIDE.
# Secim telefonda pack/dil.cfg (giris ekrani hesap dosyalari gibi; indirme yoneticisi pack/ altindaki bu dosyalara dokunmaz).
# Ortak / varsayilan dil "en": cevirisi olmayan yazi ya da bilinmeyen dil Ingilizceye duser.
import os

DOSYA = "pack/dil.cfg"
DILLER = ("tr", "en")
VARSAYILAN = "en"
_DIL = [None, False]		# [kayitli dil, okundu mu]


def _Oku():
	if _DIL[1]:
		return _DIL[0]
	_DIL[1] = True
	try:
		f = open(DOSYA, "r")
		v = f.read().strip().lower()
		f.close()
		if v in DILLER:
			_DIL[0] = v
	except:
		pass
	return _DIL[0]


def Secildi():
	"""oyuncu dilini daha once secti mi (ilk acilis penceresi icin)"""
	return _Oku() is not None


_ONERI = [None]


def Mevcut():
	"""gecerli dil kodu ("tr" / "en"); secilmemisse Oneri() (kayitli hesabi olan eski oyuncu "tr", yeni kurulum "en")
	- giris ekrani dil kartinda gosterilenle ayni olsun diye"""
	v = _Oku()
	if v:
		return v
	if _ONERI[0] is None:
		_ONERI[0] = Oneri()
	return _ONERI[0]


def Kaydet(d):
	if d not in DILLER:
		return False
	try:
		f = open(DOSYA, "w")
		f.write(d)
		f.close()
	except:
		import dbg
		dbg.TraceError("dil: kaydedilemedi " + DOSYA)
	_DIL[0] = d
	_DIL[1] = True
	return True


def Oneri():
	"""ilk acilista secili gelecek dil. Telefonun dilini okuyan yerel cagri henuz yok (APK_BEKLEYENLER 7):
	telefonda kayitli hesabi olan (mevcut, Turk) oyuncuya "tr", yeni kuruluma ortak dil "en"."""
	try:
		import app
		f = getattr(app, "GetSystemLanguage", None)
		if f:
			v = str(f()).lower()[:2]
			if v:		# bos donerse (dil okunamadi) hesap dosyasi yoklamasina dus
				return "tr" if v == "tr" else "en"
	except:
		pass
	for i in range(1, 5):		# giris ekrani hesap dosyalari pack/hesap1..4.cfg
		if os.path.exists("pack/hesap%d.cfg" % i):
			return "tr"
	if os.path.exists("pack/mobile_login.cfg"):
		return "tr"
	return VARSAYILAN


def Klasor():
	"""oyun yazi dosyalari klasoru (locale_game / locale_interface / item_proto / itemdesc / mob_proto / skilldesc ...):
	dil=en ve locale/en indirilmisse "locale/en", aksi halde oyunun kendi locale yolu (locale/tr).
	Gorseller (locale/tr/ui/...) her zaman oyunun yolundan okunur."""
	try:
		import app
		yol = app.GetLocalePath()
	except:
		yol = "locale/tr"
	if Mevcut() == "en":
		try:
			import pack
			if pack.Exist("locale/en/locale_game.txt"):
				return "locale/en"
		except:
			pass
	return yol


def Uygula():
	"""dil degisince (giris ekraninda): arayuz yazilari yeni dilden yeniden yuklenir + gomulu yazi cevirisi ac/kapa.
	Esya/canavar/beceri adlari karakter secimine girerken (networkModule.SetSelectCharacterPhase ->
	localeInfo.LoadLocaleData) zaten yeni klasorden yuklenir."""
	k = Klasor()
	try:
		import localeInfo
		localeInfo.LoadLocaleFile(k + "/locale_game.txt", localeInfo.__dict__)
	except:
		import dbg, traceback
		dbg.TraceError("dil.Uygula localeInfo: " + traceback.format_exc())
	try:
		import uiScriptLocale
		uiScriptLocale.LoadLocaleFile(k + "/locale_interface.txt", uiScriptLocale.__dict__)
		for (ad, dosya) in (("JOBDESC_WARRIOR_PATH", "jobdesc_warrior.txt"), ("JOBDESC_ASSASSIN_PATH", "jobdesc_assassin.txt"),
				("JOBDESC_SURA_PATH", "jobdesc_sura.txt"), ("JOBDESC_SHAMAN_PATH", "jobdesc_shaman.txt"),
				("EMPIREDESC_A", "empiredesc_a.txt"), ("EMPIREDESC_B", "empiredesc_b.txt"), ("EMPIREDESC_C", "empiredesc_c.txt")):
			setattr(uiScriptLocale, ad, k + "/" + dosya)
	except:
		import dbg, traceback
		dbg.TraceError("dil.Uygula uiScriptLocale: " + traceback.format_exc())
	try:
		import ceviri
		ceviri.Kur()
	except:
		import dbg, traceback
		dbg.TraceError("dil.Uygula ceviri: " + traceback.format_exc())
