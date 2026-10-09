# H-HUD: pack'teki root/uitaskbar.py'nin MOBIL surumu (kaplama: mobile_root/uitaskbar.py).
# Telefonda (ve Windows'ta M2_MOBILE_ROOT ile) pack'teki uitaskbar.py'yi GOLGELER; PC pack'i
# ve PC gorunumu degismez. interfacemodule.py / game.py'nin kullandigi genel API AYNEN
# korunur (grep: TaskBar(), LoadWindow, BUTTON_*, IS_EXPANDED, SetToggleButtonEvent,
# BindInterface, SetItemToolTip, SetSkillToolTip, Destroy, OnUseSkill, OnActivateSkill,
# OnDeactivateSkill, OnChangeCurrentSkill, SelectMouseButtonEvent, RefreshStatus,
# RefreshStamina, RefreshSkill, RefreshQuickSlot, Show, Hide, IsShow, ShowMouseImage,
# HideMouseImage, ShowGift, HideGift, ExpandedTaskBar, modul MOUSE_SETTINGS islevleri).
# PC alt cubugu CIZILMEZ; yerine onayli tasarim (sancak2_mobil_hud.html):
#   (a) altin 4 kutu   = hizli slot F1-F4 (yerel 4-7)         uiscript/mobiletaskbar.py
#   (b) yetenek yayi 6 = hizli slot 1-4 + SONRAKI sayfanin 1-2 (player.GetGlobalQuickSlot)
#   (c) HP/SP/Enerji/EXP barlari (RefreshStatus/SetHP/SetSP/SetST/SetExperience yolu korunur)
#   (d) Yerden al Z   -> game.py:456 DIK_Z -> PickUpItem (1405 player.PickCloseItem)
#   (e) kamera kaydirici -> game.py:442 R ZoomCamera(CAMERA_TO_NEGATIVE) / 579 F
#       ZoomCamera(CAMERA_TO_POSITIVE) / 496-497 birakinca ZoomCamera(CAMERA_STOP)
#   (f) At -> game.py:583 (__PressGKey, Ctrl basili) net.SendChatPacket("/ride")
#   (g) Oto Av (KULLANICI 2026-09-15) -> interface.ToggleAutoWindow (mobile_root/uiauto.py); av surerken yesil ikon
# Ust sag dizi / sol ust / KISAYOLLAR paneli uimobilehud.py'de; TaskBar icinden kurulur
# (interfacemodule golgelenmez, tek golgelenen betik budur).
# Oyun penceresine erisim: interface.stream.curPhaseWindow (game.py:123 SetStream,
# networkmodule.py:247 SetPhaseWindow(game.GameWindow(self))).
#
# DOKUNMA KURALI (CSlotWindow::CCoverButton semantigi, PythonWindow.cpp):
#   kapak dugmesi sol=acik: dokun-birak -> OnSelectItemSlot -> SelectItemQuickSlot
#     -> tutulan esya yoksa KULLAN (PC: game.py:611 RequestUseLocalQuickSlot), varsa birak.
#   uzun basma (InputCore TAP_LONGPRESS -> sag tus) -> OnUnselectItemSlot -> ikonu TUT
#     (PC'deki sol-tik tutma); sonra baska kutuya dokun = tasi (AddQuickSlot),
#     dunyaya dokun = sil (game.py:1476-1477 RequestDeleteGlobalQuickSlot) - PC kurali.
import ui
import net
import item
import skill
import localeInfo
import wndMgr
import player
import constInfo
import mouseModule
import uiScriptLocale
import app
import uimobilestatus	# MOBIL (2026-09-24 gece): Durum HUD (EXP kureleri + HP/SP/Enerji satirlari)

MOBILE_TASKBAR = [None]	# MOBIL (2026-09-28): gecerli TaskBar (uicharacter "Hizli Aktar" buradan ulasir)

MOUSE_SETTINGS = [0, 0]

def InitMouseButtonSettings(left, right):
	global MOUSE_SETTINGS
	MOUSE_SETTINGS = [left, right]

def SetMouseButtonSetting(dir, event):
	global MOUSE_SETTINGS
	MOUSE_SETTINGS[dir] = event

def GetMouseButtonSettings():
	global MOUSE_SETTINGS
	return MOUSE_SETTINGS

def SaveMouseButtonSettings():
	global MOUSE_SETTINGS
	open("mouse.cfg", "w").write("%s\t%s" % tuple(MOUSE_SETTINGS))

def LoadMouseButtonSettings():
	global MOUSE_SETTINGS
	tokens = open("mouse.cfg", "r").read().split()

	if len(tokens) != 2:
		raise RuntimeError, "MOUSE_SETTINGS_FILE_ERROR"

	MOUSE_SETTINGS[0] = int(tokens[0])
	MOUSE_SETTINGS[1] = int(tokens[1])

def unsigned32(n):
	return n & 0xFFFFFFFFL

#-------------------Giftbox Begin------------------------------
# PC ile ayni (locale/tr/ui/giftbox.py); interface.ShowGift -> TaskBar.ShowGift

class GiftBox(ui.ScriptWindow):
	class TextToolTip(ui.Window):
		def __init__(self):
			ui.Window.__init__(self, "TOP_MOST")
			if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
			self.SetWindowName("GiftBox")
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetHorizontalAlignCenter()
			textLine.SetOutline()
			textLine.Show()
			self.textLine = textLine

		def __del__(self):
			ui.Window.__del__(self)

		def SetText(self, text):
			self.textLine.SetText(text)

		def OnRender(self):
			(mouseX, mouseY) = wndMgr.GetMousePosition()
			self.textLine.SetPosition(mouseX, mouseY - 15)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.tooltipGift = self.TextToolTip()
		self.tooltipGift.Show()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "giftbox.py")
		except:
			import exception
			exception.Abort("GiftBox.LoadWindow.LoadObject")

		# PC root/uitaskbar.py:83-84 BIREBIR. Bu pack'in ui.py ImageBox.SetEvent'i olay anahtari
		# ister (ui.py:1324) - PC GiftBox olay baglamaz (cihazda olculdu: IndexError -> arayuz kurulamadi).
		self.giftBoxIcon = self.GetChild("GiftBox_Icon")
		self.giftBoxToolTip = self.GetChild("GiftBox_ToolTip")
		self.tooltipGift.Hide()

	def __OnClickGiftBoxIcon(self):
		net.SendChatPacket("/gift")

	def __OnMouseOverIn(self):
		self.tooltipGift.Show()

	def __OnMouseOverOut(self):
		self.tooltipGift.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.giftBoxIcon = 0
		self.giftBoxToolTip = 0

#-------------------Giftbox End------------------------------

class ExpandedTaskBar(ui.ScriptWindow):

	def __init__(self):
		ui.Window.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.SetWindowName("ExpandedTaskBar")

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "ExpandedTaskBar.py")
		except:
			import exception
			exception.Abort("ExpandedTaskBar.LoadWindow.LoadObject")

		self.expandedTaskBarBoard = self.GetChild("ExpanedTaskBar_Board")

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def SetToolTipText(self, eButton, text):
		self.toggleButtonDict[eButton].SetToolTipText(text)

	def SetToggleButtonEvent(self, eButton, kEventFunc):
		self.toggleButtonDict[eButton].SetEvent(kEventFunc)

	def OnPressEscapeKey(self):
		self.Close()
		return True

class CameraKnob(ui.ImageBox):
	"""Kamera kaydirici topuzu: yukari surukle = R (ZoomCamera CAMERA_TO_NEGATIVE, game.py:442),
	asagi = F (CAMERA_TO_POSITIVE, 579), birakinca CAMERA_STOP (496-497). Sol tus basili
	surukleme fareyi yakalar (CWindowManager::m_pLeftCaptureWindow) -> parmak raydan
	ciksa da OnMouseLeftButtonUp gelir."""

	DEAD_ZONE = 6

	def __init__(self):
		ui.ImageBox.__init__(self, "TOP_MOST")
		self.dragging = False
		self.zoomDir = None
		self.centerX = 0
		self.centerY = 0
		self.travel = 0
		self.knobHalf = 0

	def __del__(self):
		ui.ImageBox.__del__(self)

	def Setup(self, centerX, centerY, travel):
		self.centerX = centerX
		self.centerY = centerY
		self.travel = travel
		self.knobHalf = self.GetWidth() / 2
		self.__Rest()

	def __Rest(self):
		self.SetPosition(self.centerX - self.knobHalf, self.centerY - self.knobHalf)

	def __SetZoom(self, dir):
		if dir == self.zoomDir:
			return
		self.zoomDir = dir
		app.ZoomCamera(dir)

	def BeginDrag(self):
		self.dragging = True
		self.zoomDir = None
		return True

	def EndDrag(self):
		if not self.dragging:
			return True
		self.dragging = False
		self.zoomDir = None
		app.ZoomCamera(app.CAMERA_STOP)
		self.__Rest()
		return True

	def OnMouseLeftButtonDown(self):
		return self.BeginDrag()

	def OnMouseLeftButtonUp(self):
		return self.EndDrag()

	# CImageBox::OnUpdate Python OnUpdate CAGIRMAZ (native PythonWindow.cpp:881, gercek client ile
	# ayni) -> kare basi tik ZoomTouchArea.OnUpdate (ui.Window, cagrilir) icinden gelir.
	# Cihazda olculdu: onceki OnUpdate hic calismiyordu, cubuk yakinlastirmiyordu.
	def Tick(self):
		if not self.dragging:
			return
		(mouseX, mouseY) = wndMgr.GetMousePosition()
		dy = mouseY - self.centerY
		dy = max(-self.travel, min(self.travel, dy))
		self.SetPosition(self.centerX - self.knobHalf, self.centerY + dy - self.knobHalf)
		if dy < -self.DEAD_ZONE:
			self.__SetZoom(app.CAMERA_TO_NEGATIVE)
		elif dy > self.DEAD_ZONE:
			self.__SetZoom(app.CAMERA_TO_POSITIVE)
		else:
			self.__SetZoom(app.CAMERA_STOP)

class ZoomTouchArea(ui.Window):
	"""KULLANICI (cihazda): kaydirici calismiyordu - parmak cogu zaman 35 px topuza degil raya
	dusuyordu (ray ImageBox dokunmayi yutar, olay yok). Rayin tamamini kaplayan genis, gorunmez
	dokunma alani: basinca topuz surukleme baslar, birakinca biter (sol tus yakalamasi bu
	pencerede kalir, parmak alan disina ciksa da OnMouseLeftButtonUp gelir)."""

	def __init__(self, knob):
		ui.Window.__init__(self, "UI_BOTTOM")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.knob = knob

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		if self.knob:
			self.knob.BeginDrag()
		return True

	def OnMouseLeftButtonUp(self):
		if self.knob:
			self.knob.EndDrag()
		return True

	def OnUpdate(self):
		if self.knob:
			self.knob.Tick()

class TaskBar(ui.ScriptWindow):

	BUTTON_CHARACTER = 0
	BUTTON_INVENTORY = 1
	BUTTON_MESSENGER = 2
	BUTTON_SYSTEM = 3
	BUTTON_CHAT = 4
	BUTTON_UMUT = 5
	BUTTON_EXPAND = 4
	IS_EXPANDED = False
	BUTTON_ANTI_EXP = 6
	IS_EXPANDED = False

	MOUSE_BUTTON_LEFT = 0
	MOUSE_BUTTON_RIGHT = 1
	NONE = 255

	EVENT_MOVE = 0
	EVENT_ATTACK = 1
	EVENT_MOVE_AND_ATTACK = 2
	EVENT_CAMERA = 3
	EVENT_SKILL = 4
	EVENT_AUTO = 5

	GAUGE_WIDTH = 95
	GAUGE_HEIGHT = 13

	# Mobil: slot pencere adlari ve yerel indeksleri (uiscript/mobiletaskbar.py ile ayni)
	QUICK_SLOT_PER_PAGE = 8			# QUICKSLOT_MAX_COUNT_PER_LINE (Packet.h:1151)
	QUICK_PAGE_COUNT = 4			# QUICKSLOT_MAX_LINE (Packet.h:1150)
	NEXT_PAGE_BASE = 8				# yay 5-6: sonraki sayfanin yerel 0/1'i = 8/9
	ARC_SLOT_INDEX = (0, 1, 2, 3, 4, 5)	# 1 2 3 4 F1 F2 (gecerli sayfa)
	## KULLANICI (2026-09-28): Butonlari Ozellestir > "Buton Ekle/Sil" - ekrana EKSTRA hizli slot. Once bos yerel F3/F4
	## (6, 7), sonra SONRAKI sayfanin 8 kutusu (8-15 = __IsNextPageSlot yolu). Liste EXTRA_FILE'da (cihazda kalici).
	EXTRA_SLOT_INDEX = (6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
	EXTRA_FILE = "mobile_hud_extra.cfg"
	BAR_IMG_W = 289.0				# bar_bg.tga
	BAR_FILL_IMG_W = 285.0			# bar_fill_*.tga
	COVER_UP = "mobile/ui/cover_up.tga"
	COVER_DOWN = "mobile/ui/cover_down.tga"

	QUICKPAGE_NUMBER_FILENAME = [
		"d:/ymir work/ui/game/taskbar/1.sub",
		"d:/ymir work/ui/game/taskbar/2.sub",
		"d:/ymir work/ui/game/taskbar/3.sub",
		"d:/ymir work/ui/game/taskbar/4.sub",
	]

	#gift icon show and hide
	def ShowGift(self):
		if not localeInfo.IsBRAZIL():
			self.wndGiftBox.Show()

	def HideGift(self):
		self.wndGiftBox.Hide()

	class TextToolTip(ui.Window):
		def __init__(self):
			ui.Window.__init__(self, "TOP_MOST")
			if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi

			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetHorizontalAlignCenter()
			textLine.SetOutline()
			textLine.Show()
			self.textLine = textLine

		def __del__(self):
			ui.Window.__del__(self)

		def SetText(self, text):
			self.textLine.SetText(text)

		def OnRender(self):
			(mouseX, mouseY) = wndMgr.GetMousePosition()
			self.textLine.SetPosition(mouseX, mouseY - 15)

	class SkillButton(ui.SlotWindow):
		# PC ile ayni (sag fare tusu "beceri" kipi icin gecerli beceri dugmesi); mobilde
		# gizli tutulur, OnChangeCurrentSkill / RefreshSkill API'si icin korunur.

		def __init__(self):
			ui.SlotWindow.__init__(self)
			if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi

			self.event = 0
			self.arg = 0

			self.slotIndex = 0
			self.skillIndex = 0
			self.tooltipSkill = 0

			slotIndex = 0
			wndMgr.SetSlotBaseImage(self.hWnd, "d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			wndMgr.AppendSlot(self.hWnd, slotIndex, 0, 0, 32, 32)
			self.SetCoverButton(slotIndex,	"d:/ymir work/ui/public/slot_cover_button_01.sub",\
											"d:/ymir work/ui/public/slot_cover_button_02.sub",\
											"d:/ymir work/ui/public/slot_cover_button_03.sub",\
											"d:/ymir work/ui/public/slot_cover_button_04.sub", True, False)
			self.SetSize(32, 32)

		def __del__(self):
			ui.SlotWindow.__del__(self)

		def Destroy(self):
			if 0 != self.tooltipSkill:
				self.tooltipSkill.HideToolTip()

		def RefreshSkill(self):
			if 0 != self.slotIndex:
				self.SetSkill(self.slotIndex)

		def SetSkillToolTip(self, tooltip):
			self.tooltipSkill = tooltip

		def SetSkill(self, skillSlotNumber):
			slotNumber = 0
			skillIndex = player.GetSkillIndex(skillSlotNumber)
			skillGrade = player.GetSkillGrade(skillSlotNumber)
			skillLevel = player.GetSkillLevel(skillSlotNumber)

			self.skillIndex = skillIndex
			if 0 == self.skillIndex:
				self.ClearSlot(slotNumber)
				return

			self.slotIndex = skillSlotNumber

			self.SetSkillSlotNew(slotNumber, skillIndex, skillGrade, skillLevel)
			self.SetSlotCountNew(slotNumber, skillGrade, skillLevel)

			if player.IsSkillCoolTime(skillSlotNumber):
				(coolTime, elapsedTime) = player.GetSkillCoolTime(skillSlotNumber)
				self.SetSlotCoolTime(slotNumber, coolTime, elapsedTime)

			if player.IsSkillActive(skillSlotNumber):
				self.ActivateSlot(slotNumber)

		def SetSkillEvent(self, event, arg=0):
			self.event = event
			self.arg = arg

		def GetSkillIndex(self):
			return self.skillIndex

		def GetSlotIndex(self):
			return self.slotIndex

		def Activate(self, coolTime):
			self.SetSlotCoolTime(0, coolTime)

			if skill.IsToggleSkill(self.skillIndex):
				self.ActivateSlot(0)

		def Deactivate(self):
			if skill.IsToggleSkill(self.skillIndex):
				self.DeactivateSlot(0)

		def OnOverInItem(self, dummy):
			# KULLANICI (2026-09-13): yaydaki beceri kutusunda ipucu ACILMAZ (savasirken pencere sacma)
			return

		def OnOverOutItem(self):
			if 0 != self.tooltipSkill:
				self.tooltipSkill.HideToolTip()

		def OnSelectItemSlot(self, dummy):
			if 0 != self.event:
				if 0 != self.arg:
					self.event(self.arg)
				else:
					self.event()

	def __init__(self):
		# KULLANICI (2026-09-13): mobil HUD en alt UI katmaninda; pack pencereleri ustte.
		ui.ScriptWindow.__init__(self, "UI_BOTTOM")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi

		self.quickPageNumImageBox = None
		self.tooltipItem = 0
		self.tooltipSkill = 0
		self.interface = None
		self.mobileHud = None
		self.cameraKnob = None
		self.zoomTouchArea = None

		self.tooltipHP = self.TextToolTip()
		self.tooltipHP.Show()
		self.tooltipSP = self.TextToolTip()
		self.tooltipSP.Show()
		self.tooltipST = self.TextToolTip()
		self.tooltipST.Show()
		self.tooltipEXP = self.TextToolTip()
		self.tooltipEXP.Show()

		self.skillCategoryNameList = [ "ACTIVE_1", "ACTIVE_2", "ACTIVE_3" ]
		self.skillPageStartSlotIndexDict = {
			"ACTIVE_1" : 1,
			"ACTIVE_2" : 21,
			"ACTIVE_3" : 41,
		}

		self.selectSkillButtonList = []
		self.quickslot = []
		self.quickslotDict = {}
		self.ringDict = {}
		self.statusHud = None	# MOBIL: Durum HUD (LoadWindow kurar)

		self.lastUpdateQuickSlot = 0
		self.SetWindowName("TaskBar")

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/mobiletaskbar.py")
		except:
			import exception
			exception.Abort("TaskBar.LoadWindow.LoadObject")

		# Hizli slotlar: her kutu tek slotlu SlotWindow (yerel indeks = slot numarasi);
		# halka gorseli ayri bir dugme (kenara dokunma da ayni isi yapar).
		self.quickslot = []
		self.quickslotDict = {}
		self.ringDict = {}
		MOBILE_TASKBAR[0] = self
		for i in xrange(len(self.ARC_SLOT_INDEX)):
			self.__BindQuickSlot(self.GetChild("arc_slot_%d" % i), self.GetChild("arc_ring_%d" % i), self.ARC_SLOT_INDEX[i])
		## KULLANICI (2026-09-27): beceri derecesi (P / G / M / seviye) ikonun ustune degil, kutunun sag altinda
		## ayri kucuk bronz kenarli kutuda (mobile/ui/skill_badge.png). Native sayi satiri beceride gizlenir.
		self.gradeBadge = {}
		for n in self.ARC_SLOT_INDEX:
			try:
				self.__MakeGradeBadge(n)
			except:
				import dbg, traceback
				dbg.TraceError("MOBIL beceri rozeti: " + traceback.format_exc())

		# Ust sag dizi + sol ust + KISAYOLLAR paneli (ayri kok pencere, TaskBar yonetir)
		import uiMobileHud
		self.mobileHud = uiMobileHud.MobileHud()
		self.mobileHud.LoadWindow()
		self.mobileHud.SetTaskBar(self)

		toggleButtonDict = {}
		toggleButtonDict[TaskBar.BUTTON_CHARACTER]=self.mobileHud.GetChild("CharacterButton")
		toggleButtonDict[TaskBar.BUTTON_INVENTORY]=self.mobileHud.GetChild("InventoryButton")
		toggleButtonDict[TaskBar.BUTTON_MESSENGER]=self.mobileHud.GetChild("MessengerButton")
		toggleButtonDict[TaskBar.BUTTON_SYSTEM]=self.mobileHud.GetChild("SystemButton")
		toggleButtonDict[TaskBar.BUTTON_UMUT]=self.mobileHud.GetChild("UmutBalikButton")
		if app.ENABLE_ANTI_EXP:
			toggleButtonDict[TaskBar.BUTTON_ANTI_EXP]=self.mobileHud.GetChild("AntiexpButton")
		# ChatButton var -> IS_EXPANDED False: interface ExpandedTaskBar kurmaz, ToggleChat baglar.
		toggleButtonDict[TaskBar.BUTTON_CHAT]=self.mobileHud.GetChild("ChatButton")
		# Mobil tasarimda olmayan PC dugmeleri (arkadaslar / balik botu / anti-exp) gizli.
		for name in ("UmutBalikButton", "AntiexpButton"):	# KULLANICI 2026-09-14: Arkadas dugmesi ust sirada gorunur
			self.mobileHud.GetChild(name).Hide()

		self.GetChild("PickButton").SetEvent(ui.__mem_func__(self.__OnClickPickButton))
		self.GetChild("HorseButton").SetEvent(ui.__mem_func__(self.__OnClickHorseButton))
		if hasattr(wndMgr, "SetButtonScale"):	# KULLANICI 2026-09-14: 2x ikon
			wndMgr.SetButtonScale(self.GetChild("HorseButton").hWnd, 46.0 / 128.0, 46.0 / 128.0)	# KULLANICI 2026-09-14: 64 -> 46 px
		self.mobileHorseMounted = None
		## KULLANICI (2026-09-15): Otomatik Av dugmesi (At'in solunda, uiscript/mobiletaskbar.py AutoHuntButton)
		autoBtn = self.GetChild2("AutoHuntButton")
		if autoBtn:
			autoBtn.SetEvent(ui.__mem_func__(self.__OnClickAutoHuntButton))
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(autoBtn.hWnd, 46.0 / 128.0, 46.0 / 128.0)
		self.mobileAutoRunning = None
		## KULLANICI (2026-09-15): Emoji dugmesi (Oto Av'in solunda) - basili tut + cek = emoji halkasi
		self.emojiTouchArea = None
		emojiImg = self.GetChild2("EmojiButton")
		if emojiImg:
			try:
				import uiEmojiWheel
				et = uiEmojiWheel.EmojiTouchArea(emojiImg, "mobile/ui/hud_emoji_up.tga", "mobile/ui/hud_emoji_down.tga")
				et.SetParent(self)
				(ex, ey) = emojiImg.GetGlobalPosition()
				et.SetPosition(ex - 6, ey - 6)
				et.SetSize(46 + 12, 46 + 12)
				et.Show()
				self.emojiTouchArea = et
			except:
				import dbg, traceback
				dbg.TraceError("EmojiTouchArea: " + traceback.format_exc())
		## DUGME DUZENI: yay slotlari, At, Yerden Al (uiMobileLayout)
		try:
			import uiMobileLayout
			for i in xrange(6):
				ring = self.GetChild2("arc_ring_%d" % i)
				slot = self.GetChild2("arc_slot_%d" % i)
				if ring and slot:
					# +/- paralar yayin MERKEZINDEN (saldiri topu 0.9152, 0.7328) DISARI - komsu kutularla cakismaz (Unity)
					(rx, ry) = self.__RingCenter(ring)
					uiMobileLayout.Register("arc%d" % i, slot, None, "slot", 1.0, ring, (rx - 0.9152 * wndMgr.GetScreenWidth(), ry - 0.7328 * wndMgr.GetScreenHeight()), ui.__mem_func__(self.__FollowGradeBadge))
			uiMobileLayout.Register("horse", self.GetChild("HorseButton"), self.GetChild2("HorseLabel"), "button", 46.0 / 128.0, None, (-1.0, 0.0))
			if self.GetChild2("AutoHuntButton"):	# KULLANICI 2026-09-15: Oto Av dugmesi de duzenlenebilir
				uiMobileLayout.Register("autohunt", self.GetChild2("AutoHuntButton"), self.GetChild2("AutoHuntLabel"), "button", 46.0 / 128.0, None, (-1.0, 0.0))
			if self.GetChild2("EmojiButton") and self.emojiTouchArea:	# KULLANICI 2026-09-16: Emoji dugmesi de duzenlenebilir
				uiMobileLayout.Register("emoji", self.GetChild2("EmojiButton"), self.GetChild2("EmojiLabel"), "image", 46.0 / 128.0, None, (-1.0, 0.0), self.emojiTouchArea.FollowImage)
			uiMobileLayout.Register("pick", self.GetChild("PickButton"), self.GetChild2("PickLabel"), "button", 1.0, None, (-1.0, -1.0))
			uiMobileLayout.Register("att", None, None, "touch", 1.0, None, (0.0, 1.0))	# native saldiri topu
			uiMobileLayout.SetDimHost(self)	# duzenleme karartmasi bu kokun icinde (GAME katmani gorunmuyordu)
			## ekstra hizli slot dugmeleri (kayitli liste) - ApplySaved'den ONCE kaydolur ki kayitli konumlari uygulansin
			self.extraSlots = []
			self.extraGrave = []
			for n in self.__LoadExtraList():
				self.__CreateExtra(n)
			uiMobileLayout.SetExtraHandlers(ui.__mem_func__(self.MobileAddExtra), ui.__mem_func__(self.MobileRemoveExtra))
			uiMobileLayout.ApplySaved()
		except:
			import dbg, traceback
			dbg.TraceError("MOBIL duzen kayit (taskbar): " + traceback.format_exc())

		# KULLANICI (2026-09-24 gece): Durum HUD - EXP kureleri + HP/SP/Enerji satirlari (uimobilestatus.py,
		# Desktop/Metin2-Durum-HUD prototipi). PC cagri yolu korunur: RefreshStatus -> SetHP/SetSP/SetST/SetExperience.
		try:
			self.statusHud = uimobilestatus.MobileStatusHud(self)
			self.statusHud.OnEnter()
		except:
			import dbg, traceback
			dbg.TraceError("MOBIL durum HUD kurulamadi: " + traceback.format_exc())
			self.statusHud = None

		# Kamera kaydirici topuzu (ray uiscript'te: ZoomTrack)
		track = self.GetChild("ZoomTrack")
		(trackX, trackY) = track.GetGlobalPosition()
		knob = CameraKnob()
		knob.SetParent(self)
		knob.LoadImage("mobile/ui/zoom_knob.tga")
		centerX = trackX + track.GetWidth() / 2
		centerY = trackY + track.GetHeight() / 2
		knob.Setup(centerX, centerY, track.GetHeight() / 2 - knob.GetHeight() / 2 - 4)
		# Genis dokunma alani (topuzun ALTINDA; topuza dogrudan dokunma da calisir)
		touch = ZoomTouchArea(knob)
		touch.SetParent(self)
		touchW = max(64, track.GetWidth() + 40)
		touch.SetPosition(centerX - touchW / 2, trackY - 8)
		touch.SetSize(touchW, track.GetHeight() + 16)
		touch.Show()
		self.zoomTouchArea = touch
		knob.SetTop()
		knob.Show()
		self.cameraKnob = knob

		# PC API: gecerli beceri dugmesi (mobilde gizli)
		self.curSkillButton = self.SkillButton()
		self.curSkillButton.SetParent(self)
		self.curSkillButton.SetPosition(0, 0)
		self.curSkillButton.Hide()
		self.curMouseModeButton = [ None, None ]

		self.mouseImage = ui.ImageBox("TOP_MOST")
		self.mouseImage.AddFlag("float")
		self.mouseImage.LoadImage("d:/ymir work/ui/game/taskbar/mouse_button_camera_01.sub")
		self.mouseImage.SetPosition(wndMgr.GetScreenWidth() - 40, wndMgr.GetScreenHeight() - 34)
		self.mouseImage.Hide()

		self.toggleButtonDict = toggleButtonDict

		#giftbox object
		wndGiftBox = GiftBox()
		wndGiftBox.LoadWindow()
		self.wndGiftBox = wndGiftBox

		self.__LoadMouseSettings()
		self.RefreshStatus()
		self.RefreshQuickSlot()

	def __BindQuickSlot(self, slot, ring, slotIndex):
		slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		# KULLANICI: suruklenen ikon kutunun icini TAM doldursun (dairesel). Ic cap: halka
		# gorselinin ic karanlik alani (slot_arc 62 -> 52, slot_gold 46 -> 38).
		if hasattr(wndMgr, "SetSlotRoundIcon"):
			inner = 52
			if ring.GetWidth() < 56:
				inner = 38
			wndMgr.SetSlotRoundIcon(slot.hWnd, inner)
		slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptyQuickSlot))
		slot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemQuickSlot))
		slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.UnselectItemQuickSlot))
		slot.SetUnselectEmptySlotEvent(ui.__mem_func__(self.SelectEmptyQuickSlot))
		slot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		ring.SetEvent(ui.__mem_func__(self.__OnClickRing), slotIndex)
		self.quickslot.append(slot)
		self.quickslotDict[slotIndex] = slot
		self.ringDict[slotIndex] = ring

	def BindInterface(self, interface):
		self.interface = interface
		if self.mobileHud:
			self.mobileHud.BindInterface(interface)

	def GetGameWindow(self):
		# game.py:123 interface.SetStream(stream); networkmodule.py:247 curPhaseWindow = GameWindow
		if not self.interface:
			return None
		stream = getattr(self.interface, "stream", None)
		if not stream:
			return None
		return getattr(stream, "curPhaseWindow", None)

	def __OnClickPickButton(self):
		# game.py:456 onPressKeyDict[app.DIK_Z] = PickUpItem -> 1405 player.PickCloseItem()
		gameWindow = self.GetGameWindow()
		if gameWindow:
			gameWindow.PickUpItem()
		else:
			player.PickCloseItem()

	def __OnClickHorseButton(self):
		# game.py:581-583 __PressGKey: Ctrl basili -> net.SendChatPacket("/ride")
		net.SendChatPacket("/ride")

	def __OnClickAutoHuntButton(self):
		# KULLANICI (2026-09-15): Otomatik Av penceresi (interfacemodule.ToggleAutoWindow -> uiAuto.AutoWindow)
		if self.interface and hasattr(self.interface, "ToggleAutoWindow"):
			self.interface.ToggleAutoWindow()

	def __LoadMouseSettings(self):
		try:
			LoadMouseButtonSettings()
			(mouseLeftButtonEvent, mouseRightButtonEvent) = GetMouseButtonSettings()
			if not self.__IsInSafeMouseButtonSettingRange(mouseLeftButtonEvent) or not self.__IsInSafeMouseButtonSettingRange(mouseRightButtonEvent):
					raise RuntimeError, "INVALID_MOUSE_BUTTON_SETTINGS"
		except:
			InitMouseButtonSettings(self.EVENT_MOVE_AND_ATTACK, self.EVENT_CAMERA)
			(mouseLeftButtonEvent, mouseRightButtonEvent) = GetMouseButtonSettings()

		try:
			self.SelectMouseButtonEvent(self.MOUSE_BUTTON_LEFT,	mouseLeftButtonEvent)
			self.SelectMouseButtonEvent(self.MOUSE_BUTTON_RIGHT,	mouseRightButtonEvent)
		except:
			InitMouseButtonSettings(self.EVENT_MOVE_AND_ATTACK, self.EVENT_CAMERA)
			(mouseLeftButtonEvent, mouseRightButtonEvent) = GetMouseButtonSettings()

			self.SelectMouseButtonEvent(self.MOUSE_BUTTON_LEFT,	mouseLeftButtonEvent)
			self.SelectMouseButtonEvent(self.MOUSE_BUTTON_RIGHT,	mouseRightButtonEvent)

	def __IsInSafeMouseButtonSettingRange(self, arg):
		return arg >= self.EVENT_MOVE and arg <= self.EVENT_AUTO

	def Destroy(self):
		SaveMouseButtonSettings()

		self.ClearDictionary()
		if self.mobileHud:
			self.mobileHud.Destroy()
		self.mobileHud = None
		self.cameraKnob = None
		self.zoomTouchArea = None
		if getattr(self, "emojiTouchArea", None):
			self.emojiTouchArea.Destroy()
		self.emojiTouchArea = None
		self.curMouseModeButton = 0
		self.curSkillButton = 0
		self.selectSkillButtonList = 0

		if getattr(self, "statusHud", None):
			self.statusHud.Destroy()
		self.statusHud = None

		self.tooltipItem = 0
		self.tooltipSkill = 0
		self.quickslot = 0
		self.quickslotDict = {}
		self.ringDict = {}
		self.toggleButtonDict = 0


		self.tooltipHP = 0
		self.tooltipSP = 0
		self.tooltipST = 0
		self.tooltipEXP = 0

		self.mouseImage = None
		self.interface = None

	# ui.Window.__init__ (ui.py:113) KURUCUDA self.Hide() cagirir - o anda TaskBar uyeleri
	# henuz yoktur (cihazda olculdu: AttributeError -> arayuz kurulamadi, yuklemede takildi).
	def Show(self):
		ui.ScriptWindow.Show(self)
		mobileHud = getattr(self, "mobileHud", None)
		if mobileHud:
			mobileHud.Show()

	def Hide(self):
		ui.ScriptWindow.Hide(self)
		mobileHud = getattr(self, "mobileHud", None)
		if mobileHud:
			mobileHud.Hide()

	def __OnClickQuickPageUpButton(self):
		player.SetQuickPage(player.GetQuickPage()-1)

	def __OnClickQuickPageDownButton(self):
		player.SetQuickPage(player.GetQuickPage()+1)

	def SetToggleButtonEvent(self, eButton, kEventFunc):
		self.toggleButtonDict[eButton].SetEvent(kEventFunc)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SetSkillToolTip(self, tooltipSkill):
		self.tooltipSkill = tooltipSkill
		self.curSkillButton.SetSkillToolTip(self.tooltipSkill)

	## Mouse Image
	def ShowMouseImage(self):
		self.mouseImage.SetTop()
		self.mouseImage.Show()

	def HideMouseImage(self):
		player.SetQuickCameraMode(False)
		self.mouseImage.Hide()

	## Gauge (PC ile ayni cagri yolu: interface.RefreshStatus -> RefreshStatus -> SetHP/SetSP/SetExperience)
	def RefreshStatus(self):
		curHP = player.GetStatus(player.HP)
		maxHP = player.GetStatus(player.MAX_HP)
		curSP = player.GetStatus(player.SP)
		maxSP = player.GetStatus(player.MAX_SP)
		curEXP = unsigned32(player.GetStatus(player.EXP))
		nextEXP = unsigned32(player.GetStatus(player.NEXT_EXP))
		recoveryHP = player.GetStatus(player.HP_RECOVERY)
		recoverySP = player.GetStatus(player.SP_RECOVERY)

		self.RefreshStamina()

		self.SetHP(curHP, recoveryHP, maxHP)
		self.SetSP(curSP, recoverySP, maxSP)
		self.SetExperience(curEXP, nextEXP)

	def RefreshStamina(self):
		curST = player.GetStatus(player.STAMINA)
		maxST = player.GetStatus(player.MAX_STAMINA)
		self.SetST(curST, maxST)

	def RefreshSkill(self):
		self.curSkillButton.RefreshSkill()
		for button in self.selectSkillButtonList:
			button.RefreshSkill()

	# KULLANICI (2026-09-24 gece): barlar/kureler uimobilestatus.MobileStatusHud'da (animasyonlu). PC imzalari korunur.
	def SetHP(self, curPoint, recoveryPoint, maxPoint):
		curPoint = min(curPoint, maxPoint)
		if maxPoint > 0:
			self.tooltipHP.SetText("%s : %d / %d" % (localeInfo.TASKBAR_HP, curPoint, maxPoint))
			if self.statusHud:
				self.statusHud.SetBar(0, curPoint, maxPoint, "HP", recoveryPoint)

	def SetSP(self, curPoint, recoveryPoint, maxPoint):
		curPoint = min(curPoint, maxPoint)
		if maxPoint > 0:
			self.tooltipSP.SetText("%s : %d / %d" % (localeInfo.TASKBAR_SP, curPoint, maxPoint))
			if self.statusHud:
				self.statusHud.SetBar(1, curPoint, maxPoint, "SP", recoveryPoint)

	def SetST(self, curPoint, maxPoint):
		curPoint = min(curPoint, maxPoint)
		if maxPoint > 0:
			self.tooltipST.SetText("%s : %d / %d" % (localeInfo.TASKBAR_ST, curPoint, maxPoint))
			if self.statusHud:
				self.statusHud.SetBar(2, curPoint, maxPoint, "ENERJÝ", 0)

	def SetExperience(self, curPoint, maxPoint):
		curPoint = min(curPoint, maxPoint)
		curPoint = max(curPoint, 0)
		maxPoint = max(maxPoint, 0)
		if self.statusHud:
			self.statusHud.SetExperience(curPoint, maxPoint)
		self.tooltipEXP.SetText("%s : %.2f%%" % (localeInfo.TASKBAR_EXP, float(curPoint) / max(1, float(maxPoint)) * 100))

	## QuickSlot
	def __IsNextPageSlot(self, slotNumber):
		return slotNumber >= self.NEXT_PAGE_BASE

	def __GetQuickSlotData(self, slotNumber):
		"""(Type, Position): yerel 0-7 gecerli sayfadan, 8-9 sonraki sayfadan (Alt+1/2 gibi)."""
		if self.__IsNextPageSlot(slotNumber):
			nextPage = (player.GetQuickPage() + 1) % self.QUICK_PAGE_COUNT
			globalIndex = nextPage * self.QUICK_SLOT_PER_PAGE + (slotNumber - self.NEXT_PAGE_BASE)
			return player.GetGlobalQuickSlot(globalIndex)
		return player.GetLocalQuickSlot(slotNumber)

	def __ToGlobalQuickSlotIndex(self, slotNumber):
		if self.__IsNextPageSlot(slotNumber):
			nextPage = (player.GetQuickPage() + 1) % self.QUICK_PAGE_COUNT
			return nextPage * self.QUICK_SLOT_PER_PAGE + (slotNumber - self.NEXT_PAGE_BASE)
		return player.LocalQuickSlotIndexToGlobalQuickSlotIndex(slotNumber)

	def __WithNextPage(self, slotNumber, func):
		"""Sonraki sayfa kutulari icin PC'deki Alt kurali (game.py:1299 ShowName SetQuickPage(+1),
		1365 HideName geri): sayfayi gecici degistirip yerel islevi cagirir."""
		if not self.__IsNextPageSlot(slotNumber):
			return func(slotNumber)
		page = player.GetQuickPage()
		player.SetQuickPage(page + 1)
		try:
			return func(slotNumber - self.NEXT_PAGE_BASE)
		finally:
			player.SetQuickPage(page)

	def __UseQuickSlot(self, slotNumber):
		# game.py:611 __PressQuickSlot -> player.RequestUseLocalQuickSlot(localSlotIndex)
		self.__WithNextPage(slotNumber, player.RequestUseLocalQuickSlot)

	## ---- HIZLI AKTAR (KULLANICI 2026-09-28): beceri penceresindeki dugme ------------------------------------
	def MobileQuickFillSkills(self, srcSlots):
		"""Ogrenilmis becerileri (beceri kaynak kutusu no) sirayla yay kutularina (1 2 3 4 F1 F2), sonra ekstra
		dugmelere yerlestirir (PC'de beceriyi kutuya surukleme = RequestAddLocalQuickSlot(yerel, SKILL, kaynak)).
		Donus: (yerlesen, sigmayan)."""
		targets = list(self.ARC_SLOT_INDEX) + list(getattr(self, "extraSlots", []))
		n = 0
		for (target, src) in zip(targets, srcSlots):
			self.__WithNextPage(target, lambda local, s=src: player.RequestAddLocalQuickSlot(local, player.SLOT_TYPE_SKILL, s))
			n += 1
		self.RefreshQuickSlot()
		return (n, max(0, len(srcSlots) - n))

	## ---- KARAKTER PENCERESI "Beceri Tuslari" (2026-10-09): hizli tus yonetimi icin acik arayuz -----------------
	## Tus no: yay 0-5 + eklenen (self.extraSlots, 6..15). Ad = SIRA (1..6 yay, 7.. eklenenler) - halka yazisiyla ayni.
	def MobileTusListesi(self):
		return list(self.ARC_SLOT_INDEX) + list(getattr(self, "extraSlots", []))

	def MobileTusAd(self, n):
		if n in self.ARC_SLOT_INDEX:
			return str(list(self.ARC_SLOT_INDEX).index(n) + 1)
		ek = list(getattr(self, "extraSlots", []))
		if n in ek:
			return str(len(self.ARC_SLOT_INDEX) + 1 + ek.index(n))
		return "?"

	def MobileTusVeri(self, n):
		return self.__GetQuickSlotData(n)

	def MobileTusKoy(self, n, tip, konum):
		self.__WithNextPage(n, lambda local: player.RequestAddLocalQuickSlot(local, tip, konum))
		self.RefreshQuickSlot()

	def MobileTusBosalt(self, n):
		try:
			player.RequestDeleteGlobalQuickSlot(self.__ToGlobalQuickSlotIndex(n))
		except:
			import dbg, traceback
			dbg.TraceError("MobileTusBosalt: " + traceback.format_exc())
		self.RefreshQuickSlot()

	def MobileTusDegistir(self, a, b):
		g = self.__ToGlobalQuickSlotIndex(a)
		self.__WithNextPage(b, lambda local: player.RequestMoveGlobalQuickSlotToLocalQuickSlot(g, local))
		self.RefreshQuickSlot()

	def MobileTusEkle(self):
		return self.MobileAddExtra()

	def MobileTusSil(self, n):
		return self.MobileRemoveExtra("ex%d" % n)

	def __EkHalkaNumarala(self):
		"""eklenen tuslarin halka dokusu = sira numarasi (7..16); silinen tusun arkasindakiler kayar"""
		for (i, n) in enumerate(list(getattr(self, "extraSlots", []))):
			ring = self.ringDict.get(n)
			if not ring:
				continue
			img = "mobile/ui/slot_arc_%d.tga" % (len(self.ARC_SLOT_INDEX) + 1 + i)
			try:
				ring.SetUpVisual(img)
				ring.SetOverVisual(img)
				ring.SetDownVisual(img)
			except:
				pass

	## ---- BECERI YER DEGISTIRME MODU (KULLANICI 2026-09-28) ----------------------------------------------------
	## Beceri penceresi yan dugmesi "Duzenle" (uibeceriduzen.py): kutular hafif nefes alan hale + "yer degistir"
	## isareti; basta iki kutunun ikonu bir kez yer degistirip geri gelir (ipucu). Dokun-dokun: once kaynak (parlar),
	## sonra hedef -> sunucu QuickSlotSwap (RequestMoveGlobalQuickSlotToLocalQuickSlot). Bu modda dokunmak KULLANMAZ.
	SWAP_HINT_SEC = 0.9
	SWAP_HINT_CYCLES = 2
	SWAP_PULSE_SEC = 1.6

	def MobileIsSwapMode(self):
		return getattr(self, "swapMode", False)

	def MobileSwapMode(self, on):
		if on == self.MobileIsSwapMode():
			return
		self.swapMode = on
		self.swapSel = -1
		if not hasattr(self, "swapFx"):
			self.swapFx = {}
		if on:
			if mouseModule.mouseController.isAttached():
				mouseModule.mouseController.DeattachObject()
			self.mobilePressQuick = -1
			self.__SwapHintStart()
			self.__SwapPlace()
		else:
			self.__SwapHintStop()
			for fx in self.swapFx.values():
				fx["glow"].Hide()
				fx["badge"].Hide()

	def __SwapFx(self, n):
		fx = self.swapFx.get(n)
		if fx:
			return fx
		glow = ui.ExpandedImageBox()
		glow.SetParent(self)
		glow.AddFlag("not_pick")
		glow.LoadImage("mobile/ui/edit_glow.tga")
		badge = ui.ExpandedImageBox()
		badge.SetParent(self)
		badge.AddFlag("not_pick")
		badge.LoadImage("mobile/ui/swap_badge.png")
		fx = {"glow": glow, "badge": badge}
		self.swapFx[n] = fx
		return fx

	def __SwapPlace(self):
		import math
		t = app.GetTime()
		for (n, ring) in self.ringDict.items():
			fx = self.__SwapFx(n)
			if not ring.IsShow():
				fx["glow"].Hide()
				fx["badge"].Hide()
				continue
			(rx, ry) = ring.GetLocalPosition()
			w = ring.GetWidth()
			sel = (n == self.swapSel)
			size = w * (sel and 1.7 or 1.45)
			g = fx["glow"]
			g.SetScale(size / 192.0, size / 192.0)
			g.SetPosition(int(rx + w / 2.0 - size / 2.0), int(ry + w / 2.0 - size / 2.0))
			if sel:
				g.SetAlpha(0.95)
			else:
				g.SetAlpha(0.30 + 0.25 * (0.5 + 0.5 * math.sin(t * 2.0 * math.pi / self.SWAP_PULSE_SEC + n * 0.7)))
			bs = w * 0.44
			b = fx["badge"]
			b.SetScale(bs / 48.0, bs / 48.0)
			b.SetPosition(int(rx - bs * 0.25), int(ry - bs * 0.25))
			if not g.IsShow():
				g.Show()
			if not b.IsShow():
				b.Show()

	def __SwapHintStart(self):
		order = [n for n in list(self.ARC_SLOT_INDEX) + list(getattr(self, "extraSlots", [])) if n in self.quickslotDict]
		filled = [n for n in order if self.__GetQuickSlotData(n)[0] != player.SLOT_TYPE_NONE]
		pair = []
		for n in filled + order:
			if n not in pair:
				pair.append(n)
			if len(pair) == 2:
				break
		self.swapHint = None
		if len(pair) < 2:
			return
		(a, b) = pair
		sa = self.quickslotDict[a]
		sb = self.quickslotDict[b]
		self.swapHint = {"a": sa, "b": sb, "pa": sa.GetLocalPosition(), "pb": sb.GetLocalPosition(), "t0": app.GetTime()}

	def __SwapHintUpdate(self):
		import math
		h = getattr(self, "swapHint", None)
		if not h:
			return
		el = app.GetTime() - h["t0"]
		if el >= self.SWAP_HINT_SEC * self.SWAP_HINT_CYCLES:
			self.__SwapHintStop()
			return
		u = (el % self.SWAP_HINT_SEC) / self.SWAP_HINT_SEC
		p = 0.5 - 0.5 * math.cos(2.0 * math.pi * u)		# 0 -> 1 -> 0 (yer degistirip geri gelir)
		(ax, ay) = h["pa"]
		(bx, by) = h["pb"]
		h["a"].SetPosition(int(ax + (bx - ax) * p), int(ay + (by - ay) * p))
		h["b"].SetPosition(int(bx + (ax - bx) * p), int(by + (ay - by) * p))

	def __SwapHintStop(self):
		h = getattr(self, "swapHint", None)
		self.swapHint = None
		if h:
			h["a"].SetPosition(*h["pa"])
			h["b"].SetPosition(*h["pb"])

	def MobileSwapRemoveSelected(self):
		## Duzenle modunda secili kutunun icerigini kaldirir (PC: ikonu tutup dunyaya birakmak = RequestDeleteGlobalQuickSlot)
		n = getattr(self, "swapSel", -1)
		if n < 0:
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "\xd6nce kald\xfdr\xfdlacak kutuya dokun, sonra Kald\xfdr'a bas.")
			return False
		self.swapSel = -1
		self.__SwapHintStop()
		try:
			player.RequestDeleteGlobalQuickSlot(self.__ToGlobalQuickSlotIndex(n))
		except:
			import dbg, traceback
			dbg.TraceError("MOBIL kutu kaldir: " + traceback.format_exc())
		self.RefreshQuickSlot()
		return True

	def __SwapTap(self, n):
		if self.swapSel < 0:
			self.swapSel = n
			return
		if self.swapSel == n:
			self.swapSel = -1
			return
		src = self.swapSel
		self.swapSel = -1
		self.__SwapHintStop()
		g = self.__ToGlobalQuickSlotIndex(src)
		self.__WithNextPage(n, lambda local: player.RequestMoveGlobalQuickSlotToLocalQuickSlot(g, local))
		self.RefreshQuickSlot()

	## ---- EKSTRA HIZLI SLOT DUGMELERI (KULLANICI 2026-09-28) --------------------------------------------------
	def __LoadExtraList(self):
		out = []
		try:
			f = open(self.EXTRA_FILE, "r")
			for t in f.read().split():
				n = int(t)
				if n in self.EXTRA_SLOT_INDEX and n not in out:
					out.append(n)
			f.close()
		except:
			pass
		return out

	def __SaveExtraList(self):
		try:
			f = open(self.EXTRA_FILE, "w")
			f.write(" ".join([str(n) for n in self.extraSlots]))
			f.close()
		except:
			import dbg, traceback
			dbg.TraceError("MOBIL ekstra dugme kaydi: " + traceback.format_exc())

	def __CreateExtra(self, n):
		import uiMobileLayout
		W = wndMgr.GetScreenWidth()
		H = wndMgr.GetScreenHeight()
		k = self.EXTRA_SLOT_INDEX.index(n)
		# varsayilan: beceri yayinin solunda, ekran ortasina dogru 5'erli iki sira (sonra suruklenir)
		cx = int(W * (0.66 - 0.055 * (k % 5)))
		cy = int(H * (0.50 + 0.13 * (k / 5)))
		ring = ui.Button()
		ring.SetParent(self)
		img = "mobile/ui/slot_arc_blank.tga"
		ring.SetUpVisual(img)
		ring.SetOverVisual(img)
		ring.SetDownVisual(img)
		ring.SetPosition(cx - ring.GetWidth() / 2, cy - ring.GetHeight() / 2)
		ring.Show()
		slot = ui.SlotWindow()
		slot.SetParent(self)
		slot.SetSize(32, 32)
		slot.AppendSlot(n, 0, 0, 32, 32)
		slot.SetPosition(cx - 16, cy - 16)
		slot.Show()
		self.__BindQuickSlot(slot, ring, n)
		try:
			self.__MakeGradeBadge(n)
		except:
			pass
		uiMobileLayout.Register("ex%d" % n, slot, None, "slot", 1.0, ring, (0.0, 1.0), ui.__mem_func__(self.__FollowGradeBadge))
		self.extraSlots.append(n)
		self.__EkHalkaNumarala()

	def MobileAddExtra(self):
		free = [n for n in self.EXTRA_SLOT_INDEX if n not in self.extraSlots]
		if not free:
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "En fazla %d ekstra buton eklenebilir." % len(self.EXTRA_SLOT_INDEX))
			return None
		n = free[0]
		self.__CreateExtra(n)
		self.__SaveExtraList()
		self.RefreshQuickSlot()
		return "ex%d" % n

	def MobileRemoveExtra(self, key):
		import uiMobileLayout
		n = None
		if key and key.startswith("ex"):
			try:
				n = int(key[2:])
			except:
				n = None
		if n is None and self.extraSlots:
			n = self.extraSlots[-1]
		if n is None or n not in self.extraSlots:
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Silinecek ekstra buton yok.")
			return False
		uiMobileLayout.Unregister("ex%d" % n)
		## kutudaki beceri/esya da kalksin (yeniden eklenince eski icerik gelmesin)
		try:
			player.RequestDeleteGlobalQuickSlot(self.__ToGlobalQuickSlotIndex(n))
		except:
			pass
		slot = self.quickslotDict.pop(n, None)
		ring = self.ringDict.pop(n, None)
		if slot in self.quickslot:
			self.quickslot.remove(slot)
		b = getattr(self, "gradeBadge", {}).pop(n, None)
		for w in (slot, ring, b and b.get("img")):
			if w:
				w.Hide()
		self.extraGrave.append((slot, ring, b))	# C++ pencereleri Python referansiyla yasar; gizli tutulur
		self.extraSlots.remove(n)
		self.__SaveExtraList()
		self.__EkHalkaNumarala()
		return True

	def __MakeGradeBadge(self, n):
		slot = self.quickslotDict.get(n)
		if not slot:
			return
		img = ui.ExpandedImageBox()
		img.SetParent(slot)		# kutuyla gizlenir/tasinir; ikonun USTUNDE cizilir (son cocuk)
		img.AddFlag("not_pick")
		img.LoadImage("mobile/ui/skill_badge.png")
		txt = ui.TextLine()
		txt.SetParent(img)
		txt.AddFlag("not_pick")
		txt.SetOutline()
		txt.SetFontColor(0.96, 0.92, 0.84)
		txt.SetHorizontalAlignCenter()
		txt.SetVerticalAlignCenter()
		txt.Show()
		img.Hide()
		self.gradeBadge[n] = {"img": img, "txt": txt, "font": 0, "text": ""}
		self.__PlaceGradeBadge(n)

	def __PlaceGradeBadge(self, n):
		b = self.gradeBadge.get(n)
		ring = self.ringDict.get(n)
		slot = self.quickslotDict.get(n)
		if not b or not ring or not slot:
			return
		(rx, ry) = ring.GetGlobalPosition()
		w = float(ring.GetWidth())
		size = max(12, int(round(w * 0.36)))
		(sx, sy) = slot.GetGlobalPosition()
		cx = rx + w * 0.5 + w * 0.31
		cy = ry + ring.GetHeight() * 0.5 + w * 0.31
		b["img"].SetScale(size / 96.0, size / 96.0)
		b["img"].SetPosition(int(cx - size / 2.0 - sx), int(cy - size / 2.0 - sy))
		f = max(9, int(round(size * 0.6)))
		if len(b["text"]) >= 3:
			f = max(8, int(round(size * 0.46)))
		if f != b["font"]:
			b["font"] = f
			b["txt"].SetFontName("Tahoma:%d" % f)
			if b["text"]:
				b["txt"].SetText(b["text"])
		b["txt"].SetPosition(size / 2, size / 2 - 1)

	def __FollowGradeBadge(self, main):
		## uiMobileLayout: halka tasininca/boyutlaninca rozet de gelsin (main = halka)
		for (n, ring) in self.ringDict.items():
			if ring is main or ring.hWnd == getattr(main, "hWnd", None):
				self.__PlaceGradeBadge(n)

	def __SetGradeBadge(self, n, text):
		b = getattr(self, "gradeBadge", {}).get(n)
		if not b:
			return
		if not text:
			b["img"].Hide()
			return
		if text != b["text"]:
			b["text"] = text
			b["font"] = 0	# 3 harfli (M10) kucuk font: yeniden hesapla
			self.__PlaceGradeBadge(n)
			b["txt"].SetText(text)
		b["img"].Show()

	def __FillQuickSlot(self, slot, slotNumber):
		(Type, Position) = self.__GetQuickSlotData(slotNumber)
		self.__SetGradeBadge(slotNumber, None)

		if player.SLOT_TYPE_NONE == Type:
			slot.ClearSlot(slotNumber)
			return

		if player.SLOT_TYPE_INVENTORY == Type:

			itemIndex = player.GetItemIndex(Position)
			itemCount = player.GetItemCount(Position)
			if itemCount <= 1:
				itemCount = 0

			if constInfo.IS_AUTO_POTION(itemIndex):
				metinSocket = [player.GetItemMetinSocket(Position, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]

				if 0 != int(metinSocket[0]):
					slot.ActivateSlot(slotNumber)
				else:
					slot.DeactivateSlot(slotNumber)

			slot.SetItemSlot(slotNumber, itemIndex, itemCount)

		elif player.SLOT_TYPE_SKILL == Type:

			skillIndex = player.GetSkillIndex(Position)
			if 0 == skillIndex:
				slot.ClearSlot(slotNumber)
				return

			skillType = skill.GetSkillType(skillIndex)
			if skill.SKILL_TYPE_GUILD == skillType:
				import guild
				skillGrade = 0
				skillLevel = guild.GetSkillLevel(Position)

			else:
				skillGrade = player.GetSkillGrade(Position)
				skillLevel = player.GetSkillLevel(Position)

			slot.SetSkillSlotNew(slotNumber, skillIndex, skillGrade, skillLevel)
			if slotNumber in getattr(self, "gradeBadge", {}):
				slot.SetSlotCountNew(slotNumber, skillGrade, 0)	# native yazi gizli -> rozet
				if skillGrade >= 3:
					t = "P"
				elif skillGrade == 2:
					t = "G%d" % max(1, min(10, skillLevel - 29 if skillLevel > 29 else skillLevel))
				elif skillGrade == 1:
					t = "M%d" % max(1, min(10, skillLevel - 19 if skillLevel > 19 else skillLevel))
				else:
					t = skillLevel > 0 and str(skillLevel) or ""
				self.__SetGradeBadge(slotNumber, t)
			else:
				slot.SetSlotCountNew(slotNumber, skillGrade, skillLevel)

			if player.IsSkillCoolTime(Position):
				(coolTime, elapsedTime) = player.GetSkillCoolTime(Position)
				slot.SetSlotCoolTime(slotNumber, coolTime, elapsedTime)

			if player.IsSkillActive(Position):
				slot.ActivateSlot(slotNumber)

		elif player.SLOT_TYPE_EMOTION == Type:

			emotionIndex = Position
			slot.SetEmotionSlot(slotNumber, emotionIndex)
			slot.SetSlotCount(slotNumber, 0)

		# Dolu her kutuya seffaf kapak: dokun-birak = kullan, uzun bas = tut (bkz. dosya basi)
		slot.SetCoverButton(slotNumber, self.COVER_UP, self.COVER_UP, self.COVER_DOWN, self.COVER_UP, True, True)

	def RefreshQuickSlot(self):
		for slotNumber, slot in self.quickslotDict.items():
			self.__FillQuickSlot(slot, slotNumber)
			slot.RefreshSlot()

	def canAddQuickSlot(self, Type, slotNumber):

		if player.SLOT_TYPE_INVENTORY == Type:

			itemIndex = player.GetItemIndex(slotNumber)
			return item.CanAddToQuickSlotItem(itemIndex)

		return True

	def __AddQuickSlotLocal(self, localSlotIndex):
		AttachedSlotType = mouseModule.mouseController.GetAttachedType()
		AttachedSlotNumber = mouseModule.mouseController.GetAttachedSlotNumber()
		AttachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

		if player.SLOT_TYPE_QUICK_SLOT == AttachedSlotType:
			player.RequestMoveGlobalQuickSlotToLocalQuickSlot(AttachedSlotNumber, localSlotIndex)

		elif player.SLOT_TYPE_EMOTION == AttachedSlotType:

			player.RequestAddLocalQuickSlot(localSlotIndex, AttachedSlotType, AttachedItemIndex)

		elif True == self.canAddQuickSlot(AttachedSlotType, AttachedSlotNumber):

			player.RequestAddLocalQuickSlot(localSlotIndex, AttachedSlotType, AttachedSlotNumber)

	def AddQuickSlot(self, localSlotIndex):
		self.__WithNextPage(localSlotIndex, self.__AddQuickSlotLocal)
		mouseModule.mouseController.DeattachObject()
		self.RefreshQuickSlot()

	def __OnClickRing(self, slotIndex):
		if getattr(self, "swapMode", False):
			self.__SwapTap(slotIndex)
			return
		# Halka (kutu kenari) dokunusu: kutunun kendisine dokunmak ile ayni
		if True == mouseModule.mouseController.isAttached():
			self.AddQuickSlot(slotIndex)
		else:
			(Type, Position) = self.__GetQuickSlotData(slotIndex)
			if player.SLOT_TYPE_NONE != Type:
				self.__UseQuickSlot(slotIndex)

	def SelectEmptyQuickSlot(self, slotIndex):
		if getattr(self, "swapMode", False):
			self.__SwapTap(slotIndex)
			return

		if True == mouseModule.mouseController.isAttached():
			self.AddQuickSlot(slotIndex)

	def SelectItemQuickSlot(self, localQuickSlotIndex):
		if getattr(self, "swapMode", False):
			self.__SwapTap(localQuickSlotIndex)
			return
		# Dokun-birak (kapak) / sol tus: tutulan esya varsa buraya birak, yoksa KULLAN
		if True == mouseModule.mouseController.isAttached():
			self.AddQuickSlot(localQuickSlotIndex)

		else:
			## KULLANICI (2026-09-14): basili tutup SURUKLEYINCE ikon parmaga yapisir, baska kutuya
			## birakinca yer degistirir (envanterdeki gibi); kisa dokunus birakinca KULLANIR.
			self.mobilePressQuick = localQuickSlotIndex

	def __MobileUpdateQuickPress(self):
		slot = getattr(self, "mobilePressQuick", -1)
		if slot < 0:
			return
		if wndMgr.IsDragging():
			self.mobilePressQuick = -1
			if False == mouseModule.mouseController.isAttached():
				globalQuickSlotIndex = self.__ToGlobalQuickSlotIndex(slot)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_QUICK_SLOT, globalQuickSlotIndex, globalQuickSlotIndex)
				self.mobileDragFrom = slot	# parmak kalkinca __MobileUpdateQuickDrop birakir
		elif not wndMgr.IsLeftButtonDown():
			self.mobilePressQuick = -1
			self.__UseQuickSlot(slot)

	def __MobileUpdateQuickDrop(self):
		## KULLANICI (2026-09-28): "sagdaki kutularin icindeki beceri ikonlarinin yerini degistiremiyoruz" - surukle-birak:
		## kutudan suruklenen ikon parmak KALKINCA birakilir (PC'de ikinci tik gerekirdi; telefonda birakma tik uretmez,
		## ikon parmakta asili kalip sonraki dunya dokunusunda SILINIYORDU). Baska kutunun ustunde birakma = yer degistir
		## (sunucu QuickSlotSwap), bos yerde birakma = iptal (ikon kutusunda kalir, silinmez).
		src = getattr(self, "mobileDragFrom", -1)
		if src < 0 or wndMgr.IsLeftButtonDown():
			return
		self.mobileDragFrom = -1
		if not mouseModule.mouseController.isAttached():
			return		# kutu kendi birakma olayini isledi
		if mouseModule.mouseController.GetAttachedType() != player.SLOT_TYPE_QUICK_SLOT:
			return
		target = -1
		try:
			(mx, my) = wndMgr.GetMousePosition()
			for (n, ring) in self.ringDict.items():
				if not ring.IsShow():
					continue
				(rx, ry) = ring.GetGlobalPosition()
				pad = 6
				if rx - pad <= mx <= rx + ring.GetWidth() + pad and ry - pad <= my <= ry + ring.GetHeight() + pad:
					target = n
					break
		except:
			target = -1
		if target >= 0 and target != src:
			self.AddQuickSlot(target)		# RequestMoveGlobalQuickSlotToLocalQuickSlot -> yer degistirir
		else:
			mouseModule.mouseController.DeattachObject()

	def UnselectItemQuickSlot(self, localSlotIndex):
		if getattr(self, "swapMode", False):
			self.__SwapTap(localSlotIndex)
			return
		# Uzun basma (sag tus): PC'deki sol-tik tutma - kutunun ikonunu fareye al
		if False == mouseModule.mouseController.isAttached():
			globalQuickSlotIndex=self.__ToGlobalQuickSlotIndex(localSlotIndex)
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_QUICK_SLOT, globalQuickSlotIndex, globalQuickSlotIndex)
			return

		elif mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()
			return

	def __ForEachSkillQuickSlot(self, usedSlotIndex, func):
		for slotNumber, slotWindow in self.quickslotDict.items():
			(Type, Position) = self.__GetQuickSlotData(slotNumber)
			if Type == player.SLOT_TYPE_SKILL:
				if usedSlotIndex == Position:
					func(slotWindow, slotNumber)

	def OnUseSkill(self, usedSlotIndex, coolTime):

		## Current Skill Button
		if usedSlotIndex == self.curSkillButton.GetSlotIndex():
			self.curSkillButton.Activate(coolTime)

		## Quick Slot
		self.__ForEachSkillQuickSlot(usedSlotIndex, lambda slotWindow, slotNumber: slotWindow.SetSlotCoolTime(slotNumber, coolTime))

	def OnActivateSkill(self, usedSlotIndex):

		if usedSlotIndex == self.curSkillButton.GetSlotIndex():
			self.curSkillButton.Deactivate()

		self.__ForEachSkillQuickSlot(usedSlotIndex, lambda slotWindow, slotNumber: slotWindow.ActivateSlot(slotNumber))

	def OnDeactivateSkill(self, usedSlotIndex):

		if usedSlotIndex == self.curSkillButton.GetSlotIndex():
			self.curSkillButton.Deactivate()

		self.__ForEachSkillQuickSlot(usedSlotIndex, lambda slotWindow, slotNumber: slotWindow.DeactivateSlot(slotNumber))

	## ToolTip
	def OverInItem(self, slotNumber):
		# KULLANICI (2026-09-13): yay kutularinda (beceri/esya) ipucu acilmaz
		return

		(Type, Position) = self.__GetQuickSlotData(slotNumber)

		if player.SLOT_TYPE_INVENTORY == Type:
			if 0 != self.tooltipItem:
				self.tooltipItem.SetInventoryItem(Position)
			if 0 != self.tooltipSkill:
				self.tooltipSkill.HideToolTip()

		elif player.SLOT_TYPE_SKILL == Type:

			skillIndex = player.GetSkillIndex(Position)
			skillType = skill.GetSkillType(skillIndex)

			if skill.SKILL_TYPE_GUILD == skillType:
				import guild
				skillGrade = 0
				skillLevel = guild.GetSkillLevel(Position)

			else:
				skillGrade = player.GetSkillGrade(Position)
				skillLevel = player.GetSkillLevel(Position)

			if 0 != self.tooltipSkill:
				self.tooltipSkill.SetSkillNew(Position, skillIndex, skillGrade, skillLevel)
			if 0 != self.tooltipItem:
				self.tooltipItem.HideToolTip()

	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		if 0 != self.tooltipSkill:
			self.tooltipSkill.HideToolTip()

	def __RingCenter(self, ring):
		(x, y) = ring.GetGlobalPosition()
		return (x + ring.GetWidth() / 2.0, y + ring.GetHeight() / 2.0)

	def __MobileUpdateHorseIcon(self):
		## KULLANICI (2026-09-14): Unity gibi - ata binili iken yesil (hud_horse_on), inik iken kahve.
		try:
			m = player.IsMountingHorse()
			if m != getattr(self, "mobileHorseMounted", None):
				self.mobileHorseMounted = m
				btn = self.GetChild("HorseButton")
				img = m and "mobile/ui/hud_horse_on.tga" or "mobile/ui/hud_horse_up.tga"
				btn.SetUpVisual(img)
				btn.SetOverVisual(img)
		except:
			pass

	def __MobileUpdateAutoHuntIcon(self):
		## KULLANICI (2026-09-15): At ikonu gibi - otomatik av SURERKEN yesil (hud_autohunt_on), degilken kahve.
		try:
			wnd = getattr(self.interface, "wndAutoWindow", None)
			running = bool(wnd and wnd.GetAutoStartonoff())
			if running != getattr(self, "mobileAutoRunning", None):
				self.mobileAutoRunning = running
				btn = self.GetChild2("AutoHuntButton")
				if btn:
					img = running and "mobile/ui/hud_autohunt_on.tga" or "mobile/ui/hud_autohunt_up.tga"
					btn.SetUpVisual(img)
					btn.SetOverVisual(img)
		except:
			pass

	def OnUpdate(self):
		hud = getattr(self, "mobileHud", None)	# DUELLO KILIT DUGMESI: HUD kendi OnUpdate'ini almayabilir
		if hud:
			hud.OnUpdate()
		self.__MobileUpdateHorseIcon()
		self.__MobileUpdateAutoHuntIcon()	# KULLANICI 2026-09-15: av suruyorsa yesil ikon
		self.__MobileUpdateQuickPress()
		self.__MobileUpdateQuickDrop()
		if getattr(self, "swapMode", False):
			self.__SwapHintUpdate()
			self.__SwapPlace()	# KULLANICI 2026-09-14: yay kutusu dokun/surukle ayrimi
		if app.GetGlobalTime() - self.lastUpdateQuickSlot > 500:
			self.lastUpdateQuickSlot = app.GetGlobalTime()
			self.RefreshQuickSlot()

		# KULLANICI (2026-09-24 gece): Durum HUD animasyonlari; PC ipuclari (IsIn) mobilde yok - kureye dokununca
		# EXP yazisi kurenin icinde (uimobilestatus).
		if self.statusHud:
			self.statusHud.OnUpdate()
		self.tooltipHP.Hide()
		self.tooltipSP.Hide()
		self.tooltipST.Hide()
		self.tooltipEXP.Hide()

	## Skill / fare kipi (PC API; mobilde fare kipi pencereleri yok)
	def ToggleLeftMouseButtonModeWindow(self):
		pass

	def ToggleRightMouseButtonModeWindow(self):
		pass

	def OpenSelectSkill(self):
		pass

	def CloseSelectSkill(self, slotIndex=-1):
		for button in self.selectSkillButtonList:
			button.Destroy()

		self.selectSkillButtonList = []

		if -1 != slotIndex:
			player.SetMouseFunc(player.MBT_RIGHT, player.MBF_SKILL)
			player.ChangeCurrentSkillNumberOnly(slotIndex-1)

	def SelectMouseButtonEvent(self, dir, event):
		# PC: fare tusu kipi (mouse.cfg) -> player.SetMouseFunc; gorsel dugme yok
		SetMouseButtonSetting(dir, event)

		self.CloseSelectSkill()

		type = self.NONE
		func = self.NONE

		if self.MOUSE_BUTTON_LEFT == dir:
			type = player.MBT_LEFT

		elif self.MOUSE_BUTTON_RIGHT == dir:
			type = player.MBT_RIGHT

		if self.EVENT_MOVE == event:
			func = player.MBF_MOVE
		elif self.EVENT_ATTACK == event:
			func = player.MBF_ATTACK
		elif self.EVENT_AUTO == event:
			func = player.MBF_AUTO
		elif self.EVENT_MOVE_AND_ATTACK == event:
			func = player.MBF_SMART
		elif self.EVENT_CAMERA == event:
			func = player.MBF_CAMERA
		elif self.EVENT_SKILL == event:
			func = player.MBF_SKILL

		player.SetMouseFunc(type, func)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.curSkillButton.SetSkill(skillSlotNumber)
