# MOBIL KAPLAMA (mobile_root/uiminimap.py): pack root/uiminimap.py BIREBIR kopyasi; farklar "MOBIL" yorumlu.
MOBILE_MINIMAP_SHIFT = 30	# KULLANICI (2026-09-20, iPhone/Android): 12 -> 30; kapatma dugmesi ekranin yuvarlak kosesine giriyordu
## iPHONE (KULLANICI 2026-09-20): yuvarlak kose + ada yuzunden biraz daha sola ve asagi (yalniz iOS).
## iOS tespiti: veri koku iOS uygulama kabinda (/Containers/Data/Application/); sys.platform iki
## platformda da "linux2" oldugu icin ayirt edemez. Android/PC'de 0.
import os as _os
MOBILE_IOS = ("/Containers/Data/Application/" in _os.getcwd())
MOBILE_MINIMAP_IOS_EXTRA_X = 14 if MOBILE_IOS else 0
MOBILE_MINIMAP_IOS_Y = 10 if MOBILE_IOS else 0
import ui
import uiScriptLocale
import wndMgr
import player
import miniMap
import localeInfo
import net
import app
import colorInfo
import constInfo
import background
import serverInfo
import time
## MOBIL (KULLANICI 2026-09-26): mini harita artik Minimap + HP/SP yay HUD'u (uiminimaphud.py) icinde
try:
	import uiminimaphud
except:
	uiminimaphud = None
## MOBIL (KULLANICI 2026-09-26): buyuk harita + yol gosterici (uibuyukharita.py)
try:
	import uibuyukharita
except:
	uibuyukharita = None

class MapTextToolTip(ui.Window):
	def __init__(self):			
		ui.Window.__init__(self)

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetHorizontalAlignCenter()
		textLine.SetOutline()
		textLine.SetHorizontalAlignRight()
		textLine.Show()
		self.textLine = textLine

	def __del__(self):			
		ui.Window.__del__(self)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetTooltipPosition(self, PosX, PosY):
		if localeInfo.IsARABIC():
			w, h = self.textLine.GetTextSize()
			self.textLine.SetPosition(PosX - w - 5, PosY)
		else:
			self.textLine.SetPosition(PosX - 5, PosY)

	def SetTextColor(self, TextColor):
		self.textLine.SetPackedFontColor(TextColor)

	def GetTextSize(self):
		return self.textLine.GetTextSize()

class AtlasWindow(ui.ScriptWindow):

	class AtlasRenderer(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.AddFlag("not_pick")

		def OnUpdate(self):
			miniMap.UpdateAtlas()

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			fx = float(x)
			fy = float(y)
			miniMap.RenderAtlas(fx, fy)

		def HideAtlas(self):
			miniMap.HideAtlas()

		def ShowAtlas(self):
			miniMap.ShowAtlas()

	def __init__(self):
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Hide()
		self.infoGuildMark = ui.MarkBox()
		self.infoGuildMark.Hide()
		self.AtlasMainWindow = None
		self.mapName = ""
		self.board = 0

		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def SetMapName(self, mapName):
		if 949==app.GetDefaultCodePage():
			try:
				self.board.SetTitleName(localeInfo.MINIMAP_ZONE_NAME_DICT[mapName])
			except:
				pass

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/AtlasWindow.py")
		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.LoadScript")

		try:
			self.board = self.GetChild("board")

		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.BindObject")

		self.AtlasMainWindow = self.AtlasRenderer()
		self.board.SetCloseEvent(self.Hide)
		self.AtlasMainWindow.SetParent(self.board)
		self.AtlasMainWindow.SetPosition(7, 30)
		self.tooltipInfo.SetParent(self.board)
		self.infoGuildMark.SetParent(self.board)
		self.SetPosition(wndMgr.GetScreenWidth() - 136 - 256 - 10, 0)
		self.Hide()

		miniMap.RegisterAtlasWindow(self)

	def Destroy(self):
		miniMap.UnregisterAtlasWindow()
		self.ClearDictionary()
		self.AtlasMainWindow = None
		self.tooltipAtlasClose = 0
		self.tooltipInfo = None
		self.infoGuildMark = None
		self.board = None

	def OnUpdate(self):

		if not self.tooltipInfo:
			return

		if not self.infoGuildMark:
			return

		self.infoGuildMark.Hide()
		self.tooltipInfo.Hide()

		if False == self.board.IsIn():
			return

		(mouseX, mouseY) = wndMgr.GetMousePosition()
		(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)

		if False == bFind:
			return

		if "empty_guild_area" == sName:
			sName = localeInfo.GUILD_EMPTY_AREA

		if localeInfo.IsARABIC() and sName[-1].isalnum():
			self.tooltipInfo.SetText("(%s)%d, %d" % (sName, iPosX, iPosY))						
		else:
			self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))
			
		(x, y) = self.GetGlobalPosition()
		self.tooltipInfo.SetTooltipPosition(mouseX - x, mouseY - y)
		self.tooltipInfo.SetTextColor(dwTextColor)
		self.tooltipInfo.Show()
		self.tooltipInfo.SetTop()

		if 0 != dwGuildID:
			textWidth, textHeight = self.tooltipInfo.GetTextSize()
			self.infoGuildMark.SetIndex(dwGuildID)
			self.infoGuildMark.SetPosition(mouseX - x - textWidth - 18 - 5, mouseY - y)
			self.infoGuildMark.Show()

	def Hide(self):
		if self.AtlasMainWindow:
			self.AtlasMainWindow.HideAtlas()
			self.AtlasMainWindow.Hide()
		ui.ScriptWindow.Hide(self)

	def Show(self):
		if self.AtlasMainWindow:
			(bGet, iSizeX, iSizeY) = miniMap.GetAtlasSize()
			if bGet:
				self.SetSize(iSizeX + 15, iSizeY + 38)

				if localeInfo.IsARABIC():
					self.board.SetPosition(iSizeX+15, 0)

				self.board.SetSize(iSizeX + 15, iSizeY + 38)
				#self.AtlasMainWindow.SetSize(iSizeX, iSizeY)
				self.AtlasMainWindow.ShowAtlas()
				self.AtlasMainWindow.Show()
		ui.ScriptWindow.Show(self)

	def SetCenterPositionAdjust(self, x, y):
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2 + x, (wndMgr.GetScreenHeight() - self.GetHeight()) / 2 + y)

	def OnPressEscapeKey(self):
		self.Hide()
		return True

def __RegisterMiniMapColor(type, rgb):
	miniMap.RegisterColor(type, rgb[0], rgb[1], rgb[2])

class MiniMap(ui.ScriptWindow):

	CANNOT_SEE_INFO_MAP_DICT = {
		"metin2_map_monkeydungeon" : False,
		"metin2_map_monkeydungeon_02" : False,
		"metin2_map_monkeydungeon_03" : False,
		"metin2_map_devilsCatacomb" : False,
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		## MOBIL: kucuk mini harita genel UI olceginin DISINDA (kose ogesi); buyuk harita (AtlasWindow) olcekli kalir
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)

		self.__Initialize()

		miniMap.Create()
		miniMap.SetScale(2.0)

		self.AtlasWindow = AtlasWindow()
		self.AtlasWindow.LoadWindow()
		self.AtlasWindow.Hide()

		self.tooltipMiniMapOpen = MapTextToolTip()
		self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)
		self.tooltipMiniMapOpen.Show()
		self.tooltipMiniMapClose = MapTextToolTip()
		self.tooltipMiniMapClose.SetText(localeInfo.UI_CLOSE)
		self.tooltipMiniMapClose.Show()
		self.tooltipScaleUp = MapTextToolTip()
		self.tooltipScaleUp.SetText(localeInfo.MINIMAP_INC_SCALE)
		self.tooltipScaleUp.Show()
		self.tooltipScaleDown = MapTextToolTip()
		self.tooltipScaleDown.SetText(localeInfo.MINIMAP_DEC_SCALE)
		self.tooltipScaleDown.Show()
		self.tooltipAtlasOpen = MapTextToolTip()
		self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_SHOW_AREAMAP)
		self.tooltipAtlasOpen.Show()
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()
		self.VectorsF = MapTextToolTip()
		self.VectorsF.SetText("Facebook Sayfasi")
		self.VectorsF.Show()
		self.VectorsT = MapTextToolTip()
		self.VectorsT.SetText("Discord Sunucumuz")
		self.VectorsT.Show()
		self.VectorsY = MapTextToolTip()
		self.VectorsY.SetText("Instagram Sayfasi")
		self.VectorsY.Show()
		self.VectorsS = MapTextToolTip()
		self.VectorsS.SetText("Tiktok Sayfasi")
		self.VectorsS.Show()


		if miniMap.IsAtlas():
			self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_SHOW_AREAMAP)
		else:
			self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_CAN_NOT_SHOW_AREAMAP)

		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()

		self.mapName = ""

		self.isLoaded = 0
		self.canSeeInfo = True
		
		# AUTOBAN
		self.imprisonmentDuration = 0
		self.imprisonmentEndTime = 0
		self.imprisonmentEndTimeText = ""
		# END_OF_AUTOBAN

	def __del__(self):
		miniMap.Destroy()
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.positionInfo = 0
		self.observerCount = 0

		self.OpenWindow = 0
		self.CloseWindow = 0
		self.ScaleUpButton = 0
		self.ScaleDownButton = 0
		self.MiniMapHideButton = 0
		self.MiniMapShowButton = 0
		self.AtlasShowButton = 0

		self.tooltipMiniMapOpen = 0
		self.tooltipMiniMapClose = 0
		self.tooltipScaleUp = 0
		self.tooltipScaleDown = 0
		self.tooltipAtlasOpen = 0
		self.tooltipInfo = None
		self.serverInfo = None
		self.Facebook = 0
		self.Twitter = 0
		self.Youtube = 0
		self.Site = 0
		self.VectorsF = 0
		self.VectorsT = 0
		self.VectorsY = 0
		self.VectorsS = 0

	def SetMapName(self, mapName):
		self.mapName=mapName
		self.AtlasWindow.SetMapName(mapName)

		if self.CANNOT_SEE_INFO_MAP_DICT.has_key(mapName):
			self.canSeeInfo = False
			self.HideMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP_CANNOT_SEE)
		else:
			self.canSeeInfo = True
			self.ShowMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)
		## MOBIL (KULLANICI 2026-10-02): gizli haritada HUD dairesinde aciklama (orijinal: MINIMAP_CANNOT_SEE ipucu)
		hud = getattr(self, "hud", None)
		if hud:
			if self.canSeeInfo:
				hud.SetNote(None)
			else:
				hud.SetNote("kucuk")
			bm = getattr(self, "bigMap", None)
			if bm and bm.IsShow() and not self.__CanBigMap():
				bm.Close()
			
	# AUTOBAN
	def SetImprisonmentDuration(self, duration):
		self.imprisonmentDuration = duration
		self.imprisonmentEndTime = app.GetGlobalTimeStamp() + duration				
		
		self.__UpdateImprisonmentDurationText()
		
	def __UpdateImprisonmentDurationText(self):
		restTime = max(self.imprisonmentEndTime - app.GetGlobalTimeStamp(), 0)
		
		imprisonmentEndTimeText = localeInfo.SecondToDHM(restTime)
		if imprisonmentEndTimeText != self.imprisonmentEndTimeText:
			self.imprisonmentEndTimeText = imprisonmentEndTimeText
			self.serverInfo.SetText("%s: %s" % (uiScriptLocale.AUTOBAN_QUIZ_REST_TIME, self.imprisonmentEndTimeText))
	# END_OF_AUTOBAN	

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "Minimap.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/MiniMap.py")
		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.LoadScript")

		## MOBIL: mini harita sag kenardan MOBILE_MINIMAP_SHIFT px sola (kosedeki dugmeler parmakla tiklanabilsin)
		self.SetPosition(wndMgr.GetScreenWidth() - 136 - MOBILE_MINIMAP_SHIFT - MOBILE_MINIMAP_IOS_EXTRA_X, MOBILE_MINIMAP_IOS_Y)
		## KULLANICI (2026-09-20): "Sunucu, CH1" yazisi sagda kaliyordu -> mini haritanin altina ORTALI
		## (pencere genisliginin ortasi = harita dairesinin ortasi; yukseklik scriptteki gibi).
		try:
			sy = self.serverInfo.GetLocalPosition()[1]
			self.serverInfo.SetHorizontalAlignCenter()
			self.serverInfo.SetPosition(self.GetWidth() / 2, sy)
		except:
			pass

		try:
			self.OpenWindow = self.GetChild("OpenWindow")
			self.MiniMapWindow = self.GetChild("MiniMapWindow")
			self.ScaleUpButton = self.GetChild("ScaleUpButton")
			self.ScaleDownButton = self.GetChild("ScaleDownButton")
			self.MiniMapHideButton = self.GetChild("MiniMapHideButton")
			self.AtlasShowButton = self.GetChild("AtlasShowButton")
			self.CloseWindow = self.GetChild("CloseWindow")
			self.MiniMapShowButton = self.GetChild("MiniMapShowButton")
			self.positionInfo = self.GetChild("PositionInfo")
			self.observerCount = self.GetChild("ObserverCount")
			self.serverInfo = self.GetChild("ServerInfo")
			self.Facebook = self.GetChild("Facebook")
			self.Twitter = self.GetChild("Twitter")
			self.Youtube = self.GetChild("Youtube")
			self.Site = self.GetChild("Site")
		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.Bind")

		if constInfo.MINIMAP_POSITIONINFO_ENABLE==0:
			self.positionInfo.Hide()

		self.serverInfo.SetText(net.GetServerInfo())
		self.ScaleUpButton.SetEvent(ui.__mem_func__(self.ScaleUp))
		self.ScaleDownButton.SetEvent(ui.__mem_func__(self.ScaleDown))
		self.MiniMapHideButton.SetEvent(ui.__mem_func__(self.HideMiniMap))
		self.MiniMapShowButton.SetEvent(ui.__mem_func__(self.ShowMiniMap))
		## KULLANICI (2026-10-08): sosyal medya dugmeleri (baska oyunlarin linkleri) kaldirildi -> hep gizli
		for sosyal in (self.Facebook, self.Twitter, self.Youtube, self.Site):
			sosyal.Hide()

		if miniMap.IsAtlas():
			self.AtlasShowButton.SetEvent(ui.__mem_func__(self.ShowAtlas))

		(ButtonPosX, ButtonPosY) = self.MiniMapShowButton.GetGlobalPosition()
		self.tooltipMiniMapOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.MiniMapHideButton.GetGlobalPosition()
		self.tooltipMiniMapClose.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.ScaleUpButton.GetGlobalPosition()
		self.tooltipScaleUp.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.ScaleDownButton.GetGlobalPosition()
		self.tooltipScaleDown.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.AtlasShowButton.GetGlobalPosition()
		self.tooltipAtlasOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)
		(ButtonPosX, ButtonPosY) = self.Facebook.GetGlobalPosition()
		self.VectorsF.SetTooltipPosition(ButtonPosX, ButtonPosY)
		(ButtonPosX, ButtonPosY) = self.Twitter.GetGlobalPosition()
		self.VectorsT.SetTooltipPosition(ButtonPosX, ButtonPosY)
		(ButtonPosX, ButtonPosY) = self.Youtube.GetGlobalPosition()
		self.VectorsY.SetTooltipPosition(ButtonPosX, ButtonPosY)
		(ButtonPosX, ButtonPosY) = self.Site.GetGlobalPosition()
		self.VectorsS.SetTooltipPosition(ButtonPosX, ButtonPosY)

		## MOBIL (KULLANICI 2026-09-26): yeni Minimap HUD - eski cerceve/dugmeler/yazilar gizli; pencere HUD kutusu
		## boyunda, kok not_pick (bos alanlar dunyaya gecer), gercek harita tasarim dairesinin icine cizilir (OnRender).
		self.hud = None
		if uiminimaphud:
			try:
				self.OpenWindow.Hide()
				self.CloseWindow.Hide()
				self.AddFlag("not_pick")
				self.hud = uiminimaphud.MinimapHud(self, {
					"close": ui.__mem_func__(self.__CollapseHud),
					"open": ui.__mem_func__(self.__ExpandHud),
					"world": ui.__mem_func__(self.__OpenBigMap),
					"zin": ui.__mem_func__(self.ScaleUp),
					"zout": ui.__mem_func__(self.ScaleDown),
				})
			except:
				import dbg
				dbg.TraceError("MiniMap: Minimap HUD kurulamadi")
				self.hud = None
				self.OpenWindow.Show()

		self.ShowMiniMap()

	## KULLANICI (2026-09-26): buyuk harita (bolge dokulari + Ayrintilar + Buraya Git yol gosterici); bolge dokusu
	## olmayan haritada (zindan) eski atlas penceresi
	## KULLANICI (2026-10-02): "kurallar neyse o olmali" - ORIJINAL kural: buyuk harita (atlas) yalniz atlasi olan
	## haritada (miniMap.IsAtlas: <harita>/atlas.sub ya da ui/atlas/<harita>/atlas.sub) ve minimap'in gizlenmedigi
	## haritada acilir. Seytan Kulesi, orumcek/skipia zindanlari, duello/OX vb. -> acilmaz, kisa uyari.
	def __CanBigMap(self):
		if not self.canSeeInfo:
			return False
		try:
			return bool(miniMap.IsAtlas())
		except:
			return False

	def __OpenBigMap(self):
		bm = getattr(self, "bigMap", None)
		if bm and bm.IsShow():
			bm.Close()
			return
		if not self.__CanBigMap():
			hud = getattr(self, "hud", None)
			if hud:
				hud.Flash("buyuk")
			else:
				import chat
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Bu b\xf6lgede b\xfcy\xfck harita kullan\xfdlamaz.")
			return
		if bm is None and uibuyukharita:
			try:
				self.guide = uibuyukharita.GuideOverlay()
				self.bigMap = uibuyukharita.BigMapWindow(self.guide)
				self.guide.SetMapOpener(ui.__mem_func__(self.__OpenBigMap))
				bm = self.bigMap
			except:
				import dbg, traceback
				dbg.TraceError("MiniMap: buyuk harita kurulamadi: " + traceback.format_exc())
				self.bigMap = None
				bm = None
		if bm:
			try:
				if bm.IsShow():
					bm.Close()
					return
				if bm.Open():
					return
			except:
				import dbg, traceback
				dbg.TraceError("MiniMap: buyuk harita acilamadi: " + traceback.format_exc())
		self.ToggleAtlasWindow()

	## KULLANICI (2026-09-26): X tum mini harita HUD'unu kapatir, sag ustteki "+" geri acar
	def __CollapseHud(self):
		miniMap.Hide()
		if getattr(self, "hud", None):
			self.hud.Collapse()

	def __ExpandHud(self):
		if self.canSeeInfo:
			miniMap.Show()
		if getattr(self, "hud", None):
			self.hud.Expand()

	def __ToggleMiniMap(self):
		if miniMap.isShow():
			self.HideMiniMap()
		else:
			self.ShowMiniMap()

	def Destroy(self):
		## KULLANICI (2026-09-27): "mini haritada iki tane olmus, biri sola kaymis" - isinlaninca arayuz yeniden
		## kurulur; eski MiniMap, HUD katmaninin sahip referansi (dongu + __del__ -> Py2 GC toplayamaz) yuzunden
		## bellekte kalip gercek haritayi ESKI konumuna cizmeye devam ediyordu. Yok edilince: gizle, cizme, donguleri kir.
		self.destroyed = True
		self.HideMiniMap()
		try:
			if getattr(self, "hud", None):
				self.hud.Destroy()
		except:
			pass
		self.hud = None
		try:
			if getattr(self, "guide", None):
				self.guide.Stop()
				self.guide.Destroy()
			if getattr(self, "bigMap", None):
				self.bigMap.Destroy()
		except:
			pass
		self.guide = None
		self.bigMap = None
		self.Hide()

		self.AtlasWindow.Destroy()
		self.AtlasWindow = None

		self.ClearDictionary()

		self.__Initialize()

	def UpdateObserverCount(self, observerCount):
		if observerCount>0:
			self.observerCount.Show()
		elif observerCount<=0:
			self.observerCount.Hide()

		self.observerCount.SetText(localeInfo.MINIMAP_OBSERVER_COUNT % observerCount)
		
	def OnUpdate(self):
		if getattr(self, "destroyed", False):
			return
		(x, y, z) = player.GetMainCharacterPosition()
		miniMap.Update(x, y)
		if getattr(self, "hud", None):
			self.hud.Update()

		## HIZ (2026-10-01): koordinat/sunucu yazisi ve PC fare ipuclari (IsIn x9) her kare yerine 0.1 s'de bir
		## (HUD altinda gizli yazilar; dokunmatikte ipucu zaten anlik degil)
		tq = app.GetTime()
		if 0.0 <= tq - getattr(self, "_mobTipT", -1.0) < 0.1:
			return
		self._mobTipT = tq
		self.positionInfo.SetText("(%.0f, %.0f)" % (x/100, y/100))
		
		serverName = serverInfo.SERVER_1
		self.serverInfo.SetText(str(serverName)+", CH"+str(constInfo.indexver))

		if self.tooltipInfo:
			if True == self.MiniMapWindow.IsIn():
				(mouseX, mouseY) = wndMgr.GetMousePosition()
				(bFind, sName, iPosX, iPosY, dwTextColor) = miniMap.GetInfo(mouseX, mouseY)
				if bFind == 0:
					self.tooltipInfo.Hide()
				elif not self.canSeeInfo:
					self.tooltipInfo.SetText("%s(%s)" % (sName, localeInfo.UI_POS_UNKNOWN))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
				else:
					if localeInfo.IsARABIC() and sName[-1].isalnum():
						self.tooltipInfo.SetText("(%s)%d, %d" % (sName, iPosX, iPosY))
					else:
						self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
			else:
				self.tooltipInfo.Hide()
			
			# AUTOBAN
			if self.imprisonmentDuration:
				self.__UpdateImprisonmentDurationText()				
			# END_OF_AUTOBAN

		if True == self.MiniMapShowButton.IsIn():
			self.tooltipMiniMapOpen.Show()
		else:
			self.tooltipMiniMapOpen.Hide()

		if True == self.MiniMapHideButton.IsIn():
			self.tooltipMiniMapClose.Show()
		else:
			self.tooltipMiniMapClose.Hide()

		if True == self.ScaleUpButton.IsIn():
			self.tooltipScaleUp.Show()
		else:
			self.tooltipScaleUp.Hide()

		if True == self.ScaleDownButton.IsIn():
			self.tooltipScaleDown.Show()
		else:
			self.tooltipScaleDown.Hide()

		if True == self.AtlasShowButton.IsIn():
			self.tooltipAtlasOpen.Show()
		else:
			self.tooltipAtlasOpen.Hide()
		for sosyal in (self.VectorsF, self.VectorsT, self.VectorsY, self.VectorsS):
			sosyal.Hide()

	def OnRender(self):
		if getattr(self, "destroyed", False):
			return
		(x, y) = self.GetGlobalPosition()
		fx = float(x)
		fy = float(y)
		hud = getattr(self, "hud", None)
		if hud:
			(mx, my) = uiminimaphud.G.VIEW[0] * hud.k + hud.dx, uiminimaphud.G.VIEW[1] * hud.k + hud.dy
			miniMap.Render(fx + round(mx), fy + round(my))
			return
		miniMap.Render(fx + 4.0, fy + 5.0)

	def Close(self):
		self.HideMiniMap()

	def HideMiniMap(self):
		miniMap.Hide()
		if getattr(self, "hud", None):
			self.hud.SetMapOn(False)
			return
		self.OpenWindow.Hide()
		self.CloseWindow.Show()

	def ShowMiniMap(self):
		if not self.canSeeInfo:
			return

		miniMap.Show()
		if getattr(self, "hud", None):
			self.hud.SetMapOn(True)
			return
		self.OpenWindow.Show()
		self.CloseWindow.Hide()

	def isShowMiniMap(self):
		return miniMap.isShow()

	def ScaleUp(self):
		miniMap.ScaleUp()

	def ScaleDown(self):
		miniMap.ScaleDown()

	def ShowAtlas(self):
		if not miniMap.IsAtlas():
			return
		if not self.AtlasWindow.IsShow():
			self.AtlasWindow.Show()

	## KULLANICI (2026-10-08): eski sosyal medya dugmeleri baska oyunlara gidiyordu (chaos2/vevo) -> KALDIRILDI.
	## Dugmeler gizli, fonksiyonlar hicbir sey yapmaz (ui betigi Facebook/Twitter/Youtube/Site cocuklarini hala tanimliyor).
	def Vectors(self):
		pass
	def Vectors1(self):
		pass
	def Vectors2(self):
		pass
	def Vectors3(self):
		pass


	def ToggleAtlasWindow(self):
		if not miniMap.IsAtlas():
			return
		if self.AtlasWindow.IsShow():
			self.AtlasWindow.Hide()
		else:
			self.AtlasWindow.Show()
