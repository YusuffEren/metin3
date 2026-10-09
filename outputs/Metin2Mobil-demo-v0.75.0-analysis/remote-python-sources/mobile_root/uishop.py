# MOBIL KAPLAMA (mobile_root/uishop.py): pack root/uishop.py BIREBIR kopyasi; farklar "MOBIL" yorumlu.
# KULLANICI (2026-09-14): dukkan/market/zirhci/silahci: esyaya DOKUNUNCA ikon kopyasi (yapisma) degil,
# ozellik penceresi + yaninda "Satin Al" dugmesi acilsin; basili tutup surukleme = PC yolu (envantere birak).
import net
import player
import item
import snd
import shop
import net
import wndMgr
import app
import chat

import ui
import uiCommon
import mouseModule
import localeInfo
import constInfo
import uiToolTip	# MOBIL: ipucu dukkanin yaninda acilsin (MOBILE_SHOP_WINDOW)

###################################################################################################
## Shop
class ShopDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		uiToolTip.MOBILE_SHOP_WINDOW = self	# MOBIL
		self.mobilePressSlot = -1	# MOBIL: basilan (henuz yapismamis) kutu
		self.mobileBuySlot = -1		# MOBIL: "Satin Al" dugmesinin hedefi (yerel kutu no)
		self.mobileBuyButton = None
		self.tooltipItem = 0
		self.xShopStart = 0
		self.yShopStart = 0
		self.questionDialog = None
		self.popup = None
		self.itemBuyQuestionDialog = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def __GetRealIndex(self, i):
		return self.tabIdx * shop.SHOP_SLOT_COUNT + i
	
	def Refresh(self):
		getItemID=shop.GetItemID
		getItemCount=shop.GetItemCount
		setItemID=self.itemSlotWindow.SetItemSlot
		for i in xrange(shop.SHOP_SLOT_COUNT):
			idx = self.__GetRealIndex(i)
			itemCount = getItemCount(idx)
			if itemCount <= 1:
				itemCount = 0
			setItemID(i, getItemID(idx), itemCount)

		wndMgr.RefreshSlot(self.itemSlotWindow.GetWindowHandle())

	def SetItemData(self, pos, itemID, itemCount, itemPrice):
		shop.SetItemData(pos, itemID, itemCount, itemPrice)

	def LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/shopdialog.py")
		except:
			import exception
			exception.Abort("ShopDialog.LoadDialog.LoadObject")

		smallTab1 = None
		smallTab2 = None
		smallTab3 = None
		middleTab1 = None
		middleTab2 = None
		
		try:
			GetObject = self.GetChild
			self.itemSlotWindow = GetObject("ItemSlot")
			self.btnBuy = GetObject("BuyButton")
			self.btnSell = GetObject("SellButton")
			self.btnClose = GetObject("CloseButton")
			self.titleBar = GetObject("TitleBar")
			middleTab1 = GetObject("MiddleTab1")
			middleTab2 = GetObject("MiddleTab2")
			smallTab1 = GetObject("SmallTab1")
			smallTab2 = GetObject("SmallTab2")
			smallTab3 = GetObject("SmallTab3")
		except:
			import exception
			exception.Abort("ShopDialog.LoadDialog.BindObject")

		self.itemSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.itemSlotWindow.SAFE_SetButtonEvent("LEFT", "EMPTY", self.SelectEmptySlot)
		self.itemSlotWindow.SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
		self.itemSlotWindow.SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)

		self.itemSlotWindow.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlotWindow.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.btnBuy.SetToggleUpEvent(ui.__mem_func__(self.CancelShopping))
		self.btnBuy.SetToggleDownEvent(ui.__mem_func__(self.OnBuy))

		self.btnSell.SetToggleUpEvent(ui.__mem_func__(self.CancelShopping))
		self.btnSell.SetToggleDownEvent(ui.__mem_func__(self.OnSell))

		self.btnClose.SetEvent(ui.__mem_func__(self.AskClosePrivateShop))

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.smallRadioButtonGroup = ui.RadioButtonGroup.Create([[smallTab1, lambda : self.OnClickTabButton(0), None], [smallTab2, lambda : self.OnClickTabButton(1), None], [smallTab3, lambda : self.OnClickTabButton(2), None]])
		self.middleRadioButtonGroup = ui.RadioButtonGroup.Create([[middleTab1, lambda : self.OnClickTabButton(0), None], [middleTab2, lambda : self.OnClickTabButton(1), None]])

		self.__HideMiddleTabs()
		self.__HideSmallTabs()
		
		self.tabIdx = 0
		self.coinType = shop.SHOP_COIN_TYPE_GOLD
		
		self.Refresh()
	
	def __ShowBuySellButton(self):
		self.btnBuy.Show()
		self.btnSell.Show()
		
	def __ShowMiddleTabs(self):
		self.middleRadioButtonGroup.Show()
	
	def __ShowSmallTabs(self):
		self.smallRadioButtonGroup.Show()
	
	def __HideBuySellButton(self):
		self.btnBuy.Hide()
		self.btnSell.Hide()
	
	def __HideMiddleTabs(self):
		self.middleRadioButtonGroup.Hide()
	
	def __HideSmallTabs(self):
		self.smallRadioButtonGroup.Hide()
		
	def __SetTabNames(self):
		if shop.GetTabCount() == 2:
			self.middleRadioButtonGroup.SetText(0, shop.GetTabName(0))
			self.middleRadioButtonGroup.SetText(1, shop.GetTabName(1))
		elif shop.GetTabCount() == 3:
			self.smallRadioButtonGroup.SetText(0, shop.GetTabName(0))
			self.smallRadioButtonGroup.SetText(1, shop.GetTabName(1))
			self.smallRadioButtonGroup.SetText(2, shop.GetTabName(2))
	 
 
	def Destroy(self):
		try:
			import uitoplusat
			uitoplusat.Yoket()
		except:
			pass
		self.Close()
		self.ClearDictionary()

		self.mobileBuyButton = None	# MOBIL
		self.tooltipItem = 0
		self.itemSlotWindow = 0
		self.btnBuy = 0
		self.btnSell = 0
		self.btnClose = 0
		self.titleBar = 0
		self.questionDialog = None
		self.popup = None

	def Open(self, vid):

		isPrivateShop = False
		isMainPlayerPrivateShop = False

		import chr
		if chr.IsNPC(vid):
			isPrivateShop = False
		else:
			isPrivateShop = True

		if player.IsMainCharacterIndex(vid):

			isMainPlayerPrivateShop = True

			self.btnBuy.Hide()
			self.btnSell.Hide()
			self.btnClose.Show()

		else:

			isMainPlayerPrivateShop = False

			self.btnBuy.Show()
			self.btnSell.Show()
			self.btnClose.Hide()

		shop.Open(isPrivateShop, isMainPlayerPrivateShop)

		self.tabIdx = 0

		if isPrivateShop:
			self.__HideMiddleTabs()
			self.__HideSmallTabs()
		else:
			if shop.GetTabCount() == 1:
				self.__ShowBuySellButton()
				self.__HideMiddleTabs()
				self.__HideSmallTabs()
			elif shop.GetTabCount() == 2:
				self.__HideBuySellButton()
				self.__ShowMiddleTabs()
				self.__HideSmallTabs()
				self.__SetTabNames()
				self.middleRadioButtonGroup.OnClick(0)
			elif shop.GetTabCount() == 3:
				self.__HideBuySellButton()
				self.__HideMiddleTabs()
				self.__ShowSmallTabs()
				self.__SetTabNames()
				self.middleRadioButtonGroup.OnClick(1)

		self.Refresh()
		self.SetTop()
		
		self.Show()
		self.__MobileCenterShop()

		(self.xShopStart, self.yShopStart, z) = player.GetMainCharacterPosition()

	def __MobileCenterShop(self):
		## KULLANICI (2026-09-27): "market/silahci/zirhci tam solda cikiyor, kotu - biraz ortaya getir":
		## ekranin solu ile envanter kutusu arasindaki boslugun ORTASINA (dikey konum yerlesimdeki gibi ustte;
		## efsun penceresi dukkanin saginda ust hizali acilir, envantere kadar sigar).
		try:
			sc = wndMgr.GetUIScale(self.hWnd)
		except:
			sc = 1.0
		limit = wndMgr.GetScreenWidth()
		inv = uiToolTip.MOBILE_INVENTORY_WINDOW
		if inv:
			try:
				board = inv.GetChild2("board")
				if board:
					limit = board.GetGlobalPosition()[0]
			except:
				pass
		w = int(self.GetWidth() * sc)
		(x0, y0) = self.GetGlobalPosition()
		self.SetPosition(max(4, (limit - w) / 2), y0)

	def Close(self):
		if self.itemBuyQuestionDialog:
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None		
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		if self.questionDialog:
			self.OnCloseQuestionDialog()
		shop.Close()
		net.SendShopEndPacket()
		self.CancelShopping()
		self.tooltipItem.HideToolTip()
		self.mobileBuySlot = -1	# MOBIL
		if self.mobileBuyButton:
			self.mobileBuyButton.Hide()
		self.Hide()

	def GetIndexFromSlotPos(self, slotPos):
		return self.tabIdx * shop.SHOP_SLOT_COUNT + slotPos
		
	def OnClickTabButton(self, idx):
		self.tabIdx = idx
		self.Refresh()
		
	def AskClosePrivateShop(self):
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(localeInfo.PRIVATE_SHOP_CLOSE_QUESTION)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnClosePrivateShop))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		questionDialog.Open()
		self.questionDialog = questionDialog

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		return True

	def OnClosePrivateShop(self):
		net.SendChatPacket("/close_shop")
		self.OnCloseQuestionDialog()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def OnBuy(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
		app.SetCursor(app.BUY)
		self.btnSell.SetUp()

	def OnSell(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_SELL_INFO)
		app.SetCursor(app.SELL)
		self.btnBuy.SetUp()
		## MOBIL (KULLANICI 2026-10-04): toplu satis - envanterde dokunulan esya SECILIR (uitoplusat)
		try:
			import uitoplusat
			uitoplusat.Ac()
		except:
			pass

	def CancelShopping(self):
		self.btnBuy.SetUp()
		self.btnSell.SetUp()
		app.SetCursor(app.NORMAL)
		try:
			import uitoplusat
			uitoplusat.Kapat()
		except:
			pass

	def __OnClosePopupDialog(self):
		self.pop = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	## ¿ëÈ¥¼® ÆÈ¸®´Â ±â´É Ãß°¡.
	def SellAttachedItem(self):

		if shop.IsPrivateShop():
			mouseModule.mouseController.DeattachObject()
			return

		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		attachedCount = mouseModule.mouseController.GetAttachedItemCount()
		if localeInfo.IsBRAZIL() == 0:
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
		
		if app.ENABLE_SPECIAL_STORAGE:
			if player.SLOT_TYPE_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_UPGRADE_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_BOOK_INVENTORY == attachedSlotType or\
				player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType:
	
				item.SelectItem(attachedItemIndex)
	
				if item.IsAntiFlag(item.ANTIFLAG_SELL):
					popup = uiCommon.PopupDialog()
					popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
					popup.SetAcceptEvent(self.__OnClosePopupDialog)
					popup.Open()
					self.popup = popup
					return
	
				itemtype = player.SlotTypeToInvenType(attachedSlotType)
	
				if player.IsValuableItem(itemtype, attachedSlotPos):
	
					itemPrice = item.GetISellItemPrice()
	
					if item.Is1GoldItem():
						itemPrice = attachedCount / itemPrice
					else:
						itemPrice = itemPrice * max(1, attachedCount)
	
					itemName = item.GetItemName()
	
					questionDialog = uiCommon.QuestionDialog()
					questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, attachedCount, itemPrice))
	
					questionDialog.SetAcceptEvent(lambda arg1=attachedSlotPos, arg2=attachedCount, arg3 = itemtype: self.OnSellItem(arg1, arg2, arg3))
					questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
					questionDialog.Open()
					self.questionDialog = questionDialog
	
					#constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
	
				else:
					self.OnSellItem(attachedSlotPos, attachedCount, itemtype)
			else:
				snd.PlaySound("sound/ui/loginfail.wav")
		else:
			if player.SLOT_TYPE_INVENTORY == attachedSlotType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
	
				item.SelectItem(attachedItemIndex)
	
				if item.IsAntiFlag(item.ANTIFLAG_SELL):
					popup = uiCommon.PopupDialog()
					popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
					popup.SetAcceptEvent(self.__OnClosePopupDialog)
					popup.Open()
					self.popup = popup
					return
	
				itemtype = player.INVENTORY
	
				if player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
					itemtype = player.DRAGON_SOUL_INVENTORY

				if player.IsValuableItem(itemtype, attachedSlotPos):
	
					itemPrice = item.GetISellItemPrice()
	
					if item.Is1GoldItem():
						itemPrice = attachedCount / itemPrice
					else:
						itemPrice = itemPrice * max(1, attachedCount)
	
					itemName = item.GetItemName()
	
					questionDialog = uiCommon.QuestionDialog()
					questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, attachedCount, itemPrice))
	
					questionDialog.SetAcceptEvent(lambda arg1=attachedSlotPos, arg2=attachedCount, arg3 = itemtype: self.OnSellItem(arg1, arg2, arg3))
					questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
					questionDialog.Open()
					self.questionDialog = questionDialog
	
					#constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
	
				else:
					self.OnSellItem(attachedSlotPos, attachedCount, itemtype)
			else:
				snd.PlaySound("sound/ui/loginfail.wav")
		mouseModule.mouseController.DeattachObject()

	def OnSellItem(self, slotPos, count, itemtype):
		net.SendShopSellPacketNew(slotPos, count, itemtype)
		snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return
			
		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SelectEmptySlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			self.SellAttachedItem()

	def UnselectItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
		if shop.IsPrivateShop():
			self.AskBuyItem(selectedSlotPos)
		else:
			net.SendShopBuyPacket(self.__GetRealIndex(selectedSlotPos))

	## MOBIL (kullanici 2026-09-14): dokunma = ipucu + "Satin Al"; basili tutup surukleme = PC yolu
	## (yapistir, envantere birakinca satin alma sorusu). Yapisik esya (satis) / al-sat imleci: PC yolu.
	def SelectItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
		if mouseModule.mouseController.isAttached() or app.GetCursor() in (app.SELL, app.BUY) or shop.IsMainPlayerPrivateShop():
			self.__SelectItemSlotPack(selectedSlotPos)
			return
		self.mobilePressSlot = selectedSlotPos

	def __MobileUpdatePress(self):
		slot = self.mobilePressSlot
		if slot < 0:
			return
		if wndMgr.IsDragging():
			self.mobilePressSlot = -1
			self.mobileBuySlot = -1
			if 0 != self.tooltipItem:
				self.tooltipItem.HideToolTip()
			self.__SelectItemSlotPack(slot)
		elif not wndMgr.IsLeftButtonDown():
			self.mobilePressSlot = -1
			self.mobileBuySlot = slot
			self.OverInItem(slot)

	def __MobileCreateBuyButton(self):
		if self.mobileBuyButton or 0 == self.tooltipItem:
			return
		btn = ui.Button()
		btn.SetParent(self.tooltipItem)	# ipucunun cocugu: ipucuyla tasinir, "disari dokunma" sayilmaz
		btn.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
		btn.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
		btn.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
		## KULLANICI (2026-09-15): ipucunun ALTINDA ortali, 1.5x buyuk, yazisi sicak sari + dis cizgi
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(btn.hWnd, 1.5, 1.5)
		btn.SetText("Sat\xfdn Al")
		if btn.ButtonText:
			btn.ButtonText.SetFontName("Tahoma:14")	# APK v6+: GrpText olcek varyant siniri 8 -> net
			btn.ButtonText.SetOutline()
			btn.ButtonText.SetFontColor(1.0, 0.86, 0.40)
			btn.ButtonText.SetPosition(btn.GetWidth() / 2, btn.GetHeight() / 2)
		btn.SetEvent(ui.__mem_func__(self.__OnMobileBuy))
		btn.Hide()
		self.mobileBuyButton = btn

	def __MobileSyncBuyButton(self):
		btn = self.mobileBuyButton
		tip = self.tooltipItem
		if not btn or 0 == tip:
			return
		if self.mobileBuySlot >= 0 and self.IsShow() and tip.IsShow() and getattr(tip, "isShopItem", False):
			w = tip.GetWidth()
			h = tip.toolTipHeight
			try:
				sc = wndMgr.GetUIScale(tip.hWnd)
			except:
				sc = 1.0
			(tx, ty) = tip.GetGlobalPosition()
			limit = wndMgr.GetScreenWidth()
			inv = uiToolTip.MOBILE_INVENTORY_WINDOW
			if inv and inv.IsShow():
				limit = min(limit, inv.GetGlobalPosition()[0])
			# KULLANICI (2026-09-15): her zaman ipucunun ALTINDA ortali; ekrana sigmazsa ustunde
			if ty + int((h + 8 + btn.GetHeight()) * sc) <= wndMgr.GetScreenHeight():
				btn.SetPosition((w - btn.GetWidth()) / 2, h + 8)
			else:
				btn.SetPosition((w - btn.GetWidth()) / 2, -btn.GetHeight() - 8)
			if not btn.IsShow():
				btn.Show()
				btn.SetTop()
		else:
			if btn.IsShow():
				btn.Hide()
			if not (tip.IsShow() and getattr(tip, "isShopItem", False)):
				self.mobileBuySlot = -1

	def __OnMobileBuy(self):
		slot = self.mobileBuySlot
		if slot < 0:
			return
		self.mobileBuySlot = -1
		if self.mobileBuyButton:
			self.mobileBuyButton.Hide()
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
		self.AskBuyItem(slot)	# yerel kutu no (AskBuyItem icinde __GetRealIndex uygulanir)

	def __SelectItemSlotPack(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		isAttached = mouseModule.mouseController.isAttached()
		selectedSlotPos = self.__GetRealIndex(selectedSlotPos)
		if isAttached:
			self.SellAttachedItem()

		else:

			if True == shop.IsMainPlayerPrivateShop():
				return

			curCursorNum = app.GetCursor()
			if app.BUY == curCursorNum:
				self.AskBuyItem(selectedSlotPos)

			elif app.SELL == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_SELL_INFO)

			else:
				selectedItemID = shop.GetItemID(selectedSlotPos)
				itemCount = shop.GetItemCount(selectedSlotPos)

				type = player.SLOT_TYPE_SHOP
				if shop.IsPrivateShop():
					type = player.SLOT_TYPE_PRIVATE_SHOP

				mouseModule.mouseController.AttachObject(self, type, selectedSlotPos, selectedItemID, itemCount)
				mouseModule.mouseController.SetCallBack("INVENTORY", ui.__mem_func__(self.DropToInventory))
				snd.PlaySound("sound/ui/pick.wav")

	def DropToInventory(self):
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		self.AskBuyItem(attachedSlotPos)

	def AskBuyItem(self, slotPos):
		slotPos = self.__GetRealIndex(slotPos)
		
		itemIndex = shop.GetItemID(slotPos)
		itemPrice = shop.GetItemPrice(slotPos)
		if app.PRICE_TYPE:
			itemPriceType = shop.GetItemPriceType(slotPos)
		itemCount = shop.GetItemCount(slotPos)

		item.SelectItem(itemIndex)
		itemName = item.GetItemName()

		itemBuyQuestionDialog = uiCommon.QuestionDialog()
		
		if app.PRICE_TYPE:
			if itemPriceType == 0:
				itemBuyQuestionDialog.SetText(localeInfo.DO_YOU_BUY_ITEM(itemName, itemCount, localeInfo.NumberToMoneyString(itemPrice)))
			else:
				itemBuyQuestionDialog.SetText(localeInfo.DO_YOU_BUY_ITEM(itemName, itemCount, localeInfo.NumberToItemString(itemPrice, itemPriceType)))
		else:
			itemBuyQuestionDialog.SetText(localeInfo.DO_YOU_BUY_ITEM(itemName, itemCount, localeInfo.NumberToMoneyString(itemPrice)))
		
		itemBuyQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerBuyItem(arg))
		itemBuyQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerBuyItem(arg))
		itemBuyQuestionDialog.Open()
		itemBuyQuestionDialog.pos = slotPos
		self.itemBuyQuestionDialog = itemBuyQuestionDialog
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def AnswerBuyItem(self, flag):

		if flag:
			pos = self.itemBuyQuestionDialog.pos
			net.SendShopBuyPacket(pos)

		self.itemBuyQuestionDialog.Close()
		self.itemBuyQuestionDialog = None
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem
		self.__MobileCreateBuyButton()	# MOBIL

	def OverInItem(self, slotIndex):
		slotIndex = self.__GetRealIndex(slotIndex)
		if mouseModule.mouseController.isAttached():
			return

		if 0 != self.tooltipItem:
			if shop.SHOP_COIN_TYPE_GOLD == shop.GetTabCoinType(self.tabIdx):
				self.tooltipItem.SetShopItem(slotIndex)
			else: 
				self.tooltipItem.SetShopItemBySecondaryCoin(slotIndex)
	def OverOutItem(self):
		## MOBIL: parmak kutudan ayrilinca ipucu KAPANMAZ ("Satin Al" basilabilsin); ipucu disina
		## dokununca (FLAG_HIDE_ON_OUTSIDE), surukleme baslayinca veya dukkan kapaninca kapanir.
		pass

	def OnUpdate(self):
		self.__MobileUpdatePress()	# MOBIL
		self.__MobileSyncBuyButton()	# MOBIL

		USE_SHOP_LIMIT_RANGE = 1000

		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xShopStart) > USE_SHOP_LIMIT_RANGE or abs(y - self.yShopStart) > USE_SHOP_LIMIT_RANGE:
			self.Close()


class MallPageDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()

	def Open(self):
		scriptLoader = ui.PythonScriptLoader()
		scriptLoader.LoadScriptFile(self, "uiscript/mallpagedialog.py")

		self.GetChild("titlebar").SetCloseEvent(ui.__mem_func__(self.Close))
		
		(x, y)=self.GetGlobalPosition()
		x+=10
		y+=30
		
		MALL_PAGE_WIDTH = 600
		MALL_PAGE_HEIGHT = 480
		
		app.ShowWebPage(
			"http://metin2.co.kr/08_mall/game_mall/login_fail.htm", 
			(x, y, x+MALL_PAGE_WIDTH, y+MALL_PAGE_HEIGHT))

		self.Lock()
		self.Show()
		
	def Close(self):			
		app.HideWebPage()
		self.Unlock()
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
