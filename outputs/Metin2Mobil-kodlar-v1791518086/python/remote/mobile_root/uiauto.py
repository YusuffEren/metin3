# MOBIL - YENI OTOMATIK AV PENCERESI (mobile_root/uiauto.py) - KULLANICI 2026-09-30
#
# Tasarim : Desktop/Averos2-OtoAv-Prototip/otoav.html (v2, kullanici onayladi).
#           Solda 12 beceri + 12 iksir kutusu (altinda sure / % degeri), sagda Saldir / Odak (menzil
#           kaydiricisi) / Iksirler / Beceriler / Canlandirma anahtarlari, altta Kaydet + Avi Baslat/Durdur.
#           "+ Beceri ekle" / "+ Iksir ekle" (ya da bos kutuya dokunma) -> ogrenilmis aktif beceriler /
#           envanterdeki iksirler listesi; dokununca bos kutuya eklenir, tekrar dokununca cikar.
# Gorseller: mobile/ui/oto/*.png  (tools/bake_otoav.py, 2x pisirilir -> IMG_S 0.5)
# Kaynak  : tools/otoav/uiauto_kaynak.py (UTF-8) -> tools/otoav/gen_uiauto.py -> mobile_root/uiauto.py
#           (Turkce harfler cp1254 kacis dizilerine cevrilir).
#
# Dis arayuz ESKI pencereyle ayni (interfacemodule / game.py / uitaskbar / motor cagirir):
#   AutoWindow: Show, Close, Hide, IsShow, Destroy, GetAutoStartonoff, IsAutoRestartOn, SetCloseGame,
#   AutoOnOff(onoff, type, number, command), AUTO_ONOFF_*, SetSkillToolTip, SetItemToolTip,
#   SetAutoCooltime, RefreshAutoSkillSlot, RefreshAutoPositionSlot, OnUseSkill, OnActivateSkill,
#   OnDeactivateSkill, SaveAutoInfo, ReadAutoInfo.
# Motor (CPythonPlayer) bayraklarinin okuyucusu Python'a acik degil -> anahtar durumu pencerede tutulur
# ve her acilista / baslatmada motora yeniden yazilir. Kutular: 0-11 beceri, 12 ayrilmis, 13-24 iksir.
#
# TUZAK: ui.Window nesnesinin Python referansi dusunce C++ penceresi silinir -> her cocuk self.keep'te.

import ui
import app
import wndMgr
import player
import skill
import item
import net
import chr
import guild
import mouseModule
import systemSetting
import constInfo

DIR = "mobile/ui/oto/"
REF_W = 1040.0
REF_H = 640.0
IMG_S = 1.0 / 1.75	# dokular 1.75x pisirildi (bake_otoav FINAL)
## DOSEME (KULLANICI 2026-10-01): zemin pack parcalarindan (oyunun klasik pencereleri gibi), tek parca doku yok
PAT = "d:/ymir work/ui/pattern/"
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
TXT_H = {"baslik": 30, "bolum": 26, "ipucu": 26}	# bake_otoav_klasik.TXT_H ile AYNI (yazi seridi yuksekligi)
C_LINE = 0xff3d342a
LEFT_W = 640
HEAD_H = 58
FOOT_Y = 564

SKILL_MAX = 12
POS_START = 13		# 12 ayrilmis (paket ile ayni)
POS_END = 25

C_TEXT = 0xffefe4cc
C_MUTED = 0xffd0c0a2
C_GOLD = 0xffe0bd78
C_GOLD2 = 0xfff1d9a0
C_DIM = 0xff9a8c76
C_WHITE = 0xffffffff

LEVEL_MIN = 1
LEVEL_MAX = 120
RANGE_MIN = 2000
RANGE_MAX = 8000
RANGE_STEP = 500

# KULLANICI (2026-09-30): otomatik av metin taslarina SALDIRMAZ -> secenek kaldirildi, bayrak hep 0 (__NoStones)
TARGET_NAMES = ["1. Seviye", "2. Seviye", "3. Seviye", "4. Seviye", "5. Seviye", "Patron"]
CARDS_PER_PAGE = 10


def _SkillLevelText(grade, level):
	try:
		grade = int(grade)
		level = int(level)
	except:
		return ""
	if grade <= 0:
		return "%d" % level
	if grade == 1:
		return "M%d" % max(1, level - 19)
	if grade == 2:
		return "G%d" % max(1, level - 29)
	return "P"


_SKILL_ICONS = {}
_JOB_DIR = {"WARRIOR": "warrior", "ASSASSIN": "assassin", "SURA": "sura", "SHAMAN": "shaman", "PASSIVE": "passive",
	"SUPPORT": "common/support", "GUILD": "common/guild", "HORSE": "common/horse"}


def _LoadSkillIcons():
	"""skill.GetIconName bu motorda bos doner -> motorun yaptigi gibi skilldesc.txt'den kur:
	d:/ymir work/ui/skill/<meslek>/<ikon>_0N.sub (CPythonSkill::__RegisterGradeIconImage)."""
	if _SKILL_ICONS:
		return
	_SKILL_ICONS[0] = None
	try:
		import pack
		data = pack.Get(app.GetLocalePath() + "/skilldesc.txt")
	except:
		return
	for line in data.split("\n"):
		tok = line.rstrip("\r").split("\t")
		if len(tok) < 13:
			continue
		try:
			idx = int(tok[0])
		except:
			continue
		job = _JOB_DIR.get(tok[1].strip().upper())
		name = tok[12].strip()
		if job and name:
			_SKILL_ICONS[idx] = (job, name)


def _FileExists(f):
	try:
		import pack
		return bool(f) and pack.Exist(f)
	except:
		return bool(f)


def _SkillIconFile(skillIndex, grade):
	_LoadSkillIcons()
	e = _SKILL_ICONS.get(skillIndex)
	if not e:
		return ""
	(job, name) = e
	base = "d:/ymir work/ui/skill/%s/%s" % (job, name)
	try:
		active = skill.GetSkillType(skillIndex) == skill.SKILL_TYPE_ACTIVE
	except:
		active = True
	if active and skillIndex != 130:		# 130 = binicilik: normal ikon (motorla ayni)
		f = "%s_0%d.sub" % (base, min(3, max(1, int(grade) + 1)))
		if _FileExists(f):
			return f
		f = base + "_01.sub"
		if _FileExists(f):
			return f
	f = base + ".sub"
	if _FileExists(f):
		return f
	return ""


def _ItemIconFile(vnum):
	try:
		item.SelectItem(int(vnum))
		return item.GetIconImageFileName()
	except:
		return ""


def _ItemIconWH(vnum):
	"""esya ikonunun MANTIKSAL boyu (32 x 32*hucre). KULLANICI (2026-10-01): "iconlarin bazilari kucuk bazilari buyuk":
	HD ikon (icon/item, density 4) ilk yuklemede GetWidth 128 donuyor -> olcek 4 kat kucuk cikiyordu."""
	try:
		item.SelectItem(int(vnum))
		(w, h) = item.GetItemSize()
		return (32 * max(1, int(w)), 32 * max(1, int(h)))
	except:
		return (32, 32)


def _IsAutoItem(vnum):
	"""uiauto (paket) AddAutoSlot ile ayni kural: iksir / yetenek / etki esyalari ve BLEND."""
	try:
		item.SelectItem(int(vnum))
		t = item.GetItemType()
		st = item.GetItemSubType()
	except:
		return False
	if t == item.ITEM_TYPE_USE:
		remain = 0
		if st == item.USE_ABILITY_UP:
			remain = item.GetValue(1)
		elif st == item.USE_AFFECT:
			remain = item.GetValue(3)
		if st in (item.USE_POTION, item.USE_ABILITY_UP, item.USE_POTION_NODELAY, item.USE_AFFECT):
			return remain < 9999
		return False
	if t == item.ITEM_TYPE_BLEND:
		return True
	return False


def _IsPercentPotion(vnum):
	try:
		item.SelectItem(int(vnum))
		return item.GetItemType() == item.ITEM_TYPE_USE and item.GetItemSubType() == item.USE_POTION
	except:
		return False


class _Hit(ui.Window):
	"""Gorunmez dokunma alani (kutu, kaydirici, karartma)."""

	def __init__(self):
		ui.Window.__init__(self)
		self.onDown = None
		self.onUp = None

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


class AutoWindow(ui.Window):
	AUTO_ONOFF_START = 1
	AUTO_ONOFF_ATTACK = 2
	AUTO_ONOFF_SKILL = 3
	AUTO_ONOFF_POSITION = 4
	AUTO_ONOFF_AUTO_RANGE = 5
	AUTO_ONOFF_AUTO_RESTART = 6

	def __init__(self):
		ui.Window.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)	# olcek kendimizde (k)
		self.SetWindowName("AutoWindow")
		self.keep = []
		self.built = False
		self.tooltipSkill = None
		self.tooltipItem = None

		self.autostartonoff = 0
		self.autoRestartOn = False
		self.flags = {"saldir": True, "odak": True, "iksir": True, "beceri": True, "canlan": False}
		self.range = RANGE_MIN * 2
		try:
			r = int(player.GetAutoHuntRange())
			if r > 0:
				self.range = max(RANGE_MIN, min(RANGE_MAX, r))
		except:
			pass
		self.loadedFor = None
		self.cd = {}			# kutu -> (baslangic, sure)
		self.slotPos = {}		# kutu -> konum (beceri yuvasi / envanter)
		self.slotIcon = {}		# kutu -> yuklu ikon dosyasi
		self.editSlot = -1
		self.typed = ""
		self.pickType = "B"
		self.pickTarget = -1
		self.pickPage = 0
		self.pickData = []
		self.pendMove = None		# ilk hucreden (0) tasinan iksir: {"vnum", "dst", "slot", "name", "t"}
		self.slotVnum = {}		# iksir kutusu -> eklenen esya (yigin bitince ayni esyanin baska yiginina gecmek icin)
		self.dragging = False
		self.rangeFxUntil = 0.0
		self.toastUntil = 0.0
		self.tipShown = False
		self.lvMin = LEVEL_MIN
		self.lvMax = LEVEL_MAX
		self.targets = [True] * 6
		self.Hide()
		self.__NoStones()
		constInfo.wndAuto = self
		## KULLANICI (2026-10-01): "otoav butonuna basinca hafif gecikmeyle aciliyor" -> pencere ILK basista kuruluyordu
		## (yuzlerce oge + 75 doku; klasik kabuk dokulari 2.1 MB). Oyuna girerken (arayuz kurulurken) onceden kurulur,
		## dugmeye basinca yalniz gosterilir. Hata olursa eskisi gibi ilk Show() kurar.
		try:
			self.__Build()
		except:
			self.built = False
			try:
				import dbg, traceback
				dbg.TraceError("AutoWindow on kurulum: " + traceback.format_exc())
			except:
				pass

	def __del__(self):
		ui.Window.__del__(self)

	# ------------------------------------------------------------------ yerlesim
	def __Layout(self):
		W = wndMgr.GetScreenWidth()
		H = wndMgr.GetScreenHeight()
		# ust kenarda etki (buff) ikonlari var -> pencere alta yaslanir, ustte ~44 px bosluk
		k = min(0.985 * W / REF_W, 0.9 * H / REF_H)
		self.k = k
		self.winW = int(round(REF_W * k))
		self.winH = int(round(REF_H * k))
		self.SetSize(self.winW, self.winH)
		self.SetPosition((W - self.winW) / 2, max(0, H - self.winH - int(12 * k)))

	def P(self, x, y):
		return (int(round(x * self.k)), int(round(y * self.k)))

	def F(self, pt):
		s = int(round(pt * self.k))
		return "Tahoma:%d" % max(8, min(32, s))

	def _Img(self, name, x, y, parent=None, base=IMG_S, pick=False):
		w = ui.ExpandedImageBox()
		w.SetParent(parent or self)
		if not pick:
			w.AddFlag("not_pick")
		w.LoadImage(DIR + name)
		w.SetScale(self.k * base, self.k * base)
		w.SetPosition(*self.P(x, y))
		w.Show()
		self.keep.append(w)
		return w

	# ------------------------------------------------------------------ DOSEME yardimcilari
	def _PImg(self, path, x, y, sx=1.0, sy=1.0, parent=None):
		"""pack dokusu: 1 texel = sx/sy tasarim px"""
		w = ui.ExpandedImageBox()
		w.SetParent(parent or self)
		w.AddFlag("not_pick")
		w.LoadImage(path)
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		w.SetScale(sx * self.k, sy * self.k)
		w.SetPosition(*self.P(x, y))
		w.Show()
		self.keep.append(w)
		return w

	def _Tile(self, path, x, y, w, h, tw, th, sx=1.0, sy=1.0, parent=None):
		"""tw x th texel dokuyu (x, y, w, h) alanina DOSER (UV tekrari: dikissiz, ui.Board gibi); kenarlar P(x) .. P(x + w)
		tam sayisina OTURUR (bkz. _Otur) -> komsu parcalarla arada bosluk kalmaz"""
		img = self._PImg(path, x, y, sx, sy, parent)
		(x0, y0) = self.P(x, y)
		(x1, y1) = self.P(x + w, y + h)
		(zx, r) = _Otur(x1 - x0, w, tw, sx, HAS_RRS, self.k)
		(zy, b) = _Otur(y1 - y0, h, th, sy, HAS_RRS, self.k)
		img.SetScale(zx, zy)
		img.SetRenderingRect(0.0, 0.0, r, b)
		return img

	def _Box(self, x, y, w, h, color, fill=False, parent=None):
		b = ui.Bar() if fill else ui.Box()
		b.SetParent(parent or self)
		b.AddFlag("not_pick")
		b.SetColor(color)
		b.SetPosition(*self.P(x, y))
		b.SetSize(max(1, int(round(w * self.k))), max(1, int(round(h * self.k))))
		b.Show()
		self.keep.append(b)
		return b

	def _Board(self, W, H, parent=None):
		self._Tile(PAT + "board_base.tga", 32, 32, W - 64, H - 64, 128, 128, parent=parent)
		self._Tile(PAT + "board_line_top.tga", 32, 0, W - 64, 32, 128, 32, parent=parent)
		self._Tile(PAT + "board_line_bottom.tga", 32, H - 32, W - 64, 32, 128, 32, parent=parent)
		self._Tile(PAT + "board_line_left.tga", 0, 32, 32, H - 64, 32, 128, parent=parent)
		self._Tile(PAT + "board_line_right.tga", W - 32, 32, 32, H - 64, 32, 128, parent=parent)
		for (n, cx, cy) in (("lefttop", 0, 0), ("righttop", W - 32, 0), ("leftbottom", 0, H - 32), ("rightbottom", W - 32, H - 32)):
			self._Tile(PAT + "board_corner_%s.tga" % n, cx, cy, 32, 32, 32, 32, parent=parent)

	def _HBar(self, x, y, w, h):
		"""horizontalbar (32 texel kapak + dosenen orta) - bolum seridi"""
		sc = h / 32.0
		cap = 32 * sc
		self._Tile(PAT + "horizontalbar_center.tga", x + cap, y, w - 2 * cap, h, 32, 32, sc, sc)
		self._Tile(PAT + "horizontalbar_left.tga", x, y, cap, h, 32, 32, sc, sc)
		self._Tile(PAT + "horizontalbar_right.tga", x + w - cap, y, cap, h, 32, 32, sc, sc)

	def _Zemin(self):
		"""eski win_bg.png ile AYNI cizim (bake_otoav_klasik.win_bg), ama DOSEME: Board + govde/alt cubuk + ayirici
		cizgiler + TitleBar + baslik + bolum seritleri + ipucu."""
		W, H = int(REF_W), int(REF_H)
		self._Board(W, H)
		self._Box(12, 58, W - 24, 506, 0x48000000, fill=True)		# govde (siyah %28)
		self._Box(12, 58, W - 24, 506, C_LINE)
		self._Box(12, 564, W - 24, 52, 0x5a000000, fill=True)		# alt cubuk
		self._Box(640, 58, 1, 506, C_LINE, fill=True)			# sol | sag ayirici
		self._Box(641, 58, 1, 506, 0x96000000, fill=True)
		self._Box(12, 564, W - 24, 1, C_LINE, fill=True)
		# TitleBar: 32x32 texel, ust 23 satir dolu; x1.5 -> 34.5 (bos alt satirlar yukseklikle zaten disarida)
		self._Tile(PAT + "titlebar_center.tga", 8 + 48, 12, W - 16 - 96, 34.5, 32, 32, 1.5, 1.5)
		self._Tile(PAT + "titlebar_left.tga", 8, 12, 48, 34.5, 32, 32, 1.5, 1.5)
		self._Tile(PAT + "titlebar_right.tga", W - 8 - 48, 12, 48, 34.5, 32, 32, 1.5, 1.5)
		self._Img("oto_t_baslik.png", 52, 28.5 - TXT_H["baslik"] / 2.0)
		for (y, key) in ((72, "beceriler"), (306, "iksirler")):
			self._HBar(12, y, 618, 34)
			self._Img("oto_t_%s.png" % key, 22, y + 17 - TXT_H["bolum"] / 2.0)
		self._Img("oto_t_ipucu.png", 18, 552 - TXT_H["ipucu"] / 2.0)

	def _PanelZemin(self, p, w, h):
		"""eski panel_sol/sag.png: tas taban + koyu ort + cizgi (DOSEME)"""
		self._Tile(PAT + "board_base.tga", 0, 0, w, h, 128, 128, parent=p)
		self._Box(0, 0, w, h, 0x3c000000, fill=True, parent=p)
		self._Box(0, 0, w, h, C_LINE, parent=p)

	def _Txt(self, text, x, y, pt, color, align="left", parent=None, vcenter=True):
		t = ui.TextLine()
		t.SetParent(parent or self)
		t.AddFlag("not_pick")
		t.SetFontName(self.F(pt))
		if align == "center":
			t.SetHorizontalAlignCenter()
		elif align == "right":
			t.SetHorizontalAlignRight()
		if vcenter:
			t.SetVerticalAlignCenter()
		t.SetPackedFontColor(color)
		t.SetPosition(*self.P(x, y))
		t.SetText(text)
		t.Show()
		self.keep.append(t)
		return t

	def _Btn(self, name, x, y, func, parent=None):
		b = ui.Button()
		b.SetParent(parent or self)
		b.SetUpVisual(DIR + name + "_up.png")
		b.SetOverVisual(DIR + name + "_up.png")
		b.SetDownVisual(DIR + name + "_down.png")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, self.k * IMG_S, self.k * IMG_S)
		b.SetPosition(*self.P(x, y))
		b.SetEvent(func)
		b.Show()
		self.keep.append(b)
		return b

	def _ImgBtn(self, img, x, y, func, parent=None):
		"""tek gorselli dugme (anahtar, kart)"""
		b = ui.Button()
		b.SetParent(parent or self)
		b.SetUpVisual(DIR + img)
		b.SetOverVisual(DIR + img)
		b.SetDownVisual(DIR + img)
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, self.k * IMG_S, self.k * IMG_S)
		b.SetPosition(*self.P(x, y))
		b.SetEvent(func)
		b.Show()
		self.keep.append(b)
		return b

	def _HitBox(self, x, y, w, h, onUp=None, onDown=None, parent=None):
		hb = _Hit()
		hb.SetParent(parent or self)
		hb.SetPosition(*self.P(x, y))
		hb.SetSize(*self.P(w, h))
		hb.onUp = onUp
		hb.onDown = onDown
		hb.Show()
		self.keep.append(hb)
		return hb

	def _Panel(self, x, y, w, h):
		p = ui.Window()
		p.SetParent(self)
		p.SetPosition(*self.P(x, y))
		p.SetSize(*self.P(w, h))
		self.keep.append(p)
		return p

	# ------------------------------------------------------------------ iskelet
	def __Build(self):
		self.__Layout()
		# golge + zemin (zemin dokunmayi yutar -> acik balonlari kapatir)
		sh = self._Img("win_shadow.png", -60, -60, base=2.0)
		bg = self._HitBox(0, 0, REF_W, REF_H, onUp=ui.__mem_func__(self.__OnBackgroundTap))
		self._Zemin()		# DOSEME (eski win_bg.png ~7.8 MB yerine)

		# baslik
		self.pillOff = self._Img("pill_off.png", 196, 15)
		self.pillOn = self._Img("pill_on.png", 196, 15)
		self.pulse = self._Img("pulse.png", 198.5, 15)
		self.pillOn.Hide()
		self.pulse.Hide()
		## KULLANICI (2026-10-01): KLASIK KABUK (tools/otoav/bake_otoav_klasik.py) -> "?" kucuk klasik dugme,
		## kapat = baslik cubugunun kendi carpisi. Gorseller kucuk: arkalarinda genis gorunmez dokunma alani.
		self._HitBox(942, 8, 50, 46, onUp=ui.__mem_func__(self.__ToggleHelp))
		self._HitBox(994, 6, 46, 50, onUp=ui.__mem_func__(self.Close))
		self.helpBtn = self._Btn("yardim_btn", 958, 17.5, ui.__mem_func__(self.__ToggleHelp))
		self._Btn("kapat_x", 1005.5, 17.5, ui.__mem_func__(self.Close))

		# sol: beceri / iksir kutulari
		self.countB = self._Txt("", 99, 89, 14, C_MUTED)
		self.countI = self._Txt("", 87, 323, 14, C_MUTED)
		self._Btn("ekle_b", 414, 74, lambda: self.__OpenPicker("B", -1))
		self._Btn("temizle", 546, 74, ui.__mem_func__(self.__ClearSkills))
		self._Btn("ekle_i", 420, 308, lambda: self.__OpenPicker("I", -1))
		self._Btn("temizle", 546, 308, ui.__mem_func__(self.__ClearPotions))

		self.slotW = {}
		colW = (602.0 - 50.0) / 6.0 + 10.0
		for sec, (y0, base) in enumerate(((104, 0), (338, POS_START))):
			for i in range(12):
				row = i / 6
				col = i % 6
				slot = base + i
				cx = 20 + col * colW + (colW - 10) / 2.0
				sx = cx - 32
				sy = y0 + row * 101
				d = {}
				d["empty"] = self._Img("slot_empty.png", sx, sy)
				d["full"] = self._Img("slot_full.png", sx, sy)
				d["run"] = self._Img("slot_run.png", sx, sy)
				icon = ui.ExpandedImageBox()
				icon.SetParent(self)
				icon.AddFlag("not_pick")
				self.keep.append(icon)
				d["icon"] = icon
				d["iconXY"] = (cx, sy + 32)
				d["cnt"] = self._Txt("", sx + 60, sy + 55, 11, C_WHITE, "right")
				d["cd"] = self._Img("slot_cd.png", sx, sy)
				d["cdTxt"] = self._Txt("", cx, sy + 51, 13, C_WHITE, "center")
				d["hit"] = self._HitBox(sx, sy, 64, 64, onUp=lambda s=slot: self.__OnSlotTap(s))
				d["val"] = self._Img("val.png", cx - 30, sy + 69)
				d["valSel"] = self._Img("val_sel.png", cx - 30, sy + 69)
				d["valTxt"] = self._Txt("", cx, sy + 81, 15, C_TEXT, "center")
				d["valHit"] = self._HitBox(cx - 34, sy + 66, 68, 30, onUp=lambda s=slot: self.__OpenKeypad(s))
				for n in ("full", "run", "cd", "valSel"):
					d[n].Hide()
				self.slotW[slot] = d

		# sag: ayar satirlari
		self.rowW = {}
		self.swW = {}
		keys = ("saldir", "odak", "iksir", "beceri", "canlan")
		for i, key in enumerate(keys):
			y = 74 + i * 72
			on = self._Img("row_%s_on.png" % key, 658, y)
			off = self._Img("row_%s_off.png" % key, 658, y)
			if key in ("iksir", "beceri", "canlan"):
				self._HitBox(658, y, 280, 64, onUp=lambda kk=key: self.__Toggle(kk))
			swOn = self._ImgBtn("sw_on.png", 948, y + 15, lambda kk=key: self.__Toggle(kk))
			swOff = self._ImgBtn("sw_off.png", 948, y + 15, lambda kk=key: self.__Toggle(kk))
			self.rowW[key] = (on, off)
			self.swW[key] = (swOn, swOff)
		# Saldir: hedef ozeti + Hedefler >
		self.targetSummary = self._Txt("", 722, 117, 14, C_MUTED)
		self.hedefBtn = self._Btn("hedefler", 844, 106, ui.__mem_func__(self.__OpenTargets))
		# Odak: - [kaydirici] + deger
		yo = 146
		self._Btn("adim_eksi", 722, yo + 32, lambda: self.__RangeStep(-RANGE_STEP))
		self.track = self._Img("track.png", 760, yo + 44)
		self.trackFill = self._Img("track_fill.png", 760, yo + 44)
		self.knob = self._Img("knob.png", 760, yo + 37)
		self._HitBox(756, yo + 30, 128, 34, onDown=ui.__mem_func__(self.__RangeDragBegin))
		self._Btn("adim_arti", 886, yo + 32, lambda: self.__RangeStep(RANGE_STEP))
		self.rangeTxt = self._Txt("", 944, yo + 47, 15, C_GOLD2, "right")
		self._Btn("kapat_ayar", 658, 522, ui.__mem_func__(self.__AllOff))

		# alt cubuk
		self.infoTxt = self._Txt("Ayarlar bu karakter i\xe7in saklan\xfdr", 20, 602, 14, C_MUTED)
		self._Btn("kaydet", 678, 577, ui.__mem_func__(self.SaveAutoInfo))
		self.startBtn = self._Btn("baslat", 790, 577, ui.__mem_func__(self.__OnStartButton))
		self.stopBtn = self._Btn("durdur", 790, 577, ui.__mem_func__(self.__OnStartButton))
		self.stopBtn.Hide()

		self.__BuildPicker()
		self.__BuildTargets()
		self.__BuildKeypad()
		self.helpImg = self._Img("yardim.png", 646, 66, pick=True)
		self.helpImg.Hide()
		self.toastImg = self._Img("toast.png", 300, 66)
		self.toastTxt = self._Txt("", 520, 86, 15, C_TEXT, "center")
		self.toastImg.Hide()
		self.toastTxt.Hide()
		self.built = True

	def __BuildPicker(self):
		p = self._Panel(1, HEAD_H + 1, LEFT_W - 1, FOOT_Y - HEAD_H - 1)
		self.picker = p
		ox, oy = 1, HEAD_H + 1		# panel ic koordinati = pencere - (ox, oy)
		self._HitBox(0, 0, LEFT_W - 1, FOOT_Y - HEAD_H - 1, parent=p)	# arkadaki kutulara dokunma gecmesin
		self._PanelZemin(p, 639, 506)		# DOSEME (eski panel_sol.png)
		self._Btn("kare", 20 - ox, 74 - oy, ui.__mem_func__(self.__ClosePicker), parent=p)
		self._Txt("<", 41 - ox, 94 - oy, 20, C_MUTED, "center", parent=p)
		self.pickTitle = self._Txt("", 74 - ox, 85 - oy, 17, C_GOLD2, parent=p)
		self.pickSub = self._Txt("", 74 - ox, 107 - oy, 14, C_MUTED, parent=p)
		self._Img("sayac.png", 526 - ox, 80 - oy, parent=p)
		self.pickCount = self._Txt("", 574 - ox, 91 - oy, 13, C_MUTED, "center", parent=p)
		self.pgPrev = self._Btn("kare", 430 - ox, 74 - oy, lambda: self.__PickPage(-1), parent=p)
		self.pgPrevT = self._Txt("<", 451 - ox, 94 - oy, 18, C_GOLD, "center", parent=p)
		self.pgNext = self._Btn("kare", 476 - ox, 74 - oy, lambda: self.__PickPage(1), parent=p)
		self.pgNextT = self._Txt(">", 497 - ox, 94 - oy, 18, C_GOLD, "center", parent=p)
		self.cards = []
		for i in range(CARDS_PER_PAGE):
			col = i % 2
			row = i / 2
			x = 20 + col * 306 - ox
			y = 128 + row * 74 - oy
			c = {}
			c["off"] = self._ImgBtn("card.png", x, y, lambda n=i: self.__OnCard(n), parent=p)
			c["on"] = self._ImgBtn("card_on.png", x, y, lambda n=i: self.__OnCard(n), parent=p)
			icon = ui.ExpandedImageBox()
			icon.SetParent(p)
			icon.AddFlag("not_pick")
			self.keep.append(icon)
			c["icon"] = icon
			c["iconXY"] = (x + 38, y + 32)
			c["name"] = self._Txt("", x + 74, y + 22, 15, C_TEXT, parent=p)
			c["sub"] = self._Txt("", x + 74, y + 43, 14, C_MUTED, parent=p)
			c["plus"] = self._Img("mark_plus.png", x + 260, y + 19, parent=p)
			c["ok"] = self._Img("mark_ok.png", x + 260, y + 19, parent=p)
			self.cards.append(c)
		self.pickEmpty = self._Txt("", 320 - ox, 300 - oy, 14, C_MUTED, "center", parent=p)
		self._Txt("Ekli olana tekrar dokunursan kutudan \xe7\xfdkar", 20 - ox, 520 - oy, 14, C_MUTED, parent=p)
		self._Btn("bitti", 462 - ox, 500 - oy, ui.__mem_func__(self.__ClosePicker), parent=p)
		p.Hide()

	def __BuildTargets(self):
		ox, oy = LEFT_W + 1, HEAD_H + 1
		p = self._Panel(ox, oy, REF_W - LEFT_W - 2, FOOT_Y - HEAD_H - 1)
		self.targetsPanel = p
		self._HitBox(0, 0, REF_W - LEFT_W - 2, FOOT_Y - HEAD_H - 1, parent=p)
		self._PanelZemin(p, 399, 506)		# DOSEME (eski panel_sag.png)
		self._Btn("kare", 658 - ox, 74 - oy, ui.__mem_func__(self.__CloseTargets), parent=p)
		self._Txt("<", 679 - ox, 94 - oy, 20, C_MUTED, "center", parent=p)
		self._Txt("Sald\xfdr\xfd Hedefleri", 712 - ox, 95 - oy, 16, C_GOLD2, parent=p)
		self._Txt("Seviye aral\xfd\xf0\xfd", 658 - ox, 133 - oy, 14, C_MUTED, parent=p)
		for j, (x, key) in enumerate(((658, "min"), (845, "max"))):
			self._Img("stepper.png", x - ox, 146 - oy, parent=p)
			self._HitBox(x - ox, 146 - oy, 38, 40, onUp=lambda kk=key: self.__LevelStep(kk, -1), parent=p)
			self._HitBox(x + 139 - ox, 146 - oy, 38, 40, onUp=lambda kk=key: self.__LevelStep(kk, 1), parent=p)
			self._Txt(key == "min" and "En az" or "En \xe7ok", x + 88 - ox, 156 - oy, 11, C_MUTED, "center", parent=p)
		self.lvMinTxt = self._Txt("", 746 - ox, 174 - oy, 16, C_TEXT, "center", parent=p)
		self.lvMaxTxt = self._Txt("", 933 - ox, 174 - oy, 16, C_TEXT, "center", parent=p)
		self._Txt("Sald\xfdr\xfdlacak t\xfcrler", 658 - ox, 207 - oy, 14, C_MUTED, parent=p)
		self.chips = []
		for i, name in enumerate(TARGET_NAMES):
			x = 658 + (i % 2) * 187
			y = 220 + (i / 2) * 48
			off = self._ImgBtn("chip_off.png", x - ox, y - oy, lambda n=i: self.__ToggleTarget(n), parent=p)
			on = self._ImgBtn("chip_on.png", x - ox, y - oy, lambda n=i: self.__ToggleTarget(n), parent=p)
			t = self._Txt(name, x + 42 - ox, y + 20 - oy, 14, C_TEXT, parent=p)
			self.chips.append((on, off, t))
		self._Btn("sifirla", 658 - ox, 510 - oy, ui.__mem_func__(self.__ResetTargets), parent=p)
		self._Btn("onayla", 845 - ox, 510 - oy, ui.__mem_func__(self.__AcceptTargets), parent=p)
		p.Hide()

	def __BuildKeypad(self):
		p = self._Panel(0, 0, 220, 268)
		self.keypad = p
		self._Img("balon.png", 0, 0, parent=p, pick=True)
		self.kpTitle = self._Txt("", 12, 22, 13, C_MUTED, parent=p)
		self.kpShow = self._Txt("0", 196, 58, 20, C_TEXT, "right", parent=p)
		keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "<", "0", "OK"]
		for i, kx in enumerate(keys):
			x = 12 + (i % 3) * 68
			y = 88 + (i / 3) * 44
			if kx == "OK":
				self._Btn("key_ok", x, y, ui.__mem_func__(self.__KeypadOk), parent=p)
			else:
				self._Btn("key", x, y, lambda c=kx: self.__KeypadKey(c), parent=p)
				self._Txt(kx == "<" and "Sil" or kx, x + 32, y + 19, kx == "<" and 13 or 17, C_TEXT, "center", parent=p)
		p.Hide()

	# ------------------------------------------------------------------ acma / kapama
	def LoadAutoWindow(self):
		pass

	def Show(self):
		if not self.built:
			self.__Build()
		self.__LoadForCharacter()
		self.__NoStones()
		self.__ApplyFlagsToNative()
		self.RefreshAutoSkillSlot()
		self.RefreshAutoPositionSlot()
		self.__RefreshFlags()
		self.__RefreshRange()
		self.__RefreshTargetSummary()
		self.__RefreshRunState()
		self.picker.Hide()
		self.targetsPanel.Hide()
		self.keypad.Hide()
		self.helpImg.Hide()
		ui.Window.Show(self)
		self.SetTop()

	def Close(self):
		self.__HideTip()
		if self.built:
			self.keypad.Hide()
			self.helpImg.Hide()
			self.__SetValSel(-1)
		self.dragging = False
		self.rangeFxUntil = 0.0
		try:
			player.SetAutoHuntRangeEffect(0)
		except:
			pass
		self.Hide()

	def OnPressEscapeKey(self):
		if self.built and self.keypad.IsShow():
			self.keypad.Hide()
			self.__SetValSel(-1)
			return True
		if self.built and self.picker.IsShow():
			self.picker.Hide()
			return True
		if self.built and self.targetsPanel.IsShow():
			self.targetsPanel.Hide()
			return True
		self.Close()
		return True

	def Destroy(self):
		self.Close()
		try:
			constInfo.wndAuto = None
		except:
			pass
		self.keep = []
		self.built = False

	def SetCloseGame(self):
		if self.autostartonoff:
			self.__Stop()

	# ------------------------------------------------------------------ disaridan cagrilanlar
	def SetSkillToolTip(self, tooltip):
		self.tooltipSkill = tooltip

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def GetAutoStartonoff(self):
		return self.autostartonoff

	def IsAutoRestartOn(self):
		if self.autoRestartOn:
			return True
		try:
			return bool(player.GetAutoRestart())
		except:
			return False

	def AutoOnOff(self, onoff, type, number=0, command=False):
		"""eski pencerenin arayuzu: game.py AutoException / interfacemodule AutoOff cagirir"""
		if type == self.AUTO_ONOFF_START:
			if onoff:
				self.__Start()
			else:
				self.__Stop()
			if command and not onoff:
				self.Close()
			return
		key = {self.AUTO_ONOFF_ATTACK: "saldir", self.AUTO_ONOFF_SKILL: "beceri", self.AUTO_ONOFF_POSITION: "iksir",
			self.AUTO_ONOFF_AUTO_RANGE: "odak", self.AUTO_ONOFF_AUTO_RESTART: "canlan"}.get(type)
		if key:
			self.flags[key] = bool(onoff)
			self.__ApplyFlagsToNative()
			if self.built:
				self.__RefreshFlags()

	def SetAutoCooltime(self, slotindex, cooltime):
		try:
			cooltime = float(cooltime)
		except:
			cooltime = 0.0
		if cooltime > 0:
			self.cd[slotindex] = (app.GetTime(), cooltime)
		elif slotindex in self.cd:
			del self.cd[slotindex]

	def OnUseSkill(self, slotindex, coolTime):
		if self.IsShow():
			self.RefreshAutoSkillSlot()

	def OnActivateSkill(self):
		if self.IsShow():
			self.RefreshAutoSkillSlot()

	def OnDeactivateSkill(self, slotindex):
		if self.IsShow():
			self.RefreshAutoSkillSlot()

	# ------------------------------------------------------------------ kutular
	def RefreshAutoSkillSlot(self):
		if not self.built:
			return
		for slot in range(SKILL_MAX):
			pos = player.GetAutoSlotIndex(slot)
			sidx = pos and player.GetSkillIndex(pos) or 0
			if not sidx:
				self.__SetSlotEmpty(slot)
				continue
			try:
				if skill.GetSkillType(sidx) == skill.SKILL_TYPE_GUILD:
					grade = 0
				else:
					grade = player.GetSkillGrade(pos)
			except:
				grade = 0
			self.__SetSlotIcon(slot, _SkillIconFile(sidx, grade), 54.0, 32)
			self.slotPos[slot] = pos
			self.slotW[slot]["cnt"].SetText("")
			self.__SetSlotValue(slot, player.GetAutoSlotCoolTime(slot), "sn")
		self.__RefreshCounts()

	## KULLANICI (2026-10-02): "ic ice 2000 adet olsun, otoava ekleyince tek tek kullansin suresi bittikce" - motor bir yigin
	## bitince kutuyu bosaltiyordu (ayni esyanin diger yiginlarina gecmiyordu) ve Sebnem'i suresi ne olursa olsun 600 sn'de bir
	## kullaniyordu (60 sn'lik Sebnem 9 dk etkisiz kaliyordu). Kutu, yigin bitince ayni esyanin BASKA yiginina gecer; Sebnem
	## araligi kendi suresi + 2 sn (sunucu etki surerken yenisini REDDEDER ve harcamaz -> guvenli).
	def __Remember(self, slot):
		pos = player.GetAutoSlotIndex(slot)
		v = pos and player.GetItemIndex(pos) or 0
		if v:
			self.slotVnum[slot] = v
			self.__ApplyBlendInterval(slot)

	def __ApplyBlendInterval(self, slot):
		pos = player.GetAutoSlotIndex(slot)
		v = pos and player.GetItemIndex(pos) or 0
		if not v:
			return
		try:
			item.SelectItem(v)
			if item.GetItemType() != item.ITEM_TYPE_BLEND:
				return
			sure = int(player.GetItemMetinSocket(pos, 2))
		except:
			return
		if sure > 0:
			player.SetAutoSlotCoolTime(slot, sure + 2)

	def __FindStack(self, vnum, used):
		"""ayni esyanin kullanilmayan bir yigini: >0 hucre, yoksa 0 (yalniz ilk hucrede), hic yoksa -1"""
		try:
			count = int(player.INVENTORY_PAGE_SIZE) * int(player.INVENTORY_PAGE_COUNT)
		except:
			count = 192
		ilk = -1
		for p in range(count):
			if p in used or player.GetItemIndex(p) != vnum:
				continue
			if p == 0:
				ilk = 0
				continue
			return p
		return ilk

	def __Refill(self, slot):
		v = self.slotVnum.get(slot)
		if not v:
			return False
		used = {}
		for s in range(POS_START, POS_END):
			if s != slot:
				used[player.GetAutoSlotIndex(s)] = 1
		p = self.__FindStack(v, used)
		if p > 0:
			player.SetAutoPositionSlotIndex(slot, p)
			if player.GetAutoSlotIndex(slot) == p:
				self.__ApplyBlendInterval(slot)
				return True
			return False
		if p == 0 and not self.pendMove:
			try:
				item.SelectItem(v)
				name = item.GetItemName()
			except:
				name = ""
			self.__MoveFromFirstCell(slot, {"vnum": v, "name": name})
			return True
		return False

	def AutoTick(self, t):
		"""game.py OnUpdate'ten saniyede bir (pencere kapaliyken de): biten yigini ayni esyanin diger yiginiyla degistir."""
		if not self.built or not self.slotVnum:
			return
		self.__PendMoveTick(t)
		for slot in range(POS_START, POS_END):
			want = self.slotVnum.get(slot)
			if not want:
				continue
			pos = player.GetAutoSlotIndex(slot)
			if not pos or player.GetItemIndex(pos) != want:
				self.RefreshAutoPositionSlot()
				return

	def RefreshAutoPositionSlot(self):
		if not self.built:
			return
		for slot in range(POS_START, POS_END):
			pos = player.GetAutoSlotIndex(slot)
			vnum = pos and player.GetItemIndex(pos) or 0
			want = self.slotVnum.get(slot)
			if want and vnum != want:		# yigin bitti / yer degisti -> ayni esyanin baska yigini
				if self.__Refill(slot):
					pos = player.GetAutoSlotIndex(slot)
					vnum = pos and player.GetItemIndex(pos) or 0
				elif not (self.pendMove and self.pendMove.get("slot") == slot):
					self.slotVnum.pop(slot, None)		# hic kalmadi
			if not vnum:
				if pos:
					player.SetAutoPositionSlotIndex(slot, 0)
				self.__SetSlotEmpty(slot)
				continue
			self.__SetSlotIcon(slot, _ItemIconFile(vnum), 44.0, _ItemIconWH(vnum))
			self.slotPos[slot] = pos
			n = player.GetItemCount(pos)
			self.slotW[slot]["cnt"].SetText(n > 1 and ("%d" % n) or "")
			self.__SetSlotValue(slot, player.GetAutoSlotCoolTime(slot), _IsPercentPotion(vnum) and "%" or "sn")
		self.__RefreshCounts()

	def __SetSlotEmpty(self, slot):
		d = self.slotW[slot]
		self.slotPos[slot] = 0
		d["empty"].Show()
		d["full"].Hide()
		d["run"].Hide()
		d["icon"].Hide()
		self.slotIcon[slot] = ""
		d["cnt"].SetText("")
		d["valTxt"].SetText("-")
		d["valTxt"].SetPackedFontColor(C_DIM)
		if slot in self.cd:
			del self.cd[slot]
		d["cd"].Hide()
		d["cdTxt"].SetText("")

	def __SetSlotIcon(self, slot, fname, size, fixed=0):
		d = self.slotW[slot]
		d["empty"].Hide()
		if self.autostartonoff:
			d["run"].Show()
			d["full"].Hide()
		else:
			d["full"].Show()
			d["run"].Hide()
		icon = d["icon"]
		if fname and self.slotIcon.get(slot) != fname and _FileExists(fname):
			try:
				icon.LoadImage(fname)
				self.slotIcon[slot] = fname
			except:
				self.slotIcon[slot] = ""
		if not self.slotIcon.get(slot):
			icon.Hide()
			return
		if isinstance(fixed, tuple):
			(iw, ih) = fixed	# esya: hucre olcusu (HD ikonda GetWidth guvenilmez)
		elif fixed:
			iw = ih = fixed	# HD .sub (density 4): GetWidth ilk yuklemede 128 donebiliyor
		else:
			iw = max(1, icon.GetWidth())
			ih = max(1, icon.GetHeight())
		s = size * self.k / float(max(iw, ih))
		icon.SetScale(s, s)
		(cx, cy) = d["iconXY"]
		icon.SetPosition(int(round(cx * self.k - iw * s / 2.0)), int(round(cy * self.k - ih * s / 2.0)))
		icon.Show()

	def __SetSlotValue(self, slot, value, unit):
		d = self.slotW[slot]
		try:
			v = int(value)
		except:
			v = 0
		d["valTxt"].SetText(v and ("%d %s" % (v, unit)) or "-")
		d["valTxt"].SetPackedFontColor(v and C_TEXT or C_DIM)
		d["unit"] = unit

	def __RefreshCounts(self):
		nb = len([s for s in range(SKILL_MAX) if self.slotPos.get(s)])
		ni = len([s for s in range(POS_START, POS_END) if self.slotPos.get(s)])
		self.countB.SetText("%d / 12" % nb)
		self.countI.SetText("%d / 12" % ni)

	def __OnSlotTap(self, slot):
		self.__HidePopups()
		if mouseModule.mouseController.isAttached():
			if self.autostartonoff:
				self.__Toast("Av s\xfcrerken kutular de\xf0i\xfetirilemez")
				mouseModule.mouseController.DeattachObject()
				return
			self.__AddFromMouse(slot)
			return
		if not self.slotPos.get(slot):
			self.__OpenPicker(slot < SKILL_MAX and "B" or "I", slot)
			return
		self.__ShowTip(slot)

	def __AddFromMouse(self, slot):
		"""eski AddAutoSlot: beceri penceresinden / envanterden surukleyip birakma"""
		t = mouseModule.mouseController.GetAttachedType()
		num = mouseModule.mouseController.GetAttachedSlotNumber()
		if slot < SKILL_MAX:
			if player.SLOT_TYPE_SKILL == t:
				self.__PutSkill(slot, num)
		else:
			if player.SLOT_TYPE_INVENTORY == t:
				vnum = player.GetItemIndex(num)
				if _IsAutoItem(vnum):
					self.__PutItem(slot, num)
				else:
					self.__Toast("Bu e\xfeya otomatik ava eklenemez")
		mouseModule.mouseController.DeattachObject()

	def __PutSkill(self, slot, pos):
		for s in range(SKILL_MAX):		# ayni beceri iki kez -> motor TUM beceri kutularini siler
			if s != slot and player.GetAutoSlotIndex(s) == pos:
				player.SetAutoSkillSlotIndex(s, 0)
		player.SetAutoSkillSlotIndex(slot, pos)
		ok = player.GetAutoSlotIndex(slot) == pos
		self.RefreshAutoSkillSlot()
		if not ok:
			self.__Toast("Bu beceri otomatik ava eklenemez")
		return ok

	def __PutItem(self, slot, pos):
		## hucre 0 motor icin "bos": eskiden 0 == 0 diye BASARILI sayilip "eklendi" yaziyordu (KULLANICI 2026-10-02)
		if not pos:
			return False
		player.SetAutoPositionSlotIndex(slot, pos)
		ok = player.GetAutoSlotIndex(slot) == pos
		if ok:
			self.__Remember(slot)
		self.RefreshAutoPositionSlot()
		return ok

	def __FreeInvCell(self, vnum):
		"""iksirin tasinabilecegi bos envanter hucresi (0 haric). Uzun esyanin kapladigi alt hucreler dolu sayilir."""
		try:
			page = int(player.INVENTORY_PAGE_SIZE)
			count = page * int(player.INVENTORY_PAGE_COUNT)
		except:
			page, count = 48, 192
		cols = 6		# mobil envanter 6 sutun (INVENTORY_PAGE_SIZE 48 = 6 x 8)
		for p in range(1, count):
			if player.GetItemIndex(p):
				continue
			dolu = False
			for k in (1, 2):
				q = p - cols * k
				if q < (p // page) * page:
					break
				v = player.GetItemIndex(q)
				if v:
					try:
						item.SelectItem(v)
						h = item.GetItemSize()[1]
					except:
						h = 1
					if h > k:
						dolu = True
					break
			if not dolu:
				return p
		return -1

	def __MoveFromFirstCell(self, slot, d):
		"""iksir yalniz ilk hucrede (0): bos bir hucreye tasi, tasima bitince (OnUpdate) kutuya ekle."""
		dst = self.__FreeInvCell(d["vnum"])
		if dst < 0:
			self.__Toast("Envanterde bo\xfe yer yok: iksiri ilk kutudan ba\xfeka yere ta\xfe\xfd")
			return
		try:
			net.SendItemMovePacket(0, dst, player.GetItemCount(0))
		except:
			self.__Toast("\xddksir ta\xfe\xfdnamad\xfd")
			return
		self.pendMove = {"vnum": d["vnum"], "dst": dst, "slot": slot, "name": d["name"], "t": app.GetTime()}
		self.__Toast("\xddksir yerle\xfetiriliyor...")

	def __PendMoveTick(self, t):
		pm = self.pendMove
		if not pm:
			return
		if player.GetItemIndex(pm["dst"]) == pm["vnum"]:
			self.pendMove = None
			cur = player.GetAutoSlotIndex(pm["slot"])
			if cur and cur != pm["dst"] and player.GetItemIndex(cur):		# kutuyu baska bir esya almis
				pm["slot"] = self.__FreeSlot(range(POS_START, POS_END))
			if pm["slot"] >= 0 and self.__PutItem(pm["slot"], pm["dst"]):
				self.__Toast("%s eklendi" % pm["name"])
			else:
				self.__Toast("Bu e\xfeya otomatik ava eklenemez")
			if self.picker.IsShow():
				self.__CollectPickData()
				self.__RefreshPicker()
		elif t - pm["t"] > 3.0:
			self.pendMove = None
			self.__Toast("\xddksir yerle\xfetirilemedi, tekrar dene")

	def __ClearSkills(self):
		if self.autostartonoff:
			self.__Toast("Av s\xfcrerken kutular de\xf0i\xfetirilemez")
			return
		player.ClearAutoSKillSlot()
		self.RefreshAutoSkillSlot()

	def __ClearPotions(self):
		if self.autostartonoff:
			self.__Toast("Av s\xfcrerken kutular de\xf0i\xfetirilemez")
			return
		player.ClearAutoPositionSlot()
		self.slotVnum = {}
		self.RefreshAutoPositionSlot()

	# ------------------------------------------------------------------ ipucu
	def __ShowTip(self, slot):
		self.__HideTip()
		pos = self.slotPos.get(slot)
		if not pos:
			return
		try:
			if slot < SKILL_MAX:
				if not self.tooltipSkill:
					return
				sidx = player.GetSkillIndex(pos)
				if skill.GetSkillType(sidx) == skill.SKILL_TYPE_GUILD:
					grade = 0
					level = guild.GetSkillLevel(pos)
				else:
					grade = player.GetSkillGrade(pos)
					level = player.GetSkillLevel(pos)
				self.tooltipSkill.SetSkillNew(pos, sidx, grade, level)
			else:
				if not self.tooltipItem:
					return
				self.tooltipItem.SetInventoryItem(pos)
			self.tipShown = True
		except:
			pass

	def __HideTip(self):
		if not self.tipShown:
			return
		self.tipShown = False
		for t in (self.tooltipSkill, self.tooltipItem):
			if t:
				try:
					t.HideToolTip()
				except:
					pass

	# ------------------------------------------------------------------ secici (+ Ekle)
	def __OpenPicker(self, t, slot):
		self.__HidePopups()
		if self.autostartonoff:
			self.__Toast("Av s\xfcrerken kutular de\xf0i\xfetirilemez")
			return
		self.targetsPanel.Hide()
		self.pickType = t
		self.pickTarget = slot
		self.pickPage = 0
		if t == "B":
			self.pickTitle.SetText("Beceri Ekle")
			self.pickSub.SetText("\xd6\xf0rendi\xf0in aktif beceriler \xb7 dokun, bo\xfe kutuya eklensin")
		else:
			self.pickTitle.SetText("\xddksir Ekle")
			self.pickSub.SetText("Envanterindeki iksirler \xb7 dokun, bo\xfe kutuya eklensin")
		self.__CollectPickData()
		self.__RefreshPicker()
		self.picker.Show()
		self.picker.SetTop()

	def __ClosePicker(self):
		self.picker.Hide()

	def __CollectPickData(self):
		data = []
		if self.pickType == "B":
			seen = {}
			try:
				count = player.SKILL_SLOT_COUNT
			except:
				count = 255
			for pos in range(1, count):
				try:
					sidx = player.GetSkillIndex(pos)
				except:
					continue
				if not sidx or sidx in seen:
					continue
				try:
					if player.GetSkillLevel(pos) <= 0 or not skill.CanUseSkill(sidx):
						continue
					if skill.GetSkillType(sidx) != skill.SKILL_TYPE_ACTIVE:
						continue
					grade = player.GetSkillGrade(pos)
					level = player.GetSkillLevel(pos)
					name = skill.GetSkillName(sidx)
				except:
					continue
				seen[sidx] = 1
				data.append({"pos": pos, "icon": _SkillIconFile(sidx, grade), "name": name,
					"sub": "Seviye %s" % _SkillLevelText(grade, level), "size": 52.0, "fixed": 32})
		else:
			seen = {}
			try:
				count = player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
			except:
				count = 180
			for pos in range(count):
				vnum = player.GetItemIndex(pos)
				if not vnum:
					continue
				n = player.GetItemCount(pos)
				if vnum in seen:
					seen[vnum]["n"] += n
					## KULLANICI (2026-10-02): "listede gorunuyor, eklendi yaziyor ama eklenmiyor" - motor oto av kutusunda
					## 0'i BOS sayar (CPythonPlayer::SetAutoPositionSlotIndex: dwIndex == 0 -> return) -> envanterin ILK
					## hucresi (0) eklenemez. Ayni iksirin baska yigini varsa onu kullan.
					if seen[vnum]["pos"] == 0:
						seen[vnum]["pos"] = pos
					continue
				if not _IsAutoItem(vnum):
					continue
				try:
					item.SelectItem(vnum)
					name = item.GetItemName()
				except:
					name = ""
				d = {"pos": pos, "vnum": vnum, "icon": _ItemIconFile(vnum), "name": name, "n": n, "size": 40.0, "fixed": _ItemIconWH(vnum)}
				seen[vnum] = d
				data.append(d)
			for d in data:
				d["sub"] = "%d adet" % d["n"]
		self.pickData = data

	def __IsPicked(self, d):
		if self.pickType == "B":
			rng = range(SKILL_MAX)
			return len([s for s in rng if player.GetAutoSlotIndex(s) == d["pos"]]) > 0
		for s in range(POS_START, POS_END):
			p = player.GetAutoSlotIndex(s)
			if p and player.GetItemIndex(p) == d["vnum"]:
				return True
		return False

	def __RefreshPicker(self):
		data = self.pickData
		pages = max(1, (len(data) + CARDS_PER_PAGE - 1) / CARDS_PER_PAGE)
		self.pickPage = max(0, min(self.pickPage, pages - 1))
		start = self.pickPage * CARDS_PER_PAGE
		for i, c in enumerate(self.cards):
			j = start + i
			if j >= len(data):
				for n in ("off", "on", "icon", "name", "sub", "plus", "ok"):
					c[n].Hide()
				continue
			d = data[j]
			picked = self.__IsPicked(d)
			(c["on"] if picked else c["off"]).Show()
			(c["off"] if picked else c["on"]).Hide()
			(c["ok"] if picked else c["plus"]).Show()
			(c["plus"] if picked else c["ok"]).Hide()
			c["name"].SetText(d["name"])
			c["name"].Show()
			c["sub"].SetText(d["sub"])
			c["sub"].Show()
			icon = c["icon"]
			if not _FileExists(d["icon"]):
				icon.Hide()
				c["file"] = ""
				continue
			try:
				if c.get("file") != d["icon"]:		# takilma: ayni ikon her yenilemede yeniden yuklenmesin
					c["file"] = ""
					icon.LoadImage(d["icon"])
					c["file"] = d["icon"]
				fx = d.get("fixed")
				if isinstance(fx, tuple):
					(iw, ih) = fx
				elif fx:
					iw = ih = fx
				else:
					iw = max(1, icon.GetWidth())
					ih = max(1, icon.GetHeight())
				s = d["size"] * self.k / float(max(iw, ih))
				icon.SetScale(s, s)
				(cx, cy) = c["iconXY"]
				icon.SetPosition(int(round(cx * self.k - iw * s / 2.0)), int(round(cy * self.k - ih * s / 2.0)))
				icon.Show()
			except:
				c["file"] = ""
				icon.Hide()
		if not data:
			self.pickEmpty.SetText(self.pickType == "B" and "Kullan\xfdlabilir aktif becerin yok" or "Envanterinde kullan\xfdlabilir iksir yok")
			self.pickEmpty.Show()
		else:
			self.pickEmpty.Hide()
		if self.pickType == "B":
			n = len([s for s in range(SKILL_MAX) if player.GetAutoSlotIndex(s)])
		else:
			n = len([s for s in range(POS_START, POS_END) if player.GetAutoSlotIndex(s)])
		self.pickCount.SetText("%d / 12 dolu" % n)
		for w in (self.pgPrev, self.pgPrevT, self.pgNext, self.pgNextT):
			if pages > 1:
				w.Show()
			else:
				w.Hide()

	def __PickPage(self, delta):
		self.pickPage += delta
		self.__RefreshPicker()

	def __OnCard(self, n):
		j = self.pickPage * CARDS_PER_PAGE + n
		if j >= len(self.pickData):
			return
		d = self.pickData[j]
		if self.pickType == "B":
			rng = range(SKILL_MAX)
			found = [s for s in rng if player.GetAutoSlotIndex(s) == d["pos"]]
			if found:
				for s in found:
					player.SetAutoSkillSlotIndex(s, 0)
				self.RefreshAutoSkillSlot()
				self.__Toast("%s kutudan \xe7\xfdkar\xfdld\xfd" % d["name"])
			else:
				slot = self.__FreeSlot(rng)
				if slot < 0:
					self.__Toast("Bo\xfe kutu kalmad\xfd")
					return
				if self.__PutSkill(slot, d["pos"]):
					self.__Toast("%s eklendi" % d["name"])
		else:
			rng = range(POS_START, POS_END)
			found = [s for s in rng if player.GetAutoSlotIndex(s) and player.GetItemIndex(player.GetAutoSlotIndex(s)) == d["vnum"]]
			if found:
				for s in found:
					player.SetAutoPositionSlotIndex(s, 0)
					self.slotVnum.pop(s, None)
				self.RefreshAutoPositionSlot()
				self.__Toast("%s kutudan \xe7\xfdkar\xfdld\xfd" % d["name"])
			else:
				slot = self.__FreeSlot(rng)
				if slot < 0:
					self.__Toast("Bo\xfe kutu kalmad\xfd")
					return
				if not d["pos"]:
					self.__MoveFromFirstCell(slot, d)
				elif self.__PutItem(slot, d["pos"]):
					self.__Toast("%s eklendi" % d["name"])
				else:
					self.__Toast("Bu e\xfeya otomatik ava eklenemez")
		self.pickTarget = -1
		self.__RefreshPicker()

	def __FreeSlot(self, rng):
		if self.pickTarget in rng and not player.GetAutoSlotIndex(self.pickTarget):
			return self.pickTarget
		for s in rng:
			if not player.GetAutoSlotIndex(s):
				return s
		return -1

	# ------------------------------------------------------------------ sure / yuzde tus takimi
	def __OpenKeypad(self, slot):
		self.__HideTip()
		if self.autostartonoff:
			self.__Toast("Av s\xfcrerken s\xfcreler de\xf0i\xfetirilemez")
			return
		if not self.slotPos.get(slot):
			self.__OpenPicker(slot < SKILL_MAX and "B" or "I", slot)
			return
		self.helpImg.Hide()
		self.editSlot = slot
		self.typed = ""
		unit = self.slotW[slot].get("unit", "sn")
		self.kpTitle.SetText(unit == "%" and "Can/mana \xfeu y\xfczdenin alt\xfdna d\xfc\xfe\xfcnce" or "Kullan\xfdm aral\xfd\xf0\xfd (saniye)")
		self.kpShow.SetText("%d" % int(player.GetAutoSlotCoolTime(slot)))
		self.__SetValSel(slot)
		# balon kutunun ustunde (yer yoksa altinda)
		(cx, sy) = self.slotW[slot]["iconXY"]
		x = max(8, min(REF_W - 228, cx - 110))
		y = sy - 32 - 268 - 6
		if y < HEAD_H + 4:
			y = sy + 32 + 36
		self.keypad.SetPosition(*self.P(x, y))
		self.keypad.Show()
		self.keypad.SetTop()

	def __SetValSel(self, slot):
		for s, d in self.slotW.items():
			if s == slot:
				d["valSel"].Show()
				d["val"].Hide()
			else:
				d["valSel"].Hide()
				d["val"].Show()

	def __KeypadKey(self, c):
		if c == "<":
			self.typed = self.typed[:-1]
		elif len(self.typed) < 4:
			self.typed += c
		self.kpShow.SetText(self.typed or "0")

	def __KeypadOk(self):
		slot = self.editSlot
		self.keypad.Hide()
		self.__SetValSel(-1)
		if slot < 0 or self.typed == "":
			return
		v = int(self.typed)
		pos = self.slotPos.get(slot)
		if not pos:
			return
		if slot < SKILL_MAX:
			v2 = player.CheckSkillSlotCoolTime(slot, pos, v)
		else:
			v2 = player.CheckPositionSlotCoolTime(slot, pos, v)
		if v2:
			player.SetAutoSlotCoolTime(slot, int(v2))
			if int(v2) != v:
				self.__Toast("En az %d olabilir" % int(v2))
		if slot < SKILL_MAX:
			self.RefreshAutoSkillSlot()
		else:
			self.RefreshAutoPositionSlot()

	# ------------------------------------------------------------------ ayarlar
	def __Toggle(self, key):
		self.__HidePopups()
		self.flags[key] = not self.flags[key]
		self.__ApplyFlagsToNative()
		self.__RefreshFlags()

	def __AllOff(self):
		self.__HidePopups()
		for k in self.flags.keys():
			self.flags[k] = False
		self.__ApplyFlagsToNative()
		self.__RefreshFlags()

	def __NoStones(self):
		try:
			systemSetting.SetAutoHuntStoneFlag(0)	# motor (PythonCharacterManager) tas hedefini yalniz bu bayrakla secer
		except:
			pass

	def __ApplyFlagsToNative(self):
		f = self.flags
		try:
			player.AutoAttackOnOff(f["saldir"] and 1 or 0)
			player.AutoRangeOnOff(f["odak"] and 1 or 0)
			player.AutoPositionOnOff(f["iksir"] and 1 or 0)
			player.AutoSkillOnOff(f["beceri"] and 1 or 0)
			player.SetAutoRestart(f["canlan"] and True or False)
		except:
			pass
		self.autoRestartOn = f["canlan"]

	def __RefreshFlags(self):
		for key, (on, off) in self.rowW.items():
			v = self.flags[key]
			(on if v else off).Show()
			(off if v else on).Hide()
			(swOn, swOff) = self.swW[key]
			(swOn if v else swOff).Show()
			(swOff if v else swOn).Hide()

	# menzil
	def __RangeStep(self, delta):
		self.__HidePopups()
		self.__SetRange(self.range + delta)

	def __SetRange(self, r):
		r = int(max(RANGE_MIN, min(RANGE_MAX, r)))
		r = int(round(r / 100.0)) * 100
		self.range = r
		try:
			player.SetAutoHuntRange(r)
			player.SetAutoHuntRangeEffect(r)
		except:
			pass
		self.rangeFxUntil = app.GetTime() + 2.0
		self.__RefreshRange()

	def __RefreshRange(self):
		t = float(self.range - RANGE_MIN) / float(RANGE_MAX - RANGE_MIN)
		self.trackFill.SetRenderingRect(0.0, 0.0, -1.0 + t, 0.0)
		self.knob.SetPosition(*self.P(760 + 120 * t - 10, 183))
		self.rangeTxt.SetText("%d m" % (self.range / 100))

	def __RangeDragBegin(self):
		self.__HidePopups()
		self.dragging = True
		self.__RangeDragUpdate()

	def __RangeDragUpdate(self):
		try:
			(mx, my) = wndMgr.GetMousePosition()
		except:
			return
		(gx, gy) = self.GetGlobalPosition()
		lx = (mx - gx) / self.k
		t = max(0.0, min(1.0, (lx - 760.0) / 120.0))
		self.__SetRange(RANGE_MIN + (RANGE_MAX - RANGE_MIN) * t)

	# hedefler (seviye + tur)
	def __OpenTargets(self):
		self.__HidePopups()
		self.picker.Hide()
		try:
			self.lvMin = int(systemSetting.GetAutoHuntLevelMin())
			self.lvMax = int(systemSetting.GetAutoHuntLevelMax())
			self.targets = [bool(systemSetting.IsAutoHuntPawn()), bool(systemSetting.IsAutoHuntSPawn()),
				bool(systemSetting.IsAutoHuntKnight()), bool(systemSetting.IsAutoHuntSKnight()),
				bool(systemSetting.IsAutoHuntBoss()), bool(systemSetting.IsAutoHuntKing())]
		except:
			pass
		self.__RefreshTargetsPanel()
		self.targetsPanel.Show()
		self.targetsPanel.SetTop()

	def __CloseTargets(self):
		self.targetsPanel.Hide()

	def __RefreshTargetsPanel(self):
		self.lvMinTxt.SetText("%d" % self.lvMin)
		self.lvMaxTxt.SetText("%d" % self.lvMax)
		for i, (on, off, t) in enumerate(self.chips):
			v = self.targets[i]
			(on if v else off).Show()
			(off if v else on).Hide()
			t.SetPackedFontColor(v and C_TEXT or C_MUTED)

	def __LevelStep(self, key, d):
		if key == "min":
			self.lvMin = max(LEVEL_MIN, min(LEVEL_MAX, self.lvMin + d))
			if self.lvMin > self.lvMax:
				self.lvMax = self.lvMin
		else:
			self.lvMax = max(LEVEL_MIN, min(LEVEL_MAX, self.lvMax + d))
			if self.lvMax < self.lvMin:
				self.lvMin = self.lvMax
		self.__RefreshTargetsPanel()

	def __ToggleTarget(self, n):
		self.targets[n] = not self.targets[n]
		self.__RefreshTargetsPanel()

	def __ResetTargets(self):
		self.lvMin = LEVEL_MIN
		self.lvMax = LEVEL_MAX
		self.targets = [True] * 6
		self.__RefreshTargetsPanel()

	def __AcceptTargets(self):
		try:
			systemSetting.SetAutoHuntLevelMin(self.lvMin)
			systemSetting.SetAutoHuntLevelMax(self.lvMax)
			t = self.targets
			systemSetting.SetAutoHuntPawnFlag(t[0])
			systemSetting.SetAutoHuntSPawnFlag(t[1])
			systemSetting.SetAutoHuntKnightFlag(t[2])
			systemSetting.SetAutoHuntSKnightFlag(t[3])
			systemSetting.SetAutoHuntBossFlag(t[4])
			systemSetting.SetAutoHuntKingFlag(t[5])
			systemSetting.SetAutoHuntStoneFlag(0)
		except:
			pass
		self.targetsPanel.Hide()
		self.__RefreshTargetSummary()

	def __RefreshTargetSummary(self):
		try:
			mn = int(systemSetting.GetAutoHuntLevelMin())
			mx = int(systemSetting.GetAutoHuntLevelMax())
			flags = [systemSetting.IsAutoHuntPawn(), systemSetting.IsAutoHuntSPawn(), systemSetting.IsAutoHuntKnight(),
				systemSetting.IsAutoHuntSKnight(), systemSetting.IsAutoHuntBoss(), systemSetting.IsAutoHuntKing()]
			n = len([f for f in flags if f])
		except:
			mn, mx, n = LEVEL_MIN, LEVEL_MAX, 6
		if mn == 15 and mx == 15:	# motor varsayilani ("hedef yok" tuzagi) -> 1-120
			try:
				systemSetting.SetAutoHuntLevelMin(LEVEL_MIN)
				systemSetting.SetAutoHuntLevelMax(LEVEL_MAX)
				mn, mx = LEVEL_MIN, LEVEL_MAX
			except:
				pass
		self.targetSummary.SetText("Sv. %d\x96%d \xb7 %d t\xfcr" % (mn, mx, n))

	# ------------------------------------------------------------------ baslat / durdur
	def __OnStartButton(self):
		self.__HidePopups()
		if self.autostartonoff:
			self.__Stop()
			self.__Toast("Otomatik av durduruldu")
		else:
			if self.__Start():
				self.__Toast("Otomatik av ba\xfelad\xfd")

	def __Start(self):
		if self.autostartonoff:
			return True
		try:
			if player.CanStartAuto() == False:
				return False
		except:
			pass
		self.__NoStones()
		self.__ApplyFlagsToNative()
		self.__CheckCooltimes()
		player.AutoStartOnOff(1)
		self.autostartonoff = 1
		self.__RefreshRunState()
		return True

	def __Stop(self):
		for s in range(POS_START, POS_END):
			self.SetAutoCooltime(s, 0)
		try:
			player.AutoStartOnOff(0)
		except:
			pass
		self.autostartonoff = 0
		self.__RefreshRunState()

	def __CheckCooltimes(self):
		"""eski SlotKontrol: degerleri motorun alt sinirlarina gore duzelt"""
		for s in range(SKILL_MAX):
			pos = player.GetAutoSlotIndex(s)
			if pos:
				v = player.CheckSkillSlotCoolTime(s, pos, int(player.GetAutoSlotCoolTime(s)))
				if v:
					player.SetAutoSlotCoolTime(s, int(v))
		for s in range(POS_START, POS_END):
			pos = player.GetAutoSlotIndex(s)
			if pos:
				v = player.CheckPositionSlotCoolTime(s, pos, int(player.GetAutoSlotCoolTime(s)))
				if v:
					player.SetAutoSlotCoolTime(s, int(v))
		if self.built:
			self.RefreshAutoSkillSlot()
			self.RefreshAutoPositionSlot()

	def __RefreshRunState(self):
		if not self.built:
			return
		run = bool(self.autostartonoff)
		(self.pillOn if run else self.pillOff).Show()
		(self.pillOff if run else self.pillOn).Hide()
		(self.pulse.Show() if run else self.pulse.Hide())
		(self.stopBtn if run else self.startBtn).Show()
		(self.startBtn if run else self.stopBtn).Hide()
		for s, d in self.slotW.items():
			if self.slotPos.get(s):
				(d["run"] if run else d["full"]).Show()
				(d["full"] if run else d["run"]).Hide()

	# ------------------------------------------------------------------ kayit
	def __ProfilePath(self):
		return "UserData/autohunt/" + str(chr.GetName())

	def __LoadForCharacter(self):
		name = str(chr.GetName())
		if name == "0" or name == self.loadedFor:
			return
		self.loadedFor = name
		self.ReadAutoInfo()
		import os
		path = self.__ProfilePath() + ".ayar"
		if not os.path.exists(path):
			return
		try:
			tok = open(path, "r").read().split()
			keys = ("saldir", "odak", "iksir", "beceri", "canlan")
			for i, k in enumerate(keys):
				self.flags[k] = tok[i] == "1"
			self.__SetRange(int(tok[5]))
			self.rangeFxUntil = 0.0
			player.SetAutoHuntRangeEffect(0)
		except:
			pass

	def ReadAutoInfo(self):
		if str(chr.GetName()) == "0":
			return
		import os
		path = self.__ProfilePath()
		if not os.path.exists(path):
			return
		try:
			tokens = open(path, "r").read().split()
		except:
			return
		for slot in range(len(tokens) // 2):
			try:
				pos = int(tokens[slot * 2])
				val = int(tokens[slot * 2 + 1])
			except:
				break
			if pos and slot != SKILL_MAX:
				if slot < SKILL_MAX:
					player.SetAutoSkillSlotIndex(slot, pos)
				else:
					player.SetAutoPositionSlotIndex(slot, pos)
			player.SetAutoSlotCoolTime(slot, val)
			if pos and slot > SKILL_MAX:
				self.__Remember(slot)		# kayitli kutu: esyayi hatirla, Sebnem araligini kendi suresine cek

	def SaveAutoInfo(self):
		self.__HidePopups()
		if str(chr.GetName()) == "0":
			return
		import os
		if not os.path.exists("UserData/autohunt"):
			try:
				os.makedirs("UserData/autohunt")
			except:
				return
		path = self.__ProfilePath()
		try:
			f = open(path, "w")
			for slot in range(POS_END):
				f.write("%d\n" % int(player.GetAutoSlotIndex(slot)))
				f.write("%d\n" % int(player.GetAutoSlotCoolTime(slot)))
			f.close()
			f = open(path + ".ayar", "w")
			fl = self.flags
			f.write("%d %d %d %d %d %d\n" % (fl["saldir"], fl["odak"], fl["iksir"], fl["beceri"], fl["canlan"], self.range))
			f.close()
		except:
			self.__Toast("Kaydedilemedi")
			return
		if self.built:
			self.infoTxt.SetText("Kaydedildi \xb7 bu karakter i\xe7in sakland\xfd")
		self.__Toast("Ayarlar kaydedildi")

	# ------------------------------------------------------------------ yardimcilar
	def __ToggleHelp(self):
		self.keypad.Hide()
		self.__SetValSel(-1)
		self.__HideTip()
		if self.helpImg.IsShow():
			self.helpImg.Hide()
		else:
			self.helpImg.Show()
			self.helpImg.SetTop()

	def __HidePopups(self):
		self.__HideTip()
		if not self.built:
			return
		self.helpImg.Hide()
		if self.keypad.IsShow():
			self.keypad.Hide()
			self.__SetValSel(-1)

	def __OnBackgroundTap(self):
		self.__HidePopups()

	def __Toast(self, msg):
		if not self.built:
			return
		self.toastTxt.SetText(msg)
		self.toastImg.Show()
		self.toastTxt.Show()
		self.toastImg.SetTop()
		self.toastTxt.SetTop()
		self.toastUntil = app.GetTime() + 1.8

	def OnUpdate(self):
		t = app.GetTime()
		self.__PendMoveTick(t)
		if self.dragging:
			if wndMgr.IsLeftButtonDown():
				self.__RangeDragUpdate()
			else:
				self.dragging = False
		if self.rangeFxUntil and t > self.rangeFxUntil and not self.dragging:
			self.rangeFxUntil = 0.0
			try:
				player.SetAutoHuntRangeEffect(0)
			except:
				pass
		if self.toastUntil and t > self.toastUntil:
			self.toastUntil = 0.0
			self.toastImg.Hide()
			self.toastTxt.Hide()
		if self.autostartonoff:
			a = 0.5 + 0.5 * ((t * 1.4) % 1.0)
			try:
				self.pulse.SetAlpha(1.0 - (a - 0.5) * 2.0)
			except:
				pass
		# bekleme sureleri
		for s, d in self.slotW.items():
			cd = self.cd.get(s)
			if cd and self.slotPos.get(s):
				left = cd[1] - (t - cd[0])
				if left > 0:
					d["cd"].Show()
					if left >= 60:
						d["cdTxt"].SetText("%d dk" % (int(left) / 60 + 1))
					else:
						d["cdTxt"].SetText("%d sn" % (int(left) + 1))
					continue
				del self.cd[s]
			if d["cd"].IsShow():
				d["cd"].Hide()
				d["cdTxt"].SetText("")
