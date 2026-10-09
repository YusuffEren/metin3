# MOBIL KAPLAMA (mobile_root/uiinventory.py): pack root/uiinventory.py BIREBIR kopyasi. Farklar yalniz
# 'MOBIL:' yorumlu satirlar - buyuk kutular (wndMgr.SetSlotScale) ve ayri ekipman penceresinin
# kapatma dugmesi (yerlesim: mobile_root/locale/tr/ui/inventorywindow.py).
# 6 SUTUN ENVANTER (2026-09-15): 6x5 kutu, 6 sayfa sekmesi; Ekipman/Yukseltme dugmeleri + yang cubugu tek alt satirda.
## 6 SUTUN ENVANTER (2026-09-15): 6x8x4 sayfa (son sayfa 36 yuva). player.INVENTORY_PAGE_SIZE(45)/INVENTORY_PAGE_COUNT(4) client ikilisinde
## sabit ve degistirilemez; sayfa aritmetigi bu modul sabitlerini kullanir (genel yuva = sayfa*30 + yerel, yerel: sutun=%6, satir=//6).
INVENTORY_PAGE_SIZE = 48
INVENTORY_PAGE_COUNT = 4
MOBILE_SLOT_SCALE = 1.9375	# envanter yuva olcegi (uitoplusat okur; yerlesim SCALE ile AYNI)
import ui
import player
import mouseModule
import net
import app
import snd
import item
import player
import chat
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder # ���λ��� ������ ItemMove ����
import localeInfo
import constInfo
import ime
import wndMgr
import uiToolTip
if app.NEW_PVM_ATTRIBUTE:
	import uiPvMBonus

if app.ELDER_ATTRIBUTE_SYSTEM:
	import uiAttachBonus

if app.ENABLE_COSTUME_TIME:
	import uiCostumeTime

if app.__ENABLE_NEW_OFFLINESHOP__:
	import offlineshop
	import uiofflineshop

ITEM_MALL_BUTTON_ENABLE = True

ITEM_FLAG_APPLICABLE = 1 << 14

## KULLANICI (2026-09-27): "kapatma tusu cok guzel oldu, ekipman/envanter/kostum penceresine koy" -
## minimap HUD'undaki yuvarlak bronz carpi (mobile/ui/minimap/btn_close.png, 54x54) ui.TitleBar.btnClose gorseli olur.
## KULLANICI (2026-09-27): "tam kare yap, sag koseye yapisik olsun, biraz buyut belli olsun" -> ayni stilde kare surum (64x64)
ROUND_CLOSE_UP = "mobile/ui/minimap/btn_close_sq.png"
ROUND_CLOSE_DOWN = "mobile/ui/minimap/btn_close_sq_down.png"
ROUND_CLOSE_TEX = 64.0


def _MobileRoundClose(tb, size, pad):
	"""baslik cubugunun carpisini yuvarlak HUD dugmesine cevirir; size = cubuk biriminde cap."""
	btn = getattr(tb, "btnClose", None) if tb else None
	if not btn or not hasattr(wndMgr, "SetButtonScale"):
		return
	try:
		btn.SetUpVisual(ROUND_CLOSE_UP)
		btn.SetOverVisual(ROUND_CLOSE_UP)
		btn.SetDownVisual(ROUND_CLOSE_DOWN)
	except:
		return
	## standart ui.TitleBar: sag kapakta (titlebar_right.tga) pismis gri X kutusu var -> duz deri (orta parca) ile degistir
	if not getattr(tb, "mobileImgs", None) and getattr(tb, "imgRight", None):
		try:
			tb.imgRight.LoadImage("d:/ymir work/ui/pattern/titlebar_center.tga")
		except:
			pass
	k = float(size) / ROUND_CLOSE_TEX
	wndMgr.SetButtonScale(btn.hWnd, k, k)
	btn.SetPosition(tb.GetWidth() - btn.GetWidth() - pad, (tb.GetHeight() - btn.GetHeight()) / 2)
	hit = getattr(tb, "hitClose", None)
	if hit:
		hit.Fit()


def MobileMoneyDots(n):
	"""KULLANICI (2026-09-27): yang T/M/K yerine noktali: 90.685.376.402 Yang"""
	s = str(int(max(0, n)))
	g = []
	while len(s) > 3:
		g.insert(0, s[-3:])
		s = s[:-3]
	g.insert(0, s)
	return ".".join(g) + " |cffffcc00Yang|r"


COSTUME_GROW = 1.8 / 1.45		# ekipman penceresinin buyume orani ile ayni


class CostumeWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception
		
		if not app.ENABLE_COSTUME_SYSTEM:			
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return						
			 	 
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshCostumeSlot()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CostumeWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		## KULLANICI (2026-09-27): "ekipman ve kostum penceresi cok kucuk" - kostum penceresi (pack yerlesimi,
		## genel kok olcegi) ekipman penceresiyle ayni oranda (1.8 / 1.45) buyur
		try:
			if hasattr(wndMgr, "GetUIScale") and hasattr(wndMgr, "SetUIScale"):
				s0 = float(wndMgr.GetUIScale(self.hWnd))
				wndMgr.SetUIScale(self.hWnd, s0 * COSTUME_GROW)
		except:
			pass
		try:
			wndEquip = self.GetChild("CostumeSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			_MobileRoundClose(self.GetChild("TitleBar"), 27, 0)
			
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))						
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndEquip = wndEquip

	def RefreshCostumeSlot(self):
		getItemVNum=player.GetItemIndex
		
		for i in xrange(item.COSTUME_SLOT_COUNT):
			slotNumber = item.COSTUME_SLOT_START + i
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)

		self.wndEquip.RefreshSlot()
class RingWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):				
				 
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshEquipSlotWindow()
		#self.SetCenterPosition()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1
		

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/RingWindow.py")
		except:
			import exception
			exception.Abort("RingWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("RingSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))						
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndEquip = wndEquip

	def RefreshEquipSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndEquip.SetItemSlot
		for i in xrange(player.EQUIPMENT_PAGE_COUNT):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)

		if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			for i in xrange(player.NEW_EQUIPMENT_SLOT_COUNT):
				slotNumber = player.NEW_EQUIPMENT_SLOT_START + i
				itemCount = getItemCount(slotNumber)
				if itemCount <= 1:
					itemCount = 0
				setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
				print "ENABLE_NEW_EQUIPMENT_SYSTEM", slotNumber, itemCount, getItemVNum(slotNumber)

		self.wndEquip.RefreshSlot()
class InventoryWindow(ui.ScriptWindow):

	USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET","USE_COSTUME_ENCHANT", "USE_COSTUME_TRANSFORM")

	questionDialog = None
	tooltipItem = None
	wndCostume = None
	wndRing = None
	dlgPickMoney = None
	if app.ENABLE_ITEM_DELETE_SYSTEM:
		wndItemDelete = None
	if app.ENABLE_CUBE_RENEWAL:
		wndCubeRenewal = None
	sellingSlotNumber = -1
	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0		# �κ��丮 ���� �� �ڽ����� �����־����� ����-_-; ���̹� ����
	isOpenedBeltWindowWhenClosingInventory = 0		# �κ��丮 ���� �� ��Ʈ �κ��丮�� �����־����� ����-_-; ���̹� ����

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		uiToolTip.MOBILE_INVENTORY_WINDOW = self	# MOBIL: esya ipucu envanterin solunda acilsin (mobile_root/uitooltip.py)

		self.isOpenedBeltWindowWhenClosingInventory = 0		# �κ��丮 ���� �� ��Ʈ �κ��丮�� �����־����� ����-_-; ���̹� ����

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		## KULLANICI (2026-10-05): envanter HER ACILISTA ekipman KAPALI (ince) acilir - normal, markete / pazara tiklayinca;
		## ekipmani gormek isteyen baslikdaki "Ekipman" dugmesine basar
		try:
			self.__MobileGenislik(False)
		except:
			import dbg, traceback
			dbg.TraceError("TEK PENCERE ENVANTER genislik: " + traceback.format_exc())

		ui.ScriptWindow.Show(self)
		# KULLANICI (2026-09-14): ekipman ve yukseltme envanteri OTOMATIK ACILMAZ - envanterin solundaki
		# "Ekipman" / "Yukseltme" dugmeleriyle acilir (__MobileToggleEquip / __MobileToggleStorage).
		constInfo.INV_WITH_SPLIT = 0
		# MOBIL: mini haritanin/HUD'un altinda kalmasin (pencereler hep ustte)
		self.SetTop()

		# �κ��丮�� ���� �� �ڽ����� �����־��ٸ� �κ��丮�� �� �� �ڽ����� ���� ������ ��.
		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show() 

	def BindInterfaceClass(self, interface):
		self.interface = interface
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()

			if ITEM_MALL_BUTTON_ENABLE:
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "InventoryWindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindow.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.wndMoney = self.GetChild("Money")
			self.wndMoneySlot = self.GetChild("Money_Slot")
			self.mallButton = self.GetChild2("MallButton")
			self.costumeButton = self.GetChild2("CostumeButton")
			self.ringButton = self.GetChild2("RingButton")
			
			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("Inventory_Tab_01"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_02"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_03"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_04"))

			self.equipmentTab = []
			self.equipmentTab.append(self.GetChild("Equipment_Tab_01"))
			self.equipmentTab.append(self.GetChild("Equipment_Tab_02"))

			if self.costumeButton and not app.ENABLE_COSTUME_SYSTEM:
				self.costumeButton.Hide()
				self.costumeButton.Destroy()
				self.costumeButton = 0
			
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		## MOBIL: kutulari buyut + ekipman penceresi kendi carpisi ile kapanir
		MOBILE_SLOT_SCALE = 1.9375	# yerlesim SCALE ile AYNI (TEK PENCERE ENVANTER 2026-10-05: 62 px; eski 1.8)
		if hasattr(wndMgr, "SetSlotScale"):
			wndMgr.SetSlotScale(wndItem.hWnd, MOBILE_SLOT_SCALE)
			wndMgr.SetSlotScale(wndEquip.hWnd, 1.7)	# yerlesim EQ_SCALE ile AYNI (TEK PENCERE ENVANTER 2026-10-05; eski 2.1)
			wco = self.GetChild2("MobileCostumeSlot")
			if wco:
				wndMgr.SetSlotScale(wco.hWnd, 1.62)	# yerlesim CO_SCALE ile AYNI
		## KULLANICI (2026-09-14): baslik cubugu Yukseltme Envanteri gibi GENIS (1.6x), carpi 2.2x (parmakla rahat)
		self.__MobileWideTitleBar(self.GetChild2("TitleBar"), self.GetChild2("TitleName"))
		self.__MobileWideTitleBar(self.GetChild2("EquipTitleBar"), self.GetChild2("EquipTitleName"))
		## KULLANICI (2026-09-14): envanterin solundaki Ekipman / Yukseltme dugmeleri
		## 6 SUTUN ENVANTER (2026-09-15): dugmeler yang cubugunun SOLUNDA tek satirda; olcek yerlesimdeki BTN_W/BTN_H ile AYNI
		for (bn, ev) in (("MobileEquipButton", self.__MobileToggleEquip), ("MobileStorageButton", self.__MobileToggleStorage)):
			b = self.GetChild2(bn)
			if b:
				if hasattr(wndMgr, "SetButtonScale"):
					wndMgr.SetButtonScale(b.hWnd, 1.6, 1.6)	# KULLANICI 2026-09-15: topuzlu baslik cubugu dugmesi 106x23 -> 170x37
				if b.ButtonText:
					b.ButtonText.SetFontName("Tahoma:19")	# KULLANICI 2026-09-15: yazi biraz buyuk
					b.ButtonText.SetFontColor(1.0, 0.93, 0.78)	# baslik yazisi rengi
					b.ButtonText.SetVerticalAlignCenter()
					b.ButtonText.SetHorizontalAlignCenter()
					b.ButtonText.SetPosition(b.GetWidth() / 2, b.GetHeight() / 2 - 3)	# KULLANICI: dikey ortali (yazi 3 px asagida kaliyordu)
				b.SetEvent(ui.__mem_func__(ev))
		# 6 SUTUN ENVANTER (2026-09-15): dugmeler ARTIK ORTALANMAZ - yerlesim (inventorywindow.py) sola, yang cubugu saga koyar
		# MOBIL: 6 sekme pencere genisligini doldurur (39x19 gorsel -> (IW-20)/6 x 27) (6 SUTUN ENVANTER)
		if hasattr(wndMgr, "SetButtonScale"):
			for i in xrange(INVENTORY_PAGE_COUNT):
				tab = self.GetChild2("Inventory_Tab_0%d" % (i + 1))
				if tab:
					wndMgr.SetButtonScale(tab.hWnd, ((self.GetChild("board").GetWidth() - 20) / INVENTORY_PAGE_COUNT) / 39.0, 27.0 / 19.0)
		try:
			self.__MobileTekPencereKur()	# TEK PENCERE ENVANTER (2026-10-05)
		except:
			self.mobileLeft = None
			import dbg, traceback
			dbg.TraceError("TEK PENCERE ENVANTER kurulum: " + traceback.format_exc())
		self.mobileEquipBoard = self.GetChild2("EquipBoard")
		## MOBIL: ekipman penceresi KENDI kok penceresinde (envanterden AYRI surukleme;
		## baslik "attach" bayragiyla GetRoot()'u surukler). Yerlesim olcekli oldugundan genel olcek disi.
		self.mobileEquipRoot = None
		if self.mobileEquipBoard:
			root = ui.ScriptWindow()
			if hasattr(wndMgr, "SetUIScale"):
				wndMgr.SetUIScale(root.hWnd, 1.0)
			root.AddFlag("movable")
			root.AddFlag("float")
			root.SetWindowName("MobileEquipRoot")
			root.SetSize(self.mobileEquipBoard.GetWidth(), self.mobileEquipBoard.GetHeight())
			(gx, gy) = self.mobileEquipBoard.GetGlobalPosition()
			self.mobileEquipBoard.SetParent(root)
			self.mobileEquipBoard.SetPosition(0, 0)
			root.SetPosition(gx, gy)
			self.mobileEquipRoot = root
			self.mobileEquipHome = (gx, gy)
		equipTitle = self.GetChild2("EquipTitleBar")
		if equipTitle and self.mobileEquipRoot:
			equipTitle.SetCloseEvent(ui.__mem_func__(self.mobileEquipRoot.Hide))

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## Equipment
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()

		## RefineDialog
		self.refineDialog = uiRefine.RefineDialog()
		self.refineDialog.Hide()

		## AttachMetinDialog
		self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
		self.attachMetinDialog.Hide()

		if app.ELDER_ATTRIBUTE_SYSTEM:
			## AttachBonusDialog
			self.attachBonusDialog = uiAttachBonus.AttachBonusDialog(self)
			self.attachBonusDialog.Hide()
            
		if app.NEW_PVM_ATTRIBUTE:
			self.PvMBonusDialog = uiPvMBonus.PvMBonusDialog(self)
			self.PvMBonusDialog.Hide()

		if app.ENABLE_COSTUME_TIME:
			self.CostumeTimeDialog = uiCostumeTime.TimeDialog(self)
			self.CostumeTimeDialog.Hide()
            
		## MoneySlot
		self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		self.inventoryTab[0].SetEvent(lambda arg=0: self.SetInventoryPage(arg))
		self.inventoryTab[1].SetEvent(lambda arg=1: self.SetInventoryPage(arg))
		self.inventoryTab[2].SetEvent(lambda arg=2: self.SetInventoryPage(arg))
		self.inventoryTab[3].SetEvent(lambda arg=3: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()
		self.inventoryPageIndex = 0

		self.equipmentTab[0].SetEvent(lambda arg=0: self.SetEquipmentPage(arg))
		self.equipmentTab[1].SetEvent(lambda arg=1: self.SetEquipmentPage(arg))
		self.equipmentTab[0].Down()
		self.equipmentTab[0].Hide()
		self.equipmentTab[1].Hide()

		self.wndItem = wndItem
		self.wndEquip = wndEquip
		self.dlgPickMoney = dlgPickMoney

		# MallButton
		if self.mallButton:
			self.mallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))
		
		# Costume Button
		if self.costumeButton:
			self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))
		self.__MobileCostumeBesideMall()
		
		if self.ringButton:
			self.ringButton.SetEvent(ui.__mem_func__(self.ClickRingButton))

		self.wndCostume = None
		self.wndRing = None
 		#####

		## Refresh
		self.SetInventoryPage(0)
		self.SetEquipmentPage(0)
		self.RefreshItemSlot()
		self.RefreshStatus()

	def Destroy(self):
		for b in (getattr(self, "mobileChestButton", None), getattr(self, "mobileSplitButton", None)):
			if b:
				b.Hide()
		self.mobileChestButton = None
		self.mobileSplitButton = None
		self.mobileChestSlot = -1
		self.mobileSplitSlot = -1
		self.ClearDictionary()

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0

		self.refineDialog.Destroy()
		self.refineDialog = 0

		self.attachMetinDialog.Destroy()
		self.attachMetinDialog = 0

		if app.NEW_PVM_ATTRIBUTE:
			self.PvMBonusDialog.Destroy()
			self.PvMBonusDialog = 0

		if app.ENABLE_COSTUME_TIME:
			self.CostumeTimeDialog.Destroy()
			self.CostumeTimeDialog = 0
		
		if app.ELDER_ATTRIBUTE_SYSTEM:
			self.attachBonusDialog.Destroy()
			self.attachBonusDialog = 0

		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.dlgPickMoney = 0
		self.wndMoney = 0
		self.wndMoneySlot = 0
		self.questionDialog = None
		self.mallButton = None
		self.interface = None

		if self.wndRing:
			self.wndRing.Destroy()
			self.wndRing = 0

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = 0
			
		self.inventoryTab = []
		self.equipmentTab = []

	def __MobileWideTitleBar(self, tb, nameWnd, scale = 1.6, closeScale = 2.0):
		## ui.TitleBar gorselleri (32x32, 23 px cubuk) ImageBox -> olceklenemez; ExpandedImageBox ile 1.6x yeniden kur.
		if not tb:
			return
		w = tb.GetWidth()
		h = int(round(ui.TitleBar.BLOCK_HEIGHT * scale))
		bw = int(round(ui.TitleBar.BLOCK_WIDTH * scale))
		for img in (tb.imgLeft, tb.imgCenter, tb.imgRight):
			img.Hide()
		pat = "d:/ymir work/ui/pattern/titlebar_"
		imgs = []
		# sag kapak (titlebar_right.tga) icinde pismis gri X kutusu var (1.6x'te carpinin altindan tasiyordu) -> kullanilmaz
		for (n, x) in (("left", 0), ("center", bw)):
			e = ui.ExpandedImageBox()
			e.SetParent(tb)
			e.AddFlag("not_pick")
			e.LoadImage(pat + n + ".tga")
			e.SetScale(scale, scale)
			e.SetPosition(x, 0)
			e.Show()
			imgs.append(e)
		# cizim genisligi = 32*olcek + 32*r (GrpExpandedImageInstance: RenderingRect olceksiz gorsel genisligiyle carpilir)
		imgs[1].SetRenderingRect(0.0, 0.0, float(w - 2 * bw) / ui.TitleBar.BLOCK_WIDTH, 0.0)	# orta parca bar sonuna kadar
		tb.mobileImgs = imgs
		tb.SetSize(w, h)
		btn = getattr(tb, "btnClose", None)
		if btn:
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(btn.hWnd, closeScale, closeScale)
			btn.SetPosition(w - btn.GetWidth() - 4, (h - btn.GetHeight()) / 2)
			_MobileRoundClose(tb, h * 1.15, 0)	# kare HUD carpisi, sag koseye yapisik (olcek + konum yeniden)
			btn.SetTop()
		if nameWnd:
			# ayni ebeveyne SetParent cizim sirasini degistirmiyor -> yazi yeni gorsellerin altinda kaliyordu: yeni TextLine
			nameWnd.Hide()
			t = ui.TextLine()
			t.SetParent(tb)
			t.AddFlag("not_pick")
			t.SetFontName("Tahoma:22")	# KULLANICI: "yazi kucuk, silik"
			t.SetOutline()
			t.SetFontColor(1.0, 0.93, 0.78)
			t.SetHorizontalAlignCenter()
			t.SetText(nameWnd.GetText())
			t.SetPosition(w / 2, (h - 24) / 2)
			t.Show()
			tb.mobileTitle = t
		if btn:
			btn.SetParent(self)	# cizim sirasi: once baska ebeveyne...
			btn.SetParent(tb)	# ...sonra geri -> listenin sonuna (yeni gorsellerin USTUNE)
			btn.SetPosition(w - btn.GetWidth(), (h - btn.GetHeight()) / 2)	# sag koseye yapisik
			btn.Show()
			hit = getattr(tb, "hitClose", None)
			if hit:
				hit.SetParent(self)
				hit.SetParent(tb)	# carpinin ustune (son cocuk)
				hit.Fit(56)
				hit.Show()

	## ---------------- TEK PENCERE ENVANTER (KULLANICI 2026-10-05) ----------------
	## Prototip Desktop/Averos2-Envanter-Prototip onaylandi: envanter + ekipman AYNI pencerede; baslikdaki "Ekipman"
	## dugmesi sol paneli (Ekipman / Kostum sekmeleri + bebek + karakter bilgisi) katlar, pencere yalniz envanter kalir
	## (sag kenar sabit). Her acilista ince. Esyaya dokununca oyunun efsun penceresi AYNEN acilir (degismedi).
	MOBILE_LW = 342		# sol panel genisligi (locale/tr/ui/inventorywindow.py LW ile AYNI)
	MOBILE_TAB = "mobile/ui/aet/"

	def __MobileTekPencereKur(self):
		self.mobileGenis = False
		self.mobileGenisKuruldu = False
		self.mobileSolSekme = "ek"
		self.mobileStat = []
		board = self.GetChild2("board")
		L = self.GetChild2("MobileLeftPanel")
		self.mobileLeft = L
		if not board or not L:
			self.mobileLeft = None
			return
		self.mobileIW = board.GetWidth()
		## baslik yazisi sola (ortada "Ekipman" dugmesiyle cakisirdi)
		tb = self.GetChild2("TitleBar")
		t = getattr(tb, "mobileTitle", None) if tb else None
		if t:
			t.SetHorizontalAlignLeft()
			t.SetPosition(26, (tb.GetHeight() - 24) / 2)	# KULLANICI 2026-10-05: 14 kosenin disina tasiyordu -> hafif saga
		## dugmeler: Ekipman (baslikta 118x33), Yukseltme (yang satirinda 127x40)
		for (n, sx, sy, f) in (("MobileEquipButton", 118 / 106.0, 33 / 23.0, 16), ("MobileStorageButton", 127 / 106.0, 40 / 23.0, 17)):
			b = self.GetChild2(n)
			if not b:
				continue
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(b.hWnd, sx, sy)
			if b.ButtonText:
				b.ButtonText.SetFontName("Tahoma:%d" % f)
				b.ButtonText.SetPosition(b.GetWidth() / 2, b.GetHeight() / 2 - 2)
		## genis yerlesimde LW kadar saga kayan parcalar (ilk / ince konumlari)
		self.mobileSag = []
		for n in ("Inventory_Tab_01", "Inventory_Tab_02", "Inventory_Tab_03", "Inventory_Tab_04", "ItemSlot", "Money_Slot", "MobileStorageButton"):
			w = self.GetChild2(n)
			if w:
				self.mobileSag.append((w, w.GetLocalPosition()))
		## sol panel zeminleri (yerlesimdeki parcalarin ALTINDA kalsin: once kur, sonra parcalari yeniden ekle)
		ih = board.GetHeight()
		self.__MobileKutu(L, 14, 79, 324, 330)
		self.__MobileKutu(L, 14, 417, 324, ih - 417 - 9)
		for n in ("Equipment_Base", "EquipmentSlot", "RingButton", "MallButton", "CostumeButton", "Equipment_Tab_01",
				  "Equipment_Tab_02", "MobileCostumeBase", "MobileCostumeSlot"):
			w = self.GetChild2(n)
			if w:
				p = w.GetLocalPosition()
				w.SetParent(board)
				w.SetParent(L)		# cocuk listesinin sonuna: zeminin USTUNDE
				w.SetPosition(p[0], p[1])
		## Ekipman / Kostum sekmeleri (Etkiler penceresinin sekme dokusu, 217x54 -> 160x27)
		self.mobileSekmeler = {}
		for (i, key, ad) in ((0, "ek", "Ekipman"), (1, "ko", "Kost\xfcm")):
			b = ui.Button()
			b.SetParent(L)
			b.SetUpVisual(self.MOBILE_TAB + "tab_up.png")
			b.SetOverVisual(self.MOBILE_TAB + "tab_over.png")
			b.SetDownVisual(self.MOBILE_TAB + "tab_on.png")
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(b.hWnd, 160 / 217.0, 27 / 54.0)
			b.SetPosition(14 + i * 164, 48)
			b.SetText(ad)
			if b.ButtonText:
				b.ButtonText.SetFontName("Tahoma:16")
				b.ButtonText.SetPosition(b.GetWidth() / 2, b.GetHeight() / 2 - 2)
			b.SetEvent(lambda k = key: self.__MobileSolSekme(k))
			b.Show()
			self.mobileSekmeler[key] = b
		## karakter bilgisi (sol alt kutu)
		y = 427
		bas = self.__MobileYazi(L, 26, y, 0xffe8d08a, False, 17)
		bas.SetText("Karakter")
		self.mobileStat = []
		for (i, ad) in enumerate(("Seviye", "Sald\xfdr\xfd", "Savunma", "Maks. HP", "Maks. SP", "Hareket H\xfdz\xfd")):
			a = self.__MobileYazi(L, 26, y + 26 + i * 22, 0xffc9b88f, False, 16)
			a.SetText(ad)
			d = self.__MobileYazi(L, 324, y + 26 + i * 22, 0xfff1e6c0, True, 16)
			self.mobileStat.append(d)
		## kostum sekmesi yuvalari: eski ayri Kostum penceresiyle ayni olaylar
		wco = self.GetChild2("MobileCostumeSlot")
		self.wndCostumeSlot = wco
		if wco:
			wco.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			wco.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			wco.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
			wco.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
			wco.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			wco.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		self.__MobileSolSekme("ek")
		L.Hide()

	def __MobileKutu(self, parent, x, y, w, h):
		for (c, fill) in ((0x80000000, True), (0xff3d342a, False)):
			b = ui.Bar() if fill else ui.Box()
			b.SetParent(parent)
			b.AddFlag("not_pick")
			b.SetColor(c)
			b.SetPosition(x, y)
			b.SetSize(w, h)
			b.Show()
			self.mobileKeep = getattr(self, "mobileKeep", []) + [b]

	def __MobileYazi(self, parent, x, y, color, right, size):
		t = ui.TextLine()
		t.SetParent(parent)
		t.AddFlag("not_pick")
		t.SetFontName("Tahoma:%d" % size)
		t.SetOutline()
		if right:
			t.SetHorizontalAlignRight()
		t.SetPackedFontColor(color)
		t.SetPosition(x, y)
		t.Show()
		self.mobileKeep = getattr(self, "mobileKeep", []) + [t]
		return t

	def __MobileSolSekme(self, key):
		self.mobileSolSekme = key
		ek = key == "ek"
		for n in ("Equipment_Base", "EquipmentSlot", "MallButton", "RingButton"):
			w = self.GetChild2(n)
			if w:
				if ek:
					w.Show()
				else:
					w.Hide()
		for n in ("MobileCostumeBase", "MobileCostumeSlot"):
			w = self.GetChild2(n)
			if w:
				if ek:
					w.Hide()
				else:
					w.Show()
		for n in ("CostumeButton", "Equipment_Tab_01", "Equipment_Tab_02"):	# kostum artik sekme; ekipman sayfa sekmeleri kullanilmaz
			w = self.GetChild2(n)
			if w:
				w.Hide()
		for (k, b) in getattr(self, "mobileSekmeler", {}).items():
			on = k == key
			b.SetUpVisual(self.MOBILE_TAB + (on and "tab_on.png" or "tab_up.png"))
			b.SetOverVisual(self.MOBILE_TAB + (on and "tab_on.png" or "tab_over.png"))
			b.SetDownVisual(self.MOBILE_TAB + "tab_on.png")
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(b.hWnd, 160 / 217.0, 27 / 54.0)
		if not ek:
			self.__MobileKostumTazele()

	def __MobileKostumTazele(self):
		wco = getattr(self, "wndCostumeSlot", None)
		if not wco:
			return
		try:
			for i in xrange(item.COSTUME_SLOT_COUNT):
				n = item.COSTUME_SLOT_START + i
				wco.SetItemSlot(n, player.GetItemIndex(n), 0)
			for a in ("EQUIPMENT_RING1", "EQUIPMENT_RING2"):
				n = getattr(item, a, None)
				if n is not None:
					wco.SetItemSlot(n, player.GetItemIndex(n), 0)
			wco.RefreshSlot()
		except:
			pass

	def __MobileKarakterBilgi(self):
		if not getattr(self, "mobileGenis", False) or not getattr(self, "mobileStat", None):
			return
		def st(n):
			c = getattr(player, n, None)
			try:
				return int(player.GetStatus(c)) if c is not None else 0
			except:
				return 0
		def nk(v):
			s = str(abs(int(v)))
			o = ""
			while len(s) > 3:
				o = "." + s[-3:] + o
				s = s[:-3]
			return s + o
		## saldiri: karakter penceresiyle AYNI (uicharacter __GetTotalAtkText: ATT_MIN/MAX + ATT_BONUS + ATTACKER_BONUS)
		ek = st("ATT_BONUS") + st("ATTACKER_BONUS")
		amin = st("ATT_MIN") + ek
		amax = st("ATT_MAX") + ek
		atk = nk(amin) if amin == amax else "%s - %s" % (nk(amin), nk(amax))
		dfn = st("DEF_GRADE")
		if constInfo.ADD_DEF_BONUS_ENABLE:
			dfn += st("DEF_BONUS")
		val = (str(st("LEVEL")), atk, nk(dfn), nk(st("MAX_HP")), nk(st("MAX_SP")), str(st("MOVING_SPEED")))
		for (t, v) in zip(self.mobileStat, val):
			t.SetText(v)

	def __MobileBaslikGenislik(self, w):
		tb = self.GetChild2("TitleBar")
		imgs = getattr(tb, "mobileImgs", None) if tb else None
		if not imgs:
			if tb:
				tb.SetWidth(w)
			return
		h = tb.GetHeight()
		bw = int(round(ui.TitleBar.BLOCK_WIDTH * 1.6))
		imgs[1].SetRenderingRect(0.0, 0.0, float(w - 2 * bw) / ui.TitleBar.BLOCK_WIDTH, 0.0)
		tb.SetSize(w, h)
		btn = getattr(tb, "btnClose", None)
		if btn:
			btn.SetPosition(w - btn.GetWidth(), (h - btn.GetHeight()) / 2)
			hit = getattr(tb, "hitClose", None)
			if hit:
				hit.Fit(56)

	def __MobileGenislik(self, genis):
		L = getattr(self, "mobileLeft", None)
		if not L:
			return
		genis = bool(genis)
		if genis == self.mobileGenis and self.mobileGenisKuruldu:
			return
		eski = self.mobileGenis if self.mobileGenisKuruldu else False
		self.mobileGenisKuruldu = True
		board = self.GetChild2("board")
		LW = self.MOBILE_LW
		dx = genis and LW or 0
		W = self.mobileIW + dx
		oldW = self.mobileIW + (eski and LW or 0)
		(x, y) = self.GetLocalPosition()
		self.SetSize(W, self.GetHeight())
		self.SetPosition(x + oldW - W, y)		# sag kenar sabit
		board.SetSize(W, board.GetHeight())
		for (w, (px, py)) in self.mobileSag:
			w.SetPosition(px + dx, py)
		self.__MobileBaslikGenislik(W - 15)
		eb = self.GetChild2("MobileEquipButton")
		if eb:
			eb.SetPosition(W - 15 + 8 - 43 - 6 - eb.GetWidth(), 9)
			eb.SetText(genis and "\xab Ekipman" or "Ekipman \xbb")
			if eb.ButtonText:
				eb.ButtonText.SetFontName("Tahoma:16")
				eb.ButtonText.SetPosition(eb.GetWidth() / 2, eb.GetHeight() / 2 - 2)
		self.mobileGenis = genis
		if genis:
			L.Show()
			self.__MobileSolSekme(self.mobileSolSekme)
			self.__MobileKarakterBilgi()
		else:
			L.Hide()
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()
		self.__MobileArrangeStorage()

	def __MobileCostumeBesideMall(self):
		## KULLANICI (2026-09-27): "kostum dugmesini ekipman penceresindeki depo dugmesinin (MallButton) yanina al,
		## ikisini de buyut" -> ikisi 1.5x, depo sag-altta yerinde (taban icinde kalir), kostum hemen solunda ayni hizada
		mall = self.GetChild2("MallButton")
		cos = self.costumeButton
		if not mall or not cos:
			return
		if hasattr(wndMgr, "SetButtonScale"):
			## KULLANICI: "hafif asagi indir, biraz daha buyut" -> eski gorselin 1.75 kati. "pixel pixel, net degil":
			## eski taskbar gorselleri ~20 px -> HD 96x96 kare (kapatma dugmesiyle ayni stil, mobile/ui/eqbtn/)
			for (b, name) in ((mall, "depo"), (cos, "costume")):
				target = b.GetWidth() * 1.75
				try:
					b.SetUpVisual("mobile/ui/eqbtn/%s.png" % name)
					b.SetOverVisual("mobile/ui/eqbtn/%s_over.png" % name)
					b.SetDownVisual("mobile/ui/eqbtn/%s_down.png" % name)
					k = target / 128.0	# KULLANICI (2026-09-27): kendi cizdirdigi HD butonlar (Desktop/yeni buton) 128x128
				except:
					k = 1.75
				wndMgr.SetButtonScale(b.hWnd, k, k)
		base = self.GetChild2("Equipment_Base")
		(mx, my) = mall.GetLocalPosition()
		if base:
			(bx, by) = base.GetLocalPosition()
			# taban boyutu yerlesimdeki EQ_SCALE (2.1) x equipment_base.sub 156x188 (ExpandedImage GetWidth olceksiz olabilir)
			mx = min(mx, bx + int(round(156 * 1.7)) - mall.GetWidth() - 4)
			my = by + int(round(188 * 1.7)) - mall.GetHeight() - 3	# tabanin alt kenarina yakin (TEK PENCERE: 1.7)
		mall.SetPosition(mx, my)
		cos.SetPosition(mx - cos.GetWidth() - 6, my + (mall.GetHeight() - cos.GetHeight()) / 2)

	def __MobileToggleEquip(self):
		if getattr(self, "mobileLeft", None):
			try:
				self.__MobileGenislik(not getattr(self, "mobileGenis", False))
			except:
				import dbg, traceback
				dbg.TraceError("TEK PENCERE ENVANTER katla: " + traceback.format_exc())
			return
		root = getattr(self, "mobileEquipRoot", None)
		if not root:
			return
		if root.IsShow():
			root.Hide()
			self.__MobileArrangeStorage()
			return
		(ix, iy) = self.GetGlobalPosition()
		root.SetPosition(ix, iy + self.GetHeight() - root.GetHeight())
		root.Show()
		root.SetTop()
		self.__MobileArrangeStorage()

	def __MobileArrangeStorage(self, w = None):
		## Yukseltme envanteri envanterin SOLUNA: ekipman kapaliysa envanter kutusunun hemen solu (bos ekipman alani),
		## ekipman acikssa kokun solu (kok olcekli pencere: gorsel genislik = GetWidth * olcek; bkz. uiexchange.py)
		if w is None:
			w = self.interface and getattr(self.interface, "wndSpecialStorage", None)
		if not w or not w.IsShow():
			return
		try:
			sc = wndMgr.GetUIScale(w.hWnd)
		except:
			sc = 1.0
		(ix, iy) = self.GetGlobalPosition()
		root = getattr(self, "mobileEquipRoot", None)
		left = ix
		if not (root and root.IsShow()):
			board = self.GetChild2("board")
			if board:
				left = ix + board.GetLocalPosition()[0]
		w.SetPosition(max(4, left - int(w.GetWidth() * sc) - 8), max(4, iy))

	def __MobileToggleStorage(self):
		if not self.interface:
			return
		try:
			self.interface.ToggleSpecialStorageWindow()
			w = getattr(self.interface, "wndSpecialStorage", None)
			if w and w.IsShow():
				self.__MobileArrangeStorage(w)
				w.SetTop()
		except:
			import dbg, traceback
			dbg.TraceError("MOBIL yukseltme envanteri: " + traceback.format_exc())

	def Hide(self):
		self.__MobileDeselect()
		if getattr(self, "mobileEquipRoot", None):
			self.mobileEquipRoot.Hide()	# MOBIL: ekipman koku da kapanir
		# KULLANICI (2026-09-14): envanter kapaninca yukseltme envanteri de kapanir
		try:
			w = self.interface and getattr(self.interface, "wndSpecialStorage", None)
			if w and w.IsShow():
				w.Close()
		except:
			pass
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()			# �κ��丮 â�� ���� �� �ڽ����� ���� �־��°�?
			self.wndCostume.Close()
  
		if self.dlgPickMoney:
			self.dlgPickMoney.Close()
		
		wndMgr.Hide(self.hWnd)
		
	
	def Close(self):
		self.Hide()

	def SetInventoryPage(self, page):
		self.__MobileDeselect()
		self.inventoryTab[self.inventoryPageIndex].SetUp()
		self.inventoryPageIndex = page
		self.inventoryTab[self.inventoryPageIndex].Down() 
		self.RefreshBagSlotWindow()

	def SetEquipmentPage(self, page):
		self.equipmentPageIndex = page
		self.equipmentTab[1-page].SetUp()
		self.RefreshEquipSlotWindow()

	def ClickMallButton(self):
		print "click_mall_button"
		net.SendChatPacket("/click_mall")
		
	def ClickMallButton(self):
		print "click_safebox_button"
		net.SendChatPacket("/click_safebox")

	def __MobileArrangeCostume(self):
		## KULLANICI (2026-09-24): kostum penceresi ilk acilista envanterin ALTINDA cikiyordu (pack yerlesimi ekran
		## sag-alt). Simdi her acilista ekipman penceresinin hemen SOLUNA, alt kenari onunla hizali konur; ekipman
		## kapaliysa envanter kutusunun soluna; Yukseltme envanteri acikssa onun da soluna (ust uste binmesin).
		w = self.wndCostume
		if not w or not w.IsShow():
			return
		try:
			sc = wndMgr.GetUIScale(w.hWnd)
		except:
			sc = 1.0
		(ix, iy) = self.GetGlobalPosition()
		root = getattr(self, "mobileEquipRoot", None)
		if root and root.IsShow():
			(left, top) = root.GetGlobalPosition()
			bottom = top + root.GetHeight()
		else:
			left = ix
			board = self.GetChild2("board")
			if board:
				left = ix + board.GetLocalPosition()[0]
			bottom = iy + self.GetHeight()
		st = self.interface and getattr(self.interface, "wndSpecialStorage", None)
		if st and st.IsShow():
			left = min(left, st.GetGlobalPosition()[0])
		w.SetPosition(max(4, left - int(w.GetWidth() * sc) - 8), max(4, bottom - int(w.GetHeight() * sc)))
		w.SetTop()

	def ClickCostumeButton(self):
		print "Click Costume Button"
		if self.wndCostume:
			if self.wndCostume.IsShow(): 
				self.wndCostume.Hide()
			else:
				self.wndCostume.Show()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.Show()
		self.__MobileArrangeCostume()	# MOBIL: ekipmanin yanina

	def ClickRingButton(self):
		print "Click Costume Button"
		if self.wndRing:
			if self.wndRing.IsShow(): 
				self.wndRing.Hide()
			else:
				self.wndRing.Show()
		else:
			self.wndRing = RingWindow(self)
			self.wndRing.Show()

	def OpenPickMoneyDialog(self):

		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():

				if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

			mouseModule.mouseController.DeattachObject()

		else:
			curMoney = player.GetElk()

			if curMoney <= 0:
				return

			self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
			self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
			self.dlgPickMoney.Open(curMoney)
			self.dlgPickMoney.SetMax(7) # �κ��丮 990000 ���� ���� ����

	def OnPickMoney(self, money):
		mouseModule.mouseController.AttachMoney(self, player.SLOT_TYPE_INVENTORY, money)

	def OnPickItem(self, count):
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop.IsBuildingShop() and uiofflineshop.IsSaleSlot(player.INVENTORY, itemSlotIndex):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
		itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
		selectedItemVNum = player.GetItemIndex(itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		return self.inventoryPageIndex*INVENTORY_PAGE_SIZE + local

	def RefreshBagSlotWindow(self):
		try:
			import uitoplusat
			uitoplusat.Yenile(self)	# toplu satis isaretleri (sayfa / icerik degisti)
		except:
			pass
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot
		
		for i in xrange(INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
			## 6x8x4 = 192 yuva (INVENTORY_MAX_NUM 192): son sayfa da tam 48
			self.wndItem.EnableSlot(i)
			
			itemCount = getItemCount(slotNumber)
			# itemCount == 0�̸� ������ ����.
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0
				
			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)
			
			## �ڵ����� (HP: #72723 ~ #72726, SP: #72727 ~ #72730) Ư��ó�� - �������ε��� ���Կ� Ȱ��ȭ/��Ȱ��ȭ ǥ�ø� ���� �۾��� - [hyo]
			if constInfo.IS_AUTO_POTION(itemVnum):
				# metinSocket - [0] : Ȱ��ȭ ����, [1] : ����� ��, [2] : �ִ� �뷮
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]	
				
				if slotNumber >= INVENTORY_PAGE_SIZE*self.inventoryPageIndex:
					slotNumber -= INVENTORY_PAGE_SIZE*self.inventoryPageIndex
					
				isActivated = 0 != metinSocket[0]
				
				if isActivated:
					self.wndItem.ActivateSlot(slotNumber)
					potionType = 0;
					if constInfo.IS_AUTO_POTION_HP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_HP
					elif constInfo.IS_AUTO_POTION_SP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_SP						
					
					usedAmount = int(metinSocket[1])
					totalAmount = int(metinSocket[2])					
					player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))
					
				else:
					self.wndItem.DeactivateSlot(slotNumber)			
					
			if constInfo.IS_UNLIMITED_ITEM(itemVnum):
				# metinSocket - [0] : Ȱ��ȭ ����, [1] : ����� ��, [2] : �ִ� �뷮
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]	
				
				if slotNumber >= INVENTORY_PAGE_SIZE*self.inventoryPageIndex:
					slotNumber -= INVENTORY_PAGE_SIZE*self.inventoryPageIndex
					
				isActivated = 0 != metinSocket[0]
				
				if isActivated:
					self.wndItem.ActivateSlot(slotNumber)
				else:
					self.wndItem.DeactivateSlot(slotNumber)	
					
		self.wndItem.RefreshSlot()

	def RefreshEquipSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndEquip.SetItemSlot
		for i in xrange(player.EQUIPMENT_PAGE_COUNT):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)

		if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			for i in xrange(player.NEW_EQUIPMENT_SLOT_COUNT):
				slotNumber = player.NEW_EQUIPMENT_SLOT_START + i
				itemCount = getItemCount(slotNumber)
				if itemCount <= 1:
					itemCount = 0
				setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
				print "ENABLE_NEW_EQUIPMENT_SYSTEM", slotNumber, itemCount, getItemVNum(slotNumber)
				


		self.wndEquip.RefreshSlot()
		self.__MobileKostumTazele()	# TEK PENCERE ENVANTER: Kostum sekmesi
		
		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

		if self.wndRing:
			self.wndRing.RefreshEquipSlotWindow()

	def OnUpdate(self):
		self.__MobileUpdatePress()	# MOBIL: dokunma/surukleme ayrimi
		self.__MobileSyncChestButton()
		if getattr(self, "mobileSelSlot", -1) >= 0 and self.tooltipItem and not self.tooltipItem.IsShow():
			self.__MobileDeselect()	# KULLANICI 2026-09-15: ipucu kapandi -> secim isigi soner
		if app.NEW_PVM_ATTRIBUTE:
			if self.PvMBonusDialog:
				if self.PvMBonusDialog.IsShow():
					self.PvMBonusDialog.Update()
                    
		if app.ELDER_ATTRIBUTE_SYSTEM:
			if self.attachBonusDialog:
				if self.attachBonusDialog.IsShow():
					self.attachBonusDialog.Update()

		if app.ENABLE_COSTUME_TIME:
			if self.CostumeTimeDialog:
				if self.CostumeTimeDialog.IsShow():
					self.CostumeTimeDialog.Update()

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def RefreshStatus(self):
		money = player.GetElk()
		## KULLANICI (2026-09-27): T/M/K yerine nokta; kese + cerceve alanina sigmazsa yazi kuculur (22 -> 14)
		self.wndMoney.SetText(MobileMoneyDots(money))
		try:
			limit = self.wndMoneySlot.GetWidth() - 14 - 50	# TEK PENCERE: kese 50 px, sag pay 14
			for f in (19, 18, 16, 15, 14):
				if getattr(self, "mobileMoneyFont", 19) != f:
					self.wndMoney.SetFontName("Tahoma:%d" % f)
					self.wndMoney.SetText(MobileMoneyDots(money))
					self.mobileMoneyFont = f
				if self.wndMoney.GetTextSize()[0] + len(self.wndMoney.GetText()) <= limit:	# GetTextSize harf basi kesik (APK 6)
					break
		except:
			pass
		self.__MobileKarakterBilgi()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SellItem(self):
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop.IsBuildingShop() and uiofflineshop.IsSaleSlot(player.INVENTORY, self.sellingSlotNumber):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
		if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
				## ��ȥ���� �ȸ��� �ϴ� ��� �߰��ϸ鼭 ���� type �߰�
				net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return
			
		#net.SendItemUseToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)		
		self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return
		
		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if constInfo.IS_BONUS_CHANGER == TRUE:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if app.__ENABLE_NEW_OFFLINESHOP__:
				if uiofflineshop.IsBuildingShop() and uiofflineshop.IsSaleSlot(player.SlotTypeToInvenType(attachedSlotType),attachedSlotPos):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
					return

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				itemCount = player.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)

			

			elif app.ENABLE_SPECIAL_STORAGE and player.SLOT_TYPE_UPGRADE_INVENTORY == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendSpecialMovePacket(player.UPGRADE_INVENTORY, attachedSlotPos, selectedSlotPos, attachedCount)
				
			elif app.ENABLE_SPECIAL_STORAGE and player.SLOT_TYPE_BOOK_INVENTORY == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendSpecialMovePacket(player.BOOK_INVENTORY, attachedSlotPos, selectedSlotPos, attachedCount)
				
			elif app.ENABLE_SPECIAL_STORAGE and player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendSpecialMovePacket(player.STONE_INVENTORY, attachedSlotPos, selectedSlotPos, attachedCount)

			mouseModule.mouseController.DeattachObject()

	def IsChanger(self, itemVnum):
		changerList = [71084,71151] #Vnum bonus changer.
		if itemVnum in changerList:
			return TRUE
		
		return FALSE

	## MOBIL (kullanici 2026-09-14): dokunma = ipucu, basili tutup surukleme = tasima.
	## Pack'te basista hemen "yapisir" (AttachObject) ve ipucu gizlenirdi; mobilde
	## yapisma 10 px hareketten sonra (wndMgr.IsDragging), kisa dokunusta ipucu acik kalir.
	## Yapisik esya varsa (birakma) veya dukkan imleci (al/sat) aktifse PC yolu aninda.
	def SelectItemSlot(self, itemSlotIndex):
		if mouseModule.mouseController.isAttached() or app.GetCursor() in (app.SELL, app.BUY):
			self.__SelectItemSlotPack(itemSlotIndex)
			return
		self.mobilePressSlot = itemSlotIndex

	def __MobileUpdatePress(self):
		slot = getattr(self, "mobilePressSlot", -1)
		if slot < 0:
			return
		if wndMgr.IsDragging():
			self.mobilePressSlot = -1
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()
			self.__MobileBlockTip()	# KULLANICI 2026-09-15: surukleme sirasinda/sonrasinda ipucu acilmasin
			self.__SelectItemSlotPack(slot)
		elif not wndMgr.IsLeftButtonDown():
			self.mobilePressSlot = -1
			if self.tooltipItem and not self.tooltipItem.IsShow():
				self.OverInItem(slot)
			self.__MobileSelect(slot)
			self.__MobileSetChestSlot(slot)

	## KULLANICI (2026-09-15): PC'de CTRL + sol tik sandik icerigini, SHIFT + sol tik ayirmayi acar; mobilde
	## tus yok -> dokununca acilan ipucunun altinda "Sandik Icerigi" (sandik) ve "Ayir" (adet > 1) dugmeleri.
	def __MobileSetChestSlot(self, localSlot):
		self.mobileChestSlot = -1
		self.mobileSplitSlot = -1
		if player.IsEquipmentSlot(localSlot):
			return
		g = self.__InventoryLocalSlotPosToGlobalSlotPos(localSlot)
		vnum = player.GetItemIndex(g)
		if not vnum:
			return
		item.SelectItem(vnum)
		if getattr(app, "ENABLE_SHOW_CHEST_DROP", 0) and item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
			self.mobileChestSlot = g
		if player.GetItemCount(g) > 1:
			self.mobileSplitSlot = g

	def __MobileMakeTipButton(self, tip, text, event):
		btn = ui.Button()
		btn.SetParent(tip)	# ipucunun cocugu: ipucuyla tasinir, "disari dokunma" sayilmaz
		btn.SetUpVisual("mobile/ui/tbbtn_up.tga")
		btn.SetOverVisual("mobile/ui/tbbtn_over.tga")
		btn.SetDownVisual("mobile/ui/tbbtn_down.tga")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(btn.hWnd, 1.6, 1.6)	# envanter alti dugmelerle ayni (170x37)
		btn.SetText(text)
		if btn.ButtonText:
			btn.ButtonText.SetFontName("Tahoma:19")
			btn.ButtonText.SetFontColor(1.0, 0.93, 0.78)
			btn.ButtonText.SetVerticalAlignCenter()
			btn.ButtonText.SetHorizontalAlignCenter()
			btn.ButtonText.SetPosition(btn.GetWidth() / 2, btn.GetHeight() / 2 - 3)
		btn.SetEvent(ui.__mem_func__(event))
		btn.Hide()
		return btn

	def __MobileSyncChestButton(self):
		tip = self.tooltipItem
		if not tip:
			return
		if not getattr(self, "mobileChestButton", None) and (getattr(self, "mobileChestSlot", -1) >= 0 or getattr(self, "mobileSplitSlot", -1) >= 0):
			self.mobileChestButton = self.__MobileMakeTipButton(tip, "Sand�k ��eri�i", self.__OnMobileChestButton)
			self.mobileSplitButton = self.__MobileMakeTipButton(tip, "Ay�r", self.__OnMobileSplitButton)
		chestBtn = getattr(self, "mobileChestButton", None)
		if not chestBtn:
			return
		allBtns = (chestBtn, self.mobileSplitButton)
		show = []
		if tip.IsShow() and self.IsShow():
			if self.mobileChestSlot >= 0:
				show.append(chestBtn)
			if self.mobileSplitSlot >= 0:
				show.append(self.mobileSplitButton)
		else:
			if not tip.IsShow():
				self.mobileChestSlot = -1
				self.mobileSplitSlot = -1
		for b in allBtns:
			if b not in show and b.IsShow():
				b.Hide()
		if not show:
			return
		w = tip.GetWidth()
		h = getattr(tip, "toolTipHeight", tip.GetHeight())
		try:
			sc = wndMgr.GetUIScale(tip.hWnd)
		except:
			sc = 1.0
		(tx, ty) = tip.GetGlobalPosition()
		gap = 6
		bw = show[0].GetWidth()
		bh = show[0].GetHeight()
		sideBySide = len(show) * bw + gap * (len(show) - 1) <= w
		rows = 1 if sideBySide else len(show)
		blockH = rows * bh + (rows - 1) * gap
		if ty + int((h + gap + blockH) * sc) <= wndMgr.GetScreenHeight():
			by = h + gap
		else:
			by = -blockH - gap
		if sideBySide:
			x = (w - (len(show) * bw + gap * (len(show) - 1))) / 2
			for b in show:
				b.SetPosition(x, by)
				x += bw + gap
		else:
			for b in show:
				b.SetPosition((w - bw) / 2, by)
				by += bh + gap
		for b in show:
			if not b.IsShow():
				b.Show()
				b.SetTop()

	def __MobileCloseTipButtons(self):
		for b in (getattr(self, "mobileChestButton", None), getattr(self, "mobileSplitButton", None)):
			if b:
				b.Hide()
		self.mobileChestSlot = -1
		self.mobileSplitSlot = -1
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.__MobileDeselect()

	def __OnMobileSplitButton(self):
		## PC: SHIFT + sol tik (__SelectItemSlotPack) ile birebir
		slot = getattr(self, "mobileSplitSlot", -1)
		self.__MobileCloseTipButtons()
		if slot < 0:
			return
		itemCount = player.GetItemCount(slot)
		if itemCount > 1:
			self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
			self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.__OnMobilePickSplit))	# KULLANICI: Tamam -> dogrudan bos kutuya
			self.dlgPickMoney.Open(itemCount)
			self.dlgPickMoney.itemGlobalSlotIndex = slot

	def __MobileFindEmptySlot(self, size, preferPage):
		## 6 sutun x 8 satir x 4 sayfa; esya boyu (1-3) asagi dogru ayni sayfada kalmali (sunucu IsEmptyItemGrid)
		cols = 6
		total = INVENTORY_PAGE_SIZE * INVENTORY_PAGE_COUNT
		used = [False] * total
		for i in xrange(total):
			vnum = player.GetItemIndex(i)
			if not vnum:
				continue
			item.SelectItem(vnum)
			for k in xrange(max(1, item.GetItemSize()[1])):	# GetItemSize -> (genislik, yukseklik)
				c = i + cols * k
				if c < total:
					used[c] = True
		pages = [preferPage] + [pg for pg in xrange(INVENTORY_PAGE_COUNT) if pg != preferPage]
		for pg in pages:
			base = pg * INVENTORY_PAGE_SIZE
			for local in xrange(INVENTORY_PAGE_SIZE):
				if local + cols * (size - 1) >= INVENTORY_PAGE_SIZE:
					continue
				if all([not used[base + local + cols * k] for k in xrange(size)]):
					return base + local
		return -1

	def __OnMobilePickSplit(self, count):
		slot = getattr(self.dlgPickMoney, "itemGlobalSlotIndex", -1)
		if slot < 0:
			return
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop.IsBuildingShop() and uiofflineshop.IsSaleSlot(player.INVENTORY, slot):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
		vnum = player.GetItemIndex(slot)
		have = player.GetItemCount(slot)
		if not vnum or count <= 0 or count >= have:
			return
		item.SelectItem(vnum)
		dst = self.__MobileFindEmptySlot(max(1, item.GetItemSize()[1]), slot / INVENTORY_PAGE_SIZE)
		if dst < 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Envanterde bo� yer yok.")
			return
		self.__SendMoveItemPacket(slot, dst, count)
		snd.PlaySound("sound/ui/drop.wav")

	def __OnMobileChestButton(self):
		slot = getattr(self, "mobileChestSlot", -1)
		self.__MobileCloseTipButtons()
		if slot < 0 or not player.GetItemIndex(slot):
			return
		if self.interface and self.interface.dlgChestDrop:
			if not self.interface.dlgChestDrop.IsShow():
				self.interface.dlgChestDrop.Open(slot)
				net.SendChestDropInfo(slot, player.INVENTORY)
			else:
				self.interface.dlgChestDrop.SetTop()

	def __MobileBlockTip(self, sec = 0.6):
		self.mobileTipBlockUntil = app.GetTime() + sec
		self.mobilePressSlot = -1
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.__MobileDeselect()

	def __MobileSelect(self, slot):
		## KOK NEDEN (2026-09-15): onceki surum sondururken RefreshBagSlotWindow cagiriyordu; native RefreshSlot
		## ipucuyu OverOut/OverIn ile yeniden acip dokunma akisinin ortasinda pencere yasam dongusunu bozuyordu
		## (heap bozulmasi, cokme). Simdi yalniz Activate/DeactivateSlot; otomatik iksir isigi elle geri verilir.
		self.__MobileDeselect()
		try:
			if player.IsEquipmentSlot(slot):
				wnd = self.wndEquip
			else:
				wnd = self.wndItem
			wnd.ActivateSlot(slot)	# native efekt esyanin tum hucrelerine olceklenir
			self.mobileSelSlot = slot
			self.mobileSelWnd = wnd
		except:
			pass

	def __MobileDeselect(self):
		slot = getattr(self, "mobileSelSlot", -1)
		if slot < 0:
			return
		self.mobileSelSlot = -1
		try:
			self.mobileSelWnd.DeactivateSlot(slot)
			if not player.IsEquipmentSlot(slot):
				g = self.__InventoryLocalSlotPosToGlobalSlotPos(slot)
				vnum = player.GetItemIndex(g)
				if vnum and constInfo.IS_AUTO_POTION(vnum) and 0 != player.GetItemMetinSocket(g, 0):
					self.wndItem.ActivateSlot(slot)	# aktif otomatik iksir isigi geri
		except:
			pass

	def __SelectItemSlotPack(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if constInfo.IS_BONUS_CHANGER == TRUE:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			self.__MobileBlockTip()	# KULLANICI 2026-09-15: birakma sonrasi ipucu acilmasin
			## MOBIL (kullanici 2026-09-14): esya birakilinca acik ipucu kapanir - acilan
			## pencereyle (Efsun Ekle, guclendirme vb.) ust uste binmesin.
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if self.IsChanger(attachedItemVID) and not player.IsEquipmentSlot(itemSlotIndex):
				itemVnum = player.GetItemIndex(itemSlotIndex)
				item.SelectItem(itemVnum)
				if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
					self.interface.AddToBonusChange(itemSlotIndex, attachedSlotPos)
					mouseModule.mouseController.DeattachObject()
					#self.wndItem[itemSlotIndex].SetChangerImage()
					return

			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_INVENTORY == attachedSlotType or player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType:
					self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)
			else:
				if player.SLOT_TYPE_INVENTORY == attachedSlotType:
					self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:

			curCursorNum = app.GetCursor()
			
			
			if app.ENABLE_SHOW_CHEST_DROP:
				ItemVNum = player.GetItemIndex(itemSlotIndex)
				item.SelectItem(ItemVNum)
					
				if item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
					if app.IsPressed(app.DIK_LCONTROL):
						if self.interface:
							if self.interface.dlgChestDrop:
								if not self.interface.dlgChestDrop.IsShow():
									self.interface.dlgChestDrop.Open(itemSlotIndex)
									net.SendChestDropInfo(itemSlotIndex, player.INVENTORY)
									return
			
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)
				
			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(itemSlotIndex)
				
				if itemCount > 1:
					self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgPickMoney.Open(itemCount)
					self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex
				#else:
					#selectedItemVNum = player.GetItemIndex(itemSlotIndex)
					#mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum)

			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)

				if True == item.CanAddToQuickSlotItem(itemIndex):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)

			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
				
				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):				
					self.wndItem.SetUseMode(True)
				else:					
					self.wndItem.SetUseMode(False)

				snd.PlaySound("sound/ui/pick.wav")

	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		
		
		
		if srcItemSlotPos == dstItemSlotPos:
			return
			
	         	
		##frodo_fix7
		elif srcItemVID == player.GetItemIndex(dstItemSlotPos):
			self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
			return
				
		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemSlotPos, dstItemSlotPos)
			self.wndItem.SetUseMode(False)

		elif item.IsMetin(srcItemVID):
			self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)

		elif app.ELDER_ATTRIBUTE_SYSTEM and player.GetItemIndex(srcItemSlotPos) == 71051:
			self.AttachBonusToItem(srcItemSlotPos, dstItemSlotPos)
		elif app.ELDER_ATTRIBUTE_SYSTEM and player.GetItemIndex(srcItemSlotPos) == 71052:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)
            
		elif app.NEW_PVM_ATTRIBUTE and player.GetItemIndex(srcItemSlotPos) == 78210:
			self.PvMBonusToItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)			

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)			
		elif app.ENABLE_COSTUME_TIME and player.GetItemIndex(srcItemSlotPos) >= 78300 and player.GetItemIndex(srcItemSlotPos) <= 78305:
			self.CostumeTimeToItem(srcItemSlotPos, dstItemSlotPos)
		else:
			#snd.PlaySound("sound/ui/drop.wav")

			## �̵���Ų ���� ���� ������ ��� �������� ����ؼ� ���� ��Ų�� - [levites]
			if player.IsEquipmentSlot(dstItemSlotPos):

				## ��� �ִ� �������� ����϶���
				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)

			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
				#net.SendItemMovePacket(srcItemSlotPos, dstItemSlotPos, 0)

	def __SellItem(self, itemSlotPos):
		## MOBIL (KULLANICI 2026-10-04): toplu satis kipinde dokunus esyayi SECER (tek tek satis penceresi acilmaz)
		try:
			import uitoplusat
			if uitoplusat.Dokun(self, itemSlotPos):
				return
		except:
			pass
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
		if not player.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(itemSlotPos)
			itemCount = player.GetItemCount(itemSlotPos)
			
			
			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			## ��Ƽ �÷��� �˻� ������ �߰�
			## 20140220
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = itemCount / itemPrice  ##frodo_fix53
			else:
				itemPrice = itemPrice * itemCount  ##frodo_fix53

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount
		
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def __OnClosePopupDialog(self):
		self.pop = None

	def RefineItem(self, scrollSlotPos, targetSlotPos):

		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
				
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
			return
			
		if app.ENABLE_REFINE_RENEWAL:
			constInfo.AUTO_REFINE_TYPE = 1
			constInfo.AUTO_REFINE_DATA["ITEM"][0] = scrollSlotPos
			constInfo.AUTO_REFINE_DATA["ITEM"][1] = targetSlotPos

		###########################################################
		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
		#net.SendItemUseToItemPacket(scrollSlotPos, targetSlotPos)
		return
		###########################################################

		###########################################################
		#net.SendRequestRefineInfoPacket(targetSlotPos)
		#return
		###########################################################

		result = player.CanRefine(scrollIndex, targetSlotPos)

		if player.REFINE_ALREADY_MAX_SOCKET_COUNT == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_MORE_SOCKET)

		elif player.REFINE_NEED_MORE_GOOD_SCROLL == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NEED_BETTER_SCROLL)

		elif player.REFINE_CANT_MAKE_SOCKET_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_SOCKET_DISABLE_ITEM)

		elif player.REFINE_NOT_NEXT_GRADE_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_UPGRADE_DISABLE_ITEM)

		elif player.REFINE_CANT_REFINE_METIN_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.REFINE_OK != result:
			return

		self.refineDialog.Open(scrollSlotPos, targetSlotPos)

	def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if not player.CanDetach(scrollIndex, targetSlotPos):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
			return

		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.sourcePos = scrollSlotPos
		self.questionDialog.targetPos = targetSlotPos

	def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
		if app.ENABLE_SPECIAL_STORAGE:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			if player.INVENTORY == attachedSlotType:
				metinIndex = player.GetItemIndex(metinSlotPos)
			else:
				metinIndex = player.GetItemIndex(player.STONE_INVENTORY, metinSlotPos)
		else:
			metinIndex = player.GetItemIndex(metinSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = player.CanAttachMetin(metinIndex, targetSlotPos)

		if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))

		elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))

		elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)

	if app.ELDER_ATTRIBUTE_SYSTEM:
		def AttachBonusToItem(self, sourceSlotPos, targetSlotPos):
			targetIndex = player.GetItemIndex(targetSlotPos)
			item.SelectItem(targetIndex)
			if item.GetItemType() not in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				return False
			self.attachBonusDialog.Open(sourceSlotPos, targetSlotPos)

	if app.NEW_PVM_ATTRIBUTE:
		def PvMBonusToItem(self, sourceSlotPos, targetSlotPos):
			targetIndex = player.GetItemIndex(targetSlotPos)
			item.SelectItem(targetIndex)
			if item.GetItemType() not in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				return False
			self.PvMBonusDialog.Open(sourceSlotPos, targetSlotPos)

	if app.ENABLE_COSTUME_TIME:
		def CostumeTimeToItem(self, sourceSlotPos, targetSlotPos):
			targetIndex = player.GetItemIndex(targetSlotPos)
			item.SelectItem(targetIndex)
			if item.GetItemType() == item.ITEM_TYPE_COSTUME:
				self.CostumeTimeDialog.Open(sourceSlotPos, targetSlotPos)
		
	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		## MOBIL: parmak esyadan ayrilinca ipucu KAPANMAZ (surukleme icin); ipucu disina dokununca
		## kapanir (mobile_root/uitooltip.py OnOutsideTap).

	def OverInItem(self, overSlotPos):
		## KULLANICI (2026-09-15): efsun penceresi YALNIZ tek dokunmada acilir; giyme (cift dokunma) ve
		## surukleme/birakma sonrasi native RefreshSlot ipucuyu yeniden aciyordu -> kisa sure engellenir.
		if app.GetTime() < getattr(self, "mobileTipBlockUntil", 0.0):
			return
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		self.wndItem.SetUsableItem(False)

		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_INVENTORY == attachedItemType or player.SLOT_TYPE_STONE_INVENTORY == attachedItemType:
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
	
					if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
						self.wndItem.SetUsableItem(True)
						self.wndItem.SetUseMode(True)
						return	# MOBIL (kullanici 2026-09-14): surukleme sirasinda ipucu/onizleme ACILMAZ
			else:
				if player.SLOT_TYPE_INVENTORY == attachedItemType:
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
	
					if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
						self.wndItem.SetUsableItem(True)
						return	# MOBIL (kullanici 2026-09-14): surukleme sirasinda ipucu/onizleme ACILMAZ

		## MOBIL (kullanici 2026-09-14): yapisik esya (surukleme) varken parmak baska esyanin
		## ustunden gecince ipucu/onizleme acilmaz; ipucu yalniz esyaya DOKUNUNCA acilir.
		if mouseModule.mouseController.isAttached():
			return
		self.ShowToolTip(overSlotPos)


	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		"�ٸ� �����ۿ� ����� �� �ִ� �������ΰ�?"

		if item.IsRefineScroll(srcItemVNum):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		elif app.NEW_PVM_ATTRIBUTE and player.GetItemIndex(srcSlotPos) == 78210:
			return True
		elif app.ENABLE_COSTUME_TIME and  player.GetItemIndex(srcSlotPos) >= 78300 and player.GetItemIndex(srcSlotPos) <= 78305:
			return True
		elif app.ELDER_ATTRIBUTE_SYSTEM and player.GetItemIndex(srcSlotPos) == 71051 or player.GetItemIndex(srcSlotPos) == 71052:
			return True
		else:
			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True
			
		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		"��� �����ۿ� ����� �� �ִ°�?"

		if srcSlotPos == dstSlotPos:
			return False

		##frodo_fix7
		elif item.IsRefineScroll(srcItemVNum):
			if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
				return True
		##frodo_fix7
		if srcItemVNum == player.GetItemIndex(dstSlotPos):
			if player.GetItemCount(dstSlotPos) < 200:
				return True	
				
		elif item.IsMetin(srcItemVNum):
			if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True

		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		elif app.NEW_PVM_ATTRIBUTE and player.GetItemIndex(srcSlotPos) == 78210 or player.GetItemIndex(srcSlotPos) == 78211:
			if self.__CanAddItemAttr(dstSlotPos):
				return True

		elif app.ENABLE_COSTUME_TIME and player.GetItemIndex(srcSlotPos) >= 78300 and player.GetItemIndex(srcSlotPos) <= 78305:
			item.SelectItem(player.GetItemIndex(dstSlotPos))
			if item.GetItemType() == item.ITEM_TYPE_COSTUME:
				return True
			
		elif app.ELDER_ATTRIBUTE_SYSTEM and player.GetItemIndex(srcSlotPos) == 71051 or player.GetItemIndex(srcSlotPos) == 71052:
			if self.__CanPutNewAttribute(dstSlotPos):
				return True

		else:
			useType=item.GetUseType(srcItemVNum)

			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:								
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return TRUE;
			elif "USE_PUT_INTO_BELT_SOCKET" == useType:								
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				print "USE_PUT_INTO_BELT_SOCKET", srcItemVNum, dstItemVNum

				item.SelectItem(dstItemVNum)
		
				if item.ITEM_TYPE_BELT == item.GetItemType():
					return True
			elif useType == "USE_COSTUME_ENCHANT" or useType == "USE_COSTUME_TRANSFORM":
				if not app.ENABLE_COSTUME_ATTR_SYSTEM:
					return FALSE
				
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				item.SelectItem(dstItemVNum)
				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					return TRUE
		return False

	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)
		
		if item.ITEM_TYPE_WEAPON != item.GetItemType():
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
				return True

		return False

	def __CanChangeItemAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)
		
		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):	 
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	if app.ELDER_ATTRIBUTE_SYSTEM:
		def __CanPutNewAttribute(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
			item.SelectItem(dstItemVNum)
			if item.GetItemType() not in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				return False
			return True

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
			return False
		
		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)
		
		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

	def __CanAddItemAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)
		
		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):	 
			return False
			
		attrCount = 0
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				attrCount += 1

		if attrCount<4:
			return True
								
		return False

	def NPCAC(self):
		self.interface.NPCAC()
		
	def BiyoEkran(self):
		self.interface.OpenBiyologTable()
		
	def DeleteOpen(self):
		self.interface.OpenDeleteItem()
		
	def OpenEfsun(self):
		self.interface.ToggleSwitchbotWindow()
		
	def OpenOfflineShop(self):
		if self.interface.wndShopOffline.IsShow() == FALSE or self.interface.wndShopOffline.wBoard[3].IsShow():
			self.interface.wndShopOffline.Open()
		else:
			self.interface.wndShopOffline.Close()

	def ShowToolTip(self, slotIndex):
		try:
			import uitoplusat
			if uitoplusat.IpucuEngelli():	# KULLANICI 2026-10-04: toplu satista dokunus SECER, efsun penceresi acilmaz
				return
		except:
			pass
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)
			if app.__ENABLE_NEW_OFFLINESHOP__:
				if uiofflineshop.IsBuildingShop():
					self.__AddTooltipSaleMode(slotIndex)

	if app.__ENABLE_NEW_OFFLINESHOP__:
		def __AddTooltipSaleMode(self, slot):
			if player.IsEquipmentSlot(slot):
				return

			itemIndex = player.GetItemIndex(slot)
			if itemIndex !=0:
				item.SelectItem(itemIndex)
				if item.IsAntiFlag(item.ANTIFLAG_MYSHOP) or item.IsAntiFlag(item.ANTIFLAG_GIVE):
					return
				
				self.tooltipItem.AddRightClickForSale()

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def UseItemSlot(self, slotIndex):
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop.IsBuildingShop():
				globalSlot 	= self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
				itemIndex 	= player.GetItemIndex(globalSlot)
				
				item.SelectItem(itemIndex)
				
				if not item.IsAntiFlag(item.ANTIFLAG_GIVE) and not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
					offlineshop.ShopBuilding_AddItem(player.INVENTORY, globalSlot)
				
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				
				return

		if constInfo.IS_BONUS_CHANGER:
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
				return
				
		if self.isShowDeleteItemDlg():
			self.wndItemDelete.AddItemWithoutMouse(player.INVENTORY, slotIndex)
			return

		self.__UseItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()
		self.__MobileBlockTip()	# KULLANICI 2026-09-15: giyince/kullaninca efsun penceresi acilmasin

	def __UseItem(self, slotIndex):
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop.IsBuildingShop() and uiofflineshop.IsSaleSlot(player.INVENTORY, slotIndex):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
		ItemVNum = player.GetItemIndex(slotIndex)
		## MOBIL BAYRAK (2026-10-06): 71182 Bayrak Degistirme -> bayrak penceresi (sunucu nesneyi onayda harcar)
		if ItemVNum == 71182:
			try:
				import uibayrak
				uibayrak.DegistirAc()
			except:
				import dbg, traceback
				dbg.TraceError("bayrak penceresi: " + traceback.format_exc())
			return
		item.SelectItem(ItemVNum)
		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex
		
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		else:
			self.__SendUseItemPacket(slotIndex)
			#net.SendItemUsePacket(slotIndex)	

	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()		

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
		# ���λ��� ���� �ִ� ���� ������ ��� ����
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)

	def __SendUseItemPacket(self, slotPos):
		# ���λ��� ���� �ִ� ���� ������ ��� ����
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUsePacket(slotPos)
	
	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		# ���λ��� ���� �ִ� ���� ������ ��� ����
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)
	
	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoulRefine = wndDragonSoulRefine
			
	#def OnMoveWindow(self, x, y):
		#print "Inventory Global Pos : ", self.GetGlobalPosition()
	if app.WJ_NEW_DROP_DIALOG:
		def DeleteItem(self, slotPos, invenType):
			itemIndex = player.GetItemIndex(invenType, slotPos)
			item.SelectItem(itemIndex)
			itemQuestionDialog2 = uiCommon.ItemQuestionDialog2()
			itemQuestionDialog2.SetText('%s nesnesine' % item.GetItemName())
			itemQuestionDialog2.SetText2('ne yapmak istiyorsun?')
			itemQuestionDialog2.SetIcon(itemIndex)
			itemQuestionDialog2.SetText3('Fiyat: %s' % localeInfo.NumberToMoneyString(item.GetISellItemPrice() * player.GetItemCount(invenType, slotPos)))
			itemQuestionDialog2.SetDeleteAcceptEvent(lambda arg = 0: self.__AnswerDeleteItem(arg))
			itemQuestionDialog2.SetSellAcceptEvent(lambda arg = 1: self.__AnswerDeleteItem(arg))
			itemQuestionDialog2.SetCancelEvent(lambda arg = 2: self.__AnswerDeleteItem(arg))
			itemQuestionDialog2.Open()
			itemQuestionDialog2.slotPos = slotPos
			itemQuestionDialog2.invenType = invenType
			self.itemQuestionDialog2 = itemQuestionDialog2
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		def __AnswerDeleteItem(self, answer):
			if not self.itemQuestionDialog2:
				return
			else:
				if answer == 0:
					net.SendItemDeletePacket(self.itemQuestionDialog2.slotPos, self.itemQuestionDialog2.invenType)
					snd.PlaySound('sound/ui/drop.wav')
				elif answer == 1:
					if item.IsAntiFlag(item.ANTIFLAG_SELL):
						popup = uiCommon.PopupDialog()
						popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
						popup.SetAcceptEvent(self.__OnClosePopupDialog)
						popup.Open()
						self.popup = popup
						return
					net.SendItemSellPacket(self.itemQuestionDialog2.slotPos, self.itemQuestionDialog2.invenType)
					snd.PlaySound('sound/ui/money.wav')
				self.itemQuestionDialog2.Close()
				self.itemQuestionDialog2 = None
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
				return
				
	if app.ENABLE_CUBE_RENEWAL:
		def SetCubeRenewalDlg(self, wndCubeRenewal):
			self.wndCubeRenewal = wndCubeRenewal
		
		def isShowCubeRenewalDlg(self):
			if self.wndCubeRenewal:
				if self.wndCubeRenewal.IsShow():
					return 1
					
			return 0
				
	if app.ENABLE_ITEM_DELETE_SYSTEM:
		def SetDeleteItemDlg(self, wndItemDelete):
			self.wndItemDelete = wndItemDelete
			
		def isShowDeleteItemDlg(self):
			if self.wndItemDelete:
				if self.wndItemDelete.IsShow():
					return 1
					
			return 0