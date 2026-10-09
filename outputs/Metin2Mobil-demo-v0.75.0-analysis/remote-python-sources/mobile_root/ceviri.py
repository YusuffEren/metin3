# MOBIL - ceviri.py: betiklere GOMULU Turkce arayuz yazilarinin cevirisi (KULLANICI 2026-10-06: "hepsini bitir").
# locale_game/locale_interface/itemdesc/item_proto/mob_proto/skilldesc dil klasorunden (locale/en) gelir; bu modul
# yalniz Python betiklerinde sabit yazilmis Turkce yazilar icindir. ui.TextLine.SetText + chat.AppendChat cagirir.
# Tablo: cevirien.py (tools/dil/uret_cevirien.py uretir): TAM {tr: en}, KALIP [(tr, en)] (%s/%d), PARCA [(tr, en)].
# dil=tr iken ACIK[0] = False -> SetText'te tek bir liste okumasi, baska yuk yok.
import re

ACIK = [False]
_TAM = {}
_KALIP = []		# [(derlenmis regex, en, cipa)]
_PARCA = []		# [(tr, en)] uzundan kisaya
_HAFIZA = {}
_GORSEL = {}		# {kucuk harf tr yolu: en yolu}
_SOHBET = [None]
_TR_HARF = re.compile("[\xe7\xf0\xfd\xf6\xfe\xfc\xc7\xd0\xdd\xd6\xde\xdc]")
_YT = re.compile(r"%[-+ #0-9.]*[sdifxXcu]")
_YUKLU = [False]


def _Yukle():
	if _YUKLU[0]:
		return
	_YUKLU[0] = True
	try:
		import cevirien
	except:
		import dbg, traceback
		dbg.TraceError("ceviri: cevirien yuklenemedi " + traceback.format_exc())
		return
	_TAM.update(cevirien.TAM)
	for (tr, en) in cevirien.KALIP:
		parcalar = _YT.split(tr)
		## yer tutucu turune gore grup: %d/%i/%u sayi, %f ondalik, %x onaltilik, digerleri (%s) serbest
		gruplar = []
		for y in _YT.findall(tr):
			t = y[-1]
			gruplar.append(t in "diu" and r"(-?[\d.,]+)" or t == "f" and r"(-?[\d.,]+)" or t in "xX" and r"([0-9a-fA-F]+)" or "(.*?)")
		rx = "^" + re.escape(parcalar[0]) + "".join([g + re.escape(p) for (g, p) in zip(gruplar, parcalar[1:])]) + "$"
		cipa = max(parcalar, key=len)
		try:
			_KALIP.append((re.compile(rx, re.S), en, cipa))
		except:
			pass
	_PARCA.extend(cevirien.PARCA)
	_GORSEL.update(getattr(cevirien, "GORSEL", {}))


def G(p):
	"""yazili gorselin Ingilizcesi (ui.py ImageBox/Button yukleyicileri cagirir); yoksa ayni yol"""
	if not ACIK[0] or not _GORSEL or type(p) is not str:
		return p
	return _GORSEL.get(p.replace("\\", "/").lower(), p)


def Kur():
	"""dil.Mevcut()'a gore ac/kapa; ilk acilista tablo + chat.AppendChat sarmalayicisi"""
	try:
		import dil
		acik = (dil.Mevcut() == "en")
	except:
		acik = False
	if acik:
		_Yukle()
		if _SOHBET[0] is None:
			try:
				import chat
				eski = chat.AppendChat
				_SOHBET[0] = eski

				def _AppendChat(tip, mesaj, *a):
					if ACIK[0]:
						mesaj = T(mesaj)
					return eski(tip, mesaj, *a)
				chat.AppendChat = _AppendChat
			except:
				pass
	_HAFIZA.clear()
	ACIK[0] = acik


def _Kalip(s):
	for (rx, en, cipa) in _KALIP:
		if cipa and cipa not in s:
			continue
		m = rx.match(s)
		if not m:
			continue
		gruplar = list(m.groups())
		try:
			return _YT.sub(lambda x: gruplar.pop(0) if gruplar else x.group(0), en)
		except:
			return None
	return None


def _Harf(c):
	return c.isalpha() or c in "\xe7\xf0\xfd\xf6\xfe\xfc\xc7\xd0\xdd\xd6\xde\xdc"


def _Parca(s):
	"""bilinen cumle parcalarini kelime sinirinda degistir (betikte birlestirilen yazilar: "x" + ad + " kullanilsin mi?").
	Yarim Turkce-yarim Ingilizce sonuc cikmasin: degisen harfler yazinin harflerinin %60'ini kapsamiyorsa ozgun kalir."""
	ozgun = s
	harf = len([c for c in s if _Harf(c)])
	if not harf:
		return s
	kapsanan = 0
	for (tr, en) in _PARCA:
		i = s.find(tr)
		while i >= 0:
			j = i + len(tr)
			if (i == 0 or not _Harf(s[i - 1]) or not _Harf(tr[0])) and (j >= len(s) or not _Harf(s[j]) or not _Harf(tr[-1])):
				kapsanan += len([c for c in tr if _Harf(c)])
				s = s[:i] + "\x00" + en + "\x00" + s[j:]		# degisen kisim tekrar eslenmesin
				i = s.find(tr, i + len(en) + 2)
			else:
				i = s.find(tr, i + 1)
	## kalan (degismeyen) kisimda Turkce harf varsa ya da kapsama %40'tan azsa ozgun yazi kalir
	kalan = "".join(s.split("\x00")[0::2])
	if kapsanan * 10 < harf * 4 or _TR_HARF.search(kalan):
		return ozgun
	return s.replace("\x00", "")


def _Cevir(s):
	e = _TAM.get(s)
	if e is not None:
		return e
	## bas/son bosluk ve satir sonlari ayrilip tekrar denenir
	b = s.strip()
	if b != s and b:
		e = _TAM.get(b)
		if e is not None:
			return s[:len(s) - len(s.lstrip())] + e + s[len(s.rstrip()):]
	e = _Kalip(s)
	if e is not None:
		return e
	if _TR_HARF.search(s) or len(s) < 200:
		return _Parca(s)
	return s


def T(s):
	if not ACIK[0] or type(s) is not str or not s:
		return s
	r = _HAFIZA.get(s)
	if r is not None:
		return r
	try:
		r = _Cevir(s)
	except:
		r = s
	if len(_HAFIZA) > 6000:
		_HAFIZA.clear()
	_HAFIZA[s] = r
	return r
