# MOBIL (yalniz kaplama; PC'de yok): PAZAR SATIS BILDIRIMI.
# KULLANICI (2026-09-27): "pazarda bir sey satilinca telefona bildirim gelsin (pazara koydugunuz item satildi),
# oyunda da bildirim olsun; ekranin solunda bildirim ciksin, basinca ne satildigi yazsin".
#   * Sunucu satista pazar sahibine bildirim paketi yollar (baska kanaldaysa P2P ile) -> native offlineshop modulu
#     -> uiofflineshop.OfflineShopRenewal.SendNotification -> OnSale().
#   * Sol ustte Etkinlik dugmesinin ALTINDA para kesesi dugmesi (mobile/ui/pazar/hud_pazar_*.tga, ilk satista
#     belirir), okunmamis satis sayisi kirmizi rozette, okunmamis varken nefes alan parilti.
#   * Dokununca "Pazar Satislari" listesi (en yeni ustte): ikon, esya adi x adet, fiyat, ne zaman.
#   * Telefon bildirimi: app.PostPhoneNotification (APK v64+; eski APK'da yok -> atlanir).
# Satis listesi modul duzeyinde tutulur (isinlanma/HUD yeniden kurulumu arasinda kaybolmaz; oturumluk).
import ui
import wndMgr
import app
import item
import math

SALES = []		# {vnum, name, price, count, t}
MAX_SALES = 30
_unread = [0]
_button = [None]	# gecerli PazarHudButton (MobileHud kurar)
_list = [None]		# PazarListWindow (ilk acilista kurulur)

PHONE_TITLE = "Pazara koydu\xf0unuz item sat\xfdld\xfd"


def _Dots(n):
	s = str(int(max(0, n)))
	g = []
	while len(s) > 3:
		g.insert(0, s[-3:])
		s = s[:-3]
	g.insert(0, s)
	return ".".join(g)


def _Ago(t):
	d = max(0, int(app.GetTime() - t))
	if d < 60:
		return "az \xf6nce"
	if d < 3600:
		return "%d dk \xf6nce" % (d / 60)
	return "%d sa \xf6nce" % (d / 3600)


def OnSale(vnum, name, price, count):
	SALES.insert(0, {"vnum": vnum, "name": name, "price": price, "count": count, "t": app.GetTime()})
	del SALES[MAX_SALES:]
	_unread[0] += 1
	b = _button[0]
	if b:
		b.Refresh()
	w = _list[0]
	if w and w.IsShow():
		w.Rebuild()
		_unread[0] = 0
		if b:
			b.Refresh()
	if hasattr(app, "PostPhoneNotification"):
		try:
			txt = name
			if count > 1:
				txt += " x%d" % count
			txt += " - %s Yang" % _Dots(price)
			app.PostPhoneNotification(PHONE_TITLE, txt)
		except:
			import dbg, traceback
			dbg.TraceError("MOBIL pazar telefon bildirimi: " + traceback.format_exc())


def Toggle():
	w = _list[0]
	if not w:
		w = PazarListWindow()
		_list[0] = w
	if w.IsShow():
		w.Hide()
		return
	w.Open()
	_unread[0] = 0
	if _button[0]:
		_button[0].Refresh()


def Clear():
	del SALES[:]
	_unread[0] = 0
	if _list[0]:
		_list[0].Hide()
	if _button[0]:
		_button[0].Refresh()


def DestroyAll():
	## HUD yikilirken (faz degisimi) pencere de gitsin; satis listesi kalir
	w = _list[0]
	_list[0] = None
	if w:
		w.Destroy()


class PazarHudButton(ui.Window):
	CX, CY = 0.075, 0.355		# Etkinlik dugmesinin (0.075, 0.243) altinda
	SIZE = 46
	GLOW = 96
	BADGE = 22
	PULSE_SEC = 2.0
	LABEL_FONT = "Tahoma:16"

	def __init__(self):
		ui.Window.__init__(self, "UI_BOTTOM")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("PazarHudButton")
		self.AddFlag("not_pick")
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetPosition(0, 0)
		self.hidden = False
		cx = int(round(self.CX * wndMgr.GetScreenWidth()))
		cy = int(round(self.CY * wndMgr.GetScreenHeight()))
		self.cx = cx; self.cy = cy

		glow = ui.ExpandedImageBox()
		glow.SetParent(self)
		glow.AddFlag("not_pick")
		glow.LoadImage("mobile/ui/etk/hud_etk_glow.tga")
		glow.SetScale(self.GLOW / 192.0, self.GLOW / 192.0)
		glow.SetPosition(cx - self.GLOW / 2, cy - self.GLOW / 2)
		glow.Hide()
		self.glow = glow

		btn = ui.Button()
		btn.SetParent(self)
		btn.SetUpVisual("mobile/ui/pazar/hud_pazar_up.tga")
		btn.SetOverVisual("mobile/ui/pazar/hud_pazar_up.tga")
		btn.SetDownVisual("mobile/ui/pazar/hud_pazar_down.tga")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(btn.hWnd, self.SIZE / 128.0, self.SIZE / 128.0)
		btn.SetPosition(cx - self.SIZE / 2, cy - self.SIZE / 2)
		btn.SetEvent(ui.__mem_func__(self.__OnClick))
		btn.Show()
		self.btn = btn

		badge = ui.ExpandedImageBox()
		badge.SetParent(self)
		badge.AddFlag("not_pick")
		badge.LoadImage("mobile/ui/etk/hud_etk_badge.tga")
		badge.SetScale(self.BADGE / 32.0, self.BADGE / 32.0)
		badge.SetPosition(cx + self.SIZE / 2 - self.BADGE + 4, cy - self.SIZE / 2 - 4)
		badge.Hide()
		self.badge = badge
		num = ui.TextLine()
		num.SetParent(badge)
		num.AddFlag("not_pick")
		num.SetFontName("Tahoma:14")
		num.SetOutline()
		num.SetHorizontalAlignCenter()
		num.SetVerticalAlignCenter()
		num.SetPackedFontColor(0xffffffff)
		num.SetPosition(self.BADGE / 2, self.BADGE / 2 - 1)
		num.Show()
		self.num = num

		label = ui.TextLine()
		label.SetParent(self)
		label.AddFlag("not_pick")
		label.SetFontName(self.LABEL_FONT)
		label.SetOutline()
		label.SetHorizontalAlignCenter()
		label.SetPackedFontColor(0xfff1e6c8)
		label.SetText("Pazar")
		label.SetPosition(cx - 2, cy + self.SIZE / 2 + 1)
		label.Show()
		self.label = label

		_button[0] = self
		self.Refresh()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		if _button[0] is self:
			_button[0] = None
		self.Hide()
		self.glow = None
		self.btn = None
		self.badge = None
		self.num = None
		self.label = None

	def __OnClick(self):
		Toggle()

	def SetHidden(self, hidden):
		self.hidden = hidden
		self.Refresh()

	def Refresh(self):
		if not self.btn:
			return
		if self.hidden or not SALES:
			self.Hide()
			w = _list[0]
			if w and not SALES:
				w.Hide()
			return
		self.Show()
		n = _unread[0]
		if n > 0:
			self.num.SetText(n > 99 and "99" or str(n))
			self.badge.Show()
		else:
			self.badge.Hide()
			self.glow.Hide()

	def Update(self):
		if self.hidden or not self.btn or not self.IsShow():
			return
		if _unread[0] > 0:
			a = 0.25 + 0.35 * (0.5 + 0.5 * math.sin(app.GetTime() * 2.0 * math.pi / self.PULSE_SEC))
			self.glow.SetAlpha(a)
			if not self.glow.IsShow():
				self.glow.Show()
		w = _list[0]
		if w and w.IsShow():
			w.Tick()


class PazarListWindow(ui.BoardWithTitleBar):
	W = 330
	ROW_H = 42
	MAX_ROWS = 8

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetTitleName("Pazar Sat\xfd\xfelar\xfd")
		self.SetCloseEvent(ui.__mem_func__(self.Hide))
		self.rows = []
		self.lastTick = 0.0
		btn = ui.Button()
		btn.SetParent(self)
		btn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		btn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		btn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		btn.SetText("Temizle")
		btn.SetEvent(ui.__mem_func__(self.__OnClear))
		btn.Show()
		self.clearBtn = btn
		try:
			import uiInventory
			uiInventory._MobileRoundClose(self.titleBar, 22, 1)	# envanterdeki kare HUD carpisi
		except:
			pass

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def Destroy(self):
		self.rows = []
		self.clearBtn = None
		self.Hide()

	def __OnClear(self):
		Clear()

	def Open(self):
		self.Rebuild()
		b = _button[0]
		try:
			sc = wndMgr.GetUIScale(self.hWnd)
		except:
			sc = 1.0
		if b and b.btn:
			(bx, by) = b.btn.GetGlobalPosition()
			x = bx + b.btn.GetWidth() + 12
			y = max(4, min(by - 20, wndMgr.GetScreenHeight() - int(self.GetHeight() * sc) - 4))
			self.SetPosition(x, y)
		self.Show()
		self.SetTop()

	def __Row(self, i):
		while len(self.rows) <= i:
			icon = ui.ImageBox()
			icon.SetParent(self)
			icon.AddFlag("not_pick")
			t1 = ui.TextLine()
			t1.SetParent(self)
			t1.AddFlag("not_pick")
			t1.SetPackedFontColor(0xfff1e6c8)
			t2 = ui.TextLine()
			t2.SetParent(self)
			t2.AddFlag("not_pick")
			self.rows.append([icon, t1, t2, -1])
		return self.rows[i]

	def Rebuild(self):
		## satir pencereleri bir kez kurulur, yeniden kullanilir (30 sn'lik tazeleme sizinti yapmasin)
		shown = SALES[:self.MAX_ROWS]
		top = 36
		for i in xrange(len(shown)):
			s = shown[i]
			y = top + i * self.ROW_H
			r = self.__Row(i)
			(icon, t1, t2) = r[0], r[1], r[2]
			if r[3] != s["vnum"]:
				r[3] = s["vnum"]
				try:
					item.SelectItem(s["vnum"])
					icon.LoadImage(item.GetIconImageFileName())
				except:
					pass
			icon.SetPosition(14, y + 2)
			icon.Show()
			name = s["name"]
			if s["count"] > 1:
				name += " x%d" % s["count"]
			t1.SetText(name)
			t1.SetPosition(54, y + 3)
			t1.Show()
			t2.SetText("|cffffcc00%s Yang|r  |cff9a9080%s|r" % (_Dots(s["price"]), _Ago(s["t"])))
			t2.SetPosition(54, y + 19)
			t2.Show()
		for i in xrange(len(shown), len(self.rows)):
			for w in self.rows[i][:3]:
				w.Hide()
		n = max(1, len(shown))
		h = top + n * self.ROW_H + 44
		self.SetSize(self.W, h)
		self.clearBtn.SetPosition((self.W - self.clearBtn.GetWidth()) / 2, h - 34)

	def Tick(self):
		## "x dk once" yazilari dakikada bir tazelenir
		t = app.GetTime()
		if t - self.lastTick > 30.0:
			self.lastTick = t
			self.Rebuild()

	def OnPressEscapeKey(self):
		self.Hide()
		return True
