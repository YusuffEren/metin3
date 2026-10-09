# -*- coding: latin-1 -*-
# MOBIL - YENI DOSYA (mobile_root/uizindangiris.py): RAZADOR / NEMERE ZINDAN GIRIS PENCERESI - KLASIK.
# URETILIR: tools/zindan_klasik/uizindangiris_kaynak.py (UTF-8) -> gen_uizindangiris.py (Turkce harfler cp1254 kacis).
#
# Tasarim : Desktop/Averos2-Zindan-Prototip/zindan_klasik.html (KULLANICI 2026-10-01 "tamam begendim uygula").
#           Eski tasarim (tek parca frame_*.png 2 x 5,9 MB) tools/zindan_klasik/yedek_20261001'de.
# Zemin   : oyunun klasik pencereleri gibi pack parcalarindan DOSENIR (Board, TitleBar, ThinBoard, horizontalbar,
#           slot_base) - tek parca doku yok. Kucuk seritler: mobile/ui/zindan/k_*.png (bake_zindan_klasik.py, TEX_S 2.4).
# Veri    : sunucu quest'i zindan_giris.lua NPC'ye (20394 Razador / 20395 Nemere) dokununca cmdchat ile grup durumunu
#           gonderir -> game.py "ZindanGiris"/"ZindanUye"/"ZindanGoster" -> bu pencere.
#           "Zindana Gir" -> event.QuestButtonClick(-2147483648 + qid) -> sunucu yeniden dogrular, bileti alir,
#           grubu isinlar ve "ZindanGirildi" gonderir (parlama + yazi).
#           "ZindanQid" giriste gelir; 2 sn sonra ayni yolla "ben mobilim" bildirilir (sunucu PC'ye eski diyalogu acar).
# Animasyon: acilis .55 s (belirme + asagidan kayma; tum pencere tek kap 'pen' ile kayar), sart satirlari 90 ms
#           arayla belirir, amblem halkasi 12 s'de bir doner, hazirken "Zindana Gir" nabiz + parilti.
# TUZAK: C++ penceresi Python referansi dusunce silinir -> her cocuk self.keep'te.
# TUZAK: TextLine 18 pt ustu motorda buyutulur (bulanik) -> buyuk yazilar k_*.png seridi, digerleri <= 18.
import ui
import wndMgr
import app
import math
import event

DIR = "mobile/ui/zindan/"
PAT = "d:/ymir work/ui/pattern/"
PUB = "d:/ymir work/ui/public/"
TEX_S = 2.4			# k_*.png: tasarim px x 2.4
OLD_S = 0.5			# eski dokular (amblem, halka, parilti, parlama): tasarim px x 2
WIN_W = 760.0
WIN_H = 508.0
MIN_LV = 90
MIN_PARTY = 3
ROWS = 5
OPEN_SEC = 0.55
CLOSE_SEC = 0.3
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")

# PARCA EKLEMI (2026-10-04, KULLANICI: "arkadasimin telefonunda sagda bir cizgi cikiyor"): kesirli pencere olceginde parcalar
# uc uca konunca sinir yuvarlanir (konum tam sayi, uzunluk kesirli) -> 0,3-1,5 px bosluk; ekran cozunurlugune gore GORUNEN
# cizgi. Cozum: her parca YUVARLANMIS iki kenar arasina oturur (olcek = hedef uzunluk / texel sayisi) ve komsusunun altina
# TASMA kadar tasar. Motor RenderingRect'i LONG texele KESER -> oran yarim texel payli verilir (float32 yuvarlamasi kesmeyi
# degistiremez). Denetim: tools/ortak/doseme_denetim.py (pencerenin sahte-motor testine bagli; bosluk kalirsa test KIRMIZI).
TASMA = 0.02


def _Otur(D, w, tex, s, rrs, z):
	"""D: hedef uzunluk (tam sayi mantiksal px) | w: prototip uzunluk | tex: doku texeli | s: prototip olcegi (texel -> px)
	z: pencere olcegi (yalniz eski APK yolu). Donus: (SetScale degeri, SetRenderingRect orani)."""
	t = w / float(s) - tex
	n = int(t + 0.01) if t >= 0 else -int(-t + 0.01)
	if tex + n < 1:
		n = 1 - tex
	if rrs:
		oran = 0.0 if n == 0 else (n + (0.5 if n > 0 else -0.5)) / float(tex)
		return ((D + TASMA) / float(tex + n), oran)
	e = int(round(D - tex * s * z))		# eski APK: ek uzunluk OLCEKSIZ piksel (tam sayi)
	oran = 0.0 if e == 0 else (e + (0.5 if e > 0 else -0.5)) / float(tex)
	return ((D + TASMA - e) / float(tex), oran)
DEBUG_DEMO = 0			# GECICI TEST: 1 = girisden 8 sn sonra ornek veriyle ac (yayinda 0)

C_CREAM = 0xfff1e6c0
C_SUB = 0xffc9b88f
C_OFF = 0xff8f8470
C_GOLD = 0xffe8d08a
C_BAD = 0xfff0907a
C_LINE = 0xff3d342a

JOB = {0: "Sava\xfe\xe7\xfd", 1: "Ninja", 2: "Sura", 3: "\xdeaman"}
FACE = {0: "warrior_m", 1: "assassin_w", 2: "sura_m", 3: "shaman_w"}
D = {
	1: {"k": "razador", "bilet": 71178, "ad": "Razador Ge\xe7it Bileti", "bekci": "Ate\xfe Diyar\xfd Bek\xe7isi",
	    "acik": "Yaln\xfdzca g\xfc\xe7l\xfc bir grup girebilir. Giri\xfe i\xe7in grup lideri bileti kullan\xfdr.",
	    "toast": "RAZADOR KALES\xdd'NE G\xddR\xddL\xddYOR", "acc": 0x59ff7a45},
	2: {"k": "nemere", "bilet": 71179, "ad": "Nemere Ge\xe7it Bileti", "bekci": "Buz Da\xf0\xfd Muhaf\xfdz\xfd",
	    "acik": "Yaln\xfdzca g\xfc\xe7l\xfc bir grup girebilir. Giri\xfe i\xe7in grup lideri bileti kullan\xfdr.",
	    "toast": "NEMERE G\xd6ZLEMEV\xdd'NE G\xddR\xddL\xddYOR", "acc": 0x598fd3ff},
}

## TELEFONDA OLCULDU (2026-10-01): mobile/ .png dokularda GetWidth() yuklenme aninda 0 donuyor -> ortalama, halka
## donme merkezi, yazi hizasi kayiyordu ("donen halka kaymis, yazilar ust uste"). Boyutlar SABIT (bake_zindan_klasik).
TEX_SIZE = {
	"emblem_nemere.png": (235, 224), "emblem_razador.png": (235, 224), "ring.png": (170, 170), "shine.png": (142, 80),
	"k_btn_gir_glow.png": (355, 86), "k_btn_gir_off.png": (355, 86), "k_btn_gir_on.png": (355, 86),
	"k_btn_vazgec.png": (250, 86), "k_close.png": (54, 54), "k_dot_bad.png": (24, 24), "k_dot_ok.png": (24, 24),
	"k_eksik.png": (91, 31), "k_isr_bad.png": (40, 40), "k_isr_ok.png": (40, 40),
	"k_serit_nemere.png": (552, 49), "k_serit_razador.png": (504, 49),
	"k_title_nemere.png": (394, 51), "k_title_razador.png": (314, 51),
}

# ---- yerlesim (tasarim px, pencerenin sol-ustune gore; prototip ile ayni)
SERIT = (18, 48, 724, 70)
AMB_C = (59.0, 83.0)
AMB_D = 54.0
SART_BOX = (18, 159, 352, 152)
SINIF_Y, SINIF_H = 349, 93
GRUP_BOX = (388, 159, 354, 167)
BILET_BOX = (388, 364, 354, 78)
BTN_VAZGEC = (480, 454, 104, 36)
BTN_GIR = (594, 454, 148, 36)
XBTN = (723.5, 13, 22.5, 22.5)


def _ease_out3(t):
	t = max(0.0, min(1.0, t))
	return 1.0 - (1.0 - t) ** 3


def _bump(t, peak):
	if t <= 0.0 or t >= 1.0:
		return 0.0
	if t < peak:
		return t / peak
	return 1.0 - (t - peak) / (1.0 - peak)


def _cut(s, n):
	return s if len(s) <= n else s[:n - 2] + ".."


class ZindanGirisWindow(ui.Window):
	def __init__(self):
		# TOP_MOST: "UI" katmanindaki kok pencere kare guncellemesi (OnUpdate) almiyordu (telefonda olculdu);
		# dokunma efekti (uitapfx) gibi en ust katman - quest diyaloglarinin da ustunde durur.
		ui.Window.__init__(self, "TOP_MOST")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("ZindanGirisWindow")
		self.keep = []
		self.items = []
		self.qid = -1
		self.hsT = -1.0			# el sikisma zamani
		self.tip = 1
		self.lider = 0
		self.bilet = 0
		self.uyeler = []
		self.allOk = False
		self.state = "kapali"
		self.animT0 = 0.0
		self.built = False
		self.dirty = True
		self.fxT0 = -1.0
		self.fxTip = 1
		self.openT = -100.0		# son Open() zamani (gorev diyalogu yutma penceresi)
		# kok pencere her zaman gorunur (el sikisma + giris parlamasi icin OnUpdate), ama not_pick
		W = wndMgr.GetScreenWidth()
		H = wndMgr.GetScreenHeight()
		self.W = W
		self.H = H
		self.SetSize(W, H)
		self.SetPosition(0, 0)
		self.AddFlag("not_pick")
		self.__BuildFx()
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.keep = []
		self.items = []

	# ------------------------------------------------------------------ sunucu verisi
	def SetQuestIndex(self, qid):
		self.qid = qid
		self.hsT = app.GetTime() + 2.0

	def Begin(self, tip, lider, bilet, n):
		self.tip = tip if tip in D else 1
		self.lider = lider
		self.bilet = bilet
		self.uyeler = []

	def AddMember(self, ad, job, lv, lider, yakin):
		self.uyeler.append({"ad": ad.replace("_", " "), "j": job % 4, "lv": lv, "lider": lider, "yakin": yakin})

	def Entered(self, tip):
		self.fxTip = tip if tip in D else 1
		self.fxT0 = app.GetTime()
		self.Close()

	# ------------------------------------------------------------------ yardimcilar (pen icinde, tasarim px)
	def __Layout(self):
		# KULLANICI (2026-09-25): "pencere uzak kaliyor, yakinlasmali" -> ekrana gore buyut (yukseklik %97, genislik %92)
		k = min(0.97 * self.H / WIN_H, 0.92 * self.W / WIN_W)
		self.k = k
		self.ox = int((self.W - WIN_W * k) / 2)
		self.oy = int((self.H - WIN_H * k) / 2)

	def __P(self, x, y):
		return (int(round(x * self.k)), int(round(y * self.k)))

	def __Reg(self, w, t, c=0, a=1.0, grp=-1):
		it = {"w": w, "t": t, "c": c, "a": a, "grp": grp}
		self.items.append(it)
		return it

	def __Raw(self, path, x, y, sc, grp=-1):
		"""doku: sc = texel -> tasarim px"""
		w = ui.ExpandedImageBox()
		w.SetParent(self.pen)
		w.AddFlag("not_pick")
		w.LoadImage(path)
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		w.SetScale(sc * self.k, sc * self.k)
		w.SetPosition(*self.__P(x, y))
		w.Show()
		self.keep.append(w)
		it = self.__Reg(w, "img", grp=grp)
		sz = TEX_SIZE.get(path.split("/")[-1])
		if sz is None:
			sz = (w.GetWidth(), w.GetHeight())
		it["tw"] = float(max(1, sz[0]))
		it["th"] = float(max(1, sz[1]))
		it["sc"] = sc
		return it

	def __K(self, name, x, y, grp=-1):
		return self.__Raw(DIR + name, x, y, 1.0 / TEX_S, grp)

	def __KC(self, name, cx, cy, grp=-1):
		"""k_ dokusu merkezden"""
		it = self.__K(name, 0, 0, grp)
		it["w"].SetPosition(*self.__P(cx - it["tw"] / TEX_S / 2.0, cy - it["th"] / TEX_S / 2.0))
		return it

	def __Tile(self, path, x, y, w, h, tw, th, sx=1.0, sy=1.0):
		"""tw x th texel dokuyu (x, y, w, h) alanina DOSER (UV tekrari, ui.Board gibi); kenarlar __P(x) .. __P(x + w)
		tam sayisina OTURUR (bkz. _Otur) -> komsu parcalarla arada bosluk kalmaz"""
		it = self.__Raw(path, x, y, 1.0)
		img = it["w"]
		(x0, y0) = self.__P(x, y)
		(x1, y1) = self.__P(x + w, y + h)
		(zx, r) = _Otur(x1 - x0, w, tw, sx, HAS_RRS, self.k)
		(zy, b) = _Otur(y1 - y0, h, th, sy, HAS_RRS, self.k)
		img.SetScale(zx, zy)
		img.SetRenderingRect(0.0, 0.0, r, b)
		return it

	def __TileTam(self, path, x, y, w, h, t, yatay, dikey):
		"""YARI SAYDAM parca (ThinBoard): kenarlar __P(x, y) .. __P(x + w, y + h) TAM SAYISINA oturur, tasma YOK (ust uste
		binen yari saydam parcalar koyu cizgi yapar). Doseme yonunde olcek 1 + OLCEKSIZ RenderingRect (tam piksel); diger
		yonde olcek = hedef / t (t = 16 texel = 2'nin kuvveti -> carpim float'ta TAM). yatay / dikey: doseme yonu."""
		it = self.__Raw(path, x, y, 1.0)
		img = it["w"]
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(img.hWnd, 0)
		(x0, y0) = self.__P(x, y)
		(x1, y1) = self.__P(x + w, y + h)
		dx = max(1, x1 - x0)
		dy = max(1, y1 - y0)
		r = 0.0
		b = 0.0
		if yatay and dx != t:
			r = (dx - t + (0.5 if dx > t else -0.5)) / float(t)
		if dikey and dy != t:
			b = (dy - t + (0.5 if dy > t else -0.5)) / float(t)
		img.SetScale(1.0 if yatay else dx / float(t), 1.0 if dikey else dy / float(t))
		img.SetRenderingRect(0.0, 0.0, r, b)
		return it

	def __PImg(self, path, x, y, sx=1.0, sy=1.0):
		it = self.__Raw(path, x, y, 1.0)
		it["w"].SetScale(sx * self.k, sy * self.k)
		return it

	def __Box(self, x, y, w, h, color, fill=False, grp=-1):
		b = ui.Bar() if fill else ui.Box()
		b.SetParent(self.pen)
		b.AddFlag("not_pick")
		b.SetColor(color)
		b.SetPosition(*self.__P(x, y))
		b.SetSize(max(1, int(round(w * self.k))), max(1, int(round(h * self.k))))
		b.Show()
		self.keep.append(b)
		return self.__Reg(b, "bar", color, grp=grp)

	def __Txt(self, x, y, pt, color, align="left", grp=-1, vc=True):
		t = ui.TextLine()
		t.SetParent(self.pen)
		t.AddFlag("not_pick")
		t.SetFontName("Tahoma:%d" % max(9, min(18, int(round(pt * self.k)))))		# 18 ustu bulanik
		if align == "center":
			t.SetHorizontalAlignCenter()
		elif align == "right":
			t.SetHorizontalAlignRight()
		if vc:
			t.SetVerticalAlignCenter()
		t.SetOutline()
		t.SetPosition(*self.__P(x, y))
		t.Show()
		self.keep.append(t)
		return self.__Reg(t, "txt", color, grp=grp)

	def __Bold(self, x, y, pt, color, align="left"):
		"""kalin gorunum: ayni yazi 1 px kaydirmali iki kez (motorda kalin font yok)"""
		a = self.__Txt(x, y, pt, color, align)
		b = self.__Txt(x, y, pt, color, align)
		px, py = self.__P(x, y)
		a["w"].SetPosition(px + max(1, int(round(self.k))), py)
		return (a, b)

	def __Board(self, W, H):
		self.__Tile(PAT + "board_base.tga", 32, 32, W - 64, H - 64, 128, 128)
		self.__Tile(PAT + "board_line_top.tga", 32, 0, W - 64, 32, 128, 32)
		self.__Tile(PAT + "board_line_bottom.tga", 32, H - 32, W - 64, 32, 128, 32)
		self.__Tile(PAT + "board_line_left.tga", 0, 32, 32, H - 64, 32, 128)
		self.__Tile(PAT + "board_line_right.tga", W - 32, 32, 32, H - 64, 32, 128)
		for (n, cx, cy) in (("lefttop", 0, 0), ("righttop", W - 32, 0), ("leftbottom", 0, H - 32), ("rightbottom", W - 32, H - 32)):
			self.__Tile(PAT + "board_corner_%s.tga" % n, cx, cy, 32, 32, 32, 32)

	def __ThinBoard(self, x, y, w, h):
		# YARI SAYDAM: parcalar ne bosluk birakmali ne ust uste binmeli -> butun kenarlar TAM SAYI (bkz. __TileTam)
		c = 16.0
		(fx0, fy0) = self.__P(x + c, y + c)
		(fx1, fy1) = self.__P(x + w - c, y + h - c)
		dolgu = self.__Box(x + c, y + c, w - 2 * c, h - 2 * c, 0x82000000, fill=True)
		dolgu["w"].SetSize(max(1, fx1 - fx0), max(1, fy1 - fy0))
		self.__TileTam(PAT + "thinboard_line_top.tga", x + c, y, w - 2 * c, c, 16, True, False)
		self.__TileTam(PAT + "thinboard_line_bottom.tga", x + c, y + h - c, w - 2 * c, c, 16, True, False)
		self.__TileTam(PAT + "thinboard_line_left.tga", x, y + c, c, h - 2 * c, 16, False, True)
		self.__TileTam(PAT + "thinboard_line_right.tga", x + w - c, y + c, c, h - 2 * c, 16, False, True)
		for (n, cx, cy) in (("lefttop", x, y), ("righttop", x + w - c, y), ("leftbottom", x, y + h - c), ("rightbottom", x + w - c, y + h - c)):
			self.__TileTam(PAT + "thinboard_corner_%s.tga" % n, cx, cy, c, c, 16, False, False)

	def __HBar(self, x, y, w, title):
		"""bolum basligi: klasik horizontalbar (32 texel -> 24 tasarim px) + altin yazi"""
		s = 0.75
		self.__Tile(PAT + "horizontalbar_center.tga", x + 24, y, w - 48, 24, 32, 32, s, s)
		self.__Tile(PAT + "horizontalbar_left.tga", x, y, 24, 24, 32, 32, s, s)
		self.__Tile(PAT + "horizontalbar_right.tga", x + w - 24, y, 24, 24, 32, 32, s, s)
		h = self.__Txt(x + 12, y + 12, 12, C_GOLD)
		h["w"].SetText(title)
		return h

	def __Kutu(self, x, y, w, h):
		self.__Box(x - 1, y - 1, w + 2, h + 2, 0xff000000)
		self.__Box(x, y, w, h, 0x73000000, fill=True)
		self.__Box(x, y, w, h, C_LINE)

	def __Satir(self, x, y, w, h, grp=-1):
		return (self.__Box(x, y, w, h, 0x09ffffff, fill=True, grp=grp), self.__Box(x, y, w, h, 0xcc3d342a, grp=grp))

	# ------------------------------------------------------------------ kurulum
	def __Build(self):
		self.__Layout()
		self.items = []
		k = self.k
		body = ui.Window()
		body.SetParent(self)
		body.SetSize(self.W, self.H)
		body.SetPosition(0, 0)
		self.keep.append(body)
		self.body = body
		# dokunma yakalayici: pencere disina dokunma = kapat
		catcher = _Catcher(self)
		catcher.SetParent(body)
		catcher.SetSize(self.W, self.H)
		catcher.SetPosition(0, 0)
		catcher.Show()
		self.keep.append(catcher)
		# pencere kabi: tum parcalar bunun cocugu (acilis kaymasi tek SetPosition)
		pen = ui.Window()
		pen.SetParent(body)
		pen.SetSize(int(WIN_W * k), int(WIN_H * k))
		pen.SetPosition(self.ox, self.oy)
		pen.Show()
		self.keep.append(pen)
		self.pen = pen
		## pencere govdesi dokunmayi yutar. DIKKAT: secim sirasi = OLUSTURMA sirasi (sonraki ustte) -> govde en once,
		## dugme dokunma alanlari en sonda (KULLANICI 2026-09-25 "butonlara tiklanmiyor").
		self.hitWin = self.__Hit((0, 0, WIN_W, WIN_H), None)

		# ---- zemin: Board + TitleBar (x1.5; 34.5 = 23 dolu satir, ayrica kesme YOK)
		self.__Board(int(WIN_W), int(WIN_H))
		self.__Tile(PAT + "titlebar_center.tga", 8 + 48, 8, WIN_W - 16 - 96, 34.5, 32, 32, 1.5, 1.5)
		self.__Tile(PAT + "titlebar_left.tga", 8, 8, 48, 34.5, 32, 32, 1.5, 1.5)
		self.__Tile(PAT + "titlebar_right.tga", WIN_W - 8 - 48, 8, 48, 34.5, 32, 32, 1.5, 1.5)
		self.title = {}
		self.serit = {}
		for tip in D:
			dn = D[tip]["k"]
			t = self.__K("k_title_%s.png" % dn, 46, 0)
			t["w"].SetPosition(*self.__P(46, 22 - t["th"] / TEX_S / 2.0))
			self.title[tip] = t
		self.bekci = self.__Txt(0, 22, 12, C_SUB)
		self.xbtn = self.__K("k_close.png", XBTN[0], XBTN[1])

		# ---- ust serit: ThinBoard + amblem (doner halka) + baslik + aciklama + sart sayaci
		self.__ThinBoard(*SERIT)
		s = AMB_D / 85.0
		self.ring = self.__Raw(DIR + "ring.png", AMB_C[0] - 42.5 * s, AMB_C[1] - 42.5 * s, OLD_S * s)
		self.emb = {}
		for tip in D:
			self.emb[tip] = self.__Raw(DIR + "emblem_%s.png" % D[tip]["k"], AMB_C[0] - 56.0 * s, AMB_C[1] - 50.5 * s, OLD_S * s)
		for tip in D:
			t = self.__K("k_serit_%s.png" % D[tip]["k"], 100, 0)
			t["w"].SetPosition(*self.__P(100, 74 - t["th"] / TEX_S / 2.0))
			self.serit[tip] = t
		self.acik = self.__Txt(100, 93, 12, C_SUB)
		self.okCount = self.__Bold(722, 74, 13.3, C_GOLD, "right")
		lbl = self.__Txt(722, 94, 10, C_OFF, "right")
		lbl["w"].SetText("\xdeART")

		# ---- sol: giris sartlari
		self.__HBar(18, 128, 352, "G\xddR\xdd\xde \xdeARTLARI")
		bx, by, bw, bh = SART_BOX
		self.__Kutu(bx, by, bw, bh)
		self.req = []
		for i in range(5):
			x, y, w, h = bx + 5, by + 5 + i * 29, bw - 10, 26
			r = {}
			self.__Satir(x, y, w, h, grp=i)
			r["ok"] = self.__KC("k_isr_ok.png", x + 16, y + 13, grp=i)
			r["bad"] = self.__KC("k_isr_bad.png", x + 16, y + 13, grp=i)
			r["t"] = self.__Txt(x + 32, y + 13, 13, C_CREAM, grp=i)
			r["v"] = self.__Txt(x + w - 8, y + 13, 11, C_SUB, "right", grp=i)
			self.req.append(r)

		# ---- sol: siniflar (Savasci, Ninja, Saman)
		h = self.__HBar(18, 318, 352, "SINIFLAR")
		u = self.__Txt(18 + 352 - 12, 318 + 12, 11, C_SUB, "right")
		u["w"].SetText("Sava\xfe\xe7\xfd \xb7 Ninja \xb7 \xdeaman")
		self.cls = []
		cw = (352 - 12) / 3.0
		for n, j in enumerate((0, 1, 3)):
			x = 18 + n * (cw + 6)
			c = {"j": j}
			self.__Box(x - 1, SINIF_Y - 1, cw + 2, SINIF_H + 2, 0xff000000)
			self.__Box(x, SINIF_Y, cw, SINIF_H, 0x73000000, fill=True)
			c["edge"] = self.__Box(x, SINIF_Y, cw, SINIF_H, C_LINE)
			cx = x + cw / 2.0
			self.__PImg(PUB + "slot_base.sub", cx - 22, SINIF_Y + 15, 44 / 32.0, 44 / 32.0)
			c["face"] = self.__Raw("icon/face/%s.tga" % FACE[j], cx - 18.5, SINIF_Y + 18.5, 37 / 43.0)
			c["ad"] = self.__Txt(cx, SINIF_Y + 71, 12, C_CREAM, "center")
			c["ad"]["w"].SetText(JOB[j])
			c["miss"] = self.__KC("k_eksik.png", cx, SINIF_Y)
			self.cls.append(c)

		# ---- sag: grup
		self.__HBar(388, 128, 354, "GRUBUN")
		self.partyCount = self.__Txt(388 + 354 - 12, 128 + 12, 11, C_SUB, "right")
		gx, gy, gw, gh = GRUP_BOX
		self.__Kutu(gx, gy, gw, gh)
		self.rows = []
		for i in range(ROWS):
			x, y, w, h = gx + 5, gy + 5 + i * 31, gw - 10, 28
			cy = y + h / 2.0
			r = {"x": x, "y": y}
			r["bg"] = self.__Satir(x, y, w, h)
			r["face"] = {}
			self.__Box(x + 3, cy - 12, 24, 24, 0xff000000)
			for j in FACE:
				r["face"][j] = self.__Raw("icon/face/%s.tga" % FACE[j], x + 3, cy - 12, 24 / 43.0)
			r["ad"] = self.__Txt(x + 35, cy, 13, C_CREAM)
			r["lider"] = self.__Txt(x + 35, cy, 10, C_GOLD)
			r["lider"]["w"].SetText("L\xddDER")
			r["lv"] = self.__Txt(x + w - 25, cy, 11, C_SUB, "right")
			r["dok"] = self.__KC("k_dot_ok.png", x + w - 12.5, cy)
			r["dbad"] = self.__KC("k_dot_bad.png", x + w - 12.5, cy)
			r["bos"] = self.__Txt(x + 10, cy, 12, C_OFF)
			r["bos"]["w"].SetText("\x97 bo\xfe \x97")
			self.rows.append(r)

		# ---- sag: gecit bileti
		self.__HBar(388, 333, 354, "GE\xc7\xddT B\xddLET\xdd")
		tx, ty, tw, th = BILET_BOX
		self.__ThinBoard(tx, ty, tw, th)
		sx, sy = tx + 20, ty + 16
		self.__PImg(PUB + "slot_base.sub", sx, sy, 46 / 32.0, 46 / 32.0)
		self.icon = {}
		for tip in D:
			w = ui.ExpandedImageBox()
			w.SetParent(self.pen)
			w.AddFlag("not_pick")
			try:
				w.LoadImage("icon/item/%d.tga" % D[tip]["bilet"])
			except:
				pass
			iw = float(w.GetWidth())
			ih = float(w.GetHeight())
			if iw <= 1 or ih <= 1:		# yuklenmemis (0) -> HD ikon boyu
				iw = ih = 128.0
			sc = 32.0 / max(iw, ih)
			if HAS_RRS:
				wndMgr.SetRenderingRectScaled(w.hWnd, 1)
			w.SetScale(sc * k, sc * k)
			w.SetPosition(*self.__P(sx + 23 - iw * sc / 2.0, sy + 23 - ih * sc / 2.0))
			w.Show()
			self.keep.append(w)
			self.icon[tip] = self.__Reg(w, "img")
		self.cnt = self.__Txt(sx + 43, sy + 38, 11, 0xffffffff, "right")
		self.t1 = self.__Txt(sx + 56, sy + 14, 13, C_GOLD)
		self.t2 = self.__Txt(sx + 56, sy + 32, 11, C_SUB)

		# ---- alt: not + dugmeler
		self.note = self.__Txt(18, 472, 12, C_BAD)
		self.__K("k_btn_vazgec.png", BTN_VAZGEC[0], BTN_VAZGEC[1])
		self.bOff = self.__K("k_btn_gir_off.png", BTN_GIR[0], BTN_GIR[1])
		self.bGo = self.__K("k_btn_gir_on.png", BTN_GIR[0], BTN_GIR[1])
		self.bGlow = self.__K("k_btn_gir_glow.png", BTN_GIR[0], BTN_GIR[1])
		self.shine = self.__Raw(DIR + "shine.png", BTN_GIR[0], BTN_GIR[1], OLD_S * 36.0 / 40.0)
		# dokunma alanlari (gorseller not_pick) - EN SONDA
		self.hitCancel = self.__Hit(BTN_VAZGEC, self.Close, 4)
		self.hitX = self.__Hit(XBTN, self.Close, 8)
		self.hitEnter = self.__Hit(BTN_GIR, self.__OnEnter, 4)
		self.built = True

	def __Hit(self, g, func, pad=0):
		h = _Hit(func)
		h.SetParent(self.pen)
		x, y = self.__P(g[0] - pad, g[1] - pad)
		h.SetPosition(x, y)
		h.SetSize(int((g[2] + 2 * pad) * self.k), int((g[3] + 2 * pad) * self.k))
		h.Show()
		self.keep.append(h)
		return h

	def __BuildFx(self):
		self.fxKeep = []
		self.flash = {}
		for dn in ("razador", "nemere"):
			w = ui.ExpandedImageBox()
			w.SetParent(self)
			w.AddFlag("not_pick")
			w.LoadImage(DIR + "flash_%s.png" % dn)
			w.Hide()
			self.fxKeep.append(w)
			self.flash[dn] = (w, float(w.GetWidth()), float(w.GetHeight()))
		t = ui.TextLine()
		t.SetParent(self)
		t.AddFlag("not_pick")
		t.SetFontName("Tahoma:%d" % max(12, min(18, int(round(16 * min(self.W / 1280.0, self.H / 705.0))))))
		t.SetHorizontalAlignCenter()
		t.SetOutline()
		t.Hide()
		self.fxKeep.append(t)
		self.toast = t

	# ------------------------------------------------------------------ durum
	def __Eval(self):
		u = self.uyeler
		has = lambda j: any(m["j"] == j for m in u)
		low = [m["ad"] for m in u if m["lv"] < MIN_LV]
		far = [m["ad"] for m in u if not m["yakin"]]
		miss = [JOB[j] for j in (0, 1, 3) if not has(j)]
		grup = len(u) >= 2
		r = [
			(grup and len(u) >= MIN_PARTY, "Grup en az 3 ki\xfei", "%d ki\xfei" % len(u),
			 (grup and "Grup en az 3 ki\xfei olmal\xfd, \xfeu an %d ki\xfei." % len(u)) or "\xd6nce bir grup kurmal\xfds\xfdn."),
			(not low, "Herkes %d seviye ve \xfcst\xfc" % MIN_LV, (low and ", ".join(low)) or "tamam",
			 ", ".join(low) + " hen\xfcz %d seviye de\xf0il." % MIN_LV),
			(not miss, "Sava\xfe\xe7\xfd, Ninja ve \xdeaman grupta", (miss and ", ".join(miss)) or "tamam",
			 "Grupta " + " ve ".join(miss) + " yok."),
			(not far, "Herkes bek\xe7inin yan\xfdnda", (far and ", ".join(far)) or "tamam",
			 ", ".join(far) + " bek\xe7inin yan\xfdna gelmeli."),
			(self.bilet > 0, "Liderde 1 ge\xe7it bileti", "%d adet" % self.bilet,
			 "Envanterinde ge\xe7it bileti yok."),
		]
		return r, has

	def __Refresh(self):
		r, has = self.__Eval()
		self.allOk = all(x[0] for x in r) and self.lider == 1
		self.gmTest = (self.lider == 2)
		if self.gmTest:
			self.allOk = self.bilet > 0		# GM test: sunucu yalniz bileti arar
		# zindan varyantlari
		for tip in D:
			on = (tip == self.tip)
			for it in (self.title[tip], self.serit[tip], self.emb[tip], self.icon[tip]):
				it["a"] = 1.0 if on else 0.0
		dd = D[self.tip]
		# baslik yanindaki bekci adi: baslik seridinin sagindan 12 px
		tt = self.title[self.tip]
		self.bekci["w"].SetText(dd["bekci"])
		self.bekci["w"].SetPosition(*self.__P(46 + tt["tw"] / TEX_S + 12, 22))
		self.acik["w"].SetText(dd["acik"])
		# sartlar
		okN = 0
		for i in range(5):
			ok, t, v, m = r[i]
			if ok:
				okN += 1
			self.req[i]["ok"]["a"] = 1.0 if ok else 0.0
			self.req[i]["bad"]["a"] = 0.0 if ok else 1.0
			self.req[i]["t"]["w"].SetText(t)
			self.req[i]["t"]["c"] = C_CREAM if ok else C_BAD
			self.req[i]["v"]["w"].SetText(_cut(v, 18))
		for it in self.okCount:
			it["w"].SetText("%d / 5" % okN)
		# siniflar
		for c in self.cls:
			h = has(c["j"])
			c["miss"]["a"] = 0.0 if h else 1.0
			c["face"]["a"] = 1.0 if h else 0.3
			c["ad"]["c"] = C_CREAM if h else C_OFF
			c["edge"]["c"] = ((dd["acc"] & 0xffffff) | 0xa0000000) if h else C_LINE
		self.partyCount["w"].SetText("%d ki\xfei" % len(self.uyeler))
		# grup satirlari
		for i in range(ROWS):
			row = self.rows[i]
			m = self.uyeler[i] if i < len(self.uyeler) else None
			more = (i == ROWS - 1 and len(self.uyeler) > ROWS)
			vis = m is not None
			for it in row["bg"]:
				it["a"] = 1.0 if vis else 0.35
			row["bos"]["a"] = 0.0 if vis else 0.5
			for it in (row["ad"], row["lv"], row["dok"], row["dbad"], row["lider"]):
				it["a"] = 1.0 if vis else 0.0
			for j in row["face"]:
				row["face"][j]["a"] = 1.0 if (vis and not more and m["j"] == j) else 0.0
			if not vis:
				continue
			if more:
				row["ad"]["w"].SetText("+%d ki\xfei daha" % (len(self.uyeler) - ROWS + 1))
				row["ad"]["c"] = C_SUB
				row["lv"]["a"] = 0.0
				row["lider"]["a"] = 0.0
				row["dok"]["a"] = 0.0
				row["dbad"]["a"] = 0.0
				continue
			bad = m["lv"] < MIN_LV or not m["yakin"]
			row["ad"]["w"].SetText(_cut(m["ad"], 20))
			row["ad"]["c"] = C_CREAM
			row["lv"]["w"].SetText("Lv %d" % m["lv"])
			row["lv"]["c"] = C_BAD if m["lv"] < MIN_LV else C_SUB
			row["dok"]["a"] = 0.0 if bad else 1.0
			row["dbad"]["a"] = 1.0 if bad else 0.0
			row["lider"]["a"] = 1.0 if m["lider"] else 0.0
			if m["lider"]:
				try:
					(tw, th) = row["ad"]["w"].GetTextSize()
				except:
					tw = len(m["ad"]) * 7 * self.k
				row["lider"]["w"].SetPosition(*self.__P(row["x"] + 35 + tw / self.k + 9, row["y"] + 14))
		# bilet
		self.cnt["w"].SetText(str(self.bilet) if self.bilet > 0 else "")
		self.icon[self.tip]["a"] = 1.0 if self.bilet > 0 else 0.35
		self.t1["w"].SetText("%s (%d)" % (dd["ad"], dd["bilet"]))
		self.t2["w"].SetText((self.bilet > 0 and "Giri\xfete liderden 1 adet al\xfdn\xfdr") or "Envanterinde bilet yok")
		self.t2["c"] = C_SUB if self.bilet > 0 else C_BAD
		# not + dugme
		if self.allOk and self.gmTest:
			self.note["w"].SetText("GM test: grup \xfeartlar\xfd atland\xfd.")
			self.note["c"] = C_GOLD
		elif self.allOk:
			self.note["w"].SetText("Grup haz\xfdr. T\xfcm \xfcyeler birlikte i\xe7eri \xfd\xfe\xfdnlanacak.")
			self.note["c"] = C_SUB
		else:
			first = [x for x in r if not x[0]]
			if first:
				self.note["w"].SetText(first[0][3])
			else:
				self.note["w"].SetText("Giri\xfei yaln\xfdzca grup lideri ba\xfelatabilir.")
			self.note["c"] = C_BAD
		self.bOff["a"] = 0.0 if self.allOk else 1.0
		self.bGo["a"] = 1.0 if self.allOk else 0.0
		self.bGlow["a"] = 0.0
		self.shine["a"] = 0.0
		self.dirty = True

	# ------------------------------------------------------------------ ac / kapat
	def Open(self):
		if not self.built:
			self.__Build()
		self.__Refresh()
		self.openT = app.GetTime()
		self.state = "aciliyor"
		self.animT0 = app.GetTime()
		self.body.Show()
		self.SetTop()
		self.__Apply(app.GetTime())

	def Close(self):
		if not self.built or self.state in ("kapali", "kapaniyor"):
			return
		self.state = "kapaniyor"
		self.animT0 = app.GetTime()

	## Sunucu NPC tiklamasinin sonunda bos bir gorev betigi yollar: gercek istemci onu QuestDialog olarak
	## acar -> q.Lock() (TUM dokunmalari yutar) + sinema perdesi bantlari. Telefonda olculdu: pencere
	## gorunuyor ama dugmelere basilamiyor, ust/alt siyah bantlar pencereyi kesiyor. Pencere az once
	## acildiysa o diyalog hic kurulmaz (interfacemodule.OpenQuestWindow burayi sorar).
	def SwallowQuestWindow(self):
		return self.state in ("aciliyor", "acik") and (app.GetTime() - self.openT) < 2.0

	def OnPressEscapeKey(self):
		if self.state in ("acik", "aciliyor"):
			self.Close()
			return True
		return False

	def __OnEnter(self):
		if not self.allOk or self.qid < 0:
			return
		try:
			event.QuestButtonClick(-2147483648 + self.qid)
		except:
			import dbg
			dbg.TraceError("ZindanGiris: QuestButtonClick yok")

	# ------------------------------------------------------------------ kare
	def __Alpha(self, it, a):
		a = max(0.0, min(1.0, a))
		w = it["w"]
		t = it["t"]
		## KULLANICI (2026-10-01): "carpiya basinca yazilarin golgesi ekranda gorunuyor sonra kayboluyor" - motor
		## SetOutline konturunu yazi rengiyle SOLDURMAZ; yazi silikken siyah golgesi kalir. Yazi solmaz: yarida tam
		## renk belirir, kapanista hemen gizlenir.
		if t == "txt":
			a = 1.0 if (a >= 0.5 and self.state != "kapaniyor") else 0.0
		if a <= 0.001:
			if w.IsShow():
				w.Hide()
			return
		if t == "img":
			w.SetAlpha(a)
		elif t == "txt":
			w.SetPackedFontColor((int(a * 255) << 24) | (it["c"] & 0xffffff))
		else:
			ba = (it["c"] >> 24) & 0xff
			w.SetColor((int(ba * a) << 24) | (it["c"] & 0xffffff))
		if not w.IsShow():
			w.Show()

	def __Apply(self, t):
		el = t - self.animT0
		anim = True
		if self.state == "aciliyor":
			p = el / OPEN_SEC
			if p >= 1.0:
				self.state = "acik"
				p = 1.0
			e = _ease_out3(p)
			A = min(1.0, p * 1.6)
			dy = 14.0 * (1.0 - e)
		elif self.state == "kapaniyor":
			p = el / CLOSE_SEC
			if p >= 1.0:
				self.state = "kapali"
				self.body.Hide()
				return
			A = 1.0 - p
			dy = 6.0 * p
		else:
			A = 1.0
			dy = 0.0
			anim = False
		if anim or self.dirty:
			self.dirty = False
			self.pen.SetPosition(self.ox, self.oy + int(round(dy * self.k)))
			for it in self.items:
				a = it["a"] * A
				g = it["grp"]
				if g >= 0 and self.state == "aciliyor":
					a *= max(0.0, min(1.0, (el - 0.12 - g * 0.09) / 0.35))
				self.__Alpha(it, a)
		# amblem halkasi: 12 s / tur
		ring = self.ring
		rw = ring["tw"] * ring["sc"] * self.k
		rh = ring["th"] * ring["sc"] * self.k
		ring["w"].SetOrigin(rw / 2.0, rh / 2.0)
		ring["w"].SetRotation((t % 12.0) * 30.0)
		# hazir dugme: nabiz (acik dugme dokusu) + parilti
		if self.allOk:
			pl = 0.5 - 0.5 * math.cos(t * 2.0 * math.pi / 1.6)
			self.__Alpha(self.bGlow, 0.85 * pl * A)
			# parilti: 2.4 s'de bir soldan saga (dugme icine kirpilir)
			sp = (t % 2.4) / 2.4
			bx0 = BTN_GIR[0] + 6
			bx1 = BTN_GIR[0] + BTN_GIR[2] - 6
			sw = self.shine["tw"] * self.shine["sc"]
			if sp < 0.6:
				x = bx0 - sw + (bx1 - bx0 + sw) * (sp / 0.6)
				lc = max(0.0, bx0 - x) / sw
				rc = max(0.0, (x + sw) - bx1) / sw
				self.shine["w"].SetPosition(*self.__P(x, BTN_GIR[1]))
				s2 = 1.0 if HAS_RRS else self.k * self.shine["sc"]
				self.shine["w"].SetRenderingRect(-lc * s2, 0.0, -rc * s2, 0.0)
				self.__Alpha(self.shine, 0.8 * A)
			else:
				self.shine["w"].Hide()

	def OnUpdate(self):
		t = app.GetTime()
		if DEBUG_DEMO:
			if not hasattr(self, "_demoT"):
				self._demoT = t + 8.0
			elif self._demoT > 0 and t >= self._demoT:
				self._demoT = -1
				self.Begin(DEBUG_DEMO, 1, 3, 4)
				self.AddMember("DracarysX", 0, 105, 1, 1)
				self.AddMember("Muazzam1LAZ", 1, 103, 0, 1)
				self.AddMember("HUKUMDAR", 3, 99, 0, 1)
				self.AddMember("Deneme1", 2, 94, 0, 1)
				self.Open()
		# mobil el sikisma: girisden 2 sn sonra (sunucu PC diyalogu yerine bu pencereyi kullanir)
		if self.hsT > 0.0 and t >= self.hsT and self.qid >= 0:
			self.hsT = -1.0
			try:
				event.QuestButtonClick(-2147483648 + self.qid)
			except:
				pass
		if self.built and self.state != "kapali":
			self.__Apply(t)
		self.__UpdateFx(t)

	def __UpdateFx(self, t):
		if self.fxT0 < 0.0:
			return
		el = t - self.fxT0
		dn = D[self.fxTip]["k"]
		(w, tw, th) = self.flash[dn]
		if el >= 1.6:
			self.fxT0 = -1.0
			w.Hide()
			self.toast.Hide()
			return
		# tasarim: flash 1.2 s (25%'te .9), toast 1.6 s
		p = el / 1.2
		a = 0.9 * _bump(p, 0.25) if p < 1.0 else 0.0
		S = max(self.W, self.H) * 1.6
		sc = S / tw * (0.8 + 0.4 * _ease_out3(min(1.0, p)))
		w.SetScale(sc, sc)
		w.SetPosition(int(self.W / 2 - tw * sc / 2), int(self.H / 2 - th * sc / 2))
		if a > 0.0:
			w.SetAlpha(a)
			w.Show()
		else:
			w.Hide()
		ta = min(1.0, el / 0.3) * (1.0 if el < 1.2 else max(0.0, 1.0 - (el - 1.2) / 0.4))
		self.toast.SetText(D[self.fxTip]["toast"])
		self.toast.SetPosition(int(self.W / 2), int(self.H * (0.14 - 0.02 * min(1.0, el / 0.4))))
		self.toast.SetPackedFontColor((int(ta * 255) << 24) | (C_GOLD & 0xffffff))
		self.toast.Show()


class _Hit(ui.Window):
	# KULLANICI (2026-09-25): "butonlara tiklanmiyor" - duz ui.Window'a OnMouseLeftButtonUp guvenilir gelmiyor;
	# durum HUD kureleri (uimobilestatus._OrbTap) gibi parmak degdigi an (Down) calisir.
	def __init__(self, func):
		ui.Window.__init__(self)
		self.func = func

	def OnMouseLeftButtonDown(self):
		if self.func:
			self.func()
		return True

	def OnMouseLeftButtonUp(self):
		return True


class _Catcher(ui.Window):
	"""pencere disina dokunma: kapat (Vazgec gibi)."""
	def __init__(self, owner):
		ui.Window.__init__(self)
		self.owner = owner

	def OnMouseLeftButtonDown(self):
		self.owner.Close()
		return True

	def OnMouseLeftButtonUp(self):
		return True
