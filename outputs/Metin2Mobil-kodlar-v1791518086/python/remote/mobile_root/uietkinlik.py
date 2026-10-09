# MOBIL - YENI DOSYA (mobile_root/uietkinlik.py): ETKINLIK TAKVIMI penceresi.
#
# Tasarim : Desktop/Etkinlik-Penceresi/etkinlik-penceresi.html (KULLANICI 2026-09-23):
#           koyu/altin cerceve, solda gun gun zaman cizelgesi, sagda secili etkinligin
#           detayi (durum, aciklama, geri sayim, bolge/seviye/baslangic/bitis, oduller).
# Gorseller: mobile/ui/etk/*.tga  (tools/bake_etkinlik.py tasarimin CSS'inden pisirir)
# Veri    : sunucu quest'i etkinlik_takvimi.lua (engine/server/quest) giriste ve 2 dk'da bir
#           cmdchat ile gonderir -> game.py "EtkinlikTakvimi"/"EtkinlikSatir" -> bu pencere.
#           Sunucudan veri gelmezse (quest kurulu degilse) ayni takvim TELEFON SAATIYLE
#           hesaplanir; yalniz "su anda aktif" bilgisi sunucu bayraklarindan gelir.
# Acilis  : HUD'daki Etkinlik dugmesi (uimobilehud.EventHudButton) -> interface.ToggleEtkinlik().
#           Acilis animasyonu tasarimdaki @keyframes open (0.72 -> 1.03 -> 1.0 olcek, 0.75 s);
#           kapanis @keyframes close (0.85 olcek + solma, 0.35 s). Metinler olceklenemedigi icin
#           %55'te (tasarimda bulanikligin kalktigi an) belirir.
#
# YERLESIM: tasarimin REF kutusu 1050x680; k = ekrana sigdirma carpani. Kok pencere olcek DISI
# (wndMgr.SetUIScale 1.0) - motorun kok olcegi 1.0'in altina inmedigi (GetRootUIScale) icin
# animasyon her ogeyi kendisi olcekler (ExpandedImageBox.SetScale / wndMgr.SetButtonScale).
#
# TUZAK (uiisinlanma.py ile ayni): ui.Window nesnesinin Python referansi dusunce C++ penceresi
# aninda silinir -> HER cocuk self.keep listesinde tutulur.
# Turkce metinler cp1254 kacis dizileriyle (\xdd=I-noktali, \xfd=i-siz, \xfe=s-cengelli,
# \xf0=g-yumusak, \xfc=u-umlaut, \xf6=o-umlaut, \xe7=c-cengelli, \xb7=orta nokta).

import ui
import wndMgr
import app
import dbg
import math
import time

try:
	import item
except:
	item = None

DIR = "mobile/ui/etk/"
REF_W = 1240.0			# tasarim 1050 idi; telefon ekrani (2.2:1) icin genisletildi (KULLANICI: buyumesi lazim)
REF_H = 680.0
HEAD = 82
FOOT = 52
LEFT_W = 521
ROW_W = 477
ROW_H = 62
INFO_W = 322
IMG_S = 0.5			# gorseller 2x pisirildi (bake_etkinlik.py S=2) -> keskin cizim icin 0.5
BADGE_PULSE_SEC = 1.2		# AKTIF rozeti yanip sonme (tasarim: animation pulse 1.2s)
REWARD_COLS = 7
REWARD_MAX = 14
ROW_GAP = 8
ROW_CAP = 7				# sol listede ayni anda gorunen satir (7 gunluk takvim tam sigar)
OPEN_SEC = 0.75
CLOSE_SEC = 0.35
TEXT_AT = 0.55			# metinlerin belirdigi an (tasarimda blur'un kalktigi kare)

# renkler (tasarim CSS'i) - SetPackedFontColor ARGB
C_TITLE = 0xfff0d89c
C_SUB = 0xff9d9384
C_CLOCK = 0xffe0bd78
C_DIM = 0xff9a9186
C_DAY = 0xffb89154
C_NAME = 0xffe3d1aa
C_ZONE = 0xffa8a094
C_TIME = 0xffe0bd78
C_EYEBROW = 0xffbf7a36
C_H2 = 0xfff4deb0
C_DESC = 0xffb5ada1
C_NUM = 0xfff2cf83
C_NUMLBL = 0xffa39a8c
C_INFOLBL = 0xffa39a8c
C_INFOVAL = 0xffd4c29c
C_RWTITLE = 0xffb88c4b
C_RWLBL = 0xffb3aa9b
C_FOOT = 0xffa39a8c
C_FOOTB = 0xffad8950

DAYS = {1: "Pazartesi", 2: "Sal\xfd", 3: "\xc7ar\xfeamba", 4: "Per\xfeembe", 5: "Cuma", 6: "Cumartesi", 7: "Pazar"}
DAYS_UP = {1: "PAZARTES\xdd", 2: "SALI", 3: "\xc7AR\xdeAMBA", 4: "PER\xdeEMBE", 5: "CUMA", 6: "CUMARTES\xdd", 7: "PAZAR"}
DAYS_SHORT = {1: "PZT", 2: "SAL", 3: "\xc7AR", 4: "PER", 5: "CUM", 6: "CMT", 7: "PAZ"}

# Statik metinler (isim/bolge/seviye/aciklama/oduller) ISTEMCIDE; gun/saat/bayrak sunucudan.
# icon: etkinligi temsil eden ESYA vnum'u (oyunun kendi ikonu - tasarimdaki emoji yerine).
# day/start/end: sunucu quest'i yokken kullanilan varsayilan takvim (etknquest.lua ile ayni).
EVENTS = {
	"ayisigi": {
		"name": "Ay I\xfe\xfd\xf0\xfd Sand\xfd\xf0\xfd", "zone": "T\xfcm Haritalar", "level": "1 - 120", "icon": 50011,
		"desc": "Canavarlardan Ay I\xfe\xfd\xf0\xfd Define Sand\xfd\xf0\xfd d\xfc\xfe\xfcr. Sand\xfdklar\xfd a\xe7arak nadir y\xfckseltme nesneleri ve de\xf0erli e\xfeyalar kazan.",
		"rewards": [(50011, "")],
		"chest": [71027, 71028, 71029, 71030, 71044, 71045, 71151, 71152, 71084, 71085, 50100, 50107, 71083, 70102, 50621, 27112, 27115, 70024, 25040, 71032],
		"day": 1, "start": 21 * 60, "end": 23 * 60},
	"futbol": {
		"name": "Futbol Topu", "zone": "T\xfcm Haritalar", "level": "1 - 120", "icon": 50096,
		"desc": "Canavarlar Futbol Topu d\xfc\xfe\xfcr\xfcr. Toplar\xfd a\xe7, \xfeansl\xfd olanlar Alt\xfdn Futbol Topu ve forma kazan\xfdr.",
		"rewards": [(50096, "")],
		"chest": [71027, 71028, 71029, 71030, 71044, 71045, 71151, 71152, 71084, 71085, 50100, 50107, 50621, 27112, 27115, 70024, 25040, 70049, 70048, 70051],
		"day": 2, "start": 21 * 60, "end": 23 * 60},
	"pet": {
		"name": "Pet Sand\xfd\xf0\xfd", "zone": "T\xfcm Haritalar", "level": "1 - 120", "icon": 50033,
		"desc": "Canavarlardan Pet Sand\xfd\xf0\xfd d\xfc\xfe\xfcr. Sand\xfdklardan evcil hayvan ve evcille\xfetirme e\xfeyalar\xfd \xe7\xfdkar.",
		"rewards": [(50033, "")],
		"chest": [50300, 70102, 25040, 50061],
		"day": 3, "start": 21 * 60, "end": 23 * 60},
	"kostum": {
		"name": "Kost\xfcm Sand\xfd\xf0\xfd", "zone": "T\xfcm Haritalar", "level": "1 - 120", "icon": 50125,
		"desc": "Canavarlardan Kost\xfcm Sand\xfd\xf0\xfd d\xfc\xfe\xfcr. Sand\xfdklardan nadir kost\xfcmler ve g\xf6r\xfcn\xfcm e\xfeyalar\xfd \xe7\xfdkar.",
		"rewards": [(50125, "")],
		"chest": [71085, 70039, 71032, 70024, 25040, 71012, 71130, 71083, 71004, 25041, 71125, 50126],
		"day": 4, "start": 21 * 60, "end": 23 * 60},
	"bulmaca": {
		"name": "Bulmaca Kutusu", "zone": "T\xfcm Haritalar", "level": "1 - 120", "icon": 50034,
		"desc": "Canavarlardan Bulmaca Kutusu d\xfc\xfe\xfcr. Par\xe7alar\xfd birle\xfetir, \xf6d\xfcl kutular\xfdn\xfd a\xe7.",
		"rewards": [(50034, "Bulmaca Kutusu"), (50117, "M\xfccevher Kutusu")],
		"day": 5, "start": 21 * 60, "end": 23 * 60},
	"vs": {
		"name": "VS Turnuvas\xfd", "zone": "Arena", "level": "Kay\xfdta g\xf6re", "icon": 50249,
		"desc": "Oyuncular arenada teke tek kar\xfe\xfd kar\xfe\xfdya geliyor. Turnuvay\xfd kazanan KRAL unvan\xfdn\xfd ve \xf6d\xfcl\xfc al\xfdr.",
		"rewards": [(50249, "")],
		"chest": [27001, 27002, 27003, 27004, 27005, 27006, 70048, 70102, 70051, 70049, 25040, 30045, 30051, 30038],
		"day": 6, "start": 21 * 60, "end": 23 * 60},
	"ox": {
		"name": "OX Etkinli\xf0i", "zone": "OX Alan\xfd", "level": "1 - 120", "icon": 30220,
		"desc": "Bilgi yar\xfd\xfemas\xfd: sorulara O / X alan\xfdna ge\xe7erek cevap ver. Sona kalan kazan\xfdr.",
		"rewards": [(30220, "10 Ruh Ta\xfe\xfd"), (30037, "1 Pen\xe7e"), (31022, "1 Pul")],
		"day": 7, "start": 21 * 60, "end": 22 * 60},
	# yalniz bayrakla acilan (takvimsiz) etkinlikler - aktifken listelenir
	"altigen": {
		"name": "Alt\xfdgen Hediye Paketi", "zone": "T\xfcm Haritalar", "level": "1 - 120", "icon": 50037,
		"desc": "Canavarlardan Alt\xfdgen Hediye Paketi d\xfc\xfe\xfcr. Paketlerden rastgele \xf6d\xfcller \xe7\xfdkar.",
		"rewards": [(50037, "")], "day": 0, "start": 0, "end": 0,
		"chest": [30003, 30004, 30005, 30006, 30007, 30008, 30009, 30010, 30011, 30014, 30015, 30016, 30017, 30018]},
	"okey": {
		"name": "Okey Kart", "zone": "T\xfcm Haritalar", "level": "1 - 120", "icon": 79505,
		"desc": "Canavarlardan Okey Koleksiyon Kart\xfd d\xfc\xfe\xfcr. 24 kart\xfd toplay\xfdp Okey Kart Seti'ni al.",
		"rewards": [(79506, "Okey Kart Seti"), (71194, "Alt\xfdn Okey Sand\xfd\xf0\xfd")], "day": 0, "start": 0, "end": 0},
	"atyarisi": {
		"name": "At Yar\xfd\xfe\xfd", "zone": "Yar\xfd\xfe Pisti", "level": "1 - 120", "icon": 50061,
		"desc": "At\xfdnla yar\xfd\xfe pistine gel, ilk bitiren \xf6d\xfcl\xfcn sahibi olur.",
		"rewards": [(50061, "S\xfcrpriz \xd6d\xfcl")], "day": 0, "start": 0, "end": 0},
	"harita": {
		"name": "Etkinlik Haritas\xfd", "zone": "Etkinlik Haritas\xfd", "level": "Kay\xfdta g\xf6re", "icon": 50200,
		"desc": "\xd6zel etkinlik haritas\xfd a\xe7\xfdk. Krall\xfdk muhaf\xfdz\xfdndan giri\xfe yap.",
		"rewards": [(50200, "Paket")], "day": 0, "start": 0, "end": 0},
}
ORDER = ["ayisigi", "futbol", "pet", "kostum", "bulmaca", "vs", "ox"]
EXTRA = ["altigen", "okey", "atyarisi", "harita"]


def _EaseOutCubic(t):
	t = 1.0 - t
	return 1.0 - t * t * t


def _EaseInOut(t):
	return 0.5 - 0.5 * math.cos(t * math.pi)


def _Pad2(n):
	n = int(n)
	if n < 0:
		n = 0
	if n < 10:
		return "0%d" % n
	return "%d" % n


def _ItemName(vnum):
	if not item or not vnum:
		return ""
	try:
		item.SelectItem(int(vnum))
		return item.GetItemName()
	except:
		return ""


def _Short(text, n):
	if len(text) <= n:
		return text
	return text[:n - 1] + "."


def _IconFile(vnum):
	if not item or not vnum:
		return ""
	try:
		item.SelectItem(int(vnum))
		return item.GetIconImageFileName()
	except:
		return ""


class EventCalendarWindow(ui.Window):

	def __init__(self):
		ui.Window.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)		# olcekleme animasyonu kendimizde
		self.SetWindowName("EventCalendarWindow")
		self.keep = []
		self.rowWnds = []
		self.badges = []
		self.detailKeep = []
		self.imgs = []			# (wnd, fx, fy)  -> animasyonda olceklenen gorseller
		self.btns = []			# (btn, fx, fy)
		self.texts = []			# animasyon sonunda gorunen metinler
		self.rows = []			# {key, aktif, bas, bit, gun, odul}
		self.sel = 0
		self.page = 0
		self.state = "kapali"		# kapali / aciliyor / acik / kapaniyor
		self.animT0 = 0.0
		self.lastTick = 0.0
		self.hasServer = False
		self.pending = []
		self.pendingN = 0
		self.srvNow = 0
		self.srvRecv = 0.0
		self.srvGun = 0
		self.srvDakika = 0
		# PERFORMANS (2026-09-24): gorseller (2x zemin ~13 MB GPU) oyuna girer girmez DEGIL, ilk acilista yuklenir
		self.built = False
		## PERFORMANS (KULLANICI 2026-09-27: "etkinlik penceresi oyunu cok agirlastiriyor, buyuk harita gibi hizli
		## acilsin, oyunu yormasin"): satirlar/detay her acilista DEGIL, veri degisince ya da 60 sn'den eskiyse kurulur;
		## olcek/konum animasyonu (her kare 100+ pencere) kalkti - pencere aninda gorunur/kapanir.
		self.rowsSig = None
		self.builtAt = -100.0
		self.Hide()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.Hide()		# isinlanmada eski pencere bellekte kalirsa cizmesin
		self.__ClearRows()
		self.__ClearDetail()
		self.keep = []
		self.imgs = []
		self.btns = []
		self.texts = []

	# ------------------------------------------------------------------ yerlesim
	def __Layout(self):
		W = wndMgr.GetScreenWidth()
		H = wndMgr.GetScreenHeight()
		self.scrW = W
		self.scrH = H
		k = min(0.985 * W / REF_W, 0.965 * H / REF_H)
		self.k = k
		self.winW = int(round(REF_W * k))
		self.winH = int(round(REF_H * k))
		self.winX = (W - self.winW) / 2
		self.winY = (H - self.winH) / 2
		self.SetSize(W, H)
		self.SetPosition(0, 0)

	def P(self, rx, ry):
		return (int(round(rx * self.k)), int(round(ry * self.k)))

	def F(self, pt):
		s = int(round(pt * self.k))
		if s < 8:
			s = 8
		if s > 32:
			s = 32
		return "Tahoma:%d" % s

	# ------------------------------------------------------------------ yapi taslari
	def _Img(self, name, rx, ry, parent=None, keep=None, anim=True, base=IMG_S):
		w = ui.ExpandedImageBox()
		w.SetParent(parent or self.body)
		w.AddFlag("not_pick")
		w.LoadImage(DIR + name)
		w.SetScale(self.k * base, self.k * base)
		w.m2BaseScale = base
		(x, y) = self.P(rx, ry)
		w.SetPosition(x, y)
		w.Show()
		(keep if keep is not None else self.keep).append(w)
		if anim:
			self.imgs.append((w, x, y))
		return w

	def _ItemIcon(self, vnum, rcx, rcy, rsize, parent=None, keep=None):
		f = _IconFile(vnum)
		if not f:
			return None
		w = ui.ExpandedImageBox()
		w.SetParent(parent or self.body)
		w.AddFlag("not_pick")
		try:
			w.LoadImage(f)
		except:
			return None
		iw = w.GetWidth()
		ih = w.GetHeight()
		if iw <= 0 or ih <= 0:
			iw = ih = 32
		s = rsize * self.k / float(max(iw, ih))
		w.SetScale(s, s)
		w.m2BaseScale = s / self.k		# __ApplyAnim: k*a*taban
		x = int(round(rcx * self.k - iw * s / 2.0))
		y = int(round(rcy * self.k - ih * s / 2.0))
		w.SetPosition(x, y)
		w.Show()
		(keep if keep is not None else self.keep).append(w)
		self.imgs.append((w, x, y))
		return w

	def _Txt(self, text, rx, ry, pt, color, align="left", parent=None, keep=None, outline=False):
		t = ui.TextLine()
		t.SetParent(parent or self.body)
		t.AddFlag("not_pick")
		t.SetFontName(self.F(pt))
		if outline:
			t.SetOutline()
		if align == "center":
			t.SetHorizontalAlignCenter()
		elif align == "right":
			t.SetHorizontalAlignRight()
		t.SetPackedFontColor(color)
		(x, y) = self.P(rx, ry)
		t.SetPosition(x, y)
		t.SetText(text)
		t.Show()
		(keep if keep is not None else self.keep).append(t)
		self.texts.append(t)
		return t

	def _Btn(self, up, over, down, rx, ry, func, parent=None, keep=None, sx=1.0, sy=1.0):
		b = ui.Button()
		b.SetParent(parent or self.body)
		b.SetUpVisual(DIR + up)
		b.SetOverVisual(DIR + over)
		b.SetDownVisual(DIR + down)
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, self.k * IMG_S * sx, self.k * IMG_S * sy)
		(x, y) = self.P(rx, ry)
		b.SetPosition(x, y)
		b.SetEvent(func)
		b.Show()
		(keep if keep is not None else self.keep).append(b)
		self.btns.append((b, x, y, sx, sy))
		return b

	# ------------------------------------------------------------------ sabit iskelet
	def __Build(self):
		W = self.scrW
		H = self.scrH
		# karartma (tasarimdaki koyu sahne) - tasarimda pencere disina dokunma yok ama mobilde
		# disari dokunma = kapat (kok pencere OnMouseLeftButtonUp)
		dim = ui.Bar()
		dim.SetParent(self)
		dim.AddFlag("not_pick")
		dim.SetSize(W, H)
		dim.SetPosition(0, 0)
		dim.SetColor(0xa6000000)
		dim.Show()
		self.keep.append(dim)
		self.dim = dim

		# govde: pencere dikdortgeni; icindeki dokunmalari yutar (dugmeler cocuk)
		body = ui.Window()
		body.SetParent(self)
		body.SetSize(self.winW, self.winH)
		body.SetPosition(self.winX, self.winY)
		body.Show()
		self.keep.append(body)
		self.body = body

		self._Img("win_shadow.png", -80, -110, base=2.0)
		## DOSEME (KULLANICI 2026-10-01 "her pencereyi hizlandiralim"): tek parca win_bg.png (2480x1360 ~12.9 MB) yerine
		## YUMUSAK katman (gecisler, 1/4 cozunurluk, base 2.0) + birbirine binmeyen KESKIN seritler (cerceve, cizgiler,
		## kose susleri). Hepsi resim -> acilis animasyonuyla birlikte olceklenir. Uretim: tools/bake_etkinlik.py
		import uietkinlikzemin as EZ
		self._Img(EZ.YUMUSAK, 0, 0, base=2.0)
		for (nm, zx, zy) in EZ.PARCALAR:
			self._Img(nm, zx, zy)

		# baslik
		# KULLANICI (2026-09-23): baslik muhru yerine Desktop/etkinlik-iconu.png (256 px, 0.27 -> 69 mantiksal)
		self._Img("etkinlik_ikon.png", 22, 6, base=0.27)
		self._Txt("ETK\xddNL\xddK TAKV\xddM\xdd", 98, 14, 26, C_TITLE)
		self._Txt("Yakla\xfean etkinlikler ve \xf6d\xfcller", 98, 50, 15, C_SUB)
		self.clock = self._Txt("00:00", REF_W - 108, 18, 24, C_CLOCK, "right")
		self._Txt("SUNUCU SAAT\xdd", REF_W - 108, 52, 13, C_DIM, "right")
		self._Btn("close_up.png", "close_down.png", "close_down.png", REF_W - 56, 17, ui.__mem_func__(self.Close))

		# altbilgi
		self._Txt("\xddPUCU", 30, 643, 14, C_FOOTB)
		self._Txt("Etkinli\xf0e kat\xfdlmadan \xf6nce envanterinde bo\xfe yer b\xfdrak.", 92, 643, 14, C_FOOT)
		self._Img("dot_active.png", REF_W - 250, 641)
		self._Txt("Aktif", REF_W - 230, 643, 14, C_FOOT)
		self._Img("dot_next.png", REF_W - 150, 641)
		self._Txt("Yakla\xfean", REF_W - 130, 643, 14, C_FOOT)

		# sayfa dugmeleri (liste tasarsa)
		self.pgUp = self._Btn("count_box.png", "count_box.png", "count_box.png", 25, 596, ui.__mem_func__(self.__PageUp), sy=0.5)
		self.pgDn = self._Btn("count_box.png", "count_box.png", "count_box.png", 25 + ROW_W - 68, 596, ui.__mem_func__(self.__PageDown), sy=0.5)
		self.pgUpT = self._Txt("^", 59, 599, 14, C_TIME, "center", parent=self.pgUp)
		self.pgDnT = self._Txt("v", 25 + ROW_W - 34, 599, 12, C_TIME, "center", parent=self.pgDn)
		self.pgUpT.SetPosition(*self.P(34, 3))
		self.pgDnT.SetPosition(*self.P(34, 4))
		self.pgUp.Hide()
		self.pgDn.Hide()

		self.__RebuildRows()
		self.__RebuildDetail()
		self.__ApplyAnim(1.0, 0, 1.0, True)

	# ------------------------------------------------------------------ veri
	def BeginServerData(self, n, now, gun, dakika):
		self.pending = []
		self.pendingN = n
		self.srvNow = now
		self.srvRecv = app.GetTime()
		self.srvGun = gun
		self.srvDakika = dakika

	def AddServerRow(self, key, aktif, bas, bit, gun, odul):
		if not EVENTS.has_key(key):
			return
		self.pending.append({"key": key, "aktif": aktif, "bas": bas, "bit": bit, "gun": gun, "odul": odul})
		if len(self.pending) >= self.pendingN:
			self.hasServer = True
			rows = self.__Order(self.pending)
			self.pending = []
			if repr(rows) == repr(self.rows):
				return		# 2 dk'lik tazeleme ayni veriyi getirdi: hicbir sey kurma
			self.rows = rows
			self.rowsSig = None
			if self.IsShow():
				self.__EnsureRows(True)

	def __Order(self, rows):
		# takvimliler gune gore (bugunden baslayarak), takvimsiz aktifler en uste
		out = []
		for r in rows:
			if r["gun"] == 0 and r["aktif"]:
				out.append(r)
		sched = [r for r in rows if r["gun"] > 0]
		sched.sort(lambda a, b: cmp(a["bas"], b["bas"]))
		return out + sched

	def __FallbackRows(self):
		# sunucu quest'i yoksa: ayni takvim, telefon saati
		lt = time.localtime()
		now = int(time.time())
		gun = lt[6] + 1			# tm_wday Pzt=0
		dakika = lt[3] * 60 + lt[4]
		gunbasi = now - (lt[3] * 3600 + lt[4] * 60 + lt[5])
		rows = []
		for key in ORDER:
			e = EVENTS[key]
			fark = e["day"] - gun
			if fark < 0:
				fark += 7
			bas = gunbasi + fark * 86400 + e["start"] * 60
			bit = gunbasi + fark * 86400 + e["end"] * 60
			if fark == 0 and dakika >= e["end"]:
				bas += 7 * 86400
				bit += 7 * 86400
			aktif = 0
			if bas <= now < bit:
				aktif = 1
			rows.append({"key": key, "aktif": aktif, "bas": bas, "bit": bit, "gun": e["day"], "odul": 0})
		return rows

	def Now(self):
		if self.hasServer:
			return self.srvNow + (app.GetTime() - self.srvRecv)
		return time.time()

	def __SrvMidnight(self):
		# sunucu yerel gun baslangicinin epoch'u (saniye hassasiyeti yeterli)
		if self.hasServer:
			return self.srvNow - self.srvDakika * 60
		lt = time.localtime()
		return int(time.time()) - (lt[3] * 3600 + lt[4] * 60 + lt[5])

	def HM(self, epoch):
		s = int(epoch - self.__SrvMidnight()) % 86400
		return "%s:%s" % (_Pad2(s / 3600), _Pad2((s % 3600) / 60))

	def ClockText(self):
		if self.hasServer:
			s = int(self.srvDakika * 60 + (app.GetTime() - self.srvRecv)) % 86400
			return "%s:%s" % (_Pad2(s / 3600), _Pad2((s % 3600) / 60))
		lt = time.localtime()
		return "%s:%s" % (_Pad2(lt[3]), _Pad2(lt[4]))

	def __DayWord(self, r):
		# BUGUN / YARIN / gun adi
		if r["gun"] == 0:
			return "\xdeU AN"
		d = int((r["bas"] - self.__SrvMidnight()) / 86400)
		if d <= 0:
			return "BUG\xdcN"
		if d == 1:
			return "YARIN"
		return DAYS_UP.get(r["gun"], "")

	def __DayWordMixed(self, r):
		if r["gun"] == 0:
			return "\xdeimdi"
		d = int((r["bas"] - self.__SrvMidnight()) / 86400)
		if d <= 0:
			return "Bug\xfcn"
		if d == 1:
			return "Yar\xfdn"
		return DAYS.get(r["gun"], "")

	def GetActiveCount(self):
		n = 0
		for r in self.rows:
			if r["aktif"]:
				n += 1
		return n

	# ------------------------------------------------------------------ sol liste
	def __ClearRows(self):
		for w in self.rowWnds:
			try:
				w.Hide()
			except:
				pass
		self.rowWnds = []
		self.badges = []
		self.imgs = [e for e in self.imgs if e[0] not in self.__rowSet]
		self.btns = [e for e in self.btns if e[0] not in self.__rowSet]
		self.texts = [t for t in self.texts if t not in self.__rowSet]
		self.__rowSet = []

	__rowSet = []

	def __RebuildRows(self):
		self.__ClearRows()
		if not self.rows:
			self.rows = self.__FallbackRows()
		if self.sel >= len(self.rows):
			self.sel = 0
		n = len(self.rows)
		pages = (n + ROW_CAP - 1) / ROW_CAP
		if self.page >= pages:
			self.page = max(0, pages - 1)
		start = self.page * ROW_CAP
		shown = self.rows[start:start + ROW_CAP]
		y = HEAD + 20
		lastDay = None
		for i in range(len(shown)):
			r = shown[i]
			idx = start + i
			e = EVENTS[r["key"]]
			active = r["aktif"] and 1 or 0
			selected = (idx == self.sel)
			rowKeep = []
			# satir zemini = dugme
			if selected:
				bg = "row_bg_active.png"
				ox, oy = -20, -20
			else:
				bg = "row_bg.png"
				ox, oy = 0, 0
			b = self._Btn(bg, "row_bg_over.png" if not selected else bg, bg, 25 + ox, y + oy,
				lambda a0=idx: self.__Select(a0), keep=rowKeep)
			# isaretci (sol elmas)
			self._Img(active and "marker_active.png" or "marker.png", 25 - 15 - 12, y + ROW_H / 2 - 12, keep=rowKeep)
			# ikon cercevesi + esya ikonu
			if selected or active:
				self._Img("icon_frame_active.png", 25 + 11 - 15, y + 9 - 15, keep=rowKeep)
			else:
				self._Img("icon_frame.png", 25 + 11, y + 9, keep=rowKeep)
			self._ItemIcon(e["icon"], 25 + 11 + 22, y + 9 + 22, 34, keep=rowKeep)
			# isim + AKTIF rozeti
			t = self._Txt(e["name"], 25 + 66, y + 7, 18, C_NAME, keep=rowKeep)
			if active:
				try:
					(tw, th) = t.GetTextSize()
				except:
					tw = len(e["name"]) * 10 * self.k
				bx = int(round((25 + 66) * self.k + tw + 6 * self.k))
				badge = ui.ExpandedImageBox()
				badge.SetParent(self.body)
				badge.AddFlag("not_pick")
				badge.LoadImage(DIR + "badge_live.png")
				badge.SetScale(self.k * IMG_S, self.k * IMG_S)
				badge.m2BaseScale = IMG_S
				self.badges.append(badge)
				by = int(round((y + 9) * self.k))
				badge.SetPosition(bx, by)
				badge.Show()
				rowKeep.append(badge)
				self.imgs.append((badge, bx, by))
			self._Txt(e["zone"], 25 + 66, y + 36, 14, C_ZONE, keep=rowKeep)
			# sag: gun + saat
			if r["gun"] > 0:
				tt = "%s \xb7 %s - %s" % (self.__DayWord(r), self.HM(r["bas"]), self.HM(r["bit"]))
			else:
				tt = "\xdeU ANDA"
			self._Txt(tt, 25 + ROW_W - 13, y + 21, 15, C_TIME, "right", keep=rowKeep)
			self.rowWnds.extend(rowKeep)
			self.__rowSet = self.__rowSet + rowKeep
			y += ROW_H + ROW_GAP
		# sayfa dugmeleri
		if pages > 1:
			self.pgUp.Show()
			self.pgDn.Show()
		else:
			self.pgUp.Hide()
			self.pgDn.Hide()

	def __PageUp(self):
		if self.page > 0:
			self.page -= 1
			self.__RebuildRows()
			self.__ApplyAnim(1.0, 0, 1.0, True)

	def __PageDown(self):
		pages = (len(self.rows) + ROW_CAP - 1) / ROW_CAP
		if self.page < pages - 1:
			self.page += 1
			self.__RebuildRows()
			self.__ApplyAnim(1.0, 0, 1.0, True)

	def __Select(self, idx):
		if idx == self.sel:
			return
		self.sel = idx
		self.__EnsureRows(True)

	# ------------------------------------------------------------------ sag detay
	def __ClearDetail(self):
		for w in self.detailKeep:
			try:
				w.Hide()
			except:
				pass
		self.imgs = [e for e in self.imgs if e[0] not in self.detailKeep]
		self.btns = [e for e in self.btns if e[0] not in self.detailKeep]
		self.texts = [t for t in self.texts if t not in self.detailKeep]
		self.detailKeep = []

	def __RebuildDetail(self):
		self.__ClearDetail()
		if not self.rows:
			return
		r = self.rows[self.sel]
		e = EVENTS[r["key"]]
		K = self.detailKeep
		X = LEFT_W + 32
		# one cikan ikon (sag ust daire)
		self._Img("featured.png", REF_W - 30 - 82 - 20, HEAD + 26 - 20, keep=K)
		self._ItemIcon(e["icon"], REF_W - 30 - 41, HEAD + 26 + 41, 46, keep=K)
		# durum satiri
		self.eyebrow = self._Txt(self.__StateText(r), X, HEAD + 22, 14, C_EYEBROW, keep=K)
		self._Txt(e["name"], X, HEAD + 40, 32, C_H2, keep=K)
		d = self._Txt("", X, HEAD + 90, 16, C_DESC, keep=K)
		d.SetLimitWidth(int(round((REF_W - LEFT_W - 64 - 130) * self.k)))
		d.SetMultiLine()
		d.SetText(e["desc"])
		# geri sayim
		cy = HEAD + 160
		self.cnt = []
		labels = ("G\xdcN", "SAAT", "DAK\xddKA", "SAN\xddYE")
		for i in range(4):
			bx = X + i * 76
			self._Img("count_box.png", bx, cy, keep=K)
			n = self._Txt("00", bx + 34, cy + 5, 26, C_NUM, "center", keep=K)
			self._Txt(labels[i], bx + 34, cy + 37, 12, C_NUMLBL, "center", keep=K)
			self.cnt.append(n)
		self.cntTitle = self._Txt("", X + 4 * 76 + 10, cy + 17, 14, C_EYEBROW, keep=K)
		# bilgi izgarasi
		gy = cy + 54 + 14
		if r["gun"] > 0:
			bas = "%s \xb7 %s" % (self.__DayWordMixed(r), self.HM(r["bas"]))
			bit = "%s \xb7 %s" % (self.__DayWordMixed(r), self.HM(r["bit"]))
		else:
			bas = "\xdeimdi"
			bit = "GM kapatana kadar"
		cells = (("ETK\xddNL\xddK B\xd6LGES\xdd", e["zone"]), ("SEV\xddYE ARALI\xd0I", e["level"]),
			("BA\xdeLANGI\xc7", bas), ("B\xddT\xdd\xde", bit))
		for i in range(4):
			cx = X + (i % 2) * (INFO_W + 10)
			cyy = gy + (i / 2) * 64
			self._Img("info_box.png", cx, cyy, keep=K)
			self._Txt(cells[i][0], cx + 14, cyy + 7, 13, C_INFOLBL, keep=K)
			self._Txt(cells[i][1], cx + 14, cyy + 28, 17, C_INFOVAL, keep=K)
		# oduller
		ry = gy + 2 * 64 + 6
		t = self._Txt(e.has_key("chest") and "SANDIK \xdd\xc7ER\xdd\xd0\xdd" or "\xd6NE \xc7IKAN \xd6D\xdcLLER", X, ry, 14, C_RWTITLE, keep=K)
		self._Img("rewards_line.png", X + 190, ry + 8, keep=K)
		# sandik icerigi (sunucu special_item_group) varsa onu, yoksa one cikan odulleri goster;
		# adlar istemci esya tablosundan (item.GetItemName), 7 x 2 satir
		rewards = []
		if e.has_key("chest"):
			rewards = [(v, "") for v in e["chest"]]
		else:
			rewards = list(e["rewards"])
		if r["key"] == "vs" and r["odul"]:
			rewards = [(r["odul"], "Turnuva \xd6d\xfcl\xfc")] + [x for x in rewards if x[0] != 0]
		rewards = [x for x in rewards if x[0]][:REWARD_MAX]
		for i in range(len(rewards)):
			(vnum, label) = rewards[i]
			if not label:
				label = _ItemName(vnum)
			label = _Short(label, 13)
			rx = X + (i % REWARD_COLS) * 90
			ryy = ry + 22 + (i / REWARD_COLS) * 82
			self._Img("reward_slot.png", rx, ryy, keep=K)
			self._ItemIcon(vnum, rx + 29, ryy + 29, 40, keep=K)
			self._Txt(label, rx + 29, ryy + 61, 12, C_RWLBL, "center", keep=K)
		self.__UpdateCountdown(r, force=True)

	def __StateText(self, r):
		if r["aktif"]:
			return "\xdeU ANDA AKT\xddF"
		now = self.Now()
		left = r["bas"] - now
		if left < 0:
			return "\xdeU ANDA AKT\xddF"
		d = int((r["bas"] - self.__SrvMidnight()) / 86400)
		if d <= 0:
			h = int(left / 3600)
			if h >= 1:
				return "%d SAAT SONRA" % h
			return "%d DAK\xddKA SONRA" % max(1, int(left / 60))
		if d == 1:
			return "YARIN BA\xdeLIYOR"
		return "%d G\xdcN SONRA" % d

	def __UpdateCountdown(self, r, force=False):
		now = self.Now()
		if r["aktif"] and r["bit"] > now:
			left = r["bit"] - now
			title = "B\xddTMES\xddNE"
		elif r["aktif"]:
			left = 0
			title = "AKT\xddF"
		else:
			left = r["bas"] - now
			title = "BA\xdeLAMASINA"
		if left < 0:
			left = 0
		left = int(left)
		vals = (left / 86400, (left % 86400) / 3600, (left % 3600) / 60, left % 60)
		for i in range(4):
			self.cnt[i].SetText(_Pad2(vals[i]))
		self.cntTitle.SetText(title)
		self.eyebrow.SetText(self.__StateText(r))

	# ------------------------------------------------------------------ animasyon
	def __ApplyAnim(self, a, dy, alpha, textsOn):
		cx = self.winW / 2.0
		cy = self.winH / 2.0
		for (w, fx, fy) in self.imgs:
			try:
				w.SetPosition(int(round(cx + (fx - cx) * a)), int(round(cy + (fy - cy) * a + dy)))
				w.SetScale(self.k * a * self.__ImgBaseScale(w), self.k * a * self.__ImgBaseScale(w))
				w.SetAlpha(alpha)
			except:
				pass
		for (b, fx, fy, sx, sy) in self.btns:
			try:
				b.SetPosition(int(round(cx + (fx - cx) * a)), int(round(cy + (fy - cy) * a + dy)))
				if hasattr(wndMgr, "SetButtonScale"):
					wndMgr.SetButtonScale(b.hWnd, self.k * a * IMG_S * sx, self.k * a * IMG_S * sy)
			except:
				pass
		for t in self.texts:
			try:
				if textsOn:
					t.Show()
				else:
					t.Hide()
			except:
				pass

	def __ImgBaseScale(self, w):
		# esya ikonlari kendi olcegiyle (32 px -> hedef) yuklenir; _ItemIcon bunu w'ye yazar
		return getattr(w, "m2BaseScale", 1.0)

	def __EnsureRows(self, force=False):
		"""satir + detay yalniz veri degisince / 60 sn'den eskiyse (durum yazilari 'x saat sonra' tazelensin) kurulur."""
		t = app.GetTime()
		sig = repr(self.rows) + ":%d" % self.sel
		if force or sig != self.rowsSig or t - self.builtAt > 60.0:
			self.__RebuildRows()
			self.__RebuildDetail()
			self.rowsSig = sig
			self.builtAt = t
			self.__ApplyAnim(1.0, 0, 1.0, True)

	def Open(self):
		if not self.built:
			self.__Layout()
			self.__Build()
			self.built = True
			self.__ApplyAnim(1.0, 0, 1.0, True)
		if not self.rows:
			self.rows = self.__FallbackRows()
		self.__EnsureRows()
		self.state = "acik"
		self.lastTick = 0.0
		self.SetTop()
		self.Show()

	def Close(self):
		if not self.IsShow():
			return
		self.state = "kapali"
		self.Hide()

	def OnMouseLeftButtonUp(self):
		# pencere disina dokunma (govde disi) = kapat
		self.Close()
		return True

	def Tick(self):
		if not self.IsShow():
			return
		t = app.GetTime()
		if self.state == "aciliyor":
			p = (t - self.animT0) / OPEN_SEC
			if p >= 1.0:
				self.state = "acik"
				self.__ApplyAnim(1.0, 0, 1.0, True)
			elif p < TEXT_AT:
				q = _EaseOutCubic(p / TEXT_AT)
				self.__ApplyAnim(0.72 + (1.03 - 0.72) * q, 28 * self.k * (1.0 - q), q, False)
			else:
				q = _EaseInOut((p - TEXT_AT) / (1.0 - TEXT_AT))
				self.__ApplyAnim(1.03 - 0.03 * q, 0, 1.0, True)
		elif self.state == "kapaniyor":
			p = (t - self.animT0) / CLOSE_SEC
			if p >= 1.0:
				self.state = "kapali"
				self.Hide()
				return
			self.__ApplyAnim(1.0 - 0.15 * p, 0, 1.0 - p, False)
		# AKTIF rozetleri: yanip sonme (tasarim .live pulse 1.2s)
		if self.state == "acik" and self.badges:
			a = 0.55 + 0.45 * math.sin(t * 2.0 * math.pi / BADGE_PULSE_SEC)
			for b in self.badges:
				try:
					b.SetAlpha(a)
				except:
					pass
		# saat + geri sayim (saniyede ~4)
		if t - self.lastTick >= 0.25 and self.rows:
			self.lastTick = t
			try:
				self.clock.SetText(self.ClockText())
				self.__UpdateCountdown(self.rows[self.sel])
			except:
				pass
