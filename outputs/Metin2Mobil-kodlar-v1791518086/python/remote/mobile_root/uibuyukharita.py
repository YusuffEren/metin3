# -*- coding: latin-1 -*-
# MOBIL: BUYUK HARITA + YOL GOSTERICI (KULLANICI 2026-09-26, tasarim Desktop/Metin2-Buyuk-Harita/buyuk-harita.html):
#   "mini map boyle buyuk gozukecek, ayrintilara basinca ayrintilar gozukecek" + "buraya git dedigimizde heronun
#   ustunde veya yerde seffaf oklar belirsin oraya gidecek yonu gostersin" -> prototip onaylandi ("mukemmel, yapalim").
#
# Harita: oyunun kendi bolge mini haritalari (<harita>/<xxxyyy>/minimap.dds, 256 px = 256 m) izgara halinde,
#   gorunum alanina SetRenderingRect ile kirpilir (kaydir: parmakla surukle, yakinlastir: + / - / cift dokun).
# Isaretler: sunucunun gonderdigi NPC / gecit listesi (miniMap.GetAtlasMarkList, APK v63+; eski APK'da
#   locale/tr/map/<harita>_point.txt konumlari isimsiz). Patron sureleri sunucuda yok -> patron listesi bos.
# Ayrintilar: her isaretin yaninda isim + koordinat etiketi; cakisan etiket konumu degisir / gizlenir.
# Isarete dokun: kart (tur, isim, koordinat, "Buraya Git"). Buraya Git -> harita kapanir, YolGosterici acilir.
# YolGosterici: kahramanin ayaginda zemine yatik akan oklar (32 yon, perspektif pisirilmis), bas ustunde pusula
#   ignesi + "hedef . N m"; yon = hedefin harita acisi - kamera acisi (app.GetCameraRotation = mini haritadaki
#   kamera konisi, kuzeyden saat yonu). 5 m'ye gelince "HEDEFE ULASTIN". Hedef mini haritada da isaretlenir (waypoint).
# Gorseller tools/bigmap_export.py -> mobile/ui/bigmap (2x); geometri mobilebigmapgeom.py (tasarim px).
# cp1254: \xdd=I-noktali \xfd=i-siz \xfe=s-cengelli \xf0=g-yumusak \xfc=u-umlaut \xf6=o-umlaut \xe7=c-cengelli
import math
import ui
import wndMgr
import app
import player
import chr
import miniMap
import background
import dbg
import mobilebigmapgeom as G
import mobilebigmapgeomk as K		# KLASIK pencere geometrisi (KULLANICI 2026-10-01; tools/bigmap_klasik)

DIR = "mobile/ui/bigmap/"
PAT = "d:/ymir work/ui/pattern/"
PUB = "d:/ymir work/ui/public/"
TEX_S = 2.0
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")
WAYPOINT_ID = 917
TILE_M = 256.0			# bolge boyu (metre = 256 hucre x 2 m ... mini harita dokusu 256 px)
ZMAX = 2.2
ZSTEP = 1.3
FONT = "Tahoma:%d"
C_PARCH = 0xfff3e3bf
C_DIM = 0xffcdb68c
C_GOLD = 0xffe8b848
C_WHITE = 0xfffff2c8
# klasik pencere renkleri (prototip harita_klasik.html)
C_CREAM = 0xfff1e6c0
C_SUB = 0xffc9b88f
C_OFF = 0xff8f8470
C_KGOLD = 0xffe8d08a
# yuz simgesi: pack icon/face/<ad>.tga (playerSettingModule.RACE_<AD> ile eslenir, gercek uicharacter.py gibi)
FACES = ("warrior_m", "assassin_w", "sura_m", "shaman_w", "warrior_w", "assassin_m", "sura_w", "shaman_m")
T_NPC, T_BOSS, T_WARP, T_PARTY = 0, 1, 2, 3
TYPES = (
	("npc", "NPC", 0xff6fe06a),
	("boss", "Patron", 0xffff3b28),
	("warp", "Ge\xe7it", 0xff57d4ff),
	("party", "Grup", 0xff7fb2ff),
)
JOBS = ("Sava\xfe\xe7\xfd", "Ninja", "Sura", "\xdeaman", "Lycan")
TR_UP = {"i": "\xdd", "\xfd": "I", "\xfc": "\xdc", "\xf6": "\xd6", "\xe7": "\xc7", "\xfe": "\xde", "\xf0": "\xd0"}


def _upper(s):
	return "".join([TR_UP.get(c, c.upper()) for c in s])


def _spaced(s):
	return " ".join(list(s))


def _rgba(c, a=1.0):
	return (((c >> 16) & 255) / 255.0, ((c >> 8) & 255) / 255.0, (c & 255) / 255.0, a)


class _Tap(ui.Window):
	def __init__(self, parent, func):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.func = func

	def OnMouseLeftButtonDown(self):
		self.func()
		return True

	def OnMouseLeftButtonUp(self):
		return True


class _Area(ui.Window):
	"""surukleme / dokunma alani: basis owner.OnAreaDown(name) ile bildirilir; takip owner.OnUpdate'te."""
	def __init__(self, parent, owner, name):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.owner = owner
		self.name = name

	def OnMouseLeftButtonDown(self):
		self.owner.OnAreaDown(self.name)
		return True

	def OnMouseLeftButtonUp(self):
		return True


def _mapName():
	try:
		return background.GetCurrentMapName()
	except:
		return ""


def _playerLocal():
	"""(x, y) metre, haritanin sol ustune gore. TELEFONDA OLCULDU (2026-09-26): player.GetMainCharacterPosition
	ZATEN yerel (santimetre) - GlobalPositionToLocalPosition ile ikinci kez cevirince -8807,-1330 cikiyordu ve
	yol gosterici hedefi hep ayni yonde / 9 km uzakta sandi."""
	(x, y, z) = player.GetMainCharacterPosition()
	return (x / 100.0, abs(y) / 100.0, x, y)


def _readSetting(mapName):
	"""(sizeX, sizeY) bolge sayisi; yoksa None."""
	try:
		import pack
		data = pack.Get(mapName + "/setting.txt")
	except:
		return None
	for line in data.splitlines():
		t = line.split()
		if len(t) >= 3 and t[0].lower() == "mapsize":
			try:
				return (int(t[1]), int(t[2]))
			except:
				return None
	return None


def _readMarks(mapName):
	"""[(tip, isim, x_m, y_m)] - sunucudan gelen liste; eski APK: yerel nokta dosyasi (isimsiz)."""
	out = []
	if hasattr(miniMap, "GetAtlasMarkList"):
		try:
			for (t, n, x, y) in miniMap.GetAtlasMarkList():
				if t == getattr(miniMap, "TYPE_WARP", 5):
					out.append((T_WARP, n, x, y))
				else:
					out.append((T_NPC, n, x, y))
			if out:
				return out
		except:
			dbg.TraceError("BuyukHarita: GetAtlasMarkList okunamadi")
	try:
		import pack
		data = pack.Get("locale/tr/map/%s_point.txt" % mapName)
		for line in data.splitlines():
			t = line.split()
			if len(t) >= 4 and t[0].isdigit():
				tip = T_WARP if t[1] == "WARP" else T_NPC
				out.append((tip, "Ge\xe7it" if tip == T_WARP else "NPC", float(t[2]) / 100.0, float(t[3]) / 100.0))
	except:
		pass
	return out


# ======================================================================================================== buyuk harita
class BigMapWindow(ui.Window):
	ROWS = 9

	def __init__(self, guide):
		ui.Window.__init__(self, "TOP_MOST")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("BuyukHarita")
		self.guide = guide
		self.W = float(wndMgr.GetScreenWidth())
		self.H = float(wndMgr.GetScreenHeight())
		self.k = self.H / 705.0
		k = self.k
		self.x0 = int(round((self.W - K.WIN[2] * k) / 2.0))
		self.y0 = int(round((self.H - K.WIN[3] * k) / 2.0))
		self.ROWS = K.ROWS
		self.SetPosition(0, 0)
		self.SetSize(int(self.W), int(self.H))
		self.keep = []
		self.tex = {}
		self.mapName = ""
		self.tiles = []
		self.size = (0, 0)
		self.marks = []
		self.show = [True, True, True, True]
		self.details = False
		self.sel = -1
		self.listTop = 0
		self.scale = 0.62
		self.tx = 0.0
		self.ty = 0.0
		self.me = (0.0, 0.0)
		self.dirty = True
		self.lastLayout = 0.0
		self.drag = None
		self.lastTap = (-10.0, 0, 0)
		self.tOpen = -1.0
		# --- karartma (dunyaya dokunmayi da yutar: kok pencere secilebilir)
		dim = ui.Bar()
		dim.SetParent(self)
		dim.AddFlag("not_pick")
		dim.SetPosition(0, 0)
		dim.SetSize(int(self.W), int(self.H))
		dim.SetColor(0x99000000)
		dim.Show()
		self.keep.append(dim)
		self.dim = dim
		# --- KLASIK pencere zemini (KULLANICI 2026-10-01): Board + TitleBar + bolum cizgileri + kutular
		self.__BuildFrame()		# DOSEME (oyunun klasik pencereleri gibi; tek parca ~11 MB doku yerine kucuk parcalar)
		# harita katmani: dokular + isaretler + etiketler (pencere zemininin ustunde)
		vx, vy, vw, vh = K.VIEWPORT
		self.VR = (self.x0 + vx * k, self.y0 + vy * k, vw * k, vh * k)
		self.mapLayer = ui.Window()
		self.mapLayer.SetParent(self)
		self.mapLayer.AddFlag("not_pick")
		self.mapLayer.SetPosition(0, 0)
		self.mapLayer.SetSize(int(self.W), int(self.H))
		self.mapLayer.Show()
		self.keep.append(self.mapLayer)
		self.markLayer = ui.Window()
		self.markLayer.SetParent(self)
		self.markLayer.AddFlag("not_pick")
		self.markLayer.SetPosition(0, 0)
		self.markLayer.SetSize(int(self.W), int(self.H))
		self.markLayer.Show()
		self.keep.append(self.markLayer)
		self.labelLayer = ui.Window()
		self.labelLayer.SetParent(self)
		self.labelLayer.AddFlag("not_pick")
		self.labelLayer.SetPosition(0, 0)
		self.labelLayer.SetSize(int(self.W), int(self.H))
		self.labelLayer.Show()
		self.keep.append(self.labelLayer)
		self.__BuildEdge()
		# harita surukleme alani (isaretler ve bos harita dokunuslari)
		self.mapArea = _Area(self, self, "map")
		self.mapArea.SetPosition(int(self.VR[0]), int(self.VR[1]))
		self.mapArea.SetSize(int(self.VR[2]), int(self.VR[3]))
		self.mapArea.Show()
		self.keep.append(self.mapArea)
		# harita dugmeleri (klasik middle_button)
		self.compass = self.__Img("k_compass.png", K.compass)
		self.bCenter = self.__Btn("k_btn_center.png", K.btn_center, self.__OnCenter)
		self.bZin = self.__Btn("k_btn_zin.png", K.btn_zin, lambda: self.__ZoomAt(ZSTEP, None))
		self.bZout = self.__Btn("k_btn_zout.png", K.btn_zout, lambda: self.__ZoomAt(1.0 / ZSTEP, None))
		self.bDetailOff = self.__Btn("k_btn_detail_off.png", K.btn_detail, self.__OnDetail)
		self.bDetailOn = self.__Img("k_btn_detail_on.png", K.btn_detail)
		self.bDetailOn.Hide()
		self.detailT = self.__Text(K.DETAIL_TXT[0], K.DETAIL_TXT[1], 14, C_CREAM, vcenter=True)
		self.detailT.SetText("Ayr\xfdnt\xfdlar")
		self.bClose = self.__Btn("k_close.png", K.close, self.Close)
		# baslik: kalin gorunum = ayni yazi 1 px kaydirmali iki kez (motorda kalin font yok)
		self.title2 = self.__Text(K.TITLE[0], K.TITLE[1], 17, 0xffffffff, vcenter=True)
		self.title = self.__Text(K.TITLE[0], K.TITLE[1], 17, 0xffffffff, vcenter=True)
		self.title2.SetPosition(int(round(self.x0 + K.TITLE[0] * k)) + max(1, int(round(k))), int(round(self.y0 + K.TITLE[1] * k)))
		self.subTitle = self.__Text(K.TITLE[0], K.TITLE[1], 12, C_SUB, vcenter=True)
		# bolum basliklari
		for (g, txt) in ((K.H_KONUM, "KONUMUN"), (K.H_GOSTER, "G\xd6STER"), (K.H_NOKTA, "NOKTALAR")):
			h = self.__Text(g[0], g[1], 12, C_KGOLD)
			h.SetText(txt)
		# konum karti: yuz simgesi (slot zeminde) + ad + sinif/seviye + koordinat
		self.face = ui.ExpandedImageBox()
		self.face.SetParent(self)
		self.face.AddFlag("not_pick")
		self.keep.append(self.face)
		self.faceFile = ""
		self.meName = self.__Text(K.ME_NAME[0], K.ME_NAME[1], 16, 0xffffffff)
		self.meSub = self.__Text(K.ME_SUB[0], K.ME_SUB[1], 13, C_SUB)
		self.meXY = self.__Text(K.ME_XY[0], K.ME_XY[1], 16, C_KGOLD, right=True)
		self.meXYs = self.__Text(K.ME_XYS[0], K.ME_XYS[1], 10, C_OFF, right=True)
		self.meXYs.SetText("KOORD\xddNAT")
		# filtre dugmeleri (Goster): basili = acik
		# KULLANICI (2026-10-01): Patron filtresi KALDIRILDI ("patron yerleri gosterilirse oyunun rekabeti biter");
		# NPC / Gecit / Grup tek sira (K.CHIPS: (TYPES indeksi, geometri))
		self.chips = [None, None, None, None]
		for (i, g) in K.CHIPS:
			key = TYPES[i][0]
			on = self.__Img("k_chip_on_%s.png" % key, g)
			off = self.__Img("k_chip_off_%s.png" % key, g)
			off.Hide()
			lbl = self.__Text(g[0] + 28, g[1] + g[3] / 2.0, 14, C_CREAM, vcenter=True)
			lbl.SetText(TYPES[i][1])
			n = self.__Text(g[0] + g[2] - 12, g[1] + g[3] / 2.0, 13, C_SUB, right=True, vcenter=True)
			self.__TapBox(g, lambda i=i: self.__OnChip(i))
			self.chips[i] = (on, off, n, lbl)
		# liste
		self.rows = []
		rx, ry, rw, rh = K.ROW
		step = float(K.ROW_STEP)
		for j in xrange(self.ROWS):
			g = (rx, ry + j * step, rw, rh)
			bgN = self.__Img("k_row.png", g)
			bgS = self.__Img("k_row_sel.png", g)
			bgS.Hide()
			dots = []
			for t in xrange(4):
				dd = self.__Img("k_dot_%s.png" % TYPES[t][0], (rx + 9.5, g[1] + rh / 2.0 - 6.0))
				dd.Hide()
				dots.append(dd)
			name = self.__Text(rx + 28, g[1] + rh / 2.0, 15, 0xfff6ecd0, vcenter=True)
			right = self.__Text(rx + rw - 10, g[1] + rh / 2.0, 13, C_SUB, right=True, vcenter=True)
			self.rows.append({"bgN": bgN, "bgS": bgS, "dots": dots, "name": name, "right": right, "idx": -1})
		self.listArea = _Area(self, self, "list")
		self.listArea.SetPosition(int(self.x0 + rx * k), int(self.y0 + ry * k))
		self.listArea.SetSize(int(rw * k), int(self.ROWS * step * k))
		self.listArea.Show()
		self.keep.append(self.listArea)
		self.thumb = self.__Img("k_thumb.png", (K.SCROLL[0], K.SCROLL[1] + 17))
		# secim karti (opak klasik kart + Buraya Git)
		self.popLayer = ui.Window()
		self.popLayer.SetParent(self)
		self.popLayer.AddFlag("not_pick")
		self.popLayer.SetPosition(0, 0)
		self.popLayer.SetSize(int(self.W), int(self.H))
		self.keep.append(self.popLayer)
		self.pop = self.__Img("k_pop.png", K.pop, self.popLayer)
		self.popDots = []
		for t in xrange(4):
			dd = self.__Img("k_dot_%s.png" % TYPES[t][0], K.POP_DOT, self.popLayer)
			dd.Hide()
			self.popDots.append(dd)
		self.popTy = self.__Text(0, 0, 12, C_GOLD, parent=self.popLayer, vcenter=True)
		self.popName = self.__Text(0, 0, 17, 0xffffffff, parent=self.popLayer)
		self.popXY = self.__Text(0, 0, 13, C_SUB, parent=self.popLayer)
		self.popGo = self.__Img("k_btn_go.png", K.btn_go, self.popLayer)
		self.popGoT = self.__Text(0, 0, 14, C_CREAM, center=True, parent=self.popLayer, vcenter=True)
		self.popGoT.SetText("Buraya Git")
		self.popGoTap = _Tap(self, self.__OnGo)
		self.keep.append(self.popGoTap)
		self.popLayer.Hide()
		self.popGoTap.Hide()
		# isaret / etiket havuzlari
		self.mkPool = {}
		self.lbPool = []
		self.meMk = None
		self.mePing = None
		self.Hide()

	# ------------------------------------------------------------------ yardimcilar
	def __Img(self, name, g, parent=None):
		w = ui.ExpandedImageBox()
		w.SetParent(parent or self)
		w.AddFlag("not_pick")
		w.LoadImage(DIR + name)
		max(0, 0)
		self.tex[w] = (float(w.GetWidth()), float(w.GetHeight()))
		s = self.k / TEX_S
		w.SetScale(s, s)
		w.SetPosition(int(round(self.x0 + g[0] * self.k)), int(round(self.y0 + g[1] * self.k)))
		w.Show()
		self.keep.append(w)
		return w

	def __Raw(self, name, parent):
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(name)
		max(0, 0)
		self.tex[w] = (float(w.GetWidth()), float(w.GetHeight()))
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		w.Show()
		self.keep.append(w)
		return w

	# ------------------------------------------------------------------ klasik zemin: DOSEME
	def __PImg(self, path, x, y, sx=1.0, sy=1.0):
		"""pack dokusu (texel olcegi sx/sy tasarim px) tasarim konumuna"""
		w = ui.ExpandedImageBox()
		w.SetParent(self)
		w.AddFlag("not_pick")
		w.LoadImage(path)
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		w.SetScale(sx * self.k, sy * self.k)
		w.SetPosition(int(round(self.x0 + x * self.k)), int(round(self.y0 + y * self.k)))
		w.Show()
		self.keep.append(w)
		return w

	def __Tile(self, path, x, y, w, h, tw, th, sx=1.0, sy=1.0, cutB=0.0):
		"""tw x th texel dokuyu (x, y, w, h) tasarim alanina DOSER (UV tekrari - dikissiz, ui.Board gibi).
		cutB: alttan kesilecek texel orani (TitleBar'in bos alt satirlari)."""
		img = self.__PImg(path, x, y, sx, sy)
		if HAS_RRS:
			r = w / (tw * sx) - 1.0
			b = h / (th * sy) - 1.0 - cutB
		else:		# eski APK: uzatma olceksiz texel -> uzunluk dogru, desen yogunlugu hafif farkli
			r = (w - tw * sx) * self.k / tw
			b = (h - th * sy) * self.k / th - cutB
		img.SetRenderingRect(0.0, 0.0, r, b)
		return img

	def __Box(self, x, y, w, h, color, fill=False):
		b = ui.Bar() if fill else ui.Box()
		b.SetParent(self)
		b.AddFlag("not_pick")
		b.SetColor(color)
		b.SetPosition(int(round(self.x0 + x * self.k)), int(round(self.y0 + y * self.k)))
		b.SetSize(max(1, int(round(w * self.k))), max(1, int(round(h * self.k))))
		b.Show()
		self.keep.append(b)
		return b

	def __ThinBoard(self, x, y, w, h):
		c = 16.0
		self.__Box(x + c, y + c, w - 2 * c, h - 2 * c, 0x82000000, fill=True)
		self.__Tile(PAT + "thinboard_line_top.tga", x + c, y, w - 2 * c, c, 16, 16)
		self.__Tile(PAT + "thinboard_line_bottom.tga", x + c, y + h - c, w - 2 * c, c, 16, 16)
		self.__Tile(PAT + "thinboard_line_left.tga", x, y + c, c, h - 2 * c, 16, 16)
		self.__Tile(PAT + "thinboard_line_right.tga", x + w - c, y + c, c, h - 2 * c, 16, 16)
		for (n, cx, cy) in (("lefttop", x, y), ("righttop", x + w - c, y), ("leftbottom", x, y + h - c), ("rightbottom", x + w - c, y + h - c)):
			self.__PImg(PAT + "thinboard_corner_%s.tga" % n, cx, cy)

	def __BuildFrame(self):
		"""Board (32 texel kose, 128 texel kenar/taban) + TitleBar (x1.5, alt 9 texel kesik) + bolum cizgileri +
		Konumun ThinBoard + yuz slotu + liste kutusu + ince kaydirma rayi. KULLANICI: '2. yol' (dosen zemin)."""
		W, H = K.WIN[2], K.WIN[3]
		self.__Tile(PAT + "board_base.tga", 32, 32, W - 64, H - 64, 128, 128)
		self.__Tile(PAT + "board_line_top.tga", 32, 0, W - 64, 32, 128, 32)
		self.__Tile(PAT + "board_line_bottom.tga", 32, H - 32, W - 64, 32, 128, 32)
		self.__Tile(PAT + "board_line_left.tga", 0, 32, 32, H - 64, 32, 128)
		self.__Tile(PAT + "board_line_right.tga", W - 32, 32, 32, H - 64, 32, 128)
		for (n, cx, cy) in (("lefttop", 0, 0), ("righttop", W - 32, 0), ("leftbottom", 0, H - 32), ("rightbottom", W - 32, H - 32)):
			self.__PImg(PAT + "board_corner_%s.tga" % n, cx, cy)
		# TitleBar: 32x32 texel, ust 23 satir dolu; x1.5 -> 34.5 tasarim px
		tb = K.TITLEBAR
		# yukseklik 34.5 (= 23 dolu satir x 1.5) bos alt 9 satiri ZATEN disarida birakir - ayrica kesme YOK
		# (KULLANICI 2026-10-01: "ust kirmizi yer bozulmus, kesilmis" - cutB ikinci kez kesiyordu)
		self.__Tile(PAT + "titlebar_center.tga", tb[0] + 48, tb[1], tb[2] - 96, 34.5, 32, 32, 1.5, 1.5)
		self.__Tile(PAT + "titlebar_left.tga", tb[0], tb[1], 48, 34.5, 32, 32, 1.5, 1.5)
		self.__Tile(PAT + "titlebar_right.tga", tb[0] + tb[2] - 48, tb[1], 48, 34.5, 32, 32, 1.5, 1.5)
		# bolum basligi cizgileri (yazinin sagindan sonen)
		for (x, y, w) in K.RULES:
			r = ui.ExpandedImageBox()
			r.SetParent(self)
			r.AddFlag("not_pick")
			r.LoadImage(DIR + "k_rule.png")		# 256 x 2 px
			r.SetScale(w * self.k / 256.0, self.k / 2.0)
			r.SetPosition(int(round(self.x0 + x * self.k)), int(round(self.y0 + y * self.k)))
			r.Show()
			self.keep.append(r)
		# Konumun kutusu + yuz slotu
		bx, by, bw, bh = K.ME_BOX
		self.__ThinBoard(bx, by, bw, bh)
		fx, fy, fw, fh = K.FACE
		self.__PImg(PUB + "slot_base.sub", fx, fy, fw / 32.0, fh / 32.0)
		# liste kutusu: koyu ic + dis siyah + ic cizgi
		lx, ly, lw, lh = K.LIST_BOX
		self.__Box(lx, ly, lw, lh, 0x73000000, fill=True)
		self.__Box(lx - 1, ly - 1, lw + 2, lh + 2, 0xff000000)
		self.__Box(lx, ly, lw, lh, 0xff3d342a)
		# ince kaydirma: ust/alt ok + ray (tutamak k_thumb ayri)
		sx0, sy0, sw, sh = K.SCROLL
		self.__Tile(PAT + "scrollbar_middle.tga", sx0, sy0 + 17, 17, sh - 34, 16, 4, 17 / 16.0, 1.0)
		self.__PImg(PUB + "scrollbar_thin_up_button_01.sub", sx0, sy0)
		self.__PImg(PUB + "scrollbar_thin_down_button_01.sub", sx0, sy0 + sh - 17)

	def __BuildEdge(self):
		"""harita cercevesi: dis siyah + ic cizgi + ic golge (4 kucuk serit) - tek parca 6 MB doku yerine"""
		vx, vy, vw, vh = K.VIEWPORT
		self.__Box(vx - 2, vy - 2, vw + 4, vh + 4, 0xff000000)
		self.__Box(vx - 1, vy - 1, vw + 2, vh + 2, 0xff000000)
		self.__Box(vx - 1, vy - 1, vw + 2, vh + 2, 0xff3d342a)
		g = 18.0
		for (name, x, y, w, h, tw, th) in (("t", vx, vy, vw, g, 8, 36), ("b", vx, vy + vh - g, vw, g, 8, 36),
				("l", vx, vy, g, vh, 36, 8), ("r", vx + vw - g, vy, g, vh, 36, 8)):
			im = ui.ExpandedImageBox()
			im.SetParent(self)
			im.AddFlag("not_pick")
			im.LoadImage(DIR + "k_shade_%s.png" % name)
			im.SetScale(w * self.k / float(tw), h * self.k / float(th))
			im.SetPosition(int(round(self.x0 + x * self.k)), int(round(self.y0 + y * self.k)))
			im.Show()
			self.keep.append(im)

	def __Text(self, x, y, pt, color, center=False, right=False, parent=None, bold=False, vcenter=False):
		t = ui.TextLine()
		t.SetParent(parent or self)
		t.AddFlag("not_pick")
		t.SetFontName(FONT % max(8, min(18, int(round(pt * self.k)))))		# 18 ustu motorda buyutulur (bulanik)
		if center:
			t.SetHorizontalAlignCenter()
		elif right:
			t.SetHorizontalAlignRight()
		if vcenter:
			t.SetVerticalAlignCenter()
		t.SetOutline()
		t.SetPackedFontColor(color)
		t.SetPosition(int(round(self.x0 + x * self.k)), int(round(self.y0 + y * self.k)))
		t.Show()
		self.keep.append(t)
		return t

	def __TapBox(self, g, func, pad=0.0):
		tp = _Tap(self, func)
		tp.SetPosition(int(self.x0 + (g[0] - pad) * self.k), int(self.y0 + (g[1] - pad) * self.k))
		tp.SetSize(int((g[2] + 2 * pad) * self.k), int((g[3] + 2 * pad) * self.k))
		tp.Show()
		self.keep.append(tp)
		return tp

	def __Btn(self, name, g, func):
		w = self.__Img(name, g)
		self.__TapBox(g, func, 4.0)
		return w

	# ------------------------------------------------------------------ ac / kapat
	def Open(self):
		name = _mapName()
		if name != self.mapName:
			if not self.__BuildMap(name):
				return False
		self.__RefreshMe()
		self.marks = []
		# TELEFONDA OLCULDU (2026-09-26): sunucunun NPC konumlari DUNYA (global) koordinatinda geliyor (hedef 9432 m
		# gorundu; koy ~1000 m). Harita disina dusen isaretler haritanin koken noktasi cikarilarak yerele cevrilir.
		for (t, n, x, y) in _readMarks(name):
			if x > self.size[0] + 50.0 or y > self.size[1] + 50.0:
				continue		# harita disi (beklenmez)
			# sunucu bazi isimleri Korece gonderiyor -> istemcide "???" gorunuyordu (Skipia gecitleri)
			if "?" in n or not n.strip():
				n = "Geçit" if t == T_WARP else "NPC"
			self.marks.append({"t": t, "n": n, "x": x, "y": y})
		self.sel = -1
		self.listTop = 0
		self.__HidePop()
		self.__FitScale()
		self.__Focus(self.me[0], self.me[1], max(self.zmin, 0.62))
		self.__RefreshTexts()
		self.__RefreshChips()
		self.__RefreshList()
		self.dirty = True
		self.tOpen = app.GetTime()
		if self.guide:
			self.guide.SetHiddenForMap(True)
		self.Show()
		self.SetTop()
		return True

	def Close(self):
		self.__HidePop()
		self.Hide()
		if self.guide:
			self.guide.SetHiddenForMap(False)

	def Destroy(self):
		self.Hide()
		self.guide = None
		self.keep = []
		self.tiles = []
		self.mkPool = {}
		self.lbPool = []
		self.rows = []
		self.chips = []
		self.tex = {}

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __BuildMap(self, name):
		sz = _readSetting(name)
		if not sz:
			return False
		for t in self.tiles:
			t["w"].Hide()
		self.tiles = []
		for x in xrange(sz[0]):
			for y in xrange(sz[1]):
				path = "%s/%03d%03d/minimap.dds" % (name, x, y)
				try:
					import pack
					if not pack.Exist(path):
						continue
				except:
					pass
				w = self.__Raw(path, self.mapLayer)
				self.tiles.append({"w": w, "x": x, "y": y})
		if not self.tiles:
			return False
		self.mapName = name
		self.size = (sz[0] * TILE_M, sz[1] * TILE_M)
		return True

	# ------------------------------------------------------------------ gorunum
	def __FitScale(self):
		vw, vh = self.VR[2] / self.k, self.VR[3] / self.k
		fit = min(vw / max(1.0, self.size[0]), vh / max(1.0, self.size[1]))
		self.zmin = min(fit, 0.42)

	def __Clamp(self):
		k = self.k
		W = self.VR[2]
		H = self.VR[3]
		w = self.size[0] * self.scale * k
		h = self.size[1] * self.scale * k
		self.tx = (W - w) / 2.0 if w <= W else min(0.0, max(W - w, self.tx))
		self.ty = (H - h) / 2.0 if h <= H else min(0.0, max(H - h, self.ty))

	def __Focus(self, x, y, s=None):
		if s:
			self.scale = max(self.zmin, min(ZMAX, s))
		k = self.k
		self.tx = self.VR[2] / 2.0 - x * self.scale * k
		self.ty = self.VR[3] / 2.0 - y * self.scale * k
		self.__Clamp()
		self.dirty = True

	def __ZoomAt(self, f, pt):
		if pt is None:
			pt = (self.VR[2] / 2.0, self.VR[3] / 2.0)
		ns = max(self.zmin, min(ZMAX, self.scale * f))
		q = ns / self.scale
		self.tx = pt[0] - (pt[0] - self.tx) * q
		self.ty = pt[1] - (pt[1] - self.ty) * q
		self.scale = ns
		self.__Clamp()
		self.dirty = True

	def __ToScreen(self, x, y):
		s = self.scale * self.k
		return (self.VR[0] + self.tx + x * s, self.VR[1] + self.ty + y * s)

	def __PlaceTiles(self):
		k = self.k
		s = self.scale * k
		vx0, vy0, vw, vh = self.VR
		for t in self.tiles:
			w = t["w"]
			(tw, th) = self.tex[w]
			x0 = vx0 + self.tx + t["x"] * TILE_M * s
			y0 = vy0 + self.ty + t["y"] * TILE_M * s
			size = TILE_M * s
			x1 = x0 + size
			y1 = y0 + size
			if x1 <= vx0 or y1 <= vy0 or x0 >= vx0 + vw or y0 >= vy0 + vh:
				if w.IsShow():
					w.Hide()
				continue
			sc = size / tw
			w.SetScale(sc, sc)
			w.SetPosition(int(math.floor(x0)), int(math.floor(y0)))
			l = max(0.0, (vx0 - x0) / size)
			tp = max(0.0, (vy0 - y0) / size)
			r = max(0.0, (x1 - (vx0 + vw)) / size)
			b = max(0.0, (y1 - (vy0 + vh)) / size)
			w.SetRenderingRect(-l, -tp, -r, -b)
			if not w.IsShow():
				w.Show()

	# ------------------------------------------------------------------ isaretler
	def __Mk(self, key):
		lst = self.mkPool.setdefault(key, [])
		for m in lst:
			if not m["used"]:
				m["used"] = True
				return m
		w = self.__Raw(DIR + "k_mk_%s.png" % key, self.markLayer)
		m = {"w": w, "used": True}
		lst.append(m)
		return m

	def __PlaceMarks(self):
		for lst in self.mkPool.values():
			for m in lst:
				m["used"] = False
		vx0, vy0, vw, vh = self.VR
		s = self.k / TEX_S
		self.vis = []
		for i in xrange(len(self.marks)):
			mk = self.marks[i]
			if not self.show[mk["t"]]:
				continue
			(sx, sy) = self.__ToScreen(mk["x"], mk["y"])
			if sx < vx0 or sy < vy0 or sx > vx0 + vw or sy > vy0 + vh:
				continue
			key = TYPES[mk["t"]][0]
			m = self.__Mk(key)
			half = (K.MK[key] + 3) / 2.0		# k_mk dokusu: cap + 3 tasarim px (parilti payi)
			m["w"].SetScale(s, s)
			m["w"].SetPosition(int(round(sx - half * self.k)), int(round(sy - half * self.k)))
			if not m["w"].IsShow():
				m["w"].Show()
			self.vis.append((i, sx, sy))
		for lst in self.mkPool.values():
			for m in lst:
				if not m["used"] and m["w"].IsShow():
					m["w"].Hide()
		# kahraman: ok + ping
		if not self.meMk:
			self.mePing = self.__Raw(DIR + "ping_me.png", self.markLayer)
			self.meMk = self.__Raw(DIR + "k_mk_me.png", self.markLayer)
		(sx, sy) = self.__ToScreen(self.me[0], self.me[1])
		inside = vx0 <= sx <= vx0 + vw and vy0 <= sy <= vy0 + vh
		if inside:
			self.meXYs2 = (sx, sy)
			self.__RotAt(self.meMk, sx, sy, self.meRot, 1.0)
			self.meMk.Show()
		else:
			self.meMk.Hide()
			self.mePing.Hide()
		self.meIn = inside

	def __RotAt(self, w, cx, cy, deg, sc, a=1.0):
		(tw, th) = self.tex[w]
		s = self.k / TEX_S * sc
		ix = int(math.floor(cx))
		iy = int(math.floor(cy))
		w.SetScale(s, s)
		w.SetPosition(ix, iy)
		w.SetOrigin(cx - ix, cy - iy)
		w.SetRotation(deg if abs(deg) > 1e-4 else 1e-4)
		w.SetAlpha(max(0.0, min(1.0, a)))

	# ------------------------------------------------------------------ etiketler (ayrintilar)
	def __Label(self, j):
		while len(self.lbPool) <= j:
			lb = {}
			lb["bg"] = self.__Bar(0xf50e0804)
			lb["b0"] = self.__Bar(0xffa88d5a)
			lb["b1"] = self.__Bar(0xffa88d5a)
			lb["b2"] = self.__Bar(0xffa88d5a)
			lb["b3"] = self.__Bar(0xffa88d5a)
			lb["ac"] = self.__Bar(0xffe6bd5c)
			t = ui.TextLine()
			t.SetParent(self.labelLayer)
			t.AddFlag("not_pick")
			t.SetFontName(FONT % max(10, int(round(15 * self.k))))
			t.SetOutline()
			t.SetPackedFontColor(0xfffff6e0)
			self.keep.append(t)
			lb["t"] = t
			e = ui.TextLine()
			e.SetParent(self.labelLayer)
			e.AddFlag("not_pick")
			e.SetFontName(FONT % max(10, int(round(14 * self.k))))
			e.SetOutline()
			e.SetPackedFontColor(0xffe8cf95)
			self.keep.append(e)
			lb["e"] = e
			self.lbPool.append(lb)
		return self.lbPool[j]

	def __Bar(self, color):
		b = ui.Bar()
		b.SetParent(self.labelLayer)
		b.AddFlag("not_pick")
		b.SetColor(color)
		self.keep.append(b)
		return b

	def __HideLabels(self, fromJ=0):
		for j in xrange(fromJ, len(self.lbPool)):
			for key in ("bg", "b0", "b1", "b2", "b3", "ac", "t", "e"):
				if self.lbPool[j][key].IsShow():
					self.lbPool[j][key].Hide()

	def __LayoutLabels(self):
		if not self.details:
			self.lbRects = []
			self.__HideLabels()
			return
		vx0, vy0, vw, vh = self.VR
		k = self.k
		placed = []
		# harita ustu dugmeler engel
		for g in (K.compass, K.btn_center, K.btn_zin, K.btn_zout, K.btn_detail):
			placed.append((self.x0 + g[0] * k - 4, self.y0 + g[1] * k - 4, self.x0 + (g[0] + g[2]) * k + 4, self.y0 + (g[1] + g[3]) * k + 4))
		marks = [(sx - 7, sy - 7, sx + 7, sy + 7) for (i, sx, sy) in self.vis]
		if self.meIn:
			(mx, my) = self.__ToScreen(self.me[0], self.me[1])
			marks.append((mx - 13, my - 13, mx + 13, my + 13))
		pr = {T_BOSS: 0, T_PARTY: 1, T_WARP: 2, T_NPC: 3}
		order = sorted(self.vis, key=lambda v: (pr[self.marks[v[0]]["t"]], v[2]))
		self.lbRects = []		# (x0, y0, x1, y1, isaret) - KULLANICI: "isimlerin ustune basinca da Buraya Git cikisn"
		j = 0
		for (i, sx, sy) in order:
			mk = self.marks[i]
			lb = self.__Label(j)
			lb["t"].SetText(mk["n"])
			lb["e"].SetText(" (%d, %d)" % (int(mk["x"]), int(mk["y"])))
			(w1, h1) = lb["t"].GetTextSize()
			(w2, h2) = lb["e"].GetTextSize()
			pad = 8.0 * k
			w = w1 + w2 + pad * 2 + 9 * k
			h = max(h1, h2) + 9.0 * k
			# adaylar: sag, sol, sag-ust, sag-alt, sol-ust, sol-alt (c[2] = 1 ise etiket isaretin solunda)
			g12 = 12.0 * k
			g8 = 8.0 * k
			C = ((sx + g12, sy - h / 2.0, 0), (sx - g12 - w, sy - h / 2.0, 1), (sx + g12, sy - h - g8, 0),
				 (sx + g12, sy + g8, 0), (sx - g12 - w, sy - h - g8, 1), (sx - g12 - w, sy + g8, 1))
			best = None
			for c in C:
				r = (c[0], c[1], c[0] + w, c[1] + h)
				if r[0] < vx0 + 2 or r[2] > vx0 + vw - 2 or r[1] < vy0 + 2 or r[3] > vy0 + vh - 2:
					continue
				hit = False
				for q in placed:
					if r[0] < q[2] and r[2] > q[0] and r[1] < q[3] and r[3] > q[1]:
						hit = True
						break
				if not hit:
					for q in marks:
						if abs(q[0] + 7 - sx) < 1 and abs(q[1] + 7 - sy) < 1:
							continue
						if r[0] < q[2] and r[2] > q[0] and r[1] < q[3] and r[3] > q[1]:
							hit = True
							break
				if not hit:
					best = (c, r)
					break
			if not best:
				continue
			(c, r) = best
			placed.append(r)
			self.lbRects.append((r[0], r[1], r[2], r[3], i))
			x, y, x1, y1 = [int(round(v)) for v in r]
			ww = x1 - x
			hh = y1 - y
			lb["bg"].SetPosition(x, y); lb["bg"].SetSize(ww, hh)
			lb["b0"].SetPosition(x, y); lb["b0"].SetSize(ww, 1)
			lb["b1"].SetPosition(x, y1 - 1); lb["b1"].SetSize(ww, 1)
			lb["b2"].SetPosition(x, y); lb["b2"].SetSize(1, hh)
			lb["b3"].SetPosition(x1 - 1, y); lb["b3"].SetSize(1, hh)
			acw = max(2, int(round(3 * k)))
			lb["ac"].SetColor(TYPES[mk["t"]][2])
			lb["ac"].SetPosition(x if c[2] == 0 else x1 - acw, y)
			lb["ac"].SetSize(acw, hh)
			tx0 = x + (acw if c[2] == 0 else 0) + int(pad)
			ty0 = y + int((hh - h1) / 2.0) - 1
			lb["t"].SetPosition(tx0, ty0)
			lb["e"].SetPosition(tx0 + int(w1 + 6 * k), ty0)		# isim ile koordinat yapismasin
			for key in ("bg", "b0", "b1", "b2", "b3", "ac", "t", "e"):
				if not lb[key].IsShow():
					lb[key].Show()
			j += 1
		self.__HideLabels(j)

	# ------------------------------------------------------------------ sag panel
	def __RefreshMe(self):
		(x, y, gx, gy) = _playerLocal()
		self.me = (x, y)
		self.meG = (gx, gy)
		rot = 0.0
		try:
			chr.SelectInstance(player.GetMainCharacterIndex())
			rot = chr.GetRotation()
		except:
			pass
		self.meRot = (180.0 + rot) % 360.0		# native atlas: 540 - inst.rot; chr.GetRotation = 360 - inst.rot

	def __RefreshTexts(self):
		try:
			import localeInfo
			nm = localeInfo.MINIMAP_ZONE_NAME_DICT.get(self.mapName, "")
		except:
			nm = ""
		if not nm:
			# sozlukte yoksa (zindanlar: "season2/skipia_dungeon_01") klasor adindan okunur bir ad
			base = self.mapName.replace("\\", "/").split("/")[-1].replace("metin2_map_", "")
			words = []
			for wd in base.split("_"):
				if wd.lower() == "dungeon":
					wd = "Zindaný"
				elif wd.isdigit():
					wd = str(int(wd))
				words.append(wd)
			nm = " ".join(words)
		self.title.SetText(nm)
		self.title2.SetText(nm)
		ch = ""
		try:
			import constInfo
			ch = " \xb7 Kanal %d" % int(constInfo.indexver)
		except:
			pass
		self.subTitle.SetText("B\xf6lge Haritas\xfd" + ch)
		try:
			(tw, th) = self.title.GetTextSize()
		except:
			tw = 160
		self.subTitle.SetPosition(int(round(self.x0 + K.TITLE[0] * self.k + tw + 14 * self.k)), int(round(self.y0 + K.TITLE[1] * self.k)))
		self.__RefreshFace()
		self.meName.SetText(player.GetName())
		job = ""
		try:
			import playerSettingModule
			job = JOBS[playerSettingModule.RACE_JOB_TABLE[player.GetRace()]]
		except:
			try:
				job = JOBS[player.GetRace() % 4]
			except:
				job = ""
		lv = 0
		try:
			lv = int(player.GetStatus(player.LEVEL))
		except:
			lv = 0
		self.meSub.SetText(job and ("%s \xb7 Sv. %d" % (job, lv)) or ("Sv. %d" % lv))
		self.meXY.SetText("%d, %d" % (int(self.me[0]), int(self.me[1])))

	def __RefreshFace(self):
		"""Konumun: karakterin yuz simgesi (pack icon/face, oyundaki karakter penceresiyle ayni)"""
		f = ""
		try:
			## GERCEK CLIENT (root/uicharacter.py FACE_IMAGE_DICT): playerSettingModule.RACE_* -> icon/face/<sinif>_<m|w>.tga
			import playerSettingModule as PSM
			faces = {}
			for nm in FACES:
				c = getattr(PSM, "RACE_" + nm.upper(), None)
				if c is not None:
					faces[c] = nm
			r = int(player.GetRace())
			if r in faces:
				f = "icon/face/%s.tga" % faces[r]
		except:
			f = ""
		if not f:
			self.face.Hide()
			return
		if f != self.faceFile:
			try:
				self.face.LoadImage(f)
				self.faceFile = f
			except:
				self.face.Hide()
				return
		g = K.FACE_IMG
		s = g[2] * self.k / 43.0		# yuz dokusu 43 px
		self.face.SetScale(s, s)
		self.face.SetPosition(int(round(self.x0 + g[0] * self.k)), int(round(self.y0 + g[1] * self.k)))
		self.face.Show()

	def __RefreshChips(self):
		for i in xrange(4):
			if not self.chips[i]:
				continue
			(on, off, n, lbl) = self.chips[i]
			cnt = len([m for m in self.marks if m["t"] == i])
			n.SetText("%d" % cnt)
			if self.show[i]:
				on.Show(); off.Hide()
				lbl.SetPackedFontColor(C_CREAM)
			else:
				on.Hide(); off.Show()
				lbl.SetPackedFontColor(C_OFF)

	def __ListItems(self):
		pr = {T_BOSS: 0, T_PARTY: 1, T_WARP: 2, T_NPC: 3}
		idx = [i for i in xrange(len(self.marks)) if self.show[self.marks[i]["t"]]]
		idx.sort(key=lambda i: (pr[self.marks[i]["t"]], i))
		return idx

	def __RefreshList(self):
		items = self.__ListItems()
		self.listTop = max(0, min(self.listTop, max(0, len(items) - self.ROWS)))
		for j in xrange(self.ROWS):
			r = self.rows[j]
			q = self.listTop + j
			if q >= len(items):
				r["idx"] = -1
				for key in ("bgN", "bgS", "name", "right"):
					r[key].Hide()
				for d in r["dots"]:
					d.Hide()
				continue
			i = items[q]
			mk = self.marks[i]
			r["idx"] = i
			if i == self.sel:
				r["bgS"].Show(); r["bgN"].Hide()
			else:
				r["bgN"].Show(); r["bgS"].Hide()
			for t in xrange(4):
				if t == mk["t"]:
					r["dots"][t].Show()
				else:
					r["dots"][t].Hide()
			r["name"].SetText(mk["n"])
			r["right"].SetText("%d, %d" % (int(mk["x"]), int(mk["y"])))
			r["name"].Show()
			r["right"].Show()
		# klasik kaydirma cubugu tutamagi (liste satir sayisini asinca)
		n = len(items)
		if n > self.ROWS:
			rail = K.SCROLL[3] - 34 - K.THUMB[1]
			p = self.listTop / float(max(1, n - self.ROWS))
			self.thumb.SetPosition(int(round(self.x0 + K.SCROLL[0] * self.k)), int(round(self.y0 + (K.SCROLL[1] + 17 + rail * p) * self.k)))
			self.thumb.Show()
		else:
			self.thumb.Hide()

	# ------------------------------------------------------------------ secim karti
	def __Select(self, i):
		self.sel = i
		mk = self.marks[i]
		self.popTy.SetText(TYPES[mk["t"]][1])
		self.popTy.SetPackedFontColor(TYPES[mk["t"]][2])
		for t in xrange(4):
			if t == mk["t"]:
				self.popDots[t].Show()
			else:
				self.popDots[t].Hide()
		self.popName.SetText(mk["n"])
		dist = int(round(math.hypot(mk["x"] - self.me[0], mk["y"] - self.me[1])))
		self.popXY.SetText("%d, %d \xb7 %d m" % (int(mk["x"]), int(mk["y"]), dist))
		self.popLayer.Show()
		self.popGoTap.Show()
		self.__RefreshList()
		self.__PlacePop()

	def __HidePop(self):
		self.sel = -1
		self.popLayer.Hide()
		self.popGoTap.Hide()

	def __PlacePop(self):
		if self.sel < 0:
			return
		mk = self.marks[self.sel]
		(sx, sy) = self.__ToScreen(mk["x"], mk["y"])
		k = self.k
		vx0, vy0, vw, vh = self.VR
		pw, ph = K.POP_BOX[2] * k, K.POP_BOX[3] * k
		px = max(vx0 + 6, min(vx0 + vw - pw - 6, sx - pw / 2.0))
		py = sy - ph - 22 * k
		if py < vy0 + 4:
			py = sy + 22 * k
		ox = px - self.x0
		oy = py - self.y0
		s = k / TEX_S

		def put(w, g):
			w.SetPosition(int(round(px + g[0] * k)), int(round(py + g[1] * k)))
		put(self.pop, K.pop)
		put(self.popGo, K.btn_go)
		for dd in self.popDots:
			put(dd, K.POP_DOT)
		self.popTy.SetPosition(int(px + K.POP_TY[0] * k), int(py + K.POP_TY[1] * k))
		self.popName.SetPosition(int(px + K.POP_NAME[0] * k), int(py + K.POP_NAME[1] * k))
		self.popXY.SetPosition(int(px + K.POP_XY[0] * k), int(py + K.POP_XY[1] * k))
		self.popGoT.SetPosition(int(px + K.GO_TXT[0] * k), int(py + K.GO_TXT[1] * k))
		g = K.btn_go
		self.popGoTap.SetPosition(int(px + g[0] * k), int(py + g[1] * k))
		self.popGoTap.SetSize(int(g[2] * k), int(g[3] * k))
		self.popGoTap.SetTop()

	def __OnGo(self):
		if self.sel < 0:
			return
		mk = self.marks[self.sel]
		self.Close()
		if self.guide:
			self.guide.Start(mk["n"], mk["x"], mk["y"], TYPES[mk["t"]][0], self.meG, self.me)

	# ------------------------------------------------------------------ olaylar
	def __OnCenter(self):
		self.__Focus(self.me[0], self.me[1], max(self.scale, 1.1))

	def __OnDetail(self):
		self.details = not self.details
		if self.details:
			self.bDetailOn.Show()
			self.detailT.SetPackedFontColor(C_KGOLD)
		else:
			self.bDetailOn.Hide()
			self.detailT.SetPackedFontColor(C_CREAM)
		self.dirty = True

	def __OnChip(self, i):
		self.show[i] = not self.show[i]
		if self.sel >= 0 and self.marks[self.sel]["t"] == i and not self.show[i]:
			self.__HidePop()
		self.__RefreshChips()
		self.__RefreshList()
		self.dirty = True

	def OnAreaDown(self, name):
		(mx, my) = wndMgr.GetMousePosition()
		self.drag = {"name": name, "x0": mx, "y0": my, "x": mx, "y": my, "t0": app.GetTime(), "moved": False,
					 "tx": self.tx, "ty": self.ty, "top": self.listTop}

	def __TrackDrag(self):
		d = self.drag
		if not d:
			return
		(mx, my) = wndMgr.GetMousePosition()
		down = wndMgr.IsLeftButtonDown()
		if abs(mx - d["x0"]) + abs(my - d["y0"]) > 8:
			d["moved"] = True
		if d["name"] == "map" and d["moved"]:
			self.tx = d["tx"] + (mx - d["x0"])
			self.ty = d["ty"] + (my - d["y0"])
			self.__Clamp()
			self.dirty = True
		elif d["name"] == "list" and d["moved"]:
			nt = d["top"] - int((my - d["y0"]) / (K.ROW_STEP * self.k))
			if nt != self.listTop:
				self.listTop = nt
				self.__RefreshList()
		if down:
			return
		self.drag = None
		if d["moved"]:
			return
		# dokunma
		if d["name"] == "map":
			t = app.GetTime()
			(lt, lx, ly) = self.lastTap
			if t - lt < 0.33 and abs(lx - mx) + abs(ly - my) < 30:
				self.__ZoomAt(1.6, (mx - self.VR[0], my - self.VR[1]))
				self.lastTap = (-10.0, 0, 0)
				return
			self.lastTap = (t, mx, my)
			if self.details:
				for (x0, y0, x1, y1, i) in getattr(self, "lbRects", []):
					if x0 - 4 <= mx <= x1 + 4 and y0 - 4 <= my <= y1 + 4:
						self.__Select(i)
						return
			best = None
			bd = 26.0 * self.k
			for (i, sx, sy) in getattr(self, "vis", []):
				dd = math.hypot(sx - mx, sy - my)
				if dd < bd:
					bd = dd
					best = i
			if best is not None:
				self.__Select(best)
			else:
				self.__HidePop()
				self.__RefreshList()
		elif d["name"] == "list":
			j = int((my - (self.y0 + K.ROW[1] * self.k)) / (K.ROW_STEP * self.k))
			if 0 <= j < self.ROWS and self.rows[j]["idx"] >= 0:
				i = self.rows[j]["idx"]
				mk = self.marks[i]
				self.__Focus(mk["x"], mk["y"])
				self.__Select(i)

	def OnUpdate(self):
		t = app.GetTime()
		self.__TrackDrag()
		# kahraman konumu (yurudukce)
		old = self.me
		self.__RefreshMe()
		if abs(old[0] - self.me[0]) + abs(old[1] - self.me[1]) > 0.3:
			self.meXY.SetText("%d, %d" % (int(self.me[0]), int(self.me[1])))
			self.dirty = True
		if self.dirty:
			self.dirty = False
			self.__PlaceTiles()
			self.__PlaceMarks()
			self.__LayoutLabels()
			self.__PlacePop()
		elif self.meMk and self.meIn:
			(sx, sy) = self.__ToScreen(self.me[0], self.me[1])
			self.__RotAt(self.meMk, sx, sy, self.meRot, 1.0)
		# kahraman ping halkasi (2.2 s): olcek .45 -> 1.25, alfa .9 -> 0
		if self.mePing and self.meIn:
			(sx, sy) = self.__ToScreen(self.me[0], self.me[1])
			p = (t % 2.2) / 2.2
			self.__RotAt(self.mePing, sx, sy, 0.0, 0.45 + 0.8 * p, 0.9 * (1.0 - p))
			self.mePing.Show()


# ======================================================================================================== yol gosterici
class GuideOverlay(ui.Window):
	N_CHEV = 5
	CHEV_PERIOD = 1.35
	NDIR = 32

	def __init__(self):
		ui.Window.__init__(self, "TOP_MOST")		# "UI" katmani kokune telefonda OnUpdate gelmiyordu
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("YolGosterici")
		self.W = float(wndMgr.GetScreenWidth())
		self.H = float(wndMgr.GetScreenHeight())
		self.k = self.H / 705.0
		self.SetPosition(0, 0)
		self.SetSize(int(self.W), int(self.H))
		self.AddFlag("not_pick")
		self.keep = []
		self.tex = {}
		self.on = False
		self.done = -1.0
		self.target = None
		self.onMap = None
		self.ring = self.__Img("gring.png")
		self.chev = []
		for i in xrange(self.N_CHEV):
			w = self.__Img("chev_00.png")
			self.chev.append({"w": w, "dir": 0})
		self.needleBg = self.__Img("needle_bg.png")
		self.needle = self.__Img("needle.png")
		self.tag = self.__Img("tag.png")
		self.tagBar = ui.Bar()
		self.tagBar.SetParent(self)
		self.tagBar.AddFlag("not_pick")
		self.tagBar.SetColor(0xd80c0805)
		self.tagBar.Hide()
		self.keep.append(self.tagBar)
		self.tName = self.__Text(17, 0xfffff6e0)
		self.tDist = self.__Text(17, 0xffffd060)
		self.dots = {}
		for (key, ad, col) in TYPES:
			self.dots[key] = self.__Img("dot_%s.png" % key)
		self.dot = self.dots["npc"]
		self.arrived = self.__Text(20, 0xfffff2c8, center=True)
		self.arrived.SetText("HEDEFE ULA\xdeTIN")
		self.bMap = self.__Img("btn_gmap.png")
		self.bStop = self.__Img("btn_gstop.png")
		self.tapMap = _Tap(self, self.__OnMap)
		self.tapStop = _Tap(self, self.Stop)
		self.keep += [self.tapMap, self.tapStop]
		for (w, g) in ((self.bMap, G.btn_gmap), (self.bStop, G.btn_gstop)):
			self.__PlaceBtn(w, g)
		for (tp, g) in ((self.tapMap, G.btn_gmap), (self.tapStop, G.btn_gstop)):
			x = (self.W - 1280.0 * self.k) / 2.0 + g[0] * self.k
			tp.SetPosition(int(x), int(g[1] * self.k))
			tp.SetSize(int(g[2] * self.k), int(g[3] * self.k))
		self.__ShowAll(False)
		self.Show()

	def SetMapOpener(self, func):
		self.onMap = func

	# ------------------------------------------------------------------ yardimcilar
	def __Img(self, name):
		w = ui.ExpandedImageBox()
		w.SetParent(self)
		w.AddFlag("not_pick")
		w.LoadImage(DIR + name)
		max(0, 0)
		self.tex[w] = (float(w.GetWidth()), float(w.GetHeight()))
		w.SetScale(self.k / TEX_S, self.k / TEX_S)
		w.Hide()
		self.keep.append(w)
		return w

	def __Text(self, pt, color, center=False):
		t = ui.TextLine()
		t.SetParent(self)
		t.AddFlag("not_pick")
		t.SetFontName(FONT % max(8, int(round(pt * self.k))))
		if center:
			t.SetHorizontalAlignCenter()
		t.SetOutline()
		t.SetPackedFontColor(color)
		t.Hide()
		self.keep.append(t)
		return t

	def __PlaceBtn(self, w, g):
		x = (self.W - 1280.0 * self.k) / 2.0 + g[0] * self.k
		w.SetPosition(int(x), int(g[1] * self.k))

	def __ShowAll(self, on):
		for w in [self.ring, self.needleBg, self.needle, self.tag, self.tagBar, self.tName, self.tDist, self.dot, self.bMap, self.bStop,
				  self.tapMap, self.tapStop] + [c["w"] for c in self.chev]:
			if w is None:
				continue
			if on:
				w.Show()
			else:
				w.Hide()
		if not on:
			self.arrived.Hide()

	def __Put(self, w, cx, cy, sc=1.0, a=1.0, deg=0.0, sx=None):
		"""gorsel merkezini (cx, cy) ekran px'e koy."""
		(tw, th) = self.tex[w]
		s = self.k / TEX_S * sc
		fx = s * (sx if sx else 1.0)
		ix = int(math.floor(cx))
		iy = int(math.floor(cy))
		w.SetScale(fx, s)
		w.SetPosition(ix, iy)
		w.SetOrigin(cx - ix, cy - iy)
		w.SetRotation(deg if abs(deg) > 1e-4 else 1e-4)
		w.SetAlpha(max(0.0, min(1.0, a)))

	# ------------------------------------------------------------------ dis API
	def Start(self, name, x, y, typeKey, meG, meL):
		self.target = (x, y)
		self.name = name
		self.done = -1.0
		self.tName.SetText(name)
		for d in self.dots.values():
			d.Hide()
		self.dot = self.dots.get(typeKey, self.dots["npc"])
		self.on = True
		self.__ShowAll(True)
		self.arrived.Hide()
		self.SetTop()
		# mini haritada hedef (waypoint: global birim)
		try:
			miniMap.RemoveWayPoint(WAYPOINT_ID)
			miniMap.AddWayPoint(WAYPOINT_ID, float(x * 100.0), float(y * 100.0), name)
		except:
			pass

	def Stop(self):
		self.on = False
		self.target = None
		self.__ShowAll(False)
		try:
			miniMap.RemoveWayPoint(WAYPOINT_ID)
		except:
			pass

	def IsActive(self):
		return self.on

	def Destroy(self):
		self.Stop()
		self.Hide()
		self.onMap = None
		self.keep = []
		self.chev = []
		self.dots = {}
		self.tex = {}

	def __OnMap(self):
		if self.onMap:
			self.onMap()

	def SetHiddenForMap(self, hidden):
		if not self.on:
			return
		self.__ShowAll(not hidden)

	# ------------------------------------------------------------------ kare
	def __Feet(self):
		"""kahramanin ayak noktasi (ekran px). Izdusum bazen sacma (bkz. uioyuncupaneli) -> ekran icinde degilse sabit."""
		try:
			vid = player.GetMainCharacterIndex()
			(x, y) = chr.GetProjectPosition(vid, 0)
			if 0 < x < self.W and self.H * 0.25 < y < self.H:
				return (float(x), float(y))
		except:
			pass
		return (self.W * 0.49, self.H * 0.61)

	def OnUpdate(self):
		if not self.on or not self.target:
			return
		if not self.bMap.IsShow() and not self.ring.IsShow():
			return		# harita acikken gizli
		t = app.GetTime()
		k = self.k
		(px, py, gx, gy) = _playerLocal()
		dx = self.target[0] - px
		dy = self.target[1] - py
		dist = math.hypot(dx, dy)
		(fx, fy) = self.__Feet()
		# hedefin harita acisi (kuzeyden saat yonu) - kamera acisi = ekranda yukaridan saat yonu
		beta = math.degrees(math.atan2(dx, -dy))
		try:
			roll = app.GetCameraRotation()
		except:
			roll = 0.0
		rel = beta - roll
		ang = rel - 90.0					# zemin duzleminde +x'ten saat yonu (css rotateZ)
		ar = math.radians(ang)
		sq = G.PLANE_SQUASH
		# varis
		if self.done < 0.0 and dist < 5.0:
			self.done = t
			self.arrived.SetPosition(int(self.W / 2.0), int(self.H * 0.30))
			self.arrived.Show()
			for c in self.chev:
				c["w"].Hide()
			try:
				miniMap.RemoveWayPoint(WAYPOINT_ID)
			except:
				pass
		# zemin halkasi
		gr = G.GRING
		rcx = fx + (gr[0] + gr[2] / 2.0) * k
		rcy = fy + (gr[1] + gr[3] / 2.0) * k
		if self.done >= 0.0:
			e = (t - self.done) / 0.8
			self.__Put(self.ring, rcx, rcy, 1.0 + 1.2 * min(1.0, e), max(0.0, 1.0 - e))
			if t - self.done > 1.8:
				self.Stop()
			return
		pulse = 0.5 - 0.5 * math.cos(t / 1.8 * 2.0 * math.pi)
		self.__Put(self.ring, rcx, rcy, 1.0 + 0.08 * pulse, 1.0 - 0.4 * pulse)
		# akan oklar: 60 -> 360 tasarim px, opaklik 0 / .9 (%15) / .6 (%70) / 0, olcek .85 -> 1.08
		di = int(round(ang / (360.0 / self.NDIR))) % self.NDIR
		cg = G.CHEV[di]
		for j in xrange(self.N_CHEV):
			c = self.chev[j]
			if c["dir"] != di:
				c["w"].LoadImage(DIR + "chev_%02d.png" % di)
				max(0, 0)
				self.tex[c["w"]] = (float(c["w"].GetWidth()), float(c["w"].GetHeight()))
				c["dir"] = di
			p = ((t + j * self.CHEV_PERIOD / self.N_CHEV) % self.CHEV_PERIOD) / self.CHEV_PERIOD
			d = 60.0 + 300.0 * p
			if p < 0.15:
				a = 0.9 * p / 0.15
			elif p < 0.7:
				a = 0.9 - 0.3 * (p - 0.15) / 0.55
			else:
				a = 0.6 * (1.0 - (p - 0.7) / 0.3)
			sc = 0.85 + 0.23 * p
			ccx = fx + (cg[0] + cg[2] / 2.0) * k + math.cos(ar) * d * k
			ccy = fy + (cg[1] + cg[3] / 2.0) * k + math.sin(ar) * d * k * sq
			self.__Put(c["w"], ccx, ccy, sc, a)
		# bas ustu igne + etiket (bob 1.4 s, 5 px)
		bob = -5.0 * k * (0.5 - 0.5 * math.cos(t / 1.4 * 2.0 * math.pi))
		hx = fx
		hy = fy - self.H * 0.36 + bob
		ng = G.needle_bg
		self.__Put(self.needleBg, hx + (ng[0] + ng[2] / 2.0) * k, hy + (ng[1] + ng[3] / 2.0) * k)
		nd = G.needle
		self.__Put(self.needle, hx + (nd[0] + nd[2] / 2.0) * k, hy + (nd[1] + nd[3] / 2.0) * k, 1.0, 1.0, rel)
		self.tDist.SetText("%d m" % int(round(dist)))
		(w1, h1) = self.tName.GetTextSize()
		(w2, h2) = self.tDist.GetTextSize()
		tw = w1 + w2 + 24 * k
		tg = G.tag
		tcy = hy + (tg[1] + tg[3] / 2.0) * k
		(txw, txh) = self.tex[self.tag]
		self.__Put(self.tag, hx, tcy, 1.0, 1.0, 0.0, max(1.0, (tw + 40 * k) / (txw * k / TEX_S)))
		x0 = hx - tw / 2.0
		bh = int(max(h1, h2) + 10 * k)
		self.tagBar.SetPosition(int(x0 - 6 * k), int(tcy - bh / 2.0))
		self.tagBar.SetSize(int(tw + 12 * k), bh)
		self.__Put(self.dot, x0 + 5 * k, tcy, 0.6)
		self.tName.SetPosition(int(x0 + 14 * k), int(tcy - h1 / 2.0 - 1))
		self.tDist.SetPosition(int(x0 + 14 * k + w1 + 8 * k), int(tcy - h2 / 2.0 - 1))
