# -*- coding: latin-1 -*-
# MOBIL - mobile_root/uicharacter.py: KARAKTER PENCERESI (yeniden tasarim, 2026-10-09).
# URETILIR: tools/karakter/uicharacter_kaynak.py (UTF-8) -> gen_uicharacter.py (Turkce harfler cp1254 kacis).
#
# KULLANICI: "karakter ekrani penceresini bizim tasarim stilimizle yeniden yapalim, yetenekler duygular gorevler dahil"
#   + "ayrintilar kismi da dahil" + "skill butonlarini ayarla yeri olsun" + "duygular da eklensin" + "derece (rutbe) gorunsun"
#   -> prototip Desktop/Averos2-KarakterPenceresi-Prototip (onaylandi: "oldu oyuna uygula, fps/boyut/donma yapmasin").
# Eski pack penceresi (uiscript/characterwindow.py + uicharacterdetails + uibeceriduzen) KULLANILMAZ; yedek
# tools/karakter/yedek_20261009/. Disari acik arayuz eskisiyle AYNI (interfacemodule / game.py cagirir):
#   CharacterWindow(), Show/Hide/Close/Destroy/IsShow/SetTop, SetState("STATUS"|"SKILL"|"EMOTICON"|"QUEST"), GetState,
#   RefreshStatus/RefreshAlignment/RefreshSkill/RefreshCharacter/RefreshQuest, OnUseSkill/OnActivateSkill/
#   OnDeactivateSkill, SetSkillToolTip, OverOutItem, ActEmotion.
#
# HIZ: pencere ILK acilista kurulur, her sekme ILK ziyarette (tembel); kapaliyken OnUpdate calismaz. RefreshStatus
# (HP yenilenmesinde bile gelir) yalniz "kirli" isaretler; gorunurken en fazla saniyede 4 yenileme. Uzun listeler
# (Ayrintilar 67 satir, gorevler, tusa konabilecekler) SABIT HAVUZ: yalniz gorunen satirlar kadar pencere.
# Kok SetUIScale(1.0) -> motorun kok olcek taramasi (GetContentExtent) bu pencerede YOK.
# Zemin pack parcalarindan DOSENIR (Board / TitleBar / ThinBoard), kucuk dokular mobile/ui/krk (bake_karakter.py).
import ui
import wndMgr
import app
import net
import player
import skill
import quest
import chr
import localeInfo
import playerSettingModule
import emotion
import item
import constInfo
import uikarakterveri

DIR = "mobile/ui/krk/"
PAT = "d:/ymir work/ui/pattern/"
MU = "mobile/ui/"
B = uikarakterveri.B
BOYUT = uikarakterveri.BOYUT
WIN_W = 1140.0
WIN_H = 634.0
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")
TASMA = 0.02
YENILE_SN = 0.25

C_KREM = 0xfff1e6c0
C_ALTIN = 0xffe8d08a
C_ALT = 0xffdccdab
C_SARI = 0xfff2c94c
C_KENAR = 0xff6b5a3e
C_CIZGI = 0xff3d342a
C_YESIL = 0xff8fd16a
C_TURUNCU = 0xfff0a24a
C_KIRMIZI = 0xffe0705a
C_SOLUK = 0xffb3a78f
C_BEYAZ = 0xffffffff
F_KART = 0xff18120c
F_NAV = 0xff1a140e
F_SEC = 0xff3a2d17
F_YUVA = 0xff0a0806
K_YUVA = 0xff4a3e2c
F_PARLA = 0x38f2c94c
DERECE_RENK = {"n": C_KREM, "m": 0xff9fd0ff, "g": C_TURUNCU, "p": 0xffff8fd0, "yok": C_SOLUK}


def _En():
	try:
		import dil
		return dil.Mevcut() == "en"
	except:
		return False


_EN = [None]


def _Y(tr, en):
	if _EN[0] is None:
		_EN[0] = _En()
	return en if _EN[0] else tr


def _Sayi(n):
	try:
		n = int(n)
	except:
		return str(n)
	s = str(abs(n))
	g = []
	while len(s) > 3:
		g.insert(0, s[-3:])
		s = s[:-3]
	g.insert(0, s)
	return ("-" if n < 0 else "") + _Y(".", ",").join(g)


def _Yuzde(v):
	return _Y("%%%d" % v, "%d%%" % v)


def _PT(pt):
	"""TELEFON: tasarim yazisi +2 pt (en az 14 okunur). Pisirilmis yazida tavan YOK; motor TextLine'i min(18, _PT)."""
	return pt + 2


def _Sar(metin, genislik, pt, satir=3):
	"""kelime kaydirma (motor TextLine tek satir): Tahoma ortalama harf ~0.56 pt"""
	pt = _PT(pt)
	harf = max(4, int(genislik / (pt * 0.56)))
	out = []
	cur = ""
	for k in metin.split(" "):
		if cur and len(cur) + 1 + len(k) > harf:
			out.append(cur)
			cur = k
		else:
			cur = (cur + " " + k) if cur else k
	if cur:
		out.append(cur)
	if len(out) > satir:
		out = out[:satir]
		out[-1] = out[-1][:max(1, harf - 2)] + ".."
	return out or [""]

# ---------------------------------------------------------------- yazi katmani (pisirilmis net yazi / TextLine yedegi)
TOPLA = None		# sahte test: [] verilirse pisirilebilir yazilar (metin, pt) buraya toplanir (bake_karakter.py listesi)


def _FNV(s):
	h = 2166136261
	for ch in s:
		h = ((h ^ ord(ch)) * 16777619) & 0xffffffff
	return h


def _PismisAd(metin, pt):
	return "y/y_%08x.png" % _FNV("%s|%d" % (metin, _PT(pt)))


GLIF = "0123456789.,"
ADV_PAD = 2		# pisirilmis serit/glif: sagda golge payi 2 fiziksel px (ilerleme = genislik - 2)


def _GlifAd(ch, pt):
	return "g/g%d_%02x.png" % (_PT(pt), ord(ch))


def _Rakamli(s):
	for ch in s:
		if "0" <= ch <= "9":
			return True
	return False


def _Bol(s):
	"""[(rakam_dizisi_mi, parca)]: rakam dizileri (0-9 . ,) glif, gerisi pisirilmis kelime parcasi"""
	out = []
	cur = ""
	tur = None
	for ch in s:
		t = ch in GLIF
		if tur is None or t == tur:
			cur += ch
		else:
			out.append((tur, cur))
			cur = ch
		tur = t
	if cur:
		out.append((tur, cur))
	return out


class _Etiket(object):
	"""TextLine yerine: SetText / SetPackedFontColor / Show / Hide / IsShow / GetText / Yer / Gen / SetTop.
	Pisirilmis kip: bir ya da birkac ExpandedImageBox (serit + rakam glifleri) yan yana; renk SetDiffuseColor."""
	def __init__(self, sahip, par, x, y, pt, renk, hiza, vc, pisir):
		self.s = sahip
		self.par = par
		self.x = x
		self.y = y
		self.pt = pt
		self._pt = pt
		self.renk = renk
		self.hiza = hiza
		self.vc = vc
		self.pisir = pisir
		self.metin = None
		self.gor = True
		self.tl = None
		self.imgs = []
		self.n = 0
		self.parca = []
		self.mod = None

	def _TL(self):
		if not self.tl:
			t = ui.TextLine()
			t.SetParent(self.par)
			t.AddFlag("not_pick")
			t.SetFontName("Tahoma:%d" % max(9, min(18, int(round(_PT(self.pt) * self.s.k)))))
			if self.hiza == "orta":
				t.SetHorizontalAlignCenter()
			elif self.hiza == "sag":
				t.SetHorizontalAlignRight()
			if self.vc:
				t.SetVerticalAlignCenter()
			t.SetOutline()
			t.SetPackedFontColor(self.renk)
			self.s.keep.append(t)
			self.tl = t
		return self.tl

	def _Parcalar(self, m):
		"""pisirilmis parca listesi ya da None (motor yazisi)"""
		if not m or self.pisir is False:
			return None
		if self.pisir is True or not _Rakamli(m):
			if TOPLA is not None:
				TOPLA.append(("y", m, self.pt))
			a = _PismisAd(m, self.pt)
			return [a] if a in BOYUT else None
		pc = []
		for (rk, s) in _Bol(m):
			if rk:
				if TOPLA is not None:
					TOPLA.append(("g", "", self.pt))
				for ch in s:
					a = _GlifAd(ch, self.pt)
					if a not in BOYUT:
						return None
					pc.append(a)
			else:
				if TOPLA is not None:
					TOPLA.append(("y", s, self.pt))
				a = _PismisAd(s, self.pt)
				if a not in BOYUT:
					return None
				pc.append(a)
		return pc

	def SetText(self, m):
		if m == self.metin:
			return
		self.metin = m
		pc = self._Parcalar(m)
		if pc:
			while len(self.imgs) < len(pc):
				img = ui.ExpandedImageBox()
				img.SetParent(self.par)
				img.AddFlag("not_pick")
				img._yol = None
				self.s.keep.append(img)
				self.imgs.append(img)
			for (i, a) in enumerate(pc):
				img = self.imgs[i]
				if img._yol != a:
					img.LoadImage(DIR + a)
					img._yol = a
			for img in self.imgs[len(pc):]:
				img.Hide()
			self.parca = pc
			self.n = len(pc)
			self.mod = "img"
			if self.tl:
				self.tl.Hide()
		else:
			self._TL().SetText(m or "")
			self.mod = "tl"
			self.n = 0
			for img in self.imgs:
				img.Hide()
		self._Renk()
		self._Yer()
		self._Gor()

	def _Gor(self):
		on = self.gor and bool(self.metin)
		if self.mod == "img":
			for img in self.imgs[:self.n]:
				if on:
					img.Show()
				else:
					img.Hide()
		elif self.tl:
			if on:
				self.tl.Show()
			else:
				self.tl.Hide()

	def Show(self):
		self.gor = True
		self._Gor()

	def Hide(self):
		self.gor = False
		if self.tl:
			self.tl.Hide()
		for img in self.imgs:
			img.Hide()

	def IsShow(self):
		return self.gor

	def GetText(self):
		return self.metin or ""

	def SetPackedFontColor(self, c):
		self.renk = c
		self._Renk()

	def _Renk(self):
		c = self.renk
		if self.mod == "img":
			if hasattr(wndMgr, "SetDiffuseColor"):
				r, g, b, a = ((c >> 16) & 255) / 255.0, ((c >> 8) & 255) / 255.0, (c & 255) / 255.0, ((c >> 24) & 255) / 255.0
				for img in self.imgs[:self.n]:
					wndMgr.SetDiffuseColor(img.hWnd, r, g, b, a)
		elif self.tl:
			self.tl.SetPackedFontColor(c)

	def Yer(self, x, y):
		self.x = x
		self.y = y
		self._Yer()

	def _Ilerle(self):
		return [(BOYUT[a][0] - ADV_PAD) / B for a in self.parca[:self.n]]

	def _Yer(self):
		k = self.s.k
		if self.mod == "img":
			adv = self._Ilerle()
			w = sum(adv)
			h = BOYUT[self.parca[0]][1] / B
			x = self.x - (w if self.hiza == "sag" else (w / 2.0 if self.hiza == "orta" else 0))
			y0 = self.y - (h / 2.0 if self.vc else 0)
			for (i, img) in enumerate(self.imgs[:self.n]):
				img.SetScale(k / B, k / B)
				img.SetPosition(*self.s._P(self.par, x, y0))
				x += adv[i]
		elif self.tl:
			self.tl.SetPosition(*self.s._P(self.par, self.x, self.y))

	def Gen(self):
		"""yazi genisligi (tasarim px). Motor GetTextSize harf basina ~1 px dar olcer (+1 px/harf telafi)."""
		if self.mod == "img":
			return sum(self._Ilerle())
		try:
			(w, h) = self._TL().GetTextSize()
			return (w + len(self.GetText())) / self.s.k
		except:
			return len(self.GetText()) * min(18, _PT(self.pt)) * 0.56

	def SetTop(self):
		if self.mod == "img":
			for img in self.imgs[:self.n]:
				img.SetTop()
		elif self.tl:
			self.tl.SetTop()


# ---------------------------------------------------------------- prototip CSS cizimi: gecisli zemin + secili parilti
## linear-gradient(ust, alt) zeminleri: duz renk anahtari -> pisirilmis dikey serit (bake_karakter.py GRAD)
GRAD_MAP = {0xff1a140e: "g_nav", 0xff3a2d17: "g_sec", 0xff18120c: "g_kart", 0xff1c150d: "g_av", 0xff15100b: "g_sat",
	0xff21190e: "g_avs", 0xff201911: "g_link", 0xff221b12: "g_link", 0xff3a2c14: "g_sv"}


class _GradBar(object):
	"""ui.Bar gibi (SetColor / SetPosition / SetSize / Show / Hide); zemin pisirilmis gecis seridi"""
	def __init__(self, sahip, par, c):
		img = ui.ExpandedImageBox()
		img.SetParent(par)
		img.AddFlag("not_pick")
		sahip.keep.append(img)
		self.img = img
		self.hWnd = img.hWnd
		self.ad = None
		self.boy = (1, 1)
		self.sz = (1, 1)
		self.SetColor(c)

	def SetColor(self, c):
		ad = c if isinstance(c, str) else GRAD_MAP.get(c, "g_kart")
		if ad == self.ad:
			return
		self.ad = ad
		self.img.LoadImage(DIR + ad + ".png")
		self.boy = BOYUT[ad + ".png"]
		self._Olcek()

	def SetSize(self, w, h):
		self.sz = (w, h)
		self._Olcek()

	def _Olcek(self):
		self.img.SetScale(self.sz[0] / float(self.boy[0]), self.sz[1] / float(self.boy[1]))

	def SetPosition(self, x, y):
		self.img.SetPosition(x, y)

	def Show(self):
		self.img.Show()

	def Hide(self):
		self.img.Hide()

	def IsShow(self):
		return self.img.IsShow()


PARILTI_A = (0x34, 0x27, 0x1c, 0x13, 0x0c, 0x06)		# inset 0 0 12px rgba(242,201,76,.22): 6 ic cizgi


class _Parilti(object):
	def __init__(self, sahip, par, x, y, w, h):
		self.s = sahip
		self.par = par
		self.k = []
		for a in PARILTI_A:
			b = ui.Box()
			b.SetParent(par)
			b.AddFlag("not_pick")
			b.SetColor((a << 24) | 0xf2c94c)
			sahip.keep.append(b)
			self.k.append(b)
		self.Yer(x, y, w, h)

	def Yer(self, x, y, w, h):
		for (i, b) in enumerate(self.k):
			self.s._BarYer(self.par, b, x + 1 + i, y + 1 + i, max(1, w - 2 - 2 * i), max(1, h - 2 - 2 * i))

	def Show(self):
		for b in self.k:
			b.Show()

	def Hide(self):
		for b in self.k:
			b.Hide()


def _Otur(D, w, tex, s, rrs, z):
	"""zindan/uizindangiris ile ayni: dosenen parca YUVARLANMIS iki kenar arasina oturur (eklem cizgisi yok)"""
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


# ---------------------------------------------------------------- beceri ikonlari (skill.GetIconName bos doner)
_BEC_IKON = {}
_JOB_DIR = {"WARRIOR": "warrior", "ASSASSIN": "assassin", "SURA": "sura", "SHAMAN": "shaman", "PASSIVE": "passive",
	"SUPPORT": "common/support", "GUILD": "common/guild", "HORSE": "common/horse"}


def _BecIkon(idx, grade):
	if not _BEC_IKON:
		_BEC_IKON[0] = None
		try:
			import pack
			data = pack.Get(app.GetLocalePath() + "/skilldesc.txt")
			for line in data.split("\n"):
				tok = line.rstrip("\r").split("\t")
				if len(tok) < 13:
					continue
				try:
					i = int(tok[0])
				except:
					continue
				job = _JOB_DIR.get(tok[1].strip().upper())
				ad = tok[12].strip()
				if job and ad:
					_BEC_IKON[i] = (job, ad)
		except:
			pass
	e = _BEC_IKON.get(idx)
	if not e:
		return ""
	base = "d:/ymir work/ui/skill/%s/%s" % e
	if e[0] in ("warrior", "assassin", "sura", "shaman"):
		return "%s_0%d.sub" % (base, min(3, max(1, int(grade) + 1)))
	## destek/at: cogu tek ikon (combo.sub); binicilik gibi kademeliler yalniz riding_01..03.sub (riding.sub YOK)
	f = base + ".sub"
	if _Var(f):
		return f
	return "%s_0%d.sub" % (base, min(3, max(1, int(grade) + 1)))


def _Var(f):
	try:
		import pack
		return bool(f) and pack.Exist(f)
	except:
		return bool(f)


# ---------------------------------------------------------------- veriler
STAT = [
	("ht", "HT", "VIT", 0xff7c2a1e, "Canl\xfdl\xfdk", "Vitality", "STAT_TOOLTIP_CON"),
	("iq", "IQ", "INT", 0xff2a4f86, "Zeka", "Intelligence", "STAT_TOOLTIP_INT"),
	("st", "ST", "STR", 0xff8a5a12, "G\xfc\xe7", "Strength", "STAT_TOOLTIP_STR"),
	("dx", "DX", "DEX", 0xff2f6b33, "\xc7eviklik", "Dexterity", "STAT_TOOLTIP_DEX"),
]
POINT_STAT_RESET_COUNT = 112

# Derece (rutbe): localeinfo.GetAlignmentTitleName esikleri, colorinfo TITLE_RGB_* renkleri, ad localeInfo.TITLE_NAME_LIST
DRC_ESIK = (12000, 8000, 4000, 1000, 0, -3999, -7999, -11999, None)
DRC_RENK = (0xff00ccff, 0xff0090ff, 0xff5c6eff, 0xff9b9bff, 0xffffffff, 0xffcf7500, 0xffeb5300, 0xffe30000, 0xffff0000)

AKAT = [
	("av", "Av Bonuslar\xfd", "Hunting Bonuses", "Av", "Hunting"),
	("can", "Canavarlara Kar\xfe\xfd", "Against Monsters", "Canavar", "Monsters"),
	("sal", "Sald\xfdr\xfd ve Savunma", "Attack & Defence", "Sald\xfdr\xfd", "Combat"),
	("ele", "Element Diren\xe7leri", "Elemental Resistances", "Element", "Elements"),
	("sin", "S\xfdn\xfdflara Kar\xfe\xfd", "Against Classes", "S\xfdn\xfdf", "Classes"),
	("sil", "Silah Savunmalar\xfd", "Weapon Defences", "Silah", "Weapons"),
	("dig", "Di\xf0er Bonuslar", "Other Bonuses", "Di\xf0er", "Other"),
	("oze", "\xd6zel Bonuslar", "Special Bonuses", "\xd6zel", "Special"),
]
AYR = [
	('av', (83, 116), "Tecr\xfcbe Bonusu", "EXP Bonus", 'DETAILS_TOOLTIP_68'),
	('av', (84, 118), "Yang D\xfc\xfe\xfcrme \xdeans\xfd", "Yang Drop Chance", 'DETAILS_TOOLTIP_69'),
	('av', (85, 117, 126), "E\xfeya D\xfc\xfe\xfcrme \xdeans\xfd", "Item Drop Chance", 'DETAILS_TOOLTIP_70'),
	('can', 53, "Canavarlara kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Monsters", 'DETAILS_TOOLTIP_5'),
	('can', 139, "Metinlere kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Metin Stones", 'DETAILS_TOOLTIP_METIN'),
	('can', 138, "Bosslara kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Bosses", 'DETAILS_TOOLTIP_BOSS'),
	('can', 43, "Yar\xfd insanlara kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Half-Humans", 'DETAILS_TOOLTIP_1'),
	('can', 45, "Orklara kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Orcs", 'DETAILS_TOOLTIP_3'),
	('can', 47, "\xd6l\xfcms\xfczlere kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Undead", 'DETAILS_TOOLTIP_4'),
	('can', 44, "Hayvanlara kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Animals", 'DETAILS_TOOLTIP_7'),
	('can', 46, "Mistiklere kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Mystics", 'DETAILS_TOOLTIP_8'),
	('can', 48, "\xdeeytanlara kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Demons", 'DETAILS_TOOLTIP_9'),
	('sal', 95, "Sald\xfdr\xfd de\xf0eri", "Attack Value", 'DETAILS_TOOLTIP_12'),
	('sal', 96, "Savunma de\xf0eri", "Defence Value", 'DETAILS_TOOLTIP_13'),
	('sal', 122, "Ortalama hasar", "Average Damage", 'DETAILS_TOOLTIP_14'),
	('sal', 140, "PvM ortalama hasar", "PvM Average Damage", 'DETAILS_TOOLTIP_PVM_HIT'),
	('sal', 124, "Ortalama hasar direnci", "Average Damage Resistance", 'DETAILS_TOOLTIP_15'),
	('sal', 121, "Beceri hasar\xfd", "Skill Damage", 'DETAILS_TOOLTIP_16'),
	('sal', 123, "Beceri hasar\xfd direnci", "Skill Damage Resistance", 'DETAILS_TOOLTIP_17'),
	('sal', 132, "B\xfcy\xfc ve yak\xfdn d\xf6v\xfc\xfe sald\xfdr\xfds\xfd", "Magic & Melee Attack", 'DETAILS_TOOLTIP_18'),
	('sal', 131, "B\xfcy\xfc sald\xfdr\xfds\xfd", "Magic Attack", 'DETAILS_TOOLTIP_19'),
	('sal', 40, "Kritik vuru\xfe \xfeans\xfd", "Critical Hit Chance", 'DETAILS_TOOLTIP_20'),
	('sal', 41, "Delici vuru\xfe \xfeans\xfd", "Piercing Hit Chance", 'DETAILS_TOOLTIP_21'),
	('sal', 136, "Kritik vuru\xfe direnci", "Critical Hit Resistance", 'DETAILS_TOOLTIP_22'),
	('sal', 137, "Delici vuru\xfe direnci", "Piercing Hit Resistance", 'DETAILS_TOOLTIP_23'),
	('ele', 77, "B\xfcy\xfcye kar\xfe\xfd diren\xe7", "Magic Resistance", 'DETAILS_TOOLTIP_76'),
	('ele', 76, "\xdeim\xfee\xf0e kar\xfe\xfd diren\xe7", "Lightning Resistance", 'DETAILS_TOOLTIP_24'),
	('ele', 133, "Buza kar\xfe\xfd diren\xe7", "Ice Resistance", 'DETAILS_TOOLTIP_25'),
	('ele', 135, "Karanl\xfd\xf0a kar\xfe\xfd diren\xe7", "Darkness Resistance", 'DETAILS_TOOLTIP_26'),
	('ele', 75, "Ate\xfee kar\xfe\xfd diren\xe7", "Fire Resistance", 'DETAILS_TOOLTIP_27'),
	('ele', 78, "R\xfczgara kar\xfe\xfd diren\xe7", "Wind Resistance", 'DETAILS_TOOLTIP_28'),
	('ele', 134, "Topra\xf0a kar\xfe\xfd diren\xe7", "Earth Resistance", 'DETAILS_TOOLTIP_29'),
	('sin', 54, "Sava\xfe\xe7\xfdlara kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Warriors", 'DETAILS_TOOLTIP_36'),
	('sin', 55, "Ninjalara kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Ninjas", 'DETAILS_TOOLTIP_37'),
	('sin', 56, "Suralara kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Suras", 'DETAILS_TOOLTIP_38'),
	('sin', 57, "\xdeamanlara kar\xfe\xfd g\xfc\xe7l\xfc", "Strong vs Shamans", 'DETAILS_TOOLTIP_39'),
	('sin', 59, "Sava\xfe\xe7\xfdlara kar\xfe\xfd savunma", "Defence vs Warriors", 'DETAILS_TOOLTIP_41'),
	('sin', 60, "Ninjalara kar\xfe\xfd savunma", "Defence vs Ninjas", 'DETAILS_TOOLTIP_42'),
	('sin', 61, "Suralara kar\xfe\xfd savunma", "Defence vs Suras", 'DETAILS_TOOLTIP_43'),
	('sin', 62, "\xdeamanlara kar\xfe\xfd savunma", "Defence vs Shamans", 'DETAILS_TOOLTIP_44'),
	('sil', 69, "K\xfdl\xfd\xe7 savunmas\xfd", "Sword Defence", 'DETAILS_TOOLTIP_46'),
	('sil', 70, "\xc7ift el savunmas\xfd", "Two-Handed Defence", 'DETAILS_TOOLTIP_47'),
	('sil', 71, "Han\xe7er savunmas\xfd", "Dagger Defence", 'DETAILS_TOOLTIP_48'),
	('sil', 72, "\xc7an savunmas\xfd", "Bell Defence", 'DETAILS_TOOLTIP_50'),
	('sil', 73, "Yelpaze savunmas\xfd", "Fan Defence", 'DETAILS_TOOLTIP_51'),
	('sil', 74, "Ok savunmas\xfd", "Arrow Defence", 'DETAILS_TOOLTIP_52'),
	('dig', 38, "Bay\xfdltma \xfeans\xfd", "Stun Chance", 'DETAILS_TOOLTIP_53'),
	('dig', 39, "Yava\xfelatma \xfeans\xfd", "Slow Chance", 'DETAILS_TOOLTIP_54'),
	('dig', 37, "Zehirleme \xfeans\xfd", "Poison Chance", 'DETAILS_TOOLTIP_55'),
	('dig', 81, "Zehre kar\xfe\xfd diren\xe7", "Poison Resistance", 'DETAILS_TOOLTIP_56'),
	('dig', 63, "HP emme", "HP Absorption", 'DETAILS_TOOLTIP_59'),
	('dig', 64, "SP emme", "SP Absorption", 'DETAILS_TOOLTIP_60'),
	('dig', 65, "SP \xe7alma \xfeans\xfd", "Mana Burn Chance", 'DETAILS_TOOLTIP_MANA_BURN'),
	('dig', 32, "HP yenilenmesi", "HP Regeneration", 'DETAILS_TOOLTIP_61'),
	('dig', 33, "SP yenilenmesi", "SP Regeneration", 'DETAILS_TOOLTIP_62'),
	('dig', 67, "Yak\xfdn sald\xfdr\xfd engelleme", "Block Melee Attacks", 'DETAILS_TOOLTIP_63'),
	('dig', 68, "Ok sald\xfdr\xfds\xfdndan s\xfdyr\xfdlma", "Dodge Arrows", 'DETAILS_TOOLTIP_64'),
	('dig', 79, "Yak\xfdn d\xf6v\xfc\xfe hasar\xfd yans\xfdtma", "Reflect Melee Damage", 'DETAILS_TOOLTIP_65'),
	('dig', 87, "\xd6ld\xfcr\xfcnce HP yenileme", "HP Restore on Kill", 'DETAILS_TOOLTIP_66'),
	('dig', 82, "\xd6ld\xfcr\xfcnce SP yenileme", "SP Restore on Kill", 'DETAILS_TOOLTIP_67'),
	('dig', 88, "Sersemlik ba\xf0\xfd\xfe\xfdkl\xfd\xf0\xfd", "Stun Immunity", 'DETAILS_TOOLTIP_IMMUNE_STUN'),
	('dig', 89, "Yava\xfelama ba\xf0\xfd\xfe\xfdkl\xfd\xf0\xfd", "Slow Immunity", 'DETAILS_TOOLTIP_IMMUNE_SLOW'),
	('oze', 93, "Sald\xfdr\xfd g\xfcc\xfc", "Attack Power", 'DETAILS_TOOLTIP_ATT_BONUS_PCT'),
	('oze', 114, "Ek sald\xfdr\xfd hasar\xfd", "Extra Attack Damage", 'DETAILS_TOOLTIP_71'),
	('oze', 115, "Savunma g\xfcc\xfc", "Defence Power", 'DETAILS_TOOLTIP_72'),
	('oze', 119, "Maks. HP art\xfd\xfe\xfd", "Max HP Bonus", 'DETAILS_TOOLTIP_MAX_HP_PCT'),
	('oze', 120, "Maks. SP art\xfd\xfe\xfd", "Max SP Bonus", 'DETAILS_TOOLTIP_MAX_SP_PCT'),
]
# Av satirlarinin kaynaklari (ayni sey tek satir TOPLAM; bilgide kaynak cipleri)
PARCA = {83: ("Efsun + Tecr\xfcbe Y\xfcz\xfc\xf0\xfc", "Bonuses + EXP Ring"), 116: ("\xddksir / market", "Potion / shop"),
	84: ("Efsun", "Bonuses"), 118: ("Market", "Shop"), 85: ("Efsun", "Bonuses"),
	117: ("Premium H\xfdrs\xfdz Eldiveni", "Premium Thief's Gloves"), 126: ("H\xfdrs\xfdz Eldiveni (tak\xfdl\xfd)", "Thief's Gloves (worn)")}
AV_IKON = {(83, 116): "icon/item/70005.tga", (84, 118): "icon/item/money.tga", (85, 117, 126): "icon/item/70043.tga"}

# duygu indeksi -> HD ikon anahtari (krk/em_<anahtar>.png)
DUYGU_ANAHTAR = [("EMOTION_CLAP", "clap"), ("EMOTION_CONGRATULATION", "congratulation"), ("EMOTION_FORGIVE", "forgive"),
	("EMOTION_ANGRY", "angry"), ("EMOTION_ATTRACTIVE", "attractive"), ("EMOTION_SAD", "sad"), ("EMOTION_SHY", "shy"),
	("EMOTION_CHEERUP", "cheerup"), ("EMOTION_BANTER", "banter"), ("EMOTION_JOY", "joy"), ("EMOTION_CHEERS_1", "cheers_1"),
	("EMOTION_CHEERS_2", "cheers_2"), ("EMOTION_DANCE_1", "dance1"), ("EMOTION_DANCE_2", "dance2"), ("EMOTION_DANCE_3", "dance3"),
	("EMOTION_DANCE_4", "dance4"), ("EMOTION_DANCE_5", "dance5"), ("EMOTION_DANCE_6", "dance6"), ("EMOTION_KISS", "kiss"),
	("EMOTION_FRENCH_KISS", "french_kiss"), ("EMOTION_SLAP", "slap")]

YUZ = {}
for (_r, _a) in (("RACE_WARRIOR_M", "warrior_m"), ("RACE_WARRIOR_W", "warrior_w"), ("RACE_ASSASSIN_M", "assassin_m"),
		("RACE_ASSASSIN_W", "assassin_w"), ("RACE_SURA_M", "sura_m"), ("RACE_SURA_W", "sura_w"), ("RACE_SHAMAN_M", "shaman_m"),
		("RACE_SHAMAN_W", "shaman_w")):
	if hasattr(playerSettingModule, _r):
		YUZ[getattr(playerSettingModule, _r)] = _a
JOB_AD = {0: "JOB_WARRIOR", 1: "JOB_ASSASSIN", 2: "JOB_SURA", 3: "JOB_SHAMAN"}
GRUP_AD = {0: "SKILL_GROUP_WARRIOR_", 1: "SKILL_GROUP_ASSASSIN_", 2: "SKILL_GROUP_SURA_", 3: "SKILL_GROUP_SHAMAN_"}
DESTEK_GOSTER = (121, 122, 123, 124, 147, 126, 127, 128, 129, 130, 131, 145, 146)

SEKME = ["kar", "ayr", "bec", "tus", "duy", "gor"]
DIS_DURUM = {"STATUS": "kar", "SKILL": "bec", "EMOTICON": "duy", "QUEST": "gor"}
IC_DURUM = {"kar": "STATUS", "ayr": "STATUS", "tus": "STATUS", "bec": "SKILL", "duy": "EMOTICON", "gor": "QUEST"}

NAV_X, NAV_Y, NAV_W, NAV_BH, NAV_GAP = 40, 72, 168, 74, 6
AYR_SATIR, AYR_H = 8, 44
GOR_SATIR, GOR_H = 5, 86
KAY_SATIR, KAY_H = 4, 56


def _Metin(sekme):
	return {
		"kar": _Y("Karakter", "Character"), "ayr": _Y("Ayr\xfdnt\xfdlar", "Details"), "bec": _Y("Yetenekler", "Skills"),
		"tus": _Y("Beceri Tu\xfelar\xfd", "Skill Buttons"), "duy": _Y("Duygular", "Emotes"), "gor": _Y("G\xf6revler", "Quests"),
	}[sekme]


class _Bas(ui.Window):
	"""dokunma alani: basis sahibine bildirilir; DOKUNMA / KAYDIRMA / SURUKLEME ayrimi sahibin OnUpdate'inde
	(parmak 12 px'ten az kayip kalkarsa dokunma). Dokunma kalkista islenir (kaydirirken yanlis secim olmaz)."""
	def __init__(self, sahip, ad, veri):
		ui.Window.__init__(self)
		self.sahip = sahip
		self.ad = ad
		self.veri = veri

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		s = self.sahip
		if s:
			s._BasBasla(self.ad, self.veri)
		return True

	def OnMouseLeftButtonUp(self):
		s = self.sahip
		if s:
			s._BasBitir()
		return True


class CharacterWindow(ui.Window):
	def __init__(self):
		ui.Window.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("CharacterWindow")
		_EN[0] = _En()		# dil giriste secilir; oyun penceresi her giriste yeniden kurulur
		self.keep = []
		self.kap = {}
		self.kurulu = False
		self.sekme = "kar"
		self.kirli = set(SEKME + ["nav"])
		self.sonTaze = 0.0
		self.gorT = 0.0
		self.tusT = 0.0
		self.bas = None
		self.toolTipSkill = None
		self.k = 1.0
		# sekme durumlari
		self.ayrKat = "hepsi"
		self.ayrYalniz = True
		self.ayrSec = 2
		self.ayrKay = 0
		self.ayrSatir = []
		self.bsek = "aktif"
		self.secBec = -1
		self.onizGrup = 1
		self.secTus = None
		self.tasinan = None
		self.degisMod = False
		self.temizT = 0.0
		self.kaynak = "bec"
		self.kayKay = 0
		self.gorKay = 0
		self.tusImza = None
		self.drcAcik = False
		self.parlakTus = None
		self.parlakT = 0.0
		self.parlaT = 0.0
		self.hayalet = None
		self.canUseHorseSkill = -1

	def __del__(self):
		ui.Window.__del__(self)

	# ============================================================ disari acik arayuz (eski pencereyle ayni)
	def Destroy(self):
		self.Hide()
		self.keep = []
		self.kap = {}
		self.kurulu = False
		self.hayalet = None

	def Show(self):
		if not self.kurulu:
			self._Kur()
		self.kirli.update(SEKME + ["nav"])
		self._SekmeAc(self.sekme)
		ui.Window.Show(self)
		self.SetTop()

	def Hide(self):
		## DIKKAT: ui.Window.__init__ RegisterWindow'dan hemen sonra Hide() cagirir - alanlar henuz yok (getattr)
		self.bas = None
		self._HayaletGizle()
		ui.Window.Hide(self)

	def Close(self):
		self.tasinan = None
		self.degisMod = False
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def SetSkillToolTip(self, toolTipSkill):
		self.toolTipSkill = toolTipSkill

	def OverOutItem(self):
		pass

	def SetState(self, stateKey):
		self.sekme = DIS_DURUM.get(stateKey, stateKey if stateKey in SEKME else "kar")
		if self.kurulu and self.IsShow():
			self._SekmeAc(self.sekme)

	def GetState(self):
		return IC_DURUM.get(self.sekme, "STATUS")

	def RefreshStatus(self):
		self.kirli.update(("kar", "ayr", "nav"))

	def RefreshAlignment(self):
		self.kirli.add("kar")

	def RefreshQuest(self):
		self.kirli.update(("gor", "nav"))

	def RefreshSkill(self):
		if self._AtDegisti():
			self.RefreshCharacter()
			return
		self.kirli.update(("bec", "tus", "nav"))

	def RefreshCharacter(self):
		## beceri yuvalari (player.SetSkill) pencere hic acilmasa da kaydedilmeli: hizli tuslar buna bakar (eskisiyle ayni)
		try:
			race = net.GetMainActorRace()
			group = net.GetMainActorSkillGroup()
			empire = net.GetMainActorEmpire()
			playerSettingModule.RegisterSkill(race, group if group else self.onizGrup, empire)
		except:
			import dbg, traceback
			dbg.TraceError("CharacterWindow.RefreshCharacter: " + traceback.format_exc())
		self.kirli.update(SEKME + ["nav"])

	def OnUseSkill(self, slotIndex, coolTime):
		pass

	def OnActivateSkill(self, slotIndex):
		pass

	def OnDeactivateSkill(self, slotIndex):
		pass

	def ActEmotion(self, emotionIndex):
		self._DuyguYap(emotionIndex)

	# ============================================================ yardimcilar (tasarim px; parent ._o = kabin tasarim konumu)
	def _P(self, par, x, y):
		ox, oy = par._o
		return (int(round((x - ox) * self.k)), int(round((y - oy) * self.k)))

	def _Kap(self, ad, x, y, w, h, par=None):
		par = par or self
		c = ui.Window()
		c.SetParent(par)
		c._o = (x, y)
		(px, py) = self._P(par, x, y)
		(qx, qy) = self._P(par, x + w, y + h)
		c.SetPosition(px, py)
		c.SetSize(max(1, qx - px), max(1, qy - py))
		c.Show()
		self.keep.append(c)
		if ad:
			self.kap[ad] = c
		return c

	def _Img(self, par, path, x, y, w, h, tex=None, goster=True):
		img = ui.ExpandedImageBox()
		img.SetParent(par)
		img.AddFlag("not_pick")
		img._par = par
		self.keep.append(img)
		self._Yukle(img, path, x, y, w, h, tex)
		if goster and path:
			img.Show()
		return img

	def _Yukle(self, img, path, x, y, w, h, tex=None):
		"""LoadImage olcegi sifirlar -> her yuklemede yeniden olcek (GetWidth'e guvenme: sabit/bilinen boy)"""
		if not path:
			img.Hide()
			img._iz = None
			return
		iz = (path, x, y, w, h)
		if getattr(img, "_iz", None) == iz:
			return
		try:
			img.LoadImage(path)
		except:
			img.Hide()
			img._iz = None
			return
		img._iz = iz
		if tex is None:
			ad = path[len(DIR):] if path.startswith(DIR) else None
			tex = BOYUT.get(ad) if ad else None
			if tex is None:
				tex = (32, 32)
		img.SetScale(w * self.k / float(tex[0]), h * self.k / float(tex[1]))
		img.SetPosition(*self._P(img._par, x, y))

	def _Bar(self, par, x, y, w, h, color, dolu=True, goster=True):
		if dolu and (isinstance(color, str) or color in GRAD_MAP):
			b = _GradBar(self, par, color)
			self._BarYer(par, b, x, y, w, h)
			if goster:
				b.Show()
			else:
				b.Hide()
			return b
		b = ui.Bar() if dolu else ui.Box()
		b.SetParent(par)
		b.AddFlag("not_pick")
		b.SetColor(color)
		self.keep.append(b)
		self._BarYer(par, b, x, y, w, h)
		if goster:
			b.Show()
		return b

	def _BarYer(self, par, b, x, y, w, h):
		(x0, y0) = self._P(par, x, y)
		(x1, y1) = self._P(par, x + w, y + h)
		b.SetPosition(x0, y0)
		b.SetSize(max(1, x1 - x0), max(1, y1 - y0))

	def _Txt(self, par, x, y, pt, color, hiza="sol", text="", vc=True, pisir=None):
		t = _Etiket(self, par, x, y, pt, color, hiza, vc, pisir)
		t.SetText(text)
		return t

	def _TxtYer(self, par, t, x, y):
		t.Yer(x, y)

	def _Gen(self, t):
		return t.Gen()

	def _Kart(self, par, x, y, w, h, dolgu=F_KART, kenar=C_CIZGI, goster=True):
		k = {"bg": self._Bar(par, x, y, w, h, dolgu, True, goster), "kn": self._Bar(par, x, y, w, h, kenar, False, goster),
			"ic": _Parilti(self, par, x, y, w, h)}
		k["ic"].Hide()
		k["kenar"] = kenar
		return k

	def _KartSec(self, k, on):
		k["kn"].SetColor(C_SARI if on else k["kenar"])
		if on:
			k["ic"].Show()
		else:
			k["ic"].Hide()

	def _KartGoster(self, k, on):
		for a in ("bg", "kn"):
			if on:
				k[a].Show()
			else:
				k[a].Hide()
		if not on:
			k["ic"].Hide()

	def _Yuva(self, par, x, y, w, h, goster=True):
		return (self._Bar(par, x, y, w, h, F_YUVA, True, goster), self._Bar(par, x, y, w, h, K_YUVA, False, goster))

	def _Hit(self, par, ad, veri, x, y, w, h):
		hb = _Bas(self, ad, veri)
		hb.SetParent(par)
		self._BarYer(par, hb, x, y, w, h)
		hb.Show()
		self.keep.append(hb)
		return hb

	def _Dugme(self, par, x, y, w, h, text, olay, boyut=None):
		"""pack middle/large_button 9 dilim (fiziksel px pisirilmis) + TextLine; ui.Button basili gorseli kendi yonetir"""
		b = ui.Button()
		b.SetParent(par)
		bw, bh = boyut or (w, h)
		ad = "btn_%dx%d" % (bw, bh)
		b.SetUpVisual(DIR + ad + "_up.png")
		b.SetOverVisual(DIR + ad + "_up.png")
		b.SetDownVisual(DIR + ad + "_down.png")
		tw, th = BOYUT[ad + "_up.png"]
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, w * self.k / float(tw), h * self.k / float(th))
		b.SetPosition(*self._P(par, x, y))
		b.SetEvent(olay)
		b.Show()
		b._o = (x, y)
		t = self._Txt(b, x + w / 2.0, y + h / 2.0 - 1, 15 if h >= 50 else 14, C_KREM, "orta", text)
		b._txt = t
		self.keep.append(b)
		return b

	def _Kare(self, par, x, y, w, h, ad, olay):
		"""statu / beceri "+" "-" dugmesi (44x44 pisirilmis)"""
		b = ui.Button()
		b.SetParent(par)
		b.SetUpVisual(DIR + ad + "_up.png")
		b.SetOverVisual(DIR + ad + "_up.png")
		b.SetDownVisual(DIR + ad + "_down.png")
		tw, th = BOYUT[ad + "_up.png"]
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, w * self.k / float(tw), h * self.k / float(th))
		b.SetPosition(*self._P(par, x, y))
		b.SetEvent(olay)
		b.Show()
		self.keep.append(b)
		return b

	def _Link(self, par, x, y, w, h, text, ad, veri=None):
		"""kucuk altin cerceveli yazi dugmesi (Tum Ayrintilar, Vazgec, Kapat)"""
		d = {"bg": self._Bar(par, x, y, w, h, 0xff201911), "kn": self._Bar(par, x, y, w, h, C_KENAR, False),
			"t": self._Txt(par, x + w / 2.0, y + h / 2.0, 13, C_ALTIN, "orta", text)}
		d["hit"] = self._Hit(par, ad, veri, x - 4, y - 6, w + 8, h + 12)
		return d

	def _LinkGoster(self, d, on):
		for a in ("bg", "kn", "t", "hit"):
			if on:
				d[a].Show()
			else:
				d[a].Hide()

	# ---- doseme (pack parcalari)
	def _Tile(self, par, path, x, y, w, h, tw, th, sx=1.0, sy=1.0):
		img = ui.ExpandedImageBox()
		img.SetParent(par)
		img.AddFlag("not_pick")
		img.LoadImage(path)
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(img.hWnd, 1)
		(x0, y0) = self._P(par, x, y)
		(x1, y1) = self._P(par, x + w, y + h)
		(zx, r) = _Otur(x1 - x0, w, tw, sx, HAS_RRS, self.k)
		(zy, b) = _Otur(y1 - y0, h, th, sy, HAS_RRS, self.k)
		img.SetScale(zx, zy)
		img.SetRenderingRect(0.0, 0.0, r, b)
		img.SetPosition(x0, y0)
		img.Show()
		self.keep.append(img)
		return img

	def _TileTam(self, par, path, x, y, w, h, t, yatay, dikey):
		img = ui.ExpandedImageBox()
		img.SetParent(par)
		img.AddFlag("not_pick")
		img.LoadImage(path)
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(img.hWnd, 0)
		(x0, y0) = self._P(par, x, y)
		(x1, y1) = self._P(par, x + w, y + h)
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
		img.SetPosition(x0, y0)
		img.Show()
		self.keep.append(img)
		return img

	def _Board(self, par, W, H):
		self._Tile(par, PAT + "board_base.tga", 32, 32, W - 64, H - 64, 128, 128)
		self._Tile(par, PAT + "board_line_top.tga", 32, 0, W - 64, 32, 128, 32)
		self._Tile(par, PAT + "board_line_bottom.tga", 32, H - 32, W - 64, 32, 128, 32)
		self._Tile(par, PAT + "board_line_left.tga", 0, 32, 32, H - 64, 32, 128)
		self._Tile(par, PAT + "board_line_right.tga", W - 32, 32, 32, H - 64, 32, 128)
		for (n, cx, cy) in (("lefttop", 0, 0), ("righttop", W - 32, 0), ("leftbottom", 0, H - 32), ("rightbottom", W - 32, H - 32)):
			self._Tile(par, PAT + "board_corner_%s.tga" % n, cx, cy, 32, 32, 32, 32)

	def _Thin(self, par, x, y, w, h):
		c = 16.0
		dolgu = self._Bar(par, x + c, y + c, w - 2 * c, h - 2 * c, 0x82000000)
		self._TileTam(par, PAT + "thinboard_line_top.tga", x + c, y, w - 2 * c, c, 16, True, False)
		self._TileTam(par, PAT + "thinboard_line_bottom.tga", x + c, y + h - c, w - 2 * c, c, 16, True, False)
		self._TileTam(par, PAT + "thinboard_line_left.tga", x, y + c, c, h - 2 * c, 16, False, True)
		self._TileTam(par, PAT + "thinboard_line_right.tga", x + w - c, y + c, c, h - 2 * c, 16, False, True)
		for (n, cx, cy) in (("lefttop", x, y), ("righttop", x + w - c, y), ("leftbottom", x, y + h - c), ("rightbottom", x + w - c, y + h - c)):
			self._TileTam(par, PAT + "thinboard_corner_%s.tga" % n, cx, cy, c, c, 16, False, False)
		return dolgu

	def _Baslik(self, par, x, y, w, metin):
		"""bolum basligi: altin yazi + alt cizgi (prototip .kb-bas)"""
		t = self._Txt(par, x, y + 12, 15, C_ALTIN, "sol", metin)
		self._Bar(par, x, y + 28, w, 1, C_CIZGI)
		return t

	def _Hap(self, par):
		"""sag yasli kucuk kutu (puan / sayi): yeri yazi genisligine gore _HapYaz'da"""
		return {"bg": self._Bar(par, 0, 0, 1, 1, 0x8c000000), "kn": self._Bar(par, 0, 0, 1, 1, C_KENAR, False),
			"t": self._Txt(par, 0, 0, 13, C_SARI, "sol")}

	def _HapYaz(self, par, h, sag, y, metin, renk=C_SARI, kenar=C_KENAR, yuk=24):
		h["t"].SetText(metin)
		h["t"].SetPackedFontColor(renk)
		w = self._Gen(h["t"]) + 20
		x = sag - w
		self._BarYer(par, h["bg"], x, y, w, yuk)
		self._BarYer(par, h["kn"], x, y, w, yuk)
		h["kn"].SetColor(kenar)
		self._TxtYer(par, h["t"], x + 10, y + yuk / 2.0)
		return x

	# ============================================================ kurulum
	def _Kur(self):
		W = float(wndMgr.GetScreenWidth())
		H = float(wndMgr.GetScreenHeight())
		self.k = k = min(H / 705.0, (W - 12.0) / WIN_W, (H - 10.0) / WIN_H)
		self._o = (0, 0)
		pw, ph = int(WIN_W * k), int(WIN_H * k)
		self.SetSize(pw, ph)
		self.SetPosition(int((W - pw) / 2), int((H - ph) / 2))
		self.keep = []
		self.kap = {}
		## govde dokunusu yutar (dunyaya gecmez); DIKKAT secim sirasi = olusturma sirasi -> govde EN ONCE
		self._Hit(self, "govde", None, 0, 0, WIN_W, WIN_H)
		self._Board(self, WIN_W, WIN_H)
		self._Tile(self, PAT + "titlebar_center.tga", 8 + 48, 8, WIN_W - 16 - 96, 34.5, 32, 32, 1.5, 1.5)
		self._Tile(self, PAT + "titlebar_left.tga", 8, 8, 48, 34.5, 32, 32, 1.5, 1.5)
		self._Tile(self, PAT + "titlebar_right.tga", WIN_W - 8 - 48, 8, 48, 34.5, 32, 32, 1.5, 1.5)
		self.baslik = self._Img(self, "", 0, 0, 1, 1, None, False)
		kp = ui.Button()
		kp.SetParent(self)
		kp.SetUpVisual(DIR + "kapat_up.png")
		kp.SetOverVisual(DIR + "kapat_up.png")
		kp.SetDownVisual(DIR + "kapat_down.png")
		tw, th = BOYUT["kapat_up.png"]
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(kp.hWnd, 30 * k / float(tw), 30 * k / float(th))
		kp.SetPosition(*self._P(self, WIN_W - 44, 10))
		kp.SetEvent(ui.__mem_func__(self.Close))
		kp.Show()
		self.keep.append(kp)
		self._KurNav()
		self.kurulu = True

	def _KurNav(self):
		self._Thin(self, 22, 54, 204, 558)
		self.nav = {}
		for (i, s) in enumerate(SEKME):
			x, y, w, h = NAV_X, NAV_Y + i * (NAV_BH + NAV_GAP), NAV_W, NAV_BH
			n = {"kart": self._Kart(self, x, y, w, h, F_NAV, 0x00000000)}
			if s == "tus":
				self._Img(self, MU + "slot_arc_blank.tga", x + 10, y + 14, 46, 46, (62, 62))
				n["ikon"] = self._Img(self, "", x + 17, y + 21, 32, 32, None, False)
			else:
				n["ikon"] = self._Img(self, "", x + 10, y + 14, 46, 46, None, False)
			n["rozet"] = {"bg": self._Bar(self, x + 40, y + 8, 22, 22, 0xffb53a26, True, False),
				"kn": self._Bar(self, x + 40, y + 8, 22, 22, 0xfff09a7f, False, False),
				"t": self._Txt(self, x + 51, y + 19, 12, C_BEYAZ, "orta")}
			n["ad1"] = self._Txt(self, x + 68, y + 28, 16, C_KREM)
			n["ad2"] = self._Txt(self, x + 68, y + 28, 16, C_KREM)
			n["alt"] = self._Txt(self, x + 68, y + 52, 12, C_SOLUK)
			n["xy"] = (x, y)
			self.nav[s] = n
		for (i, s) in enumerate(SEKME):
			self._Hit(self, "nav", s, NAV_X, NAV_Y + i * (NAV_BH + NAV_GAP), NAV_W, NAV_BH)

	def _NavTaze(self):
		race = self._Irk()
		ikon = {
			"kar": DIR + "yuz_%s.png" % YUZ.get(race, "warrior_m"),
			"ayr": "d:/ymir work/ui/skill/common/support/jeunghyul3.sub",
			"bec": self._IlkBecIkon(),
			"tus": self._IlkBecIkon(),
			"duy": DIR + "em_clap.png",
			"gor": DIR + "q_scroll_open.png",
		}
		alt = {
			"kar": _Y("Seviye %d", "Level %d") % player.GetStatus(player.LEVEL),
			"ayr": _Y("%d bonus", "%d bonuses") % self._AktifSay(),
			"bec": self._GrupAd() or _Y("Grup se\xe7ilmedi", "No group yet"),
			"tus": self._TusAltYazi(),
			"duy": _Y("%d hareket", "%d emotes") % len(self._DuyguListe()),
			"gor": _Y("%d g\xf6rev", "%d quests") % quest.GetQuestCount(),
		}
		rozet = {"kar": player.GetStatus(player.STAT), "bec": max(0, player.GetStatus(player.SKILL_ACTIVE))}
		for s in SEKME:
			n = self.nav[s]
			x, y = n["xy"]
			sec = (s == self.sekme)
			self._KartSec(n["kart"], sec)
			n["kart"]["bg"].SetColor(F_SEC if sec else F_NAV)
			if s == "tus":
				self._Yukle(n["ikon"], ikon[s], x + 17, y + 21, 32, 32)
			else:
				self._Yukle(n["ikon"], ikon[s], x + 10, y + 14, 46, 46)
			if ikon[s]:
				n["ikon"].Show()
			ad = _Metin(s)
			renk = C_SARI if sec else C_KREM
			n["ad1"].SetPackedFontColor(renk)
			n["ad2"].SetPackedFontColor(renk)
			n["alt"].SetPackedFontColor(C_ALTIN if sec else C_SOLUK)
			if len(ad) * _PT(16) * 0.56 > NAV_W - 72 and " " in ad:
				a1, a2 = ad.split(" ", 1)
				n["ad1"].SetText(a1)
				n["ad2"].SetText(a2)
				n["ad2"].Show()
				self._TxtYer(self, n["ad1"], x + 68, y + 15)
				self._TxtYer(self, n["ad2"], x + 68, y + 35)
				self._TxtYer(self, n["alt"], x + 68, y + 57)
			else:
				n["ad1"].SetText(ad)
				n["ad2"].Hide()
				self._TxtYer(self, n["ad1"], x + 68, y + 27)
				self._TxtYer(self, n["alt"], x + 68, y + 52)
			n["alt"].SetText(alt[s])
			r = rozet.get(s, 0)
			rz = n["rozet"]
			if r > 0:
				rz["t"].SetText(str(r))
				w = max(24, self._Gen(rz["t"]) + 10)
				self._BarYer(self, rz["bg"], x + 62 - w, y + 6, w, 24)
				self._BarYer(self, rz["kn"], x + 62 - w, y + 6, w, 24)
				self._TxtYer(self, rz["t"], x + 62 - w / 2.0, y + 18)
				for a in ("bg", "kn", "t"):
					rz[a].Show()
			else:
				for a in ("bg", "kn", "t"):
					rz[a].Hide()

	def _SekmeAc(self, s):
		self.sekme = s
		self.bas = None
		self._HayaletGizle()
		if s != "kar":
			self.drcAcik = False
		kur = {"kar": self._KurKar, "ayr": self._KurAyr, "bec": self._KurBec, "tus": self._KurTus, "duy": self._KurDuy, "gor": self._KurGor}
		if s not in self.kap:
			kur[s]()
			self.kirli.add(s)
		for (a, c) in self.kap.items():
			if a in SEKME:
				if a == s:
					c.Show()
				else:
					c.Hide()
		yol = DIR + _Y("", "en/") + "baslik_%s.png" % s
		(tw, th) = BOYUT[_Y("", "en/") + "baslik_%s.png" % s]
		w, h = tw / B, th / B
		self._Yukle(self.baslik, yol, WIN_W / 2.0 - w / 2.0, 25.5 - h / 2.0, w, h, (tw, th))
		self.baslik.Show()
		self.kirli.update((s, "nav"))
		self._Taze(True)

	def _Taze(self, zorla=False):
		t = app.GetTime()
		if not zorla and t < self.sonTaze:
			return
		self.sonTaze = t + YENILE_SN
		if "nav" in self.kirli:
			self.kirli.discard("nav")
			self._NavTaze()
		s = self.sekme
		if s in self.kirli:
			self.kirli.discard(s)
			try:
				{"kar": self._TazeKar, "ayr": self._TazeAyr, "bec": self._TazeBec, "tus": self._TazeTus,
					"duy": self._TazeDuy, "gor": self._TazeGor}[s]()
			except:
				import dbg, traceback
				dbg.TraceError("CharacterWindow taze %s: %s" % (s, traceback.format_exc()))

	# ============================================================ oyuncu verisi
	def _Irk(self):
		try:
			return net.GetMainActorRace()
		except:
			return 0

	def _Job(self):
		try:
			return chr.RaceToJob(self._Irk())
		except:
			return 0

	def _JobAd(self):
		return getattr(localeInfo, JOB_AD.get(self._Job(), "JOB_WARRIOR"), "")

	def _Grup(self):
		try:
			return net.GetMainActorSkillGroup()
		except:
			return 0

	def _GrupAd(self, g=None):
		if g is None:
			g = self._Grup()
		if not g:
			return ""
		return getattr(localeInfo, GRUP_AD.get(self._Job(), "SKILL_GROUP_WARRIOR_") + str(g), "")

	def _AtKullanir(self):
		try:
			slot = player.GetSkillSlotIndex(player.SKILL_INDEX_RIDING)
			if not slot:
				return False
			grade = player.GetSkillGrade(slot)
			level = abs(player.GetSkillLevel(slot))
			## at becerileri at seviyesi 21-30'da (sunucu CanUseHorseSkill grade 3): ustalik 1'de sv 21 -> 2
			return (grade == 1 and level >= 2) or grade >= 2
		except:
			return False

	def _AtDegisti(self):
		v = self._AtKullanir()
		if self.canUseHorseSkill == -1:
			self.canUseHorseSkill = v
		ret = (self.canUseHorseSkill != v)
		self.canUseHorseSkill = v
		return ret

	def _Derece(self, grade, level):
		"""(rozet, uzun ad, renk anahtari, ilerleme 0..1) - uitaskbar rozetiyle ayni kural"""
		if grade >= 3:
			return ("P", _Y("Kusursuz Usta", "Perfect Master"), "p", 1.0)
		if grade == 2:
			g = max(1, min(10, level - 29 if level > 29 else level))
			return ("G%d" % g, _Y("B\xfcy\xfck Usta %d", "Grand Master %d") % g, "g", g / 10.0)
		if grade == 1:
			m = max(1, min(10, level - 19 if level > 19 else level))
			return ("M%d" % m, _Y("Usta %d", "Master %d") % m, "m", m / 10.0)
		if level <= 0:
			return ("", _Y("\xd6\xf0renilmedi", "Not learned"), "yok", 0.0)
		return (str(level), _Y("Normal %d", "Normal %d") % level, "n", min(1.0, level / 16.0))

	def _Bec(self, slot):
		try:
			idx = player.GetSkillIndex(slot)
		except:
			return None
		if not idx:
			return None
		grade = player.GetSkillGrade(slot)
		level = player.GetSkillLevel(slot)
		if idx == getattr(player, "SKILL_INDEX_RIDING", 130):
			if grade == 1:
				level += 19
			elif grade == 2:
				level += 29
			elif grade == 3:
				level = 40
			return {"slot": slot, "idx": idx, "grade": 0, "level": level, "binicilik": True}
		return {"slot": slot, "idx": idx, "grade": grade, "level": level}

	def _AktifYuvalar(self):
		return [s for s in xrange(1, 9) if player.GetSkillIndex(s)]

	def _AtYuvalar(self):
		return [s for s in xrange(9, 17) if player.GetSkillIndex(s)]

	def _DestekYuvalar(self):
		out = []
		for s in xrange(101, 113):
			i = player.GetSkillIndex(s)
			if i and i in DESTEK_GOSTER:
				out.append(s)
		return out

	def _IlkBecIkon(self):
		for s in xrange(1, 9):
			try:
				i = player.GetSkillIndex(s)
			except:
				i = 0
			if i:
				f = _BecIkon(i, 0)
				if f:
					return f
		return "d:/ymir work/ui/skill/common/support/jeunghyul4.sub"

	def _BecAd(self, idx):
		try:
			return skill.GetSkillName(idx)
		except:
			return str(idx)

	def _KullanilirMi(self, idx):
		try:
			return skill.CanUseSkill(idx)
		except:
			return False

	def _DuyguListe(self):
		out = []
		for (sabit, anahtar) in DUYGU_ANAHTAR:
			i = getattr(emotion, sabit, None)
			if i is not None and i in emotion.EMOTION_DICT:
				out.append((i, anahtar))
		return out

	def _DuyguAd(self, i):
		try:
			return emotion.EMOTION_DICT[i]["name"]
		except:
			return str(i)

	def _DuyguIkon(self, i):
		for (sabit, anahtar) in DUYGU_ANAHTAR:
			if getattr(emotion, sabit, None) == i:
				return DIR + "em_%s.png" % anahtar
		return ""

	def _DuyguYap(self, i):
		import chat
		if i not in emotion.EMOTION_DICT:
			return
		if player.IsActingEmotion():
			return
		komut = emotion.EMOTION_DICT[i]["command"]
		if i > 50:
			vid = player.GetTargetVID()
			if 0 == vid or vid == player.GetMainCharacterIndex() or chr.IsNPC(vid) or chr.IsEnemy(vid):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EMOTION_CHOOSE_ONE)
				return
			komut += " " + chr.GetNameByVID(vid)
		net.SendChatPacket(komut)

	# ============================================================ KARAKTER
	def _KurKar(self):
		p = self._Kap("kar", 234, 54, 884, 558)
		# --- kimlik
		self._Thin(p, 234, 54, 372, 276)
		self._Yuva(p, 250, 70, 100, 100)
		self.kYuz = self._Img(p, "", 255, 75, 90, 90, None, False)
		self._Bar(p, 244, 148, 34, 28, 0xff3a2c14)
		self._Bar(p, 244, 148, 34, 28, C_SARI, False)
		self.kSv = self._Txt(p, 261, 162, 15, C_SARI, "orta")
		self.kAd = self._Txt(p, 364, 83, 18, C_SARI, pisir=False)
		self.kAdB = self._Txt(p, 365, 83, 18, C_SARI, pisir=False)
		self.kSinif = self._Txt(p, 364, 108, 14, C_ALT, pisir=False)
		self.kLoncaE = self._Txt(p, 364, 128, 14, C_ALT, "sol", _Y("Lonca:", "Guild:"))
		self.kLonca = self._Txt(p, 364, 128, 14, C_KREM, pisir=False)
		self.kDrc = {"bg": self._Bar(p, 364, 141, 10, 28, 0x8c000000), "kn": self._Bar(p, 364, 141, 10, 28, C_KENAR, False),
			"et": self._Txt(p, 372, 155, 12, C_SOLUK, "sol", _Y("Derece", "Rank")),
			"ad": self._Txt(p, 372, 155, 15, C_BEYAZ), "puan": self._Txt(p, 372, 155, 13, C_KREM),
			"s": self._Txt(p, 380, 154, 14, C_ALTIN, "orta", "\x9b")}
		self.kBar = {}
		for (ad, y, ust, alt) in (("exp", 190, 0xffe9c457, 0xffa87818), ("hp", 237, 0xffe05a44, 0xffa02c1b), ("sp", 267, 0xff5a95e6, 0xff2a5aa8)):
			self._Txt(p, 250, y + 11, 12, C_ALT, "sol", ad.upper())
			self._Bar(p, 288, y, 302, 22, F_YUVA)
			b = {"f": self._Bar(p, 289, y + 1, 300, 20, "g_" + ad), "y": y}
			self._Bar(p, 288, y, 302, 22, 0xff3f3424, False)
			b["t"] = self._Txt(p, 439, y + 11, 13, C_BEYAZ, "orta")
			self.kBar[ad] = b
		self.kKalan = self._Txt(p, 590, 221, 12, C_SOLUK, "sag")
		# --- statu
		self._Thin(p, 614, 54, 504, 276)
		self._Baslik(p, 630, 70, 472, _Y("Stat\xfc Puanlar\xfd", "Status Points"))
		self.kPuan = self._Hap(p)
		self.kStat = []
		for (i, st) in enumerate(STAT):
			y = 106 + i * 53
			self._Kart(p, 630, y, 472, 48)
			self._Bar(p, 638, y + 11, 44, 26, st[3])
			self._Bar(p, 638, y + 11, 44, 26, 0x2effffff, False)
			self._Txt(p, 660, y + 24, 13, C_BEYAZ, "orta", st[2])
			self._Txt(p, 692, y + 15, 15, C_KREM, "sol", _Y(st[4], st[5]))
			self._Txt(p, 692, y + 33, 12, C_SOLUK, "sol", getattr(localeInfo, st[6], ""))
			r = {"deg": self._Txt(p, 1042, y + 24, 20, C_KREM, "sag"), "y": y}
			r["arti"] = self._Kare(p, 1052, y + 2, 44, 44, "arti", lambda a=st: self._StatArti(a))
			r["eksi"] = self._Kare(p, 1002, y + 2, 44, 44, "eksi", lambda a=st: self._StatEksi(a))
			self.kStat.append(r)
		# --- av bonuslari
		self._Thin(p, 234, 338, 372, 274)
		self._Baslik(p, 250, 354, 340, _Y("Av Bonuslar\xfd", "Hunting Bonuses"))
		self.kAv = []
		avs = [r for r in AYR if r[0] == "av"]
		for (i, r) in enumerate(avs):
			y = 390 + i * 54
			self._Kart(p, 250, y, 340, 48, 0xff1c150d, 0xff4a3a22)
			self._Yuva(p, 254, y + 4, 40, 40)
			self._Img(p, AV_IKON.get(r[1], ""), 257, y + 7, 34, 34, (32, 32))
			self._Txt(p, 304, y + 24, 15, C_KREM, "sol", _Y(r[2], r[3]))
			self.kAv.append((r, self._Txt(p, 580, y + 24, 20, C_SARI, "sag")))
		self.kIst = []
		for (i, et) in enumerate((_Y("\xd6ld\xfcr\xfclen patron", "Bosses killed"), _Y("Kesilen metin", "Metins destroyed"))):
			x = 250 + i * 173
			self._Kart(p, x, 554, 167, 42, 0x73000000)
			## telefonda yazilar buyudu (+2 pt): ad ustte, sayi altta (yan yana sigmiyordu)
			self._Txt(p, x + 10, 565, 11, C_ALT, "sol", et)
			self.kIst.append(self._Txt(p, x + 10, 584, 15, C_KREM, "sol"))
		# --- savas degerleri
		self._Thin(p, 614, 338, 504, 274)
		self._Baslik(p, 630, 354, 472, _Y("Sava\xfe De\xf0erleri", "Combat Values"))
		self.kSavas = {}
		ets = [("att", "Sald\xfdr\xfd", "Attack"), ("def", "Savunma", "Defence"), ("matt", "B\xfcy\xfc Sald\xfdr\xfds\xfd", "Magic Attack"),
			("mdef", "B\xfcy\xfc Savunmas\xfd", "Magic Defence"), ("aspd", "Sald\xfdr\xfd H\xfdz\xfd", "Attack Speed"), ("mspd", "Hareket H\xfdz\xfd", "Movement Speed"),
			("cspd", "B\xfcy\xfc H\xfdz\xfd", "Casting Speed"), ("er", "Ka\xe7\xfdnma", "Evasion")]
		for (i, (a, tr, en)) in enumerate(ets):
			x = 630 + (i % 2) * 240
			y = 390 + (i // 2) * 52
			self._Kart(p, x, y, 232, 46)
			self._Txt(p, x + 12, y + 23, 14, C_ALT, "sol", _Y(tr, en))
			self.kSavas[a] = self._Txt(p, x + 220, y + 23, 16, C_KREM, "sag")
		# --- dokunma alanlari (EN SONDA)
		self.kDrcHit = self._Hit(p, "drc", None, 362, 139, 230, 32)
		self._Link(p, 474, 352, 116, 26, _Y("T\xfcm Ayr\xfdnt\xfdlar \x9b", "All Details \x9b"), "tumayr")
		for (i, r) in enumerate(avs):
			self._Hit(p, "av", AYR.index(r), 250, 390 + i * 54, 340, 48)
		# --- derece tablosu (acilir; kimligin ustunde)
		self.kPop = self._Kap(None, 242, 62, 356, 260, p)
		pp = self.kPop
		self._Bar(pp, 242, 62, 356, 260, 0xf70c0906)
		self._Bar(pp, 242, 62, 356, 260, C_KENAR, False)
		self.kPopBas = self._Txt(pp, 254, 78, 15, C_ALTIN)
		self._Bar(pp, 530, 66, 58, 24, 0xff201911)
		self._Bar(pp, 530, 66, 58, 24, C_KENAR, False)
		self._Txt(pp, 559, 78, 13, C_ALTIN, "orta", _Y("Kapat", "Close"))
		self.kPopSat = []
		for i in xrange(9):
			y = 96 + i * 19
			s = {"kn": self._Bar(pp, 250, y, 340, 18, C_SARI, False, False), "ic": self._Bar(pp, 251, y + 1, 338, 16, 0x1ef2c94c, True, False),
				"nok": self._Bar(pp, 258, y + 5, 8, 8, DRC_RENK[i]), "ad": self._Txt(pp, 274, y + 9, 13, DRC_RENK[i]),
				"ar": self._Txt(pp, 584, y + 9, 12, C_SOLUK, "sag")}
			self.kPopSat.append(s)
		self.kPopNot1 = self._Txt(pp, 254, 282, 12, C_ALT)
		self.kPopNot2 = self._Txt(pp, 254, 298, 12, C_ALT)
		self._Hit(pp, "drckapat", None, 242, 62, 356, 260)
		pp.Hide()

	def _StatArti(self, st):
		if player.GetStatus(player.STAT) > 0:
			net.SendChatPacket("/stat_val %s 1" % st[0])

	def _StatEksi(self, st):
		net.SendChatPacket("/stat- %s" % st[0])

	def _DrcNo(self, puan):
		for (i, e) in enumerate(DRC_ESIK):
			if e is None or puan >= e:
				return i
		return len(DRC_ESIK) - 1

	def _DrcAd(self, i):
		try:
			return localeInfo.TITLE_NAME_LIST[i].strip()
		except:
			return str(i)

	def _DrcAralik(self, i):
		if i == 0:
			return _Sayi(DRC_ESIK[0]) + " " + _Y("ve \xfcst\xfc", "or more")
		if DRC_ESIK[i] is None:
			return _Sayi(DRC_ESIK[i - 1] - 1) + " " + _Y("ve alt\xfd", "or less")
		return _Sayi(DRC_ESIK[i]) + " \x96 " + _Sayi(DRC_ESIK[i - 1] - 1)

	def _TazeKar(self):
		p = self.kap["kar"]
		race = self._Irk()
		self._Yukle(self.kYuz, DIR + "yuz_%s.png" % YUZ.get(race, "warrior_m"), 255, 75, 90, 90)
		self.kYuz.Show()
		lv = player.GetStatus(player.LEVEL)
		self.kSv.SetText(str(lv))
		ad = player.GetName()
		self.kAd.SetText(ad)
		self.kAdB.SetText(ad)
		grup = self._GrupAd()
		self.kSinif.SetText(self._JobAd() + ((" \xb7 " + grup) if grup else ""))
		lonca = player.GetGuildName()
		if lonca:
			self.kLoncaE.Show()
			self.kLonca.SetText(lonca)
			self._TxtYer(p, self.kLonca, 364 + self._Gen(self.kLoncaE) + 5, 128)
			self.kLonca.Show()
		else:
			self.kLoncaE.Hide()
			self.kLonca.Hide()
		# derece (rutbe)
		try:
			(puan, grade) = player.GetAlignmentData()
		except:
			(puan, grade) = (0, 4)
		if grade < 0 or grade > 8:
			grade = self._DrcNo(puan)
		d = self.kDrc
		d["ad"].SetText(self._DrcAd(grade))
		d["ad"].SetPackedFontColor(DRC_RENK[grade])
		d["puan"].SetText(_Sayi(puan))
		x = 370
		self._TxtYer(p, d["et"], x, 155)
		x += self._Gen(d["et"]) + 6
		self._TxtYer(p, d["ad"], x, 155)
		x += self._Gen(d["ad"]) + 6
		self._TxtYer(p, d["puan"], x, 155)
		x += self._Gen(d["puan"]) + 6
		self._TxtYer(p, d["s"], x + 4, 154)
		x += 14
		self._BarYer(p, d["bg"], 364, 141, x - 364, 28)
		self._BarYer(p, d["kn"], 364, 141, x - 364, 28)
		self._BarYer(p, self.kDrcHit, 362, 139, x - 360, 32)
		self.kPopBas.SetText(_Y("Derece (R\xfctbe): %s", "Rank: %s") % _Sayi(puan))
		for i in xrange(9):
			s = self.kPopSat[i]
			s["ad"].SetText(self._DrcAd(i))
			s["ar"].SetText(self._DrcAralik(i))
			if i == grade:
				s["kn"].Show()
				s["ic"].Show()
				s["ar"].SetPackedFontColor(C_KREM)
			else:
				s["kn"].Hide()
				s["ic"].Hide()
				s["ar"].SetPackedFontColor(C_SOLUK)
		if grade > 0 and DRC_ESIK[grade - 1] is not None:
			not1 = _Y("%s i\xe7in %s puan kald\xfd.", "%s points to %s.")
			if _EN[0]:
				not1 = not1 % (_Sayi(DRC_ESIK[grade - 1] - puan), self._DrcAd(grade - 1))
			else:
				not1 = not1 % (self._DrcAd(grade - 1), _Sayi(DRC_ESIK[grade - 1] - puan))
		else:
			not1 = _Y("En y\xfcksek derecedesin.", "You are at the highest rank.")
		self.kPopNot1.SetText(not1)
		self.kPopNot2.SetText(_Y("Canavar avlad\xfdk\xe7a artar; masum oyuncu \xf6ld\xfcr\xfcnce d\xfc\xfeer.", "Rises as you hunt; drops when you kill innocent players."))
		if self.drcAcik:
			self.kPop.Show()
		else:
			self.kPop.Hide()
		# cubuklar
		exp = player.GetEXP() & 0xFFFFFFFFL
		nxt = player.GetStatus(player.NEXT_EXP) & 0xFFFFFFFFL
		oran = (float(exp) / nxt) if nxt > 0 else 0.0
		self._CubukYaz(p, "exp", oran, _Y(("%%%.1f" % (oran * 100.0)).replace(".", ","), "%.1f%%" % (oran * 100.0)))
		self.kKalan.SetText(_Y("Kalan EXP: %s", "EXP to next level: %s") % _Sayi(max(0, nxt - exp)))
		hp, mhp = player.GetStatus(player.HP), player.GetStatus(player.MAX_HP)
		sp, msp = player.GetStatus(player.SP), player.GetStatus(player.MAX_SP)
		self._CubukYaz(p, "hp", (float(hp) / mhp) if mhp > 0 else 0.0, "%s / %s" % (_Sayi(hp), _Sayi(mhp)))
		self._CubukYaz(p, "sp", (float(sp) / msp) if msp > 0 else 0.0, "%s / %s" % (_Sayi(sp), _Sayi(msp)))
		# statu
		puanS = player.GetStatus(player.STAT)
		if puanS > 0:
			self._HapYaz(p, self.kPuan, 1102, 70, _Y("Da\xf0\xfdt\xfdlacak puan: %d", "Points to spend: %d") % puanS)
		else:
			self._HapYaz(p, self.kPuan, 1102, 70, _Y("Da\xf0\xfdt\xfdlacak puan yok", "No points to spend"), C_SOLUK, C_CIZGI)
		eksi = player.GetStatus(POINT_STAT_RESET_COUNT) > 0
		for (i, st) in enumerate(STAT):
			r = self.kStat[i]
			r["deg"].SetText(str(player.GetStatus(getattr(player, st[1]))))
			if puanS > 0:
				r["arti"].Show()
			else:
				r["arti"].Hide()
			if eksi:
				r["eksi"].Show()
				self._TxtYer(p, r["deg"], 992, r["y"] + 24)
			else:
				r["eksi"].Hide()
				self._TxtYer(p, r["deg"], 1042 if puanS > 0 else 1092, r["y"] + 24)
		# av + istatistik
		for (r, t) in self.kAv:
			t.SetText(self._Bicim(r[1], self._Deger(r[1])))
		try:
			self.kIst[0].SetText(_Sayi(player.GetBossPuan()))
			self.kIst[1].SetText(_Sayi(player.GetMetinPuan()))
		except:
			self.kIst[0].SetText("-")
			self.kIst[1].SetText("-")
		# savas
		mn, mx = player.GetStatus(player.ATT_MIN), player.GetStatus(player.ATT_MAX)
		ek = player.GetStatus(player.ATT_BONUS) + player.GetStatus(player.ATTACKER_BONUS)
		self.kSavas["att"].SetText(_Sayi(mn + ek) if mn == mx else "%s - %s" % (_Sayi(mn + ek), _Sayi(mx + ek)))
		df = player.GetStatus(player.DEF_GRADE)
		if constInfo.ADD_DEF_BONUS_ENABLE:
			df += player.GetStatus(player.DEF_BONUS)
		self.kSavas["def"].SetText(_Sayi(df))
		m0 = player.GetStatus(player.MAG_ATT) + player.GetStatus(player.MIN_MAGIC_WEP)
		m1 = player.GetStatus(player.MAG_ATT) + player.GetStatus(player.MAX_MAGIC_WEP)
		self.kSavas["matt"].SetText(_Sayi(m0) if m0 == m1 else "%s - %s" % (_Sayi(m0), _Sayi(m1)))
		self.kSavas["mdef"].SetText(_Sayi(player.GetStatus(player.MAG_DEF)))
		self.kSavas["aspd"].SetText(str(player.GetStatus(player.ATT_SPEED)))
		self.kSavas["mspd"].SetText(str(player.GetStatus(player.MOVING_SPEED)))
		self.kSavas["cspd"].SetText(str(player.GetStatus(player.CASTING_SPEED)))
		self.kSavas["er"].SetText(str(player.GetStatus(player.EVADE_RATE)))

	def _CubukYaz(self, p, ad, oran, metin):
		b = self.kBar[ad]
		oran = max(0.0, min(1.0, oran))
		w = 300.0 * oran
		if w < 0.5:
			b["f"].Hide()
		else:
			self._BarYer(p, b["f"], 289, b["y"] + 1, w, 20)
			b["f"].Show()
		b["t"].SetText(metin)

	# ============================================================ AYRINTILAR
	def _Deger(self, t):
		"""eski uicharacterdetails.__Deger ile ayni: ayni seyin parcalari TOPLAM (sunucu GetPoint her parcayi 100'de keser)"""
		if isinstance(t, tuple):
			top = 0
			for x in t:
				top += min(int(player.GetStatus(x)), 100)
			return top
		return player.GetStatus(t)

	def _Bicim(self, t, v):
		try:
			v = int(v)
		except:
			return str(v)
		if t == 88 or t == 89:
			return _Y("Var", "Yes") if v > 0 else _Y("Yok", "No")
		if t in (85, 117, 126):
			v = min(v, 100)
		if t == 95 or t == 96 or v == 0:
			return str(v)
		return _Yuzde(v)

	def _AktifSay(self):
		n = 0
		for r in AYR:
			try:
				if self._Deger(r[1]) != 0:
					n += 1
			except:
				pass
		return n

	def _KurAyr(self):
		p = self._Kap("ayr", 234, 54, 884, 558)
		self.aCip = []
		for (k, tr, en, ktr, ken) in [("hepsi", "", "", "T\xfcm\xfc", "All")] + AKAT:
			c = {"k": k, "bg": self._Bar(p, 0, 56, 1, 42, F_NAV), "kn": self._Bar(p, 0, 56, 1, 42, C_CIZGI, False), "ic": _Parilti(self, p, 0, 56, 1, 42),
				"t": self._Txt(p, 0, 77, 14, C_KREM, "orta", _Y(ktr, ken))}
			self.aCip.append(c)
		x = 234
		for c in self.aCip:
			w = self._Gen(c["t"]) + 26
			self._BarYer(p, c["bg"], x, 56, w, 42)
			self._BarYer(p, c["kn"], x, 56, w, 42)
			c["ic"].Yer(x, 56, w, 42)
			self._TxtYer(p, c["t"], x + w / 2.0, 77)
			c["x"] = (x, w)
			x += w + 6
		tg = {"t": self._Txt(p, 0, 77, 14, C_ALT, "sol", _Y("Yaln\xfdz aktifler", "Active only"))}
		tw = self._Gen(tg["t"])
		x0 = 1118 - tw - 54
		tg["bg"] = self._Bar(p, x0, 56, 1118 - x0, 42, 0xff221b12)
		tg["kn"] = self._Bar(p, x0, 56, 1118 - x0, 42, C_KENAR, False)
		tg["kare"] = self._Bar(p, x0 + 12, 67, 20, 20, F_YUVA)
		self._Bar(p, x0 + 12, 67, 20, 20, C_KENAR, False)
		tg["isr"] = self._Bar(p, x0 + 16, 71, 12, 12, C_SARI)
		self._TxtYer(p, tg["t"], x0 + 42, 77)
		tg["t"].SetTop()
		tg["x"] = x0
		self.aTog = tg
		# liste
		self._Thin(p, 234, 108, 884, 396)
		self.aSat = []
		for j in xrange(AYR_SATIR):
			y = 124 + j * AYR_H
			s = {"y": y,
				"bt": self._Txt(p, 276, y + 21, 15, C_ALTIN), "bs": self._Txt(p, 276, y + 21, 12, C_SOLUK),
				"bl": self._Bar(p, 250, y + 21, 18, 1, C_KENAR, True, False), "br": self._Bar(p, 400, y + 21, 600, 1, C_KENAR, True, False),
				"gn": self._Txt(p, 676, y + 21, 13, C_ALTIN, "orta"), "h": []}
			for c in xrange(2):
				x = 250 + c * 424
				h = {"kart": self._Kart(p, x, y + 2, 416, 40, 0xff15100b, C_CIZGI, False), "x": x}
				h["ad"] = self._Txt(p, x + 12, y + 22, 14, C_KREM)
				h["deg"] = self._Txt(p, x + 404, y + 22, 16, C_SARI, "sag")
				s["h"].append(h)
			self.aSat.append(s)
		self.aKay = self._Bar(p, 1097, 124, 4, 352, 0x40000000)
		self.aKayB = self._Bar(p, 1097, 124, 4, 40, C_KENAR)
		# bilgi kutusu
		self._Thin(p, 234, 512, 884, 100)
		self.aBilT = self._Txt(p, 250, 539, 16, C_SARI)
		self.aBilA = self._Txt(p, 250, 560, 13, C_ALT, pisir=False)
		self.aBilA2 = self._Txt(p, 250, 577, 13, C_ALT, pisir=False)
		self.aBilC = []
		for i in xrange(3):
			self.aBilC.append({"bg": self._Bar(p, 250, 530, 10, 18, 0x80000000, True, False), "kn": self._Bar(p, 250, 530, 10, 18, C_CIZGI, False, False),
				"a": self._Txt(p, 256, 539, 12, C_KREM), "d": self._Txt(p, 256, 539, 12, C_SARI)})
		# dokunma alanlari
		for c in self.aCip:
			self._Hit(p, "cip", c["k"], c["x"][0], 52, c["x"][1], 50)
		self._Hit(p, "yalniz", None, tg["x"], 52, 1118 - tg["x"], 50)
		self._Hit(p, "ayrliste", None, 250, 124, 852, AYR_SATIR * AYR_H)

	def _AyrSatirlar(self):
		"""gorunen satir modeli: ("b", kat, gorunen, toplam) | ("c", [i, i]) | ("g", gizli)"""
		out = []
		gizli = 0
		kats = AKAT if self.ayrKat == "hepsi" else [a for a in AKAT if a[0] == self.ayrKat]
		for a in kats:
			tum = [i for (i, r) in enumerate(AYR) if r[0] == a[0]]
			gor = []
			for i in tum:
				try:
					v = self._Deger(AYR[i][1])
				except:
					v = 0
				if not self.ayrYalniz or v != 0:
					gor.append(i)
			gizli += len(tum) - len(gor)
			if not gor and self.ayrKat == "hepsi":
				continue
			out.append(("b", a, len(gor), len(tum)))
			if not gor:
				out.append(("bos",))
			for j in xrange(0, len(gor), 2):
				out.append(("c", gor[j:j + 2]))
		if self.ayrYalniz and gizli:
			out.append(("g", gizli))
		return out

	def _TazeAyr(self):
		p = self.kap["ayr"]
		for c in self.aCip:
			on = (c["k"] == self.ayrKat)
			c["bg"].SetColor(F_SEC if on else F_NAV)
			c["kn"].SetColor(C_SARI if on else C_CIZGI)
			if on:
				c["ic"].Show()
			else:
				c["ic"].Hide()
			c["t"].SetPackedFontColor(C_SARI if on else C_KREM)
		if self.ayrYalniz:
			self.aTog["isr"].Show()
		else:
			self.aTog["isr"].Hide()
		self.ayrSatir = self._AyrSatirlar()
		n = len(self.ayrSatir)
		self.ayrKay = max(0, min(self.ayrKay, n - AYR_SATIR))
		for j in xrange(AYR_SATIR):
			s = self.aSat[j]
			m = self.ayrSatir[self.ayrKay + j] if self.ayrKay + j < n else None
			tur = m[0] if m else None
			for a in ("bt", "bs", "bl", "br", "gn"):
				s[a].Hide()
			for h in s["h"]:
				self._KartGoster(h["kart"], False)
				h["ad"].Hide()
				h["deg"].Hide()
			if tur == "b":
				a = m[1]
				s["bt"].SetText(_Y(a[1], a[2]))
				s["bs"].SetText(("%d / %d" % (m[2], m[3])) if self.ayrYalniz else str(m[3]))
				bx = 276 + self._Gen(s["bt"]) + 8
				self._TxtYer(p, s["bs"], bx, s["y"] + 21)
				rx = bx + self._Gen(s["bs"]) + 10
				self._BarYer(p, s["br"], rx, s["y"] + 21, 1090 - rx, 1)
				for a2 in ("bt", "bs", "bl", "br"):
					s[a2].Show()
			elif tur == "bos":
				s["gn"].SetText(_Y("Bu b\xf6l\xfcmde aktif bonus yok.", "No active bonuses in this section."))
				s["gn"].SetPackedFontColor(C_SOLUK)
				s["gn"].Show()
			elif tur == "g":
				s["gn"].SetText(_Y("%d bo\xfe bonus gizli \xb7 G\xf6ster", "%d empty bonuses hidden \xb7 Show") % m[1])
				s["gn"].SetPackedFontColor(C_ALTIN)
				s["gn"].Show()
			elif tur == "c":
				for (c, i) in enumerate(m[1]):
					h = s["h"][c]
					r = AYR[i]
					v = self._Deger(r[1])
					av = (r[0] == "av")
					self._KartGoster(h["kart"], True)
					h["kart"]["bg"].SetColor(0xff21190e if av else 0xff15100b)
					h["kart"]["kenar"] = 0xff5a4626 if av else C_CIZGI
					self._KartSec(h["kart"], i == self.ayrSec)
					h["ad"].SetText(_Y(r[2], r[3]))
					h["ad"].SetPackedFontColor(C_KREM if (v != 0 or av) else 0xff8a806c)
					h["deg"].SetText(self._Bicim(r[1], v))
					h["deg"].SetPackedFontColor(C_SARI if (v != 0 or av) else 0xff5d5444)
					h["ad"].Show()
					h["deg"].Show()
		# kaydirma cubugu
		if n > AYR_SATIR:
			bh = max(24.0, 352.0 * AYR_SATIR / n)
			by = 124 + (352.0 - bh) * self.ayrKay / float(n - AYR_SATIR)
			self._BarYer(p, self.aKayB, 1097, by, 4, bh)
			self.aKay.Show()
			self.aKayB.Show()
		else:
			self.aKay.Hide()
			self.aKayB.Hide()
		self._AyrBilgi()

	def _AyrBilgi(self):
		p = self.kap["ayr"]
		for c in self.aBilC:
			for a in ("bg", "kn", "a", "d"):
				c[a].Hide()
		if self.ayrSec < 0 or self.ayrSec >= len(AYR):
			self.aBilT.SetText("")
			self.aBilA.SetText(_Y("Bir bonusa dokun; ne i\xfee yarad\xfd\xf0\xfdn\xfd burada g\xf6r.", "Tap a bonus to see what it does here."))
			self.aBilA2.SetText("")
			return
		r = AYR[self.ayrSec]
		v = self._Deger(r[1])
		self.aBilT.SetText("%s: %s" % (_Y(r[2], r[3]), self._Bicim(r[1], v)))
		acik = getattr(localeInfo, r[4], "")
		ls = _Sar(acik, 852, 13, 2) if acik else [""]
		self.aBilA.SetText(ls[0])
		self.aBilA2.SetText(ls[1] if len(ls) > 1 else "")
		if isinstance(r[1], tuple):
			x = 250 + self._Gen(self.aBilT) + 14
			for (i, pt) in enumerate(r[1][:3]):
				c = self.aBilC[i]
				ad = PARCA.get(pt, ("", ""))
				c["a"].SetText(_Y(ad[0], ad[1]))
				dv = min(int(player.GetStatus(pt)), 100)
				c["d"].SetText(_Yuzde(dv) if dv else "0")
				w1 = self._Gen(c["a"])
				w = w1 + self._Gen(c["d"]) + 18
				self._BarYer(p, c["bg"], x, 530, w, 18)
				self._BarYer(p, c["kn"], x, 530, w, 18)
				self._TxtYer(p, c["a"], x + 6, 539)
				self._TxtYer(p, c["d"], x + 10 + w1, 539)
				for a in ("bg", "kn", "a", "d"):
					c[a].Show()
				x += w + 6

	def _AyrDokun(self, mx, my):
		j = int((my - 124) / AYR_H)
		if j < 0 or j >= AYR_SATIR:
			return
		i = self.ayrKay + j
		if i >= len(self.ayrSatir):
			return
		m = self.ayrSatir[i]
		if m[0] == "g":
			self.ayrYalniz = False
			self.kirli.add("ayr")
			self._Taze(True)
		elif m[0] == "c":
			c = 0 if mx < 670 else 1
			if c < len(m[1]):
				self.ayrSec = m[1][c]
				self.kirli.add("ayr")
				self._Taze(True)

	# ============================================================ YETENEKLER
	def _KurBec(self):
		p = self._Kap("bec", 234, 54, 884, 558)
		# serit: alt sekmeler / grup onizleme
		self.bSek = []
		for i in xrange(3):
			self.bSek.append({"ic": _Parilti(self, p, 0, 56, 1, 42), "bg": self._Bar(p, 0, 56, 1, 42, F_NAV, True, False), "kn": self._Bar(p, 0, 56, 1, 42, C_CIZGI, False, False),
				"t": self._Txt(p, 0, 77, 15, C_KREM, "orta")})
		self.bGrupHap = self._Hap(p)
		self.bPuanHap = self._Hap(p)
		self._Thin(p, 234, 108, 536, 504)
		self._Thin(p, 778, 108, 340, 504)
		# buyuk kartlar (aktif / at): 2 sutun x 3 satir
		self.bBuyuk = []
		for i in xrange(6):
			x = 250 + (i % 2) * 256
			y = 124 + (i // 2) * 156
			c = {"x": x, "y": y, "kart": self._Kart(p, x, y, 248, 148, F_KART, C_CIZGI, False)}
			c["yuva"] = self._Yuva(p, x + 8, y + 28, 92, 92, False)
			c["ikon"] = self._Img(p, "", x + 14, y + 34, 80, 80, None, False)
			c["rz"] = self._Txt(p, x + 96, y + 110, 12, C_BEYAZ, "sag")
			c["ad1"] = self._Txt(p, x + 110, y + 48, 15, C_KREM, pisir=False)
			c["ad2"] = self._Txt(p, x + 110, y + 66, 15, C_KREM, pisir=False)
			c["der"] = self._Txt(p, x + 110, y + 84, 14, C_KREM)
			c["it"] = self._Bar(p, x + 110, y + 98, 126, 6, F_YUVA, True, False)
			c["ik"] = self._Bar(p, x + 110, y + 98, 126, 6, 0xff3a3022, False, False)
			c["id"] = self._Bar(p, x + 111, y + 99, 60, 4, "gh_n", True, False)
			c["cip"] = {"bg": self._Bar(p, x + 180, y + 6, 60, 18, 0x99000000, True, False), "kn": self._Bar(p, x + 180, y + 6, 60, 18, C_KENAR, False, False),
				"t": self._Txt(p, x + 210, y + 15, 11, C_SARI, "orta")}
			self.bBuyuk.append(c)
		# ipucu karti (seviye nasil artar)
		self.bIpucu = {"kn": self._Bar(p, 506, 436, 248, 148, C_CIZGI, False, False)}
		self.bIpucu["t"] = self._Txt(p, 520, 460, 13, C_ALT, "sol", _Y("Seviye nas\xfdl artar?", "How do skills level up?"))
		ipu = _Y("1\x9615: beceri puan\xfdyla; 16'da Usta (M1) olur. M1\x96M10: Beceri Kitab\xfd. G1\x96G10: Ruh Ta\xfe\xfd. Sonra Kusursuz (P).",
			"1\x9615: with skill points; at 16 it becomes Master (M1). M1\x96M10: Skill Book. G1\x96G10: Soul Stone. Then Perfect (P).")
		self.bIpucu["s"] = [self._Txt(p, 520, 484 + i * 17, 12, C_SOLUK, "sol", l, True, True) for (i, l) in enumerate(_Sar(ipu, 220, 12, 5))]
		# kucuk kartlar (destek): 3 sutun x 4 satir
		self.bKucuk = []
		for i in xrange(12):
			x = 250 + (i % 3) * 170
			y = 124 + (i // 3) * 118
			c = {"x": x, "y": y, "kart": self._Kart(p, x, y, 162, 110, F_KART, C_CIZGI, False)}
			c["yuva"] = self._Yuva(p, x + 53, y + 10, 56, 56, False)
			c["ikon"] = self._Img(p, "", x + 57, y + 14, 48, 48, None, False)
			c["rz"] = self._Txt(p, x + 106, y + 58, 12, C_BEYAZ, "sag")
			c["ad1"] = self._Txt(p, x + 81, y + 80, 13, C_KREM, "orta", pisir=False)
			c["ad2"] = self._Txt(p, x + 81, y + 96, 13, C_KREM, "orta", pisir=False)
			self.bKucuk.append(c)
		# at bilgisi
		self.bAt = {"kart": self._Kart(p, 250, 436, 504, 76, 0x66000000, C_CIZGI, False)}
		self.bAt["yuva"] = self._Yuva(p, 260, 446, 56, 56, False)
		self.bAt["ikon"] = self._Img(p, "icon/item/50050.tga", 265, 451, 46, 46, (32, 32), False)
		self.bAt["t1"] = self._Txt(p, 330, 462, 15, C_SARI)
		self.bAt["t2"] = self._Txt(p, 330, 486, 13, C_ALT, "sol",
			_Y("At becerileri at \xfczerindeyken kullan\xfdl\xfdr. At\xfdn\xfd Seyis'te geli\xfetirebilirsin.", "Horse skills are used while riding. Train your horse at the Stable Boy."))
		self.bNot = self._Txt(p, 502, 360, 14, C_SOLUK, "orta")
		# detay
		self._Yuva(p, 794, 124, 92, 92)
		self.dIkon = self._Img(p, "", 800, 130, 80, 80, None, False)
		self.dAd = self._Txt(p, 898, 150, 18, C_SARI, pisir=False)
		self.dDer = self._Txt(p, 898, 178, 14, C_KREM)
		self.dAcik = [self._Txt(p, 794, 236 + i * 20, 14, C_ALT, pisir=False) for i in xrange(3)]
		self.dOz = []
		for i in xrange(6):
			y = 300 + i * 24
			self.dOz.append({"e": self._Txt(p, 794, y + 10, 13, C_SOLUK), "d": self._Txt(p, 1102, y + 10, 13, C_KREM, "sag", pisir=False),
				"c": self._Bar(p, 794, y + 21, 308, 1, C_CIZGI, True, False)})
		self.dNotU = self._Txt(p, 948, 474, 12, C_SOLUK, "orta")
		self.dNot = [self._Txt(p, 948, 574 + i * 15, 12, C_SOLUK, "orta") for i in xrange(2)]
		# dokunma: serit sekmeleri, kartlar, dugmeler (EN SONDA)
		self.bSekHit = [self._Hit(p, "bsek", i, 0, 52, 1, 50) for i in xrange(3)]
		self.bBuyukHit = [self._Hit(p, "bk", i, self.bBuyuk[i]["x"], self.bBuyuk[i]["y"], 248, 148) for i in xrange(6)]
		self.bKucukHit = [self._Hit(p, "bkk", i, self.bKucuk[i]["x"], self.bKucuk[i]["y"], 162, 110) for i in xrange(12)]
		for c in self.bBuyuk:
			c["arti"] = self._Kare(p, c["x"] + 196, c["y"] + 52, 44, 44, "arti", lambda c=c: self._BecArti(c))
		self.dYuk = self._Dugme(p, 794, 446, 308, 54, _Y("Seviye Y\xfckselt (+1)", "Level Up (+1)"), ui.__mem_func__(self._DetayYukselt))
		self.dTus = self._Dugme(p, 794, 506, 308, 54, _Y("Tu\xfea Koy", "Put on Button"), ui.__mem_func__(self._DetayTusaKoy))
		self.bListe = []

	def _BecSekmeler(self):
		g = self._Grup()
		if g == 0:
			return [("g1", self._GrupAd(1)), ("g2", self._GrupAd(2))]
		out = [("aktif", _Y("Aktif", "Active")), ("destek", _Y("Destek", "Support"))]
		if self._AtKullanir():
			out.append(("at", _Y("At", "Horse")))
		return out

	def _BecPuanTur(self):
		return player.SKILL_HORSE if self.bsek == "at" else player.SKILL_ACTIVE

	def _Yukselir(self, b):
		if not b or self._Grup() == 0 or b.get("binicilik"):
			return False
		try:
			if self.bsek == "at":
				return (player.GetStatus(player.SKILL_HORSE) > 0 and b["grade"] == 0 and b["level"] < 20 and
					player.GetStatus(player.LEVEL) >= skill.GetSkillLevelLimit(b["idx"]))
			if self.bsek != "aktif":
				return False
			return (player.GetStatus(player.SKILL_ACTIVE) > 0 and b["grade"] == 0 and skill.CanLevelUpSkill(b["idx"], b["level"]))
		except:
			return False

	def _TazeBec(self):
		p = self.kap["bec"]
		g = self._Grup()
		seks = self._BecSekmeler()
		anahtarlar = [a for (a, t) in seks]
		if g == 0:
			if self.bsek not in ("g1", "g2"):
				self.bsek = "g%d" % self.onizGrup
		elif self.bsek not in anahtarlar:
			self.bsek = "aktif"
		x = 234
		for i in xrange(3):
			s = self.bSek[i]
			if i < len(seks):
				(a, t) = seks[i]
				on = (a == self.bsek)
				s["t"].SetText(t)
				w = self._Gen(s["t"]) + 36
				self._BarYer(p, s["bg"], x, 56, w, 42)
				self._BarYer(p, s["kn"], x, 56, w, 42)
				s["ic"].Yer(x, 56, w, 42)
				self._TxtYer(p, s["t"], x + w / 2.0, 77)
				self._BarYer(p, self.bSekHit[i], x, 52, w, 50)
				s["bg"].SetColor(F_SEC if on else F_NAV)
				s["kn"].SetColor(C_SARI if on else C_CIZGI)
				s["t"].SetPackedFontColor(C_SARI if on else C_KREM)
				for a2 in ("bg", "kn", "t"):
					s[a2].Show()
				if on:
					s["ic"].Show()
				else:
					s["ic"].Hide()
				self.bSekHit[i].Show()
				self.bSekHit[i].veri = a
				x += w - 1
			else:
				for a2 in ("bg", "kn", "t", "ic"):
					s[a2].Hide()
				self.bSekHit[i].Hide()
		# sag: grup + puan
		if g:
			pt = max(0, player.GetStatus(self._BecPuanTur()))
			if pt > 0:
				sx = self._HapYaz(p, self.bPuanHap, 1118, 65, _Y("Beceri puan\xfd: %d", "Skill points: %d") % pt)
			else:
				sx = self._HapYaz(p, self.bPuanHap, 1118, 65, _Y("Beceri puan\xfd yok", "No skill points"), C_SOLUK, C_CIZGI)
			self._HapYaz(p, self.bGrupHap, sx - 6, 65, "%s \xb7 %s" % (self._JobAd(), self._GrupAd()), C_SARI)
		else:
			self._HapYaz(p, self.bPuanHap, 1118, 65, _Y("Grubunu Beceri \xd6\xf0retmeni'nden se\xe7", "Choose your group at the Skill Teacher"), C_ALT, C_CIZGI)
			self.bGrupHap["bg"].Hide()
			self.bGrupHap["kn"].Hide()
			self.bGrupHap["t"].Hide()
		if g:
			for a2 in ("bg", "kn", "t"):
				self.bGrupHap[a2].Show()
		# liste
		if self.bsek in ("aktif", "g1", "g2"):
			yuvalar = self._AktifYuvalar()
		elif self.bsek == "at":
			yuvalar = self._AtYuvalar()
		else:
			yuvalar = self._DestekYuvalar()
		self.bListe = [self._Bec(s) for s in yuvalar]
		self.bListe = [b for b in self.bListe if b]
		if self.secBec not in [b["slot"] for b in self.bListe]:
			self.secBec = self.bListe[0]["slot"] if self.bListe else -1
		buyuk = self.bsek != "destek"
		for (i, c) in enumerate(self.bBuyuk):
			b = self.bListe[i] if (buyuk and i < len(self.bListe)) else None
			self._BuyukKart(p, c, b, i)
		for (i, c) in enumerate(self.bKucuk):
			b = self.bListe[i] if ((not buyuk) and i < len(self.bListe)) else None
			self._KucukKart(p, c, b, i)
		ipucu = buyuk and self.bsek != "at" and len(self.bListe) <= 5
		for a in ("kn", "t"):
			if ipucu:
				self.bIpucu[a].Show()
			else:
				self.bIpucu[a].Hide()
		for t in self.bIpucu["s"]:
			if ipucu:
				t.Show()
			else:
				t.Hide()
		at = (self.bsek == "at")
		satir = (len(self.bListe) + 1) // 2
		ay = 124 + satir * 156 + 4
		if at:
			binic = self._Bec(player.GetSkillSlotIndex(player.SKILL_INDEX_RIDING)) if player.GetSkillSlotIndex(player.SKILL_INDEX_RIDING) else None
			self.bAt["t1"].SetText(_Y("Binicilik seviyesi: %s", "Riding level: %s") % (str(binic["level"]) if binic else "-"))
			self._KartGoster(self.bAt["kart"], True)
			for b in self.bAt["yuva"]:
				b.Show()
			self.bAt["ikon"].Show()
			self.bAt["t1"].Show()
			self.bAt["t2"].Show()
			self._BarYer(p, self.bAt["kart"]["bg"], 250, ay, 504, 76)
			self._BarYer(p, self.bAt["kart"]["kn"], 250, ay, 504, 76)
			self._BarYer(p, self.bAt["yuva"][0], 260, ay + 10, 56, 56)
			self._BarYer(p, self.bAt["yuva"][1], 260, ay + 10, 56, 56)
			self._Yukle(self.bAt["ikon"], "icon/item/50050.tga", 265, ay + 15, 46, 46, (32, 32))
			self._TxtYer(p, self.bAt["t1"], 330, ay + 26)
			self._TxtYer(p, self.bAt["t2"], 330, ay + 50)
		else:
			self._KartGoster(self.bAt["kart"], False)
			for b in self.bAt["yuva"]:
				b.Hide()
			for a in ("ikon", "t1", "t2"):
				self.bAt[a].Hide()
		if not self.bListe:
			self.bNot.SetText(_Y("Bu b\xf6l\xfcmde beceri yok.", "No skills in this section."))
			self.bNot.Show()
		else:
			self.bNot.Hide()
		self._TazeDetay()

	def _BuyukKart(self, p, c, b, i):
		x, y = c["x"], c["y"]
		hit = self.bBuyukHit[i]
		if not b:
			self._KartGoster(c["kart"], False)
			for w in c["yuva"]:
				w.Hide()
			for a in ("ikon", "rz", "ad1", "ad2", "der", "it", "ik", "id", "arti"):
				c[a].Hide()
			for a in ("bg", "kn", "t"):
				c["cip"][a].Hide()
			hit.Hide()
			return
		c["b"] = b
		self._KartGoster(c["kart"], True)
		self._KartSec(c["kart"], b["slot"] == self.secBec)
		for w in c["yuva"]:
			w.Show()
		(rz, uzun, renk, ilerleme) = self._Derece(b["grade"], b["level"])
		self._Yukle(c["ikon"], _BecIkon(b["idx"], b["grade"]), x + 14, y + 34, 80, 80, (32, 32))
		c["ikon"].Show()
		c["rz"].SetText(rz)
		c["rz"].Show()
		yuk = self._Yukselir(b)
		satirlar = _Sar(self._BecAd(b["idx"]), 80 if yuk else 126, 15, 2)
		c["ad1"].SetText(satirlar[0])
		c["ad1"].Show()
		if len(satirlar) > 1:
			c["ad2"].SetText(satirlar[1])
			c["ad2"].Show()
			self._TxtYer(self.kap["bec"], c["ad1"], x + 110, y + 40)
			self._TxtYer(self.kap["bec"], c["ad2"], x + 110, y + 58)
			dy = y + 80
		else:
			c["ad2"].Hide()
			self._TxtYer(self.kap["bec"], c["ad1"], x + 110, y + 48)
			dy = y + 70
		c["der"].SetText(uzun)
		c["der"].SetPackedFontColor(DERECE_RENK[renk])
		self._TxtYer(self.kap["bec"], c["der"], x + 110, dy)
		c["der"].Show()
		bw = 80 if yuk else 126
		self._BarYer(p, c["it"], x + 110, dy + 14, bw, 6)
		self._BarYer(p, c["ik"], x + 110, dy + 14, bw, 6)
		c["it"].Show()
		c["ik"].Show()
		if ilerleme > 0:
			self._BarYer(p, c["id"], x + 111, dy + 15, (bw - 2) * ilerleme, 4)
			c["id"].SetColor("gh_" + (renk if renk in ("n", "m", "g", "p") else "n"))
			c["id"].Show()
		else:
			c["id"].Hide()
		if yuk:
			c["arti"].Show()
		else:
			c["arti"].Hide()
		tk = self._IcerikTus(("S", b["slot"]))
		cp = c["cip"]
		if tk is not None:
			cp["t"].SetText(_Y("Tu\xfe %s", "Button %s") % self._TusAd(tk))
			w = self._Gen(cp["t"]) + 12
			self._BarYer(p, cp["bg"], x + 242 - w, y + 6, w, 18)
			self._BarYer(p, cp["kn"], x + 242 - w, y + 6, w, 18)
			self._TxtYer(p, cp["t"], x + 242 - w / 2.0, y + 15)
			for a in ("bg", "kn", "t"):
				cp[a].Show()
		else:
			for a in ("bg", "kn", "t"):
				cp[a].Hide()
		hit.Show()

	def _KucukKart(self, p, c, b, i):
		x, y = c["x"], c["y"]
		hit = self.bKucukHit[i]
		if not b:
			self._KartGoster(c["kart"], False)
			for w in c["yuva"]:
				w.Hide()
			for a in ("ikon", "rz", "ad1", "ad2"):
				c[a].Hide()
			hit.Hide()
			return
		c["b"] = b
		self._KartGoster(c["kart"], True)
		self._KartSec(c["kart"], b["slot"] == self.secBec)
		for w in c["yuva"]:
			w.Show()
		(rz, uzun, renk, ilerleme) = self._Derece(b["grade"], b["level"])
		if b["idx"] == 122:
			rz = "%d/2" % max(0, b["level"])
		self._Yukle(c["ikon"], _BecIkon(b["idx"], b["grade"]), x + 57, y + 14, 48, 48, (32, 32))
		c["ikon"].SetAlpha(1.0 if b["level"] > 0 else 0.4)
		c["ikon"].Show()
		c["rz"].SetText(rz if b["level"] > 0 else "")
		c["rz"].Show()
		satirlar = _Sar(self._BecAd(b["idx"]), 150, 13, 2)
		c["ad1"].SetText(satirlar[0])
		c["ad1"].SetPackedFontColor(C_KREM if b["level"] > 0 else C_SOLUK)
		c["ad2"].SetPackedFontColor(C_KREM if b["level"] > 0 else C_SOLUK)
		c["ad1"].Show()
		if len(satirlar) > 1:
			c["ad2"].SetText(satirlar[1])
			self._TxtYer(p, c["ad1"], x + 81, y + 78)
			c["ad2"].Show()
		else:
			self._TxtYer(p, c["ad1"], x + 81, y + 86)
			c["ad2"].Hide()
		hit.Show()

	def _SeciliBec(self):
		for b in self.bListe:
			if b["slot"] == self.secBec:
				return b
		return None

	def _TazeDetay(self):
		p = self.kap["bec"]
		b = self._SeciliBec()
		for o in self.dOz:
			o["e"].Hide()
			o["d"].Hide()
			o["c"].Hide()
		for t in self.dAcik + self.dNot + [self.dNotU]:
			t.Hide()
		self.dYuk.Hide()
		self.dTus.Hide()
		if not b:
			self.dIkon.Hide()
			self.dAd.SetText("")
			self.dDer.SetText("")
			return
		idx = b["idx"]
		(rz, uzun, renk, ilerleme) = self._Derece(b["grade"], b["level"])
		self._Yukle(self.dIkon, _BecIkon(idx, b["grade"]), 800, 130, 80, 80, (32, 32))
		self.dIkon.Show()
		ad = _Sar(self._BecAd(idx), 204, 18, 1)[0]
		self.dAd.SetText(ad)
		self.dDer.SetText(uzun)
		self.dDer.SetPackedFontColor(DERECE_RENK[renk])
		try:
			acik = skill.GetSkillDescription(idx)
		except:
			acik = ""
		for (i, l) in enumerate(_Sar(acik, 308, 14, 3)):
			self.dAcik[i].SetText(l)
			self.dAcik[i].Show()
		oz = []
		try:
			if b["level"] > 0 and not b.get("binicilik") and skill.GetSkillType(idx) == skill.SKILL_TYPE_ACTIVE:
				pct = player.GetSkillCurrentEfficientPercentage(b["slot"])
				npct = player.GetSkillNextEfficientPercentage(b["slot"])
				n = skill.GetSkillAffectDescriptionCount(idx)
				for i in xrange(min(n, 2)):
					oz.append((_Y("\xdeu an", "Now") if i == 0 else "", skill.GetSkillAffectDescription(idx, i, pct), C_KREM))
				if b["grade"] < 3 and n > 0:
					oz.append((_Y("Sonraki", "Next"), skill.GetSkillAffectDescription(idx, 0, npct), C_YESIL))
				sp = skill.GetSkillNeedSP(idx, pct)
				if sp > 0:
					oz.append((_Y("SP maliyeti", "SP cost"), _Sayi(sp), C_KREM))
				cd = skill.GetSkillCoolTime(idx, pct)
				if cd > 0:
					oz.append((_Y("Bekleme", "Cooldown"), _Y("%d sn", "%d s") % cd, C_KREM))
				du = skill.GetDuration(idx, pct)
				if du > 0:
					oz.append((_Y("S\xfcre", "Duration"), _Y("%d sn", "%d s") % du, C_KREM))
		except:
			pass
		if not oz:
			oz.append((_Y("Seviye", "Level"), uzun, DERECE_RENK[renk]))
		koyulur = self._KullanilirMi(idx) and b["level"] > 0 and not b.get("binicilik")
		if koyulur:
			tk = self._IcerikTus(("S", b["slot"]))
			oz.append((_Y("Ekrandaki tu\xfe", "On-screen button"), self._TusAd(tk) if tk is not None else _Y("Tu\xfeta de\xf0il", "Not on a button"),
				C_SARI if tk is not None else C_SOLUK))
		for (i, (e, d, renk2)) in enumerate(oz[:6]):
			o = self.dOz[i]
			o["e"].SetText(e)
			o["d"].SetText(_Sar(d, 300 - (len(e) * 7.3), 13, 1)[0])
			o["d"].SetPackedFontColor(renk2)
			o["e"].Show()
			o["d"].Show()
			o["c"].Show()
		if self._Yukselir(b):
			self.dYuk.Show()
		elif self.bsek in ("aktif",) and b["grade"] in (1, 2):
			self.dNotU.SetText(_Y("Usta sonras\xfd: Beceri Kitab\xfd", "After Master: Skill Book") if b["grade"] == 1 else
				_Y("B\xfcy\xfck Usta sonras\xfd: Ruh Ta\xfe\xfd", "After Grand Master: Soul Stone"))
			self.dNotU.Show()
		if koyulur:
			self.dTus.Show()
		for (i, l) in enumerate(_Sar(_Y("Ekrandaki tu\xfelar\xfdn\xfd \xabBeceri Tu\xfelar\xfd\xbb sekmesinden y\xf6netirsin.",
				"Manage your on-screen buttons in the \xabSkill Buttons\xbb tab."), 300, 12, 2)):
			self.dNot[i].SetText(l)
			self.dNot[i].Show()

	def _BecArti(self, c):
		b = c.get("b")
		if b and self._Yukselir(b):
			net.SendChatPacket("/skillup " + str(b["idx"]))

	def _DetayYukselt(self):
		b = self._SeciliBec()
		if b and self._Yukselir(b):
			net.SendChatPacket("/skillup " + str(b["idx"]))

	def _DetayTusaKoy(self):
		b = self._SeciliBec()
		if not b:
			return
		self.tasinan = ("S", b["slot"])
		self.kaynak = "bec"
		self.secTus = None
		self.degisMod = False
		self._SekmeAc("tus")

	# ============================================================ BECERI TUSLARI (ekrandaki hizli tuslar)
	def _Tb(self):
		try:
			import uiTaskBar
			return uiTaskBar.MOBILE_TASKBAR[0]
		except:
			return None

	def _Tuslar(self):
		tb = self._Tb()
		if not tb or not hasattr(tb, "MobileTusListesi"):
			return []
		return tb.MobileTusListesi()

	def _TusAd(self, n):
		tb = self._Tb()
		if tb and hasattr(tb, "MobileTusAd"):
			return tb.MobileTusAd(n)
		return str(n + 1)

	def _TusIcerik(self, n):
		"""(tur, veri): ("S", beceri yuvasi) | ("E", duygu) | ("I", envanter hucresi) | None"""
		tb = self._Tb()
		try:
			(tip, konum) = tb.MobileTusVeri(n)
		except:
			return None
		if tip == player.SLOT_TYPE_SKILL:
			return ("S", konum)
		if tip == player.SLOT_TYPE_EMOTION:
			return ("E", konum)
		if tip == player.SLOT_TYPE_INVENTORY:
			return ("I", konum)
		return None

	def _IcerikTus(self, ic):
		for n in self._Tuslar():
			if self._TusIcerik(n) == ic:
				return n
		return None

	def _TusAltYazi(self):
		ts = self._Tuslar()
		bos = len([n for n in ts if not self._TusIcerik(n)])
		if _EN[0]:
			return "%d free of %d" % (bos, len(ts))
		return "%d tu\xfe \xb7 %d bo\xfe" % (len(ts), bos)

	def _KurTus(self):
		p = self._Kap("tus", 234, 54, 884, 558)
		self._Thin(p, 234, 54, 520, 558)
		self._Thin(p, 762, 54, 356, 558)
		self._Baslik(p, 250, 70, 488, _Y("Ekrandaki Tu\xfelar\xfdn", "Your On-Screen Buttons"))
		self.tHap = self._Hap(p)
		self.tTop = self._Img(p, MU + "touch_attack.tga", 0, 0, 1, 1, (320, 320), False)
		for (i, l) in enumerate(_Sar(_Y("Sald\xfdr\xfd d\xfc\xf0mesinin yan\xfdndaki tu\xfelar, ekrandaki dizili\xfeiyle.",
				"The buttons next to the attack button, laid out as on your screen."), 160, 12, 4)):
			self._Txt(p, 252, 116 + i * 15, 12, C_SOLUK, "sol", l)
		self.tEkBas = self._Txt(p, 250, 446, 15, C_ALTIN, "sol", _Y("Ekledi\xf0in Tu\xfelar", "Buttons You Added"))
		self.tEkSay = self._Txt(p, 250, 446, 12, C_SOLUK)
		self._Bar(p, 250, 462, 488, 1, C_CIZGI)
		# tus havuzu: 6 yay + 10 ek
		self.tTus = []
		for i in xrange(16):
			d = {"glow": self._Img(p, MU + "edit_glow.tga", 0, 0, 1, 1, (192, 192), False),
				"halka": self._Img(p, "", 0, 0, 1, 1, (62, 62), False),
				"ikon": self._Img(p, "", 0, 0, 1, 1, None, False),
				"rz": self._Img(p, MU + "skill_badge.png", 0, 0, 1, 1, (96, 96), False),
				"rzt": self._Txt(p, 0, 0, 11, 0xfff5ebd6, "orta"),
				"adet": self._Txt(p, 0, 0, 11, C_BEYAZ, "sag"),
				"ebg": self._Bar(p, 0, 0, 1, 1, 0xff1b140c, True, False), "ekn": self._Bar(p, 0, 0, 1, 1, C_KENAR, False, False),
				"et": self._Txt(p, 0, 0, 11, C_ALTIN, "orta")}
			d["rzt"].Hide()
			d["adet"].Hide()
			d["et"].Hide()
			self.tTus.append(d)
		self.tEkle = {"halka": self._Img(p, MU + "slot_arc_blank.tga", 0, 0, 1, 1, (62, 62), False),
			"t": self._Txt(p, 0, 0, 18, C_ALTIN, "orta", "+"), "t2": self._Txt(p, 0, 0, 10, C_ALTIN, "orta", _Y("Tu\xfe Ekle", "Add"))}
		# sag panel
		self.tSecBos = {"kn": self._Bar(p, 778, 70, 324, 64, C_CIZGI, False)}
		self.tSecBos["t"] = [self._Txt(p, 940, 92 + i * 18, 14, C_SOLUK, "orta", l) for (i, l) in
			enumerate(_Sar(_Y("Bir tu\xfea dokun ya da a\xfea\xf0\xfddan bir beceri / duygu se\xe7.", "Tap a button, or pick a skill / emote below."), 300, 14, 2))]
		self.tBant = {"bg": self._Bar(p, 778, 70, 324, 64, F_SEC, True, False), "kn": self._Bar(p, 778, 70, 324, 64, C_SARI, False, False),
			"ikon": self._Img(p, "", 786, 80, 44, 44, None, False), "t1": self._Txt(p, 838, 92, 14, C_SARI, pisir=False), "t2": self._Txt(p, 838, 110, 14, C_SARI, pisir=False)}
		self.tSec = {"halka": self._Img(p, "", 778, 72, 66, 66, (62, 62), False), "ikon": self._Img(p, "", 788, 82, 46, 46, None, False),
			"b": self._Txt(p, 858, 88, 17, C_SARI), "a": self._Txt(p, 858, 110, 15, C_KREM, pisir=False), "c": self._Txt(p, 858, 130, 13, C_SOLUK, pisir=False)}
		self.tBasYazi = self._Baslik(p, 778, 204, 324, "")
		self.tKsek = []
		for i in xrange(2):
			x = 778 + i * 162
			self.tKsek.append({"bg": self._Bar(p, x, 240, 162, 38, F_NAV), "kn": self._Bar(p, x, 240, 162, 38, C_CIZGI, False), "ic": _Parilti(self, p, x, 240, 162, 38),
				"t": self._Txt(p, x + 81, 259, 14, C_KREM, "orta")})
		self.tSat = []
		for j in xrange(KAY_SATIR):
			y = 286 + j * KAY_H
			s = {"y": y, "kart": self._Kart(p, 778, y, 316, 52, F_KART, C_CIZGI, False),
				"ikon": self._Img(p, "", 782, y + 4, 44, 44, None, False),
				"a": self._Txt(p, 834, y + 17, 15, C_KREM, pisir=False), "b": self._Txt(p, 834, y + 36, 12, C_SOLUK),
				"cbg": self._Bar(p, 1000, y + 16, 1, 20, 0x66000000, True, False), "ckn": self._Bar(p, 1000, y + 16, 1, 20, C_CIZGI, False, False),
				"ct": self._Txt(p, 1088, y + 26, 12, C_SOLUK, "sag")}
			for a in ("a", "b", "ct"):
				s[a].Hide()
			self.tSat.append(s)
		self.tKay = self._Bar(p, 1098, 286, 4, KAY_SATIR * KAY_H - 4, 0x40000000)
		self.tKayB = self._Bar(p, 1098, 286, 4, 40, C_KENAR)
		self.tNot = [self._Txt(p, 940, 580 + i * 15, 12, C_SOLUK, "orta", l) for (i, l) in
			enumerate(_Sar(_Y("S\xfcr\xfckle-b\xfdrak da olur. Envanterdeki e\xfeyalar\xfd envanterden tu\xfea s\xfcr\xfckle.",
				"Drag and drop works too. Drag inventory items onto a button from the inventory."), 316, 12, 2))]
		# dokunma alanlari (EN SONDA): tuslar, ekle, sag liste, sekmeler, dugmeler
		self.tTusHit = [self._Hit(p, "tus", i, 0, 0, 1, 1) for i in xrange(16)]
		for h in self.tTusHit:
			h.Hide()
		self.tEkleHit = self._Hit(p, "tusekle", None, 0, 0, 1, 1)
		self.tKsekHit = [self._Hit(p, "ksek", k, 778 + i * 162, 236, 162, 46) for (i, k) in enumerate(("bec", "duy"))]
		self.tListeHit = self._Hit(p, "kayliste", None, 778, 286, 324, KAY_SATIR * KAY_H)
		self.tVaz = self._Link(p, 1036, 85, 60, 30, _Y("Vazge\xe7", "Cancel"), "vazgec")
		self.tKaldir = self._Dugme(p, 778, 150, 104, 44, _Y("Kald\xfdr", "Remove"), ui.__mem_func__(self._TusKaldir))
		self.tDegis = self._Dugme(p, 888, 150, 104, 44, _Y("Yer De\xf0i\xfetir", "Swap"), ui.__mem_func__(self._TusDegisBasla))
		self.tSil = self._Dugme(p, 998, 150, 104, 44, _Y("Tu\xfeu Sil", "Delete"), ui.__mem_func__(self._TusSil))
		self.tSil._txt.SetPackedFontColor(C_TURUNCU)
		self.tAktar = self._Dugme(p, 778, 524, 158, 44, _Y("H\xfdzl\xfd Aktar", "Quick Fill"), ui.__mem_func__(self._HizliAktar))
		self.tTemiz = self._Dugme(p, 944, 524, 158, 44, _Y("Hepsini Bo\xfealt", "Clear All"), ui.__mem_func__(self._HepsiniBosalt))
		self.tYer = {}

	def _TusGeometri(self):
		"""ekrandaki yay tuslarinin + saldiri topunun GERCEK konumu (Butonlari Ozellestir dahil) -> pencere icine sigdir"""
		pts = []
		try:
			import uiMobileLayout as L
			for i in xrange(6):
				e = L._elements.get("arc%d" % i)
				(cx, cy, sz) = L._Geometry(e)
				pts.append((cx, cy, max(30.0, sz)))
			e = L._elements.get("att")
			(cx, cy, sz) = L._Geometry(e)
			if sz <= 0:
				raise Exception("top yok")
			pts.append((cx, cy, sz))
		except:
			W = float(wndMgr.GetScreenWidth())
			H = float(wndMgr.GetScreenHeight())
			d = ((0.8984, 0.5920), (0.9506, 0.5797), (0.8037, 0.9059), (0.8532, 0.6265), (0.8202, 0.7037), (0.8084, 0.7995), (0.90466, 0.78085))
			A = W / H
			pts = []
			for (i, (x, y)) in enumerate(d):
				cx = (1.0 - (1.0 - x) * (2712.0 / 1220.0) / A) * W
				pts.append((cx, y * H, 167.0 if i == 6 else 62.0))
		x0 = min(p[0] - p[2] / 2.0 for p in pts)
		x1 = max(p[0] + p[2] / 2.0 for p in pts)
		y0 = min(p[1] - p[2] / 2.0 for p in pts)
		y1 = max(p[1] + p[2] / 2.0 for p in pts)
		s = min(1.15, 440.0 / max(1.0, x1 - x0), 320.0 / max(1.0, y1 - y0))
		ox = 250 + (488 - (x1 - x0) * s) / 2.0 + 30
		oy = 108 + (324 - (y1 - y0) * s) / 2.0
		return [(ox + (p[0] - x0) * s, oy + (p[1] - y0) * s, p[2] * s) for p in pts]

	def _TazeTus(self):
		p = self.kap["tus"]
		tb = self._Tb()
		ts = self._Tuslar()
		if self.secTus is not None and self.secTus not in ts:
			self.secTus = None
		bos = len([n for n in ts if not self._TusIcerik(n)])
		self._HapYaz(p, self.tHap, 738, 70, _Y("%d tu\xfe \xb7 %d bo\xfe", "%d buttons \xb7 %d empty") % (len(ts), bos))
		geo = self._TusGeometri()
		(bx, by, bs) = geo[6]
		self._Yukle(self.tTop, MU + "touch_attack.tga", bx - bs / 2.0, by - bs / 2.0, bs, bs, (320, 320))
		self.tTop.SetAlpha(0.85)
		self.tTop.Show()
		ekler = [n for n in ts if n not in ts[:6]]
		self.tYer = {}
		for (j, n) in enumerate(ts[:6]):
			(cx, cy, sz) = geo[j]
			self.tYer[n] = (cx, cy, sz)
		for (j, n) in enumerate(ekler):
			cx = 256 + 29 + (j % 6) * 72
			cy = 478 + 29 + (j // 6) * 66
			self.tYer[n] = (cx, cy, 58.0)
		self.tEkSay.SetText("%d / 10" % len(ekler))
		self._TxtYer(p, self.tEkSay, 250 + self._Gen(self.tEkBas) + 8, 446)
		for i in xrange(16):
			d = self.tTus[i]
			hit = self.tTusHit[i]
			n = ts[i] if i < len(ts) else None
			if n is None:
				for a in ("glow", "halka", "ikon", "rz", "rzt", "adet", "ebg", "ekn", "et"):
					d[a].Hide()
				hit.Hide()
				continue
			(cx, cy, sz) = self.tYer[n]
			d["n"] = n
			hit.veri = n
			ad = self._TusAd(n)
			self._Yukle(d["glow"], MU + "edit_glow.tga", cx - sz * 0.8, cy - sz * 0.8, sz * 1.6, sz * 1.6, (192, 192))
			halka = MU + ("slot_arc_%s.tga" % ad)
			if not _Var(halka):
				halka = MU + "slot_arc_blank.tga"
			self._Yukle(d["halka"], halka, cx - sz / 2.0, cy - sz / 2.0, sz, sz, (62, 62))
			d["halka"].Show()
			self._TusIcerikCiz(p, d, self._TusIcerik(n), cx, cy, sz)
			# numara etiketi (sol ust)
			d["et"].SetText(ad)
			w = max(20.0, self._Gen(d["et"]) + 10)
			ex, ey = cx - sz / 2.0 - 5, cy - sz / 2.0 - 5
			self._BarYer(p, d["ebg"], ex, ey, w, 18)
			self._BarYer(p, d["ekn"], ex, ey, w, 18)
			self._TxtYer(p, d["et"], ex + w / 2.0, ey + 9)
			for a in ("ebg", "ekn", "et"):
				d[a].Show()
			self._BarYer(p, hit, cx - sz / 2.0 - 4, cy - sz / 2.0 - 4, sz + 8, sz + 8)
			hit.Show()
		self._TusParla(app.GetTime())
		# tus ekle
		if len(ekler) < 10 and tb and hasattr(tb, "MobileTusEkle"):
			j = len(ekler)
			cx = 256 + 29 + (j % 6) * 72
			cy = 478 + 29 + (j // 6) * 66
			self._Yukle(self.tEkle["halka"], MU + "slot_arc_blank.tga", cx - 29, cy - 29, 58, 58, (62, 62))
			self.tEkle["halka"].SetAlpha(0.5)
			self.tEkle["halka"].Show()
			self._TxtYer(p, self.tEkle["t"], cx, cy - 6)
			self._TxtYer(p, self.tEkle["t2"], cx, cy + 13)
			self.tEkle["t"].Show()
			self.tEkle["t2"].Show()
			self._BarYer(p, self.tEkleHit, cx - 33, cy - 33, 66, 66)
			self.tEkleHit.Show()
		else:
			self.tEkle["halka"].Hide()
			self.tEkle["t"].Hide()
			self.tEkle["t2"].Hide()
			self.tEkleHit.Hide()
		self._TazeTusSag()
		self.tusImza = self._TusImza()

	def _TusIcerikCiz(self, p, d, ic, cx, cy, sz):
		d["rzt"].Hide()
		d["rz"].Hide()
		d["adet"].Hide()
		if not ic:
			d["ikon"].Hide()
			return
		isz = sz * 0.62
		if ic[0] == "S":
			b = self._Bec(ic[1])
			if not b:
				d["ikon"].Hide()
				return
			self._Yukle(d["ikon"], _BecIkon(b["idx"], b["grade"]), cx - isz / 2.0, cy - isz / 2.0, isz, isz, (32, 32))
			(rz, uzun, renk, il) = self._Derece(b["grade"], b["level"])
			if rz:
				bsz = sz * 0.38
				bx, by = cx + sz * 0.31 - bsz / 2.0, cy + sz * 0.31 - bsz / 2.0
				self._Yukle(d["rz"], MU + "skill_badge.png", bx, by, bsz, bsz, (96, 96))
				d["rz"].Show()
				d["rzt"].SetText(rz)
				self._TxtYer(p, d["rzt"], bx + bsz / 2.0, by + bsz / 2.0)
				d["rzt"].Show()
		elif ic[0] == "E":
			self._Yukle(d["ikon"], self._DuyguIkon(ic[1]), cx - isz / 2.0, cy - isz / 2.0, isz, isz)
		else:
			vnum = player.GetItemIndex(ic[1])
			if not vnum:
				d["ikon"].Hide()
				return
			item.SelectItem(vnum)
			(iw, ih) = item.GetItemSize()
			f = item.GetIconImageFileName()
			h = isz
			w = isz / max(1, ih)
			self._Yukle(d["ikon"], f, cx - w / 2.0, cy - h / 2.0, w, h, (32, 32 * max(1, ih)))
			adet = player.GetItemCount(ic[1])
			if adet > 1:
				d["adet"].SetText(str(adet))
				self._TxtYer(p, d["adet"], cx + sz * 0.26, cy + sz * 0.24)
				d["adet"].Show()
		d["ikon"].Show()

	def _TusParla(self, t):
		"""hedef modunda (tasinan / yer degistir / surukleme) tuslar nefes alir; secili tus sabit parlak"""
		import math
		hedef = bool(self.tasinan) or self.degisMod or bool(self.bas and self.bas.get("mod") == "surukle")
		for i in xrange(16):
			d = self.tTus[i]
			n = d.get("n")
			if n is None or not self.tTusHit[i].IsShow():
				d["glow"].Hide()
				continue
			isabet = (self.bas and self.bas.get("hedef") == n)
			if n == self.secTus or isabet:
				a = 0.95
			elif hedef:
				a = 0.25 + 0.55 * (0.5 + 0.5 * math.sin(t * 2.0 * math.pi / 1.6 + i * 0.7))
			elif n == self.parlakTus:
				a = 0.6
			else:
				a = 0.0
			if a <= 0.01:
				d["glow"].Hide()
			else:
				if hasattr(wndMgr, "SetDiffuseColor"):
					wndMgr.SetDiffuseColor(d["glow"].hWnd, 0.95, 0.79, 0.30, a)
				else:
					d["glow"].SetAlpha(a)
				d["glow"].Show()

	def _KaynakListe(self):
		"""tusa konabilenler (oyunda suruklenebilenler): kullanilabilir beceriler (skill.CanUseSkill) + duygular"""
		out = []
		if self.kaynak == "bec":
			for s in self._AktifYuvalar() + (self._AtYuvalar() if self._AtKullanir() else []) + self._DestekYuvalar():
				b = self._Bec(s)
				if b and b["level"] > 0 and self._KullanilirMi(b["idx"]) and not b.get("binicilik"):
					out.append(("S", s))
		else:
			for (i, a) in self._DuyguListe():
				out.append(("E", i))
		return out

	def _TazeTusSag(self):
		p = self.kap["tus"]
		# ust blok
		for a in ("bg", "kn", "ikon", "t1", "t2"):
			self.tBant[a].Hide()
		for a in ("halka", "ikon", "b", "a", "c"):
			self.tSec[a].Hide()
		self.tSecBos["kn"].Hide()
		for t in self.tSecBos["t"]:
			t.Hide()
		self._LinkGoster(self.tVaz, False)
		for b in (self.tKaldir, self.tDegis, self.tSil):
			b.Hide()
		if self.tasinan or self.degisMod:
			if self.tasinan:
				metin = _Y("%s se\xe7ildi: koymak istedi\xf0in tu\xfea dokun.", "%s selected: tap the button to put it on.") % self._IcerikAd(self.tasinan)
				self._Yukle(self.tBant["ikon"], self._IcerikIkon(self.tasinan), 786, 80, 44, 44, self._IcerikTex(self.tasinan))
				self.tBant["ikon"].Show()
				tx = 838
			else:
				metin = _Y("%s tu\xfeuyla yer de\xf0i\xfetirecek tu\xfea dokun.", "Tap the button to swap with %s.") % self._TusAd(self.secTus)
				tx = 790
			ls = _Sar(metin, 1028 - tx, 14, 2)
			self.tBant["t1"].SetText(ls[0])
			self._TxtYer(p, self.tBant["t1"], tx, 92 if len(ls) > 1 else 102)
			self.tBant["t1"].Show()
			if len(ls) > 1:
				self.tBant["t2"].SetText(ls[1])
				self._TxtYer(p, self.tBant["t2"], tx, 112)
				self.tBant["t2"].Show()
			self.tBant["bg"].Show()
			self.tBant["kn"].Show()
			self._LinkGoster(self.tVaz, True)
		elif self.secTus is not None:
			ic = self._TusIcerik(self.secTus)
			ad = self._TusAd(self.secTus)
			halka = MU + ("slot_arc_%s.tga" % ad)
			if not _Var(halka):
				halka = MU + "slot_arc_blank.tga"
			self._Yukle(self.tSec["halka"], halka, 778, 72, 66, 66, (62, 62))
			self.tSec["halka"].Show()
			if ic:
				self._Yukle(self.tSec["ikon"], self._IcerikIkon(ic), 790, 84, 42, 42, self._IcerikTex(ic))
				self.tSec["ikon"].Show()
			self.tSec["b"].SetText(_Y("%s tu\xfeu", "Button %s") % ad)
			self.tSec["a"].SetText(self._IcerikAd(ic) if ic else _Y("Bo\xfe", "Empty"))
			self.tSec["c"].SetText(self._IcerikAlt(ic)[0] if ic else "")
			self.tSec["c"].SetPackedFontColor(self._IcerikAlt(ic)[1] if ic else C_SOLUK)
			for a in ("b", "a", "c"):
				self.tSec[a].Show()
			ek = (self.secTus not in self._Tuslar()[:6])
			if ic:
				self.tKaldir.Show()
				self.tDegis.Show()
			if ek:
				self.tSil.Show()
		else:
			self.tSecBos["kn"].Show()
			for t in self.tSecBos["t"]:
				t.Show()
		# baslik + sekmeler
		if self.secTus is not None and not self.tasinan and not self.degisMod:
			self.tBasYazi.SetText(_Y("%s tu\xfeuna koymak i\xe7in se\xe7:", "Pick something for button %s:") % self._TusAd(self.secTus))
		else:
			self.tBasYazi.SetText(_Y("Tu\xfea koyabileceklerin", "What you can put on buttons"))
		sayi = {"bec": 0, "duy": len(self._DuyguListe())}
		k0 = self.kaynak
		self.kaynak = "bec"
		sayi["bec"] = len(self._KaynakListe())
		self.kaynak = k0
		for (i, k) in enumerate(("bec", "duy")):
			s = self.tKsek[i]
			on = (k == self.kaynak)
			s["t"].SetText(_Y("Beceriler", "Skills") if k == "bec" else _Y("Duygular", "Emotes"))
			s["bg"].SetColor(F_SEC if on else F_NAV)
			s["kn"].SetColor(C_SARI if on else C_CIZGI)
			s["t"].SetPackedFontColor(C_SARI if on else C_KREM)
			if on:
				s["ic"].Show()
			else:
				s["ic"].Hide()
		# liste
		self.kayListe = self._KaynakListe()
		n = len(self.kayListe)
		self.kayKay = max(0, min(self.kayKay, n - KAY_SATIR))
		for j in xrange(KAY_SATIR):
			s = self.tSat[j]
			i = self.kayKay + j
			if i >= n:
				self._KartGoster(s["kart"], False)
				for a in ("ikon", "a", "b", "ct", "cbg", "ckn"):
					s[a].Hide()
				continue
			ic = self.kayListe[i]
			y = s["y"]
			self._KartGoster(s["kart"], True)
			self._KartSec(s["kart"], self.tasinan == ic)
			self._Yukle(s["ikon"], self._IcerikIkon(ic), 782, y + 4, 44, 44, self._IcerikTex(ic))
			s["ikon"].Show()
			s["a"].SetText(_Sar(self._IcerikAd(ic), 150, 15, 1)[0])
			(alt, renk) = self._IcerikAlt(ic)
			s["b"].SetText(alt)
			s["b"].SetPackedFontColor(renk)
			tk = self._IcerikTus(ic)
			s["ct"].SetText((_Y("Tu\xfe %s", "Button %s") % self._TusAd(tk)) if tk is not None else _Y("Bo\xfeta", "Unused"))
			s["ct"].SetPackedFontColor(C_SARI if tk is not None else C_SOLUK)
			w = self._Gen(s["ct"]) + 14
			self._BarYer(p, s["cbg"], 1094 - w, y + 16, w, 20)
			self._BarYer(p, s["ckn"], 1094 - w, y + 16, w, 20)
			s["ckn"].SetColor(C_KENAR if tk is not None else C_CIZGI)
			self._TxtYer(p, s["ct"], 1094 - 7, y + 26)
			for a in ("a", "b", "ct", "cbg", "ckn"):
				s[a].Show()
		if n > KAY_SATIR:
			th = KAY_SATIR * KAY_H - 4.0
			bh = max(24.0, th * KAY_SATIR / n)
			byy = 286 + (th - bh) * self.kayKay / float(n - KAY_SATIR)
			self._BarYer(p, self.tKayB, 1098, byy, 4, bh)
			self.tKay.Show()
			self.tKayB.Show()
		else:
			self.tKay.Hide()
			self.tKayB.Hide()
		tz = app.GetTime() < self.temizT
		self.tTemiz._txt.SetText(_Y("Emin misin? Tekrar dokun", "Sure? Tap again") if tz else _Y("Hepsini Bo\xfealt", "Clear All"))
		self.tTemiz._txt.SetPackedFontColor(C_TURUNCU if tz else C_KREM)

	def _IcerikAd(self, ic):
		if not ic:
			return ""
		if ic[0] == "S":
			b = self._Bec(ic[1])
			return self._BecAd(b["idx"]) if b else ""
		if ic[0] == "E":
			return self._DuyguAd(ic[1])
		vnum = player.GetItemIndex(ic[1])
		if not vnum:
			return ""
		item.SelectItem(vnum)
		return item.GetItemName()

	def _IcerikAlt(self, ic):
		if not ic:
			return ("", C_SOLUK)
		if ic[0] == "S":
			b = self._Bec(ic[1])
			if not b:
				return ("", C_SOLUK)
			if b["idx"] == 122:
				return (_Y("A\xe7 / kapa \xb7 %d/2", "Toggle \xb7 %d/2") % max(0, b["level"]), C_KREM)
			(rz, uzun, renk, il) = self._Derece(b["grade"], b["level"])
			return (uzun, DERECE_RENK[renk])
		if ic[0] == "E":
			return ((_Y("Ortak hareket", "Mutual emote") if ic[1] > 50 else _Y("Normal hareket", "Normal emote")), C_SOLUK)
		return ("x%d" % player.GetItemCount(ic[1]), C_SOLUK)

	def _IcerikIkon(self, ic):
		if not ic:
			return ""
		if ic[0] == "S":
			b = self._Bec(ic[1])
			return _BecIkon(b["idx"], b["grade"]) if b else ""
		if ic[0] == "E":
			return self._DuyguIkon(ic[1])
		vnum = player.GetItemIndex(ic[1])
		if not vnum:
			return ""
		item.SelectItem(vnum)
		return item.GetIconImageFileName()

	def _IcerikTex(self, ic):
		if ic and ic[0] == "E":
			return BOYUT.get("em_clap.png", (128, 128))
		if ic and ic[0] == "I":
			vnum = player.GetItemIndex(ic[1])
			item.SelectItem(vnum)
			(iw, ih) = item.GetItemSize()
			return (32, 32 * max(1, ih))
		return (32, 32)

	def _TusImza(self):
		ts = self._Tuslar()
		out = [tuple(ts)]
		for n in ts:
			ic = self._TusIcerik(n)
			if ic and ic[0] == "S":
				b = self._Bec(ic[1])
				out.append((ic, b and b["grade"], b and b["level"]))
			elif ic and ic[0] == "I":
				out.append((ic, player.GetItemIndex(ic[1]), player.GetItemCount(ic[1])))
			else:
				out.append(ic)
		return tuple(out)

	# ---- tus islemleri (hepsi sunucuya; sonuc tus imzasi degisince ekrana gelir)
	def _TusKoy(self, ic, n):
		tb = self._Tb()
		if not tb or not ic:
			return
		tip = {"S": player.SLOT_TYPE_SKILL, "E": player.SLOT_TYPE_EMOTION, "I": player.SLOT_TYPE_INVENTORY}[ic[0]]
		eski = self._IcerikTus(ic)
		ad = self._IcerikAd(ic)
		if eski == n:
			self._Bilgi(_Y("%s zaten %s tu\xfeunda.", "%s is already on button %s.") % (ad, self._TusAd(n)))
			return
		tb.MobileTusKoy(n, tip, ic[1])
		self.parlakTus = n
		self.parlakT = app.GetTime() + 1.2
		if eski is not None:
			self._Bilgi(_Y("%s: %s tu\xfeundan %s tu\xfeuna ta\xfe\xfdnd\xfd.", "%s: moved from button %s to %s.") % (ad, self._TusAd(eski), self._TusAd(n)))
		else:
			self._Bilgi(_Y("%s, %s tu\xfeuna kondu.", "%s placed on button %s.") % (ad, self._TusAd(n)))

	def _TusYerDegistir(self, a, b):
		tb = self._Tb()
		if tb and a is not None and b is not None and a != b:
			tb.MobileTusDegistir(a, b)
			self.parlakTus = b
			self.parlakT = app.GetTime() + 1.2
			self._Bilgi(_Y("%s ve %s yer de\xf0i\xfetirdi.", "%s and %s swapped.") % (self._TusAd(a), self._TusAd(b)))

	def _TusKaldir(self):
		tb = self._Tb()
		if tb and self.secTus is not None:
			tb.MobileTusBosalt(self.secTus)
			self._Bilgi(_Y("%s tu\xfeu bo\xfealt\xfdld\xfd.", "Button %s cleared.") % self._TusAd(self.secTus))
		self.kirli.update(("tus", "nav"))

	def _TusDegisBasla(self):
		if self.secTus is not None:
			self.degisMod = True
			self.tasinan = None
			self.kirli.add("tus")
			self._Taze(True)

	def _TusSil(self):
		tb = self._Tb()
		if tb and self.secTus is not None and self.secTus not in self._Tuslar()[:6]:
			ad = self._TusAd(self.secTus)
			tb.MobileTusSil(self.secTus)
			self.secTus = None
			self._Bilgi(_Y("%s tu\xfeu silindi.", "Button %s deleted.") % ad)
		self.kirli.update(("tus", "nav"))
		self._Taze(True)

	def _TusEkle(self):
		tb = self._Tb()
		if not tb:
			return
		key = tb.MobileTusEkle()
		if key:
			try:
				self.secTus = int(key[2:])
			except:
				pass
			self.tasinan = None
			self.degisMod = False
			self._Bilgi(_Y("%s tu\xfeu eklendi. Ekrandaki yerini Ayarlar \x9b Butonlar\xfd \xd6zelle\xfetir'den de\xf0i\xfetirirsin.",
				"Button %s added. Move it in Settings \x9b Customize Buttons.") % self._TusAd(self.secTus))
		self.kirli.update(("tus", "nav"))
		self._Taze(True)

	def _HizliAktar(self):
		import chat
		tb = self._Tb()
		if not tb:
			return
		srcs = []
		for s in self._AktifYuvalar():
			b = self._Bec(s)
			if b and b["level"] > 0 and self._KullanilirMi(b["idx"]):
				srcs.append(s)
		if not srcs:
			self._Bilgi(_Y("Aktar\xfdlacak \xf6\xf0renilmi\xfe beceri yok.", "No learned skills to place."))
			return
		(n, kalan) = tb.MobileQuickFillSkills(srcs)
		msg = _Y("%d beceri tu\xfelara s\xfdrayla aktar\xfdld\xfd.", "%d skills placed on the buttons in order.") % n
		if kalan:
			msg += _Y(" %d beceri s\xfd\xf0mad\xfd (Tu\xfe Ekle).", " %d did not fit (Add button).") % kalan
		self.tasinan = None
		self.degisMod = False
		self._Bilgi(msg)
		self.kirli.update(("tus", "nav"))

	def _HepsiniBosalt(self):
		t = app.GetTime()
		if t >= self.temizT:
			self.temizT = t + 3.0
			self.kirli.add("tus")
			self._Taze(True)
			return
		self.temizT = 0.0
		tb = self._Tb()
		if tb:
			for n in self._Tuslar():
				if self._TusIcerik(n):
					tb.MobileTusBosalt(n)
		self._Bilgi(_Y("B\xfct\xfcn tu\xfelar bo\xfealt\xfdld\xfd.", "All buttons cleared."))
		self.kirli.update(("tus", "nav"))
		self._Taze(True)

	def _Bilgi(self, metin):
		import chat
		chat.AppendChat(chat.CHAT_TYPE_INFO, metin)

	def _TusDokun(self, n):
		if self.tasinan:
			self._TusKoy(self.tasinan, n)
			self.tasinan = None
			self.secTus = n
		elif self.degisMod:
			self.degisMod = False
			if n != self.secTus:
				self._TusYerDegistir(self.secTus, n)
			self.secTus = n
		else:
			self.secTus = None if self.secTus == n else n
		self.kirli.update(("tus", "nav"))
		self._Taze(True)

	def _KaynakDokun(self, ic):
		if self.secTus is not None and not self.degisMod and not self.tasinan:
			self._TusKoy(ic, self.secTus)
		else:
			self.tasinan = None if self.tasinan == ic else ic
			self.degisMod = False
		self.kirli.add("tus")
		self._Taze(True)

	# ---- surukleme hayaleti
	def _HayaletGoster(self, ic, mx, my):
		if not ic:
			return
		if not self.hayalet:
			h = ui.ExpandedImageBox()
			h.SetParent(self)
			h.AddFlag("not_pick")
			h._par = self
			self.keep.append(h)
			self.hayalet = h
		self.hayaletIc = ic
		self._Yukle(self.hayalet, self._IcerikIkon(ic), mx - 30, my - 30, 60, 60, self._IcerikTex(ic))
		self.hayalet.SetAlpha(0.9)
		self.hayalet.Show()
		self.hayalet.SetTop()

	def _HayaletGizle(self):
		h = self.__dict__.get("hayalet")
		if h:
			h.Hide()

	def _TusBul(self, x, y):
		for (n, (cx, cy, sz)) in self.tYer.items():
			if abs(x - cx) <= sz / 2.0 + 6 and abs(y - cy) <= sz / 2.0 + 6:
				return n
		return None

	# ============================================================ DUYGULAR
	def _KurDuy(self):
		p = self._Kap("duy", 234, 54, 884, 558)
		self._Thin(p, 234, 54, 884, 384)
		self._Baslik(p, 250, 70, 852, _Y("Normal Hareketler", "Normal Emotes"))
		self._Txt(p, 1102, 82, 12, C_SOLUK, "sag", _Y("Dokun: hareketi yap \xb7 +: tu\xfea koy", "Tap: perform \xb7 +: put on a button"))
		self._Thin(p, 234, 446, 884, 166)
		self._Baslik(p, 250, 462, 852, _Y("Ortak Hareketler", "Mutual Emotes"))
		liste = self._DuyguListe()
		normal = [d for d in liste if d[0] <= 50]
		ortak = [d for d in liste if d[0] > 50]
		self.dKare = []
		yerler = []
		for (j, d) in enumerate(normal[:18]):
			yerler.append((d, 250 + int(round((j % 6) * (860 / 6.0))), 106 + (j // 6) * 108, 100))
		for (j, d) in enumerate(ortak[:3]):
			yerler.append((d, 250 + int(round(j * (860 / 6.0))), 498, 96))
		for (d, x, y, h) in yerler:
			(i, anahtar) = d
			w = 135
			k = {"i": i, "x": x, "y": y, "w": w, "h": h, "kart": self._Kart(p, x, y, w, h)}
			self._Yuva(p, x + w / 2.0 - 30, y + 10, 60, 60)
			self._Img(p, DIR + "em_%s.png" % anahtar, x + w / 2.0 - 26, y + 14, 52, 52)
			self._Txt(p, x + w / 2.0, y + h - 14, 13, C_KREM, "orta", _Sar(self._DuyguAd(i), 130, 13, 1)[0])
			k["cip"] = {"bg": self._Bar(p, x + 3, y + 3, 10, 18, 0x99000000, True, False), "kn": self._Bar(p, x + 3, y + 3, 10, 18, C_KENAR, False, False),
				"t": self._Txt(p, x + 8, y + 12, 11, C_SARI)}
			k["cip"]["t"].Hide()
			self.dKare.append(k)
		nx = 250 + int(round(3 * (860 / 6.0)))
		self._Bar(p, nx, 498, 1102 - nx, 96, C_CIZGI, False)
		for (i, l) in enumerate(_Sar(_Y("Ortak hareket i\xe7in \xf6nce bir oyuncuyu hedef al.", "To do a mutual emote, target a player first."), 380, 14, 2)):
			self._Txt(p, nx + 18, 528 + i * 19, 14, C_ALT, "sol", l)
		self._Txt(p, nx + 18, 572, 12, C_SOLUK, "sol", _Y("Kar\xfe\xfd taraf kabul ederse hareketi birlikte yapars\xfdn\xfdz.", "If they accept, you perform it together."))
		for k in self.dKare:
			self._Hit(p, "duy", k["i"], k["x"], k["y"], k["w"], k["h"])
		for k in self.dKare:
			k["arti"] = self._Kare(p, k["x"] + k["w"] - 33, k["y"] + 3, 30, 30, "arti", lambda i=k["i"]: self._DuyguTusa(i))

	def _TazeDuy(self):
		p = self.kap["duy"]
		for k in self.dKare:
			tk = self._IcerikTus(("E", k["i"]))
			c = k["cip"]
			if tk is not None:
				c["t"].SetText(_Y("Tu\xfe %s", "Button %s") % self._TusAd(tk))
				w = self._Gen(c["t"]) + 10
				self._BarYer(p, c["bg"], k["x"] + 3, k["y"] + 3, w, 18)
				self._BarYer(p, c["kn"], k["x"] + 3, k["y"] + 3, w, 18)
				self._TxtYer(p, c["t"], k["x"] + 8, k["y"] + 12)
				for a in ("bg", "kn", "t"):
					c[a].Show()
			else:
				for a in ("bg", "kn", "t"):
					c[a].Hide()

	def _DuyguTusa(self, i):
		self.tasinan = ("E", i)
		self.kaynak = "duy"
		self.secTus = None
		self.degisMod = False
		self._SekmeAc("tus")

	# ============================================================ GOREVLER
	def _KurGor(self):
		p = self._Kap("gor", 234, 54, 884, 558)
		self.gUst = self._Txt(p, 234, 77, 15, C_ALT)
		self._Thin(p, 234, 108, 884, 504)
		self.gSat = []
		for j in xrange(GOR_SATIR):
			y = 124 + j * GOR_H
			s = {"y": y, "kart": self._Kart(p, 250, y, 852, 80, F_KART, C_CIZGI, False)}
			s["yuva"] = self._Yuva(p, 258, y + 10, 60, 60, False)
			s["ikon"] = self._Img(p, "", 262, y + 14, 52, 52, None, False)
			s["ad"] = self._Txt(p, 332, y + 28, 17, C_KREM, pisir=False)
			s["alt"] = self._Txt(p, 332, y + 54, 13, C_ALT, pisir=False)
			s["sbg"] = self._Bar(p, 936, y + 24, 130, 32, 0x8c000000, True, False)
			s["skn"] = self._Bar(p, 936, y + 24, 130, 32, C_CIZGI, False, False)
			s["st"] = self._Txt(p, 1001, y + 40, 14, C_ALT, "orta")
			s["ok"] = self._Txt(p, 1086, y + 39, 18, C_KENAR, "orta", "\x9b")
			for a in ("ad", "alt", "st", "ok"):
				s[a].Hide()
			self.gSat.append(s)
		self.gBos = self._Txt(p, 676, 300, 15, C_SOLUK, "orta", _Y("Aktif g\xf6revin yok.", "You have no active quests."))
		self.gKay = self._Bar(p, 1097, 124, 4, GOR_SATIR * GOR_H - 6, 0x40000000)
		self.gKayB = self._Bar(p, 1097, 124, 4, 40, C_KENAR)
		self._Hit(p, "gorliste", None, 250, 124, 852, GOR_SATIR * GOR_H)

	def _GorSure(self, i):
		try:
			(ad, kalan) = quest.GetQuestLastTime(i)
		except:
			return ("", C_ALT)
		if len(ad) == 0:
			return ("", C_ALT)
		if kalan <= 0:
			return (localeInfo.QUEST_TIMEOVER, C_KIRMIZI)
		if kalan >= 86400:
			return (_Y("%d g\xfcn", "%d days") % (kalan // 86400), C_ALT)
		return ("%02d:%02d:%02d" % (kalan // 3600, (kalan % 3600) // 60, kalan % 60), C_TURUNCU if kalan < 3600 else C_ALT)

	def _GorIkon(self, ikon):
		if not isinstance(ikon, str):
			return (DIR + "q_scroll_open.png", None)		# motor goruntu tutamaci (int): yol yok
		k = (ikon or "").replace("\\", "/").split("/")[-1].lower()
		if k.startswith("scroll_open"):
			return (DIR + "q_scroll_open.png", None)
		if k.startswith("scroll_close"):
			return (DIR + "q_scroll_close.png", None)
		return (ikon, (32, 32))

	def _TazeGor(self):
		p = self.kap["gor"]
		n = quest.GetQuestCount()
		self.gUst.SetText(_Y("Aktif g\xf6rev: %d", "Active quests: %d") % n)
		self.gorKay = max(0, min(self.gorKay, n - GOR_SATIR))
		for j in xrange(GOR_SATIR):
			s = self.gSat[j]
			i = self.gorKay + j
			if i >= n:
				self._KartGoster(s["kart"], False)
				for w in s["yuva"]:
					w.Hide()
				for a in ("ikon", "ad", "alt", "sbg", "skn", "st", "ok"):
					s[a].Hide()
				continue
			try:
				(ad, ikon, sayacAd, sayac) = quest.GetQuestData(i)
			except:
				(ad, ikon, sayacAd, sayac) = ("", "", "", 0)
			y = s["y"]
			self._KartGoster(s["kart"], True)
			for w in s["yuva"]:
				w.Show()
			(yol, tex) = self._GorIkon(ikon)
			self._Yukle(s["ikon"], yol, 262, y + 14, 52, 52, tex)
			if yol:
				s["ikon"].Show()
			s["ad"].SetText(_Sar(ad, 560, 17, 1)[0])
			s["alt"].SetText(("%s: %d" % (sayacAd, sayac)) if len(sayacAd) > 0 else "")
			for a in ("ad", "alt", "ok"):
				s[a].Show()
			self._GorSureYaz(s, i)
		self.gBos.Show() if n == 0 else self.gBos.Hide()
		if n > GOR_SATIR:
			th = GOR_SATIR * GOR_H - 6.0
			bh = max(24.0, th * GOR_SATIR / n)
			byy = 124 + (th - bh) * self.gorKay / float(n - GOR_SATIR)
			self._BarYer(p, self.gKayB, 1097, byy, 4, bh)
			self.gKay.Show()
			self.gKayB.Show()
		else:
			self.gKay.Hide()
			self.gKayB.Hide()

	def _GorSureYaz(self, s, i):
		(metin, renk) = self._GorSure(i)
		if metin:
			s["st"].SetText(metin)
			s["st"].SetPackedFontColor(renk)
			for a in ("sbg", "skn", "st"):
				s[a].Show()
		else:
			for a in ("sbg", "skn", "st"):
				s[a].Hide()

	# ============================================================ dokunma / kaydirma / surukleme
	def _Fare(self):
		(mx, my) = wndMgr.GetMousePosition()
		(gx, gy) = self.GetGlobalPosition()
		return ((mx - gx) / self.k, (my - gy) / self.k)

	def _BasBasla(self, ad, veri):
		(x, y) = self._Fare()
		self.bas = {"ad": ad, "veri": veri, "x0": x, "y0": y, "mod": None, "kay0": 0, "hedef": None}
		if ad == "ayrliste":
			self.bas["kay0"] = self.ayrKay
		elif ad == "kayliste":
			self.bas["kay0"] = self.kayKay
		elif ad == "gorliste":
			self.bas["kay0"] = self.gorKay

	def _BasBitir(self):
		b = self.bas
		if not b:
			return
		self.bas = None
		(x, y) = self._Fare()
		if b["mod"] == "surukle":
			self._HayaletGizle()
			hedef = self._TusBul(x, y)
			if hedef is not None:
				if b["ad"] == "tus":
					if hedef != b["veri"]:
						self._TusYerDegistir(b["veri"], hedef)
				else:
					self._TusKoy(b.get("ic"), hedef)
				self.secTus = hedef
				self.tasinan = None
				self.degisMod = False
			self.kirli.update(("tus", "nav"))
			self._Taze(True)
			return
		if b["mod"] == "kaydir":
			return
		self._Dokun(b["ad"], b["veri"], x, y)

	def _BasGuncelle(self):
		b = self.bas
		if not wndMgr.IsLeftButtonDown():
			self._BasBitir()
			return
		(x, y) = self._Fare()
		dx, dy = x - b["x0"], y - b["y0"]
		if b["mod"] is None:
			if abs(dx) < 12 and abs(dy) < 12:
				return
			if b["ad"] in ("ayrliste", "gorliste") or (b["ad"] == "kayliste" and abs(dy) >= abs(dx)):
				b["mod"] = "kaydir"
			elif b["ad"] == "kayliste" and dx < 0:
				j = int((b["y0"] - 286) / KAY_H) + self.kayKay
				if 0 <= j < len(getattr(self, "kayListe", [])):
					b["ic"] = self.kayListe[j]
					b["mod"] = "surukle"
				else:
					b["mod"] = "kaydir"
			elif b["ad"] == "tus" and self._TusIcerik(b["veri"]):
				b["ic"] = self._TusIcerik(b["veri"])
				b["mod"] = "surukle"
			else:
				b["mod"] = "bos"
		if b["mod"] == "kaydir":
			if b["ad"] == "ayrliste":
				k = max(0, min(b["kay0"] - int(round(dy / AYR_H)), len(self.ayrSatir) - AYR_SATIR))
				if k != self.ayrKay:
					self.ayrKay = k
					self._TazeAyr()
			elif b["ad"] == "kayliste":
				k = max(0, min(b["kay0"] - int(round(dy / KAY_H)), len(self.kayListe) - KAY_SATIR))
				if k != self.kayKay:
					self.kayKay = k
					self._TazeTusSag()
			elif b["ad"] == "gorliste":
				k = max(0, min(b["kay0"] - int(round(dy / GOR_H)), quest.GetQuestCount() - GOR_SATIR))
				if k != self.gorKay:
					self.gorKay = k
					self._TazeGor()
		elif b["mod"] == "surukle":
			self._HayaletGoster(b.get("ic"), x, y)
			b["hedef"] = self._TusBul(x, y)

	def _Dokun(self, ad, veri, x, y):
		if ad == "nav":
			if veri != self.sekme:
				self._SekmeAc(veri)
		elif ad == "drc":
			self.drcAcik = True
			self.kPop.Show()
		elif ad == "drckapat":
			self.drcAcik = False
			self.kPop.Hide()
		elif ad == "tumayr":
			self.ayrKat = "hepsi"
			self._SekmeAc("ayr")
		elif ad == "av":
			self.ayrSec = veri
			self.ayrKat = "av"
			self.ayrKay = 0
			self._SekmeAc("ayr")
		elif ad == "cip":
			self.ayrKat = veri
			self.ayrKay = 0
			self.kirli.add("ayr")
			self._Taze(True)
		elif ad == "yalniz":
			self.ayrYalniz = not self.ayrYalniz
			self.ayrKay = 0
			self.kirli.add("ayr")
			self._Taze(True)
		elif ad == "ayrliste":
			self._AyrDokun(x, y)
		elif ad == "bsek":
			if veri in ("g1", "g2"):
				self.onizGrup = int(veri[1])
				try:
					playerSettingModule.RegisterSkill(net.GetMainActorRace(), self.onizGrup, net.GetMainActorEmpire())
				except:
					pass
			self.bsek = veri
			self.kirli.add("bec")
			self._Taze(True)
		elif ad == "bk" or ad == "bkk":
			kartlar = self.bBuyuk if ad == "bk" else self.bKucuk
			b = kartlar[veri].get("b")
			if b:
				self.secBec = b["slot"]
				self.kirli.add("bec")
				self._Taze(True)
		elif ad == "tus":
			self._TusDokun(veri)
		elif ad == "tusekle":
			self._TusEkle()
		elif ad == "vazgec":
			self.tasinan = None
			self.degisMod = False
			self.kirli.add("tus")
			self._Taze(True)
		elif ad == "ksek":
			self.kaynak = veri
			self.kayKay = 0
			self.kirli.add("tus")
			self._Taze(True)
		elif ad == "kayliste":
			j = int((y - 286) / KAY_H)
			i = self.kayKay + j
			if 0 <= j < KAY_SATIR and i < len(getattr(self, "kayListe", [])):
				self._KaynakDokun(self.kayListe[i])
		elif ad == "duy":
			if veri > 50:
				self._DuyguYap(veri)
			else:
				self._DuyguYap(veri)
		elif ad == "gorliste":
			j = int((y - 124) / GOR_H)
			i = self.gorKay + j
			if 0 <= j < GOR_SATIR and i < quest.GetQuestCount():
				import event
				event.QuestButtonClick(-2147483648 + quest.GetQuestIndex(i))

	# ============================================================ kare
	def OnUpdate(self):
		t = app.GetTime()
		if self.bas:
			self._BasGuncelle()
		if self.kirli and t >= self.sonTaze:
			self._Taze()
		s = self.sekme
		if s == "gor" and t >= self.gorT:
			self.gorT = t + 1.0
			n = quest.GetQuestCount()
			for j in xrange(GOR_SATIR):
				i = self.gorKay + j
				if i < n:
					self._GorSureYaz(self.gSat[j], i)
		elif s == "tus" and "tus" in self.kap:
			if t >= self.tusT:
				self.tusT = t + YENILE_SN
				imza = self._TusImza()
				if imza != self.tusImza:
					self.kirli.update(("tus", "nav"))
				if self.temizT and t >= self.temizT:
					self.temizT = 0.0
					self.kirli.add("tus")
			if self.parlakTus is not None and t >= self.parlakT:
				self.parlakTus = None
				self._TusParla(t)
			## nefes alma yalniz hedef modunda (tasinan / yer degistir / surukleme), 20 Hz; sabit durumlar _TazeTus icinde bir kez
			if (self.tasinan or self.degisMod or (self.bas and self.bas.get("mod") == "surukle")) and t >= self.parlaT:
				self.parlaT = t + 0.05
				self._TusParla(t)
