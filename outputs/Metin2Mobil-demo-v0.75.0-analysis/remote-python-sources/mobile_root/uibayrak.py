# -*- coding: utf-8 -*-
# MOBIL - mobile_root/uibayrak.py: HESAP BA\xdeINA \xdcLKE BAYRA\xd0I (nick yan\xfdnda, herkes g\xf6r\xfcr).
# \xdcRET\xddL\xddR: tools/bayrak/uibayrak_kaynak.py (UTF-8) -> tools/bayrak/gen_uibayrak.py -> bu dosya (cp1254 ka\xe7\xfd\xfel\xfd ASCII).
#
# KULLANICI (2026-10-06): prototip Desktop/Averos2-Bayrak-Prototip (bayrak.html + degistir.html) onayland\xfd.
#  - Karakter olu\xfeturma: sa\xf0 altta "Bayrak Se\xe7" d\xfc\xf0mesi -> pencere; se\xe7im hesab\xfdn \xddLK bayra\xf0\xfd olur (oyuna ilk giri\xfete
#    "/bayrak ilk <kod>"; sunucu hesab\xfdn bayra\xf0\xfd yoksa kabul eder). Hesab\xfdn bayra\xf0\xfd varsa d\xfc\xf0me kilitli (hesap bayra\xf0\xfd).
#  - Oyun i\xe7i: 71182 "Bayrak De\xf0i\xfetirme" nesnesine iki kez dokununca (uiinventory __UseItem) de\xf0i\xfetirme penceresi;
#    "/bayrak degistir <kod>" -> sunucu nesneyi 1 harcar, "bayrak_tamam <kod>" d\xf6ner.
#  - Sunucu her oyuncunun bayra\xf0\xfdn\xfd "bayrak <vid> <kod>" komutuyla bildirir -> textTail.SetCharacterFlag (yeni APK;
#    eski APK'da herkes eskisi gibi T\xfcrk bayra\xf0\xfd).
#  - \xddK\xdd D\xddL: t\xfcm yaz\xfdlar YAZI[tr/en] (dil.Mevcut()).
import ui
import wndMgr
import app
import net
import dil
import bayrakveri

DIR = "mobile/ui/bayrak/"
PT = "d:/ymir work/ui/pattern/"
PUB = "d:/ymir work/ui/public/"
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")
TASMA = 0.02
ONBELLEK = "pack/bayrak_hesap.cfg"		# "hesap kod" sat\xfdrlar\xfd (karakter olu\xfeturmada kilit i\xe7in)
BEKLEYEN = "pack/bayrak_bekleyen.cfg"	# "hesap kod" - olu\xfeturmada se\xe7ilen, oyuna girince sunucuya gider
NESNE = 71182

W, H = 600, 600		# KULLANICI: oklarin altindaki bilgi yazisi cok yakin/kucuktu -> asagi alindi, pencere uzadi
SUTUN, SATIR = 6, 3
HW, HH, ARA = 86, 74, 6		# h\xfccre
GX, GY = 27, 174

C_KREM = 0xfff1e6c0
C_ALTIN = 0xffe8d08a
C_ALT = 0xffc9b88f
C_KAPALI = 0xff8f8470
C_SARI = 0xfff2c94c
C_BASLIK = 0xfffeedc6
C_DUGME = 0xffffe08a
C_ADK = 0xfff4ead2		# hucre ulke adi: telefonda pencere ~1.7x buyutulur, 12 px soluk/bulanikti -> 14 px + acik renk

YAZI = {
	"tr": {"sec": "Bayrak Se\xe7", "degistir_bas": "Bayrak De\xf0i\xfetir", "mevcut": "Mevcut bayrak", "yeni": "Yeni bayrak",
		"ara": "\xdclke ara...", "sayfa": "Sayfa %d / %d", "bos": "Sonu\xe7 yok", "tamam": "Tamam", "degistir": "De\xf0i\xfetir",
		"vazgec": "Vazge\xe7", "hesap_not": "Hesap ba\xfe\xfdna tek bayrak: hesab\xfdndaki t\xfcm karakterlerde g\xf6r\xfcn\xfcr.",
		"hesap_not2": "Sonradan de\xf0i\xfetirmek i\xe7in oyundaki Bayrak De\xf0i\xfetirme nesnesi gerekir.",
		"degistir_not": "Bu i\xfelem 1 adet Bayrak De\xf0i\xfetirme nesnesi harcar.",
		"degistir_not2": "Bayrak hesab\xfdndaki t\xfcm karakterlerde de\xf0i\xfeir.",
		"onay": "Bayra\xf0\xfdn %s olarak de\xf0i\xfeecek. Onayl\xfdyor musun?", "oldu": "Bayra\xf0\xfdn de\xf0i\xfeti: %s",
		"kilit": "Hesab\xfdn\xfdn bayra\xf0\xfd: %s. De\xf0i\xfetirmek i\xe7in oyundaki Bayrak De\xf0i\xfetirme nesnesini kullan.",
		"hesap_bayrak": "Hesap bayra\xf0\xfd"},
	"en": {"sec": "Choose Flag", "degistir_bas": "Change Flag", "mevcut": "Current flag", "yeni": "New flag",
		"ara": "Search country...", "sayfa": "Page %d / %d", "bos": "No results", "tamam": "OK", "degistir": "Change",
		"vazgec": "Cancel", "hesap_not": "One flag per account: shown on all characters of your account.",
		"hesap_not2": "To change it later you need a Flag Change item in game.",
		"degistir_not": "This uses 1 Flag Change item.",
		"degistir_not2": "The flag changes on all characters of your account.",
		"onay": "Your flag will change to %s. Are you sure?", "oldu": "Your flag is now: %s",
		"kilit": "Your account flag: %s. Use a Flag Change item in game to change it.",
		"hesap_bayrak": "Account flag"},
}

HESAP = [None]			# giri\xfe kimli\xf0i (networkModule stream.id) - Hesap() ile
_ULKE = {}
for _u in bayrakveri.ULKE:
	_ULKE[_u[0]] = _u


def Y():
	try:
		return YAZI.get(dil.Mevcut(), YAZI["en"])
	except:
		return YAZI["en"]


def Ad(kod):
	u = _ULKE.get(kod)
	if not u:
		return kod
	try:
		return u[1] if dil.Mevcut() == "tr" else u[2]
	except:
		return u[2]


def Yol(kod):
	return DIR + kod + ".png"


def Hesap(hid):
	if hid:
		HESAP[0] = str(hid).strip().lower()
		_KENDI[0] = HesapBayragi()		# telefondaki onbellek: giri\xfete bayrak sunucuyu beklemeden konur


def _Oku(yol):
	d = {}
	try:
		for l in open(yol, "r").read().split("\n"):
			p = l.split()
			if len(p) == 2:
				d[p[0]] = p[1]
	except:
		pass
	return d


def _Yaz(yol, d):
	try:
		f = open(yol, "w")
		f.write("\n".join(["%s %s" % (k, v) for (k, v) in d.items()]))
		f.close()
	except:
		pass


def HesapBayragi():
	"""bu hesab\xfdn bilinen bayra\xf0\xfd (sunucudan gelmi\xfe \xf6nbellek) ya da None"""
	if not HESAP[0]:
		return None
	return _Oku(ONBELLEK).get(HESAP[0])


# ------------------------------------------------------------------ bayrak yenileyici
# MOTOR HATASI (v75): her GC_CHARACTER_UPDATE'te ChangeGuild -> DetachTextTail -> DeleteCharacterTextTail isim etiketini
# silip yeniden kurar ve SetCharacterFlag kaydini da siler (PythonTextTail.cpp:1084) -> bayrak Turk bayragina doner.
# Paket telafisi: vid -> yol burada tutulur; game.py OnRender HER KAREDE cizimden hemen once Yenile() cagirir ->
# silinen kayit ayni karede geri gelir, Turk bayragi hic gorunmez. Maliyet: bayrakli gorunen oyuncu basina bir C
# cagrisi (std::map atamasi). Karakter gitmisse (saniyede bir denetim) kayit silinir. Kendi bayragimiz telefondaki
# onbellekten (pack/bayrak_hesap.cfg) giriste HEMEN konur; sunucu farkliysa komutu ustune yazar.
# Motor duzeltmesi APK_BEKLEYENLER 9 (kayit karakter yok edilince silinmeli, etiket yenilenince degil).
_BAYRAKLAR = {}
_KENDI = [None]		# bu hesabin bayrak kodu (telefondaki onbellek / sunucudan)
_DURUM = {"f": None, "budama": 0.0}


def Sifirla():
	"""oyun penceresi acilinca (game.py Open): onceki oturumun vid'leri gecersiz (chr.Destroy) -> instance'i
	olmayanlar atilir. Tumden silinmez: Open'dan once islenmis bir "bayrak" komutu kaybolmasin."""
	try:
		import chr
		for vid in list(_BAYRAKLAR.keys()):
			if not chr.HasInstance(vid):
				del _BAYRAKLAR[vid]
	except:
		_BAYRAKLAR.clear()


def Yenile():
	"""game.py OnRender: her karede, app.RenderGame'den once.
	Eski motor (v75): kayit her karakter guncellemesinde siliniyor -> bayraklar HER KAREDE yeniden uygulanir.
	v76+ motor (textTail.BAYRAK_KALICI): kayit kalici, karakter yok edilince motor unutur -> kare basi uygulama YOK;
	yalniz kendi bayragimiz (telefondaki onbellek) giriste bir kez konur. Maliyet ~0."""
	f = _DURUM["f"]
	if f is None:
		try:
			import textTail
			f = getattr(textTail, "SetCharacterFlag", None)
			_DURUM["kalici"] = bool(f and getattr(textTail, "BAYRAK_KALICI", 0))
		except:
			f = None
		_DURUM["f"] = f or False
	if not f:
		return		# eski APK: isim etiketi bayragi yok
	try:
		import player
		ana = player.GetMainCharacterIndex()
		if ana and _KENDI[0] and ana not in _BAYRAKLAR:
			_BAYRAKLAR[ana] = Yol(_KENDI[0])
			f(ana, _BAYRAKLAR[ana])		# giri\xfete sunucuyu beklemeden
		if not _BAYRAKLAR:
			return
		kalici = _DURUM.get("kalici")
		if not kalici:
			for vid, yol in _BAYRAKLAR.iteritems():		# iteritems: her karede liste kopyasi olusturmaz
				f(vid, yol)
		t = app.GetTime()
		if t - _DURUM["budama"] >= 1.0:
			_DURUM["budama"] = t
			import chr
			for vid in list(_BAYRAKLAR.keys()):
				if not chr.HasInstance(vid):
					del _BAYRAKLAR[vid]
					if not kalici:
						f(vid, "")
	except:
		pass


# ------------------------------------------------------------------ sunucu komutlar\xfd (game.py)
def Komut(vid, kod):
	"""bayrak <vid> <kod>: isim etiketine bayrak (yeni APK) + kendi bayra\xf0\xfdm\xfdzsa \xf6nbellek"""
	if kod not in bayrakveri.GECERLI:
		return
	try:
		import textTail
		f = getattr(textTail, "SetCharacterFlag", None)
		if f:
			f(int(vid), Yol(kod))
			_BAYRAKLAR[int(vid)] = Yol(kod)
	except:
		import dbg, traceback
		dbg.TraceError("bayrak Komut: " + traceback.format_exc())
	try:
		import player
		if int(vid) == player.GetMainCharacterIndex() and HESAP[0]:
			_KENDI[0] = kod
			d = _Oku(ONBELLEK)
			if d.get(HESAP[0]) != kod:
				d[HESAP[0]] = kod
				_Yaz(ONBELLEK, d)
	except:
		pass


def Tamam(kod):
	"""bayrak_tamam <kod>: de\xf0i\xfeiklik sunucuda yap\xfdld\xfd"""
	Kapat()
	try:
		import chat
		chat.AppendChat(chat.CHAT_TYPE_INFO, Y()["oldu"] % Ad(kod))
	except:
		pass


def GirisGonder():
	"""oyuna girince (game.py, /dil'den sonra): karakter olu\xfeturmada se\xe7ilen bayra\xf0\xfd bir kez g\xf6nder"""
	if not HESAP[0]:
		return
	d = _Oku(BEKLEYEN)
	kod = d.get(HESAP[0])
	if not kod:
		return
	if kod in bayrakveri.GECERLI:
		net.SendChatPacket("/bayrak ilk " + kod)
	del d[HESAP[0]]
	_Yaz(BEKLEYEN, d)


# ------------------------------------------------------------------ pencere par\xe7alar\xfd
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


class _Kok(ui.Window):
	def __init__(self, yut=True):
		ui.Window.__init__(self, "TOP_MOST")
		self.yut = yut
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		return self.yut

	def OnMouseLeftButtonUp(self):
		return self.yut


class _Hit(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.onUp = None

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		return True

	def OnMouseLeftButtonUp(self):
		if self.onUp:
			self.onUp()
		return True


class _Ara(ui.EditLine):
	def __init__(self):
		ui.EditLine.__init__(self)
		self.degisti = None

	def __del__(self):
		ui.EditLine.__del__(self)

	def OnIMEUpdate(self):
		ui.EditLine.OnIMEUpdate(self)
		if self.degisti:
			self.degisti()


class _Parca(object):
	"""ortak \xe7izim yard\xfdmc\xfdlar\xfd (pencere i\xe7i koordinat = mant\xfdksal px)"""

	def _Img(self, parent, path, x, y, sx=1.0, sy=1.0):
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(path)
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		w.SetScale(sx, sy)
		w.SetPosition(int(round(x)), int(round(y)))
		w.Show()
		self.keep.append(w)
		return w

	def _Tile(self, parent, path, x, y, w, h, tw, th, sx=1.0, sy=1.0):
		img = self._Img(parent, path, x, y, sx, sy)
		(zx, r) = _Otur(int(round(x + w)) - int(round(x)), w, tw, sx, HAS_RRS, 1.0)
		(zy, b) = _Otur(int(round(y + h)) - int(round(y)), h, th, sy, HAS_RRS, 1.0)
		img.SetScale(zx, zy)
		img.SetRenderingRect(0.0, 0.0, r, b)
		return img

	def _Rect(self, parent, x, y, w, h, color, fill=True):
		b = ui.Bar() if fill else ui.Box()
		b.SetParent(parent)
		b.AddFlag("not_pick")
		b.SetColor(color)
		b.SetPosition(int(round(x)), int(round(y)))
		b.SetSize(max(1, int(round(x + w)) - int(round(x))), max(1, int(round(y + h)) - int(round(y))))
		b.Show()
		self.keep.append(b)
		return b

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
		t.SetPosition(int(round(x)), int(round(y)))
		t.Show()
		self.keep.append(t)
		return t

	def _Dugme(self, parent, x, y, w, h, olay, buyuk=True):
		b = ui.Button()
		b.SetParent(parent)
		n = "large_button" if buyuk else "middle_button"
		b.SetUpVisual(PUB + n + "_01.sub")
		b.SetOverVisual(PUB + n + "_02.sub")
		b.SetDownVisual(PUB + n + "_03.sub")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, w / (88.0 if buyuk else 61.0), h / 21.0)
		b.SetPosition(int(round(x)), int(round(y)))
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
		x, y, w = 8, 7, W - 15
		bh = 23 * 1.6
		bw = 32 * 1.6
		self._Tile(p, PT + "titlebar_left.tga", x, y, bw, bh, 32, 32, 1.6, 1.6)
		self._Tile(p, PT + "titlebar_center.tga", x + bw, y, w - bw, bh, 32, 32, 1.6, 1.6)
		t = self._Txt(p, 20, C_BASLIK, 36, y + bh / 2.0 - 1)
		t.SetText(yazi)
		if kapat:
			c = 23 * 1.6 * 1.15
			cb = ui.Button()
			cb.SetParent(p)
			cb.SetUpVisual("mobile/ui/minimap/btn_close_sq.png")
			cb.SetOverVisual("mobile/ui/minimap/btn_close_sq.png")
			cb.SetDownVisual("mobile/ui/minimap/btn_close_sq_down.png")
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(cb.hWnd, c / 64.0, c / 64.0)
			cb.SetPosition(int(round(8 + W - 15 - c)), int(round(7 + (23 * 1.6 - c) / 2.0)))
			cb.SetEvent(kapat)
			cb.Show()
			self.keep.append(cb)
			hb = _Hit()
			hb.SetParent(p)
			hb.SetPosition(int(round(8 + W - 15 - c - 8)), 0)
			hb.SetSize(int(round(c + 16)), 52)
			hb.onUp = kapat
			hb.Show()
			self.keep.append(hb)
		return t


# ------------------------------------------------------------------ bayrak penceresi (olu\xfeturma / de\xf0i\xfetirme)
class BayrakPenceresi(_Parca):

	def __init__(self, mod, mevcut, bitti=None):
		"""mod: "olustur" (se\xe7im, bitti(kod)) | "degistir" (oyun i\xe7i; nesne harcar)"""
		self.mod = mod
		self.mevcut = mevcut or "tr"
		self.sec = self.mevcut
		self.bitti = bitti
		self.keep = []
		self.sayfa = 0
		self.liste = list(bayrakveri.ULKE)
		self.soru = None
		self.sw = float(wndMgr.GetScreenWidth())
		self.sh = float(wndMgr.GetScreenHeight())
		self.__Kur()
		self.__Suz()

	def __Kur(self):
		y = Y()
		kok = _Kok(True)
		kok.SetSize(int(self.sw), int(self.sh))
		kok.SetPosition(0, 0)
		kok.Show()
		self.keep.append(kok)
		self.kok = kok
		self._Rect(kok, 0, 0, self.sw, self.sh, 0x88000000 if self.mod == "degistir" else 0x44000000)
		## olu\xfeturmada sa\xf0da (karakterler g\xf6r\xfcns\xfcn), oyunda ortada
		if self.mod == "olustur":
			x0 = int(round(self.sw - W - 24))
		else:
			x0 = int(round((self.sw - W) / 2.0))
		y0 = int(round(max(4, (self.sh - H) / 2.0)))
		p = ui.Window()
		p.SetParent(kok)
		p.SetPosition(x0, y0)
		p.SetSize(W, H)
		p.Show()
		self.keep.append(p)
		self.pen = p
		self._Board(p, W, H)
		self._Baslik(p, W, y["sec"] if self.mod == "olustur" else y["degistir_bas"], ui.__mem_func__(self.Kapat))

		## \xfcst bilgi kutusu
		self._Rect(p, 22, 52, W - 44, 72, 0x8c000000)
		self._Rect(p, 22, 52, W - 44, 72, 0xff3d342a, False)
		if self.mod == "degistir":
			self._Txt(p, 13, C_ALT, 22 + (W - 44) * 0.25, 66, "center").SetText(y["mevcut"])
			self._Txt(p, 13, C_ALT, 22 + (W - 44) * 0.75, 66, "center").SetText(y["yeni"])
			self.mBay = self._Img(p, Yol(self.mevcut), 0, 82, 45 / 96.0, 30 / 64.0)
			self.mAd = self._Txt(p, 15, C_KREM, 0, 97)
			self.yBay = self._Img(p, Yol(self.mevcut), 0, 82, 45 / 96.0, 30 / 64.0)
			self.yAd = self._Txt(p, 15, C_SARI, 0, 97)
			self.okT = self._Txt(p, 18, C_ALTIN, W / 2.0, 92, "center")
			self.okT.SetText(">")
		else:
			self.oBay = self._Img(p, Yol(self.sec), 0, 64, 45 / 96.0, 30 / 64.0)
			self.oAd = self._Txt(p, 17, C_KREM, 0, 79)
			self._Txt(p, 13, C_ALT, W / 2.0, 108, "center").SetText(y["hesap_not"])

		## arama kutusu
		self._Rect(p, 22, 132, W - 44, 32, 0xff0e0b08)
		self._Rect(p, 22, 132, W - 44, 32, 0xff6b5a3e, False)
		ed = _Ara()
		ed.SetParent(p)
		ed.SetMax(24)
		ed.SetFontName("Tahoma:15")
		ed.SetPosition(34, 140)
		ed.SetSize(W - 70, 20)
		try:
			ed.overLay.SetFontName("Tahoma:15")
			ed.SetOverlayText(y["ara"])
		except:
			pass
		ed.degisti = ui.__mem_func__(self.__Suz)
		ed.Show()
		self.keep.append(ed)
		self.ara = ed
		h = _Hit()
		h.SetParent(p)
		h.SetPosition(22, 132)
		h.SetSize(W - 44, 32)
		h.onUp = ui.__mem_func__(self.__AraOdak)
		h.Show()
		self.keep.append(h)

		## \xfdzgara (SUTUN x SATIR h\xfccre, sayfal\xfd)
		self.hucre = []
		for i in xrange(SUTUN * SATIR):
			c, r = i % SUTUN, i / SUTUN
			x = GX + c * (HW + ARA)
			yy = GY + r * (HH + ARA)
			o = {}
			o["zemin"] = self._Rect(p, x, yy, HW, HH, 0x73000000)
			o["cizgi"] = self._Rect(p, x, yy, HW, HH, 0xff3d342a, False)
			o["sec1"] = self._Rect(p, x, yy, HW, HH, C_SARI, False)
			o["sec2"] = self._Rect(p, x + 1, yy + 1, HW - 2, HH - 2, 0x99f2c94c, False)
			o["parla"] = self._Rect(p, x + 2, yy + 2, HW - 4, HH - 4, 0x26f2c94c)
			o["cerceve"] = self._Rect(p, x + HW / 2.0 - 28, yy + 8, 56, 38, 0xff6b5a3e)
			o["bay"] = self._Img(p, Yol("tr"), x + HW / 2.0 - 27, yy + 9, 54 / 96.0, 36 / 64.0)
			o["ad"] = self._Txt(p, 14, C_ADK, x + HW / 2.0, yy + HH - 13, "center")
			o["tik"] = self._Rect(p, x + HW - 12, yy + 4, 8, 8, C_SARI)
			o["yesil"] = self._Rect(p, x + 4, yy + 4, 7, 7, 0xff7fc66b)
			hb = _Hit()
			hb.SetParent(p)
			hb.SetPosition(int(x), int(yy))
			hb.SetSize(HW, HH)
			hb.onUp = lambda i0=i: self.__Hucre(i0)
			hb.Show()
			self.keep.append(hb)
			o["hit"] = hb
			o["kod"] = None
			self.hucre.append(o)
		self.bosT = self._Txt(p, 13, C_KAPALI, W / 2.0, GY + 100, "center")

		## sayfa \xe7ubu\xf0u
		py = GY + SATIR * (HH + ARA) + 4
		self.solB = self._SayfaDugme(p, W / 2.0 - 120, py, "l", -1)
		self.sagB = self._SayfaDugme(p, W / 2.0 + 88, py, "r", 1)
		self.sayfaT = self._Txt(p, 14, C_ALT, W / 2.0, py + 18, "center")

		## alt bilgi + d\xfc\xf0meler
		ny = py + 66		# oklar 36 px (47 px doku 36'ya olceklenir); yazi oklardan belirgin uzak
		n1 = self._Txt(p, 15, C_ADK, W / 2.0, ny, "center")
		n2 = self._Txt(p, 15, C_ADK, W / 2.0, ny + 22, "center")
		if self.mod == "degistir":
			n1.SetText(y["degistir_not"])
			n2.SetText(y["degistir_not2"])
			by = ny + 44
			self.degB = self._Dugme(p, W / 2.0 - 214, by, 200, 38, ui.__mem_func__(self.__Degistir))
			self.degT = self._Txt(p, 17, C_DUGME, W / 2.0 - 114, by + 19, "center")
			self.degT.SetText(y["degistir"])
			self._Dugme(p, W / 2.0 + 14, by, 200, 38, ui.__mem_func__(self.Kapat))
			self._Txt(p, 17, C_KREM, W / 2.0 + 114, by + 19, "center").SetText(y["vazgec"])
		else:
			n1.SetText(y["hesap_not2"])
			by = ny + 26
			self._Dugme(p, W / 2.0 - 100, by, 200, 38, ui.__mem_func__(self.__Tamam))
			self._Txt(p, 17, C_DUGME, W / 2.0, by + 19, "center").SetText(y["tamam"])

	def _SayfaDugme(self, p, x, y, yon, adim):
		b = ui.Button()
		b.SetParent(p)
		b.SetUpVisual("mobile/ui/aet/pg_%s_up.png" % yon)
		b.SetOverVisual("mobile/ui/aet/pg_%s_up.png" % yon)
		b.SetDownVisual("mobile/ui/aet/pg_%s_down.png" % yon)
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, 36 / 47.0, 36 / 47.0)
		b.SetPosition(int(round(x)), int(round(y)))
		b.SetEvent(lambda a=adim: self.__Sayfa(a))
		b.Show()
		self.keep.append(b)
		return b

	# ---------------- olaylar
	def __AraOdak(self):
		self.ara.SetFocus()
		try:
			import ime
			ime.SetCursorPosition(100000)
		except:
			pass

	def __Suz(self):
		q = _Sade(self.ara.GetText().strip())
		if q:
			self.liste = [u for u in bayrakveri.ULKE if q in _Sade(u[1]) or q in _Sade(u[2]) or u[0] == q]
		else:
			self.liste = list(bayrakveri.ULKE)
		self.sayfa = 0
		self.__Ciz()

	def __Sayfa(self, adim):
		n = self.__SayfaSay()
		self.sayfa = max(0, min(n - 1, self.sayfa + adim))
		self.__Ciz()

	def __SayfaSay(self):
		return max(1, (len(self.liste) + SUTUN * SATIR - 1) / (SUTUN * SATIR))

	def __Hucre(self, i):
		kod = self.hucre[i]["kod"]
		if kod:
			self.sec = kod
			self.__Ciz()

	def __Ciz(self):
		y = Y()
		bas = self.sayfa * SUTUN * SATIR
		for (i, o) in enumerate(self.hucre):
			j = bas + i
			if j < len(self.liste):
				u = self.liste[j]
				o["kod"] = u[0]
				o["bay"].LoadImage(Yol(u[0]))
				o["bay"].SetScale(54 / 96.0, 36 / 64.0)
				ad = u[1] if dil.Mevcut() == "tr" else u[2]
				if len(ad) > 11:		# 14 px yazi hucreye (86 px) ~11 harf sigar
					ad = ad[:10] + ".."
				o["ad"].SetText(ad)
				on = u[0] == self.sec
				for n in ("zemin", "bay", "ad", "cerceve", "hit"):
					o[n].Show()
				for n in ("sec1", "sec2", "parla", "tik"):
					if on:
						o[n].Show()
					else:
						o[n].Hide()
				if on:
					o["cizgi"].Hide()
					o["ad"].SetPackedFontColor(C_KREM)
				else:
					o["cizgi"].Show()
					o["ad"].SetPackedFontColor(C_ADK)
				if self.mod == "degistir" and u[0] == self.mevcut:
					o["yesil"].Show()
				else:
					o["yesil"].Hide()
			else:
				o["kod"] = None
				for n in ("zemin", "cizgi", "sec1", "sec2", "parla", "cerceve", "bay", "ad", "tik", "yesil", "hit"):
					o[n].Hide()
		self.bosT.SetText(y["bos"] if not self.liste else "")
		self.sayfaT.SetText(y["sayfa"] % (self.sayfa + 1, self.__SayfaSay()))
		## \xfcst kutu
		if self.mod == "degistir":
			self.__Yan(self.mBay, self.mAd, self.mevcut, 22 + (W - 44) * 0.25)
			farkli = self.sec != self.mevcut
			if farkli:
				self.__Yan(self.yBay, self.yAd, self.sec, 22 + (W - 44) * 0.75)
				self.yBay.Show()
			else:
				self.yBay.Hide()
				self.yAd.SetText("-")
				self.yAd.SetPosition(int(22 + (W - 44) * 0.75), 97)
			self.degT.SetPackedFontColor(C_DUGME if farkli else C_KAPALI)
		else:
			self.__Yan(self.oBay, self.oAd, self.sec, W / 2.0)

	def __Yan(self, bay, adT, kod, cx):
		"""bayrak + ad yan yana, cx etraf\xfdnda ortal\xfd"""
		ad = Ad(kod)
		adT.SetText(ad)
		try:
			tw = adT.GetTextSize()[0] + len(ad)		# GetTextSize harf ba\xfe\xfd kesik (+1 px/harf)
		except:
			tw = len(ad) * 8
		top = 45 + 8 + tw
		x = cx - top / 2.0
		bay.LoadImage(Yol(kod))
		bay.SetScale(45 / 96.0, 30 / 64.0)
		bay.SetPosition(int(round(x)), bay.GetLocalPosition()[1])
		adT.SetPosition(int(round(x + 53)), adT.GetLocalPosition()[1])

	def __Tamam(self):
		kod = self.sec
		self.Kapat()
		if self.bitti:
			try:
				self.bitti(kod)
			except:
				import dbg, traceback
				dbg.TraceError("uibayrak bitti: " + traceback.format_exc())

	def __Degistir(self):
		"""onay kutusu pencerenin KEND\xdd katman\xfdnda (k\xf6k TOP_MOST dokunu\xfeu yutar; uiCommon.QuestionDialog altta kal\xfdrd\xfd)"""
		if self.sec == self.mevcut:
			return
		self.__OnayIptal()
		y = Y()
		ow, oh = 440, 196
		perde = _Hit()		# kutu d\xfd\xfe\xfdna dokunu\xfelar\xfd yutar (\xf6nce eklenir: sonra eklenen kutu \xfcstte kal\xfdr)
		perde.SetParent(self.kok)
		perde.SetPosition(0, 0)
		perde.SetSize(int(self.sw), int(self.sh))
		perde.Show()
		self.keep.append(perde)
		o = ui.Window()
		o.SetParent(self.kok)
		o.SetPosition(int(round((self.sw - ow) / 2.0)), int(round((self.sh - oh) / 2.0)))
		o.SetSize(ow, oh)
		o.Show()
		self.keep.append(o)
		self._Board(o, ow, oh)
		metin = y["onay"] % Ad(self.sec)
		i = metin.find(". ")
		(s1, s2) = (metin[:i + 1], metin[i + 2:]) if i > 0 else (metin, "")
		self._Txt(o, 15, C_KREM, ow / 2.0, 58, "center").SetText(s1)
		self._Txt(o, 15, C_KREM, ow / 2.0, 82, "center").SetText(s2)
		self._Dugme(o, 44, 124, 166, 38, ui.__mem_func__(self.__Onay))
		self._Txt(o, 17, C_DUGME, 44 + 83, 143, "center").SetText("Evet" if dil.Mevcut() == "tr" else "Yes")
		self._Dugme(o, 230, 124, 166, 38, ui.__mem_func__(self.__OnayIptal))
		self._Txt(o, 17, C_KREM, 230 + 83, 143, "center").SetText("Hay\xfdr" if dil.Mevcut() == "tr" else "No")
		self.soru = (o, perde)

	def __Onay(self):
		self.__OnayIptal()
		net.SendChatPacket("/bayrak degistir " + self.sec)		# sunucu nesneyi harcar, "bayrak_tamam" d\xf6ner

	def __OnayIptal(self):
		if self.soru:
			for w in self.soru:
				try:
					w.Hide()
				except:
					pass
			self.soru = None

	def Kapat(self):
		self.__OnayIptal()
		try:
			self.ara.KillFocus()
		except:
			pass
		try:
			self.kok.Hide()
		except:
			pass
		self.keep = []
		self.hucre = []


def _Sade(s):
	"""arama: b\xfcy\xfck/k\xfc\xe7\xfck ve T\xfcrk\xe7e harf duyars\xfdz (cp1254 bayt dizgesi)"""
	s = s.lower()
	for (a, b) in (("\xfd", "i"), ("\xdd", "i"), ("\xfe", "s"), ("\xde", "s"), ("\xf0", "g"), ("\xd0", "g"), ("\xfc", "u"), ("\xdc", "u"),
			("\xf6", "o"), ("\xd6", "o"), ("\xe7", "c"), ("\xc7", "c"), ("\xe2", "a"), ("\xee", "i"), ("\xfb", "u")):
		s = s.replace(a, b)
	return s


# ------------------------------------------------------------------ karakter olu\xfeturma d\xfc\xf0mesi
class OlusturDugmesi(_Parca):
	"""karakter olu\xfeturma ekran\xfdn\xfdn sa\xf0 alt\xfdnda: se\xe7ili bayrak + "Bayrak Se\xe7"; hesab\xfdn bayra\xf0\xfd varsa kilitli"""

	def __init__(self):
		self.keep = []
		self.pen = None
		self.kilit = HesapBayragi()
		self.sec = self.kilit or "tr"
		sw = float(wndMgr.GetScreenWidth())
		sh = float(wndMgr.GetScreenHeight())
		kok = _Kok(False)
		bw, bh = 236, 46
		kok.SetSize(bw, bh)
		kok.SetPosition(int(sw - bw - 40), int(sh - bh - 58))
		kok.Show()
		self.keep.append(kok)
		self.kok = kok
		self._Dugme(kok, 0, 0, bw, bh, ui.__mem_func__(self.__Tik))
		self.bay = self._Img(kok, Yol(self.sec), 34, (bh - 22) / 2.0, 33 / 96.0, 22 / 64.0)
		self.yazi = self._Txt(kok, 17, C_DUGME, 78, bh / 2.0)
		self.__Ciz()

	def __Ciz(self):
		self.bay.LoadImage(Yol(self.sec))
		self.bay.SetScale(33 / 96.0, 22 / 64.0)
		self.yazi.SetText(Y()["hesap_bayrak"] if self.kilit else Y()["sec"])

	def __Tik(self):
		if self.kilit:
			try:
				import uiCommon
				pd = uiCommon.PopupDialog()
				pd.SetText(Y()["kilit"] % Ad(self.kilit))
				try:		# uzun yazi kutuya sigsin: kutuyu yazi genisligine gore genislet (eski APK dar olcer: +1 px/harf)
					tw = pd.message.GetTextSize()[0] + len(Y()["kilit"])
					if tw + 60 > pd.GetWidth():
						pd.SetWidth(tw + 60)
				except:
					pass
				pd.Open()
				self.keep.append(pd)
			except:
				pass
			return
		if self.pen:
			self.pen.Kapat()
		self.pen = BayrakPenceresi("olustur", self.sec, ui.__mem_func__(self.__Secildi))

	def __Secildi(self, kod):
		self.sec = kod
		self.pen = None
		self.__Ciz()

	def Bitti(self):
		"""karakter olu\xfeturuldu: se\xe7im (kilitli de\xf0ilse) bekleyene yaz\xfdl\xfdr -> oyuna girince sunucuya"""
		if self.kilit or not HESAP[0]:
			return
		d = _Oku(BEKLEYEN)
		d[HESAP[0]] = self.sec
		_Yaz(BEKLEYEN, d)

	def Kapat(self):
		if self.pen:
			self.pen.Kapat()
			self.pen = None
		try:
			self.kok.Hide()
		except:
			pass
		self.keep = []


_PEN = [None]
_OLUSTUR = [None]


def DegistirAc():
	"""71182 nesnesine iki kez dokununca (uiinventory)"""
	try:
		Kapat()
		_PEN[0] = BayrakPenceresi("degistir", HesapBayragi() or "tr")
	except:
		import dbg, traceback
		dbg.TraceError("uibayrak DegistirAc: " + traceback.format_exc())


def Kapat():
	w = _PEN[0]
	_PEN[0] = None
	if w:
		w.Kapat()


def OlusturAc(hid=None):
	try:
		Hesap(hid)
		OlusturKapat()
		_OLUSTUR[0] = OlusturDugmesi()
	except:
		import dbg, traceback
		dbg.TraceError("uibayrak OlusturAc: " + traceback.format_exc())


def OlusturBitti():
	try:
		if _OLUSTUR[0]:
			_OLUSTUR[0].Bitti()
	except:
		import dbg, traceback
		dbg.TraceError("uibayrak OlusturBitti: " + traceback.format_exc())


def OlusturKapat():
	w = _OLUSTUR[0]
	_OLUSTUR[0] = None
	if w:
		w.Kapat()
