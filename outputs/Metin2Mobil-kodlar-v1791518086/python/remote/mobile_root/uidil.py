# -*- coding: utf-8 -*-
# MOBIL - mobile_root/uidil.py: \xddLK A\xc7ILI\xde D\xddL SE\xc7\xddM\xdd penceresi (T\xfcrk\xe7e / English).
# \xdcRET\xddL\xddR: tools/dil/uidil_kaynak.py (UTF-8) -> tools/dil/gen_uidil.py -> bu dosya (cp1254 ka\xe7\xfd\xfel\xfd ASCII).
#
# KULLANICI (2026-10-06): prototip Desktop/Averos2-Dil-Prototip/dil.html onayland\xfd. Oyun ilk a\xe7\xfdld\xfd\xf0\xfdnda giri\xfe ekran\xfdnda,
# giri\xfe panelinin yerinde klasik pencere: bayrakl\xfd iki se\xe7enek (English yan\xfdnda "Ortak dil" rozeti), se\xe7ince penceredeki
# yaz\xfdlar o dile d\xf6ner, "Devam" ile pack/dil.cfg'ye kaydedilir (dil.py), bir daha sorulmaz (Ayarlar'dan de\xf0i\xfeir).
# Giri\xfe ekran\xfdn\xfdn (uimobilelogin.LoginSkin) arka plan\xfd ve logosu altta g\xf6r\xfcn\xfcr; pencere EN \xdcSTTE (TOP_MOST), dokunu\xfeu yutar.
# KULLANICI (2026-10-06, telefonda denedi): "pencere yapmak yerine sunucu ve kanal se\xe7 ekran\xfdna koysak; t\xfdklay\xfdnca o pencere
#   gelse" -> sunucu ekran\xfdnda "Dil \xb7 Language" kart\xfd (uimobilelogin __BuildDil), dokununca bu pencere MODAL a\xe7\xfdl\xfdr (ekran
#   ortas\xfdnda, karartma + kare \xe7arp\xfd ile kapan\xfdr, "Devam" kaydeder). Otomatik ilk a\xe7\xfdl\xfd\xfe penceresi kullan\xfdlm\xfdyor (IlkAcilis
#   duruyor ama \xe7a\xf0r\xfdlm\xfdyor); varsay\xfdlan dil dil.Oneri().
import ui
import wndMgr
import app
import dil

DIR = "mobile/ui/dil/"
LOGIN = "mobile/ui/login/"
PT = "d:/ymir work/ui/pattern/"
PUB = "d:/ymir work/ui/public/"
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")
TASMA = 0.02
DW, DH = 1356.0, 610.0			# giri\xfe tasar\xfdm\xfd (mobileloginskin.DESIGN_W / H)
PANEL = (848, 38, 452, 542)		# giri\xfe paneli (mobileloginskin ANCHORS login_panel) - pencere bunun ortas\xfdnda
BRAND = (46, 12, 518, 235)		# logo (RECTS brand; brand.png 2x)
W, H = 460, 400				# pencere (prototip px = mant\xfdksal px)

C_KREM = 0xfff1e6c0
C_ALTIN = 0xffe8d08a
C_ALT = 0xffc9b88f
C_KAPALI = 0xff8f8470
C_KOYU = 0xff1b1206
C_BASLIK = 0xfffeedc6

YAZI = {
	"tr": {"soru": "Oynamak istedi\xf0in dili se\xe7", "soru2": "Choose your language", "not": "Bunu daha sonra Ayarlar'dan de\xf0i\xfetirebilirsin.",
		"devam": "Devam", "trAlt": "T\xfcrkiye", "enAlt": "Global", "rozet": "Ortak dil"},
	"en": {"soru": "Choose your language", "soru2": "Oynamak istedi\xf0in dili se\xe7", "not": "You can change this later in Settings.",
		"devam": "Continue", "trAlt": "Turkey", "enAlt": "Global", "rozet": "Common language"},
}


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
	"""tam ekran, en \xfcst: dokunu\xfeu yutar (giri\xfe ekran\xfdna ge\xe7mez)"""

	def __init__(self):
		ui.Window.__init__(self, "TOP_MOST")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		return True

	def OnMouseLeftButtonUp(self):
		return True

	def OnPressEscapeKey(self):
		return True


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


class DilSecimi(object):

	def __init__(self, bitti=None, modal=False):
		self.bitti = bitti
		self.modal = modal
		self.keep = []
		self.sec = dil.Mevcut() if (modal and dil.Secildi()) else dil.Oneri()
		self.sw = float(wndMgr.GetScreenWidth())
		self.sh = float(wndMgr.GetScreenHeight())
		self.k = min(self.sw / DW, self.sh / DH)
		self.oy = (self.sh - DH * self.k) / 2.0
		self.__Kur()
		self.__Ciz()

	# ---------------- yard\xfdmc\xfdlar (pencere i\xe7i koordinat = mant\xfdksal px)
	def _Img(self, parent, path, x, y, sx=1.0, sy=1.0):
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(path)
		max(0, 0)
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
		"""y = yaz\xfdn\xfdn dikey ortas\xfd"""
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

	# ---------------- kurulum
	def __Kur(self):
		sw, sh, k = self.sw, self.sh, self.k
		kok = _Kok()
		kok.SetSize(int(sw), int(sh))
		kok.SetPosition(0, 0)
		kok.Show()
		self.keep.append(kok)
		self.kok = kok
		if self.modal:
			self._Rect(kok, 0, 0, sw, sh, 0x99000000)		# sunucu ekran\xfd \xfcst\xfcnde karartma
			x0 = int(round((sw - W) / 2.0))
			y0 = int(round((sh - H) / 2.0))
			self.__Pencere(kok, x0, y0)
			return
		## giri\xfe ekran\xfdn\xfdn arka plan\xfd (dura\xf0an resim; kaplama) + logo: giri\xfe paneli yokmu\xfe gibi
		bg = ui.ExpandedImageBox()
		bg.SetParent(kok)
		bg.AddFlag("not_pick")
		bg.LoadImage(LOGIN + "bg_login.jpg")
		max(0, 0)
		bw = float(max(1, bg.GetWidth()))
		bh = float(max(1, bg.GetHeight()))
		s = max(sw / bw, sh / bh)
		bg.SetScale(s, s)
		bg.SetPosition(int(round((sw - bw * s) / 2.0)), int(round((sh - bh * s) / 2.0)))
		bg.Show()
		self.keep.append(bg)
		self._Rect(kok, 0, 0, sw, sh, 0x38000000)
		(bx, by, bww, bhh) = BRAND
		self._Img(kok, LOGIN + "brand.png", bx * k, self.oy + by * k, bww * k / 1036.0, bww * k / 1036.0)
		## pencere: giri\xfe panelinin ortas\xfdnda
		(px, py, pw, ph) = PANEL
		pX = sw - (DW - px) * k
		pY = self.oy + py * k
		x0 = int(round(pX + (pw * k - W) / 2.0))
		y0 = int(round(pY + (ph * k - H) / 2.0))
		self.__Pencere(kok, x0, y0)

	def __Pencere(self, kok, x0, y0):
		p = ui.Window()
		p.SetParent(kok)
		p.SetPosition(x0, y0)
		p.SetSize(W, H)
		p.Show()
		self.keep.append(p)
		self.pen = p
		self.__Board(p)
		self.__Baslik(p)
		if self.modal:		# kare \xe7arp\xfd (envanterle ayn\xfd): kaydetmeden kapat\xfdr
			c = 23 * 1.6 * 1.15
			cb = ui.Button()
			cb.SetParent(p)
			cb.SetUpVisual("mobile/ui/minimap/btn_close_sq.png")
			cb.SetOverVisual("mobile/ui/minimap/btn_close_sq.png")
			cb.SetDownVisual("mobile/ui/minimap/btn_close_sq_down.png")
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(cb.hWnd, c / 64.0, c / 64.0)
			cb.SetPosition(int(round(8 + W - 15 - c)), int(round(7 + (23 * 1.6 - c) / 2.0)))
			cb.SetEvent(ui.__mem_func__(self.Kapat))
			cb.Show()
			self.keep.append(cb)
			hb = _Hit()
			hb.SetParent(p)
			hb.SetPosition(int(round(8 + W - 15 - c - 8)), 0)
			hb.SetSize(int(round(c + 16)), 52)
			hb.onUp = ui.__mem_func__(self.Kapat)
			hb.Show()
			self.keep.append(hb)
		self.soruT = self._Txt(p, 18, C_ALTIN, W / 2.0, 72, "center")
		self.soru2T = self._Txt(p, 14, C_ALT, W / 2.0, 96, "center")
		self.sec_ = {}
		for (d, y, bayrak, ad) in (("tr", 116, "flag_tr.png", "T\xfcrk\xe7e"), ("en", 216, "flag_en.png", "English")):
			o = {}
			o["zemin"] = self._Rect(p, 24, y, 412, 92, 0x80000000)
			o["cizgi"] = self._Rect(p, 24, y, 412, 92, 0xff3d342a, False)
			o["sec1"] = self._Rect(p, 24, y, 412, 92, 0xfff2c94c, False)
			o["sec2"] = self._Rect(p, 25, y + 1, 410, 90, 0x99f2c94c, False)
			o["parla"] = self._Rect(p, 26, y + 2, 408, 88, 0x22f2c94c)
			self._Rect(p, 41, y + 21, 74, 50, 0xff6b5a3e)		# bayrak \xe7er\xe7evesi
			self._Img(p, DIR + bayrak, 42, y + 22, 0.5, 0.5)
			t = self._Txt(p, 20, C_KREM, 134, y + 32)
			t.SetText(ad)
			o["alt"] = self._Txt(p, 14, C_ALT, 134, y + 62)
			o["roff"] = self._Img(p, DIR + "radio_off.png", 390, y + 31, 0.5, 0.5)
			o["ron"] = self._Img(p, DIR + "radio_on.png", 390, y + 31, 0.5, 0.5)
			if d == "en":
				o["rozetB"] = self._Rect(p, 256, y + 36, 120, 20, C_ALTIN)
				o["rozetK"] = self._Rect(p, 256, y + 36, 120, 20, 0xfffff3c4, False)
				o["rozetT"] = self._Txt(p, 12, C_KOYU, 316, y + 46, "center", False)
			h = _Hit()
			h.SetParent(p)
			h.SetPosition(24, y)
			h.SetSize(412, 92)
			h.onUp = lambda d0=d: self.__Sec(d0)
			h.Show()
			self.keep.append(h)
			self.sec_[d] = o
		self.notT = self._Txt(p, 13, C_KAPALI, W / 2.0, 330, "center")
		b = ui.Button()
		b.SetParent(p)
		b.SetUpVisual(PUB + "large_button_01.sub")
		b.SetOverVisual(PUB + "large_button_02.sub")
		b.SetDownVisual(PUB + "large_button_03.sub")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, 220 / 88.0, 40 / 21.0)
		b.SetPosition(120, 344)
		b.SetEvent(ui.__mem_func__(self.__Devam))
		b.Show()
		self.keep.append(b)
		self.devamT = self._Txt(p, 19, 0xffffe08a, W / 2.0, 363, "center")

	def __Board(self, p):
		self._Tile(p, PT + "board_base.tga", 32, 32, W - 64, H - 64, 128, 128)
		self._Tile(p, PT + "board_line_top.tga", 32, 0, W - 64, 32, 128, 32)
		self._Tile(p, PT + "board_line_bottom.tga", 32, H - 32, W - 64, 32, 128, 32)
		self._Tile(p, PT + "board_line_left.tga", 0, 32, 32, H - 64, 32, 128)
		self._Tile(p, PT + "board_line_right.tga", W - 32, 32, 32, H - 64, 32, 128)
		for (n, cx, cy) in (("lefttop", 0, 0), ("righttop", W - 32, 0), ("leftbottom", 0, H - 32), ("rightbottom", W - 32, H - 32)):
			self._Tile(p, PT + "board_corner_%s.tga" % n, cx, cy, 32, 32, 32, 32)

	def __Baslik(self, p):
		"""envanterin geni\xfe ba\xfel\xfdk \xe7ubu\xf0u (titlebar sol + orta x1.6); kapatma YOK (dil se\xe7ilmeden ge\xe7ilmez)"""
		x, y, w = 8, 7, W - 15
		bh = 23 * 1.6
		bw = 32 * 1.6
		self._Tile(p, PT + "titlebar_left.tga", x, y, bw, bh, 32, 32, 1.6, 1.6)
		self._Tile(p, PT + "titlebar_center.tga", x + bw, y, w - bw, bh, 32, 32, 1.6, 1.6)
		t = self._Txt(p, 20, C_BASLIK, 36, y + bh / 2.0 - 1)
		t.SetText("Dil \xb7 Language")

	# ---------------- olaylar
	def __Sec(self, d):
		self.sec = d
		self.__Ciz()

	def __Ciz(self):
		y = dil_yazi = YAZI[self.sec]
		self.soruT.SetText(y["soru"])
		self.soru2T.SetText(y["soru2"])
		self.notT.SetText(y["not"])
		self.devamT.SetText(y["devam"])
		self.sec_["tr"]["alt"].SetText(y["trAlt"])
		self.sec_["en"]["alt"].SetText(y["enAlt"])
		self.sec_["en"]["rozetT"].SetText(y["rozet"])
		# rozet geni\xfeli\xf0i yaz\xfdya g\xf6re (GetTextSize harf ba\xfe\xfd kesik: +1 px/harf, bkz. APK_BEKLEYENLER 6)
		try:
			tw = self.sec_["en"]["rozetT"].GetTextSize()[0] + len(y["rozet"]) + 16
		except:
			tw = 120
		for n in ("rozetB", "rozetK"):
			r = self.sec_["en"][n]
			r.SetSize(int(tw), 20)
			r.SetPosition(int(376 - tw), r.GetLocalPosition()[1])
		self.sec_["en"]["rozetT"].SetPosition(int(376 - tw / 2.0), self.sec_["en"]["rozetT"].GetLocalPosition()[1])
		for (d, o) in self.sec_.items():
			on = d == self.sec
			for n in ("sec1", "sec2", "parla", "ron"):
				if on:
					o[n].Show()
				else:
					o[n].Hide()
			if on:
				o["roff"].Hide()
				o["cizgi"].Hide()
			else:
				o["roff"].Show()
				o["cizgi"].Show()

	def __Devam(self):
		dil.Kaydet(self.sec)
		self.Kapat()
		if self.bitti:
			try:
				self.bitti(self.sec)
			except:
				import dbg, traceback
				dbg.TraceError("uidil bitti: " + traceback.format_exc())

	def Kapat(self):
		try:
			self.kok.Hide()
		except:
			pass
		self.keep = []
		self.sec_ = {}


_PEN = [None]


def IlkAcilis(bitti=None):
	"""dil daha \xf6nce se\xe7ilmediyse se\xe7im penceresini a\xe7ar. D\xf6ner: a\xe7\xfdld\xfd m\xfd"""
	try:
		if dil.Secildi():
			return False
		if _PEN[0] is None:
			_PEN[0] = DilSecimi(bitti)
		return True
	except:
		import dbg, traceback
		dbg.TraceError("uidil: " + traceback.format_exc())
		return False


def Ac(bitti=None):
	"""sunucu ekran\xfdndaki Dil kart\xfd: pencereyi MODAL a\xe7ar (se\xe7ili dil i\xfearetli)"""
	try:
		Kapat()
		_PEN[0] = DilSecimi(bitti, True)
		return True
	except:
		import dbg, traceback
		dbg.TraceError("uidil Ac: " + traceback.format_exc())
		return False


def Kapat():
	w = _PEN[0]
	_PEN[0] = None
	if w:
		w.Kapat()
