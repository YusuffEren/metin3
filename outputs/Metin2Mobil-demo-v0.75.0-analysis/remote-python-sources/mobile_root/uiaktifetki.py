# MOBIL - mobile_root/uiaktifetki.py: "ETKILER" HUD DUGMESI + "AKTIF ETKILER" PENCERESI.
# URETILIR: tools/aktifetki/uiaktifetki_kaynak.py (UTF-8) -> tools/aktifetki/gen_uiaktifetki.py -> bu dosya (cp1254 kacisli).
#
# KULLANICI (2026-10-01): sol ustteki buff ikon sirasi yerine tek dugme; dokununca aktif etkiler klasik pencerede
#   ("hem de ekranda yer kazaniriz"). Prototip Desktop/Averos2-Buff-Prototip/etkiler.html -> "uygula".
#   Kabuk Dusen Esyalar / Oto Av ile AYNI klasik dokular (tools/aktifetki/bake_aktifetki.py -> mobile/ui/aet/).
# KULLANICI (2026-10-01): "iconlar pixel pixel gozukmesin, net olsun" -> ikonlar HD kaynaklardan (_HdIcon):
#   yeniaffect_icon/<vnum>.png ve affect/<vnum>.tga = esya ikonunun 32 px kopyasi -> icon/item HD (Real-ESRGAN, density 4);
#   beceri/genel etki .sub zaten HD (skill*_hd.png, density 4); at/sevgi -> mobile/ui/aet/ikon/ (4x).
# Veri: pack uiAffectShower.AffectShower ESKISI GIBI calisir (veri deposu) ama GORUNMEZ; bu modul onun affectImageDict'ini
#   okur. Sureler: shower beceri/iksir (bayrak) etkilerinin suresini bilmez -> BINARY_NEW_AddAffect/RemoveAffect
#   sarmalanir, her tur icin bitis zamani + puan/deger burada tutulur.
# "Etkileri goster" oyun secenegi (constInfo.premiumgoster -> game.__premium shower.Show/Hide) artik bu dugmeyi acar/kapar.
# Olcu: tasarim birimi = prototip sahnesi (1568x705); k = ekran yuksekligi / 705; dokular fiziksel (x1220/705) -> IMG_S.

import ui
import wndMgr
import app
import dbg
import player
import chr
import item
import skill
import localeInfo
from _weakref import ref as _wref
try:
	import uiaktifetkitablo		# (puan, deger) -> [(sure, vnum)] (tools/aktifetki/gen_ozut_tablosu.py, sunucu item_proto)
except:
	uiaktifetkitablo = None		# weakref.py telefonun lib'inde olmayabilir; _weakref yerlesik

DIR = "mobile/ui/aet/"
REF_H = 705.0
IMG_S = 705.0 / 1220.0
## DOSEME (KULLANICI 2026-10-01 "her pencereyi hizlandiralim"): zemin pack parcalarindan, tek parca pen_bg yok
PAT = "d:/ymir work/ui/pattern/"
HAS_RRS_W = hasattr(wndMgr, "SetRenderingRectScaled")

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
ZOOM = 1.12			# pencere (bake_aktifetki.py ile AYNI)
FONT_BOOST = 1.15
FONT_MAX = 18			# motor yaziyi en fazla 32 px pisirir; telefonda 18 ustu pikselli (bkz. uihedefkarti)
REFRESH_OPEN = 0.25		# pencere acikken yenileme (sn)
REFRESH_CLOSED = 0.5		# kapaliyken yalniz rozet/uyari
WARN_SEC = 60			# bu kadar sn kala satir kirmizi + dugmede uyari noktasi
INFINITE = 0x1FFFFFFF
MALL_START = 1000

# ---- olculer ----
# INCE PENCERE (KULLANICI 2026-10-04: "cok buyuk, ince kucuk olsun, tasarim ayni, elle kaydirarak asagi gorelim"; prototip
#   Desktop/Averos2-Etkiler-Prototip/etkiler.html "4 satir gorunur" onaylandi): 2 sutun x 5 satir + sayfa oklari yerine
#   TEK sutun, 4 satir gorunur, liste parmakla surukleyerek SATIR SATIR kayar (yazilar kirpilamaz), sagda ince kaydirma cubugu.
WIN_X, WIN_Y = 72, 6
W, H = 428, 404
TITLE_Y, TITLE_H = 8, 34
TITLE_X = 52			# kalin baslik seridi (bake_aktifetki.py TITLE_X ile AYNI)
CHIP_X, CHIP_Y, CHIP_W, CHIP_H = 152, 15, 66, 20
CLOSE_X, CLOSE_Y = W - 35, 12.5
TAB_X, TAB_Y, TAB_W, TAB_H, TAB_GAP = 18, 50, 112, 28, 6
MAX_TABS = 5
LIST = (14, 86, 400, 278)
ROW_XS = (19,)
ROW_Y0, ROW_W, ROW_H, ROW_GAP = 92, 373, 62, 6
ROWS = 4
PER_PAGE = ROWS * len(ROW_XS)
SB_X, SB_Y, SB_W, SB_H = 400, 92, 8, 266	# kaydirma cubugu (iz); tutamak icinde 2 px payla
ICON = 40
BAR_W, BAR_H = 86, 8
FOOT_Y = 384
# HUD (zoom 1.0)
# KULLANICI (2026-10-05): "Etkiler butonu cok buyuk, Cark butonlarinin boyutuna getir, az sag a yaklastir, cok kosede"
#   -> 52 -> 46 (Cark / Etkinlik / Ejder dugmeleri 46 px), sol kenardan 12 -> 28; merkez yuksekligi ayni kalir (8 + 26 = 11 + 23).
HUD_X, HUD_Y, HUD = 28, 11, 46
HUD_DOKU = 52.0			# hud_*.png 90 px x IMG_S = 52 tasarim px
BADGE, WARN = 22, 20

# ---- renkler ----
C_WHITE = 0xffffffff
C_CREAM = 0xfff1e6c0
C_SUB = 0xffc9b88f
C_OFF = 0xff8f8470
C_GOLD = 0xffe8d08a
C_RED = 0xffff8a72
C_DARK = 0xff1b1206
C_LABEL = 0xfff1e6c8
KINDS = (
	("iksir", "\xddksir", 0xff6fb0e6),
	("beceri", "Beceri", 0xffe2826a),
	("premium", "Premium", 0xffe2b95f),
	("diger", "Di\xf0er", 0xff8d7d62),
)
KIND_COLOR = dict([(x[0], x[2]) for x in KINDS])


def _C(name, default=None):
	return getattr(chr, name, default)


# yeni (sureli) etkiler: Turkce ad + tur
NEW_INFO = (
	("NEW_AFFECT_EXP_BONUS", "Deneyim Bonusu", "premium"),
	("NEW_AFFECT_ITEM_BONUS", "E\xfeya D\xfc\xfe\xfcrme Bonusu", "premium"),
	("NEW_AFFECT_SAFEBOX", "Depo Geni\xfeletme", "premium"),
	("NEW_AFFECT_AUTOLOOT", "Otomatik Toplama", "premium"),
	("NEW_AFFECT_FISH_MIND", "Bal\xfdk\xe7\xfd Zihni", "premium"),
	("NEW_AFFECT_MARRIAGE_FAST", "Evlilik H\xfdzland\xfdrma", "premium"),
	("NEW_AFFECT_GOLD_BONUS", "Yang Bonusu", "premium"),
	("NEW_AFFECT_NO_DEATH_PENALTY", "\xd6l\xfcm Cezas\xfd Korumas\xfd", "premium"),
	("NEW_AFFECT_SKILL_BOOK_BONUS", "Beceri Kitab\xfd Bonusu", "premium"),
	("NEW_AFFECT_SKILL_BOOK_NO_DELAY", "Kitap Bekleme S\xfcresi Yok", "premium"),
	("NEW_AFFECT_AUTO_HP_RECOVERY", "Otomatik HP \xddksiri", "premium"),
	("NEW_AFFECT_AUTO_SP_RECOVERY", "Otomatik SP \xddksiri", "premium"),
	("NEW_AFFECT_DRAGON_SOUL_DECK1", "Simya Tak\xfdm\xfd I", "diger"),
	("NEW_AFFECT_DRAGON_SOUL_DECK2", "Simya Tak\xfdm\xfd II", "diger"),
)
# beceri olmayan bayrak etkileri (game.SetAffect): ad + tur; iksirlerin suresi puandan bulunur
FLAG_INFO = (
	("AFFECT_ATT_SPEED_POTION", "Sald\xfdr\xfd H\xfdz\xfd", "iksir"),
	("AFFECT_MOV_SPEED_POTION", "Hareket H\xfdz\xfd", "iksir"),
	("AFFECT_POISON", "Zehir", "diger"),
	("AFFECT_SLOW", "Yava\xfelama", "diger"),
	("AFFECT_STUN", "Sersemleme", "diger"),
	("AFFECT_FISH_MIND", "Bal\xfdk\xe7\xfd Zihni", "diger"),
	("AFFECT_CHINA_FIREWORK", "G\xfc\xe7l\xfc Vuru\xfe", "diger"),
)
# puan adlari (beceri/iksir etkisinin ikinci satiri). (oznitelik adlari, varsayilan EPointTypes degeri, ad, yuzde)
POINT_INFO = (
	(("POINT_DEF_GRADE",), 16, "Savunma", False),		# 2026-10-09: player.DEF_GRADE = 20 (istemci gosterim savunmasi); sunucu etkileri 16 yollar
	(("POINT_ATT_SPEED", "ATT_SPEED"), 17, "Sald\xfdr\xfd H\xfdz\xfd", True),
	(("POINT_ATT_GRADE", "ATT_GRADE"), 18, "Sald\xfdr\xfd De\xf0eri", False),
	(("POINT_MOV_SPEED", "MOVING_SPEED"), 19, "Hareket H\xfdz\xfd", True),
	(("POINT_CASTING_SPEED", "CASTING_SPEED"), 21, "B\xfcy\xfc H\xfdz\xfd", True),
	(("POINT_MAGIC_ATT_GRADE",), 22, "B\xfcy\xfc Sald\xfdr\xfds\xfd", False),
	(("POINT_MAGIC_DEF_GRADE",), 23, "B\xfcy\xfc Savunmas\xfd", False),
	(("POINT_HP_REGEN",), 32, "HP Yenilenmesi", True),
	(("POINT_SP_REGEN",), 33, "SP Yenilenmesi", True),
	(("POINT_CRITICAL_PCT",), 40, "Kritik Vuru\xfe", True),
	(("POINT_PENETRATE_PCT",), 41, "Delici Vuru\xfe", True),
	(("POINT_MAX_HP", "MAX_HP"), 6, "Maks. HP", False),
	(("POINT_MAX_SP", "MAX_SP"), 8, "Maks. SP", False),
	(("POINT_MAX_HP_PCT",), -1, "Maks. HP", True),
	(("POINT_MAX_SP_PCT",), -1, "Maks. SP", True),
)


def _PointTable():
	t = {}
	for (names, default, label, pct) in POINT_INFO:
		v = None
		for n in names:
			v = getattr(player, n, None)
			if v is not None:
				break
		if v is None:
			v = default
		if v is not None and v >= 0 and v not in t:
			t[v] = (label, pct)
	return t


def _FileExists(f):
	try:
		import pack
		return bool(f) and pack.Exist(f)
	except:
		return bool(f)


def _IconVnum(path):
	"""etki ikonu bir esya ikonunun kopyasiysa esya vnum'u (yeniaffect_icon/71028.png, affect/50821.tga)"""
	p = path.replace("\\", "/").lower()
	if p.endswith("affect/greenpotion.tga"):
		return 27102
	if p.endswith("affect/purplepotion.tga"):
		return 27105
	# KULLANICI (2026-10-01 telefon): otomatik iksir ikonu (pattern/auto_hpgauge/05.dds, 32 px) kucucuk ve pikselli
	# cikiyordu -> otomatik iksir esyasinin HD ikonu
	if "pattern/auto_hpgauge/" in p:
		return 72723
	if "pattern/auto_spgauge/" in p:
		return 72724
	for tag in ("yeniaffect_icon/", "affect/", "icon/item/"):
		i = p.rfind(tag)
		if i >= 0:
			base = p[i + len(tag):].split(".")[0]
			if base.isdigit():
				return int(base)
	return 0


def _HdIcon(path):
	"""-> (dosya, mantiksal boy). Boy 0 = GetWidth ile olc. KULLANICI (2026-10-01): "iconlar pixel pixel gozukmesin".
	HD esya ikonu (icon/item, density 4) ve HD .sub (density 4) mantiksal 32; GetWidth ilk yuklemede 128 donebiliyor."""
	if not path:
		return ("", 0)
	v = _IconVnum(path)
	if v:
		try:
			item.SelectItem(v)
			f = item.GetIconImageFileName()
			if f:
				return (f, 32)
		except:
			pass
	p = path.replace("\\", "/")
	low = p.lower()
	if low.endswith(".sub"):
		return (p, 32)
	for folder in ("horsestate", "lovepoint"):
		tag = "pattern/%s/" % folder
		i = low.find(tag)
		if i >= 0:
			hd = DIR + "ikon/%s_%s.png" % (folder, low[i + len(tag):].split(".")[0])
			if _FileExists(hd):
				return (hd, 128)
	return (p, 32)		# bilinmeyen: GetWidth'e GUVENME (yukleme bitmeden 0/128 donuyor -> boy bir kucuk bir dogru); etki ikonlari 32 px


def _ItemName(vnum):
	try:
		item.SelectItem(vnum)
		return item.GetItemName() or ""
	except:
		return ""


def _Sure(s):
	if s is None:
		return ""
	if s < 0:
		return "S\xfcresiz"
	s = int(max(0, s))
	if s >= 86400:
		return "%d g\xfcn %d sa" % (s // 86400, (s % 86400) // 3600)
	h = s // 3600
	m = (s % 3600) // 60
	x = s % 60
	if h:
		return "%d:%02d:%02d" % (h, m, x)
	return "%d:%02d" % (m, x)


class _Root(ui.Window):
	"""pencere koku: icindeki dokunusu yutar; dunyaya dokununca kapanir, baska arayuze dokunmak (dugme...) kapatmaz"""

	def __init__(self, owner):
		ui.Window.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.AddFlag("hide_on_outside")
		self.owner = owner

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		o = self.owner
		if o:
			o._SurukleBasla()
		return True

	def OnMouseLeftButtonUp(self):
		o = self.owner
		if o:
			o._SurukleBitir()
		return True

	def OnOutsideTap(self):
		o = self.owner
		if o:
			o.Close()

	def OnOutsideTapUI(self):
		o = self.owner
		if o:
			o._SurukleBitir()		# parmak pencere disinda kalktiysa (Up gelmez) baska dokunus listeyi kaydirmasin

	def OnPressEscapeKey(self):
		o = self.owner
		if o:
			o.Close()
		return True


class AktifEtkiler(ui.Window):

	def __init__(self, shower):
		ui.Window.__init__(self, "UI_BOTTOM")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)		# olcek kendimizde (k)
		self.SetWindowName("MobileAktifEtkiler")
		self.SetSize(1, 1)
		self.SetPosition(0, 0)
		self.shower = shower
		self.keep = []
		self.k = wndMgr.GetScreenHeight() / REF_H
		self.timers = {}
		self.horse = (0, 0, 0)
		self.entries = []
		self.filter = "all"
		self.ust = 0			# listede en ustteki satirin sirasi (kaydirma)
		self.surukle = None		# (baslangic fare y, baslangic ust)
		self.nextRefresh = 0.0
		self.hudAllowed = True
		self.hudHidden = False
		self.invCache = None
		self.errLogged = False
		self.points = _PointTable()
		self.newInfo = {}
		for (n, label, kind) in NEW_INFO:
			v = _C(n)
			if v is not None:
				self.newInfo[v] = (label, kind)
		for (attr, label) in (("POINT_MALL_EXPBONUS", "Deneyim Bonusu"), ("POINT_MALL_ITEMBONUS", "Premium H\xfdrs\xfdz Eldiveni"),
				("POINT_MALL_GOLDBONUS", "Yang Bonusu"), ("POINT_PC_BANG_EXP_BONUS", "Deneyim Bonusu (P)"), ("POINT_PC_BANG_DROP_BONUS", "E\xfeya Bonusu (P)")):
			v = getattr(player, attr, None)
			if v is not None:
				self.newInfo[MALL_START + v] = (label, "premium")
		## 2026-10-09 2. asama: 71016 yine POINT_MALL_ITEMBONUS (117); 1. asamada 85'e tasinmisti -> o arada kullanilan etkiler
		## icin 85 de 'Esya Dusurme Bonusu' (game.py AFFECT_DATA_DICT 1000+85 eslemesiyle birlikte)
		self.newInfo.setdefault(MALL_START + getattr(player, "POINT_ITEM_DROP_BONUS", 85), ("E\xfeya D\xfc\xfe\xfcrme Bonusu", "premium"))
		self.flagInfo = {}
		for (n, label, kind) in FLAG_INFO:
			v = _C(n)
			if v is not None:
				self.flagInfo[v] = (label, kind)
		self.potionPoint = {}
		for (n, pn, alt) in (("AFFECT_ATT_SPEED_POTION", "POINT_ATT_SPEED", "ATT_SPEED"), ("AFFECT_MOV_SPEED_POTION", "POINT_MOV_SPEED", "MOVING_SPEED")):
			v = _C(n)
			if v is not None:
				pv = getattr(player, pn, None)
				if pv is None:
					pv = getattr(player, alt, None)
				if pv is None:
					pv = (pn == "POINT_ATT_SPEED") and 17 or 19
				self.potionPoint[v] = pv
		self.__BuildHud()
		self.__BuildWindow()
		self.Show()
		self.__Hook()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.__Unhook()
		try:
			self.win.Hide()
			self.win.owner = None
		except:
			pass
		self.Hide()
		self.keep = []
		self.rows = []
		self.tabs = []
		self.shower = None

	# ------------------------------------------------------------------ eski buff sirasi: veri deposu
	def __Hook(self):
		sh = self.shower
		me = _wref(self)
		shr = _wref(sh)
		cls = sh.__class__

		def add(type, pointIdx, value, duration):
			o = me()
			if o:
				o.OnAffectAdd(type, pointIdx, value, duration)
			s = shr()
			if s is not None:
				cls.BINARY_NEW_AddAffect(s, type, pointIdx, value, duration)

		def rem(type, pointIdx):
			o = me()
			if o:
				o.OnAffectRemove(type, pointIdx)
			s = shr()
			if s is not None:
				cls.BINARY_NEW_RemoveAffect(s, type, pointIdx)

		def horse(level, health, battery):
			o = me()
			if o:
				o.horse = (level, health, battery)
				o.nextRefresh = 0.0
			s = shr()
			if s is not None:
				cls.SetHorseState(s, level, health, battery)

		def show():
			o = me()
			if o:
				o.SetHudAllowed(True)

		def hide():
			o = me()
			if o:
				o.SetHudAllowed(False)

		sh.BINARY_NEW_AddAffect = add
		sh.BINARY_NEW_RemoveAffect = rem
		sh.SetHorseState = horse
		ui.Window.Hide(sh)		# eski ikon sirasi gorunmez (veri deposu olarak yasar)
		sh.Show = show
		sh.Hide = hide

	def __Unhook(self):
		sh = self.shower
		if not sh:
			return
		for n in ("BINARY_NEW_AddAffect", "BINARY_NEW_RemoveAffect", "SetHorseState", "Show", "Hide"):
			try:
				delattr(sh, n)
			except:
				pass

	def __Key(self, type, pointIdx):
		if type == _C("NEW_AFFECT_MALL", -12345):
			return MALL_START + pointIdx
		return type

	def OnAffectAdd(self, type, pointIdx, value, duration):
		try:
			key = self.__Key(type, pointIdx)
			now = app.GetTime()
			inf = duration <= 0 or duration >= INFINITE
			end = now + max(0, duration)
			t = self.timers.get(key)
			if t and t["inf"] == inf and (inf or abs(t["end"] - end) < 3.0):
				if (pointIdx, value) not in t["pts"]:
					t["pts"].append((pointIdx, value))		# ayni etkinin ikinci puani (beceriler 2 puan verir)
			else:
				self.timers[key] = {"end": end, "total": float(max(1, duration)), "inf": inf, "pts": [(pointIdx, value)]}
			self.nextRefresh = 0.0
		except:
			self.__Err()

	def OnAffectRemove(self, type, pointIdx):
		try:
			key = self.__Key(type, pointIdx)
			if key in self.timers:
				del self.timers[key]
			self.nextRefresh = 0.0
		except:
			self.__Err()

	def __Err(self):
		if self.errLogged:
			return
		self.errLogged = True
		import traceback
		dbg.TraceError("uiaktifetki: " + traceback.format_exc())

	# ------------------------------------------------------------------ veri
	def __InvVnums(self):
		"""envanterdeki esya vnum'lari (yenileme basina bir kez)"""
		if self.invCache is not None:
			return self.invCache
		inv = {}
		try:
			n = int(getattr(player, "INVENTORY_PAGE_SIZE", 45)) * int(getattr(player, "INVENTORY_PAGE_COUNT", 4))
			for i in xrange(max(n, 192)):
				v = player.GetItemIndex(i)
				if v > 0:
					inv[int(v)] = 1
		except:
			pass
		self.invCache = inv
		return inv

	def _FindItem(self, point, value, total):
		"""KULLANICI (2026-10-01): "buyuk boy ozut acmisim, etkilerde kucuk boy ozut ikonu cikiyor; envanterdeki aktif olanla
		pencere yanlis". Sunucu esyayi gondermez; (puan, deger) -> aday esyalar (uiaktifetkitablo, sunucu item_proto),
		sure: kalan asil sureyi asamaz -> sure >= kalan adaylar (en kisasi); ayni degerli adaylardan ENVANTERDE OLAN secilir.
		Bulunamazsa 0 (ad = etki aciklamasi)."""
		try:
			cands = uiaktifetkitablo.TABLO.get((int(point), int(value)))
		except:
			cands = None
		if not cands:
			return 0
		ok = [c for c in cands if c[0] >= total - 2] or list(cands)
		best = min([c[0] for c in ok])
		ok = [c for c in ok if c[0] == best]
		inv = self.__InvVnums()
		for (d, v) in ok:
			if v in inv:
				return v
		return ok[0][1]

	def __TimerByPoint(self, point):
		"""iksir bayragi (saldiri/hareket hizi) -> ayni puani veren beceri disi (tur 200-499) etkinin zamanlayicisi"""
		best = None
		for (key, t) in self.timers.items():
			if key < 200 or key >= 500:
				continue
			for (p, v) in t["pts"]:
				if p == point and (best is None or t["end"] > best["end"]):
					best = t
		return best

	def __PointsText(self, t):
		if not t:
			return ""
		out = []
		for (p, v) in t["pts"]:
			if p not in self.points or not v:
				continue
			(label, pct) = self.points[p]
			sign = (v < 0) and "-" or "+"
			if pct:
				out.append("%s %s%%%d" % (label, sign, abs(v)))
			else:
				out.append("%s %s%d" % (label, sign, abs(v)))
			if len(out) >= 2:
				break
		return " \xb7 ".join(out)

	def __Timed(self, t, now):
		"""-> (kalan sn, toplam). Zamanlayici yoksa (None, 0) = bilinmiyor"""
		if not t:
			return (None, 0.0)
		if t["inf"]:
			return (-1, 0.0)
		return (max(0.0, t["end"] - now), t["total"])

	def __Entry(self, key, img, now):
		AS = self.shower.__class__
		data = AS.AFFECT_DATA_DICT.get(key)
		icon = data and data[1] or ""
		isSkill = True
		try:
			isSkill = img.IsSkillAffect()
		except:
			isSkill = True
		if isSkill:
			sk = 0
			try:
				sk = player.AffectIndexToSkillIndex(key)
			except:
				sk = 0
			if sk:
				name = ""
				try:
					name = skill.GetSkillName(sk)
				except:
					name = ""
				kind = "beceri"
				t = self.timers.get(sk)
			else:
				(name, kind) = self.flagInfo.get(key, ("", "diger"))
				t = None
				if key in self.potionPoint:
					t = self.__TimerByPoint(self.potionPoint[key])
				if t and key in self.potionPoint:		# hangi iksir? (Yesil Iksir K/O/B, Saldiri Iksiri +10/+15...)
					for (p, v) in t["pts"]:
						if p == self.potionPoint[key]:
							vn = self._FindItem(p, v, t["total"])
							if vn:
								nm = _ItemName(vn)
								if nm:
									name = nm
									icon = "icon/item/%05d.tga" % vn
									kind = "iksir"
							break
				if not name:		# karisim/renkli iksirler (310-323): ikon bir esyanin kopyasi -> esya adi
					v = _IconVnum(icon)
					if v:
						name = _ItemName(v)
						if name:
							kind = "iksir"
			if not name and data and isinstance(data[0], str):
				name = data[0]
			eff = self.__PointsText(t) or (kind == "beceri" and "Beceri etkisi" or "")
			(left, total) = self.__Timed(t, now)
		else:
			desc = getattr(img, "description", None)
			if not isinstance(desc, str):
				desc = ""
			autoVnum = 0
			if key in (_C("NEW_AFFECT_AUTO_HP_RECOVERY"), _C("NEW_AFFECT_AUTO_SP_RECOVERY")):
				# KULLANICI (2026-10-01): "72726 buyuk ozut / 72730 mavi ozut: ozutlerin ikonu pencerede yanlis" -> aktif
				# otomatik iksir ENVANTER YUVASINDAN kesin bilinir (GetAutoPotionInfo slot -> vnum); kalan yuzde ipucuyla
				# ayni kaynaktan (esya yuvalari: 1 kullanilan, 2 toplam), olmazsa GetAutoPotionInfo cur/tot.
				desc = ""
				try:
					# AUTO_POTION_TYPE_HP = 0 -> "and/or" kisayolu HP'yi de SP'ye dusuruyordu (iki satirda da mavi ozut cikti)
					if key == _C("NEW_AFFECT_AUTO_HP_RECOVERY"):
						pt = player.AUTO_POTION_TYPE_HP
					else:
						pt = player.AUTO_POTION_TYPE_SP
					(act, cur, tot, slot) = player.GetAutoPotionInfo(pt)
					if tot > 0:
						desc = "Kalan: %%%d" % int(cur * 100.0 / tot)
					try:
						autoVnum = int(player.GetItemIndex(int(slot)))
						used = float(player.GetItemMetinSocket(int(slot), 1))
						total = float(player.GetItemMetinSocket(int(slot), 2))
						if total > 0:
							desc = "Kalan: %%%d" % int(round(100.0 - used * 100.0 / total))
					except:
						pass
				except:
					desc = ""
			(label, kind) = self.newInfo.get(key, (None, "iksir"))
			name = label or ""
			if autoVnum > 0:
				nm = _ItemName(autoVnum)
				if nm:
					name = nm
				icon = "icon/item/%05d.tga" % autoVnum
			# KULLANICI (2026-10-01): "mavi ozut buyuk basmisim kucuk gozukuyor, kirmizi iksir basmisim baska sey gozukuyor,
			# gerceklik yok" -> ikondan ESYA ADI UYDURMA: sunucu hangi esyanin basildigini gondermez, yalniz etkiyi
			# (puan + deger + sure). Ad = pack'in gercek etki aciklamasi ("Maks. SP +%20"); esya adi YOK.
			if not name and key >= MALL_START:
				t = self.timers.get(key)
				if t:
					for (p, v) in t["pts"]:
						vn = self._FindItem(key - MALL_START, v, t["total"])
						if vn:
							nm = _ItemName(vn)
							if nm:
								name = nm
								icon = "icon/item/%05d.tga" % vn
							break
			if not name:
				name = desc
				desc = ""
			eff = (desc.lower() != name.lower()) and desc or ""
			clocked = getattr(img, "isClocked", True)
			endTime = getattr(img, "endTime", 0)
			if not clocked or endTime <= 0:
				(left, total) = (-1, 0.0)
			else:
				t = self.timers.get(key)
				if t and not t["inf"]:
					(left, total) = (max(0.0, t["end"] - now), t["total"])
				else:
					left = 0.0
					try:
						left = max(0.0, endTime - app.GetGlobalTimeStamp())
					except:
						left = 0.0
					total = max(1.0, left)
		return {"key": key, "name": name or "?", "eff": eff, "icon": icon, "kind": kind, "left": left, "total": total}

	def __Collect(self):
		sh = self.shower
		if not sh:
			return []
		now = app.GetTime()
		self.invCache = None
		out = []
		try:
			items = sh.affectImageDict.items()
		except:
			items = []
		for (key, img) in items:
			try:
				out.append(self.__Entry(key, img, now))
			except:
				self.__Err()
		# at
		try:
			(level, health, battery) = self.horse
			if level > 0 and getattr(sh, "horseImage", None):
				name = "At"
				try:
					g = (level <= 0) and 0 or ((level - 1) // 10 + 1)
					name = localeInfo.LEVEL_LIST[g] or "At"
				except:
					pass
				effs = []
				try:
					hn = localeInfo.HEALTH_LIST[health]
					if hn:
						effs.append(hn)
				except:
					pass
				if health > 0 and battery == 0:
					try:
						effs.append(localeInfo.NEEFD_REST)
					except:
						pass
				icon = sh.horseImage.__class__.FILE_DICT.get(health * 10 + battery, "")
				out.append({"key": "at", "name": name, "eff": " \xb7 ".join(effs), "icon": icon, "kind": "diger", "left": None, "total": 0.0})
		except:
			self.__Err()
		# sevgi (evlilik)
		try:
			lp = getattr(sh, "lovePointImage", None)
			if lp and lp.IsShow():
				p = max(0, min(100, int(lp.lovePoint)))
				g = (p == 0) and 0 or (p // 25 + 1)
				icon = lp.__class__.FILE_DICT.get(g, "")
				eff = ""
				try:
					eff = localeInfo.AFF_LOVE_POINT % p
				except:
					eff = ""
				out.append({"key": "sevgi", "name": lp.loverName or "Sevgi", "eff": eff, "icon": icon, "kind": "diger", "left": None, "total": 0.0})
		except:
			self.__Err()

		def order(e):
			l = e["left"]
			if l is not None and l >= 0:
				return (0, l, e["name"])
			return (1, 0, e["name"])
		out.sort(key=order)
		return out

	# ------------------------------------------------------------------ yardimci
	def H(self, v):
		"""HUD olcegi (zoom 1)"""
		return int(round(v * self.k))

	def S(self, v):
		"""pencere olcegi"""
		return int(round(v * self.k * ZOOM))

	def F(self, pt, z=ZOOM):
		return "Tahoma:%d" % max(8, min(FONT_MAX, int(round(pt * self.k * z * FONT_BOOST))))

	def _Img(self, name, parent, x, y, sc):
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(DIR + name)
		w.SetScale(self.k * IMG_S, self.k * IMG_S)
		w.SetPosition(sc(x), sc(y))
		w.Show()
		self.keep.append(w)
		return w

	def _Txt(self, parent, font, color, align="left", outline=True, vcenter=False):
		t = ui.TextLine()
		t.SetParent(parent)
		t.AddFlag("not_pick")
		t.SetFontName(font)
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

	def _Btn(self, parent, up, over, down, x, y, func, sc):
		b = ui.Button()
		b.SetParent(parent)
		b.SetUpVisual(DIR + up)
		b.SetOverVisual(DIR + over)
		b.SetDownVisual(DIR + down)
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, self.k * IMG_S, self.k * IMG_S)
		b.SetPosition(sc(x), sc(y))
		b.SetEvent(func)
		b.Show()
		self.keep.append(b)
		return b

	# ------------------------------------------------------------------ DOSEME
	def _PImg(self, path, parent, x, y, sx=1.0, sy=1.0):
		"""pack dokusu: 1 texel = sx/sy tasarim px (pencere olcegi S)"""
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(path)
		if HAS_RRS_W:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		z = self.k * ZOOM
		w.SetScale(sx * z, sy * z)
		w.SetPosition(self.S(x), self.S(y))
		w.Show()
		self.keep.append(w)
		return w

	def _Tile(self, path, parent, x, y, w, h, tw, th, sx=1.0, sy=1.0):
		"""tw x th texel dokuyu (x, y, w, h) alanina doser; kenarlar S(x) .. S(x + w) tam sayisina OTURUR (bkz. _Otur)"""
		img = self._PImg(path, parent, x, y, sx, sy)
		z = self.k * ZOOM
		(zx, r) = _Otur(self.S(x + w) - self.S(x), w, tw, sx, HAS_RRS_W, z)
		(zy, b) = _Otur(self.S(y + h) - self.S(y), h, th, sy, HAS_RRS_W, z)
		img.SetScale(zx, zy)
		img.SetRenderingRect(0.0, 0.0, r, b)
		return img

	def _Rect(self, parent, x, y, w, h, color, fill):
		b = ui.Bar() if fill else ui.Box()
		b.SetParent(parent)
		b.AddFlag("not_pick")
		b.SetColor(color)
		b.SetPosition(self.S(x), self.S(y))
		b.SetSize(max(1, self.S(x + w) - self.S(x)), max(1, self.S(y + h) - self.S(y)))
		b.Show()
		self.keep.append(b)
		return b

	def __Zemin(self, win):
		"""eski pen_bg.png ile ayni: Board (32 texel) + TitleBar (x1.5, 34.5) + baslik + sayi cipi kutusu + liste kutusu"""
		self._Tile(PAT + "board_base.tga", win, 32, 32, W - 64, H - 64, 128, 128)
		self._Tile(PAT + "board_line_top.tga", win, 32, 0, W - 64, 32, 128, 32)
		self._Tile(PAT + "board_line_bottom.tga", win, 32, H - 32, W - 64, 32, 128, 32)
		self._Tile(PAT + "board_line_left.tga", win, 0, 32, 32, H - 64, 32, 128)
		self._Tile(PAT + "board_line_right.tga", win, W - 32, 32, 32, H - 64, 32, 128)
		for (n, cx, cy) in (("lefttop", 0, 0), ("righttop", W - 32, 0), ("leftbottom", 0, H - 32), ("rightbottom", W - 32, H - 32)):
			self._Tile(PAT + "board_corner_%s.tga" % n, win, cx, cy, 32, 32, 32, 32)
		self._Tile(PAT + "titlebar_center.tga", win, 8 + 48, TITLE_Y, W - 16 - 96, 34.5, 32, 32, 1.5, 1.5)
		self._Tile(PAT + "titlebar_left.tga", win, 8, TITLE_Y, 48, 34.5, 32, 32, 1.5, 1.5)
		self._Tile(PAT + "titlebar_right.tga", win, W - 8 - 48, TITLE_Y, 48, 34.5, 32, 32, 1.5, 1.5)
		self._Img("baslik.png", win, TITLE_X, TITLE_Y, self.S)
		self._Rect(win, CHIP_X, CHIP_Y, CHIP_W, CHIP_H, 0x8c000000, True)
		self._Rect(win, CHIP_X, CHIP_Y, CHIP_W, CHIP_H, 0xff6b5a3e, False)
		self._Rect(win, LIST[0], LIST[1], LIST[2], LIST[3], 0x5a000000, True)
		self._Rect(win, LIST[0], LIST[1], LIST[2], LIST[3], 0xff3d342a, False)

	def _Bar(self, parent, color):
		b = ui.Bar()
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

	def _Fit(self, t, text, maxw):
		"""yaziyi maxw (mantiksal px) genislige sigdirir; sigmazsa sonu '..'"""
		t.SetText(text)
		if self._TextW(t) <= maxw:
			return
		s = text
		while len(s) > 1 and self._TextW(t) > maxw:
			s = s[:-1]
			t.SetText(s.rstrip() + "..")

	# ------------------------------------------------------------------ HUD dugmesi
	def __BuildHud(self):
		hs = self.H		# HUD olcegi (modul sabiti H = pencere yuksekligi; golgeleme yok)
		self.hudBtn = self._Btn(self, "hud_up.png", "hud_up.png", "hud_down.png", HUD_X, HUD_Y, ui.__mem_func__(self.Toggle), hs)
		if hasattr(wndMgr, "SetButtonScale"):
			hb = self.k * IMG_S * HUD / HUD_DOKU
			wndMgr.SetButtonScale(self.hudBtn.hWnd, hb, hb)
		self.hudOn = False
		self.hudLabel = self._Txt(self, "Tahoma:%d" % min(FONT_MAX, int(round(14 * self.k * FONT_BOOST))), C_LABEL, "center")
		self.hudLabel.SetPosition(hs(HUD_X + HUD / 2.0), hs(HUD_Y + HUD + 2))
		self.hudLabel.SetText("Etkiler")
		self.badge = self._Img("badge.png", self, HUD_X + HUD + 5 - BADGE, HUD_Y - 5, hs)
		self.badgeT = self._Txt(self, "Tahoma:%d" % min(FONT_MAX, int(round(11 * self.k * FONT_BOOST))), C_DARK, "center", outline=False, vcenter=True)
		self.badgeT.SetPosition(hs(HUD_X + HUD + 5 - BADGE / 2.0), hs(HUD_Y - 5 + BADGE / 2.0))
		self.warn = self._Img("uyari.png", self, HUD_X - 3 + 6 - WARN / 2.0, HUD_Y + HUD + 3 - 6 - WARN / 2.0, hs)
		for w in (self.badge, self.badgeT, self.warn):
			w.Hide()
		self.warnOn = False

	def SetHudAllowed(self, allowed):
		"""oyun secenegi "etkileri goster" (game.__premium -> shower.Show/Hide)"""
		self.hudAllowed = bool(allowed)
		self.__ApplyVisible()

	def SetHudHidden(self, hidden):
		"""HUD "Gizle" (uimobilehud.SetHudHidden): ust sira ile birlikte dugme de gizlenir"""
		self.hudHidden = bool(hidden)
		self.__ApplyVisible()

	def __ApplyVisible(self):
		if self.hudAllowed and not getattr(self, "hudHidden", False):
			self.Show()
		else:
			self.Close()
			self.Hide()

	def __SetHudOn(self, on):
		if self.hudOn == on:
			return
		self.hudOn = on
		up = on and "hud_on.png" or "hud_up.png"
		self.hudBtn.SetUpVisual(DIR + up)
		self.hudBtn.SetOverVisual(DIR + up)
		self.hudBtn.SetDownVisual(DIR + "hud_down.png")

	def __UpdateHud(self):
		n = len(self.entries)
		if n > 0:
			self.badgeT.SetText(str(min(n, 99)))
			self.badge.Show()
			self.badgeT.Show()
		else:
			self.badge.Hide()
			self.badgeT.Hide()
		warn = False
		for e in self.entries:
			l = e["left"]
			if l is not None and 0 <= l < WARN_SEC:
				warn = True
				break
		self.warnOn = warn
		if warn:
			self.warn.Show()
		else:
			self.warn.Hide()

	# ------------------------------------------------------------------ pencere
	def __BuildWindow(self):
		S = self.S
		win = _Root(self)
		win.SetSize(S(W), S(H))
		win.SetPosition(self.H(WIN_X), self.H(WIN_Y))
		win.Hide()
		self.keep.append(win)
		self.win = win
		self.__Zemin(win)		# DOSEME (eski pen_bg.png ~5.5 MB yerine); "Aktif Etkiler" basligi kucuk kalin serit
		self.chipT = self._Txt(win, self.F(12), C_GOLD, "center", vcenter=True)
		self.chipT.SetPosition(S(CHIP_X + CHIP_W / 2.0), S(CHIP_Y + CHIP_H / 2.0))
		self._Btn(win, "close_up.png", "close_over.png", "close_down.png", CLOSE_X, CLOSE_Y, ui.__mem_func__(self.Close), S)
		# sekmeler
		self.tabs = []
		for i in xrange(MAX_TABS):
			x = TAB_X + i * (TAB_W + TAB_GAP)
			b = self._Btn(win, "tab_up.png", "tab_over.png", "tab_on.png", x, TAB_Y, lambda i0=i: self.__OnTab(i0), S)
			dot = self._Bar(win, C_OFF)
			lbl = self._Txt(win, self.F(13), C_CREAM, vcenter=True)
			for w in (b, dot, lbl):
				w.Hide()
			self.tabs.append({"btn": b, "dot": dot, "lbl": lbl, "kind": None, "on": None, "x": x, "text": ""})
		# satirlar
		self.rows = []
		for i in xrange(PER_PAGE):
			rx = ROW_XS[i // ROWS]
			ry = ROW_Y0 + (i % ROWS) * (ROW_H + ROW_GAP)
			bg = self._Img("row.png", win, rx, ry, S)
			stripe = self._Bar(win, C_OFF)
			stripe.SetPosition(S(rx), S(ry + 6))
			stripe.SetSize(max(2, S(3)), S(ROW_H - 12))
			ic = ui.ExpandedImageBox()
			ic.SetParent(win)
			ic.AddFlag("not_pick")
			ic.Hide()
			self.keep.append(ic)
			nameT = self._Txt(win, self.F(14), C_CREAM)
			nameT.SetPosition(S(rx + 68), S(ry + 8))
			timeT = self._Txt(win, self.F(13), C_GOLD, "right")
			timeT.SetPosition(S(rx + ROW_W - 10), S(ry + 9))
			effT = self._Txt(win, self.F(12), C_SUB)
			effT.SetPosition(S(rx + 68), S(ry + 35))
			bx = rx + ROW_W - 10 - BAR_W
			by = ry + 38
			track = self._Img("bar_track.png", win, bx, by, S)
			fill = self._Img("bar_fill.png", win, bx, by, S)
			fill.SetPosition(S(bx) + 1, S(by) + 1)
			row = {"x": rx, "y": ry, "bg": bg, "stripe": stripe, "ic": ic, "file": "", "nameT": nameT, "timeT": timeT,
				"effT": effT, "track": track, "fill": fill, "fillRed": None, "cache": None}
			self.__ShowRow(row, False)
			self.rows.append(row)
		self.emptyT = self._Txt(win, self.F(13), C_OFF, "center", vcenter=True)
		self.emptyT.SetPosition(S(LIST[0] + LIST[2] / 2.0), S(LIST[1] + LIST[3] / 2.0))
		self.emptyT.SetText("\xdeu an aktif etki yok.")
		self.emptyT.Hide()
		# alt satir: "Ilk bitecek: <ad> \xb7 0:42"
		# KULLANICI (2026-10-01 telefon): uc parcali alt yazi birbirine yapisiyordu (motorun GetTextSize'i ekrandaki
		# genislikten kucuk donuyor) -> TEK yazi
		self.footA = self._Txt(win, self.F(12), C_SUB, vcenter=True)
		self.footA.SetPosition(S(LIST[0] + 4), S(FOOT_Y))
		# kaydirma cubugu (prototip: koyu iz + altin tutamak); liste ROWS'tan uzunsa gorunur
		self.sbIz = [self._Rect(win, SB_X, SB_Y, SB_W, SB_H, 0x73000000, True), self._Rect(win, SB_X, SB_Y, SB_W, SB_H, 0xff3d342a, False)]
		self.sbTut = self._Bar(win, C_GOLD)
		self.sbGeo = None
		for w in self.sbIz + [self.sbTut]:
			w.Hide()

	def __ShowRow(self, row, show):
		for n in ("bg", "stripe", "ic", "nameT", "timeT", "effT", "track", "fill"):
			w = row[n]
			if show and n in ("ic", "track", "fill"):
				continue		# bunlar duruma gore ayrica
			if show:
				w.Show()
			else:
				w.Hide()
		if not show:
			row["cache"] = None

	def IsOpen(self):
		return self.win.IsShow()

	def Toggle(self):
		if self.IsOpen():
			self.Close()
		else:
			self.Open()

	def Open(self):
		if not self.hudAllowed or self.hudHidden:
			return
		self.ust = 0
		self.surukle = None
		self.entries = self.__Collect()
		self.__UpdateHud()
		self.win.Show()
		self.win.SetTop()
		self.__SetHudOn(True)
		self.__Render()
		self.nextRefresh = app.GetTime() + REFRESH_OPEN

	def Close(self):
		self.surukle = None
		try:
			self.win.Hide()
		except:
			pass
		self.__SetHudOn(False)

	def __Filtered(self):
		if self.filter == "all":
			return self.entries
		return [e for e in self.entries if e["kind"] == self.filter]

	def __Render(self):
		S = self.S
		entries = self.entries
		self.chipT.SetText("%d etki" % len(entries))
		# sekmeler
		counts = {}
		for e in entries:
			counts[e["kind"]] = counts.get(e["kind"], 0) + 1
		tabs = []
		if entries:
			tabs.append(("all", "T\xfcm\xfc", len(entries), None))
			for (kind, label, color) in KINDS:
				if counts.get(kind):
					tabs.append((kind, label, counts[kind], color))
		if self.filter != "all" and not counts.get(self.filter):
			self.filter = "all"
		# ince pencere: sekmeler satira sigsin (en fazla TAB_W); dar sekmede yazi bir kademe kucuk
		tw = float(TAB_W)
		if tabs:
			tw = min(float(TAB_W), (W - 2 * TAB_X - (len(tabs) - 1) * TAB_GAP) / float(len(tabs)))
		for i in xrange(MAX_TABS):
			t = self.tabs[i]
			if i >= len(tabs):
				for w in (t["btn"], t["dot"], t["lbl"]):
					w.Hide()
				t["kind"] = None
				continue
			(kind, label, n, color) = tabs[i]
			t["kind"] = kind
			geo = (TAB_X + i * (tw + TAB_GAP), tw)
			if t.get("geo") != geo:
				t["geo"] = geo
				t["x"] = geo[0]
				t["text"] = ""
				if hasattr(wndMgr, "SetButtonScale"):
					wndMgr.SetButtonScale(t["btn"].hWnd, self.k * IMG_S * tw / float(TAB_W), self.k * IMG_S)
				t["btn"].SetPosition(S(geo[0]), S(TAB_Y))
				t["lbl"].SetFontName(self.F(13 if tw >= 100 else 11))
			on = (kind == self.filter)
			if t["on"] != on:
				t["on"] = on
				t["btn"].SetUpVisual(DIR + (on and "tab_on.png" or "tab_up.png"))
				t["btn"].SetOverVisual(DIR + (on and "tab_on.png" or "tab_over.png"))
				t["btn"].SetDownVisual(DIR + "tab_on.png")
				t["text"] = ""
			txt = "%s %d" % (label, n)
			if t["text"] != txt:
				t["text"] = txt
				t["lbl"].SetText(txt)
				t["lbl"].SetPackedFontColor(on and C_WHITE or C_CREAM)
				lw = self._TextW(t["lbl"])
				dw = color and S(7) + S(5) or 0
				x0 = S(t["x"] + tw / 2.0) - (dw + lw) // 2
				if color:
					t["dot"].SetColor(color)
					t["dot"].SetPosition(x0, S(TAB_Y + TAB_H / 2.0) - S(3.5))
					t["dot"].SetSize(S(7), S(7))
					t["dot"].Show()
				else:
					t["dot"].Hide()
				t["lbl"].SetPosition(x0 + dw, S(TAB_Y + TAB_H / 2.0))
			t["btn"].Show()
			t["lbl"].Show()
		# satirlar
		lst = self.__Filtered()
		self.ust = max(0, min(self.ust, len(lst) - PER_PAGE))
		base = self.ust
		blink = int(app.GetTime() * 2.0) % 2 == 0
		for i in xrange(PER_PAGE):
			row = self.rows[i]
			j = base + i
			if j >= len(lst):
				self.__ShowRow(row, False)
				continue
			self.__DrawRow(row, lst[j], blink)
		if entries:
			self.emptyT.Hide()
		else:
			self.emptyT.Show()
		self.__DrawScroll(len(lst))
		self.__DrawFooter()

	def __DrawScroll(self, n):
		"""ince kaydirma cubugu: tutamak boyu = gorunen / toplam, konumu = ust / (toplam - gorunen)"""
		if n <= PER_PAGE:
			if self.sbGeo is not None:
				self.sbGeo = None
				for w in self.sbIz + [self.sbTut]:
					w.Hide()
			return
		S = self.S
		yol = SB_H - 4
		th = max(18.0, yol * PER_PAGE / float(n))
		ty = SB_Y + 2 + (yol - th) * self.ust / float(n - PER_PAGE)
		geo = (int(round(th)), int(round(ty)))
		if geo == self.sbGeo:
			return
		self.sbGeo = geo
		self.sbTut.SetPosition(S(SB_X + 2), S(ty))
		self.sbTut.SetSize(max(2, S(SB_X + SB_W - 2) - S(SB_X + 2)), max(2, S(ty + th) - S(ty)))
		for w in self.sbIz + [self.sbTut]:
			w.Show()

	def _SurukleBasla(self):
		"""liste alaninda parmak basildi: surukleme baslar (pencerenin geri kalani yalniz dokunusu yutar)"""
		try:
			(mx, my) = wndMgr.GetMousePosition()
			(gx, gy) = self.win.GetGlobalPosition()
		except:
			return
		S = self.S
		if S(LIST[0]) <= mx - gx <= S(LIST[0] + LIST[2]) and S(LIST[1]) <= my - gy <= S(LIST[1] + LIST[3]):
			self.surukle = (my, self.ust)

	def _SurukleBitir(self):
		self.surukle = None

	def __SurukleGuncelle(self):
		try:
			(mx, my) = wndMgr.GetMousePosition()
		except:
			return
		(y0, u0) = self.surukle
		adim = max(1, self.S(ROW_H + ROW_GAP))
		dy = my - y0
		k = int((abs(dy) + adim // 2) // adim)
		u = u0 - k if dy > 0 else u0 + k		# parmak asagi -> listenin basi gorunur
		n = len(self.__Filtered())
		u = max(0, min(u, n - PER_PAGE))
		if u != self.ust:
			self.ust = u
			self.__Render()

	def __DrawRow(self, row, e, blink):
		S = self.S
		rx, ry = row["x"], row["y"]
		left = e["left"]
		timed = left is not None and left >= 0
		ending = timed and left < WARN_SEC
		tstr = _Sure(left)
		key = (e["key"], e["name"], e["eff"], e["icon"], e["kind"], tstr, ending and blink)
		if row["cache"] == key:
			self.__DrawBar(row, e)
			return
		first = row["cache"] is None
		row["cache"] = key
		if first:
			self.__ShowRow(row, True)
		row["stripe"].SetColor(KIND_COLOR.get(e["kind"], C_OFF))
		self.__SetIcon(row, e["icon"])
		# sure
		row["timeT"].SetText(tstr)
		if ending:
			row["timeT"].SetPackedFontColor(blink and C_RED or 0xffc8604c)
		elif timed:
			row["timeT"].SetPackedFontColor(C_GOLD)
		else:
			row["timeT"].SetPackedFontColor(C_SUB)
		tw = self._TextW(row["timeT"])
		self._Fit(row["nameT"], e["name"], S(ROW_W - 10 - 68) - tw - S(8))
		effMax = S(ROW_W - 10 - 68 - 8) - (timed and S(BAR_W) or 0)
		self._Fit(row["effT"], e["eff"], effMax)
		self.__DrawBar(row, e)

	def __DrawBar(self, row, e):
		left = e["left"]
		if left is None or left < 0:
			row["track"].Hide()
			row["fill"].Hide()
			return
		row["track"].Show()
		p = 0.0
		if e["total"] > 0:
			p = max(0.0, min(1.0, left / float(e["total"])))
		fw = (BAR_W - 2.2) * p
		red = left < WARN_SEC
		f = row["fill"]
		if row["fillRed"] != red:
			row["fillRed"] = red
			f.LoadImage(DIR + (red and "bar_fill_red.png" or "bar_fill.png"))
		if fw >= 0.5:
			f.SetScale(self.k * ZOOM * fw / 4.0, self.k * IMG_S)
			f.Show()
		else:
			f.Hide()

	def __SetIcon(self, row, path):
		ic = row["ic"]
		(f, ls) = _HdIcon(path)
		if not f:
			ic.Hide()
			row["file"] = ""
			return
		if f != row["file"]:
			row["file"] = ""
			try:
				ic.LoadImage(f)
				row["file"] = f
			except:
				ic.Hide()
				return
		if not ls:
			ls = 32
		size = ICON * self.k * ZOOM
		s = size / float(ls)
		ic.SetScale(s, s)
		cx = self.S(row["x"] + 8 + 25)
		cy = self.S(row["y"] + 6 + 25)
		ic.SetPosition(int(round(cx - size / 2.0)), int(round(cy - size / 2.0)))
		ic.Show()

	def __DrawFooter(self):
		S = self.S
		first = None
		for e in self.entries:
			l = e["left"]
			if l is not None and l >= 0:
				first = e
				break
		if not first:
			self.footA.SetText(self.entries and "S\xfcreli etki yok" or "")
			return
		limit = S(LIST[0] + LIST[2] - 4) - S(LIST[0] + 4)
		self._Fit(self.footA, "\xddlk bitecek: %s  (%s)" % (first["name"], _Sure(first["left"])), limit)

	def __OnTab(self, i):
		try:
			kind = self.tabs[i]["kind"]
		except:
			return
		if not kind or kind == self.filter:
			return
		self.filter = kind
		self.ust = 0
		self.__Render()

	# ------------------------------------------------------------------ kare
	def OnUpdate(self):
		now = app.GetTime()
		if self.surukle:
			if self.IsOpen():
				self.__SurukleGuncelle()
			else:
				self.surukle = None
		if now >= self.nextRefresh:
			opened = self.IsOpen()
			self.nextRefresh = now + (opened and REFRESH_OPEN or REFRESH_CLOSED)
			self.entries = self.__Collect()
			self.__UpdateHud()
			if opened:
				self.__Render()
		if self.warnOn:
			import math
			self.warn.SetAlpha(0.35 + 0.65 * (0.5 + 0.5 * math.cos(now * 2.0 * math.pi / 1.2)))
