# MOBIL - mobile_root/uihedefkarti.py: CANAVAR / METIN HEDEF KARTI + "DUSEN ESYALAR" PENCERESI.
# URETILIR: tools/hedefkarti/uihedefkarti_kaynak.py (UTF-8) -> tools/hedefkarti/gen_uihedefkarti.py -> bu dosya (cp1254 kacisli).
#
# KULLANICI (2026-10-01): eski ince hedef penceresi ust menunun (Sohbet/Karakter/Envanter...) USTUNE biniyordu.
#   Prototip Desktop/Averos2-Hedef-Prototip/hedef_klasik.html: "mukemmel, uygula - bug cikmasin".
#   Kabuk clientin KENDI dokulari (ThinBoard kart, Board pencere, TitleBar, slot_base, middle_button, close_button);
#   can cubugu kodla cizildi (tools/hedefkarti/bake_hedefkarti.py -> mobile/ui/hdk/).
# Kapsam: yalniz OYUNCU OLMAYAN hedefler (canavar, metin tasi, patron). Oyuncu paneli (uioyuncupaneli), duello
#   paneli ve kendi karakterin menusu (at inme/gozlemci) ESKISI GIBI uitarget'ta kalir.
# Veri: "Dusenler" = eski "?" dugmesinin aynisi: net.SendTargetInfoLoad -> game.BINARY_AddTargetMonsterDropInfo
#   (constInfo.MONSTER_INFO_DATA; silah/zirh +N ve ruh taslari tek satirda gruplu) -> BINARY_RefreshTargetMonsterDropInfo
#   -> TargetBoard.RefreshMonsterInfoBoard -> RefreshDrops.
# Dokunma: kok 1x1 hep acik + hide_on_outside -> OnOutsideTap = TargetBoard.OnOutsideTap (eski ince pencereyle AYNI davranis).
# Olcu: tasarim birimi = prototip sahnesi (1568x705); k = ekran yuksekligi / 705; dokular fiziksel (x1220/705) -> IMG_S.

import ui
import wndMgr
import app
import dbg
import player
import chr
import net
import item
import nonplayer
import localeInfo
import constInfo

DIR = "mobile/ui/hdk/"
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
REF_H = 705.0
IMG_S = 705.0 / 1220.0
TOP_FRAC = 0.135			# uioyuncupaneli ile ayni: ust HUD sirasinin altinda
OPEN_SEC = 0.16
FILL_SEC = 0.25			# can dolgusu yumusak iner
GHOST_WAIT = 0.45			# kaybedilen can izi once bekler
GHOST_SEC = 0.6			# sonra kapanir
DROPS_WAIT = 2.5			# sunucu dusen esya yaniti icin en fazla bekleme (sn)
STONE_CYCLE = 2.5			# ruh tasi yuvasi 2,5 sn'de bir cesit degistirir (eski pencere gibi)
# KULLANICI (2026-10-01 telefonda): "ekran cok kucuk, yazilar zor okunuyor" -> bake_hedefkarti.py ile AYNI oranlar
ZOOM_CARD = 1.15
ZOOM_DROPS = 1.3
FONT_BOOST = 1.15			# oyun fontu kalin degil: yazilar ayrica buyur
# KULLANICI (2026-10-01): "Dusen Esyalar yazisi pixel pixel" -> motor (GrpFontTexture ComputeBakeSize) yaziyi en fazla
# 32 px pisirir; telefonda 1 mantiksal px = 1.73 fiziksel -> 18 pt ustu buyutulerek cizilir (pikselli). Tavan 18.
FONT_MAX = 18
# KULLANICI (2026-10-01): "metinin ustune tiklayinca acilan panel ekranin ustune yapisik ciksin"
# -> kart ust kenarda; soldaki HUD (Gizle/Etkinlik) ile ust menu (Sohbet...Menu, sagdan ~744) ARASINDAKI bosluga ortalanir.
CARD_TOP = 4
# KULLANICI (2026-10-01): "her telefonda ayni cikmali". Ust HUD GENISLIGIN ORANIYLA yerlesir (uiscript/mobilehud.py PX):
# Gizle merkezi 0.075 W, dugme 46 px; Sohbet dugme+yazisinin sol kenari 1568 genislikte 832 olculdu -> 832/1568 W.
HUD_LEFT_FRAC = 0.075		# Gizle merkezi (mobilehud.py HideButton cx)
HUD_LEFT_HALF = 23 + 1		# yarim dugme (MD 46) + 1 px pay
HUD_RIGHT_FRAC = 832.0 / 1568.0	# Sohbet sol kenari / genislik
# KULLANICI (2026-10-01): "sigmiyorsa ona gore boyutlanmali; PUBG'de ust menunun alta indigini gordun mu" ->
# kart HER telefonda ustte, yalniz boyutu bosluga uyar. (4:3 tablette arada yer yok -> gecici yedek, bkz. __Layout)
CARD_FIT_MIN = 0.5
HUD_GAP = 6			# kart ile dugmeler arasi bosluk (mantiksal px)
# KULLANICI (2026-10-01): "kafaya gore olmaz" -> bosluk HUD dugmelerinin GERCEK konumundan olculur (uimobilehud)
HUD_LEFT_NAMES = ("HideButton",)
HUD_TOP_NAMES = ("ChatButton", "CharacterButton", "InventoryButton", "MessengerButton", "SystemButton",
	"DeleteItemButton", "KeyPanelButton", "MenuButton")

# ---- olculer (bake_hedefkarti.py ile AYNI) ----
CARD_W, CARD_H = 590, 88
MEDAL_X, MEDAL_Y = 16, 16
NAME_X, NAME_Y = 84, 17
HP_X, HP_Y, HP_W, HP_H = 84, 46, 384, 19
HP_IN_X0, HP_IN_Y0, HP_IN_W, HP_IN_H = 11, 4, 362, 11
BTN_DROPS_X, BTN_DROPS_Y = 478, 16
BTN_CLOSE_X, BTN_CLOSE_Y = 550, 16
DROPS_W, DROPS_H = 664, 428
DROPS_GAP = 7
TITLE_Y, TITLE_H = 8, 34
SLOT, SLOT_GAP = 60, 6
GRID_COLS, GRID_ROWS = 9, 3
PAGE = GRID_COLS * GRID_ROWS
GRID_X, GRID_Y = 38, 144
STAT_X, STAT_Y, STAT_W, STAT_GAP = 19, 50, 152, 6
TAB_X, TAB_Y, TAB_W, TAB_H, TAB_GAP = 18, 102, 84, 28, 6
MAX_TABS = 7
PANEL = (18, 138, 628, 204)
DETAIL_X, DETAIL_Y, DETAIL_W, DETAIL_H = 18, 350, 628, 60
DCLOSE_X, DCLOSE_Y = 629, 12.5
PG_Y = 368
PG_L_X, PG_R_X = 548, 604

# ---- renkler ----
C_WHITE = 0xffffffff
C_CREAM = 0xfff1e6c0
C_SUB = 0xffc9b88f
C_OFF = 0xff8f8470
C_GOLD = 0xffe8d08a
C_GOLD_TXT = 0xfff6e1b3
C_TITLE_SUB = 0xffe8d4a8
C_DARK = 0xff1b1206
C_STONE_TXT = 0xffdbeeff
PILLS = {
	"gold": (0x8c000000, 0xff6b5a3e, C_GOLD),
	"dark": (0x8c000000, 0xff4d4232, C_SUB),
	"king": (0xbf5a140a, 0xffa0522d, 0xffffcf9a),
}
CATS = (
	("weapon", "Silah", 0xffe2b95f),
	("armor", "Z\xfdrh", 0xffc9a877),
	("stone", "Ruh ta\xfe\xfd", 0xff6fb0e6),
	("book", "Kitap", 0xffb08fe0),
	("chest", "Sand\xfdk", 0xff62c27a),
	("other", "Di\xf0er", 0xff8d7d62),
)
CAT_NAME = dict([(c[0], c[1]) for c in CATS])
CAT_COLOR = dict([(c[0], c[2]) for c in CATS])


def _Grade(g):
	for (attr, label) in (("KING", "Kral"), ("BOSS", "Patron"), ("S_KNIGHT", "G\xfc\xe7l\xfc Se\xe7kin"), ("KNIGHT", "Se\xe7kin"), ("S_PAWN", "G\xfc\xe7l\xfc"), ("PAWN", "S\xfdradan")):
		try:
			if g == getattr(nonplayer, attr):
				return (attr, label)
		except:
			pass
	return ("", "")


def _Dotted(n):
	try:
		return localeInfo.DottedNumber(max(0, int(n)))
	except:
		return str(n)


def _ItemCat(vnum):
	try:
		item.SelectItem(vnum)
		t = item.GetItemType()
	except:
		return "other"
	if t == item.ITEM_TYPE_WEAPON:
		return "weapon"
	if t == item.ITEM_TYPE_ARMOR:
		return "armor"
	if t == item.ITEM_TYPE_METIN:
		return "stone"
	if t == getattr(item, "ITEM_TYPE_SKILLBOOK", -99) or t == getattr(item, "ITEM_TYPE_SKILLFORGET", -99):
		return "book"
	if t == getattr(item, "ITEM_TYPE_GIFTBOX", -99) or t == getattr(item, "ITEM_TYPE_TREASURE_BOX", -99):
		return "chest"
	return "other"


def _ItemName(vnum):
	try:
		item.SelectItem(vnum)
		return item.GetItemName() or ""
	except:
		return ""


def _BaseName(name):
	i = name.find("+")
	if i > 0:
		return name[:i].rstrip()
	return name


def _Boy(vnum):
	"""esyanin dikey yuva sayisi (1..GRID_ROWS)"""
	try:
		item.SelectItem(vnum)
		(w, h) = item.GetItemSize()
		return max(1, min(GRID_ROWS, int(h)))
	except:
		return 1


def _Bos(occ, h):
	"""satir satir ilk bos yer (envanter gibi): h yuva alt alta bos olmali"""
	for r in xrange(GRID_ROWS - h + 1):
		for c in xrange(GRID_COLS):
			ok = True
			for i in xrange(h):
				if (r + i, c) in occ:
					ok = False
					break
			if ok:
				return (r, c)
	return None


def _Yerlestir(lst):
	"""COK YUVALI ESYA (KULLANICI 2026-10-04: "cift slotlu item cift slotta olmali"): her esya boyu kadar yuva kaplar.
	Esya ilk sigdigi sayfaya / yere girer (envanterin otomatik yerlestirmesi gibi). -> [[(e, sutun, satir, boy), ...], ...]"""
	pages = []
	for e in lst:
		h = max(1, min(GRID_ROWS, e.get("h", 1)))
		yer = None
		for pg in pages:
			pos = _Bos(pg[0], h)
			if pos:
				yer = (pg, pos)
				break
		if yer is None:
			pg = (set(), [])
			pages.append(pg)
			yer = (pg, _Bos(pg[0], h))
		(pg, (r, c)) = yer
		for i in xrange(h):
			pg[0].add((r + i, c))
		pg[1].append((e, c, r, h))
	return [pg[1] for pg in pages]


def _Entries(race):
	"""constInfo.MONSTER_INFO_DATA[race]["items"] -> ekran satirlari. Veri yoksa None."""
	try:
		data = constInfo.MONSTER_INFO_DATA
	except:
		return None
	if race not in data:
		return None
	out = []
	for cur in data[race].get("items", []):
		try:
			count = int(cur.get("count", 1))
			if cur.has_key("vnum_list"):
				vnums = sorted([int(v) for v in cur["vnum_list"]])
			else:
				vnums = [int(cur["vnum"])]
			if not vnums:
				continue
			cat = _ItemCat(vnums[0])
			e = {"vnums": vnums, "count": count, "cat": cat, "badge": "", "rng": "", "extra": ""}
			if cat == "stone":
				lv = sorted(set([(v % 1000) // 100 for v in vnums]))
				e["rng"] = (len(lv) > 1) and ("+%d~%d" % (lv[0], lv[-1])) or ("+%d" % lv[0])
				stoneName = "Ruh Ta\xfe\xfd"		# localeInfo.TARGET_INFO_STONE_NAME bu sunucuda "Metin" (yaniltici)
				e["name"] = (len(lv) > 1) and ("%s +%d \x96 +%d" % (stoneName, lv[0], lv[-1])) or ("%s +%d" % (stoneName, lv[0]))
				n = len(set([v % 100 for v in vnums]))
				e["extra"] = (n > 1) and ("%d \xe7e\xfeit" % n) or ""
			elif cat in ("weapon", "armor"):
				ups = sorted(set([v % 10 for v in vnums]))
				nm = _ItemName(vnums[-1])
				if len(ups) > 1:
					e["name"] = "%s +%d \x96 +%d" % (_BaseName(nm), ups[0], ups[-1])
					e["badge"] = "+%d~%d" % (ups[0], ups[-1])
				else:
					e["name"] = nm
					if ups[0] > 0:
						e["badge"] = "+%d" % ups[0]
			else:
				e["name"] = _ItemName(vnums[0])
			if not e["name"]:
				e["name"] = "#%d" % vnums[0]
			e["h"] = _Boy(vnums[-1])
			out.append(e)
		except:
			continue
	return out


def HudGap(scrH, k):
	"""(sol, sag) mantiksal px: Gizle dugmesinin sag kenari ile ust menu sirasinin en soldaki dugmesinin sol kenari
	arasindaki bosluk (HUD_GAP payi dusulmus). GERCEK konumlar uimobilehud.GetInstance'tan; HUD yoksa None.
	Hedef karti (metin/canavar) ve oyuncu karti (uioyuncupaneli) AYNI yuvayi kullanir."""
	try:
		import uiMobileHud
		hud = uiMobileHud.GetInstance()
	except:
		hud = None
	if not hud:
		return None
	left = None
	right = None
	try:
		for n in HUD_LEFT_NAMES:
			w = hud.GetChild2(n)
			if w:
				(x, y) = w.GetGlobalPosition()
				r = x + w.GetWidth()
				left = (left is None) and r or max(left, r)
		for n in HUD_TOP_NAMES:
			w = hud.GetChild2(n)
			if w:
				(x, y) = w.GetGlobalPosition()
				if y > scrH * 0.5:		# duzen editoruyle asagi tasinmis dugme kartin satirinda degil
					continue
				right = (right is None) and x or min(right, x)
	except:
		return None
	if left is None or right is None or right <= left:
		return None
	return (int(left) + int(round(HUD_GAP * k)), int(right) - int(round(HUD_GAP * k)))


def HudGapOrFrac(scrW, scrH, k):
	"""HudGap; HUD yoksa oranli yedek (mobilehud.py formulu: Gizle 0.075 W, ust sira sag kenara bagli)"""
	g = HudGap(scrH, k)
	if g is None:
		g = (int(round(HUD_LEFT_FRAC * scrW + HUD_LEFT_HALF * k)), int(round(HUD_RIGHT_FRAC * scrW)))
	return g


def _Ease(t):
	t = 1.0 - t
	return 1.0 - t * t * t


class _Hit(ui.Window):
	"""gorunmez dokunma alani (yuva)"""

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


class _Root(ui.Window):
	"""kart / pencere icin KENDI boyutunda kok: icindeki her dokunusu yakalar (yuva, bos alan). Disari dokunma:
	dunya -> OnOutsideTap (eski ince pencereyle ayni: hedef birakilir), baska arayuz -> OnOutsideTapUI (acik kalir)."""

	def __init__(self, owner, z):
		ui.Window.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.AddFlag("hide_on_outside")
		self.owner = owner
		self.z = z

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		return True

	def OnMouseLeftButtonUp(self):
		return True

	def OnOutsideTap(self):
		o = self.owner
		if o:
			o.OnOutsideTap()

	def OnOutsideTapUI(self):
		pass


class HedefKarti(ui.Window):

	def __init__(self, board):
		ui.Window.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)		# olcek kendimizde (k)
		self.SetWindowName("MobileTargetCard")
		self.SetSize(1, 1)
		self.SetPosition(0, 0)
		self.board = board
		self.keep = []
		self.scrW = wndMgr.GetScreenWidth()
		self.scrH = wndMgr.GetScreenHeight()
		self.k = self.scrH / REF_H
		self.fit = 1.0
		self.layoutKey = None
		self.__Layout()
		self.vid = 0
		self.race = 0
		self.level = -1
		self.dropsAsked = 0.0
		self.dropsAnswered = False
		self.gradeLabel = ""
		self.isStone = False
		self.state = "kapali"
		self.animT0 = 0.0
		# can
		self.hpTarget = 100.0
		self.hpShown = 100.0
		self.hpFrom = 100.0
		self.hpT0 = 0.0
		self.ghost = 100.0
		self.ghostFrom = 100.0
		self.ghostT0 = 0.0
		# dusenler
		self.entries = None
		self.filter = "all"
		self.page = 0
		self.sel = None
		self.cycle = 0
		self.nextCycle = 0.0
		self.__BuildCard()
		self.__BuildDrops()
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def __HudGap(self):
		return HudGap(self.scrH, self.k)

	def __Layout(self):
		"""kart konumu + olcegi. KULLANICI (2026-10-01): her telefonda AYNI yerlesim: kart HEP ustte, Gizle ile ust menu
		arasinda; bosluk HUD'un gercek konumundan (yoksa oranla); sigmazsa orantili kuculur. True = degisti."""
		g = self.__HudGap()
		if g is None:
			g = (int(round(HUD_LEFT_FRAC * self.scrW + HUD_LEFT_HALF * self.k)), int(round(HUD_RIGHT_FRAC * self.scrW)))
		(gapL, gapR) = g
		full = CARD_W * self.k * ZOOM_CARD
		fit = 1.0
		if gapR - gapL < full:
			fit = (gapR - gapL) / full
		if fit >= CARD_FIT_MIN:
			cw = int(round(CARD_W * self.k * ZOOM_CARD * fit))
			x = gapL + max(0, (gapR - gapL - cw) // 2)
			y = int(round(CARD_TOP * self.k))
		else:
			# GECICI: 4:3 tablet (iPad) - ust menu Gizle'ye neredeyse degiyor, arada kart icin YER YOK. Kalici cozum
			# motor duzeyinde: mantiksal cozunurlukte EN AZ genislik (M2Android_FullscreenGameSize / iOS esdegeri).
			fit = 1.0
			cw = int(round(CARD_W * self.k * ZOOM_CARD))
			x = (self.scrW - cw) // 2
			y = int(round(self.scrH * TOP_FRAC))
		key = (x, y, round(fit, 3))
		if key == self.layoutKey:
			return False
		self.layoutKey = key
		self.fit = fit
		self.cardX = x
		self.cardY = y
		return True

	def __Rebuild(self):
		"""HUD duzeni degisti: kart + pencere yeni olcek/konumla yeniden kurulur"""
		for n in ("box", "dbox"):
			w = getattr(self, n, None)
			if w:
				try:
					w.Hide()
					w.owner = None
				except:
					pass
		self.keep = []
		self.medalKind = None
		self.__BuildCard()
		self.__BuildDrops()

	def Destroy(self):
		self.Hide()
		try:
			self.box.Hide()
			self.dbox.Hide()
			self.box.owner = None
			self.dbox.owner = None
		except:
			pass
		self.keep = []
		self.cells = []
		self.tabs = []
		self.pills = []
		self.board = None

	# ------------------------------------------------------------------ yardimci
	def S(self, v):
		"""kart olcegi"""
		return int(round(v * self.k * ZOOM_CARD * self.fit))

	def D(self, v):
		"""pencere olcegi"""
		return int(round(v * self.k * ZOOM_DROPS))

	def _Z(self, parent):
		return getattr(parent, "z", None) or getattr(getattr(parent, "zroot", None), "z", 1.0)

	def _P(self, parent, v):
		return int(round(v * self.k * self._Z(parent)))

	def _ImgF(self, parent):
		return getattr(parent, "imgf", None) or getattr(getattr(parent, "zroot", None), "imgf", 1.0)

	def F(self, pt, z=ZOOM_CARD):
		return "Tahoma:%d" % max(8, min(FONT_MAX, int(round(pt * self.k * z * FONT_BOOST))))

	# ------------------------------------------------------------------ DOSEME (Dusen Esyalar zemini)
	def _PImg(self, path, parent, x, y, sx=1.0, sy=1.0):
		"""pack dokusu: 1 texel = sx/sy tasarim px (kokun zoom'u ile)"""
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(path)
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		z = self.k * self._Z(parent)
		w.SetScale(sx * z, sy * z)
		w.SetPosition(self._P(parent, x), self._P(parent, y))
		w.Show()
		self.keep.append(w)
		return w

	def _Tile(self, path, parent, x, y, w, h, tw, th, sx=1.0, sy=1.0):
		"""tw x th texel dokuyu (x, y, w, h) alanina doser; kenarlar _P(x) .. _P(x + w) tam sayisina OTURUR (bkz. _Otur)"""
		img = self._PImg(path, parent, x, y, sx, sy)
		z = self.k * self._Z(parent)
		(zx, r) = _Otur(self._P(parent, x + w) - self._P(parent, x), w, tw, sx, HAS_RRS, z)
		(zy, b) = _Otur(self._P(parent, y + h) - self._P(parent, y), h, th, sy, HAS_RRS, z)
		img.SetScale(zx, zy)
		img.SetRenderingRect(0.0, 0.0, r, b)
		return img

	def _Rect(self, parent, x, y, w, h, color, fill):
		b = ui.Bar() if fill else ui.Box()
		b.SetParent(parent)
		b.AddFlag("not_pick")
		b.SetColor(color)
		x0, y0 = self._P(parent, x), self._P(parent, y)
		b.SetPosition(x0, y0)
		b.SetSize(max(1, self._P(parent, x + w) - x0), max(1, self._P(parent, y + h) - y0))
		b.Show()
		self.keep.append(b)
		return b

	def __DropsZemin(self, d):
		"""eski drops_bg.png ile ayni: Board + TitleBar + baslik + 4 bilgi kutusu + yuva paneli + 27 yuva + ayrinti seridi"""
		W, H = DROPS_W, DROPS_H
		PT = "d:/ymir work/ui/pattern/"
		self._Tile(PT + "board_base.tga", d, 32, 32, W - 64, H - 64, 128, 128)
		self._Tile(PT + "board_line_top.tga", d, 32, 0, W - 64, 32, 128, 32)
		self._Tile(PT + "board_line_bottom.tga", d, 32, H - 32, W - 64, 32, 128, 32)
		self._Tile(PT + "board_line_left.tga", d, 0, 32, 32, H - 64, 32, 128)
		self._Tile(PT + "board_line_right.tga", d, W - 32, 32, 32, H - 64, 32, 128)
		for (n, cx, cy) in (("lefttop", 0, 0), ("righttop", W - 32, 0), ("leftbottom", 0, H - 32), ("rightbottom", W - 32, H - 32)):
			self._Tile(PT + "board_corner_%s.tga" % n, d, cx, cy, 32, 32, 32, 32)
		self._Tile(PT + "titlebar_center.tga", d, 8 + 48, TITLE_Y, W - 16 - 96, 34.5, 32, 32, 1.5, 1.5)
		self._Tile(PT + "titlebar_left.tga", d, 8, TITLE_Y, 48, 34.5, 32, 32, 1.5, 1.5)
		self._Tile(PT + "titlebar_right.tga", d, W - 8 - 48, TITLE_Y, 48, 34.5, 32, 32, 1.5, 1.5)
		self._Img("drops_baslik.png", d, 52, TITLE_Y)
		for (i, key) in enumerate(("can", "seviye", "rutbe", "irk")):
			bx = STAT_X + i * (STAT_W + STAT_GAP)
			self._Rect(d, bx, STAT_Y, STAT_W, 44, 0x80000000, True)
			self._Rect(d, bx, STAT_Y, STAT_W, 44, 0xff3d342a, False)
			self._Img("drops_lbl_%s.png" % key, d, bx + 10, STAT_Y + 6)
		self._Rect(d, PANEL[0], PANEL[1], PANEL[2], PANEL[3], 0x5a000000, True)
		self._Rect(d, PANEL[0], PANEL[1], PANEL[2], PANEL[3], 0xff3d342a, False)
		for r in xrange(GRID_ROWS):
			for c in xrange(GRID_COLS):
				self._PImg("d:/ymir work/ui/public/slot_base.sub", d, GRID_X + c * (SLOT + SLOT_GAP), GRID_Y + r * (SLOT + SLOT_GAP), SLOT / 32.0, SLOT / 32.0)
		self._Rect(d, DETAIL_X, DETAIL_Y, DETAIL_W, DETAIL_H, 0x73000000, True)
		self._Rect(d, DETAIL_X, DETAIL_Y, DETAIL_W, DETAIL_H, 0xff3d342a, False)
		self._PImg("d:/ymir work/ui/public/slot_base.sub", d, DETAIL_X + 4, DETAIL_Y + 4, 52 / 32.0, 52 / 32.0)

	def _Img(self, name, parent, x=0, y=0):
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(DIR + name)
		f = self.k * IMG_S * self._ImgF(parent)
		w.SetScale(f, f)		# dokular zaten ZOOM ile pisirildi; kart dar ekranda fit ile kuculur
		w.SetPosition(self._P(parent, x), self._P(parent, y))
		w.Show()
		self.keep.append(w)
		return w

	def _Txt(self, parent, pt, color, align="left", outline=True, vcenter=False):
		t = ui.TextLine()
		t.SetParent(parent)
		t.AddFlag("not_pick")
		t.SetFontName(self.F(pt, self._Z(parent)))
		if outline:
			t.SetOutline()
		if align == "center":
			t.SetHorizontalAlignCenter()
		elif align == "right":
			t.SetHorizontalAlignRight()
		if vcenter:
			t.SetVerticalAlignCenter()
		t.SetPackedFontColor(color)
		t.Show()
		self.keep.append(t)
		return t

	def _Btn(self, parent, up, over, down, x, y, func):
		b = ui.Button()
		b.SetParent(parent)
		b.SetUpVisual(DIR + up)
		b.SetOverVisual(DIR + over)
		b.SetDownVisual(DIR + down)
		if hasattr(wndMgr, "SetButtonScale"):
			f = self.k * IMG_S * self._ImgF(parent)
			wndMgr.SetButtonScale(b.hWnd, f, f)
		b.SetPosition(self._P(parent, x), self._P(parent, y))
		b.SetEvent(func)
		b.Show()
		self.keep.append(b)
		return b

	def _Bar(self, parent, color):
		b = ui.Bar()
		b.SetParent(parent)
		b.AddFlag("not_pick")
		b.SetColor(color)
		b.Show()
		self.keep.append(b)
		return b

	def _Frame(self, parent, color):
		b = ui.Box()
		b.SetParent(parent)
		b.AddFlag("not_pick")
		b.SetColor(color)
		b.Show()
		self.keep.append(b)
		return b

	def _TextW(self, t):
		try:
			(w, h) = t.GetTextSize()
			return w
		except:
			return 0

	# ------------------------------------------------------------------ kart
	def __BuildCard(self):
		box = _Root(self, ZOOM_CARD * self.fit)		# kendi kok penceresi: dokunusu yutar
		box.imgf = self.fit
		box.SetSize(self.S(CARD_W), self.S(CARD_H))
		box.SetPosition(self.cardX, self.cardY)
		box.Hide()
		self.keep.append(box)
		self.box = box
		self._Img("card_bg.png", box)
		self.medal = self._Img("medal_mob.png", box, MEDAL_X, MEDAL_Y)
		self.medalKind = "mob"
		self.nameT = self._Txt(box, 17, C_WHITE)
		self.nameT.SetPosition(self.S(NAME_X), self.S(NAME_Y))
		self.pills = []
		for i in xrange(3):
			bar = self._Bar(box, 0x8c000000)
			fr = self._Frame(box, 0xff6b5a3e)
			tx = self._Txt(box, 12, C_GOLD, "center", outline=False)
			for w in (bar, fr, tx):
				w.Hide()
			self.pills.append({"bar": bar, "fr": fr, "tx": tx})
		# can cubugu
		self._Img("hp_track.png", box, HP_X, HP_Y)
		fx, fy = HP_X + HP_IN_X0, HP_Y + HP_IN_Y0
		self.hpGhost = self._Img("hp_ghost.png", box, fx, fy)
		self.hpFill = self._Img("hp_fill.png", box, fx, fy)
		self.hpEdge = self._Img("hp_edge.png", box, fx, fy)
		self._Img("hp_ticks.png", box, fx, fy)
		self.hpT = self._Txt(box, 12, C_WHITE, "center", vcenter=True)
		self.hpT.SetPosition(self.S(HP_X + HP_W / 2), self.S(HP_Y + HP_H / 2.0))
		self.pctT = self._Txt(box, 11, C_GOLD_TXT, "right", vcenter=True)
		self.pctT.SetPosition(self.S(HP_X + HP_IN_X0 + HP_IN_W - 5), self.S(HP_Y + HP_H / 2.0))
		self.dropsBtn = self._Btn(box, "btn_drops_up.png", "btn_drops_over.png", "btn_drops_down.png", BTN_DROPS_X, BTN_DROPS_Y, ui.__mem_func__(self.__OnDrops))
		self._Btn(box, "btn_close_up.png", "btn_close_over.png", "btn_close_down.png", BTN_CLOSE_X, BTN_CLOSE_Y, ui.__mem_func__(self.__OnClose))

	def __SetMedal(self, kind):
		if kind == self.medalKind:
			return
		self.medalKind = kind
		try:
			self.medal.LoadImage(DIR + "medal_%s.png" % kind)
			self.medal.SetScale(self.k * IMG_S * self.fit, self.k * IMG_S * self.fit)
		except:
			pass

	def __SetInfo(self, vid):
		b = self.board
		race = 0
		try:
			race = int(getattr(b, "vnum", 0) or 0)
		except:
			race = 0
		if race <= 0:
			try:
				race = nonplayer.GetRaceNumByVID(vid)
			except:
				race = 0
		self.race = race
		name = ""
		try:
			name = chr.GetNameByVID(vid)
		except:
			name = ""
		level = -1
		try:
			level = nonplayer.GetLevelByVID(vid)
		except:
			level = -1
		grade = -1
		try:
			grade = nonplayer.GetGradeByVID(vid)
		except:
			grade = -1
		stone = False
		try:
			stone = race > 0 and bool(nonplayer.IsMonsterStone(race))
		except:
			stone = False
		(gkey, glabel) = _Grade(grade)
		self.level = level
		self.gradeLabel = glabel
		self.isStone = stone
		boss = gkey in ("BOSS", "KING")
		self.__SetMedal(stone and "stone" or (boss and "boss" or "mob"))
		pills = []
		if level >= 0:
			pills.append(("Sv. %d" % level, "gold"))
		if stone:
			pills.append(("Metin ta\xfe\xfd", "dark"))
		elif not boss:
			pills.append(("Canavar", "dark"))
		if boss:
			pills.append((glabel, "king"))
		self.nameT.SetText(name or "")
		self.__PlacePills(pills)

	def __PlacePills(self, pills):
		limit = HP_X + HP_W		# ad + haplar can cubugunun sagini gecmesin
		kc = max(self.k * ZOOM_CARD * self.fit, 0.01)
		nw = self._TextW(self.nameT) / kc
		# sigmayan hap once dusurulur (tur hapi), sonra ad kisaltilir
		def width(ps):
			tot = 0
			for (txt, style) in ps:
				tot += 8 + self.__PillW(txt)
			return tot
		while pills and NAME_X + nw + width(pills) > limit and len(pills) > 1:
			drop = [i for i in xrange(len(pills)) if pills[i][1] == "dark"]
			if drop:
				pills.pop(drop[0])
			else:
				pills.pop(len(pills) - 1)
		if NAME_X + nw + width(pills) > limit:
			full = self.nameT.GetText()
			while full and NAME_X + nw + width(pills) > limit:
				full = full[:-1]
				self.nameT.SetText(full.rstrip() + "..")
				nw = self._TextW(self.nameT) / kc
		x = NAME_X + nw + 8
		for i in xrange(3):
			p = self.pills[i]
			if i >= len(pills):
				for w in (p["bar"], p["fr"], p["tx"]):
					w.Hide()
				continue
			(txt, style) = pills[i]
			(bg, border, fg) = PILLS[style]
			pw = self.__PillW(txt)
			p["tx"].SetText(txt)
			p["tx"].SetPackedFontColor(fg)
			p["bar"].SetColor(bg)
			p["fr"].SetColor(border)
			p["bar"].SetPosition(self.S(x), self.S(NAME_Y + 2))
			p["bar"].SetSize(self.S(pw), self.S(18))
			p["fr"].SetPosition(self.S(x), self.S(NAME_Y + 2))
			p["fr"].SetSize(self.S(pw), self.S(18))
			p["tx"].SetPosition(self.S(x + pw / 2.0), self.S(NAME_Y + 3))
			for w in (p["bar"], p["fr"], p["tx"]):
				w.Show()
			x += pw + 8

	def __PillW(self, txt):
		t = self.pills[0]["tx"]
		old = t.GetText()
		t.SetText(txt)
		w = self._TextW(t) / max(self.k * ZOOM_CARD * self.fit, 0.01)
		t.SetText(old)
		return int(w) + 14

	# ------------------------------------------------------------------ can
	def SetHP(self, pct, cur, mx):
		try:
			pct = max(0, min(100, int(pct)))
		except:
			return
		now = app.GetTime()
		if pct < self.hpTarget and self.state != "kapali":
			# iz: onceki gorunen yerden bekleyip kapanir
			if self.ghost < self.hpShown:
				self.ghost = self.hpShown
			self.ghostFrom = max(self.ghost, self.hpShown)
			self.ghost = self.ghostFrom
			self.ghostT0 = now + GHOST_WAIT
		self.hpFrom = self.hpShown
		self.hpTarget = float(pct)
		self.hpT0 = now
		if self.state == "kapali":
			self.hpShown = self.hpFrom = self.ghost = self.ghostFrom = float(pct)
		try:
			if mx and int(mx) > 0:
				self.hpT.SetText("%s / %s" % (_Dotted(cur), _Dotted(mx)))
			else:
				self.hpT.SetText("")
		except:
			self.hpT.SetText("")
		self.pctT.SetText("%%%d" % pct)
		self.__DrawHP()

	def __DrawHP(self):
		fw = HP_IN_W * self.hpShown / 100.0
		gw = HP_IN_W * max(self.ghost, self.hpShown) / 100.0
		sx = self.k * IMG_S * self.fit
		# hp_fill/hp_ghost 4 px genisliginde tek renkli sutun: yatayda istenen genislige gerilir
		kc = self.k * ZOOM_CARD * self.fit
		if fw >= 0.5:
			self.hpFill.SetScale(kc * fw / 4.0, sx)
			self.hpFill.Show()
			self.hpEdge.SetPosition(self.S(HP_X + HP_IN_X0 + fw) - 1, self.S(HP_Y + HP_IN_Y0))
			self.hpEdge.Show()
		else:
			self.hpFill.Hide()
			self.hpEdge.Hide()
		if gw - fw >= 0.5:
			self.hpGhost.SetScale(kc * gw / 4.0, sx)
			self.hpGhost.Show()
		else:
			self.hpGhost.Hide()

	# ------------------------------------------------------------------ ac / kapa
	def IsOpen(self):
		return self.box.IsShow()

	def Suppressed(self):
		"""KULLANICI (2026-10-01): Oto Av penceresi acikken kart pencerenin ustune biniyordu (oto av surekli yeni
		hedef secer) -> Oto Av acikken kart gosterilmez; kapaninca bir sonraki hedef paketinde geri gelir."""
		try:
			w = constInfo.wndAuto
			return bool(w) and w.IsShow()
		except:
			return False

	def Open(self):
		b = self.board
		if not b or not b.vid:
			return
		if self.Suppressed():
			self.CloseNow()
			return
		if not self.box.IsShow() and self.__Layout():		# HUD duzeni/ekran degistiyse yeniden kur
			self.CloseDrops()
			self.__Rebuild()
			self.vid = 0
		vid = b.vid
		newTarget = (vid != self.vid)
		wasClosed = not self.box.IsShow()
		if newTarget:
			self.CloseDrops()
		if newTarget or wasClosed:
			self.vid = vid
			self.__SetInfo(vid)
		try:
			(pct, cur, mx) = b.mobileEnemy
		except:
			(pct, cur, mx) = (-1, 0, 0)
		if wasClosed:
			self.state = "aciliyor"
			self.animT0 = app.GetTime()
			self.box.SetPosition(self.cardX, self.cardY - self.S(14))
			self.box.Show()
			self.box.SetTop()
		if pct is not None and pct >= 0:
			if newTarget or wasClosed:
				# yeni hedef: can cubugu kaymadan dogrudan yerine oturur (iz yok)
				v = float(max(0, min(100, pct)))
				self.hpShown = self.hpTarget = self.hpFrom = self.ghost = self.ghostFrom = v
			self.SetHP(pct, cur, mx)

	def Close(self):
		self.CloseNow()

	def CloseNow(self):
		self.state = "kapali"
		self.box.Hide()
		self.CloseDrops()
		self.vid = 0

	def __OnClose(self):
		try:
			player.ClearTarget()
		except:
			pass
		b = self.board
		if b:
			try:
				b.Close()
				return
			except:
				pass
		self.CloseNow()

	def OnOutsideTap(self):
		if self.IsOpen() and self.board:
			self.board.OnOutsideTap()

	def OnOutsideTapUI(self):
		pass

	# ------------------------------------------------------------------ dusenler penceresi
	def __BuildDrops(self):
		d = _Root(self, ZOOM_DROPS)
		dw, dh = self.D(DROPS_W), self.D(DROPS_H)
		d.SetSize(dw, dh)
		dy = self.cardY + self.S(CARD_H) + self.D(DROPS_GAP)		# kart S (fit) ile olceklenir
		dy = max(0, min(dy, self.scrH - dh - 2))
		d.SetPosition((self.scrW - dw) // 2, dy)
		d.Hide()
		self.keep.append(d)
		self.dbox = d
		self.__DropsZemin(d)		# DOSEME (KULLANICI 2026-10-01; eski drops_bg.png ~5.5 MB yerine)
		# "Dusen Esyalar" basligi drops_bg.png'de (kalin, keskin); hedefin adi + seviyesi basligin SAGINDA
		self.titleSubT = self._Txt(d, 12, C_TITLE_SUB, "right", vcenter=True)
		self.titleSubT.SetPosition(self.D(DCLOSE_X - 12), self.D(TITLE_Y + TITLE_H / 2.0 - 1))
		self._Btn(d, "dclose_up.png", "dclose_over.png", "dclose_down.png", DCLOSE_X, DCLOSE_Y, ui.__mem_func__(self.CloseDrops))
		# bilgi degerleri
		self.statT = []
		for i in xrange(4):
			t = self._Txt(d, 14, C_CREAM)
			t.SetPosition(self.D(STAT_X + i * (STAT_W + STAT_GAP) + 10), self.D(STAT_Y + 21))
			self.statT.append(t)
		# sekmeler
		self.tabs = []
		for i in xrange(MAX_TABS):
			x = TAB_X + i * (TAB_W + TAB_GAP)
			b = self._Btn(d, "tab_up.png", "tab_over.png", "tab_on.png", x, TAB_Y, lambda i0=i: self.__OnTab(i0))
			dot = self._Bar(d, C_OFF)
			lbl = self._Txt(d, 13, C_CREAM, vcenter=True)
			for w in (b, dot, lbl):
				w.Hide()
			self.tabs.append({"btn": b, "dot": dot, "lbl": lbl, "cat": None, "on": None, "x": x})
		# yuvalar
		self.cells = []
		for i in xrange(PAGE):
			c = i % GRID_COLS
			r = i // GRID_COLS
			x = GRID_X + c * (SLOT + SLOT_GAP)
			y = GRID_Y + r * (SLOT + SLOT_GAP)
			ic = ui.ExpandedImageBox()
			ic.SetParent(d)
			ic.AddFlag("not_pick")
			ic.Hide()
			self.keep.append(ic)
			line = self._Bar(d, C_OFF)
			line.SetPosition(self.D(x + 12), self.D(y + 3))
			line.SetSize(self.D(SLOT - 24), max(1, self.D(2)))
			badgeBar = self._Bar(d, C_GOLD)
			badgeT = self._Txt(d, 11, C_DARK, outline=False)
			cntT = self._Txt(d, 12, C_WHITE, "right")
			cntT.SetPosition(self.D(x + SLOT - 5), self.D(y + SLOT - 18))
			rngT = self._Txt(d, 11, C_STONE_TXT, "center")
			rngT.SetPosition(self.D(x + SLOT / 2.0), self.D(y + SLOT - 17))
			hit = _Hit()
			hit.SetParent(d)
			hit.SetPosition(self.D(x), self.D(y))
			hit.SetSize(self.D(SLOT), self.D(SLOT))
			hit.onUp = lambda i0=i: self.__OnSlot(i0)
			self.keep.append(hit)
			for w in (line, badgeBar, badgeT, cntT, rngT, hit):
				w.Hide()
			self.cells.append({"x": x, "y": y, "h": 1, "ic": ic, "file": "", "line": line, "badgeBar": badgeBar, "badgeT": badgeT,
				"cntT": cntT, "rngT": rngT, "hit": hit, "e": None})
		self.selImg = self._Img("slot_sel.png", d)
		self.selImg.Hide()
		self.msgT = self._Txt(d, 14, C_SUB, "center", vcenter=True)
		self.msgT.SetPosition(self.D(PANEL[0] + PANEL[2] / 2.0), self.D(PANEL[1] + PANEL[3] / 2.0))
		self.msgT.Hide()
		# ayrinti seridi
		dic = ui.ExpandedImageBox()
		dic.SetParent(d)
		dic.AddFlag("not_pick")
		dic.Hide()
		self.keep.append(dic)
		self.detIc = dic
		self.detFile = ""
		self.detNameT = self._Txt(d, 15, C_CREAM)
		self.detNameT.SetPosition(self.D(DETAIL_X + 68), self.D(DETAIL_Y + 11))
		self.detDot = self._Bar(d, C_OFF)
		self.detDot.SetPosition(self.D(DETAIL_X + 68), self.D(DETAIL_Y + 38))
		self.detDot.SetSize(self.D(7), self.D(7))
		self.detSubT = self._Txt(d, 11, C_SUB)
		self.detSubT.SetPosition(self.D(DETAIL_X + 80), self.D(DETAIL_Y + 33))
		self.countT = self._Txt(d, 12, C_OFF, "right", vcenter=True)
		self.countT.SetPosition(self.D(DETAIL_X + DETAIL_W - 12), self.D(DETAIL_Y + DETAIL_H / 2.0))
		self.pgL = self._Btn(d, "pg_l_up.png", "pg_l_up.png", "pg_l_down.png", PG_L_X, PG_Y, ui.__mem_func__(self.__OnPrev))
		self.pgR = self._Btn(d, "pg_r_up.png", "pg_r_up.png", "pg_r_down.png", PG_R_X, PG_Y, ui.__mem_func__(self.__OnNext))
		self.pageT = self._Txt(d, 12, C_CREAM, "center", vcenter=True)
		self.pageT.SetPosition(self.D((PG_L_X + 24 + PG_R_X) / 2.0), self.D(PG_Y + 12))
		for w in (self.pgL, self.pgR, self.pageT):
			w.Hide()

	def IsDropsOpen(self):
		return self.dbox.IsShow()

	def __OnDrops(self):
		if self.dbox.IsShow():
			self.CloseDrops()
			return
		if self.race <= 0:
			return
		try:
			net.SendTargetInfoLoad(player.GetTargetVID())
		except:
			pass
		self.filter = "all"
		self.page = 0
		self.sel = None
		self.dropsAsked = app.GetTime()
		self.dropsAnswered = False
		self.__FillStats()
		self.dbox.Show()
		self.dbox.SetTop()
		self.RefreshDrops()

	def CloseDrops(self):
		try:
			self.dbox.Hide()
		except:
			pass

	def __FillStats(self):
		race = self.race
		name = self.nameT.GetText() if hasattr(self.nameT, "GetText") else ""
		lvText = (self.level >= 0) and ("Sv. %d" % self.level) or ""
		self.titleSubT.SetText(lvText and ("%s \xb7 %s" % (name, lvText)) or name)
		mhp = 0
		try:
			mhp = nonplayer.GetMonsterMaxHP(race)
		except:
			mhp = 0
		lv = self.level
		if lv < 0:
			try:
				lv = nonplayer.GetMonsterLevel(race)
			except:
				lv = -1
		irk = self.__RaceText(race)
		vals = (mhp > 0 and _Dotted(mhp) or "-", lv >= 0 and str(lv) or "-", self.gradeLabel or "-", irk or "-")
		for i in xrange(4):
			t = self.statT[i]
			v = vals[i]
			t.SetText(v)
			while len(v) > 3 and self._TextW(t) > self.D(STAT_W - 18):
				v = v[:-1]
				t.SetText(v.rstrip() + "..")

	def __RaceText(self, race):
		names = []
		try:
			flag = nonplayer.GetMonsterRaceFlag(race)
			table = self.board.InfoBoard.RACE_FLAG_TO_NAME
			for i in xrange(17):
				f = 1 << i
				if (flag & f) and table.has_key(f):
					names.append(table[f])
		except:
			pass
		if self.isStone:
			try:
				names.append(localeInfo.TARGET_INFO_RACE_METIN)
			except:
				names.append("Metin")
		return ", ".join(names)

	def RefreshDrops(self):
		if not self.dbox.IsShow():
			return
		self.__LoadEntries()
		# yenilenen listede secim ayni esyaya (degerce) tasinir; yoksa birakilir
		if self.sel is not None:
			old = self.sel
			self.sel = None
			for e in (self.entries or []):
				if e["vnums"] == old["vnums"] and e["count"] == old["count"]:
					self.sel = e
					break
		self.__Render()

	def __LoadEntries(self):
		"""KULLANICI (2026-10-01): esya dusurmeyen canavarda (Ac Yabani Kopek) "Yukleniyor..." takiliyordu: sunucu bos
		liste gonderince game.BINARY_AddTargetMonsterDropInfo hic cagrilmaz, MONSTER_INFO_DATA'da kayit olusmaz.
		Sunucu yaniti (RefreshMonsterInfoBoard) geldiyse ya da 2.5 sn gectiyse kayit yok = esya yok."""
		e = _Entries(self.race)
		if e is None and (self.dropsAnswered or app.GetTime() - self.dropsAsked > DROPS_WAIT):
			e = []
		self.entries = e

	def OnDropsAnswer(self):
		"""TargetBoard.RefreshMonsterInfoBoard -> sunucunun dusen esya yaniti geldi"""
		self.dropsAnswered = True
		self.RefreshDrops()

	def __Filtered(self):
		if not self.entries:
			return []
		if self.filter == "all":
			return self.entries
		return [e for e in self.entries if e["cat"] == self.filter]

	def __Render(self):
		entries = self.entries
		# sekmeler
		cats = []
		if entries:
			counts = {}
			for e in entries:
				counts[e["cat"]] = counts.get(e["cat"], 0) + 1
			cats.append(("all", "T\xfcm\xfc", len(entries), None))
			for (key, label, color) in CATS:
				if counts.get(key):
					cats.append((key, label, counts[key], color))
			if self.filter != "all" and not counts.get(self.filter):
				self.filter = "all"
		for i in xrange(MAX_TABS):
			t = self.tabs[i]
			if i >= len(cats):
				for w in (t["btn"], t["dot"], t["lbl"]):
					w.Hide()
				t["cat"] = None
				continue
			(key, label, n, color) = cats[i]
			t["cat"] = key
			on = (key == self.filter)
			if t["on"] != on:
				t["on"] = on
				up = on and "tab_on.png" or "tab_up.png"
				t["btn"].SetUpVisual(DIR + up)
				t["btn"].SetOverVisual(DIR + (on and "tab_on.png" or "tab_over.png"))
				t["btn"].SetDownVisual(DIR + "tab_on.png")
			t["lbl"].SetText("%s %d" % (label, n))
			t["lbl"].SetPackedFontColor(on and C_WHITE or C_CREAM)
			lw = self._TextW(t["lbl"])
			dw = color and self.D(7) + self.D(5) or 0
			x0 = self.D(t["x"] + TAB_W / 2.0) - (dw + lw) // 2
			if color:
				t["dot"].SetColor(color)
				t["dot"].SetPosition(x0, self.D(TAB_Y + TAB_H / 2.0) - self.D(3.5))
				t["dot"].SetSize(self.D(7), self.D(7))
				t["dot"].Show()
			else:
				t["dot"].Hide()
			t["lbl"].SetPosition(x0 + dw, self.D(TAB_Y + TAB_H / 2.0))
			t["btn"].Show()
			t["lbl"].Show()
		# izgara
		lst = self.__Filtered()
		yer = _Yerlestir(lst)
		pages = max(1, len(yer))
		self.page = max(0, min(self.page, pages - 1))
		sayfa = yer and yer[self.page] or []
		if entries is None:
			self.msgT.SetText("Y\xfckleniyor...")
			self.msgT.Show()
		elif not entries:
			self.msgT.SetText(getattr(localeInfo, "TARGET_INFO_NO_ITEM_TEXT", "") or "Bu hedef e\xfeya d\xfc\xfe\xfcrm\xfcyor.")
			self.msgT.Show()
		else:
			self.msgT.Hide()
		selShown = False
		for i in xrange(PAGE):
			c = self.cells[i]
			if i >= len(sayfa):
				self.__HideCell(c)
				continue
			(e, col, row, h) = sayfa[i]
			c["e"] = e
			c["x"] = GRID_X + col * (SLOT + SLOT_GAP)
			c["y"] = GRID_Y + row * (SLOT + SLOT_GAP)
			c["h"] = h
			self.__DrawCell(c, e)
			if self.sel is e:
				self.__SetSel(h)
				self.selImg.SetPosition(self.D(c["x"] - 3), self.D(c["y"] - 3))
				self.selImg.Show()
				selShown = True
		if not selShown:
			self.selImg.Hide()
		# sayfa / sayi
		if pages > 1:
			self.pageT.SetText("%d/%d" % (self.page + 1, pages))
			for w in (self.pgL, self.pgR, self.pageT):
				w.Show()
			self.countT.Hide()
		else:
			for w in (self.pgL, self.pgR, self.pageT):
				w.Hide()
			if entries:
				self.countT.SetText("%d \xe7e\xfeit e\xfeya d\xfc\xfeebilir" % len(entries))
				self.countT.Show()
			else:
				self.countT.Hide()
		self.__DrawDetail()

	def __SetSel(self, h):
		"""secim cercevesi esyanin boyunda (slot_sel / slot_sel2 / slot_sel3)"""
		if getattr(self, "selH", 1) == h:
			return
		self.selH = h
		self.selImg.LoadImage(DIR + (h > 1 and ("slot_sel%d.png" % h) or "slot_sel.png"))
		f = self.k * IMG_S * self._ImgF(self.dbox)
		self.selImg.SetScale(f, f)

	def __Span(self, h):
		"""h yuvalik esyanin tasarim yuksekligi"""
		return SLOT * h + SLOT_GAP * (h - 1)

	def __HideCell(self, c):
		c["e"] = None
		for w in (c["ic"], c["line"], c["badgeBar"], c["badgeT"], c["cntT"], c["rngT"], c["hit"]):
			w.Hide()

	def __ShowVnum(self, e):
		v = e["vnums"]
		if e["cat"] == "stone" and len(v) > 1:
			return v[self.cycle % len(v)]
		return v[-1]

	def __LoadIcon(self, img, vnum, box, cx, cy, key):
		"""ikonu kutuya (box x box tasarim px) sigdirip ortalar; basarisiz yuklemede gizler"""
		fname = ""
		try:
			item.SelectItem(vnum)
			fname = item.GetIconImageFileName()
			(sw, sh) = item.GetItemSize()
		except:
			(sw, sh) = (1, 1)
		if not fname:
			img.Hide()
			return ""
		if fname != key:
			try:
				img.LoadImage(fname)
				max(0, 0)		# Py_BuildException bekleyen hatasi try icinde tetiklensin
			except:
				img.Hide()
				return ""
		# KULLANICI (2026-10-04): "tiklayinca buyuyup kuculuyorlar" -> GetWidth'e GUVENILMEZ (ilk yuklemede doku pikseli,
		# SetScale'den sonra OLCEKLI boy doner; her yeniden cizimde olcek degisiyordu). Mantiksal ikon = 32 x yuva sayisi.
		iw = 32.0 * max(1, sw)
		ih = 32.0 * max(1, sh)
		s = min(box[0] / float(iw), box[1] / float(ih))
		img.SetScale(self.k * ZOOM_DROPS * s, self.k * ZOOM_DROPS * s)
		img.SetPosition(self.D(cx - iw * s / 2.0), self.D(cy - ih * s / 2.0))
		img.Show()
		return fname

	def __DrawCell(self, c, e):
		x, y = c["x"], c["y"]
		hh = self.__Span(c.get("h", 1))
		c["file"] = self.__LoadIcon(c["ic"], self.__ShowVnum(e), (42, hh - 8), x + SLOT / 2.0, y + hh / 2.0, c["file"])
		c["line"].SetPosition(self.D(x + 12), self.D(y + 3))
		c["cntT"].SetPosition(self.D(x + SLOT - 5), self.D(y + hh - 18))
		c["rngT"].SetPosition(self.D(x + SLOT / 2.0), self.D(y + hh - 17))
		c["hit"].SetPosition(self.D(x), self.D(y))
		c["hit"].SetSize(self.D(SLOT), self.D(hh))
		c["line"].SetColor(CAT_COLOR.get(e["cat"], C_OFF))
		c["line"].Show()
		if e["badge"]:
			c["badgeT"].SetText(e["badge"])
			bw = self._TextW(c["badgeT"]) + self.D(6)
			c["badgeBar"].SetPosition(self.D(x + 4), self.D(y + 5))
			c["badgeBar"].SetSize(bw, self.D(14))
			c["badgeT"].SetPosition(self.D(x + 4) + self.D(3), self.D(y + 5))
			c["badgeBar"].Show()
			c["badgeT"].Show()
		else:
			c["badgeBar"].Hide()
			c["badgeT"].Hide()
		if e["count"] > 1:
			c["cntT"].SetText(str(e["count"]))
			c["cntT"].Show()
		else:
			c["cntT"].Hide()
		if e["rng"]:
			c["rngT"].SetText(e["rng"])
			c["rngT"].Show()
		else:
			c["rngT"].Hide()
		c["hit"].Show()

	def __DrawDetail(self):
		e = self.sel
		if e is None or not self.entries or not [x for x in self.entries if x is e]:
			self.sel = None
			self.detIc.Hide()
			self.detFile = ""
			self.detNameT.SetText(self.entries and "Bir e\xfeyaya dokunun" or "")
			self.detSubT.SetText(self.entries and "Ad\xfd ve t\xfcr\xfc burada g\xf6r\xfcn\xfcr." or "")
			self.detDot.Hide()
			return
		self.detFile = self.__LoadIcon(self.detIc, self.__ShowVnum(e), (44, 48), DETAIL_X + 30, DETAIL_Y + 30, self.detFile)
		name = e["name"]
		if e["count"] > 1:
			name = "%s  x%d" % (name, e["count"])
		self.detNameT.SetText(name)
		sub = CAT_NAME.get(e["cat"], "")
		if e["extra"]:
			sub = "%s \xb7 %s" % (sub, e["extra"])
		self.detSubT.SetText(sub)
		self.detDot.SetColor(CAT_COLOR.get(e["cat"], C_OFF))
		self.detDot.Show()

	def __OnSlot(self, i):
		try:
			e = self.cells[i]["e"]
		except:
			return
		if e is None:
			return
		self.sel = e
		self.__Render()

	def __OnTab(self, i):
		try:
			key = self.tabs[i]["cat"]
		except:
			return
		if not key or key == self.filter:
			return
		self.filter = key
		self.page = 0
		self.__Render()

	def __OnPrev(self):
		if self.page > 0:
			self.page -= 1
			self.__Render()

	def __OnNext(self):
		self.page += 1
		self.__Render()

	# ------------------------------------------------------------------ kare
	def OnUpdate(self):
		if not self.box.IsShow():
			return
		if self.Suppressed():
			self.CloseNow()
			return
		now = app.GetTime()
		if self.state == "aciliyor":
			p = (now - self.animT0) / OPEN_SEC
			if p >= 1.0:
				p = 1.0
				self.state = "acik"
			dy = int(round(self.S(14) * (1.0 - _Ease(p))))
			self.box.SetPosition(self.cardX, self.cardY - dy)
		dirty = False
		if self.hpShown != self.hpTarget:
			p = (now - self.hpT0) / FILL_SEC
			if p >= 1.0:
				self.hpShown = self.hpTarget
			else:
				self.hpShown = self.hpFrom + (self.hpTarget - self.hpFrom) * _Ease(max(0.0, p))
			dirty = True
		if self.ghost > self.hpShown:
			if now >= self.ghostT0:
				p = (now - self.ghostT0) / GHOST_SEC
				if p >= 1.0:
					self.ghost = self.hpShown
				else:
					self.ghost = self.ghostFrom + (self.hpShown - self.ghostFrom) * _Ease(p)
			dirty = True
		elif self.ghost < self.hpShown:
			self.ghost = self.hpShown
		if dirty:
			self.__DrawHP()
		if self.dbox.IsShow() and self.entries is None and now - self.dropsAsked > DROPS_WAIT:
			self.RefreshDrops()
		if self.dbox.IsShow() and now >= self.nextCycle:
			self.nextCycle = now + STONE_CYCLE
			self.cycle += 1
			self.__CycleStones()

	def __CycleStones(self):
		for c in self.cells:
			e = c["e"]
			if e and e["cat"] == "stone" and len(e["vnums"]) > 1:
				x, y = c["x"], c["y"]
				hh = self.__Span(c.get("h", 1))
				c["file"] = self.__LoadIcon(c["ic"], self.__ShowVnum(e), (42, hh - 8), x + SLOT / 2.0, y + hh / 2.0, c["file"])
		e = self.sel
		if e and e["cat"] == "stone" and len(e["vnums"]) > 1:
			self.detFile = self.__LoadIcon(self.detIc, self.__ShowVnum(e), (44, 48), DETAIL_X + 30, DETAIL_Y + 30, self.detFile)
