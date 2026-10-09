# -*- coding: utf-8 -*-
# MOBIL - mobile_root/uitoplusat.py: MARKETE TOPLU SATI\xde (KULLANICI 2026-10-04, prototip Desktop/Averos2-TopluSat-Prototip).
# \xdcRET\xddL\xddR: tools/toplusat/uitoplusat_kaynak.py (UTF-8) -> gen_uitoplusat.py -> mobile_root/uitoplusat.py (ASCII).
#
# v3 (KULLANICI 2026-10-04 telefon: "prototiple alakas\xfd yok, ayn\xfds\xfd olmal\xfd") - PROTOT\xddPLE B\xddREB\xddR:
#  - ipucu \xfeeridi ve se\xe7im \xe7ubu\xf0u ENVANTER PENCERES\xddN\xddN \xdd\xc7\xddNDE: \xfeerit yuvalar\xfdn \xdcST\xdcNDE, \xe7ubuk ("N e\xfeya se\xe7ildi  +X Yang"
#    + T\xfcm\xfc / Temizle / Sat) yuvalar\xfdn ALTINDA, yang kutusu en altta. Kip a\xe7\xfdkken envanter uzar (Ekipman / Y\xfckseltme
#    d\xfc\xf0meleri gizlenir), kapan\xfdnca eski yerle\xfeime d\xf6ner.
#  - i\xfearetler yuva \xf6l\xe7e\xf0inde (uiinventory yerle\xfeimi SCALE 1.8: 32 -> 57,6 px); v2'de \xf6l\xe7ek okunam\xfdyordu (yerel de\xf0i\xfeken).
#  - onay penceresi envanterle AYNI \xe7er\xe7eve / geni\xfe ba\xfel\xfdk / kare \xe7arp\xfd; soru ("N e\xfeyay\xfd" sar\xfd), toplam, kayd\xfdr\xfdlabilir
#    liste (6 sat\xfdr g\xf6r\xfcn\xfcr, parmakla s\xfcr\xfckle), Evet / Hay\xfdr.
#
# Ak\xfd\xfe: markette "Sat" (uishop.OnSell -> Ac) -> envanterde dokunulan e\xfeya TEK TEK sat\xfdlmaz, SE\xc7\xddL\xddR (uiinventory.__SellItem
#   -> Dokun). Sat -> onay -> Evet: e\xfeyalar\xfdn HEPS\xdd AYNI ANDA g\xf6nderilir (net.SendShopSellPacketNew; 2026-10-09'a dek 0,12 sn
#   arayla kuyruktan gidiyordu - 40 e\xfeya ~5 sn, pencere kapan\xfdnca kalanlar iptal). Sunucu her birini kendi kurallar\xfdyla
#   denetler - sunucuda de\xf0i\xfeiklik YOK. Kip, imle\xe7 SELL olmaktan \xe7\xfdk\xfdnca kendili\xf0inden kapan\xfdr.
# "T\xfcm\xfc": yaln\xfdz g\xf6r\xfcnen sayfa; +7 ve \xfcst\xfc silah/z\xfdrh SE\xc7\xddLMEZ (yanl\xfd\xfel\xfdkla de\xf0erli e\xfeya sat\xfdlmas\xfdn) - elle se\xe7ilebilir.
# v4 (KULLANICI 2026-10-04): AKT\xddF (kullan\xfdmdaki) e\xfeya se\xe7ilemez - sunucu Lock(true) yapar ve sat\xfd\xfe\xfd SESS\xddZCE reddeder
#   (char_item.cpp: otomatik iksir + 71510-71519 / 71523-71530 s\xfdn\xfdrs\xfdz buff, soket 0 = 1); "N e\xfeya sat\xfdld\xfd" art\xfdk
#   GER\xc7EKTEN sat\xfdlan\xfd sayar (kuyruk bitince 1 sn sonra yuvalar denetlenir). Kip a\xe7\xfdkken e\xfeya bilgisi (efsun) penceresi
#   a\xe7\xfdlmaz (uiinventory.ShowToolTip -> IpucuEngelli).
import ui
import wndMgr
import app
import player
import item
import net
import chat
from _weakref import ref as _wref

DIR = "mobile/ui/toplusat/"
PT = "d:/ymir work/ui/pattern/"
PUB = "d:/ymir work/ui/public/"
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")
YUVA_OLCEK = 1.9375		# TEK PENCERE ENVANTER 2026-10-05: 62 px yuva | mobile_root/locale/tr/ui/inventorywindow.py SCALE ve uiinventory MOBILE_SLOT_SCALE ile AYNI
ARALIK = 0.12			# sn: iki sat\xfd\xfe paketi aras\xfd
C_CREAM = 0xfff1e6c0
C_GOLD = 0xffe8d08a
C_SEC = 0xfff2c94c
C_SUB = 0xffc9b88f
C_KAPALI = 0xff8f8470
C_TITLE = 0xfffeedc6		# envanter ba\xfel\xfdk yaz\xfds\xfd (1.0, 0.93, 0.78)
C_KUTU = 0x80000000		# prototip .kutu: rgba(0,0,0,.5) + 1 px #3d342a \xe7er\xe7eve
C_KUTU_CIZGI = 0xff3d342a
TASMA = 0.02
# envanter i\xe7i yerle\xfeim (oyun px; prototip px x 1.8, ekran y\xfcksekli\xf0ine s\xfd\xf0acak kadar s\xfdk\xfd)
# TEK PENCERE ENVANTER (2026-10-05): envanter b\xfcy\xfcd\xfc (62 px yuva) -> sat\xfd\xfe kipinde ayr\xfd ipucu \xfeeridi ekrana s\xfd\xf0m\xfdyordu;
# ipucu art\xfdk envanterin BA\xdeLI\xd0INDA ("Sat\xfdlacak e\xfeyalara dokun"), \xfeerit yok.
SERIT_H = 0
SERIT_ARA = 0
IPUCU_BASLIK = "Sat\xfdlacak e\xfeyalara dokun"
BAR_H = 58
BAR_ARA = 3
BTN_SX, BTN_SY = 1.75, 1.5	# middle_button 61x21 -> 107x31,5 (\xfc\xe7 d\xfc\xf0me \xe7ubu\xf0u doldurur)
# onay penceresi (oyun px)
DLG_W = 432
ROW_H = 32
ROW_ARA = 4
ROW_GORUNUR = 6
ROUND_CLOSE_UP = "mobile/ui/minimap/btn_close_sq.png"
ROUND_CLOSE_DOWN = "mobile/ui/minimap/btn_close_sq_down.png"
ROUND_CLOSE_TEX = 64.0


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


def _nokta(n):
	s = str(abs(int(n)))
	out = ""
	while len(s) > 3:
		out = "." + s[-3:] + out
		s = s[:-3]
	return s + out


def _Bilgi(slot):
	"""-> None | {v, n, h, sat, tutar, ad, guclu}"""
	if player.IsEquipmentSlot(slot):
		return None
	v = player.GetItemIndex(slot)
	if not v:
		return None
	n = player.GetItemCount(slot)
	item.SelectItem(v)
	sat = not item.IsAntiFlag(item.ANTIFLAG_SELL)
	p = item.GetISellItemPrice()
	if item.Is1GoldItem():
		tutar = (n / p) if p else 0
	else:
		tutar = p * n
	try:
		(w, h) = item.GetItemSize()
	except:
		(w, h) = (1, 1)
	ad = item.GetItemName()
	guclu = False
	if item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
		guclu = ad[-2:] in ("+7", "+8", "+9")
	return {"v": v, "n": n, "h": max(1, min(3, int(h))), "w": max(1, int(w)), "sat": sat, "tutar": int(tutar), "ad": ad, "guclu": guclu,
		"aktif": _Aktif(slot, v)}


def _Aktif(slot, v):
	"""kullan\xfdmdaki (etkin) e\xfeya: sunucu kilitler, sat\xfdlamaz. Envanterin parlatt\xfd\xf0\xfd e\xfeyalarla AYNI kural
	(uiinventory.RefreshBagSlotWindow: IS_AUTO_POTION / IS_UNLIMITED_ITEM ve soket 0 != 0)"""
	try:
		import constInfo
		if not (constInfo.IS_AUTO_POTION(v) or constInfo.IS_UNLIMITED_ITEM(v)):
			return False
		return 0 != player.GetItemMetinSocket(slot, 0)
	except:
		return False


def IpucuEngelli():
	"""uiinventory.ShowToolTip ba\xfe\xfd: toplu sat\xfd\xfe kipinde dokunu\xfe SE\xc7ER, e\xfeya bilgisi (efsun) penceresi a\xe7\xfdlmaz"""
	return S.acik


class _Durum(object):
	def __init__(self):
		self.acik = False
		self.sec = {}			# slot -> (vnum, adet)
		self.inv = None			# envanter penceresi (zay\xfdf ba\xfevuru)
		self.panel = None
		self.kuyruk = []
		self.kuyrukT = 0.0
		self.satilan = 0
		self.gonderilen = []
		self.kontrol = None		# (zaman, [(slot, vnum, adet)]): g\xf6nderilenlerin ger\xe7ekten sat\xfdl\xfdp sat\xfdlmad\xfd\xf0\xfd


S = _Durum()


def _Inv():
	return S.inv() if S.inv else None


def _Sayfa(inv):
	import uiinventory
	return (inv.inventoryPageIndex, uiinventory.INVENTORY_PAGE_SIZE)


def _YuvaOlcek():
	"""mobil envanter yuvalar\xfd wndMgr.SetSlotScale ile b\xfcy\xfct\xfcl\xfcr (32 px -> 57,6); i\xfearetler ayn\xfd \xf6l\xe7ekle \xe7izilmeli.
	uiinventory'deki MOBILE_SLOT_SCALE fonksiyon i\xe7i yerel de\xf0i\xfeken -> mod\xfclden okunamaz, sabit YUVA_OLCEK kullan\xfdl\xfdr"""
	if not hasattr(wndMgr, "SetSlotScale"):
		return 1.0
	import uiinventory
	return float(getattr(uiinventory, "MOBILE_SLOT_SCALE", YUVA_OLCEK))


# ------------------------------------------------------------------ envanter \xfcst\xfc i\xfearetler
def _Ortuler(inv, goster):
	"""g\xf6r\xfcnen sayfadaki her e\xfeyan\xfdn \xfcst\xfcne: se\xe7ili i\xfeareti / sat\xfdlamaz \xf6rt\xfcs\xfc (yuva penceresinin \xe7ocu\xf0u, dokunmay\xfd ge\xe7irir)"""
	havuz = getattr(inv, "_tsHavuz", None)
	if not goster:
		if havuz:
			for im in havuz:
				im.Hide()
		return
	(sayfa, boy) = _Sayfa(inv)
	f = _YuvaOlcek()
	if havuz is None or getattr(inv, "_tsOlcek", None) != f:
		if havuz:
			for im in havuz:
				im.Hide()
		havuz = []
		for i in xrange(boy):
			im = ui.ExpandedImageBox()
			im.SetParent(inv.wndItem)
			im.AddFlag("not_pick")
			im.SetPosition(int(round((i % 6) * 32 * f)), int(round((i // 6) * 32 * f)))
			im._tur = ""
			im.Hide()
			havuz.append(im)
		inv._tsHavuz = havuz
		inv._tsOlcek = f
	for i in xrange(boy):
		slot = sayfa * boy + i
		b = _Bilgi(slot)
		im = havuz[i]
		tur = ""
		if b:
			if not b["sat"] or b["aktif"]:
				tur = "yok%d" % b["h"]
			elif slot in S.sec:
				tur = "sec%d" % b["h"]
		if not tur:
			im.Hide()
			continue
		if im._tur != tur:
			im._tur = tur
			try:
				im.LoadImage(DIR + tur + ".png")
				max(0, 0)
			except:
				im._tur = ""
				im.Hide()
				continue
			im.SetScale(0.25 * f, 0.25 * f)	# doku 4x (128 px / yuva) -> yuva boyu (32 x yuva \xf6l\xe7e\xf0i); GetWidth'e bak\xfdlmaz
		im.Show()


def _SecimiDogrula():
	"""yeri / adedi de\xf0i\xfemi\xfe e\xfeya se\xe7imden d\xfc\xfeer"""
	for (slot, (v, n)) in list(S.sec.items()):
		if player.GetItemIndex(slot) != v or player.GetItemCount(slot) != n:
			del S.sec[slot]


def Yenile(inv):
	"""uiinventory.RefreshBagSlotWindow ba\xfe\xfd"""
	try:
		S.inv = _wref(inv)
		if not S.acik:
			return
		_SecimiDogrula()
		_Ortuler(inv, True)
		if S.panel:
			S.panel.Yerles(inv)
			S.panel.Ozet()
	except:
		import dbg, traceback
		dbg.TraceError("uitoplusat.Yenile: " + traceback.format_exc())


def Ac():
	"""uishop.OnSell (imle\xe7 SELL yap\xfdld\xfdktan sonra)"""
	try:
		S.acik = True
		S.sec = {}
		S.kuyruk = []
		if S.panel is None:
			S.panel = Panel()
		S.panel.Ac()
		inv = _Inv()
		if inv:
			_Ortuler(inv, True)
	except:
		import dbg, traceback
		dbg.TraceError("uitoplusat.Ac: " + traceback.format_exc())


def Kapat():
	try:
		if not S.acik and not S.panel:
			return
		S.acik = False
		S.sec = {}
		S.kuyruk = []
		k = S.kontrol
		if k and app.GetTime() < k[0]:
			# sat\xfd\xfelar g\xf6nderildi ama sunucu yan\xfdt\xfd hen\xfcz gelmemi\xfe olabilir: yuvalardan say\xfdp yanl\xfd\xfe "sat\xfdlamad\xfd" yazma
			S.kontrol = None
			chat.AppendChat(chat.CHAT_TYPE_INFO, "%d e\xfeya sat\xfd\xfea g\xf6nderildi." % len(k[1]))
		else:
			_Bildir()
		if S.panel:
			S.panel.Kapat()
		inv = _Inv()
		if inv:
			_Ortuler(inv, False)
	except:
		import dbg, traceback
		dbg.TraceError("uitoplusat.Kapat: " + traceback.format_exc())


def _Bildir():
	"""g\xf6nderilen sat\xfd\xfelar\xfdn sonucu: yuvas\xfd bo\xfealan / adedi de\xf0i\xfeen = sat\xfdld\xfd"""
	k = S.kontrol
	S.kontrol = None
	if not k:
		return
	ok = 0
	for (slot, v, n) in k[1]:
		if player.GetItemIndex(slot) != v or player.GetItemCount(slot) != n:
			ok += 1
	kalan = len(k[1]) - ok
	if kalan:
		chat.AppendChat(chat.CHAT_TYPE_INFO, "%d e\xfeya sat\xfdld\xfd, %d e\xfeya sat\xfdlamad\xfd." % (ok, kalan))
	else:
		chat.AppendChat(chat.CHAT_TYPE_INFO, "%d e\xfeya sat\xfdld\xfd." % ok)


def Dokun(inv, slot):
	"""uiinventory.__SellItem ba\xfe\xfd. True = dokunu\xfe burada i\xfelendi (tek tek sat\xfd\xfe penceresi A\xc7ILMAZ)."""
	try:
		if not S.acik:
			return False
		S.inv = _wref(inv)
		if S.kuyruk:
			return True
		b = _Bilgi(slot)
		if not b:
			return True
		if not b["sat"]:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "%s sat\xfdlamaz." % b["ad"])
			return True
		if b["aktif"]:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "%s kullan\xfdmda, sat\xfdlamaz." % b["ad"])
			return True
		if slot in S.sec:
			del S.sec[slot]
		else:
			S.sec[slot] = (b["v"], b["n"])
		_Ortuler(inv, True)
		if S.panel:
			S.panel.Ozet()
		return True
	except:
		import dbg, traceback
		dbg.TraceError("uitoplusat.Dokun: " + traceback.format_exc())
		return False


def Yoket():
	Kapat()
	p = S.panel
	S.panel = None
	if p:
		p.Yoket()


# ------------------------------------------------------------------ \xe7izim yard\xfdmc\xfdlar\xfd (oyun px; klasik d\xf6\xfeeme)
class _Kok(ui.Window):
	def __init__(self, layer):
		ui.Window.__init__(self, layer)
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.basinca = None
		self.birakinca = None

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		if self.basinca:
			self.basinca()
		return True

	def OnMouseLeftButtonUp(self):
		if self.birakinca:
			self.birakinca()
		return True


class _Dokunmatik(ui.Window):
	"""liste alan\xfd: parmakla s\xfcr\xfckleme (bas\xfdnca / b\xfdrak\xfdnca geri \xe7a\xf0r\xfd)"""
	def __init__(self):
		ui.Window.__init__(self)
		self.basinca = None
		self.birakinca = None

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		if self.basinca:
			self.basinca()
		return True

	def OnMouseLeftButtonUp(self):
		if self.birakinca:
			self.birakinca()
		return True


class _Cizer(object):
	def Hazirla(self):
		self.scrW = wndMgr.GetScreenWidth()
		self.scrH = wndMgr.GetScreenHeight()
		self.keep = []

	def _Tile(self, parent, path, x, y, w, h, tw, th, sx=1.0, sy=1.0):
		x, y = int(round(x)), int(round(y))
		w, h = int(round(w)), int(round(h))
		img = ui.ExpandedImageBox()
		img.SetParent(parent)
		img.AddFlag("not_pick")
		img.LoadImage(path)
		max(0, 0)
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(img.hWnd, 1)
		(zx, r) = _Otur(w, w, tw, sx, HAS_RRS, 1.0)
		(zy, b) = _Otur(h, h, th, sy, HAS_RRS, 1.0)
		img.SetScale(zx, zy)
		img.SetRenderingRect(0.0, 0.0, r, b)
		img.SetPosition(x, y)
		img.Show()
		self.keep.append(img)
		return img

	def _Board(self, parent, W, H):
		"""ui.Board ile ayn\xfd: 32 px k\xf6\xfee / kenar, \xf6l\xe7eksiz (envanter penceresiyle ayn\xfd kal\xfdnl\xfdk)"""
		self._Tile(parent, PT + "board_base.tga", 32, 32, W - 64, H - 64, 128, 128)
		self._Tile(parent, PT + "board_line_top.tga", 32, 0, W - 64, 32, 128, 32)
		self._Tile(parent, PT + "board_line_bottom.tga", 32, H - 32, W - 64, 32, 128, 32)
		self._Tile(parent, PT + "board_line_left.tga", 0, 32, 32, H - 64, 32, 128)
		self._Tile(parent, PT + "board_line_right.tga", W - 32, 32, 32, H - 64, 32, 128)
		for (n, cx, cy) in (("lefttop", 0, 0), ("righttop", W - 32, 0), ("leftbottom", 0, H - 32), ("rightbottom", W - 32, H - 32)):
			self._Tile(parent, PT + "board_corner_%s.tga" % n, cx, cy, 32, 32, 32, 32)

	def _GenisBaslik(self, parent, W, baslik, kapat):
		"""envanterin geni\xfe ba\xfel\xfdk \xe7ubu\xf0u (uiinventory __MobileWideTitleBar: 1.6x sol + orta, sa\xf0 kapak yok, kare HUD \xe7arp\xfds\xfd)"""
		x, y, w = 8, 7, W - 15
		bh = int(round(23 * 1.6))
		bw = int(round(32 * 1.6))
		self._Tile(parent, PT + "titlebar_left.tga", x, y, bw, bh, 32, 32, 1.6, 1.6)
		self._Tile(parent, PT + "titlebar_center.tga", x + bw, y, w - bw, bh, 32, 32, 1.6, 1.6)
		t = self._Txt(parent, "Tahoma:22", C_TITLE, x + w / 2.0, y + bh / 2.0 - 1, "center")
		t.SetText(baslik)
		if kapat:
			c = bh * 1.15
			b = ui.Button()
			b.SetParent(parent)
			b.SetUpVisual(ROUND_CLOSE_UP)
			b.SetOverVisual(ROUND_CLOSE_UP)
			b.SetDownVisual(ROUND_CLOSE_DOWN)
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(b.hWnd, c / ROUND_CLOSE_TEX, c / ROUND_CLOSE_TEX)
			b.SetPosition(int(round(x + w - c)), int(round(y + (bh - c) / 2.0)))
			b.SetEvent(kapat)
			b.Show()
			self.keep.append(b)
		return y + bh

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

	def _Kutu(self, parent, x, y, w, h):
		"""prototip .kutu: yar\xfd saydam siyah + 1 px koyu kahve \xe7er\xe7eve"""
		return (self._Rect(parent, x, y, w, h, C_KUTU), self._Rect(parent, x, y, w, h, C_KUTU_CIZGI, False))

	def _Txt(self, parent, font, color, x, y, align="left"):
		"""y = yaz\xfdn\xfdn D\xddKEY ORTASI"""
		t = ui.TextLine()
		t.SetParent(parent)
		t.AddFlag("not_pick")
		t.SetFontName(font)
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

	def _Btn(self, parent, x, y, yazi, func):
		"""oyunun orta d\xfc\xf0mesi (61x21 texel) BTN_SX x BTN_SY"""
		b = ui.Button()
		b.SetParent(parent)
		b.SetUpVisual(PUB + "middle_button_01.sub")
		b.SetOverVisual(PUB + "middle_button_02.sub")
		b.SetDownVisual(PUB + "middle_button_03.sub")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, BTN_SX, BTN_SY)
		b.SetPosition(int(round(x)), int(round(y)))
		b.SetEvent(func)
		b.Show()
		self.keep.append(b)
		t = self._Txt(parent, "Tahoma:16", C_CREAM, x + 61 * BTN_SX / 2.0, y + 21 * BTN_SY / 2.0 - 1, "center")
		t.SetText(yazi)
		b._yazi = t
		return b


BTN_W = 61 * BTN_SX
BTN_H = 21 * BTN_SY


# ------------------------------------------------------------------ envanter \xdd\xc7\xdd \xfeerit + se\xe7im \xe7ubu\xf0u
class Panel(_Cizer):
	"""prototipteki envanter d\xfczeni: [ba\xfel\xfdk][sekmeler][\xdeER\xddT][yuvalar][\xc7UBUK: \xf6zet + T\xfcm\xfc/Temizle/Sat][yang]"""
	def __init__(self):
		self.Hazirla()
		# kare ba\xfe\xfd denetim (envanter kapal\xfd olsa da \xe7al\xfd\xfes\xfdn diye ayr\xfd, bo\xfe, g\xf6r\xfcnmez k\xf6k)
		k = _Kok("UI")
		k.AddFlag("not_pick")
		k.SetSize(0, 0)
		k.SetPosition(0, 0)
		k.Hide()
		k.OnUpdate = self.Guncelle
		self.kok = k
		self.keep.append(k)
		self.inv = None			# \xf6\xf0elerin kuruldu\xf0u envanter (zay\xfdf ba\xfevuru)
		self.ogeler = []		# \xfeerit + \xe7ubuk pencereleri (envanter board'unun \xe7ocuklar\xfd)
		self.orj = None			# kip \xf6ncesi yerle\xfeim
		self.sayiT = None
		self.tutarT = None
		self.satB = None
		self.onay = None
		self.ozetSig = None

	def _Kur(self, inv):
		"""\xfeerit ve \xe7ubu\xf0u envanterin board'una bir kez kurar"""
		board = inv.GetChild2("board")
		if not board:
			return False
		ana = self.keep
		self.keep = []
		f = _YuvaOlcek()
		(sx, sy) = inv.wndItem.GetLocalPosition()
		gw = int(round(6 * 32 * f))
		self.gw = gw
		# \xfeerit: yuvalar a\xfea\xf0\xfd itilince a\xe7\xfdlan bo\xfelukta (yerle\xfeim Ac'ta)
		if SERIT_H > 0:
			self._Kutu(board, 0, 0, gw, SERIT_H)
			ip = self._Txt(board, "Tahoma:14", C_GOLD, gw / 2.0, SERIT_H / 2.0, "center")
			ip.SetText("Satmak istedi\xf0in e\xfeyalara dokun")
		serit = self.keep
		self.keep = []
		# \xe7ubuk
		self._Kutu(board, 0, 0, gw, BAR_H)
		self.sayiT = self._Txt(board, "Tahoma:16", C_CREAM, 10, 13)
		self.tutarT = self._Txt(board, "Tahoma:16", C_GOLD, gw - 10, 13, "right")
		ara = 3
		bx = (gw - 3 * BTN_W - 2 * ara) / 2.0
		by = 23
		self._Btn(board, bx, by, "T\xfcm\xfc", ui.__mem_func__(self.Tumu))
		self._Btn(board, bx + BTN_W + ara, by, "Temizle", ui.__mem_func__(self.Temizle))
		self.satB = self._Btn(board, bx + 2 * (BTN_W + ara), by, "Sat", ui.__mem_func__(self.Sor))
		bar = self.keep
		self.keep = ana
		# her \xf6\xf0enin \xe7ubuk/\xfeerit i\xe7indeki konumu (Yerles bunlar\xfd kayd\xfdr\xfdr)
		self.ogeler = [(w, w.GetLocalPosition(), "serit") for w in serit] + [(w, w.GetLocalPosition(), "bar") for w in bar]
		for (w, p, _) in self.ogeler:
			w.Hide()
		self.inv = _wref(inv)
		return True

	def _Inv(self):
		return self.inv() if self.inv else None

	def Yerles(self, inv):
		"""kip a\xe7\xfdk: yuvalar\xfd \xfeerit kadar a\xfea\xf0\xfd, yang kutusunu \xfeerit + \xe7ubuk kadar a\xfea\xf0\xfd al, envanteri uzat"""
		if self._Inv() is not inv:
			self._Geri()
			self.ogeler = []
			if not self._Kur(inv):
				return
		board = inv.GetChild2("board")
		money = inv.GetChild2("Money_Slot")
		if not board or not money:
			return
		if self.orj is None:
			bx = [inv.GetChild2(n) for n in ("MobileEquipButton", "MobileStorageButton")]
			self.orj = {
				"slot": inv.wndItem.GetLocalPosition(),
				"money": money.GetLocalPosition(),
				"board": (board.GetWidth(), board.GetHeight()),
				"root": (inv.GetWidth(), inv.GetHeight()),
				"rootPos": inv.GetLocalPosition(),
				"btn": [(b, b.IsShow()) for b in bx if b],
			}
		o = self.orj
		if o.get("uygulandi"):
			return			# RefreshBagSlotWindow her \xe7a\xf0r\xfdda yeniden yerle\xfetirmesin (kare ba\xfe\xfd y\xfck yok)
		o["uygulandi"] = True
		tb = inv.GetChild2("TitleBar")
		bt = getattr(tb, "mobileTitle", None) if tb else None
		if bt:
			if "baslik" not in o:
				o["baslik"] = bt.GetText()
			bt.SetText(IPUCU_BASLIK)
		(sx, sy) = o["slot"]
		f = _YuvaOlcek()
		gh = int(round((uiinventory_page_rows()) * 32 * f))
		dy1 = SERIT_H + SERIT_ARA
		barY = sy + dy1 + gh + BAR_ARA
		dy2 = dy1 + BAR_H + BAR_ARA
		inv.wndItem.SetPosition(sx, sy + dy1)
		(mx, my) = o["money"]
		money.SetPosition(mx, my + dy2)
		(bw, bh) = o["board"]
		board.SetSize(bw, bh + dy2)
		by0 = board.GetLocalPosition()[1]
		yeniH = by0 + bh + dy2
		inv.SetSize(o["root"][0], yeniH)
		for (b, _) in o["btn"]:
			b.Hide()
		(rx, ry) = o["rootPos"]
		if ry + yeniH > self.scrH:
			inv.SetPosition(rx, max(0, self.scrH - yeniH))
			o["kaydi"] = True
		for (w, (px, py), tur) in self.ogeler:
			if tur == "serit":
				w.SetPosition(sx + px, sy + py)
			else:
				w.SetPosition(sx + px, barY + py)
			w.Show()

	def _Geri(self):
		"""kip kapand\xfd: envanter eski yerle\xfeimine d\xf6ner"""
		inv = self._Inv()
		if self.orj:
			self.orj["uygulandi"] = False
		for (w, p, _) in self.ogeler:
			w.Hide()
		o = self.orj
		self.orj = None
		if not inv or not o:
			return
		board = inv.GetChild2("board")
		money = inv.GetChild2("Money_Slot")
		tb = inv.GetChild2("TitleBar")
		bt = getattr(tb, "mobileTitle", None) if tb else None
		if bt and o.get("baslik"):
			bt.SetText(o["baslik"])
		inv.wndItem.SetPosition(*o["slot"])
		if money:
			money.SetPosition(*o["money"])
		if board:
			board.SetSize(*o["board"])
		inv.SetSize(*o["root"])
		if o.get("kaydi"):		# yaln\xfdz ekrana s\xfd\xf0s\xfdn diye biz yukar\xfd ald\xfdysak geri indir
			inv.SetPosition(inv.GetLocalPosition()[0], o["rootPos"][1])
		for (b, gorunur) in o["btn"]:
			if gorunur:
				b.Show()

	def Ac(self):
		inv = _Inv()
		if inv:
			self.Yerles(inv)
			tt = getattr(inv, "tooltipItem", None)
			if tt:
				try:
					tt.HideToolTip()
				except:
					pass
		self.kok.Show()
		self.ozetSig = None
		self.Ozet()

	def Kapat(self):
		self.kok.Hide()
		self._Geri()
		if self.onay:
			self.onay.Kapat()

	def Yoket(self):
		self.Kapat()
		if self.onay:
			self.onay.Yoket()
			self.onay = None
		self.kok.OnUpdate = None
		self.ogeler = []
		self.keep = []
		self.kok = None

	def Secilenler(self):
		out = []
		for slot in sorted(S.sec.keys()):
			b = _Bilgi(slot)
			if b and b["sat"] and not b["aktif"] and (b["v"], b["n"]) == S.sec[slot]:
				b["slot"] = slot
				out.append(b)
		return out

	def Ozet(self):
		if not self.sayiT:
			return
		l = self.Secilenler()
		top = 0
		for b in l:
			top += b["tutar"]
		sig = (len(l), top, len(S.kuyruk))
		if sig == self.ozetSig:
			return
		self.ozetSig = sig
		if S.kuyruk:
			self.sayiT.SetText("Sat\xfdl\xfdyor... %d kald\xfd" % len(S.kuyruk))
			self.tutarT.SetText("")
		elif l:
			self.sayiT.SetText("%d e\xfeya se\xe7ildi" % len(l))
			self.tutarT.SetText("+%s Yang" % _nokta(top))
		else:
			self.sayiT.SetText("E\xfeya se\xe7ilmedi")
			self.tutarT.SetText("")
		self.satB._yazi.SetPackedFontColor(C_CREAM if l and not S.kuyruk else C_KAPALI)

	def Tumu(self):
		inv = _Inv()
		if not inv or S.kuyruk:
			return
		(sayfa, boy) = _Sayfa(inv)
		for i in xrange(boy):
			slot = sayfa * boy + i
			b = _Bilgi(slot)
			if b and b["sat"] and not b["aktif"] and not b["guclu"]:
				S.sec[slot] = (b["v"], b["n"])
		_Ortuler(inv, True)
		self.Ozet()

	def Temizle(self):
		if S.kuyruk:
			return
		S.sec = {}
		inv = _Inv()
		if inv:
			_Ortuler(inv, True)
		self.Ozet()

	def Sor(self):
		l = self.Secilenler()
		if not l or S.kuyruk:
			return
		if self.onay is None:
			self.onay = Onay()
		self.onay.Ac(l, ui.__mem_func__(self.Sat))

	def Sat(self):
		"""KULLANICI (2026-10-09): "5 saniyede tek tek azalarak sat\xfdyor, pencereyi kapat\xfdnca iptal oluyor; Sat'a bas\xfdnca hepsini
		birden sats\xfdn". Eskiden 0,12 sn arayla kuyruktan g\xf6nderiliyordu. Art\xfdk se\xe7ilenlerin HEPS\xdd ayn\xfd anda g\xf6nderilir:
		sunucuda sat\xfd\xfe ya da paket h\xfdz s\xfdn\xfdr\xfd yok (shop_manager Sell, desc ProcessInput), paketler SIRAYLA i\xfelenir; sonradan
		gelen d\xfckk\xe2n kapatma iste\xf0i sat\xfd\xfelardan SONRA i\xfelendi\xf0i i\xe7in pencereyi kapatmak art\xfdk hi\xe7bir \xfeeyi iptal etmez."""
		l = self.Secilenler()
		_Bildir()
		gonderilen = []
		for b in l:
			(slot, v, n) = (b["slot"], b["v"], b["n"])
			if player.GetItemIndex(slot) == v and player.GetItemCount(slot) == n and not _Aktif(slot, v):
				net.SendShopSellPacketNew(slot, n, player.INVENTORY)
				gonderilen.append((slot, v, n))
		S.kuyruk = []
		S.satilan = len(gonderilen)
		S.gonderilen = []
		S.sec = {}
		S.kontrol = (app.GetTime() + 1.0, gonderilen)	# sunucu yan\xfdt\xfd (yuva bo\xfealmas\xfd) gelsin, sonra say
		inv = _Inv()
		if inv:
			_Ortuler(inv, True)
		self.Ozet()

	def Guncelle(self):
		"""kare ba\xfe\xfd: imle\xe7 SELL de\xf0ilse kip kapan\xfdr; sat\xfd\xfe kuyru\xf0u ARALIK ile i\xfelenir"""
		if app.GetCursor() != app.SELL:
			Kapat()
			return
		t = app.GetTime()
		if S.kontrol and (t >= S.kontrol[0] or t < S.kontrol[0] - 5.0):
			_Bildir()
		if not S.kuyruk:
			return
		if t - S.kuyrukT < ARALIK and t >= S.kuyrukT:
			return
		S.kuyrukT = t
		(slot, v, n) = S.kuyruk.pop(0)
		if player.GetItemIndex(slot) == v and player.GetItemCount(slot) == n and not _Aktif(slot, v):
			net.SendShopSellPacketNew(slot, n, player.INVENTORY)
			S.satilan += 1
			S.gonderilen.append((slot, v, n))
		if not S.kuyruk:
			S.kontrol = (t + 1.0, S.gonderilen)	# sunucu yan\xfdt\xfd (yuva bo\xfealmas\xfd) gelsin, sonra say
			S.gonderilen = []
		self.Ozet()


def uiinventory_page_rows():
	import uiinventory
	return uiinventory.INVENTORY_PAGE_SIZE // 6


# ------------------------------------------------------------------ onay penceresi (prototip #onay, envanter \xe7er\xe7evesiyle)
class Onay(_Cizer):
	def __init__(self):
		self.Hazirla()
		pd = _Kok("TOP_MOST")
		pd.SetSize(self.scrW, self.scrH)
		pd.SetPosition(0, 0)
		pd.Hide()
		kar = ui.Bar()
		kar.SetParent(pd)
		kar.AddFlag("not_pick")
		kar.SetColor(0x80000000)
		kar.SetPosition(0, 0)
		kar.SetSize(self.scrW, self.scrH)
		kar.Show()
		pd.birakinca = self._Birak
		pd.OnUpdate = self._Guncelle
		self.keep += [pd, kar]
		self.perde = pd
		self.pen = None
		self.penKeep = []
		self.evet = None
		self.liste = []
		self.ust = 0
		self.surukle = None
		self.satirlar = []

	def Ac(self, liste, evet):
		self.Kapat()
		self.evet = evet
		self.liste = liste
		self.ust = 0
		ana = self.keep
		self.keep = []
		W = DLG_W
		n = min(len(liste), ROW_GORUNUR)
		kaydir = len(liste) > ROW_GORUNUR
		lh = 7 + n * ROW_H + (n - 1) * ROW_ARA + 7
		y0 = 7 + int(round(23 * 1.6)) + 11			# ba\xfel\xfdk + 6 px (x1.8)
		soruY = y0 + 4 + 15
		topY = soruY + 15 + 2 + 14
		listeY = topY + 14 + 11
		btnY = listeY + lh + 4 + 11
		H = int(round(btnY + BTN_H + 14 + 10))
		p = _Kok("TOP_MOST")
		p.SetSize(W, H)
		p.SetPosition(int((self.scrW - W) // 2), int(max(0, (self.scrH - H) // 2)))
		p.birakinca = self._Birak
		self.keep.append(p)
		self._Board(p, W, H)
		self._GenisBaslik(p, W, "Toplu Sat\xfd\xfe", ui.__mem_func__(self.Kapat))
		top = 0
		for b in liste:
			top += b["tutar"]
		# soru: "<sar\xfd>N e\xfeyay\xfd</sar\xfd> satmak istiyor musun?"
		a = self._Txt(p, "Tahoma:18", C_SEC, 0, soruY)
		a.SetText("%d e\xfeyay\xfd" % len(liste))
		bb = self._Txt(p, "Tahoma:18", C_CREAM, 0, soruY)
		bb.SetText(" satmak istiyor musun?")
		wa, wb = self._Gen(a), self._Gen(bb)
		x = (W - wa - wb) / 2.0
		a.SetPosition(int(round(x)), soruY)
		bb.SetPosition(int(round(x + wa)), soruY)
		t = self._Txt(p, "Tahoma:17", C_GOLD, W / 2.0, topY, "center")
		t.SetText("Toplam %s Yang alacaks\xfdn" % _nokta(top))
		# liste kutusu
		lx, lw = 10, W - 20
		self._Kutu(p, lx, listeY, lw, lh)
		sagX = lx + lw - 11 - (16 if kaydir else 0)
		self.satirlar = []
		for i in xrange(n):
			ry = listeY + 7 + i * (ROW_H + ROW_ARA)
			im = ui.ExpandedImageBox()
			im.SetParent(p)
			im.AddFlag("not_pick")
			ad = self._Txt(p, "Tahoma:16", C_CREAM, lx + 11 + ROW_H + 11, ry + ROW_H / 2.0)
			fi = self._Txt(p, "Tahoma:16", C_GOLD, sagX, ry + ROW_H / 2.0, "right")
			self.keep.append(im)
			self.satirlar.append((im, ad, fi, lx + 11, ry))
		self.izTh = None
		if kaydir:
			# kayd\xfdrma \xe7ubu\xf0u (prototip listesindeki gibi sa\xf0da): iz + tutamak
			ix, iy, ih = lx + lw - 4 - 12, listeY + 5, lh - 10
			self._Rect(p, ix, iy, 12, ih, 0x60000000)
			self._Rect(p, ix, iy, 12, ih, C_KUTU_CIZGI, False)
			th = max(24, int(ih * float(ROW_GORUNUR) / len(liste)))
			self.izTh = (self._Rect(p, ix + 2, iy + 2, 8, th - 4, C_SUB), ix + 2, iy + 2, ih - th)
			d = _Dokunmatik()
			d.SetParent(p)
			d.SetPosition(lx, listeY)
			d.SetSize(lw, lh)
			d.basinca = self._Bas
			d.birakinca = self._Birak
			d.Show()
			self.keep.append(d)
		self._Satirlar()
		bx = (W - 2 * BTN_W - 7) / 2.0
		self._Btn(p, bx, btnY, "Evet", ui.__mem_func__(self.Evet))
		self._Btn(p, bx + BTN_W + 7, btnY, "Hay\xfdr", ui.__mem_func__(self.Kapat))
		self.pen = p
		self.penKeep = self.keep
		self.keep = ana
		self.perde.Show()
		self.perde.SetTop()
		p.Show()
		p.SetTop()

	def _Gen(self, t):
		try:
			return int(t.GetTextSize()[0])
		except:
			return 9 * len(t.GetText()) if hasattr(t, "GetText") else 0

	def _Satirlar(self):
		for (i, (im, ad, fi, x, ry)) in enumerate(self.satirlar):
			k = self.ust + i
			if k >= len(self.liste):
				im.Hide()
				ad.SetText("")
				fi.SetText("")
				continue
			b = self.liste[k]
			ad.SetText(b["ad"] + ((" x%d" % b["n"]) if b["n"] > 1 else ""))
			fi.SetText(_nokta(b["tutar"]))
			item.SelectItem(b["v"])
			ik = item.GetIconImageFileName()
			try:
				im.LoadImage(ik)
				max(0, 0)
				# mant\xfdksal ikon boyu = 32 x yuva (GetWidth'e g\xfcvenilmez); ROW_H kutuya s\xfd\xf0d\xfdr (prototip object-fit: contain)
				s = float(ROW_H) / (32.0 * max(b["w"], b["h"]))
				im.SetScale(s, s)
				im.SetPosition(int(round(x + (ROW_H - 32.0 * b["w"] * s) / 2.0)), int(round(ry)))
				im.Show()
			except:
				im.Hide()
		if self.izTh:
			(th, tx, ty, yol) = self.izTh
			en = max(1, len(self.liste) - ROW_GORUNUR)
			th.SetPosition(int(tx), int(round(ty + yol * float(self.ust) / en)))

	def _Bas(self):
		try:
			(mx, my) = wndMgr.GetMousePosition()
		except:
			return
		self.surukle = (my, self.ust)

	def _Birak(self):
		self.surukle = None

	def _Guncelle(self):
		if not self.surukle or not self.pen:
			return
		try:
			(mx, my) = wndMgr.GetMousePosition()
		except:
			return
		(y0, u0) = self.surukle
		u = u0 - int(round((my - y0) / float(ROW_H + ROW_ARA)))
		u = max(0, min(len(self.liste) - ROW_GORUNUR, u))
		if u != self.ust:
			self.ust = u
			self._Satirlar()

	def Evet(self):
		f = self.evet
		self.Kapat()
		if f:
			f()

	def Kapat(self):
		self.surukle = None
		if self.perde:
			self.perde.Hide()
		if self.pen:
			self.pen.Hide()
		self.pen = None
		self.penKeep = []
		self.satirlar = []
		self.izTh = None

	def Yoket(self):
		self.Kapat()
		self.keep = []
		self.perde = None
