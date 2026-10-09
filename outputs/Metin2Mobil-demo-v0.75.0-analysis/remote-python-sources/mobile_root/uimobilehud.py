# H-HUD: mobil HUD - ust sag 6 dugme, sol ust kume, KISAYOLLAR paneli (mobile_root/uimobilehud.py).
# uitaskbar.TaskBar.LoadWindow icinden kurulur (interfacemodule golgelenmez).
# Her dugme -> gercek client islevi (game.py __BuildKeyDict 395-513 / interfacemodule.py):
#   Envanter   I     game.py:461  interface.ToggleInventoryWindow      (BUTTON_INVENTORY, interfacemodule:235)
#   Karakter   C     game.py:457  interface.ToggleCharacterWindow("STATUS") (BUTTON_CHARACTER, interfacemodule:234)
#   Sohbet     Enter game.py:1954 OnIMEReturn -> interface.ToggleChat     (BUTTON_CHAT, interfacemodule:247)
#   Esya sil   X     game.py:416  interface.OpenDeleteItem
#   Kisayollar -     bu panel (PC karsiligi: klavye)
#   Ayarlar    ESC   TaskBar SystemButton -> interface.ToggleSystemDialog (BUTTON_SYSTEM, interfacemodule:237)
#   Ekran g.   PrtSc game.py:428  SaveScreen (1267)
#   Isimler    Alt   game.py:426  ShowName (1296) / 506 HideName (1362); uzun bas = basili tut
#   Kamera     -     game.py:200  app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)
#   ESC        ESC   game.py:1940 OnPressEscapeKey
#   Hedef      -     gercek client'ta karsiligi YOK -> konmadi (rapor)
# Panel: C I V N B G M O K L H F5 X Alt Ctrl+Q Ctrl+J (asagida KeyPanel.LoadWindow).
## 6 SUTUN ENVANTER (2026-09-15): 6x8x4 sayfa (son sayfa 36 yuva). player.INVENTORY_PAGE_SIZE(45)/INVENTORY_PAGE_COUNT(4) client ikilisinde
## sabit ve degistirilemez; sayfa aritmetigi bu modul sabitlerini kullanir (genel yuva = sayfa*30 + yerel, yerel: sutun=%6, satir=//6).
INVENTORY_PAGE_SIZE = 48
INVENTORY_PAGE_COUNT = 4
import ui
import app
import net
import player
import wndMgr

class HoldButton(ui.Button):
	"""Basili tutma dugmesi: sol tus basisi (dokun-birak) = ac/kapa; sag tus (uzun basma,
	InputCore TAP_LONGPRESS) basili kaldigi surece = PC'de tusu basili tutmak."""

	def __init__(self, layer = "UI"):
		ui.Button.__init__(self, layer)
		self.holdDownEvent = None
		self.holdUpEvent = None
		self.holding = False

	def __del__(self):
		ui.Button.__del__(self)
		self.holdDownEvent = None
		self.holdUpEvent = None

	def SetHoldEvent(self, downEvent, upEvent):
		self.holdDownEvent = downEvent
		self.holdUpEvent = upEvent

	def OnMouseRightButtonDown(self):
		if self.holding:
			return True
		self.holding = True
		self.Down()
		if self.holdDownEvent:
			self.holdDownEvent()
		return True

	def OnMouseRightButtonUp(self):
		if not self.holding:
			return True
		self.holding = False
		self.SetUp()
		if self.holdUpEvent:
			self.holdUpEvent()
		return True

class KeyPanel(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.SetWindowName("MobileKeyPanel")
		self.hud = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self, hud):
		self.hud = hud
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/mobilekeypanel.py")
		except:
			import exception
			exception.Abort("KeyPanel.LoadWindow.LoadObject")

		self.GetChild("CloseButton").SetEvent(ui.__mem_func__(self.Close))
		# (dosya adi, islev) - her satir game.py __BuildKeyDict / ilgili dalin kendisi
		bind = (
			("c",	lambda : self.__Interface().ToggleCharacterWindow("STATUS")),	# 457 DIK_C
			("i",	lambda : self.__Interface().ToggleInventoryWindow()),			# 461 DIK_I
			("v",	lambda : self.__Interface().ToggleCharacterWindow("SKILL")),		# 458 DIK_V
			("n",	lambda : self.__Interface().ToggleCharacterWindow("QUEST")),		# 460 DIK_N
			("b",	lambda : self.__Interface().ToggleCharacterWindow("EMOTICON")),	# 570-571 __PressBKey (Ctrl'siz)
			("g",	lambda : self.__Interface().ToggleGuildWindow()),				# 585-586 __PressGKey (Alt basili dali = Lonca)
			("m",	lambda : self.__Interface().PressMKey()),						# 463 DIK_M
			# "o" (game.py:462 DIK_O -> ToggleDragonSoulWindowWithNoInfo) bu pack'in interfacemodule'unde YOK
			# (PC'de de hata verir; cihazda syserr goruldu) -> panelden cikarildi.
			("k",	self.__PressK),													# 478 DIK_K -> 1966 OpenSpecialStorage
			("l",	lambda : self.__Interface().ToggleChatLogWindow()),				# 466 DIK_L
			("h",	lambda : self.__Interface().OpenHelpWindow()),					# 566 __PressHKey (Ctrl'siz)
			# ("x" -> OpenDeleteItem) KULLANICI 2026-10-02: kaldirildi
			("alt",	self.__ToggleShowName),											# 426 ShowName / 506 HideName
			("cq",	self.__PressCtrlQ),												# 594-600 __PressQKey Ctrl dali
			("cj",	self.__PressCtrlJ),												# 553-562 __PressJKey Ctrl dali
		)
		for (name, func) in bind:
			self.GetChild("key_" + name).SetEvent(lambda f=func: self.__Run(f))

		self.Hide()

	def __Interface(self):
		return self.hud.interface

	def __GameWindow(self):
		return self.hud.GetGameWindow()

	def __Run(self, func):
		# Panel bir kisayol gibi calisir: islevi cagir, paneli kapat
		if not self.hud.interface:
			return
		self.Close()
		func()

	def __PressK(self):
		# game.py:1966 OpenSpecialStorage -> interface.ToggleSpecialStorageWindow
		gameWindow = self.__GameWindow()
		if gameWindow:
			gameWindow.OpenSpecialStorage()

	def __ToggleShowName(self):
		self.hud.ToggleShowName()

	def __PressCtrlQ(self):
		# game.py:594-600 (__PressQKey, Ctrl basili): gorev dugmelerini gizle/goster
		import interfaceModule
		if 0==interfaceModule.IsQBHide:
			interfaceModule.IsQBHide = 1
			self.__Interface().HideAllQuestButton()
		else:
			interfaceModule.IsQBHide = 0
			self.__Interface().ShowAllQuestButton()

	def __PressCtrlJ(self):
		# game.py:553-562 (__PressJKey, Ctrl basili): attan in / at cagirma esyasi kullan
		import uiPrivateShopBuilder
		if player.IsMountingHorse():
			net.SendChatPacket("/unmount")
		else:
			if not uiPrivateShopBuilder.IsBuildingPrivateShop():
				for i in xrange(INVENTORY_PAGE_SIZE * 2):	## 6 SUTUN ENVANTER: eski 45 yuva kapsami (2x30)
					if player.GetItemIndex(i) in (71114, 71116, 71118, 71120):
						net.SendItemUsePacket(i)
						break

	def Open(self):
		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()

	def Toggle(self):
		if self.IsShow():
			self.Close()
		else:
			self.Open()

	def OnPressEscapeKey(self):
		self.Close()
		return True

## DUELLO KILIT DUGMESI (KULLANICI 2026-09-22): duello sirasinda yetenek yayinin yaninda
## kirmizi, yavas yanip sonen hedef dugmesi. Dokununca rakibe kilitlenir ve saldirir
## (karaktere iki kez dokunmanin karsiligi: player.MobileLockOnActor), altinda kisa sure
## "Kahramana kilitlendi" yazar. Duello bitince (DuelMode DUEL_START degil / rakip listesi bos /
## harita degisimi) kaybolur. Motor tarafi: PythonPlayerModule GetDuelMode / GetDuelOpponentVIDs.
class DuelLockButton(ui.Window):

	DUEL_START = 2			# CInstanceBase::DUEL_START
	CX, CY = 0.7650, 0.5443		# yetenek yayi 1. kutusunun solu (mobiletaskbar.py ARC[0] = 0.8547, 0.5443)
	SIZE = 60			# btn_duel_*.tga 128 px -> 60 px
	GLOW = 108			# duel_glow.tga 192 px -> 108 px
	PULSE_SEC = 1.6			# yavas yanip sonme suresi
	LABEL_SEC = 2.0			# "Kahramana kilitlendi" ekranda kalma suresi
	LABEL_FONT = "Tahoma:16"

	def __init__(self):
		ui.Window.__init__(self, "UI_BOTTOM")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("DuelLockButton")
		self.AddFlag("not_pick")
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetPosition(0, 0)
		cx = int(round(self.CX * wndMgr.GetScreenWidth()))
		cy = int(round(self.CY * wndMgr.GetScreenHeight()))

		glow = ui.ExpandedImageBox()
		glow.SetParent(self)
		glow.AddFlag("not_pick")
		glow.LoadImage("mobile/ui/duel_glow.tga")
		glow.SetScale(self.GLOW / 192.0, self.GLOW / 192.0)
		glow.SetSize(self.GLOW, self.GLOW)
		glow.SetPosition(cx - self.GLOW / 2, cy - self.GLOW / 2)
		glow.Show()
		self.glow = glow

		btn = ui.Button()
		btn.SetParent(self)
		btn.SetUpVisual("mobile/ui/btn_duel_up.tga")
		btn.SetOverVisual("mobile/ui/btn_duel_up.tga")
		btn.SetDownVisual("mobile/ui/btn_duel_down.tga")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(btn.hWnd, self.SIZE / 128.0, self.SIZE / 128.0)
		btn.SetPosition(cx - self.SIZE / 2, cy - self.SIZE / 2)
		btn.SetEvent(ui.__mem_func__(self.__OnClick))
		btn.Show()
		self.btn = btn

		label = ui.TextLine()
		label.SetParent(self)
		label.AddFlag("not_pick")
		label.SetFontName(self.LABEL_FONT)
		label.SetOutline()
		label.SetHorizontalAlignCenter()
		label.SetPosition(cx, cy + self.SIZE / 2 + 4)
		label.SetPackedFontColor(0xffff5a4a)
		label.Hide()
		self.label = label

		self.labelUntil = 0.0
		self.active = False
		self.Hide()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.glow = None
		self.btn = None
		self.label = None

	def __Opponent(self):
		# duello devam ediyor mu, rakip sahnede mi. Normal duello = PVP_MODE_FIGHT (GetPvpOpponentVIDs);
		# arena duellosu = GC_DUEL_START (GetDuelOpponentVIDs + DUEL_START kipi).
		try:
			import chr
			for vid in player.GetPvpOpponentVIDs():
				if chr.HasInstance(vid):
					return vid
			if player.GetDuelMode() == self.DUEL_START:
				for vid in player.GetDuelOpponentVIDs():
					if chr.HasInstance(vid):
						return vid
		except:
			return 0
		return 0

	def __OnClick(self):
		vid = self.__Opponent()
		if not vid:
			return
		ok = player.MobileLockOnActor(vid)
		if ok:
			self.label.SetText("Kahramana kilitlendi")
		else:
			self.label.SetText("Rakibe ula\xfe\xfdlam\xfdyor")	# cp1254: Rakibe ulasilamiyor
		self.label.Show()
		self.labelUntil = app.GetTime() + self.LABEL_SEC

	def Update(self):
		## HIZ (2026-10-01): rakip listesi (GetPvpOpponentVIDs) her kare yerine 0.25 s'de bir sorulur
		tq = app.GetTime()
		if tq - getattr(self, "_qT", -1.0) >= 0.25 or tq < getattr(self, "_qT", -1.0):
			self._qT = tq
			self._qActive = self.__Opponent() != 0
		active = self._qActive
		if not getattr(self, "logged", False):
			self.logged = True
			try:
				import dbg
				dbg.TraceError("DuelLockButton.Update calisiyor; pvp=%s duelMode=%s" % (str(player.GetPvpOpponentVIDs()), str(player.GetDuelMode())))
			except:
				pass
		if active != self.active:
			self.active = active
			if active:
				self.Show()
				self.SetTop()
			else:
				self.Hide()
				self.label.Hide()
		if not active:
			return
		t = app.GetTime()
		# yavas yanip sonme: 0.15 .. 1.0 arasi sinus
		import math
		a = 0.575 + 0.425 * math.sin(t * 2.0 * math.pi / self.PULSE_SEC)
		self.glow.SetAlpha(a)
		if self.label.IsShow() and t > self.labelUntil:
			self.label.Hide()

class EventHudButton(ui.Window):
	"""KULLANICI (2026-09-23): ETKINLIK TAKVIMI dugmesi - Desktop/Etkinlik-Penceresi tasarimi.
	Sekizgen altin dugme (hud_menu/hud_horse diliyle), ustunde her 9 sn'de bir tam tur donen ince
	altin halka ("arada bir donen"), aktif etkinlik varsa nefes alan parilti + kirmizi rozet.
	Dokunma -> interface.ToggleEtkinlik() (uietkinlik.EventCalendarWindow, animasyonlu acilis).
	Butonlari Ozellestir ile tasinabilir (uiMobileLayout "etk"); halka/parilti/rozet her kare
	dugmenin GERCEK konumundan turetilir (duzen editoru yalniz dugme+etiketi tasir)."""

	CX, CY = 0.075, 0.243		# Gizle dugmesinin altinda (sol ust kume), gorev dugmelerinin ustunde
	SIZE = 46			# hud_etk_*.tga 128 px -> 46 px (ust sira ile ayni)
	GLOW = 96			# hud_etk_glow.tga 192 px
	RING = 60			# hud_etk_ring.tga 128 px
	BADGE = 20			# hud_etk_badge.tga 32 px
	SPIN_PERIOD = 9.0		# sn: bu aralikla bir kez doner
	SPIN_SEC = 1.4			# tam turun suresi (ease-in-out)
	PULSE_SEC = 2.4
	LABEL_FONT = "Tahoma:16"

	def __init__(self, hud):
		ui.Window.__init__(self, "UI_BOTTOM")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("EventHudButton")
		self.AddFlag("not_pick")
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetPosition(0, 0)
		self.hud = hud
		self.hidden = False
		cx = int(round(self.CX * wndMgr.GetScreenWidth()))
		cy = int(round(self.CY * wndMgr.GetScreenHeight()))
		D = "mobile/ui/etk/"

		glow = ui.ExpandedImageBox()
		glow.SetParent(self)
		glow.AddFlag("not_pick")
		glow.LoadImage(D + "hud_etk_glow.tga")
		glow.SetScale(self.GLOW / 192.0, self.GLOW / 192.0)
		glow.SetPosition(cx - self.GLOW / 2, cy - self.GLOW / 2)
		glow.Hide()
		self.glow = glow

		ring = ui.ExpandedImageBox()
		ring.SetParent(self)
		ring.AddFlag("not_pick")
		ring.LoadImage(D + "hud_etk_ring.tga")
		ring.SetScale(self.RING / 128.0, self.RING / 128.0)
		# DONDURME MERKEZI: CGraphicExpandedImageInstance dondururken konumu MERKEZ + origin sayar (donmezken
		# sol-ust); origin = olcekli yarim boyut verilince iki yolda da sol-ust konum tutarli kalir
		# (KULLANICI 2026-09-23: halka dugmenin sag-altina kaymis cikiyordu).
		ring.SetOrigin(self.RING / 2.0, self.RING / 2.0)
		ring.SetPosition(cx - self.RING / 2, cy - self.RING / 2)
		ring.Show()
		self.ring = ring

		btn = ui.Button()
		btn.SetParent(self)
		btn.SetUpVisual(D + "hud_etk_up.tga")
		btn.SetOverVisual(D + "hud_etk_up.tga")
		btn.SetDownVisual(D + "hud_etk_down.tga")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(btn.hWnd, self.SIZE / 128.0, self.SIZE / 128.0)
		btn.SetPosition(cx - self.SIZE / 2, cy - self.SIZE / 2)
		btn.SetEvent(ui.__mem_func__(self.__OnClick))
		btn.Show()
		self.btn = btn

		badge = ui.ExpandedImageBox()
		badge.SetParent(self)
		badge.AddFlag("not_pick")
		badge.LoadImage(D + "hud_etk_badge.tga")
		badge.SetScale(self.BADGE / 32.0, self.BADGE / 32.0)
		badge.Hide()
		self.badge = badge

		label = ui.TextLine()
		label.SetParent(self)
		label.AddFlag("not_pick")
		label.SetFontName(self.LABEL_FONT)
		label.SetOutline()
		label.SetHorizontalAlignCenter()
		label.SetPackedFontColor(0xfff1e6c8)
		label.SetText("Etkinlik")
		label.SetPosition(cx - 2, cy + self.SIZE / 2 + 1)
		label.Show()
		self.label = label
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.glow = None
		self.ring = None
		self.btn = None
		self.badge = None
		self.label = None
		self.hud = None

	def __Window(self):
		try:
			return self.hud.interface.wndEtkinlik
		except:
			return None

	def __OnClick(self):
		try:
			self.hud.interface.ToggleEtkinlik()
		except:
			import dbg, traceback
			dbg.TraceError("EventHudButton: " + traceback.format_exc())

	def SetHidden(self, hidden):
		self.hidden = hidden
		if hidden:
			self.Hide()
		else:
			self.Show()

	def Update(self):
		w = self.__Window()
		if w and w.IsShow():
			w.Tick()			# pencere animasyonu/geri sayimi buradan surulur (HUD OnUpdate zinciri)
		if self.hidden or not self.btn:
			return
		import math
		(bx, by) = self.btn.GetGlobalPosition()
		bw = self.btn.GetWidth()
		bh = self.btn.GetHeight()
		cx = bx + bw / 2.0
		cy = by + bh / 2.0
		rs = bw / float(self.SIZE)		# duzen editoru olcegi
		t = app.GetTime()
		# halka: SPIN_PERIOD'da bir SPIN_SEC icinde tam tur (ease-in-out), kalan surede sabit
		ph = math.fmod(t, self.SPIN_PERIOD)
		ang = 0.0
		if ph < self.SPIN_SEC:
			q = ph / self.SPIN_SEC
			ang = 360.0 * (0.5 - 0.5 * math.cos(q * math.pi))
		## HIZ (2026-10-01): halka donmuyorken ve dugme yerinde dururken (9 sn'nin ~7.6'si) 4 donusum cagrisi atlanir;
		## etkin etkinlik sayisi 0.5 s'de bir sorulur. Gorunum ayni.
		size = self.RING * rs
		rk = (bx, by, bw, bh, ang)
		if rk != getattr(self, "_ringKey", None):
			self._ringKey = rk
			self.ring.SetRotation(ang)
			self.ring.SetScale(size / 128.0, size / 128.0)
			self.ring.SetOrigin(size / 2.0, size / 2.0)
			self.ring.SetPosition(int(cx - size / 2), int(cy - size / 2))
			self.label.SetPosition(int(cx) - 2, int(cy + bh / 2 + 1))
		if t - getattr(self, "_nT", -1.0) >= 0.5 or t < getattr(self, "_nT", -1.0):
			self._nT = t
			self._n = w.GetActiveCount() if w else 0
		n = self._n
		if n > 0:
			g = self.GLOW * rs
			a = 0.45 + 0.35 * math.sin(t * 2.0 * math.pi / self.PULSE_SEC)
			self.glow.SetScale(g / 192.0, g / 192.0)
			self.glow.SetPosition(int(cx - g / 2), int(cy - g / 2))
			self.glow.SetAlpha(a)
			self.glow.Show()
			b = self.BADGE * rs
			self.badge.SetScale(b / 32.0, b / 32.0)
			self.badge.SetPosition(int(cx + bw * 0.28 - b / 2), int(cy - bh * 0.28 - b / 2))
			self.badge.Show()
		else:
			self.glow.Hide()
			self.badge.Hide()

class CarkHudButton(ui.Window):
	"""KULLANICI (2026-10-03): GUNLUK SANS CARKI dugmesi (uicark). Etkinlik dugmesiyle ayni dil (sekizgen bronz,
	altin cark ikonu, 46 px + alt yazi); cevirme hakki varken kirmizi rozet. Butonlari Ozellestir ile tasinir ("cark").
	Pencerenin karesi (Tick) yalniz pencere ACIKKEN buradan surulur; kapaliyken yalniz 0.5 sn'de bir rozet bakilir."""

	CX, CY = 0.075, 0.467		# Etkinlik (0.243) ve Pazar (0.355) dugmelerinin altinda
	SIZE = 46
	BADGE = 20
	LABEL_FONT = "Tahoma:16"

	def __init__(self, hud):
		ui.Window.__init__(self, "UI_BOTTOM")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("CarkHudButton")
		self.AddFlag("not_pick")
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetPosition(0, 0)
		self.hud = hud
		self.hidden = False
		self._uc = None		# uicark modulu (kare basi import yapilmasin)
		cx = int(round(self.CX * wndMgr.GetScreenWidth()))
		cy = int(round(self.CY * wndMgr.GetScreenHeight()))
		btn = ui.Button()
		btn.SetParent(self)
		btn.SetUpVisual("mobile/ui/cark/hud_cark_up.png")
		btn.SetOverVisual("mobile/ui/cark/hud_cark_up.png")
		btn.SetDownVisual("mobile/ui/cark/hud_cark_down.png")
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
		badge.Hide()
		self.badge = badge
		label = ui.TextLine()
		label.SetParent(self)
		label.AddFlag("not_pick")
		label.SetFontName(self.LABEL_FONT)
		label.SetOutline()
		label.SetHorizontalAlignCenter()
		label.SetPackedFontColor(0xfff1e6c8)
		label.SetText("\xc7ark")
		label.SetPosition(cx - 2, cy + self.SIZE / 2 + 1)
		label.Show()
		self.label = label
		self._nT = -1.0
		self._bKey = None
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.btn = None
		self.badge = None
		self.label = None
		self.hud = None
		try:
			import uicark
			uicark.DestroyAll()
		except:
			pass

	def __OnClick(self):
		try:
			import uicark
			uicark.Toggle()
		except:
			import dbg, traceback
			dbg.TraceError("CarkHudButton: " + traceback.format_exc())

	def SetHidden(self, hidden):
		self.hidden = hidden
		if hidden:
			self.Hide()
		else:
			self.Show()

	def Update(self):
		uicark = self._uc
		try:
			if uicark is None:
				import uicark
				self._uc = uicark
			w = uicark._WND[0]
			if w and w.open:
				w.Tick()
		except:
			import dbg, traceback
			dbg.TraceError("uicark.Tick: " + traceback.format_exc())
			return
		if self.hidden or not self.btn:
			return
		t = app.GetTime()
		if t - self._nT < 0.5 and t >= self._nT:
			return
		self._nT = t
		ready = uicark.IsReady()
		(bx, by) = self.btn.GetGlobalPosition()
		bw = self.btn.GetWidth()
		bh = self.btn.GetHeight()
		key = (ready, bx, by, bw, bh)
		if key == self._bKey:
			return
		self._bKey = key
		cx = bx + bw / 2.0
		cy = by + bh / 2.0
		self.label.SetPosition(int(cx) - 2, int(cy + bh / 2 + 1))
		if ready:
			b = self.BADGE * bw / float(self.SIZE)
			self.badge.SetScale(b / 32.0, b / 32.0)
			self.badge.SetPosition(int(cx + bw * 0.28 - b / 2), int(cy - bh * 0.28 - b / 2))
			self.badge.Show()
		else:
			self.badge.Hide()

class EjderHudButton(CarkHudButton):
	"""KULLANICI (2026-10-05): EJDER UYELIK dugmesi (uiejder) - Carkin altinda, ayni dil (sekizgen bronz + altin ejder).
	Alinabilir odul / gorev varken kirmizi rozet. Butonlari Ozellestir ile tasinir ("ejder").
	Pencere karesi (Tick) yalniz ACIKKEN surulur; kapaliyken 0.5 sn'de bir rozet + INPUT_IGNORE guvenligi."""

	CX, CY = 0.075, 0.579

	def __init__(self, hud):
		CarkHudButton.__init__(self, hud)
		self.SetWindowName("EjderHudButton")
		self.btn.SetUpVisual("mobile/ui/ejder/hud_up.png")
		self.btn.SetOverVisual("mobile/ui/ejder/hud_up.png")
		self.btn.SetDownVisual("mobile/ui/ejder/hud_down.png")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(self.btn.hWnd, self.SIZE / 128.0, self.SIZE / 128.0)
		self.btn.SetEvent(ui.__mem_func__(self.__OnEjder))
		self.label.SetText("Ejder")
		self._ue = None

	def Destroy(self):
		self.btn = None
		self.badge = None
		self.label = None
		self.hud = None
		try:
			import uiejder
			uiejder.DestroyAll()
		except:
			pass

	def __OnEjder(self):
		try:
			import uiejder
			uiejder.Toggle()
		except:
			import dbg, traceback
			dbg.TraceError("EjderHudButton: " + traceback.format_exc())

	def Update(self):
		ue = self._ue
		try:
			if ue is None:
				import uiejder
				ue = self._ue = uiejder
			w = ue._WND[0]
			if w and (w.open or w.built):
				w.Tick()
		except:
			import dbg, traceback
			dbg.TraceError("uiejder.Tick: " + traceback.format_exc())
			return
		if not self.btn:
			return
		t = app.GetTime()
		if t - self._nT < 0.5 and t >= self._nT:
			return
		self._nT = t
		ue.Guvenlik()
		if self.hidden:
			return
		n = ue.Rozet()
		(bx, by) = self.btn.GetGlobalPosition()
		bw = self.btn.GetWidth()
		bh = self.btn.GetHeight()
		key = (n > 0, bx, by, bw, bh)
		if key == self._bKey:
			return
		self._bKey = key
		cx = bx + bw / 2.0
		cy = by + bh / 2.0
		self.label.SetPosition(int(cx) - 2, int(cy + bh / 2 + 1))
		if n > 0:
			b = self.BADGE * bw / float(self.SIZE)
			self.badge.SetScale(b / 32.0, b / 32.0)
			self.badge.SetPosition(int(cx + bw * 0.28 - b / 2), int(cy - bh * 0.28 - b / 2))
			self.badge.Show()
		else:
			self.badge.Hide()

## 2026-10-01: hedef karti (uihedefkarti) yerlesimi icin dugmelerin GERCEK konumunu okur
_INSTANCE = [None]


def GetInstance():
	return _INSTANCE[0]


class MobileHud(ui.ScriptWindow):

	def __init__(self):
		# KULLANICI (2026-09-13): pack pencereleri (envanter, karakter...) mobil dugmelerin
		# ALTINDA kalmaz -> HUD en alt UI katmaninda ("UI_BOTTOM"; pencereler "UI").
		ui.ScriptWindow.__init__(self, "UI_BOTTOM")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.SetWindowName("MobileHud")
		self.interface = None
		self.taskBar = None
		self.keyPanel = None
		self.nameButton = None
		self.etkButton = None
		self.showNameToggled = False
		_INSTANCE[0] = self

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/mobilehud.py")
		except:
			import exception
			exception.Abort("MobileHud.LoadWindow.LoadObject")

		## KULLANICI (2026-09-14): hud_*.tga 2x cozunurluklu -> 0.5 olcek (cihazda 1:1'e yakin, keskin)
		if hasattr(wndMgr, "SetButtonScale"):
			for n in ("ChatButton", "DeleteItemButton", "KeyPanelButton", "HideButton", "MenuButton"):
				b = self.GetChild2(n)
				if b:
					wndMgr.SetButtonScale(b.hWnd, 46.0 / 120.0, 46.0 / 120.0)	# KULLANICI 2026-09-14: 60 -> 46 px
			# Metin2 gercek gorev cubugu ikonlari (32 px .sub) -> 60 px
			for n in ("CharacterButton", "InventoryButton", "MessengerButton", "SystemButton"):
				b = self.GetChild2(n)
				if b:
					wndMgr.SetButtonScale(b.hWnd, 46.0 / 32.0, 46.0 / 32.0)
		## KULLANICI (2026-10-02): "esya sil butonunu kaldir" -> Sil dugmesi + yazisi kalici gizli (olay yok)
		## KULLANICI (2026-10-03): "ekranda yukaridaki kisayol butonu kaldirilsin, bosluk olusmasin" -> Kisayol da
		## kalici gizli (uiscript/mobilehud.py: soldaki 5 dugme bir saga kaydi; HIDE_TOP ve duzen kaydinda yok).
		for n in ("DeleteItemButton", "DeleteItemLabel", "KeyPanelButton", "KeyPanelLabel"):
			w = self.GetChild2(n)
			if w:
				w.Hide()
		self.GetChild("KeyPanelButton").SetEvent(ui.__mem_func__(self.__OnClickKeyPanel))
		self.GetChild("HideButton").SetEvent(ui.__mem_func__(self.__OnClickHide))
		self.GetChild("MenuButton").SetEvent(ui.__mem_func__(self.__OnClickMenu))	# KULLANICI 2026-09-15: Menu (F5) ust sirada

		# Isimler: dokun = ac/kapa. PC'de Alt (game.py:1296 ShowName) ayrica hizli slot SAYFASINI +1
		# kaydirir ve karakter ustu HP cubugunu (uiPlayerGauge EnableShowAlways) acar - Alt BASILI
		# TUTULDUGU surece. Telefonda ac/kapa kalici oldugundan bu yan etkiler kutulari kaydiriyor ve
		# karakter ustunde surekli dolu cubuk birakiyordu (cihazda goruldu) -> yalniz isimler.
		self.nameButton = None	# KULLANICI 2026-09-14: sol kume kaldirildi
		## KULLANICI (2026-09-23): Etkinlik Takvimi dugmesi (donen halka + aktif parilti)
		self.etkButton = None
		try:
			self.etkButton = EventHudButton(self)
		except:
			import dbg, traceback
			dbg.TraceError("EventHudButton: " + traceback.format_exc())
		## KULLANICI (2026-09-27): pazar satis bildirimi dugmesi (Etkinlik'in altinda, ilk satista belirir)
		self.pazarButton = None
		try:
			import uipazarbildirim
			self.pazarButton = uipazarbildirim.PazarHudButton()
		except:
			import dbg, traceback
			dbg.TraceError("PazarHudButton: " + traceback.format_exc())
		## KULLANICI (2026-10-03): Gunluk Sans Carki dugmesi (uicark)
		self.carkButton = None
		try:
			self.carkButton = CarkHudButton(self)
		except:
			import dbg, traceback
			dbg.TraceError("CarkHudButton: " + traceback.format_exc())
		## KULLANICI (2026-10-05): Ejder Uyelik dugmesi (uiejder) - Carkin altinda
		self.ejderButton = None
		try:
			self.ejderButton = EjderHudButton(self)
		except:
			import dbg, traceback
			dbg.TraceError("EjderHudButton: " + traceback.format_exc())
		## DUGME DUZENI: ust sira ogelerini kaydet (uiMobileLayout), kayitli duzeni uygula
		try:
			import uiMobileLayout
			for (key, bn, ln, base) in (("chat", "ChatButton", "ChatLabel", 46.0 / 120.0), ("chr", "CharacterButton", "CharacterLabel", 46.0 / 32.0),
				("inv", "InventoryButton", "InventoryLabel", 46.0 / 32.0), ("msg", "MessengerButton", "MessengerLabel", 46.0 / 32.0),
				("sys", "SystemButton", "SystemLabel", 46.0 / 32.0),
				("menu", "MenuButton", "MenuLabel", 46.0 / 120.0), ("hide", "HideButton", "HideLabel", 46.0 / 120.0)):
				b = self.GetChild2(bn)
				if b:
					uiMobileLayout.Register(key, b, self.GetChild2(ln), "button", base, None, (0.0, 1.0))
			if self.etkButton:
				uiMobileLayout.Register("etk", self.etkButton.btn, self.etkButton.label, "button", 46.0 / 128.0, None, (0.0, 1.0))
			if getattr(self, "carkButton", None):
				uiMobileLayout.Register("cark", self.carkButton.btn, self.carkButton.label, "button", 46.0 / 128.0, None, (0.0, 1.0))
			if getattr(self, "ejderButton", None):
				uiMobileLayout.Register("ejder", self.ejderButton.btn, self.ejderButton.label, "button", 46.0 / 128.0, None, (0.0, 1.0))
			uiMobileLayout.ApplySaved()
		except:
			import dbg, traceback
			dbg.TraceError("MOBIL duzen kayit (hud): " + traceback.format_exc())
		self.hudHidden = False
		self.__LoadHidden()

		keyPanel = KeyPanel()
		keyPanel.LoadWindow(self)
		self.keyPanel = keyPanel

		self.duelLock = None
		try:
			self.duelLock = DuelLockButton()
		except:
			import dbg, traceback
			dbg.TraceError("DuelLockButton: " + traceback.format_exc())

	def OnUpdate(self):
		## HIZ (2026-10-01): TaskBar.OnUpdate bunu ELLE de cagiriyor; motor da cagirirsa ayni karede ikinci kez calismasin
		t = app.GetTime()
		if t == getattr(self, "_frameT", -1.0):
			return
		self._frameT = t
		duelLock = getattr(self, "duelLock", None)
		if duelLock:
			duelLock.Update()
		etk = getattr(self, "etkButton", None)
		if etk:
			etk.Update()
		pz = getattr(self, "pazarButton", None)
		if pz:
			pz.Update()
		ck = getattr(self, "carkButton", None)
		if ck:
			ck.Update()
		ej = getattr(self, "ejderButton", None)
		if ej:
			ej.Update()

	def Destroy(self):
		if _INSTANCE[0] is self:
			_INSTANCE[0] = None
		self.ClearDictionary()
		if self.keyPanel:
			self.keyPanel.ClearDictionary()
		self.keyPanel = None
		if getattr(self, "duelLock", None):
			self.duelLock.Destroy()
		self.duelLock = None
		if getattr(self, "etkButton", None):
			self.etkButton.Destroy()
		self.etkButton = None
		if getattr(self, "pazarButton", None):
			self.pazarButton.Destroy()
		self.pazarButton = None
		if getattr(self, "carkButton", None):
			self.carkButton.Destroy()
		self.carkButton = None
		if getattr(self, "ejderButton", None):
			self.ejderButton.Destroy()
		self.ejderButton = None
		try:
			import uipazarbildirim
			uipazarbildirim.DestroyAll()
		except:
			pass
		self.nameButton = None
		self.interface = None
		self.taskBar = None

	def SetTaskBar(self, taskBar):
		self.taskBar = taskBar

	def BindInterface(self, interface):
		self.interface = interface

	def GetGameWindow(self):
		if self.taskBar:
			return self.taskBar.GetGameWindow()
		return None

	# ui.Window.__init__ kurucuda self.Hide() cagirir - uyeler henuz yok (bkz. uitaskbar.py).
	def Hide(self):
		ui.ScriptWindow.Hide(self)
		keyPanel = getattr(self, "keyPanel", None)
		if keyPanel:
			keyPanel.Hide()

	## Dugmeler
	def __OnClickShot(self):
		# game.py:428 DIK_SYSRQ -> SaveScreen (1267)
		gameWindow = self.GetGameWindow()
		if gameWindow:
			gameWindow.SaveScreen()

	def __OnClickCamera(self):
		# game.py:200 GameWindow.Open: varsayilan kamera (cameraDistance/Pitch/Rotation/Height)
		import game
		app.SetCamera(game.cameraDistance, game.cameraPitch, game.cameraRotation, game.cameraHeight)

	def __OnClickEsc(self):
		# game.py:1940 OnPressEscapeKey (hedef imleci / tutulan esya / OpenSystemDialog)
		gameWindow = self.GetGameWindow()
		if gameWindow:
			gameWindow.OnPressEscapeKey()
		elif self.interface:
			self.interface.OpenSystemDialog()

	def __OnClickDeleteItem(self):
		# game.py:416 DIK_X -> interface.OpenDeleteItem
		if self.interface:
			self.interface.OpenDeleteItem()

	def __OnClickMenu(self):
		# game.py:415 DIK_F5 -> interface.OpenMenuWindow
		if self.interface:
			self.interface.OpenMenuWindow()

	def __OnClickKeyPanel(self):
		if self.keyPanel:
			self.keyPanel.Toggle()

	## KULLANICI (2026-09-14/15): Butonlari Gizle / Goster (sol ust kose). Yalniz ust siradaki dugmeler
	## gizlenir; joystick, yetenek yayi, saldiri, At, Yerden Al, HP/SP/EXP, kamera kaydirici KALIR. Kalici
	## (mobile_hud_hide.cfg; guncellemede silinmez).
	HIDE_FILE = "mobile_hud_hide.cfg"
	HIDE_TOP = ("ChatButton", "ChatLabel", "CharacterButton", "CharacterLabel", "InventoryButton", "InventoryLabel",
		"MessengerButton", "MessengerLabel", "SystemButton", "SystemLabel",
		"MenuButton", "MenuLabel")

	def __LoadHidden(self):
		hidden = False
		try:
			f = open(self.HIDE_FILE, "r")
			hidden = f.read().strip() == "1"
			f.close()
		except:
			hidden = False
		self.SetHudHidden(hidden, False)

	def __OnClickHide(self):
		self.SetHudHidden(not self.hudHidden, True)

	def SetHudHidden(self, hidden, save):
		self.hudHidden = hidden
		for n in self.HIDE_TOP:
			w = self.GetChild2(n)
			if w:
				if hidden:
					w.Hide()
				else:
					w.Show()
		# KULLANICI (2026-09-15): yalniz UST SIRA dugmeleri gizlenir (Yerden Al kalir)
		if hidden and self.keyPanel:
			self.keyPanel.Close()
		etk = getattr(self, "etkButton", None)	# 2026-09-23: Etkinlik dugmesi de ust sira ile gizlenir
		if etk:
			etk.SetHidden(hidden)
		pz = getattr(self, "pazarButton", None)
		if pz:
			pz.SetHidden(hidden)
		ck = getattr(self, "carkButton", None)
		if ck:
			ck.SetHidden(hidden)
		ej = getattr(self, "ejderButton", None)
		if ej:
			ej.SetHidden(hidden)
		try:		# 2026-10-01: "Etkiler" dugmesi (uiaktifetki) de ust sira ile gizlenir
			ae = getattr(self.GetGameWindow(), "aktifEtki", None)
			if ae:
				ae.SetHudHidden(hidden)
		except:
			pass
		btn = self.GetChild2("HideButton")
		if btn:
			img = hidden and "mobile/ui/hud_show" or "mobile/ui/hud_hide"
			btn.SetUpVisual(img + "_up.tga")
			btn.SetOverVisual(img + "_up.tga")
			btn.SetDownVisual(img + "_down.tga")
		lbl = self.GetChild2("HideLabel")
		if lbl:
			lbl.SetText(hidden and "G\xf6ster" or "Gizle")
		if save:
			try:
				f = open(self.HIDE_FILE, "w")
				f.write(hidden and "1" or "0")
				f.close()
			except:
				pass

	## Isimler (Alt)
	def __HoldShowName(self):
		gameWindow = self.GetGameWindow()
		if gameWindow and not self.showNameToggled:
			gameWindow.ShowName()

	def __ReleaseShowName(self):
		gameWindow = self.GetGameWindow()
		if gameWindow and not self.showNameToggled:
			gameWindow.HideName()

	def ToggleShowName(self):
		# Yalniz isim etiketleri: game.py OnUpdate ShowNameFlag ile textTail.ShowAllTextTail cagirir;
		# offlineshop isimleri ShowName/HideName'deki satirlarin aynisi.
		gameWindow = self.GetGameWindow()
		if not gameWindow:
			return
		self.showNameToggled = not self.showNameToggled
		gameWindow.ShowNameFlag = self.showNameToggled
		if app.__ENABLE_NEW_OFFLINESHOP__:
			import offlineshop
			if self.showNameToggled:
				offlineshop.ShowShopNames()
			else:
				offlineshop.HideShopNames()
		if self.nameButton:
			if self.showNameToggled:
				self.nameButton.Down()
			else:
				self.nameButton.SetUp()
