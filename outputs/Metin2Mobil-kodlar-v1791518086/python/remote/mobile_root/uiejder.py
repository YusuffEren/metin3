# -*- coding: utf-8 -*-
# MOBIL - mobile_root/uiejder.py: EJDER \xdcYEL\xddK penceresi (ayl\xfdk \xfcyelik + 30 seviyelik iki \xf6d\xfcl hatt\xfd).
# \xdcRET\xddL\xddR: tools/ejder/uiejder_kaynak.py (UTF-8) -> tools/ejder/gen_uiejder.py -> bu dosya (cp1254 ka\xe7\xfd\xfel\xfd ASCII).
#
# KULLANICI (2026-10-05): \xfcyelik EP ile Nesne Market'ten al\xfdnan KARTLA a\xe7\xfdl\xfdr (71180 / 71181; sa\xf0 t\xfdk ya da
#   penceredeki "Kullan" = net.SendItemUsePacket). Kartlar takas edilir / sat\xfdl\xfdr / at\xfdl\xfdr. "eple de al\xfdnmaya devam
#   etsin" -> envanterde kart yoksa d\xfc\xf0me EP ile sat\xfdn al\xfdr (sunucu "s 1|2").
# KULLANICI (2026-10-05): prototip Desktop/Averos2-YildizKarti-Prototip/yildiz_karti.html onayland\xfd -> "oyuna uygulayal\xfdm,
#   \xe7ark\xfdn alt\xfdna g\xfczel buton, yaz\xfdlar net olsun g\xf6r\xfcns\xfcn", "fps d\xfc\xfe\xfcrmesin, kasma donmaya sebep olmas\xfdn", "ad\xfd Ejder \xdcyelik".
# Sunucu: server/quest/ejder_uyelik.lua (tools/ejder/ejder_veri.py \xfcretir). Her \xfeey sunucuda; buras\xfd yaln\xfdz g\xf6sterir ve ister.
#   istemci -> sunucu: event.QuestButtonClick(-2147483648 + qid) + net.SendQuestInputStringPacket(komut)
#     (sunucu input() bekler; getinputbegin / getinputend g\xf6rev penceresini bast\xfdr\xfdr - game.py constInfo.INPUT_IGNORE)
#   sunucu -> istemci: "Ejder <virg\xfcll\xfc alanlar>" -> game.py -> Cmd()
# HIZ / DONMA KORUMASI:
#   - pencere ilk A\xc7ILI\xdeTA kurulur; kapal\xfdyken kare ba\xfe\xfdna hi\xe7bir \xfeey yap\xfdlmaz (HUD 0,5 sn'de bir rozet say\xfds\xfdna bakar)
#   - \xf6d\xfcl \xfeeridi 8 sabit s\xfctun: kayd\xfdr\xfdnca yaln\xfdz i\xe7erik de\xf0i\xfeir (ikon yaln\xfdz vnum de\xf0i\xfeince y\xfcklenir); yaz\xfdlar de\xf0i\xfeince
#   - kare ba\xfe\xfd i\xfe: yaln\xfdz a\xe7\xfdkken parlama nabz\xfd (15 Hz), bildirim solmas\xfd, s\xfcr\xfckleme
#   - istek yan\xfdt beklerken yenisi g\xf6nderilmez (2 sn zaman a\xfe\xfdm\xfd); sunucu saniyede en \xe7ok 4 istek i\xfeler
import ui
import wndMgr
import app
import ejderveri as V

DIR = "mobile/ui/ejder/"
AET = "mobile/ui/aet/"
PT = "d:/ymir work/ui/pattern/"
PUB = "d:/ymir work/ui/public/"
CLOSE_UP = "mobile/ui/minimap/btn_close_sq.png"
CLOSE_DOWN = "mobile/ui/minimap/btn_close_sq_down.png"
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")
REF_H = 705.0
ZOOM = 1.0
FONT_BOOST = 1.4		# KULLANICI (2026-10-05): "yaz\xfdlar \xe7ok k\xfc\xe7\xfck, okunmuyor" (1.12 -> 1.4, en k\xfc\xe7\xfck 15)
FONT_MIN = 15
FONT_MAX = 18			# motor yaz\xfdy\xfd en \xe7ok 32 px pi\xfeirir; telefonda 18 \xfcst\xfc pikselli (bkz. uihedefkarti)
TEX = 3.0			# pi\xfemi\xfe dokular: 1 tasar\xfdm px = 3 doku px (bake_ejder.py)
AET_S = 705.0 / 1220.0		# Etkiler dokular\xfd (sekme)
TASMA = 0.02
YANIT_SURE = 2.0		# sn: yan\xfdt gelmezse yeni istek serbest
INPUT_SURE = 3.0		# sn: sunucu getinputend g\xf6ndermezse g\xf6rev penceresi bast\xfdrmas\xfd kalkar

# ---- \xf6l\xe7\xfcler (prototip px, yildiz_karti.html) ----
W_WIN, H_WIN = 1000, 580
UST = (16, 52, 968, 84)
SOL = (16, 146, 210, 418)
SEKME_Y = 146
PANEL = (236, 182, 748, 382)
SERIT = (364, 190, 578, 196)
KOL = 72
KOL_N = 8
BILGI = (246, 414, 728, 140)
GOREV_Y0 = 188
GOREV_BASLIK = 20
GOREV_H = 38
GOREV_ARA = 3
ONAY_W, ONAY_H = 500, 300
IPK_W = 260

# ---- renkler ----
C_KREM = 0xfff1e6c0
C_ALTIN = 0xffe8d08a
C_ALT = 0xffc9b88f
C_KAPALI = 0xff8f8470
C_SARI = 0xfff2c94c
C_MOR = 0xffb08fe0
C_OK = 0xff8fd16a
C_KOT = 0xffff7b5c
C_BASLIK = 0xfffeedc6
C_KOYU = 0xff1b1206
C_KUTU = 0x80000000
C_CIZGI = 0xff3d342a
C_KENAR = 0xff6b5a3e
AY = ("Ocak", "\xdeubat", "Mart", "Nisan", "May\xfds", "Haziran", "Temmuz", "A\xf0ustos", "Eyl\xfcl", "Ekim", "Kas\xfdm", "Aral\xfdk")
HATA = {1: "Bu \xf6d\xfcl i\xe7in seviyen yetmiyor.", 2: "Envanterin dolu \x97 \xf6d\xfcl i\xe7in yer a\xe7.", 3: "Ejder \xdcyelik gerekli.",
	4: "Yeterli Ejderha Paras\xfd (EP) yok.", 5: "Ejder \xdcyelik zaten aktif; kart harcanmad\xfd.", 6: "Bu zaten al\xfdnd\xfd.",
	7: "G\xf6rev hen\xfcz tamamlanmad\xfd."}
ENV_N = 180			# envanter yuvas\xfd (uiinventory 48 x 3 + 36)
KART_AD = {1: "Ejder \xdcyelik Kart\xfd", 2: "Ejder \xdcyelik Kart\xfd Plus"}


def _clamp(v, a, b):
	return a if v < a else (b if v > b else v)


def _nokta(n):
	s = str(abs(int(n)))
	out = ""
	while len(s) > 3:
		out = "." + s[-3:] + out
		s = s[:-3]
	return ("-" if n < 0 else "") + s + out


def _Otur(D, w, tex, s, rrs, z):
	"""par\xe7a yuvarlanm\xfd\xfe iki kenar aras\xfdna oturur (bkz. tools/ortak/doseme_denetim.py; eklem \xe7izgisi kalmas\xfdn)"""
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


# e\xfeya bilgisi (ad, ikon yolu, a\xe7\xfdklama, (en, boy)) - oyunun kendi item_proto / itemdesc'inden, \xf6nbellekli
_ITEM = {}


def _Item(v):
	v = int(v)
	r = _ITEM.get(v)
	if r is not None:
		return r
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


# ------------------------------------------------------------------ sunucu verisi (pencere olmasa da tutulur)
class _Model(object):
	def __init__(self):
		self.qid = -1
		self.known = False
		self.surum = 0
		self.odul = list(V.ODUL)		# sv-1 -> (fv, fa, yv, ya, yk)
		self._t = {}
		self.sezon = 0
		self.kalan = 0
		self.ay = 0
		self.puan = 0
		self.kart = 0
		self.fm = 0
		self.ym = 0
		self.ep = -1
		self.cins = 0
		self.gorev = [0] * 8
		self.gm = 0
		self.hm = 0
		self.gorevT = 0.0		# ilerleme geldi\xf0i an (dakika g\xf6revleri yerelde ilerler)
		self.sig = 0
		self.bekle = 0.0		# yan\xfdt beklenen istek zaman\xfd
		self.ignT = 0.0			# INPUT_IGNORE'u biz a\xe7t\xfdk (zaman)
		self.lastB = -100.0
		self._rozet = None

	def Seviye(self):
		return min(V.MAKS, 1 + self.puan // V.SV_PUAN)

	def Odul(self, sv, ejder):
		"""-> (vnum, adet) cinsiyete g\xf6re"""
		(fv, fa, yv, ya, yk) = self.odul[sv - 1]
		if not ejder:
			return (fv, fa)
		if yk > 0 and self.cins == 1:
			return (yk, ya)
		return (yv, ya)

	def Alindi(self, sv, ejder):
		m = self.ym if ejder else self.fm
		return (m >> (sv - 1)) & 1 == 1

	def Durum(self, sv, ejder):
		if self.Alindi(sv, ejder):
			return "alindi"
		if ejder and self.kart < 1:
			return "kilit"
		if sv <= self.Seviye():
			return "hazir"
		return "bekle"

	def Ilerleme(self, i):
		n = self.gorev[i]
		if i in (2, 7):		# dakika g\xf6revleri: geli\xfeten bu yana yerelde say
			n += int((app.GetTime() - self.gorevT) // 60) if self.gorevT > 0 else 0
		return min(n, V.GOREV[i][2])

	def GorevAlindi(self, i):
		if i < 4:
			return (self.gm >> i) & 1 == 1
		return (self.hm >> (i - 4)) & 1 == 1

	def GorevHazir(self, i):
		return not self.GorevAlindi(i) and self.Ilerleme(i) >= V.GOREV[i][2]

	def HazirOdul(self):
		n = 0
		for sv in range(1, self.Seviye() + 1):
			if not self.Alindi(sv, False):
				n += 1
			if self.kart >= 1 and not self.Alindi(sv, True):
				n += 1
		return n

	def HazirGorev(self):
		n = 0
		for i in range(8):
			if self.GorevHazir(i):
				n += 1
		return n


M = _Model()
_WND = [None]


def Cmd(s):
	"""game.py "Ejder <alanlar>" -> burada. Hata oyunu durdurmas\xfdn."""
	try:
		a = s.split(",")
		k = a[0]
		t = app.GetTime()
		if k == "Q":
			M.qid = int(a[1])
		elif k == "T":
			sr = int(a[1])
			ilk = int(a[2])
			v = [int(x) for x in a[3:]]
			for j in range(0, len(v) - 4, 5):
				sv = ilk + j // 5
				if 1 <= sv <= V.MAKS:
					M._t[sv] = tuple(v[j:j + 5])
			if len(M._t) == V.MAKS:
				M.odul = [M._t[sv] for sv in range(1, V.MAKS + 1)]
				M.surum = sr
				M._t = {}
		elif k == "D":
			M.sezon = int(a[1])
			M.kalan = int(a[2])
			M.ay = int(a[3])
			M.puan = int(a[4])
			M.kart = int(a[5])
			M.fm = int(a[6])
			M.ym = int(a[7])
			if int(a[8]) >= 0:
				M.ep = int(a[8])
			M.cins = int(a[9])
			M.known = True
		elif k == "G":
			M.gorev = [int(x) for x in a[1:9]]
			M.gm = int(a[9])
			M.hm = int(a[10])
			M.gorevT = t
			M.bekle = 0.0		# yan\xfdt sonu (her yan\xfdt D + G ile biter)
		elif k == "S":
			w = _WND[0]
			if w:
				w.OnSonuc([int(x) for x in a[1:]])
		elif k == "H":
			w = _WND[0]
			if w:
				w.Bildir(HATA.get(int(a[1]), "\xdd\xfelem yap\xfdlamad\xfd."), True)
		M.sig += 1
	except:
		import dbg
		dbg.TraceError("uiejder.Cmd %r" % (s,))


def _Gonder(komut):
	"""sunucuya istek: yan\xfdt beklenirken yenisi gitmez"""
	t = app.GetTime()
	if M.qid < 0:
		return False
	if M.bekle > 0.0 and t - M.bekle < YANIT_SURE:
		return False
	try:
		import event
		import net
		import constInfo
		constInfo.INPUT_IGNORE = 1		# sunucunun input() beti\xf0i g\xf6rev penceresi a\xe7mas\xfdn (getinputend kapat\xfdr)
		M.ignT = t
		event.QuestButtonClick(-2147483648 + M.qid)
		net.SendQuestInputStringPacket(komut)
		M.bekle = t
		return True
	except:
		import dbg
		dbg.TraceError("uiejder: istek gonderilemedi")
		return False


def Guvenlik():
	"""HUD her 0,5 sn: sunucu getinputend g\xf6ndermediyse g\xf6rev penceresi bast\xfdrmas\xfdn\xfd kald\xfdr"""
	if M.ignT > 0.0 and app.GetTime() - M.ignT > INPUT_SURE:
		M.ignT = 0.0
		try:
			import constInfo
			constInfo.INPUT_IGNORE = 0
		except:
			pass


def Rozet():
	"""HUD rozeti: al\xfdnabilir \xf6d\xfcl + puan\xfd al\xfdnabilir g\xf6rev"""
	if not M.known:
		return 0
	return M.HazirOdul() + M.HazirGorev()


def Toggle():
	w = _WND[0]
	if w is None:
		w = _WND[0] = EjderWindow()
	if w.IsOpen():
		w.Close()
	else:
		w.Open()


def _KartSay():
	"""envanterdeki \xfcyelik kartlar\xfd -> ({1: adet, 2: adet}, {1: ilk yuva, 2: ilk yuva})"""
	n = {1: 0, 2: 0}
	yuva = {1: -1, 2: -1}
	try:
		import player
		for i in range(ENV_N):
			v = player.GetItemIndex(i)
			if v == V.KART or v == V.KART_PLUS:
				t = 1 if v == V.KART else 2
				try:
					n[t] += max(1, int(player.GetItemCount(i)))
				except:
					n[t] += 1
				if yuva[t] < 0:
					yuva[t] = i
	except:
		pass
	return (n, yuva)


def DestroyAll():
	w = _WND[0]
	_WND[0] = None
	if w:
		w.Destroy()


# ------------------------------------------------------------------ k\xf6kler
class _Root(ui.Window):
	"""pencere k\xf6k\xfc: i\xe7indeki dokunu\xfeu yutar; \xfeerit s\xfcr\xfckleme / yuva dokunu\xfeu burada"""

	def __init__(self, owner, outside=True):
		ui.Window.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		if outside:
			self.AddFlag("hide_on_outside")
		self.owner = owner

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		o = self.owner
		if o:
			o._Bas(self)
		return True

	def OnMouseLeftButtonUp(self):
		o = self.owner
		if o:
			o._Birak(self)
		return True

	def OnOutsideTap(self):
		o = self.owner
		if o:
			o._Disari(self)

	def OnOutsideTapUI(self):
		o = self.owner
		if o:
			o._SurukleIptal()

	def OnPressEscapeKey(self):
		o = self.owner
		if o:
			o._Esc()
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
class EjderWindow(object):

	def __init__(self):
		self.built = False
		self.open = False
		self.keep = []
		self.tab = "odul"
		self.ust = 0			# \xfeeridin ilk s\xfctunu (seviye - 1)
		self.ortaladi = False
		self.surukle = None		# (fare x, ust, hareket etti mi)
		self.sig = None
		self.ustSig = None
		self.gorevSig = None
		self.seritSig = None
		self.nabiz = -1
		self.bildT = -1.0
		self.ipkT = -1.0
		self.onayTip = 0
		self.kartN = {1: 0, 2: 0}
		self.kartYuva = {1: -1, 2: -1}
		self.kartT = -100.0
		self.onayKart = False
		self.nabizVar = False
		self.bildT0 = -100.0

	# ---------------- \xf6l\xe7ek yard\xfdmc\xfdlar\xfd
	def __Scale(self):
		self.scrW = wndMgr.GetScreenWidth()
		self.scrH = wndMgr.GetScreenHeight()
		k = self.scrH / REF_H
		self.z = min(ZOOM * k, 0.98 * self.scrW / W_WIN, 0.97 * self.scrH / H_WIN)

	def P(self, v):
		return int(round(v * self.z))

	def F(self, pt):
		return "Tahoma:%d" % max(FONT_MIN, min(FONT_MAX, int(round(pt * self.z * FONT_BOOST))))

	def _PImg(self, parent, path, x, y, sx=1.0, sy=1.0, keep=None):
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(path)
		max(0, 0)		# LoadImage bekleyen hatas\xfdn\xfd burada tetikle
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		w.SetScale(sx * self.z, sy * self.z)
		w.SetPosition(self.P(x), self.P(y))
		w.Show()
		(self.keep if keep is None else keep).append(w)
		return w

	def _Img(self, parent, name, x, y, show=True):
		"""pi\xfemi\xfe doku (TEX)"""
		w = self._PImg(parent, DIR + name, x, y, 1.0 / TEX, 1.0 / TEX)
		if not show:
			w.Hide()
		return w

	def _Tile(self, parent, path, x, y, w, h, tw, th, sx=1.0, sy=1.0):
		img = self._PImg(parent, path, x, y, sx, sy)
		(zx, r) = _Otur(self.P(x + w) - self.P(x), w, tw, sx, HAS_RRS, self.z)
		(zy, b) = _Otur(self.P(y + h) - self.P(y), h, th, sy, HAS_RRS, self.z)
		img.SetScale(zx, zy)
		img.SetRenderingRect(0.0, 0.0, r, b)
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

	def _Kutu(self, parent, x, y, w, h, fill=C_KUTU):
		return (self._Rect(parent, x, y, w, h, fill), self._Rect(parent, x, y, w, h, C_CIZGI, False))

	def _Txt(self, parent, pt, color, x, y, align="left", outline=True, vc=True):
		"""vc: y = yaz\xfdn\xfdn dikey ortas\xfd"""
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
		if vc:
			t.SetVerticalAlignCenter()
		t.SetPackedFontColor(color)
		t.SetPosition(self.P(x), self.P(y))
		t.Show()
		self.keep.append(t)
		return t

	def _TW(self, t):
		"""yaz\xfd geni\xfeli\xf0i. MOTOR HATASI (native GrpTextInstance: WORD m_textWidth += float advance) her harfte k\xfcsurat\xfd
		keser -> uzun yaz\xfd ekrandakinden ~1 px/harf DAR \xf6l\xe7\xfcl\xfcr (KULLANICI 2026-10-05: "uyar\xfd yaz\xfds\xfd arka plan\xfdna s\xfd\xf0m\xfdyor").
		Harf ba\xfe\xfdna 1 px eklenir (\xfcst s\xfdn\xfdr; motor d\xfczelince yaln\xfdz biraz pay kal\xfdr)."""
		try:
			w = t.GetTextSize()[0]
			try:
				w += len(t.GetText())
			except:
				pass
			return w
		except:
			return 0

	def _Fit(self, t, text, maxw):
		t.SetText(text)
		if self._TW(t) <= maxw:
			return
		s = text
		while len(s) > 1 and self._TW(t) > maxw:
			s = s[:-1]
			t.SetText(s.rstrip() + "..")

	def _Btn(self, parent, x, y, w, h, yazi, func, buyuk=False, pt=15):
		"""oyunun orta / b\xfcy\xfck d\xfc\xf0mesi (61x21 / 88x21) w x h tasar\xfdm px'e; yaz\xfd ortada"""
		tw = 88.0 if buyuk else 61.0
		ad = "large_button_0%d.sub" if buyuk else "middle_button_0%d.sub"
		b = ui.Button()
		b.SetParent(parent)
		b.SetUpVisual(PUB + ad % 1)
		b.SetOverVisual(PUB + ad % 2)
		b.SetDownVisual(PUB + ad % 3)
		x0, y0 = self.P(x), self.P(y)
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, (self.P(x + w) - x0) / tw, (self.P(y + h) - y0) / 21.0)
		b.SetPosition(x0, y0)
		b.SetEvent(func)
		b.Show()
		self.keep.append(b)
		t = self._Txt(parent, pt, C_KREM, x + w / 2.0, y + h / 2.0 - 0.5, "center")
		t.SetText(yazi)
		b._yazi = t
		b._kapali = self._Rect(parent, x + 1, y + 1, w - 2, h - 2, 0x8c000000)
		b._kapali.Hide()
		b._acik = True
		b._geo = (x, y, w, h)
		return b

	def _BtnDurum(self, b, yazi, acik, renk=C_KREM):
		b._yazi.SetText(yazi)
		b._yazi.SetPackedFontColor(renk if acik else C_KAPALI)
		b._acik = acik
		if acik:
			b._kapali.Hide()
		else:
			b._kapali.Show()

	def _Board(self, parent, W, H):
		self._Tile(parent, PT + "board_base.tga", 32, 32, W - 64, H - 64, 128, 128)
		self._Tile(parent, PT + "board_line_top.tga", 32, 0, W - 64, 32, 128, 32)
		self._Tile(parent, PT + "board_line_bottom.tga", 32, H - 32, W - 64, 32, 128, 32)
		self._Tile(parent, PT + "board_line_left.tga", 0, 32, 32, H - 64, 32, 128)
		self._Tile(parent, PT + "board_line_right.tga", W - 32, 32, 32, H - 64, 32, 128)
		for (n, cx, cy) in (("lefttop", 0, 0), ("righttop", W - 32, 0), ("leftbottom", 0, H - 32), ("rightbottom", W - 32, H - 32)):
			self._Tile(parent, PT + "board_corner_%s.tga" % n, cx, cy, 32, 32, 32, 32)

	def _Baslik(self, parent, W, kapat):
		"""envanterin geni\xfe ba\xfel\xfdk \xe7ubu\xf0u (titlebar sol + orta x1.6, sa\xf0 kapak yok) + kare \xe7arp\xfd. D\xf6n\xfc\xfe: ba\xfel\xfdk yaz\xfds\xfd x"""
		x, y, w = 8, 7, W - 15
		bh = 23 * 1.6
		bw = 32 * 1.6
		self._Tile(parent, PT + "titlebar_left.tga", x, y, bw, bh, 32, 32, 1.6, 1.6)
		self._Tile(parent, PT + "titlebar_center.tga", x + bw, y, w - bw, bh, 32, 32, 1.6, 1.6)
		c = bh * 1.15
		b = ui.Button()
		b.SetParent(parent)
		b.SetUpVisual(CLOSE_UP)
		b.SetOverVisual(CLOSE_UP)
		b.SetDownVisual(CLOSE_DOWN)
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, c * self.z / 64.0, c * self.z / 64.0)
		b.SetPosition(self.P(x + w - c), self.P(y + (bh - c) / 2.0))
		b.SetEvent(kapat)
		b.Show()
		self.keep.append(b)
		# parmak boyu dokunma alan\xfd
		hb = _Hit()
		hb.SetParent(parent)
		hb.SetPosition(self.P(x + w - c - 8), 0)
		hb.SetSize(self.P(c + 16), self.P(y + bh + 6))
		hb.onUp = kapat
		hb.Show()
		self.keep.append(hb)
		return y + bh / 2.0

	def _Ikon(self, parent, kutu):
		"""e\xfeya ikonu (vnum sonradan); kutu = tasar\xfdm px kare"""
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.Hide()
		w._kutu = kutu
		w._v = -1
		w._yol = ""
		w._boy = (1, 1)
		self.keep.append(w)
		return w

	def _IkonAyarla(self, w, vnum, cx, cy, alpha=1.0):
		"""ikonu (cx, cy) tasar\xfdm px merkezine koy; vnum de\xf0i\xfemediyse y\xfckleme yok"""
		vnum = int(vnum)
		if w._v != vnum:
			w._v = vnum
			w._yol = ""
			if vnum > 0:
				(ad, path, ac, boy) = _Item(vnum)
				if path:
					try:
						w.LoadImage(path)
						max(0, 0)
						w._yol = path
						w._boy = boy
						# MANTIKSAL boy = 32 x yuva (HD ikon density 4). GetWidth'e G\xdcVEN\xddLMEZ (bkz. uicark)
						s = w._kutu * self.z / (32.0 * max(boy[0], boy[1]))
						w.SetScale(s, s)
						w._s = s
					except:
						w._yol = ""
		if not w._yol:
			w.Hide()
			return
		s = w._s
		(bx, by) = w._boy
		w.SetPosition(int(round(cx * self.z - 16.0 * bx * s)), int(round(cy * self.z - 16.0 * by * s)))
		w.SetAlpha(alpha)
		w.Show()

	# ---------------- kurulum (ilk a\xe7\xfdl\xfd\xfeta, bir kez)
	def __Build(self):
		self.__Scale()
		z = self.z
		w = _Root(self)
		w.SetSize(self.P(W_WIN), self.P(H_WIN))
		w.SetPosition((self.scrW - self.P(W_WIN)) // 2, max(0, (self.scrH - self.P(H_WIN)) // 2))
		w.Hide()
		self.keep.append(w)
		self.root = w
		self._Board(w, W_WIN, H_WIN)
		ty = self._Baslik(w, W_WIN, ui.__mem_func__(self.Close))
		self.logo = self._Ikon(w, 30)
		self._IkonAyarla(self.logo, 30180, 40, ty)
		t = self._Txt(w, 20, C_BASLIK, 62, ty)
		t.SetText("Ejder \xdcyelik")
		self.cipX = 62 + self._TW(t) / z + 14
		self.cip = self._Kutu(w, self.cipX, ty - 11, 200, 22, 0x8c000000)
		self.cip[1].SetColor(C_KENAR)
		self.cipT = self._Txt(w, 13, C_ALTIN, self.cipX + 9, ty)
		# ---- \xfcst b\xf6l\xfcm: seviye + puan + kart + sat\xfdn alma
		self._Kutu(w, *UST)
		self._Img(w, "sv.png", 30, 65)
		self.svT = self._Txt(w, 22, C_KOYU, 59, 94, "center", False)
		self.svL = self._Txt(w, 16, C_KREM, 102, 72)
		self.svL.SetText("Ejder Seviyesi")
		self.svT2 = self._Txt(w, 16, C_ALTIN, 102, 72)
		self._Rect(w, 102, 92, 380, 16, 0xff1c140d)
		self._Rect(w, 102, 92, 380, 16, C_KENAR, False)
		self.puanDol = self._Img(w, "dol.png", 104, 94)
		self.puanT = self._Txt(w, 12.5, C_ALT, 102, 122)
		self.kartL = self._Txt(w, 14, C_KREM, 520, 66)
		self.kartT2 = self._Txt(w, 14, C_MOR, 520, 66)
		self.kartA1 = self._Txt(w, 11, C_ALT, 520, 86.5)
		self.kartA2 = self._Txt(w, 11, C_ALT, 520, 105)
		self.epT = self._Txt(w, 13, C_ALTIN, 520, 125)
		self.alB = self._Btn(w, 738, 60, 232, 34, "", ui.__mem_func__(self.__OnKart1), True, 14)
		self.plusB = self._Btn(w, 738, 98, 232, 34, "", ui.__mem_func__(self.__OnKart2), True, 14)
		# ---- sol: ay\xfdn \xf6d\xfcl\xfc
		self._Kutu(w, *SOL)
		self._Txt(w, 16, C_ALTIN, SOL[0] + SOL[2] / 2.0, 166, "center").SetText("Ay\xfdn \xd6d\xfcl\xfc")
		self.__Yuva(w, 65, 184, 112, 112)
		self.anaIk = self._Ikon(w, 96)
		self.anaAd = self._Txt(w, 15, C_KREM, SOL[0] + SOL[2] / 2.0, 314, "center")
		self.anaAlt = self._Txt(w, 12, C_MOR, SOL[0] + SOL[2] / 2.0, 334, "center")
		self._Rect(w, 30, 352, 182, 1, C_CIZGI)
		self.__Yuva(w, 38, 366, 56, 112)
		self.kosIk = self._Ikon(w, 100)
		self.__Yuva(w, 132, 366, 56, 56)
		self.sacIk = self._Ikon(w, 48)
		self._Txt(w, 12, C_ALT, 112, 440).SetText("Kost\xfcm + sa\xe7")
		self._Txt(w, 12, C_ALT, 112, 456).SetText("Sv 10 / Sv 20")
		self._Txt(w, 12, C_ALT, SOL[0] + SOL[2] / 2.0, 506, "center").SetText("Ejder \xdcyelik Plus ile")
		t = self._Txt(w, 12, C_SARI, SOL[0] + SOL[2] / 2.0, 524, "center")
		t.SetText("hemen 10 seviye atlar.")
		self.solHit = []
		for (x, y, ww, hh, key) in ((65, 184, 112, 112, "ana"), (38, 366, 56, 112, "kos"), (132, 366, 56, 56, "sac")):
			h = _Hit()
			h.SetParent(w)
			h.SetPosition(self.P(x), self.P(y))
			h.SetSize(self.P(ww), self.P(hh))
			h.onUp = lambda k0=key: self.__OnSol(k0)
			h.Show()
			self.keep.append(h)
		# ---- sekmeler + T\xfcm\xfcn\xfc Al
		self.tabs = {}
		for (j, key, ad) in ((0, "odul", "\xd6d\xfcller"), (1, "gorev", "G\xf6revler")):
			x = 236 + j * 131
			b = ui.Button()
			b.SetParent(w)
			b.SetUpVisual(AET + "tab_up.png")
			b.SetOverVisual(AET + "tab_over.png")
			b.SetDownVisual(AET + "tab_on.png")
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(b.hWnd, z * AET_S, z * AET_S)
			b.SetPosition(self.P(x), self.P(SEKME_Y))
			b.SetEvent(lambda k0=key: self.__OnTab(k0))
			b.Show()
			self.keep.append(b)
			lt = self._Txt(w, 15, C_KREM, x + 62.5, SEKME_Y + 15.5, "center")
			lt.SetText(ad)
			self.tabs[key] = (b, lt, x)
		self.tabOn = None
		self.rozet = self._PImg(w, "mobile/ui/etk/hud_etk_badge.tga", 0, 0, 22 / 32.0, 22 / 32.0)
		self.rozet.Hide()
		self.rozetT = self._Txt(w, 11.5, 0xffffffff, 0, 0, "center")
		self.rozetT.Hide()
		# ---- \xf6d\xfcller / g\xf6revler panelleri: kendi katmanlar\xfdnda (sekme de\xf0i\xfeince katman gizlenir; par\xe7alar\xfdn durumu korunur)
		self.katOdul = self.__Katman(w)
		self.katGorev = self.__Katman(w)
		self.tumB = self._Btn(self.katOdul, 836, SEKME_Y, 148, 31, "T\xfcm\xfcn\xfc Al", ui.__mem_func__(self.__OnTumu), False, 14)
		self._Kutu(self.katOdul, *PANEL)
		self.__BuildOdul(self.katOdul)
		self.__BuildGorev(self.katGorev)
		self.katGorev.Hide()
		# ---- ipucu kutusu (en \xfcstte)
		self.__BuildIpucu(w)
		self.__BuildOnay()
		self.__BuildBildirim()
		self.built = True

	def __Katman(self, parent):
		k = ui.Window()
		k.SetParent(parent)
		k.AddFlag("not_pick")
		k.SetPosition(0, 0)
		k.SetSize(self.P(W_WIN), self.P(H_WIN))
		k.Show()
		self.keep.append(k)
		return k

	def __Yuva(self, parent, x, y, w, h, keep=None):
		"""slot_base (32x32) w x h"""
		img = self._PImg(parent, PUB + "slot_base.sub", x, y, w / 32.0, h / 32.0, keep)
		return img

	def __BuildOdul(self, w):
		y0 = SERIT[1]
		self._Txt(w, 14, C_KREM, 246, y0 + 28).SetText("\xdccretsiz")
		self._Txt(w, 11.5, C_ALT, 246, y0 + 44).SetText("herkes")
		self._Txt(w, 12, C_ALT, 246, y0 + 84).SetText("Seviye")
		self._Txt(w, 14, C_MOR, 246, y0 + 134).SetText("Ejder")
		self._Txt(w, 11.5, C_ALT, 246, y0 + 150).SetText("\xfcyelere")
		# oklar (kayd\xfdrma: 4 s\xfctun)
		self.okL = self.__Ok(w, 330, 248, "\x8b", -4)
		self.okR = self.__Ok(w, 948, 248, "\x9b", 4)
		# s\xfctunlar
		self.kol = []
		for c in range(KOL_N):
			x = SERIT[0] + c * KOL
			col = {"x": x}
			col["hl"] = self._Rect(w, x + 4, y0, KOL - 8, SERIT[3], 0x14f2c94c)
			col["hlb"] = self._Rect(w, x + 4, y0, KOL - 8, SERIT[3], 0x59f2c94c, False)
			for (key, yy) in (("f", y0 + 6), ("y", y0 + 112)):
				s = {}
				s["yuva"] = self.__Yuva(w, x + 8, yy, 56, 56)
				if key == "y":
					s["mor"] = self._Rect(w, x + 9, yy + 1, 54, 54, 0xbfb08fe0, False)
					s["mor2"] = self._Rect(w, x + 10, yy + 2, 52, 52, 0x80b08fe0, False)
				s["ik"] = self._Ikon(w, 48)
				s["adet"] = self._Txt(w, 12, 0xffffffff, x + 61, yy + 48, "right")
				s["parla"] = self._Img(w, "parla.png", x, yy - 8, False)
				s["tik"] = self._Img(w, "tik.png", x + 21, yy + 13, False)
				s["kilit"] = self._Img(w, "kilit.png", x + 46, yy + 2, False)
				s["y"] = yy
				col[key] = s
			col["pill"] = self._Rect(w, x + 8, y0 + 73, 56, 22, 0x99000000)
			col["pillb"] = self._Rect(w, x + 8, y0 + 73, 56, 22, C_KENAR, False)
			col["no"] = self._Txt(w, 13, C_ALT, x + 36, y0 + 84, "center")
			col["no2"] = self._Txt(w, 13, C_KOYU, x + 36, y0 + 84, "center", False)
			col["ozel"] = self._Txt(w, 11.5, C_SARI, x + 36, y0 + 180, "center")
			col["sig"] = None
			self.kol.append(col)
		# kayd\xfdrma \xe7ubu\xf0u
		self._Rect(w, SERIT[0], 394, SERIT[2], 8, 0x73000000)
		self._Rect(w, SERIT[0], 394, SERIT[2], 8, C_CIZGI, False)
		self.tut = self._Rect(w, SERIT[0] + 1, 395, 60, 6, C_ALTIN)
		# bilgi kutusu
		self._Kutu(w, BILGI[0], BILGI[1], BILGI[2], BILGI[3], 0x59000000)
		self._Txt(w, 14, C_ALTIN, 262, 434).SetText("Ejder \xdcyelik ile neler kazan\xfdrs\xfdn?")
		satir = ("\x95 Sand\xfdklar, Ejderha Tanr\xfd iksirleri, tak\xfdlar, y\xfcz\xfckler",
			"\x95 Kost\xfcm (Sv 10), sa\xe7 (Sv 20), Kral Kaplan\xfd bine\xf0i (Sv 27)",
			"\x95 Son seviyede Alt\xfdn Kral Kaplan\xfd \xb7 g\xf6revlerle puan topla",
			"\x95 \xd6d\xfcller ay sonuna kadar al\xfdn\xfdr; her ay yeni sezon")
		for (j, s) in enumerate(satir):
			self._Txt(w, 13, C_ALT, 262, 460 + j * 22).SetText(s)

	def __Ok(self, w, x, y, ch, adim):
		self._Rect(w, x, y, 30, 56, 0x8c000000)
		self._Rect(w, x, y, 30, 56, C_KENAR, False)
		t = self._Txt(w, 20, C_ALTIN, x + 15, y + 27, "center")
		t.SetText(ch)
		h = _Hit()
		h.SetParent(w)
		h.SetPosition(self.P(x - 4), self.P(y - 10))
		h.SetSize(self.P(38), self.P(76))
		h.onUp = lambda a=adim: self.__Kaydir(self.ust + a)
		h.Show()
		self.keep.append(h)
		return h

	def __BuildGorev(self, w):
		self._Kutu(w, *PANEL)
		self.grup = []
		self.gor = []
		y = GOREV_Y0
		for (tur, ad, ack) in ((0, "G\xfcnl\xfck G\xf6revler", "yenilenme 00:00"), (1, "Haftal\xfdk G\xf6revler", "yenilenme Pazartesi")):
			self._Txt(w, 14, C_ALTIN, 248, y + GOREV_BASLIK / 2.0).SetText(ad)
			self._Txt(w, 12, C_ALT, 972, y + GOREV_BASLIK / 2.0, "right").SetText(ack)
			y += GOREV_BASLIK
			for (i, g) in enumerate(V.GOREV):
				if g[0] != tur:
					continue
				r = {"i": i, "y": y}
				self._Kutu(w, 246, y, 728, GOREV_H)
				cy = y + GOREV_H / 2.0
				r["ad"] = self._Txt(w, 14, C_KREM, 258, cy)
				r["ad"].SetText(g[1])
				self._Rect(w, 560, cy - 11, 190, 22, 0xff1c140d)
				self._Rect(w, 560, cy - 11, 190, 22, C_KENAR, False)
				r["dol"] = self._Img(w, "dol.png", 562, cy - 9)
				r["n"] = self._Txt(w, 12, 0xffffffff, 655, cy, "center")
				r["p"] = self._Txt(w, 13, C_SARI, 840, cy, "right")
				r["p"].SetText("+%d puan" % g[3])
				r["btn"] = self._Btn(w, 864, cy - 15, 100, 30, "Devam", lambda i0=i: self.__OnGorev(i0), False, 14)
				r["bitti"] = self._Txt(w, 13, C_OK, 924, cy, "center")
				r["bitti"].SetText("Al\xfdnd\xfd")
				r["tik"] = self._PImg(w, DIR + "tik.png", 880, cy - 11, 22.0 / 90, 22.0 / 90)
				r["sig"] = None
				self.gor.append(r)
				y += GOREV_H + GOREV_ARA

	def __BuildIpucu(self, w):
		k0 = len(self.keep)
		self.ipkBar = self._Rect(w, 0, 0, IPK_W, 80, 0xf00a0805)
		self.ipkBox = self._Rect(w, 0, 0, IPK_W, 80, C_KENAR, False)
		self.ipkAd = self._Txt(w, 14, C_ALTIN, 0, 0, "left", True, False)
		self.ipkA1 = self._Txt(w, 12.5, C_KREM, 0, 0, "left", True, False)
		self.ipkA2 = self._Txt(w, 12.5, C_KREM, 0, 0, "left", True, False)
		self.ipkAlt = self._Txt(w, 12, C_ALT, 0, 0, "left", True, False)
		self.ipkW = self.keep[k0:]
		for x in self.ipkW:
			x.Hide()

	def __BuildOnay(self):
		pd = _Root(self, False)
		pd.SetSize(self.scrW, self.scrH)
		pd.SetPosition(0, 0)
		b = ui.Bar()
		b.SetParent(pd)
		b.AddFlag("not_pick")
		b.SetColor(0x8c000000)
		b.SetPosition(0, 0)
		b.SetSize(self.scrW, self.scrH)
		b.Show()
		self.keep.append(b)
		pd.Hide()
		self.keep.append(pd)
		self.perde = pd
		p = _Root(self, False)
		p.SetSize(self.P(ONAY_W), self.P(ONAY_H))
		p.SetPosition((self.scrW - self.P(ONAY_W)) // 2, (self.scrH - self.P(ONAY_H)) // 2)
		p.Hide()
		self.keep.append(p)
		self.onay = p
		self._Board(p, ONAY_W, ONAY_H)
		ty = self._Baslik(p, ONAY_W, ui.__mem_func__(self.__OnayKapat))
		self.onayBas = self._Txt(p, 20, C_BASLIK, 62, ty)
		self.onayLogo = self._Ikon(p, 30)
		self._IkonAyarla(self.onayLogo, 30180, 40, ty)
		self.onaySoru = self._Txt(p, 18, C_KREM, ONAY_W / 2.0, 72, "center")
		self.onayFiyat = self._Txt(p, 15, C_ALTIN, ONAY_W / 2.0, 98, "center")
		self._Kutu(p, 24, 118, 452, 110)
		self.onayL = [self._Txt(p, 13, C_ALT, 40, 138 + j * 24) for j in range(4)]
		self.evetB = self._Btn(p, 126, 244, 107, 32, "Kullan", ui.__mem_func__(self.__OnEvet), False, 16)
		self._Btn(p, 267, 244, 107, 32, "Vazge\xe7", ui.__mem_func__(self.__OnayKapat), False, 16)

	def __BuildBildirim(self):
		b = ui.Window("TOP_MOST")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(b.hWnd, 1.0)
		b.AddFlag("not_pick")
		b.SetSize(self.scrW, self.P(40))
		b.SetPosition(0, max(2, (self.scrH - self.P(H_WIN)) // 2 - self.P(44)))	# pencerenin USTUNDE (icerigi kapatmasin)
		b.Hide()
		self.keep.append(b)
		self.bild = b
		self.bildBar = self._Rect(b, 0, 0, 10, 36, 0xeb0a0805)
		self.bildBox = self._Rect(b, 0, 0, 10, 36, C_KENAR, False)
		self.bildT = self._Txt(b, 15, C_OK, 0, 18, "center")

	# ---------------- a\xe7 / kapa
	def IsOpen(self):
		return self.open

	def Open(self):
		if not self.built:
			self.__Build()
		self.open = True
		self.root.Show()
		self.root.SetTop()
		self.sig = None
		self.ustSig = None
		self.gorevSig = None
		self.seritSig = None
		t = app.GetTime()
		self.__KartYenile(True)
		if not M.known or t - M.lastB > 5.0:
			if _Gonder("b %d" % M.surum):
				M.lastB = t
		self.Tick()

	def Close(self):
		self.open = False
		self.surukle = None
		if self.built:
			self.root.Hide()
			self.__IpucuGizle()
			self.__OnayKapat()

	def Destroy(self):
		self.Close()
		try:
			self.bild.Hide()
		except:
			pass
		for r in (getattr(self, "root", None), getattr(self, "perde", None), getattr(self, "onay", None)):
			if r:
				r.owner = None
		self.keep = []
		self.kol = []
		self.gor = []
		self.tabs = {}
		self.ipkW = []
		self.built = False

	# ---------------- olaylar (k\xf6kler)
	def _Bas(self, kok):
		if kok is not self.root:
			return
		try:
			(mx, my) = wndMgr.GetMousePosition()
			(gx, gy) = self.root.GetGlobalPosition()
		except:
			return
		x = (mx - gx) / self.z
		y = (my - gy) / self.z
		self.__IpucuGizle()
		if self.tab == "odul" and SERIT[0] <= x <= SERIT[0] + SERIT[2] and SERIT[1] <= y <= SERIT[1] + SERIT[3] + 20:
			self.surukle = (mx, self.ust, False, x, y)

	def _Birak(self, kok):
		s = self.surukle
		self.surukle = None
		if kok is not self.root or s is None:
			return
		if not s[2]:
			self.__SeritDokun(s[3], s[4])

	def _SurukleIptal(self):
		self.surukle = None

	def _Disari(self, kok):
		if kok is self.root and not self.onay.IsShow():
			self.Close()

	def _Esc(self):
		if self.onay.IsShow():
			self.__OnayKapat()
		else:
			self.Close()

	def __OnTab(self, key):
		self.tab = key
		self.__IpucuGizle()
		self.sig = None
		self.Tick()

	def __Kaydir(self, u):
		u = _clamp(u, 0, V.MAKS - KOL_N)
		if u != self.ust:
			self.ust = u
			self.seritSig = None
			self.__Serit()
		self.__IpucuGizle()

	def __SeritDokun(self, x, y):
		c = int((x - SERIT[0]) // KOL)
		if not (0 <= c < KOL_N):
			return
		sv = self.ust + c + 1
		col = self.kol[c]
		for key in ("f", "y"):
			yy = col[key]["y"]
			if yy - 4 <= y <= yy + 60:
				ejder = key == "y"
				st = M.Durum(sv, ejder)
				if st == "hazir":
					if _Gonder("a %s %d" % (key, sv)):
						self.__IpucuGizle()
				else:
					(v, a) = M.Odul(sv, ejder)
					self.__Ipucu(v, a, ejder, sv, st, col["x"] + KOL, yy)
				return

	def __OnSol(self, key):
		if key == "ana":
			(v, a) = M.Odul(V.MAKS, True)
			self.__Ipucu(v, a, True, V.MAKS, M.Durum(V.MAKS, True), 177, 184)
		elif key == "kos":
			(v, a) = M.Odul(10, True)
			self.__Ipucu(v, a, True, 10, M.Durum(10, True), 94, 366)
		else:
			(v, a) = M.Odul(20, True)
			self.__Ipucu(v, a, True, 20, M.Durum(20, True), 188, 366)

	def __OnTumu(self):
		if not self.tumB._acik:
			return
		_Gonder("h")

	def __OnGorev(self, i):
		r = None
		for x in self.gor:
			if x["i"] == i:
				r = x
		if r is None or not r["btn"]._acik or not M.GorevHazir(i):
			return
		_Gonder("g %d" % (i + 1))

	def __OnKart1(self):
		if self.alB._acik:
			self.__OnayAc(1)

	def __OnKart2(self):
		if self.plusB._acik:
			self.__OnayAc(2)

	# ---------------- \xfcyelik kart\xfd (EP ile Nesne Market'ten al\xfdnan e\xfeya; sa\xf0 t\xfdk ya da buradan "Kullan")
	def __KartYenile(self, zorla=False):
		t = app.GetTime()
		if not zorla and t - self.kartT < 1.0 and t >= self.kartT:
			return
		self.kartT = t
		(n, yuva) = _KartSay()
		if n != self.kartN or yuva != self.kartYuva:
			self.kartN = n
			self.kartYuva = yuva
			self.ustSig = None
			self.sig = None			# d\xfc\xf0me yaz\xfdlar\xfd bu karede yenilensin

	def __Fiyat(self, tip):
		if tip == 2:
			return V.FIYAT_YUKSELT if M.kart == 1 else V.FIYAT_PLUS
		return V.FIYAT_KART

	def __OnayAc(self, tip):
		"""envanterde kart varsa KART kullan\xfdl\xfdr, yoksa EP ile sat\xfdn al\xfdn\xfdr"""
		if M.kart >= tip:
			return
		self.__KartYenile(True)
		self.onayTip = tip
		self.onayKart = self.kartN[tip] > 0
		yuk = M.kart == 1 and tip == 2
		ad = "Ejder \xdcyelik Plus" if tip == 2 else "Ejder \xdcyelik"
		satir = ["\x95 30 seviyelik Ejder \xf6d\xfcl hatt\xfd a\xe7\xfdl\xfdr",
			"\x95 %s sonuna kadar ge\xe7erli (%s)" % (self.__AyAd(), self.__Kalan())]
		if tip == 2:
			satir.append("\x95 Hemen +%d seviye (Ejder Puan\xfd)" % V.PLUS_SEVIYE)
		if self.onayKart:
			self.onayBas.SetText(KART_AD[tip])
			self.onaySoru.SetText(KART_AD[tip] + (" ile Plus'a y\xfckseltilsin mi?" if yuk else " kullan\xfdls\xfdn m\xfd?"))
			self.onayFiyat.SetText("Envanterinde %d adet \xb7 1 tane harcan\xfdr" % self.kartN[tip])
			satir.append("\x95 Bu hesaptaki b\xfct\xfcn karakterlere ge\xe7er")
			self._BtnDurum(self.evetB, "Kullan", True)
		else:
			f = self.__Fiyat(tip)
			self.onayBas.SetText(ad)
			self.onaySoru.SetText(ad + (" y\xfckseltmesi al\xfdns\xfdn m\xfd?" if yuk else " sat\xfdn al\xfdns\xfdn m\xfd?"))
			self.onayFiyat.SetText("%s EP" % _nokta(f) + ("  \xb7  bakiye %s EP" % _nokta(M.ep) if M.ep >= 0 else ""))
			satir.append("\x95 EP ile \xf6denir (kart\xfd Nesne Market'te)")
			yeter = M.ep < 0 or M.ep >= f
			self._BtnDurum(self.evetB, "Sat\xfdn Al" if yeter else "EP yetersiz", yeter)
		for (j, t) in enumerate(self.onayL):
			t.SetText(satir[j] if j < len(satir) else "")
		self.perde.Show()
		self.perde.SetTop()
		self.onay.Show()
		self.onay.SetTop()

	def __OnayKapat(self):
		if self.built:
			self.onay.Hide()
			self.perde.Hide()

	def __OnEvet(self):
		if not self.evetB._acik:
			return
		tip = self.onayTip
		if not self.onayKart:
			if _Gonder("s %d" % tip):		# EP ile sat\xfdn alma (sunucu atomik d\xfc\xfeer)
				self.__OnayKapat()
			return
		self.__KartYenile(True)
		yuva = self.kartYuva.get(tip, -1)
		self.__OnayKapat()
		if yuva < 0:
			self.Bildir("Envanterde %s yok." % KART_AD[tip], True)
			return
		try:
			import net
			net.SendItemUsePacket(yuva)		# envanterde sa\xf0 t\xfdkla ayn\xfd: sunucu "when <vnum>.use"
		except:
			import dbg
			dbg.TraceError("uiejder: kart kullanilamadi")

	# ---------------- sunucu sonu\xe7lar\xfd
	def OnSonuc(self, a):
		k = a[0]
		if k == 1:
			(tur, sv, v, n) = a[1:5]
			ad = _Item(v)[0]
			self.Bildir("%s%s envantere eklendi." % (ad, (" x%d" % n) if n > 1 else ""))
		elif k == 2:
			self.Bildir(("%d \xf6d\xfcl envantere eklendi." % a[1]) if a[1] > 0 else "Al\xfdnacak \xf6d\xfcl yok.", a[1] <= 0)
		elif k == 3:
			(i, p, sv) = a[1:4]
			once = M.Seviye()
			if sv > once:
				self.Bildir("+%d Ejder Puan\xfd \x97 Ejder Seviyesi %d! Yeni \xf6d\xfcller a\xe7\xfdld\xfd." % (p, sv))
				self.ortaladi = False
			else:
				self.Bildir("+%d Ejder Puan\xfd" % p)
		elif k == 4:
			if a[1] == 2:
				self.Bildir("Ejder \xdcyelik Plus aktif! +%d seviye kazand\xfdn." % V.PLUS_SEVIYE)
			else:
				self.Bildir("Ejder \xdcyelik aktif! Ejder \xf6d\xfclleri a\xe7\xfdld\xfd.")
			self.ortaladi = False
			self.kartT = -100.0

	def Bildir(self, s, kotu=False):
		if not self.built:
			return
		self.bildT.SetText(s)
		self.bildT.SetPackedFontColor(C_KOT if kotu else C_OK)
		tw = min(self._TW(self.bildT) / self.z + 44, self.scrW / self.z - 24)
		x = self.scrW / 2.0 / self.z
		for b in (self.bildBar, self.bildBox):
			b.SetPosition(self.P(x - tw / 2.0), 0)
			b.SetSize(self.P(tw), self.P(36))
		self.bildT.SetPosition(self.P(x), self.P(18))
		self.bild.Show()
		self.bild.SetTop()
		self.bildT0 = app.GetTime()

	# ---------------- ipucu
	def __Ipucu(self, v, a, ejder, sv, st, x, y):
		(ad, path, ac, boy) = _Item(v)
		self.ipkAd.SetText(ad + ((" x%d" % a) if a > 1 else ""))
		(l1, l2) = self.__Sar(ac.replace("|", " ") if ac else "", IPK_W - 20)
		self.ipkA1.SetText(l1)
		self.ipkA2.SetText(l2)
		alt = ("Ejder \xf6d\xfcl\xfc" if ejder else "\xdccretsiz \xf6d\xfcl") + " \xb7 Seviye %d" % sv
		if st == "kilit":
			alt += " \xb7 Ejder \xdcyelik gerekli"
		elif st == "alindi":
			alt += " \xb7 al\xfdnd\xfd"
		self.ipkAlt.SetText(alt)
		self.ipkAlt.SetPackedFontColor(C_MOR if ejder else C_ALT)
		satir = [self.ipkAd] + [t for t in (self.ipkA1, self.ipkA2) if t.GetText()] + [self.ipkAlt]
		h = 10 + len(satir) * 19 + 4
		ww = IPK_W
		for t in satir:
			ww = max(ww, self._TW(t) / self.z + 20)
		ww = min(ww, 420)
		if x + 8 + ww > W_WIN - 8:
			x = x - KOL - 16 - ww
		x = _clamp(x + 8, 8, W_WIN - 8 - ww)
		y = _clamp(y - 4, 52, H_WIN - 12 - h)
		for b in (self.ipkBar, self.ipkBox):
			b.SetPosition(self.P(x), self.P(y))
			b.SetSize(self.P(ww), self.P(h))
			b.Show()
		yy = y + 7
		for t in (self.ipkAd, self.ipkA1, self.ipkA2, self.ipkAlt):
			if t in satir:
				t.SetPosition(self.P(x + 10), self.P(yy))
				t.Show()
				yy += 19
			else:
				t.Hide()
		self.ipkT = app.GetTime()

	def __IpucuGizle(self):
		if self.ipkT >= 0.0:
			self.ipkT = -1.0
			for x in self.ipkW:
				x.Hide()

	def __Sar(self, txt, maxw):
		"""a\xe7\xfdklamay\xfd 2 sat\xfdra b\xf6l (TextLine sarmaz); geni\xfelik yaz\xfd tipiyle \xf6l\xe7\xfcl\xfcr"""
		t = self.ipkA1
		lines = [""]
		for wd in txt.split(" "):
			if not wd:
				continue
			cand = (lines[-1] + " " + wd).strip()
			t.SetText(cand)
			if self._TW(t) > self.P(maxw) and lines[-1]:
				if len(lines) == 2:
					lines[-1] = lines[-1] + "..."
					break
				lines.append(wd)
			else:
				lines[-1] = cand
		while len(lines) < 2:
			lines.append("")
		return lines

	# ---------------- kare (yaln\xfdz a\xe7\xfdkken; HUD d\xfc\xf0mesi \xe7a\xf0\xfdr\xfdr)
	def Tick(self):
		t = app.GetTime()
		if self.built and self.bild.IsShow():
			yas = t - self.bildT0
			if yas > 2.6:
				self.bild.Hide()
		if not (self.built and self.open):
			return
		if self.surukle:
			self.__Surukle()
		if self.ipkT >= 0.0 and t - self.ipkT > 4.0:
			self.__IpucuGizle()
		if M.kart < 2:
			self.__KartYenile()		# 1 sn'de bir (yaln\xfdz a\xe7\xfdkken, \xfcyelik tam de\xf0ilse)
		sig = (M.sig, self.tab, int(t // 10))		# 10 sn: dakika g\xf6revleri / rozet yerelde ilerler
		if sig != self.sig:
			self.sig = sig
			self.__Ciz()
		# al\xfdnabilir yuva parlamas\xfd (15 Hz nab\xfdz)
		if self.tab == "odul" and self.nabizVar:
			n = int(t * 15)
			if n != self.nabiz:
				self.nabiz = n
				import math
				a = 0.55 + 0.45 * (0.5 + 0.5 * math.cos(t * 2.0 * math.pi / 1.4))
				for col in self.kol:
					for key in ("f", "y"):
						p = col[key]["parla"]
						if p.IsShow():
							p.SetAlpha(a)

	def __Surukle(self):
		try:
			(mx, my) = wndMgr.GetMousePosition()
		except:
			return
		(x0, u0, hareket, px, py) = self.surukle
		dx = mx - x0
		if not hareket and abs(dx) > self.P(8):
			hareket = True
			self.__IpucuGizle()
		if hareket:
			adim = max(1, self.P(KOL))
			k = int((abs(dx) + adim // 2) // adim)
			u = u0 - k if dx > 0 else u0 + k		# parmak sa\xf0a -> \xf6nceki seviyeler
			self.surukle = (x0, u0, True, px, py)
			self.__Kaydir(u)

	def __Ciz(self):
		self.__Ust()
		self.__Sekmeler()
		if self.tab == "odul":
			if not self.ortaladi and M.known:
				self.ortaladi = True
				self.ust = _clamp(M.Seviye() - 4, 0, V.MAKS - KOL_N)
				self.seritSig = None
			self.__Serit()
		else:
			self.__Gorevler()

	def __AyAd(self):
		return AY[M.ay - 1] if 1 <= M.ay <= 12 else "Ay"

	def __Kalan(self):
		if M.kalan <= 1:
			return "son g\xfcn"
		return "%d g\xfcn kald\xfd" % M.kalan

	def __Ust(self):
		key = (M.known, M.puan, M.kart, M.ep, M.ay, M.kalan, M.cins, M.surum, self.kartN[1], self.kartN[2])
		if key == self.ustSig:
			return
		self.ustSig = key
		z = self.z
		self.cipT.SetText("%s Sezonu \xb7 %s" % (self.__AyAd(), self.__Kalan()) if M.known else "Bilgi al\xfdn\xfdyor...")
		cw = self._TW(self.cipT) / z + 18
		for b in self.cip:
			b.SetSize(max(1, self.P(self.cipX + cw) - self.P(self.cipX)), self.P(22))
		sv = M.Seviye()
		self.svT.SetText(str(sv))
		self.svT2.SetText("%d / %d" % (sv, V.MAKS))
		self.svT2.SetPosition(self.P(102) + self._TW(self.svL) + self.P(7), self.P(72))
		if sv >= V.MAKS:
			p, top = 1, 1
			self.puanT.SetText("En y\xfcksek seviye! B\xfct\xfcn \xf6d\xfcller a\xe7\xfdk.")
		else:
			p = M.puan - (sv - 1) * V.SV_PUAN
			top = V.SV_PUAN
			self.puanT.SetText("%d / %d Ejder Puan\xfd \xb7 sonraki seviyeye %d" % (p, top, top - p))
		fw = 376.0 * _clamp(p / float(top), 0.0, 1.0)
		if fw >= 0.5:
			self.puanDol.SetScale(fw * z / 200.0, 12 * z / 12.0)
			self.puanDol.Show()
		else:
			self.puanDol.Hide()
		self.kartL.SetText("\xdcyelik: ")
		kx = self.P(520) + self._TW(self.kartL)
		if M.kart >= 1:
			self.kartT2.SetText("Ejder \xdcyelik" + (" Plus" if M.kart == 2 else ""))
			self.kartT2.SetPackedFontColor(C_MOR)
			self.kartA1.SetText("Ejder \xf6d\xfclleri a\xe7\xfdk.")
			self.kartA2.SetText("%s sonuna kadar." % self.__AyAd())
		else:
			self.kartT2.SetText("\xdccretsiz")
			self.kartT2.SetPackedFontColor(C_KAPALI)
			self.kartA1.SetText("EP ile ya da")
			self.kartA2.SetText("\xdcyelik Kart\xfdyla a\xe7\xfdl\xfdr.")
		self.kartT2.SetPosition(kx, self.P(66))
		self.epT.SetText("Bakiye: %s EP" % _nokta(M.ep) if M.ep >= 0 else "Bakiye: \x97")
		n1, n2 = self.kartN[1], self.kartN[2]
		if M.kart >= 1:
			self._BtnDurum(self.alB, "\xdcyelik aktif", False)
		elif n1 > 0:
			self._BtnDurum(self.alB, "Kart\xfd Kullan (%d)" % n1, M.known, 0xffffe08a)
		else:
			self._BtnDurum(self.alB, "\xdcyelik \xb7 %d EP" % V.FIYAT_KART, M.known, 0xffffe08a)
		if M.kart >= 2:
			self._BtnDurum(self.plusB, "Plus aktif", False)
		elif n2 > 0:
			self._BtnDurum(self.plusB, ("Kartla Y\xfckselt (%d)" if M.kart == 1 else "Plus Kart\xfd Kullan (%d)") % n2, M.known, 0xffffe08a)
		elif M.kart == 1:
			self._BtnDurum(self.plusB, "Plus'a Y\xfckselt \xb7 %d EP" % V.FIYAT_YUKSELT, M.known)
		else:
			self._BtnDurum(self.plusB, "\xdcyelik Plus \xb7 %d EP" % V.FIYAT_PLUS, M.known)
		# ay\xfdn \xf6d\xfcl\xfc (cinsiyete g\xf6re kost\xfcm / sa\xe7)
		(v, a) = M.Odul(V.MAKS, True)
		self._IkonAyarla(self.anaIk, v, 121, 240)
		self._Fit(self.anaAd, _Item(v)[0], self.P(200))
		self.anaAlt.SetText("Binek \xb7 Seviye %d \xb7 Ejder" % V.MAKS)
		(v, a) = M.Odul(10, True)
		self._IkonAyarla(self.kosIk, v, 66, 422)
		(v, a) = M.Odul(20, True)
		self._IkonAyarla(self.sacIk, v, 160, 394)

	def __Sekmeler(self):
		ng = M.HazirGorev()
		nod = M.HazirOdul()
		key = (self.tab, ng, nod)
		if key == getattr(self, "_sekSig", None):
			return
		self._sekSig = key
		for (k, (b, lt, x)) in self.tabs.items():
			on = k == self.tab
			b.SetUpVisual(AET + ("tab_on.png" if on else "tab_up.png"))
			b.SetOverVisual(AET + ("tab_on.png" if on else "tab_over.png"))
			b.SetDownVisual(AET + "tab_on.png")
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(b.hWnd, self.z * AET_S, self.z * AET_S)
			lt.SetPackedFontColor(0xffffffff if on else C_KREM)
		# G\xf6revler rozeti
		(b, lt, x) = self.tabs["gorev"]
		if ng > 0:
			self.rozetT.SetText(str(ng))
			bx = x + 125 - 16
			self.rozet.SetPosition(self.P(bx - 11), self.P(SEKME_Y - 7))
			self.rozetT.SetPosition(self.P(bx), self.P(SEKME_Y + 4))
			self.rozet.Show()
			self.rozetT.Show()
		else:
			self.rozet.Hide()
			self.rozetT.Hide()
		if self.tab == "odul":
			self.katGorev.Hide()
			self.katOdul.Show()
			self._BtnDurum(self.tumB, ("T\xfcm\xfcn\xfc Al (%d)" % nod) if nod else "T\xfcm\xfcn\xfc Al", nod > 0, 0xffffe08a)
			self.seritSig = None
		else:
			self.katOdul.Hide()
			self.katGorev.Show()
			self.gorevSig = None

	def __Serit(self):
		key = (self.ust, M.sig, M.surum, M.cins)
		if key == self.seritSig:
			return
		self.seritSig = key
		sv0 = M.Seviye()
		self.nabizVar = False
		for (c, col) in enumerate(self.kol):
			sv = self.ust + c + 1
			x = col["x"]
			if sv == sv0:
				col["hl"].Show()
				col["hlb"].Show()
			else:
				col["hl"].Hide()
				col["hlb"].Hide()
			gecti = sv <= sv0
			col["no"].SetText("" if gecti else str(sv))
			col["no2"].SetText(str(sv) if gecti else "")
			col["pill"].SetColor(0xffe8d08a if gecti else 0x99000000)
			col["pillb"].SetColor(0xfffff3c4 if gecti else C_KENAR)
			col["ozel"].SetText(V.OZEL.get(sv, ""))
			for key2 in ("f", "y"):
				ejder = key2 == "y"
				s = col[key2]
				(v, a) = M.Odul(sv, ejder)
				st = M.Durum(sv, ejder)
				yy = s["y"]
				self._IkonAyarla(s["ik"], v, x + 36, yy + 28, 0.35 if st == "alindi" else (0.55 if st == "kilit" else 1.0))
				s["adet"].SetText(str(a) if a > 1 else "")
				for (n, on) in (("parla", st == "hazir"), ("tik", st == "alindi"), ("kilit", st == "kilit")):
					if on:
						s[n].Show()
					else:
						s[n].Hide()
				if st == "hazir":
					self.nabizVar = True
		# kayd\xfdrma tutama\xf0\xfd
		yol = SERIT[2] - 2
		tw = max(30.0, yol * KOL_N / float(V.MAKS))
		tx = SERIT[0] + 1 + (yol - tw) * self.ust / float(V.MAKS - KOL_N)
		self.tut.SetPosition(self.P(tx), self.P(395))
		self.tut.SetSize(max(2, self.P(tx + tw) - self.P(tx)), max(2, self.P(401) - self.P(395)))
		self.nabiz = -1

	def __Gorevler(self):
		key = (M.sig, int(app.GetTime() // 10))
		if key == self.gorevSig:
			return
		self.gorevSig = key
		for r in self.gor:
			i = r["i"]
			g = V.GOREV[i]
			n = M.Ilerleme(i)
			hedef = g[2]
			sig = (n, M.GorevAlindi(i))
			if sig == r["sig"]:
				continue
			r["sig"] = sig
			cy = r["y"] + GOREV_H / 2.0
			fw = 186.0 * _clamp(n / float(hedef), 0.0, 1.0)
			if fw >= 0.5:
				r["dol"].SetScale(fw * self.z / 200.0, 18 * self.z / 12.0)
				r["dol"].Show()
			else:
				r["dol"].Hide()
			if i in (2, 7):
				r["n"].SetText("%d / %d dk" % (n, hedef))
			else:
				r["n"].SetText("%d / %d" % (n, hedef))
			if M.GorevAlindi(i):
				r["btn"]._acik = False
				r["btn"].Hide()
				r["btn"]._yazi.Hide()
				r["btn"]._kapali.Hide()
				r["bitti"].Show()
				r["tik"].Show()
			else:
				r["bitti"].Hide()
				r["tik"].Hide()
				r["btn"].Show()
				r["btn"]._yazi.Show()
				bitti = n >= hedef
				self._BtnDurum(r["btn"], "Puan\xfd Al" if bitti else "Devam", bitti, 0xffffe08a)
