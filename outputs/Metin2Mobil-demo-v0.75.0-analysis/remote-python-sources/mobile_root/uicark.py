# -*- coding: utf-8 -*-
# MOBIL - mobile_root/uicark.py: G\xdcNL\xdcK \xdeANS \xc7ARKI penceresi (v2: \xf6d\xfcl tablosu SUNUCUDAN / kontrol panelinden).
# \xdcRET\xddL\xddR: tools/cark/uicark_kaynak.py (UTF-8) -> tools/cark/gen_uicark.py -> bu dosya (cp1254 ka\xe7\xfd\xfel\xfd ASCII).
#
# KULLANICI (2026-10-03): prototip Desktop/Averos2-Cark-Prototip/cark.html v2, b\xfcy\xfck hali; "FPS'i d\xfc\xfe\xfcnerek, donma/kasmaya
#   kar\xfe\xfd b\xfct\xfcn korumay\xfd yap" -> sonra "kontrol panelinde \xc7ark\xfd D\xfczenle: \xfcr\xfcn ekle/kald\xfdr (en fazla 10), \xfeans %, nadirlik,
#   g\xfcnl\xfck seri hediyesi". \xd6d\xfcl tablosu sunucudaki panel dosyas\xfdndan (server/quest/sans_carki.lua -> Cark2Ayar/Cark2Odul/
#   Cark2Grup); gelene kadar carkveri.py varsay\xfdlan\xfd. Dilim say\xfds\xfd 2..10: disk zemini dilim say\xfds\xfdna g\xf6re pi\xfemi\xfe doku
#   (disk<N>), nadirlik yay\xfd / yuva / ikon / etiket her dilim i\xe7in ayr\xfd par\xe7a (ikon ve ad oyunun KEND\xdd e\xfeya bilgisinden).
# \xd6l\xe7\xfc: prototip px; oyunda 1 px = z mant\xfdksal px (z = 1.28 x ekran y\xfcksekli\xf0i / 705, s\xfd\xf0mazsa k\xfc\xe7\xfcl\xfcr). Dokular 2.25x.
# HIZ / DONMA KORUMASI:
#   - pencere ilk A\xc7ILI\xdeTA kurulur; kapal\xfdyken OnUpdate hi\xe7 \xe7al\xfd\xfemaz; dilim par\xe7alar\xfd yaln\xfdz tablo de\xf0i\xfeince kurulur
#   - d\xf6nerken kare ba\xfe\xfd ~80 hafif \xe7a\xf0r\xfd (disk + dilim par\xe7alar\xfd), dururken 0; \xfd\xfe\xfdklar 90 ms'de bir, yaz\xfdlar yaln\xfdz de\xf0i\xfeince
#   - sunucu 8 sn yan\xfdt vermezse \xe7ark kendili\xf0inden durur; \xe7evirme iste\xf0i en s\xfdk 1.5 sn'de bir; komutlar try/except i\xe7inde
import math
import ui
import wndMgr
import app
import carkveri as V
import carkgeom as G

DIR = "mobile/ui/cark/"
PT = "d:/ymir work/ui/pattern/"
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")
REF_H = 705.0
ZOOM = 1.28			# KULLANICI: "b\xfcy\xfck halini" (1.15) -> telefonda "k\xfc\xe7\xfck kalm\xfd\xfe, hafif b\xfcy\xfcs\xfcn, i\xe7erik okunsun"
FONT_BOOST = 1.12		# oyun fontu ince: yaz\xfdlar ayr\xfdca b\xfcy\xfcr
FONT_MAX = 18			# motor yaz\xfdy\xfd en \xe7ok 32 px pi\xfeirir (bkz. uihedefkarti)
DPR = float(G.DPR)
ROT_EPS = 0.001

# ---- \xf6l\xe7\xfcler (prototip px, cark.html v2) ----
W_WIN, H_WIN = 756, 515
TB_X, TB_Y, TB_W, TB_H = 8, 8, 740, 23
UST = (12, 39, 732, 50)
CX, CY = 180, 263		# \xe7ark merkezi
R_IK, R_ET = 104.0, 66.0	# ikon / etiket yar\xfd\xe7ap\xfd (etiket dik durur: yan dilimde g\xf6bek 46 ile yuva 85 aras\xfdna s\xfd\xf0s\xfdn)
ET_MAXW = 36.0			# etiket bundan geni\xfese k\xfc\xe7\xfck yaz\xfd (prototip px)
LIST = (356, 131, 386, 204)
DET = (356, 341, 386, 88)
TAB_X, TAB_Y, TAB_W, TAB_GAP = 356, 97, 126, 4
CEVIR_X, CEVIR_Y = 14, 435
SURE = (174, 435, 568, 40)
SERIT = (12, 481, 732, 24)
ROW_H = 19
ROW_N = 10
R_ISIK = 160.0
POP_W, POP_H = 300, 252
KUR_W, KUR_H = 380, 289
# v78 (2026-10-08) ORANLAR: d\xfc\xf0me \xe7ark halkas\xfdn\xfdn sol \xfcst bo\xfelu\xf0unda (k\xf6\xfeesi halka merkezinden 171 px: g\xf6r\xfcnen halka
# ~166 px, \xfd\xfe\xfdklar 164 px -> \xe7ak\xfd\xfemaz); pencere her \xf6d\xfcl\xfcn y\xfczdesini A\xd0IRLIKLARDAN hesaplar (sunucu sans_carki.sec ile
# ayn\xfd kural: normal g\xfcn w / toplam; 7. g\xfcn garanti a\xe7\xfdksa yaln\xfdz Nadir+ aras\xfdnda). Dokular tools/cark/bake_oran.py.
ORAN_BTN = (12, 95)
ORAN_W, ORAN_H = 420, 384
ORAN_KUTU = (14, 40, 392, 232)
ORAN_Y0, ORAN_DY = 66, 20
ORAN_X = (24, 44, 232, 330, 396)		# ikon / ad / nadirlik / \xfeans (sa\xf0a) / 7. g\xfcn (sa\xf0a)
ORAN_AD_MAXW = 182.0
NAD_EN = ("Common", "Rare", "Legendary")

# ---- renkler ----
C_CREAM = 0xfff1e6c0
C_SUB = 0xffc9b88f
C_OFF = 0xff8f8470
C_GOLD = 0xffe8d08a
C_OK = 0xff8fd16a
C_BAD = 0xffff7b5c
C_FILL = 0xa60b0805
C_LINE = 0xff5a4630
NADR = (0xffd9cfb4, 0xff6fb7ff, 0xffffb347)
NAD = ("S\xfdradan", "Nadir", "Efsanevi")
HALE = ((1.0, 0.84, 0.43), (0.44, 0.72, 1.0), (1.0, 0.67, 0.24))
HATA = {1: "Bu hesab\xfdn g\xfcnl\xfck hakk\xfd kullan\xfdld\xfd, s\xfcre dolunca tekrar \xe7evir.", 2: "Envanterin dolu \x97 \xf6d\xfcl i\xe7in yer a\xe7.",
	4: "\xc7ark bilgisi gelmedi \x97 karakter se\xe7imine \xe7\xfdk\xfdp tekrar gir.",
	3: "\xd6nceki \xf6d\xfcl\xfcn veriliyor, birka\xe7 saniye bekle."}


def _clamp(v, a, b):
	return a if v < a else (b if v > b else v)


def _Dil():
	try:
		import dil
		return dil.Mevcut()
	except:
		return "tr"


def _Y(tr, en):
	"""v78 Oranlar penceresi yaz\xfdlar\xfd iki dilli do\xf0rudan (iki dilli kural; ceviri.py tablosuna ba\xf0l\xfd de\xf0il)."""
	return en if _Dil() == "en" else tr


def _Yuzde(v):
	"""16 -> "%16" (TR) / "16%" (EN); k\xfc\xe7\xfck de\xf0erler 2 ondal\xfdk (grup e\xfeyas\xfd %0.17)"""
	v = max(0.0, float(v))
	s = ("%.2f" % v) if v < 1.0 else ("%.1f" % v)
	s = s.rstrip("0").rstrip(".") if "." in s else s
	if s in ("", "0") and v > 0.0:
		s = "<0.01"
	return _Y("%" + s, s + "%")


def _ease_out4(p):
	q = 1.0 - _clamp(p, 0.0, 1.0)
	return 1.0 - q * q * q * q


def _sure(sn):
	sn = max(0, int(sn))
	return "%02d:%02d:%02d" % (sn // 3600, (sn % 3600) // 60, sn % 60)


def _once(yas):
	yas = max(0, int(yas))
	if yas < 60:
		return "Az \xf6nce"
	if yas < 3600:
		return "%d dk \xf6nce" % (yas // 60)
	if yas < 86400:
		return "%d saat \xf6nce" % (yas // 3600)
	return "%d g\xfcn \xf6nce" % (yas // 86400)


def _nokta(n):
	s = str(abs(int(n)))
	out = ""
	while len(s) > 3:
		out = "." + s[-3:] + out
		s = s[:-3]
	return s + out


def _kisa(n):
	"""10000000 -> 10M, 500000 -> 500K"""
	n = int(n)
	if n >= 1000000 and n % 100000 == 0:
		return ("%.1f" % (n / 1000000.0)).rstrip("0").rstrip(".") + "M"
	if n >= 1000 and n % 100 == 0:
		return ("%.1f" % (n / 1000.0)).rstrip("0").rstrip(".") + "K"
	return _nokta(n)


# e\xfeya bilgisi (ad, ikon yolu, a\xe7\xfdklama, (yuva eni, yuva boyu)) - oyunun kendi item_proto / itemdesc'inden, \xf6nbellekli
_ITEM = {}


def _Item(v):
	v = int(v)
	r = _ITEM.get(v)
	if r is not None:
		return r
	if v == 1:
		r = ("Yang", "icon/item/money.tga", "", (1, 1))
	else:
		try:
			import item
			item.SelectItem(v)
			try:
				(sw, sh) = item.GetItemSize()
				boy = (max(1, int(sw)), max(1, int(sh)))
			except:
				boy = (1, 1)
			r = (item.GetItemName() or ("#%d" % v), item.GetIconImageFileName() or "", item.GetItemDescription() or "", boy)
		except:
			r = ("#%d" % v, "", "", (1, 1))
	_ITEM[v] = r
	return r


def _AdetEt(v, a):
	return ("%s Yang" % _kisa(a)) if int(v) == 1 else ("x%d" % int(a))


# ------------------------------------------------------------------ sunucu verisi (pencere olmasa da tutulur)
def _Varsayilan():
	out = []
	for (tur, v, a, w, n, et, ad, g) in V.ODUL:
		out.append({"tur": tur, "v": v, "a": a, "w": w, "n": n, "et": et, "ad": ad, "g": list(g)})
	return out


class _Model(object):
	def __init__(self):
		self.qid = -1
		self.bqid = -1
		self.known = False
		self.readyAt = 0.0
		self.seri = 0
		self.bos = 0
		self.bek = 0
		self.gecmis = []		# (vnum, adet, nadir, mutlak zaman)
		self.kazanan = []		# (ad, vnum, adet, nadir)
		self.sig = 0
		self.lastAsk = -100.0
		# \xf6d\xfcl tablosu (sunucu g\xf6nderene kadar varsay\xfdlan)
		self.surum = -1
		self.bekleme = V.BEKLEME
		self.kopma = V.SERI_KOPMA
		self.garanti = V.GARANTI
		self.hv, self.ha = V.HEDIYE
		self.odul = _Varsayilan()
		self.cfgSig = 0
		self._yeni = None

	def Ready(self):
		return self.known and self.bek == 0 and app.GetTime() >= self.readyAt

	def N(self):
		return len(self.odul)

	def Sans(self, i):
		top = 0
		for o in self.odul:
			top += o["w"]
		return 100.0 * self.odul[i]["w"] / max(1, top)

	def Ad(self, i):
		o = self.odul[i]
		if o["ad"]:
			return o["ad"]
		if o["tur"] == 1:
			return "Yang"
		return _Item(o["v"])[0]

	def IkonV(self, i):
		"""dilimin ikonunu veren e\xfeya numaras\xfd (yang = 1)"""
		o = self.odul[i]
		return 1 if o["tur"] == 1 else o["v"]

	def Oranlar(self):
		"""v78: [(normal g\xfcn %, 7. g\xfcn %)] her \xf6d\xfcl i\xe7in. Sunucu quest'i (sans_carki.sec) ile AYNI kural: normal g\xfcn
		a\xf0\xfdrl\xfdk / toplam; 7. g\xfcn (seri 7) garanti a\xe7\xfdksa yaln\xfdz Nadir+ (n > 0) \xf6d\xfcller aras\xfdnda, onlar\xfdn toplam\xfd 0 ise
		normal da\xf0\xfdl\xfdm. A\xf0\xfdrl\xfdklar sunucudan gelen tablodan (Cark2Odul; gelene kadar carkveri varsay\xfdlan\xfd)."""
		top = 0
		top7 = 0
		for o in self.odul:
			top += max(0, o["w"])
			if o["n"] > 0:
				top7 += max(0, o["w"])
		out = []
		for o in self.odul:
			p = 100.0 * max(0, o["w"]) / max(1, top)
			if self.garanti and top7 > 0:
				p7 = (100.0 * max(0, o["w"]) / top7) if o["n"] > 0 else 0.0
			else:
				p7 = p
			out.append((p, p7))
		return out

	def Aciklama(self, i):
		o = self.odul[i]
		if o["tur"] == 1:
			return "%s Yang do\xf0rudan hesab\xfdna eklenir." % _nokta(o["a"])
		if o["tur"] == 2:
			adlar = [_Item(g)[0] for g in o["g"][:4]]
			s = "\xdeu %d e\xfeyadan rastgele biri: %s" % (len(o["g"]), ", ".join(adlar))
			return s + (", ..." if len(o["g"]) > 4 else ".")
		d = _Item(o["v"])[2]
		return d if d else "%s x%d envanterine eklenir." % (_Item(o["v"])[0], o["a"])


M = _Model()
_WND = [None]


def _txt(s):
	return "" if s == "-" else s.replace("_", " ")


def Cmd(name, *a):
	"""game.py sunucu komutlar\xfd -> burada. Hata oyunu durdurmas\xfdn."""
	try:
		t = app.GetTime()
		if name == "Cark2Qid":
			M.qid = int(a[0])
		elif name == "Cark2BilgiQid":
			M.bqid = int(a[0])
		elif name == "Cark2Ayar":
			n = int(a[1])
			if 2 <= n <= 10:
				M._yeni = {"surum": int(a[0]), "n": n, "bekleme": int(a[2]), "kopma": int(a[3]), "garanti": int(a[4]),
					"hv": int(a[5]), "ha": int(a[6]), "odul": [None] * n}
		elif name == "Cark2Odul":
			y = M._yeni
			i = int(a[0]) - 1
			if y and 0 <= i < y["n"]:
				y["odul"][i] = {"tur": int(a[1]), "v": int(a[2]), "a": int(a[3]), "w": int(a[4]), "n": _clamp(int(a[5]), 0, 2),
					"et": _txt(a[6]), "ad": _txt(a[7]), "g": []}
		elif name == "Cark2Grup":
			y = M._yeni
			i = int(a[0]) - 1
			if y and 0 <= i < y["n"] and y["odul"][i] is not None:
				y["odul"][i]["g"] = [int(x) for x in a[1].split(",") if x]
		elif name == "Cark2Durum":
			y = M._yeni
			M._yeni = None
			if y and None not in y["odul"]:		# tablo tam geldiyse uygula (yaln\xfdz de\xf0i\xfetiyse par\xe7alar yeniden kurulur)
				yeni = (y["surum"], y["bekleme"], y["kopma"], y["garanti"], y["hv"], y["ha"], repr(y["odul"]))
				if yeni != getattr(M, "_son", None):
					M._son = yeni
					M.surum = y["surum"]
					M.bekleme = max(60, y["bekleme"])
					M.kopma = y["kopma"]
					M.garanti = y["garanti"]
					M.hv, M.ha = y["hv"], y["ha"]
					M.odul = y["odul"]
					M.cfgSig += 1
			M.readyAt = t + int(a[0])
			M.seri = int(a[1])
			M.bos = int(a[2])
			M.bek = int(a[3])
			M.known = True
		elif name == "Cark2GecmisSil":
			M.gecmis = []
		elif name == "Cark2Gecmis":
			M.gecmis.append((int(a[0]), int(a[1]), _clamp(int(a[2]), 0, 2), t - int(a[3])))
		elif name == "Cark2KazananSil":
			M.kazanan = []
		elif name == "Cark2Kazanan":
			M.kazanan.append((a[0], int(a[1]), int(a[2]), _clamp(int(a[3]), 0, 2)))
		elif name == "Cark2Sonuc":
			w = _WND[0]
			M.readyAt = t + M.bekleme
			M.seri = int(a[3])
			M.bek = 1
			if w:
				w.OnResult(int(a[0]) - 1, int(a[1]), int(a[2]), int(a[4]), int(a[5]))
		elif name == "Cark2Hata":
			w = _WND[0]
			if w:
				w.OnError(int(a[0]))
		M.sig += 1
	except:
		import dbg
		dbg.TraceError("uicark.Cmd %s %r" % (name, a))


def Toggle():
	w = _WND[0]
	if w is None:
		w = _WND[0] = CarkWindow()
	if w.IsOpen():
		w.Close()
	else:
		w.Open()


def IsReady():
	return M.Ready()


def DestroyAll():
	w = _WND[0]
	_WND[0] = None
	if w:
		w.Destroy()


def _Ask(qid):
	if qid < 0:
		return False
	try:
		import event
		event.QuestButtonClick(-2147483648 + qid)
		return True
	except:
		import dbg
		dbg.TraceError("uicark: QuestButtonClick yok")
		return False


# ------------------------------------------------------------------ k\xfc\xe7\xfck pencereler
class _Root(ui.Window):
	"""kendi boyutunda k\xf6k: i\xe7indeki dokunu\xfeu yutar (d\xfcnyaya ge\xe7mez)."""

	def __init__(self):
		ui.Window.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		return True

	def OnMouseLeftButtonUp(self):
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


# ------------------------------------------------------------------ ana pencere
class CarkWindow(object):

	def __init__(self):
		self.built = False
		self.open = False
		self.keep = []
		self.slices = []
		self.sliceKeep = []
		self.cfgShown = -1
		self.tab = "odul"
		self.sel = 0
		self.state = "bos"		# bos / bekle / yavas
		self.ang = 0.0
		self.vel = 0.0
		self.t0 = 0.0
		self.tLast = 0.0
		self.dStart = 0.0
		self.dTotal = 0.0
		self.dDur = 0.0
		self.result = None
		self.err = ""
		self.errT = -1.0
		self.tickN = 0
		self.tickT = -1.0
		self.lightStep = -1
		self.blinkT = -1.0
		self.popT = -1.0
		self.lastSpinAsk = -100.0
		self.listSig = None
		self.statSig = None
		self.ticker = 0
		self.tickerT = 0.0
		self.secT = -1.0
		self.vurgu = -1

	def DIL(self):
		return 360.0 / max(1, M.N())

	# ---------------- \xf6l\xe7ek yard\xfdmc\xfdlar\xfd
	def __Scale(self):
		self.scrW = wndMgr.GetScreenWidth()
		self.scrH = wndMgr.GetScreenHeight()
		k = self.scrH / REF_H
		self.z = min(ZOOM * k, 0.98 * self.scrW / W_WIN, 0.97 * self.scrH / H_WIN)
		self.si = self.z / DPR

	def P(self, v):
		return int(round(v * self.z))

	def F(self, pt):
		return "Tahoma:%d" % max(8, min(FONT_MAX, int(round(pt * self.z * FONT_BOOST))))

	def _Img(self, parent, name, x, y, show=True, keep=None):
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(DIR + name + ".png")
		max(0, 0)	# LoadImage bekleyen hatas\xfdn\xfd burada tetikle
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		w.SetScale(self.si, self.si)
		w.SetPosition(self.P(x), self.P(y))
		if show:
			w.Show()
		(self.keep if keep is None else keep).append(w)
		return w

	def _PImg(self, parent, path, x, y, sx=1.0, sy=1.0):
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(path)
		max(0, 0)
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		w.SetScale(sx * self.z, sy * self.z)
		w.SetPosition(self.P(x), self.P(y))
		w.Show()
		self.keep.append(w)
		return w

	def _Tile(self, parent, path, x, y, w, h, tw, th, sx=1.0, sy=1.0):
		img = self._PImg(parent, path, x, y, sx, sy)
		if HAS_RRS:
			img.SetRenderingRect(0.0, 0.0, w / (tw * sx) - 1.0, h / (th * sy) - 1.0)
		else:
			img.SetRenderingRect(0.0, 0.0, (w - tw * sx) * self.z / tw, (h - th * sy) * self.z / th)
		return img

	def _Rect(self, parent, x, y, w, h, color, fill=True):
		b = ui.Bar() if fill else ui.Box()
		b.SetParent(parent)
		b.AddFlag("not_pick")
		b.SetColor(color)
		x0, y0 = self.P(x), self.P(y)
		b.SetPosition(x0, y0)
		b.SetSize(max(1, self.P(x + w) - x0), max(1, self.P(y + h) - y0))
		b.Show()
		self.keep.append(b)
		return b

	def _Kutu(self, parent, x, y, w, h):
		self._Rect(parent, x, y, w, h, C_FILL)
		self._Rect(parent, x, y, w, h, C_LINE, False)

	def _Txt(self, parent, pt, color, x, y, align="left", outline=True, keep=None):
		t = ui.TextLine()
		t.SetParent(parent)
		t.AddFlag("not_pick")
		t.SetFontName(self.F(pt))
		if outline:
			t.SetOutline()
		if align == "center":
			t.SetHorizontalAlignCenter()
		elif align == "right":
			t.SetHorizontalAlignRight()
		t.SetPackedFontColor(color)
		t.SetPosition(self.P(x), self.P(y))
		t.Show()
		(self.keep if keep is None else keep).append(t)
		return t

	def _Btn(self, parent, name, x, y, func):
		b = ui.Button()
		b.SetParent(parent)
		b.SetUpVisual(DIR + name + "_up.png")
		b.SetOverVisual(DIR + name + ("_over.png" if name not in ("soru", "gob") else "_up.png"))
		b.SetDownVisual(DIR + name + "_down.png")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, self.si, self.si)
		b.SetPosition(self.P(x), self.P(y))
		b.SetEvent(func)
		b.Show()
		self.keep.append(b)
		return b

	def _BigHit(self, parent, x, y, w, h, func):
		"""k\xfc\xe7\xfck d\xfc\xf0menin \xe7evresinde parmak boyu g\xf6r\xfcnmez dokunma alan\xfd (KULLANICI: "kapatma tu\xfeuna zor t\xfdklan\xfdyor")"""
		hb = _Hit()
		hb.SetParent(parent)
		hb.SetPosition(self.P(x), self.P(y))
		hb.SetSize(self.P(w), self.P(h))
		hb.onUp = func
		hb.Show()
		self.keep.append(hb)
		return hb

	def _Board(self, parent, W, H, ttl):
		# KULLANICI (2026-10-04, arkada\xfe\xfdn\xfdn telefonu): "sa\xf0da bir \xe7izgi \xe7\xfdk\xfdyor". Kesirli \xf6l\xe7ekte par\xe7alar u\xe7 uca konunca
		# s\xfdn\xfdr yuvarlan\xfdp 0,4-1,2 fiziksel px bo\xfeluk kal\xfdyordu (ekran \xe7\xf6z\xfcn\xfcrl\xfc\xf0\xfcne g\xf6re g\xf6r\xfcn\xfcr). Alttaki par\xe7a \xfcsttekinin
		# ALTINA O kadar ta\xfear: zemin \xe7er\xe7evenin, \xe7er\xe7eve \xfeeritleri k\xf6\xfeelerin, ba\xfel\xfdk ortas\xfd u\xe7lar\xfdn alt\xfdna (s\xfdra korunur).
		O = 2
		self._Tile(parent, PT + "board_base.tga", 32 - O, 32 - O, W - 64 + 2 * O, H - 64 + 2 * O, 128, 128)
		self._Tile(parent, PT + "board_line_top.tga", 32 - O, 0, W - 64 + 2 * O, 32, 128, 32)
		self._Tile(parent, PT + "board_line_bottom.tga", 32 - O, H - 32, W - 64 + 2 * O, 32, 128, 32)
		self._Tile(parent, PT + "board_line_left.tga", 0, 32 - O, 32, H - 64 + 2 * O, 32, 128)
		self._Tile(parent, PT + "board_line_right.tga", W - 32, 32 - O, 32, H - 64 + 2 * O, 32, 128)
		for (n, cx, cy) in (("lefttop", 0, 0), ("righttop", W - 32, 0), ("leftbottom", 0, H - 32), ("rightbottom", W - 32, H - 32)):
			self._PImg(parent, PT + "board_corner_%s.tga" % n, cx, cy)
		tw = W - 16
		self._Tile(parent, PT + "titlebar_center.tga", 40 - O, 8, tw - 64 + 2 * O, TB_H, 32, 32)
		self._Tile(parent, PT + "titlebar_left.tga", 8, 8, 32, TB_H, 32, 32)
		self._Tile(parent, PT + "titlebar_right.tga", 8 + tw - 32, 8, 32, TB_H, 32, 32)
		(iw, ih) = G.ttl[ttl]
		self._Img(parent, ttl, 8 + (tw - iw / DPR) / 2.0, 8 + (TB_H - ih / DPR) / 2.0)

	def _ItemImg(self, parent, vnum, box, keep):
		"""oyunun e\xfeya ikonu (vnum; 0 = bo\xfe) -> box prototip px kutuya s\xfd\xf0ar (uzun silah ikonlar\xfdnda oran korunur)"""
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w._kutu = box
		w._v = -1
		w._yol = ""
		keep.append(w)
		self.__SetItemImg(w, vnum)
		return w

	def __SetItemImg(self, w, vnum):
		vnum = int(vnum)
		if w._v == vnum:
			return
		w._v = vnum
		(ad, path, aciklama, boy) = _Item(vnum) if vnum > 0 else ("", "", "", (1, 1))
		w._yol = ""
		if not path:
			w.Hide()
			return
		try:
			w.LoadImage(path)
			max(0, 0)		# LoadImage bekleyen hatas\xfdn\xfd burada tetikle
		except:
			w.Hide()
			return
		w._yol = path
		# MANTIKSAL boy = 32 x yuva (motor HD ikonu density 4 ile 32 px g\xf6r\xfcr). GetWidth'e G\xdcVEN\xddLMEZ: y\xfckleme bitmeden
		# 0 ya da 128 d\xf6ner -> \xf6l\xe7ek 4 kat k\xfc\xe7\xfck \xe7\xfdkar, ikon baz\xfd cihazlarda / ilk a\xe7\xfdl\xfd\xfeta minicik g\xf6r\xfcn\xfcr ("bazen").
		s = w._kutu * self.z / (32.0 * max(boy[0], boy[1]))
		w.SetScale(s, s)
		w.Show()

	# ---------------- kurulum (ilk a\xe7\xfdl\xfd\xfeta, bir kez)
	def __Build(self):
		self.__Scale()
		w = _Root()
		w.SetSize(self.P(W_WIN), self.P(H_WIN))
		w.SetPosition((self.scrW - self.P(W_WIN)) // 2, max(0, (self.scrH - self.P(H_WIN)) // 2))
		w.Hide()
		self.keep.append(w)
		self.root = w
		self._Board(w, W_WIN, H_WIN, "ttl_cark")
		self._Btn(w, "soru", 8 + TB_W - 24 - 21, 7, ui.__mem_func__(self.__OnHelp))
		self._Btn(w, "x", 8 + TB_W - 4 - 15, 12, ui.__mem_func__(self.Close))
		self._BigHit(w, 8 + TB_W - 27, 0, 35, 38, ui.__mem_func__(self.Close))
		self._BigHit(w, 8 + TB_W - 59, 0, 32, 38, ui.__mem_func__(self.__OnHelp))
		# \xfcst bilgi \xfeeridi: seri + 7. g\xfcn hediyesi + envanter + hak
		self._Kutu(w, *UST)
		self._Txt(w, 11, C_SUB, 24, 45).SetText("G\xfcnl\xfck Seri")
		self.seriT = self._Txt(w, 13, C_GOLD, 24, 60)
		self.pips = []
		for g in range(1, 8):
			im = {}
			if g < 7:
				x = 94 + (g - 1) * 32
				if g != 6:
					self._Rect(w, x + 26, 63, 6, 2, C_LINE)
				for st in ("bos", "ok", "bugun"):
					im[st] = self._Img(w, "gun%d_%s" % (g, st), x - 4, 47, False)
			else:
				self._Rect(w, 94 + 5 * 32 + 26, 63, 6, 2, C_LINE)
				for st in ("bos", "ok", "bugun"):
					im[st] = self._Img(w, "gun7_%s" % st, 286 - 4, 43, False)
			self.pips.append(im)
		self.hedT1 = self._Txt(w, 10.5, C_SUB, 330, 45)
		self.hedT2 = self._Txt(w, 11.5, C_GOLD, 330, 60)
		self._Txt(w, 11, C_SUB, 640, 45, "right").SetText("Envanter")
		self.envT = self._Txt(w, 13, C_OK, 640, 59, "right")
		self._Txt(w, 11, C_SUB, 732, 45, "right").SetText("Bug\xfcnk\xfc hak")
		self.hakT = self._Txt(w, 13, C_CREAM, 732, 59, "right")
		# \xe7ark: d\xfd\xfe halka (sabit) + disk (d\xf6ner) + dilim par\xe7alar\xfd + \xfd\xfe\xfdklar + i\xfearet\xe7i + g\xf6bek
		self._Img(w, "rim", CX - 172, CY - 172)
		self.disk = ui.ExpandedImageBox()
		self.disk.SetParent(w)
		self.disk.AddFlag("not_pick")
		self.keep.append(self.disk)
		self.diskN = -1
		self.sliceLayer = ui.Window()		# dilim par\xe7alar\xfd bu katmanda (disk \xfcst\xfc, \xfd\xfe\xfdk/i\xfearet\xe7i alt\xfd)
		self.sliceLayer.SetParent(w)
		self.sliceLayer.AddFlag("not_pick")
		self.sliceLayer.SetPosition(0, 0)
		self.sliceLayer.SetSize(self.P(W_WIN), self.P(H_WIN))
		self.sliceLayer.Show()
		self.keep.append(self.sliceLayer)
		self.lights = []
		for i in range(20):
			a = math.radians(i * 18 - 90)
			self.lights.append(self._Img(w, "isik", CX + R_ISIK * math.cos(a) - 4, CY + R_ISIK * math.sin(a) - 4))
		self.ok = self._Img(w, "ok", CX - 20, CY - 178)
		hit = _Hit()
		hit.SetParent(w)
		hit.SetPosition(self.P(CX - 142), self.P(CY - 142))
		hit.SetSize(self.P(284), self.P(284))
		hit.onUp = ui.__mem_func__(self.__OnWheelTap)
		hit.Show()
		self.keep.append(hit)
		self._Btn(w, "gob", CX - 46, CY - 46, ui.__mem_func__(self.__OnSpin))
		self.__PlaceOk(0.0)
		# v78: "Oranlar" d\xfc\xf0mesi (halkan\xfdn sol \xfcst bo\xfelu\xf0u) + parmak boyu dokunma alan\xfd (halkaya ta\xfemaz)
		(bw, bh) = G.btn["oran"]
		self._Btn(w, "oran", ORAN_BTN[0], ORAN_BTN[1], ui.__mem_func__(self.__OnOran))
		self._BigHit(w, ORAN_BTN[0] - 4, ORAN_BTN[1] - 4, bw + 4, bh + 6, ui.__mem_func__(self.__OnOran))
		# sekmeler
		self.tabs = {}
		for (j, key) in enumerate(("odul", "gecmis", "kazanan")):
			b = self._Btn(w, "sk_" + key, TAB_X + j * (TAB_W + TAB_GAP), TAB_Y, lambda k0=key: self.__OnTab(k0))
			self.tabs[key] = b
		# liste
		self._Kutu(w, *LIST)
		self.rows = []
		for r in range(ROW_N):
			y = LIST[1] + 7 + r * ROW_H
			hl = self._Rect(w, LIST[0] + 4, y, LIST[2] - 8, ROW_H, 0x24e8d08a)
			hl.Hide()
			ic = self._ItemImg(w, 0, 17, self.keep)
			nm = self._Txt(w, 11.5, C_CREAM, LIST[0] + 33, y + 2)
			nm2 = self._Txt(w, 11.5, C_CREAM, LIST[0] + 33, y + 2)
			ad = self._Txt(w, 11, C_GOLD, 640, y + 2, "right")
			tr = self._Rect(w, 647, y + 7, 46, 5, 0xff1c140d)
			fl = self._Img(w, "bar_sans", 647, y + 7, False)
			fl.SetScale(self.z * 46 / 200.0, self.z * 5 / 10.0)
			pc = self._Txt(w, 10.5, C_OFF, 730, y + 3, "right")
			h = _Hit()
			h.SetParent(w)
			h.SetPosition(self.P(LIST[0] + 4), self.P(y))
			h.SetSize(self.P(LIST[2] - 8), self.P(ROW_H))
			h.onUp = lambda r0=r: self.__OnRow(r0)
			self.keep.append(h)
			row = {"y": y, "hl": hl, "ic": ic, "nm": nm, "nm2": nm2, "ad": ad, "tr": tr, "fl": fl, "pc": pc, "hit": h, "i": -1}
			for k0 in ("ic", "nm", "nm2", "ad", "tr", "fl", "pc", "hit"):
				row[k0].Hide()
			self.rows.append(row)
		self.bosT = self._Txt(w, 11.5, C_OFF, LIST[0] + LIST[2] / 2.0, LIST[1] + LIST[3] / 2.0 - 8, "center")
		self.bosT.Hide()
		# ayr\xfdnt\xfd kart\xfd
		self._Kutu(w, *DET)
		self._Img(w, "yuva46", DET[0] + 10, DET[1] + 9)
		self.detIc = self._ItemImg(w, 0, 34, self.keep)
		x = DET[0] + 66
		self.detAd = self._Txt(w, 13, C_CREAM, x, DET[1] + 8)
		self.detAdet = self._Txt(w, 12, C_GOLD, x, DET[1] + 8)
		self.detNd = self._Txt(w, 10, C_OFF, x, DET[1] + 25)
		self.detAc1 = self._Txt(w, 11, C_SUB, x, DET[1] + 39)
		self.detAc2 = self._Txt(w, 11, C_SUB, x, DET[1] + 53)
		self.detSt = self._Txt(w, 10.5, C_OFF, x, DET[1] + 69)
		# alt: \xc7evir + s\xfcre
		self.cevirB = self._Btn(w, "cevir", CEVIR_X, CEVIR_Y, ui.__mem_func__(self.__OnSpin))
		self.cevirKapali = self._Rect(w, CEVIR_X + 2, CEVIR_Y + 2, 146, 36, 0x99000000)
		self._Kutu(w, *SURE)
		self.sureEt = self._Txt(w, 11, C_SUB, SURE[0] + 10, SURE[1] + 6)
		self.sureT = self._Txt(w, 11.5, C_CREAM, SURE[0] + SURE[2] - 10, SURE[1] + 6, "right")
		self._Rect(w, SURE[0] + 10, SURE[1] + 26, SURE[2] - 20, 5, 0xff1c140d)
		self.pb = self._Img(w, "bar_sure", SURE[0] + 10, SURE[1] + 26)
		self.pb.SetScale(self.z * (SURE[2] - 20) / 200.0, self.z * 5 / 10.0)
		# son kazananlar \xfeeridi (kayan yaz\xfd yerine s\xfdrayla belirir: k\xfdrpma gerekmez, ucuz)
		self._Kutu(w, *SERIT)
		self._Txt(w, 11, C_GOLD, SERIT[0] + 10, SERIT[1] + 5).SetText("Son kazananlar")
		self.tkA = self._Txt(w, 11, C_CREAM, SERIT[0] + 118, SERIT[1] + 5)
		self.tkB = self._Txt(w, 11, C_GOLD, SERIT[0] + 118, SERIT[1] + 5)
		self.__BuildPopups()
		self.built = True
		self.__BuildSlices()

	def __BuildSlices(self):
		"""disk dokusu + her dilim i\xe7in nadirlik yay\xfd, yuva, e\xfeya ikonu, etiket (yaln\xfdz tablo de\xf0i\xfeince)."""
		self.cfgShown = M.cfgSig
		for wd in self.sliceKeep:
			try:
				wd.Hide()
			except:
				pass
		self.sliceKeep = []
		self.slices = []
		n = M.N()
		if n != self.diskN:
			self.diskN = n
			self.disk.LoadImage(DIR + "disk%d.png" % n)
			max(0, 0)
			self.disk.SetScale(self.si, self.si)
			self.disk.Show()
		L = self.sliceLayer
		for i in range(n):
			o = M.odul[i]
			s = {"rim": None}
			if o["n"] > 0 and (n, o["n"]) in G.YAY:
				s["rim"] = self._Img(L, "yay%d_%d" % (n, o["n"]), 0, 0, True, self.sliceKeep)
				s["rimg"] = G.YAY[(n, o["n"])]
			s["yuva"] = self._Img(L, "yuva38", 0, 0, True, self.sliceKeep)
			s["ic"] = self._ItemImg(L, M.IkonV(i), 32, self.sliceKeep)
			et = s["et"] = self._Txt(L, 11.5 if o["tur"] != 2 else 12.5, NADR[o["n"]], 0, 0, "center", True, self.sliceKeep)
			et.SetText(o["et"])
			(tw, th) = et.GetTextSize()
			if tw > ET_MAXW * self.z:		# panelde uzun etiket: k\xfc\xe7\xfck yaz\xfd
				et.SetFontName(self.F(9.5))
				et.SetText(o["et"])
				(tw, th) = et.GetTextSize()
			s["eh"] = th
			self.slices.append(s)
		if self.sel >= n:
			self.sel = 0
		self.__PlaceDisk()
		self.__PlaceSlices()
		self.listSig = None
		self.statSig = None

	def __BuildPopups(self):
		# perde: arkaya dokunma ge\xe7mesin
		pd = _Root()
		pd.SetSize(self.scrW, self.scrH)
		pd.SetPosition(0, 0)
		b = ui.Bar()
		b.SetParent(pd)
		b.AddFlag("not_pick")
		b.SetColor(0x66000000)
		b.SetPosition(0, 0)
		b.SetSize(self.scrW, self.scrH)
		b.Show()
		self.keep.append(b)
		pd.Hide()
		self.keep.append(pd)
		self.perde = pd
		# \xf6d\xfcl penceresi
		p = _Root()
		p.SetSize(self.P(POP_W), self.P(POP_H))
		p.SetPosition((self.scrW - self.P(POP_W)) // 2, (self.scrH - self.P(POP_H)) // 2)
		p.Hide()
		self.keep.append(p)
		self.pop = p
		self._Board(p, POP_W, POP_H, "ttl_odul")
		self.popIsin = self._Img(p, "isin", 150 - 120, 98 - 120, False)
		self.popHale = self._Img(p, "hale", 150 - 48, 98 - 48)
		self._Img(p, "yuva64", 150 - 32, 98 - 32)
		self.popIc = self._ItemImg(p, 0, 48, self.keep)
		self.popTeb = self._Txt(p, 15, C_GOLD, 150, 41, "center")
		self.popNd = self._Txt(p, 10.5, C_OFF, 150, 135, "center")
		self.popAd = self._Txt(p, 14, C_CREAM, 150, 150, "center")
		self.popAdet = self._Txt(p, 12, C_SUB, 150, 168, "center")
		self.popHed = self._Txt(p, 11.5, C_GOLD, 150, 185, "center")
		self._Btn(p, "tamam", 90, 204, ui.__mem_func__(self.__OnTamam))
		self._Btn(p, "x", POP_W - 8 - 4 - 15, 12, ui.__mem_func__(self.__OnTamam))	# ba\xfel\xfdk \xfeeridindeki X \xe7al\xfd\xfes\xfdn
		self._BigHit(p, POP_W - 8 - 27, 0, 35, 38, ui.__mem_func__(self.__OnTamam))
		# kurallar (metin a\xe7\xfdl\xfd\xfeta ayara g\xf6re yaz\xfdl\xfdr)
		k = _Root()
		k.SetSize(self.P(KUR_W), self.P(KUR_H))
		k.SetPosition((self.scrW - self.P(KUR_W)) // 2, (self.scrH - self.P(KUR_H)) // 2)
		k.Hide()
		self.keep.append(k)
		self.kural = k
		self._Board(k, KUR_W, KUR_H, "ttl_kural")
		self.kuralT = [self._Txt(k, 11.5, C_SUB, 22, 44 + j * 21) for j in range(9)]
		self._Btn(k, "anladim", (KUR_W - 110) / 2.0, KUR_H - 50, ui.__mem_func__(self.__OnKuralKapat))
		self._Btn(k, "x", KUR_W - 8 - 4 - 15, 12, ui.__mem_func__(self.__OnKuralKapat))
		self._BigHit(k, KUR_W - 8 - 27, 0, 35, 38, ui.__mem_func__(self.__OnKuralKapat))
		self.__BuildOran()

	def __BuildOran(self):
		"""v78: \xf6d\xfcl oranlar\xfd penceresi (klasik zemin d\xf6\xfeeme + tablo kutusu; sat\xfdrlar a\xe7\xfdl\xfd\xfeta / tablo de\xf0i\xfeince yaz\xfdl\xfdr)."""
		r = _Root()
		r.SetSize(self.P(ORAN_W), self.P(ORAN_H))
		r.SetPosition((self.scrW - self.P(ORAN_W)) // 2, (self.scrH - self.P(ORAN_H)) // 2)
		r.Hide()
		self.keep.append(r)
		self.oran = r
		self.oranSig = None
		self._Board(r, ORAN_W, ORAN_H, "ttl_oran")
		self._Kutu(r, *ORAN_KUTU)
		(xi, xa, xn, xs, x7) = ORAN_X
		self.oranBas = [self._Txt(r, 10.5, C_OFF, xi - 2, 46), self._Txt(r, 10.5, C_OFF, xn, 46),
			self._Txt(r, 10.5, C_OFF, xs, 46, "right"), self._Txt(r, 10.5, C_OFF, x7, 46, "right")]
		self._Rect(r, ORAN_KUTU[0] + 6, 62, ORAN_KUTU[2] - 12, 1, C_LINE)
		self.oranRows = []
		for j in range(ROW_N):
			y = ORAN_Y0 + j * ORAN_DY
			row = {"ic": self._ItemImg(r, 0, 16, self.keep), "y": y,
				"ad": self._Txt(r, 11.5, C_CREAM, xa, y + 1),
				"nd": self._Txt(r, 10.5, C_OFF, xn, y + 2),
				"p": self._Txt(r, 11.5, C_CREAM, xs, y + 1, "right"),
				"p7": self._Txt(r, 11.5, C_GOLD, x7, y + 1, "right")}
			if j % 2:
				zemin = self._Rect(r, ORAN_KUTU[0] + 4, y - 1, ORAN_KUTU[2] - 8, ORAN_DY, 0x14e8d08a)
				row["zemin"] = zemin
			self.oranRows.append(row)
		self.oranTop = self._Txt(r, 11, C_SUB, ORAN_W / 2.0, 280, "center")
		self.oranNot = [self._Txt(r, 10.5, C_OFF, ORAN_W / 2.0, 298 + j * 16, "center") for j in range(2)]
		self._Btn(r, "tamam", (ORAN_W - 120) / 2.0, ORAN_H - 50, ui.__mem_func__(self.__OnOranKapat))
		self._Btn(r, "x", ORAN_W - 8 - 4 - 15, 12, ui.__mem_func__(self.__OnOranKapat))
		self._BigHit(r, ORAN_W - 8 - 27, 0, 35, 38, ui.__mem_func__(self.__OnOranKapat))

	def __OranAd(self, i):
		o = M.odul[i]
		if o["tur"] == 1:
			return "%s Yang" % _kisa(o["a"])
		ad = M.Ad(i)
		if o["tur"] == 0 and o["a"] > 1:
			ad = "%s x%d" % (ad, o["a"])
		return ad

	def __OranDoldur(self):
		"""tablo -> sat\xfdrlar (yaln\xfdz a\xe7\xfdl\xfd\xfeta ve tablo de\xf0i\xfeince; kare ba\xfe\xfd i\xfe yok)."""
		self.oranSig = M.cfgSig
		n = M.N()
		oran = M.Oranlar()
		gar = bool(M.garanti) and len([o for o in M.odul if o["n"] > 0]) > 0
		(b0, b1, b2, b3) = self.oranBas
		b0.SetText(_Y("\xd6d\xfcl", "Reward"))
		b1.SetText(_Y("Nadirlik", "Rarity"))
		b2.SetText(_Y("\xdeans", "Chance"))
		b3.SetText(_Y("7. g\xfcn", "Day 7") if gar else "")
		order = sorted(range(n), key=lambda j: (-M.odul[j]["n"], -oran[j][0], j))
		maxw = ORAN_AD_MAXW * self.z
		for (k, row) in enumerate(self.oranRows):
			if row.get("zemin"):
				if k < n:
					row["zemin"].Show()
				else:
					row["zemin"].Hide()
			if k >= n:
				for key in ("ic", "ad", "nd", "p", "p7"):
					row[key].Hide()
				continue
			j = order[k]
			o = M.odul[j]
			nd = o["n"]
			self.__SetItemImg(row["ic"], M.IkonV(j))
			if row["ic"]._yol:
				self.__Center(row["ic"], (ORAN_X[0] + 8) * self.z, (row["y"] + 9) * self.z)
			ad = self.__OranAd(j)
			t = row["ad"]
			t.SetFontName(self.F(11.5))
			t.SetText(ad)
			if t.GetTextSize()[0] > maxw:
				t.SetFontName(self.F(9.5))
				t.SetText(ad)
				while len(ad) > 4 and t.GetTextSize()[0] > maxw:
					ad = ad[:-1]
					t.SetText(ad.rstrip() + "...")
			t.SetPackedFontColor(NADR[nd])
			t.Show()
			row["nd"].SetText(_Y(NAD[nd], NAD_EN[nd]))
			row["nd"].SetPackedFontColor(NADR[nd])
			row["nd"].Show()
			(p, p7) = oran[j]
			row["p"].SetText(_Yuzde(p))
			row["p"].Show()
			if gar:
				row["p7"].SetText(_Yuzde(p7) if p7 > 0.0 else "-")
				row["p7"].SetPackedFontColor(C_GOLD if p7 > 0.0 else C_OFF)
				row["p7"].Show()
			else:
				row["p7"].Hide()
		# nadirlik toplamlar\xfd (normal g\xfcn)
		top = [0.0, 0.0, 0.0]
		for (j, o) in enumerate(M.odul):
			top[o["n"]] += oran[j][0]
		ad = [_Y(NAD[k], NAD_EN[k]) for k in range(3)]
		self.oranTop.SetText(_Y("Toplam: ", "Total: ") + "  \xb7  ".join(["%s %s" % (ad[k], _Yuzde(top[k])) for k in range(3) if top[k] > 0.0]))
		# notlar: 7. g\xfcn kural\xfd + rastgele grup (her e\xfeya e\xfeit \xfeansl\xfd)
		notlar = []
		if gar:
			notlar.append(_Y("7. g\xfcn (7 g\xfcn \xfcst \xfcste) yaln\xfdz Nadir ve Efsanevi \xf6d\xfcller \xe7\xfdkar.",
				"On day 7 of a streak only Rare and Legendary rewards can drop."))
		for (j, o) in enumerate(M.odul):
			if o["tur"] == 2 and o["g"]:
				g = len(o["g"])
				notlar.append(_Y("%s: %d e\xfeyadan biri, her biri %s" % (M.Ad(j), g, _Yuzde(oran[j][0] / g)),
					"%s: one of %d items, each %s" % (M.Ad(j), g, _Yuzde(oran[j][0] / g))))
		if len(notlar) < 2:
			notlar.append(_Y("Oranlar sunucudaki g\xfcncel \xf6d\xfcl tablosundan hesaplan\xfdr.",
				"Odds are calculated from the server's current reward table."))
		for (k, t) in enumerate(self.oranNot):
			t.SetText(notlar[k] if k < len(notlar) else "")

	# ---------------- a\xe7 / kapa
	def IsOpen(self):
		return self.open

	def Open(self):
		if not self.built:
			self.__Build()
		self.open = True
		self.root.Show()
		self.root.SetTop()
		self.listSig = None
		self.statSig = None
		self.secT = -1.0
		t = app.GetTime()
		if t - M.lastAsk > 10.0 and _Ask(M.bqid):		# en s\xfdk 10 sn'de bir tazele (panelde de\xf0i\xfeen tablo da gelir)
			M.lastAsk = t
		self.Tick()

	def Close(self):
		self.open = False
		if self.built:
			self.root.Hide()
			self.pop.Hide()
			self.kural.Hide()
			self.oran.Hide()
			self.perde.Hide()

	def Destroy(self):
		self.Close()
		self.keep = []
		self.sliceKeep = []
		self.slices = []
		self.rows = []
		self.pips = []
		self.lights = []
		self.tabs = {}
		self.oranRows = []
		self.built = False

	# ---------------- olaylar
	def __OnHelp(self):
		bek = int(round(M.bekleme / 3600.0))
		kop = int(round(M.kopma / 3600.0))
		ht = ""
		if M.hv > 0:
			ht = "%s %s" % (_Item(M.hv)[0], _AdetEt(M.hv, M.ha))
		satir = ["\x95 Hesab\xfdna her %d saatte 1 \xfccretsiz \xe7evirme hakk\xfd verilir;" % bek,
			"   ayn\xfd hesaptaki karakterlerin bu hakk\xfd ortak kullan\xfdr.",
			"\x95 \xd6d\xfcl\xfc sunucu belirler; \xf6d\xfcl do\xf0rudan envanterine",
			"   (Yang hesab\xfdna) eklenir.",
			"\x95 Envanterin doluysa \xe7evirme a\xe7\xfdlmaz, \xf6nce yer a\xe7."]
		if M.garanti and M.hv > 0:
			satir += ["\x95 7 g\xfcn \xfcst \xfcste \xe7evirirsen 7. g\xfcn en az Nadir \xf6d\xfcl", "   + hediye: %s" % ht]
		elif M.garanti:
			satir += ["\x95 7 g\xfcn \xfcst \xfcste \xe7evirirsen 7. g\xfcn en az Nadir \xf6d\xfcl", "   garantilidir."]
		elif M.hv > 0:
			satir += ["\x95 7 g\xfcn \xfcst \xfcste \xe7evirirsen 7. g\xfcn hediye:", "   %s" % ht]
		satir += ["\x95 Son \xe7evirmenden %d saat ge\xe7erse seri 1. g\xfcnden ba\xfelar." % kop, "\x95 \xdeanslar her \xf6d\xfcl\xfcn yan\xfdnda yazar."]
		for (j, t) in enumerate(self.kuralT):
			t.SetText(satir[j] if j < len(satir) else "")
		self.perde.Show()
		self.perde.SetTop()
		self.kural.Show()
		self.kural.SetTop()

	def __OnKuralKapat(self):
		self.kural.Hide()
		if not self.pop.IsShow():
			self.perde.Hide()

	def __OnOran(self):
		"""v78: \xf6d\xfcl oranlar\xfd penceresi (modal, perde arkas\xfd dokunulmaz)."""
		if self.state != "bos":
			return
		self.__OranDoldur()
		self.perde.Show()
		self.perde.SetTop()
		self.oran.Show()
		self.oran.SetTop()

	def __OnOranKapat(self):
		self.oran.Hide()
		if not self.pop.IsShow() and not self.kural.IsShow():
			self.perde.Hide()

	def __OnTamam(self):
		self.pop.Hide()
		self.perde.Hide()
		self.popT = -1.0

	def __OnTab(self, key):
		self.tab = key
		self.listSig = None
		self.Tick()

	def __OnRow(self, r):
		row = self.rows[r]
		if self.tab == "odul" and row["i"] >= 0 and self.state == "bos":
			self.sel = row["i"]
			self.listSig = None

	def __OnWheelTap(self):
		if self.state != "bos":
			return
		try:
			(mx, my) = wndMgr.GetMousePosition()
			(rx, ry) = self.root.GetGlobalPosition()
		except:
			return
		dx = mx - (rx + CX * self.z)
		dy = my - (ry + CY * self.z)
		r = math.hypot(dx, dy) / self.z
		if r < 40 or r > 142:
			return
		dil = self.DIL()
		a = math.degrees(math.atan2(dx, -dy)) - self.ang		# saat y\xf6n\xfc, tepeden; diskin d\xf6n\xfc\xfe\xfc d\xfc\xfe\xfcl\xfcr
		i = int(math.floor(((a + dil / 2.0) % 360.0) / dil)) % M.N()
		self.sel = i
		self.tab = "odul"
		self.listSig = None

	def __OnSpin(self):
		if self.state != "bos":
			return
		t = app.GetTime()
		if not M.Ready():
			if M.known and M.bos < 1:
				self.__Err(2)
			return
		if t - self.lastSpinAsk < 1.5:			# \xe7ift dokunma / spam
			return
		if not _Ask(M.qid):
			self.__Err(4)
			return
		self.lastSpinAsk = t
		self.state = "bekle"
		self.t0 = t
		self.tLast = t
		self.vel = 0.0
		self.result = None
		self.vurgu = -1
		self.pop.Hide()
		self.statSig = None

	def OnResult(self, i, v, a, hv, ha):
		if not (0 <= i < M.N()):
			return
		if self.state != "bekle":
			return			# ge\xe7 geldi (zaman a\xfe\xfdm\xfdyla duruldu): yanl\xfd\xfe dilimde \xf6d\xfcl g\xf6sterme; sunucu verir, liste tazelenir
		self.result = (i, v, a, hv, ha)
		if self.open:
			if self.cfgShown != M.cfgSig:
				self.__BuildSlices()	# sunucu sonu\xe7la birlikte yeni tablo g\xf6nderdi (panel az \xf6nce de\xf0i\xfetirdi): d\xf6nerken de\xf0i\xfetir
			dil = self.DIL()
			self.__Plan(-i * dil + (((hash((i, v, a)) % 1000) / 1000.0) - 0.5) * dil * 0.5)
		else:
			self.state = "bos"

	def OnError(self, k):
		self.__Err(k)
		if self.state == "bekle":
			self.__Plan(None)

	def __Err(self, k):
		# yan\xfdt yoksa en olas\xfd sebep: sunucuda /reload q sonras\xfd g\xf6rev numaras\xfd de\xf0i\xfeti -> yeniden giri\xfe tazeler
		self.err = HATA.get(k, "Sunucu yan\xfdt vermedi \x97 karakter se\xe7imine \xe7\xfdk\xfdp tekrar gir.")
		self.errT = app.GetTime()
		self.statSig = None

	def __Plan(self, target):
		"""d\xf6nerken (vel) hedefe yava\xfela: a\xe7\xfd = ba\xfelang\xfd\xe7 + D (1 - (1-p)^4); ba\xfelang\xfd\xe7 h\xfdz\xfd s\xfcreklidir (4D/T = vel)."""
		v = max(self.vel, 300.0)
		if target is not None:
			v = max(v, 1700.0)		# sonu\xe7 h\xfdzl\xfd geldiyse de duru\xfe ~5 sn (sunucu \xf6d\xfcl\xfc 6. sn'de verir)
		if target is None:			# hedefsiz dur (hata / zaman a\xfe\xfdm\xfd)
			D = v * 1.2 / 4.0
		else:
			want = v * 4.6 / 4.0
			base = (target - self.ang) % 360.0
			D = base + 360.0 * max(0, int(math.ceil((want - base) / 360.0)))
		self.dStart = self.ang
		self.dTotal = D
		self.dDur = max(0.6, 4.0 * D / v)
		self.t0 = app.GetTime()
		self.state = "yavas"

	# ---------------- kare (yaln\xfdz a\xe7\xfdkken; HUD d\xfc\xf0mesi \xe7a\xf0\xfdr\xfdr)
	def Tick(self):
		if not (self.built and self.open):
			return
		t = app.GetTime()
		if self.cfgShown != M.cfgSig and self.state == "bos":
			self.__BuildSlices()			# panelde tablo de\xf0i\xfeti (d\xf6nerken de\xf0il)
		if self.oranSig != M.cfgSig and self.oran.IsShow():
			self.__OranDoldur()			# v78: oranlar a\xe7\xfdkken tablo de\xf0i\xfeti
		if self.state != "bos":
			self.__Spin(t)
		elif self.blinkT >= 0.0:
			self.__Blink(t)
		if self.popT >= 0.0 and t >= self.popT:
			self.popT = -1.0
			self.__ShowPop()
		if self.pop.IsShow() and self.popIsin.IsShow():
			self.__Rays(t)
		if t - self.secT >= 0.5 or t < self.secT:
			self.secT = t
			if M.bek and self.state == "bos" and t - M.lastAsk > 8.0 and _Ask(M.bqid):
				M.lastAsk = t		# \xf6d\xfcl bekliyorsa sunucuya sor (zamanlay\xfdc\xfd d\xfc\xfet\xfcyse sunucu burada verir)
			self.__Status(t)
			self.__Ticker(t)
		sig = (self.tab, self.sel, M.sig, self.vurgu, M.cfgSig)
		if sig != self.listSig:
			self.listSig = sig
			self.__List()
			self.__Detail()

	def __Center(self, wd, cx, cy, rot=0.0):
		"""d\xf6nd\xfcrme yolu: g\xf6r\xfcnt\xfc merkezi = konum + k\xf6ken (alt piksel); k\xf6ken \xe7ocu\xf0un YEREL konumuna eklenir"""
		fx = int(math.floor(cx))
		fy = int(math.floor(cy))
		wd.SetPosition(fx, fy)
		wd.SetOrigin(cx - fx, cy - fy)
		wd.SetRotation(rot or ROT_EPS)

	def __PlaceDisk(self):
		self.__Center(self.disk, CX * self.z, CY * self.z, self.ang % 360.0)

	def __PlaceSlices(self):
		"""dilim par\xe7alar\xfd diskle birlikte d\xf6ner; ikon ve etiket D\xddK durur (alt dilimler de okunur)."""
		dil = self.DIL()
		z = self.z
		for (i, s) in enumerate(self.slices):
			a = math.radians(i * dil + self.ang)
			sa, ca = math.sin(a), math.cos(a)
			if s["rim"]:
				(rw, rh, ox, oy) = s["rimg"]
				# yay tuvalinin merkezi (tepedeki dilim i\xe7in ox, oy) disk a\xe7\xfds\xfdyla d\xf6ner
				mx = ox * ca - oy * sa
				my = ox * sa + oy * ca
				self.__Center(s["rim"], (CX + mx) * z, (CY + my) * z, math.degrees(a) % 360.0)
			ix, iy = CX + R_IK * sa, CY - R_IK * ca
			self.__Center(s["yuva"], ix * z, iy * z)
			ic = s["ic"]
			if ic._yol:
				self.__Center(ic, ix * z, iy * z)
			s["et"].SetPosition(int(round((CX + R_ET * sa) * z)), int(round((CY - R_ET * ca) * z - s["eh"] / 2.0)))

	def __Spin(self, t):
		if self.state == "bekle":
			dt = max(0.0, t - self.tLast)
			self.vel = min(1700.0, self.vel + 6800.0 * dt)		# 0.25 sn'de tam h\xfdz
			self.ang += self.vel * dt
			if t - self.t0 > 8.0:				# sunucu yan\xfdt vermedi
				self.__Err(0)
				self.__Plan(None)
		if self.state == "yavas":
			p = (t - self.t0) / self.dDur
			if p >= 1.0:
				self.ang = self.dStart + self.dTotal
				self.__Landed(t)
			else:
				self.ang = self.dStart + self.dTotal * _ease_out4(p)
		self.tLast = t
		self.ang %= 3600.0
		self.disk.SetRotation((self.ang % 360.0) or ROT_EPS)
		self.__PlaceSlices()
		# i\xfearet\xe7i: dilim \xe7izgisi ge\xe7ince "t\xfdk"
		dil = self.DIL()
		tk = int(math.floor((self.ang + dil / 2.0) / dil))
		if tk != self.tickN:
			self.tickN = tk
			self.tickT = t
		k = max(0.0, 1.0 - (t - self.tickT) / 0.12)
		self.__PlaceOk(-14.0 * k)
		step = int(t / 0.09)
		if step != self.lightStep:
			self.lightStep = step
			for (j, l) in enumerate(self.lights):
				l.SetAlpha(1.0 if (j + step) % 3 == 0 else 0.35)

	def __PlaceOk(self, deg):
		"""i\xfearet\xe7iyi tepesindeki pim (0,-168) etraf\xfdnda d\xf6nd\xfcr; motor kendi merkezinde d\xf6nd\xfcr\xfcr -> merkezi biz ta\xfe\xfdr\xfdz."""
		if deg == getattr(self, "_okDeg", None):
			return
		self._okDeg = deg
		(tw, th) = G.ok
		h = th / DPR		# prototip px, tuval y -178..-128
		ox, oy = 0.0, (-178 + h / 2.0) - (-168)	# merkezin pime uzakl\xfd\xf0\xfd
		r = math.radians(deg)
		mx = ox * math.cos(r) - oy * math.sin(r)
		my = ox * math.sin(r) + oy * math.cos(r)
		self.__Center(self.ok, (CX + mx) * self.z, (CY - 168 + my) * self.z, deg)

	def __Landed(self, t):
		self.state = "bos"
		self.__PlaceOk(0.0)
		if self.result is None:
			for l in self.lights:
				l.SetAlpha(1.0)
			return
		i = self.result[0]
		self.sel = i
		self.vurgu = i
		self.tab = "odul"
		self.blinkT = t
		self.popT = t + 0.65
		M.sig += 1			# ge\xe7mi\xfe/kazananlar sunucudan gelir (\xf6d\xfcl verilince) - yerelde eklenmez (\xe7ift sat\xfdr olmas\xfdn)

	def __Blink(self, t):
		n = int((t - self.blinkT) / 0.14)
		if n > 9:
			self.blinkT = -1.0
			for l in self.lights:
				l.SetAlpha(1.0)
			return
		if n != self.lightStep:
			self.lightStep = n
			for (j, l) in enumerate(self.lights):
				l.SetAlpha(1.0 if (n + j) % 2 else 0.3)

	def __Rays(self, t):
		self.__Center(self.popIsin, 150 * self.z, 98 * self.z, (t * 40.0) % 360.0)

	def __ShowPop(self):
		if self.result is None:
			return
		(i, v, a, hv, ha) = self.result
		nd = M.odul[i]["n"] if 0 <= i < M.N() else 0
		self.popTeb.SetText(("Tebrikler!", "Nadir \xf6d\xfcl!", "EFSANEV\xdd \xd6D\xdcL!")[nd])
		self.popNd.SetText(NAD[nd].upper())
		self.popNd.SetPackedFontColor(NADR[nd])
		if v == 1:
			self.popAd.SetText("%s Yang" % _nokta(a))
			self.popAdet.SetText("Yang hesab\xfdna eklendi")
		else:
			self.popAd.SetText(_Item(v)[0])
			self.popAdet.SetText("%d adet envanterine eklendi" % a)
		self.popAd.SetPackedFontColor(NADR[nd])
		self.popHed.SetText(("+ 7. g\xfcn hediyesi: %s %s" % (_Item(hv)[0], _AdetEt(hv, ha))) if hv > 0 else "")
		self.__SetItemImg(self.popIc, v)
		self.__Center(self.popIc, 150 * self.z, 98 * self.z)
		(r, g, b) = HALE[nd]
		wndMgr.SetDiffuseColor(self.popHale.hWnd, r, g, b, 0.9)
		if nd == 2:
			self.popIsin.Show()
		else:
			self.popIsin.Hide()
		self.perde.Show()
		self.perde.SetTop()
		self.pop.Show()
		self.pop.SetTop()

	# ---------------- yaz\xfdlar (de\xf0i\xfeince)
	def __Status(self, t):
		ready = M.Ready()
		kalan = max(0.0, M.readyAt - t)
		dolu = M.known and M.bos < 1
		if self.state != "bos":
			et, sure, pb = "\xc7ark d\xf6n\xfcyor...", "", 1.0
		elif self.err and t - self.errT < 6.0:
			et, sure, pb = self.err, "", 1.0
		elif not M.known:
			et, sure, pb = ("Bilgi al\xfdn\xfdyor..." if M.qid >= 0 else "\xc7ark bilgisi gelmedi \x97 karakter se\xe7imine \xe7\xfdk\xfdp tekrar gir."), "", 0.0
		elif M.bek:
			et, sure, pb = "\xd6d\xfcl\xfcn veriliyor...", "", 1.0
		elif ready and dolu:
			et, sure, pb = "Envanterin dolu \x97 \xf6d\xfcl i\xe7in yer a\xe7", "", 1.0
		elif ready:
			et, sure, pb = "G\xfcnl\xfck hakk\xfdn haz\xfdr!", "\xc7evir", 1.0
		else:
			et, sure, pb = "Sonraki \xfccretsiz \xe7evirme", _sure(kalan), 1.0 - kalan / float(max(60, M.bekleme))
		seri = M.seri
		key = (et, sure, int(pb * 200), ready and not dolu and self.state == "bos", seri, M.bos, ready, M.known, M.cfgSig)
		if key == self.statSig:
			return
		self.statSig = key
		self.sureEt.SetText(et)
		self.sureEt.SetPackedFontColor(C_BAD if (self.err and t - self.errT < 6.0) or (ready and dolu) else C_SUB)
		self.sureT.SetText(sure)
		px = int(round(_clamp(pb, 0.0, 1.0) * 200))
		self.pb.SetRenderingRect(0.0, 0.0, -(200 - px + 0.5) / 200.0, 0.0)
		acik = ready and not dolu and self.state == "bos"
		if acik:
			self.cevirKapali.Hide()
		else:
			self.cevirKapali.Show()
		self.envT.SetText("%d bo\xfe yuva" % M.bos if M.known else "\x97")
		self.envT.SetPackedFontColor(C_BAD if dolu else C_OK)
		self.hakT.SetText("1 / 1" if ready else "0 / 1")
		# seri: tamamlanan g\xfcn say\xfds\xfd (bug\xfcn \xe7evrildiyse dahil)
		bugun = not ready
		s = seri if M.known else 0
		if ready and s >= 7:
			s = 0				# 7. g\xfcnden sonra seri 1'den
		gun = s if bugun else s + 1
		self.seriT.SetText("%d. g\xfcn" % max(1, gun))
		for (g, im) in enumerate(self.pips):
			d = g + 1
			st = "ok" if (d < gun or (d == gun and bugun)) else ("bugun" if d == gun else "bos")
			for (k0, w) in im.items():
				if k0 == st:
					w.Show()
				else:
					w.Hide()
		# 7. g\xfcn hediyesi (paneldeki ayar)
		if M.hv > 0:
			self.hedT1.SetText("7. g\xfcn hediyesi")
			self.hedT2.SetText("%s %s" % (_Item(M.hv)[0], _AdetEt(M.hv, M.ha)))
		elif M.garanti:
			self.hedT1.SetText("7. g\xfcn")
			self.hedT2.SetText("En az Nadir \xf6d\xfcl")
		else:
			self.hedT1.SetText("")
			self.hedT2.SetText("")

	def __Ticker(self, t):
		kz = M.kazanan
		if not kz:
			self.tkA.SetText("Hen\xfcz kazanan yok \x97 ilk sen ol!")
			self.tkA.SetPackedFontColor(C_OFF)
			self.tkB.Hide()
			return
		if t - self.tickerT >= 4.0:
			self.tickerT = t
			self.ticker = (self.ticker + 1) % len(kz)
			(ad, v, a, n) = kz[self.ticker % len(kz)]
			self.tkA.SetText(ad)
			self.tkA.SetPackedFontColor(C_CREAM)
			(w, h) = self.tkA.GetTextSize()
			if v == 1:
				self.tkB.SetText("%s Yang kazand\xfd" % _kisa(a))
			else:
				self.tkB.SetText("%s%s kazand\xfd" % (_Item(v)[0], (" x%d" % a) if a > 1 else ""))
			self.tkB.SetPackedFontColor(NADR[n])
			self.tkB.SetPosition(self.P(SERIT[0] + 118) + w + self.P(5), self.P(SERIT[1] + 5))
			self.tkB.Show()

	def __List(self):
		if getattr(self, "_tabShown", None) != self.tab:
			self._tabShown = self.tab
			self.__Tabs()
		self.__Rows()

	def __Tabs(self):
		for (key, b) in self.tabs.items():
			sel = key == self.tab
			b.SetUpVisual(DIR + "sk_%s_%s.png" % (key, "down" if sel else "up"))
			b.SetOverVisual(DIR + "sk_%s_%s.png" % (key, "down" if sel else "over"))
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(b.hWnd, self.si, self.si)

	def __Rows(self):
		items = []
		if self.tab == "odul":
			order = sorted(range(M.N()), key=lambda j: (-M.odul[j]["n"], j))
			for j in order:
				o = M.odul[j]
				items.append((j, M.IkonV(j), M.Ad(j), "", NADR[o["n"]], o["et"], M.Sans(j), None))
		elif self.tab == "gecmis":
			now = app.GetTime()
			for (v, a, n, ts) in M.gecmis[:ROW_N]:
				items.append((-1, v, _Item(v)[0], "", NADR[n], _AdetEt(v, a), None, _once(now - ts)))
		else:
			for (ad, v, a, n) in M.kazanan[:ROW_N]:
				items.append((-1, v, ad, _Item(v)[0], NADR[n], _AdetEt(v, a), None, None))
		top = max([M.Sans(j) for j in range(M.N())] or [1.0])
		for (r, row) in enumerate(self.rows):
			if r >= len(items):
				row["i"] = -1
				for k0 in ("hl", "ic", "nm", "nm2", "ad", "tr", "fl", "pc", "hit"):
					row[k0].Hide()
				continue
			(j, ik, ad, ad2, col, adet, sans, zaman) = items[r]
			row["i"] = j
			y = row["y"]
			self.__SetItemImg(row["ic"], ik)
			if row["ic"]._yol:
				self.__Center(row["ic"], (LIST[0] + 8 + 8.5) * self.z, (y + 9.5) * self.z)
			if ad2:
				row["nm"].SetText(ad)
				row["nm"].SetPackedFontColor(C_CREAM)
				(w, h) = row["nm"].GetTextSize()
				row["nm2"].SetText(ad2)
				row["nm2"].SetPackedFontColor(col)
				row["nm2"].SetPosition(self.P(LIST[0] + 33) + w + self.P(5), self.P(y + 2))
				row["nm2"].Show()
			else:
				row["nm"].SetText(ad)
				row["nm"].SetPackedFontColor(col)
				row["nm2"].Hide()
			row["nm"].Show()
			row["ad"].SetText(adet)
			row["ad"].Show()
			if sans is not None:
				px = int(round(_clamp(sans / max(1.0, top), 0.0, 1.0) * 200))
				row["fl"].SetRenderingRect(0.0, 0.0, -(200 - px + 0.5) / 200.0, 0.0)
				row["tr"].Show()
				row["fl"].Show()
				row["pc"].SetText("%%%s" % (("%.1f" % sans).rstrip("0").rstrip(".")))
				row["pc"].Show()
			elif zaman is not None:
				row["tr"].Hide()
				row["fl"].Hide()
				row["pc"].SetText(zaman)
				row["pc"].Show()
			else:
				row["tr"].Hide()
				row["fl"].Hide()
				row["pc"].Hide()
			if self.tab == "odul" and (j == self.vurgu or j == self.sel):
				row["hl"].SetColor(0x40e8d08a if j == self.vurgu else 0x22e8d08a)
				row["hl"].Show()
			else:
				row["hl"].Hide()
			if self.tab == "odul":
				row["hit"].Show()
			else:
				row["hit"].Hide()
		if not items:
			self.bosT.SetText("Hen\xfcz \xe7evirmedin." if self.tab == "gecmis" else "Hen\xfcz kazanan yok.")
			self.bosT.Show()
		else:
			self.bosT.Hide()

	def __Wrap(self, txt, maxw):
		"""a\xe7\xfdklamay\xfd 2 sat\xfdra b\xf6l (TextLine sarmaz); geni\xfelik yaz\xfd tipiyle \xf6l\xe7\xfcl\xfcr."""
		t = self.detAc1
		txt = txt.replace("\n", " ").replace("|", " ")
		words = txt.split(" ")
		lines = [""]
		for wd in words:
			if not wd:
				continue
			cand = (lines[-1] + " " + wd).strip()
			t.SetText(cand)
			(w, h) = t.GetTextSize()
			if w > maxw and lines[-1]:
				if len(lines) == 2:
					lines[-1] = lines[-1] + "..."
					break
				lines.append(wd)
			else:
				lines[-1] = cand
		while len(lines) < 2:
			lines.append("")
		return lines

	def __Detail(self):
		if M.N() < 1:
			return
		i = min(self.sel, M.N() - 1)
		o = M.odul[i]
		nd = o["n"]
		self.__SetItemImg(self.detIc, M.IkonV(i))
		if self.detIc._yol:
			self.__Center(self.detIc, (DET[0] + 10 + 23) * self.z, (DET[1] + 9 + 23) * self.z)
		if o["tur"] == 1:
			ad, adet = "%s Yang" % _nokta(o["a"]), ""
		else:
			ad, adet = M.Ad(i), ("x%d" % o["a"]) if (o["tur"] == 0 or o["a"] > 1) else ""
		self.detAd.SetText(ad)
		self.detAd.SetPackedFontColor(NADR[nd])
		(w, h) = self.detAd.GetTextSize()
		self.detAdet.SetText(adet)
		self.detAdet.SetPosition(self.P(DET[0] + 66) + w + self.P(6), self.P(DET[1] + 9))
		self.detNd.SetText(NAD[nd].upper())
		self.detNd.SetPackedFontColor(NADR[nd])
		(l1, l2) = self.__Wrap(M.Aciklama(i), self.P(DET[2] - 76))
		self.detAc1.SetText(l1)
		self.detAc2.SetText(l2)
		s = M.Sans(i)
		self.detSt.SetText("\xc7\xfdkma \xfeans\xfd %%%s  \xb7  ortalama %d g\xfcnde bir" % (("%.1f" % s).rstrip("0").rstrip("."), int(round(100.0 / max(0.1, s)))))
