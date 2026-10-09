# MOBIL KAPLAMA (mobile_root/introempire.py): pack root/introempire.py kopyasi. KULLANICI (2026-09-16):
#  - sol pano PC boyutundaydi -> kendi OLCEKLI kokunde (introselect.py mantigi)
#  - hikaye yazisi event sisteminden geliyordu (olceklenmez, PC konumunda kalir) -> panoda kendi TextLine sayfalari
#  - 3 imparatorluk haritasi kucuk ve solda -> olcekli kok + saga kaydirma; bolge dokunmalari haritanin COCUGU
#  - haritayla gelmeyen KIRMIZI ok dugmeleri mobilde gizli
MOBILE_EMPIRE_BOARD_SCALE = 1.8
MOBILE_DESC_FONT = "Tahoma:12"
MOBILE_DESC_LINES = 7
MOBILE_ATLAS_SCALE = 1.35
MOBILE_ATLAS_DX = 200
MOBILE_CR = "%c" % 13
MOBILE_LF = "%c" % 10
import ui
import net
import wndMgr
import dbg
import app
import event
import _weakref
import localeInfo
import uiScriptLocale

LOCALE_PATH = "uiscript/"+uiScriptLocale.CODEPAGE+"_"

class SelectEmpireWindow(ui.ScriptWindow):

	EMPIRE_DESCRIPTION_TEXT_FILE_NAME = {	
		net.EMPIRE_A : uiScriptLocale.EMPIREDESC_A,
		net.EMPIRE_B : uiScriptLocale.EMPIREDESC_B,
		net.EMPIRE_C : uiScriptLocale.EMPIREDESC_C, }

	class EmpireButton(ui.Window):
		def __init__(self, owner, arg):
			ui.Window.__init__(self)
			self.owner = owner
			self.arg = arg
		def OnMouseOverIn(self):
			self.owner.OnOverInEmpire(self.arg)
		def OnMouseOverOut(self):
			self.owner.OnOverOutEmpire(self.arg)
		def OnMouseLeftButtonDown(self):
			if self.owner.empireID != self.arg:
				self.owner.OnSelectEmpire(self.arg)

	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = 0
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet(self.descIndex)

	def __init__(self, stream):
		print "NEW EMPIRE WINDOW  ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_EMPIRE, self)

		self.stream=stream
		self.empireID=app.GetRandom(1, 3)
		self.descIndex=0
		self.empireArea = {}
		self.empireAreaFlag = {}
		self.empireFlag = {}
		self.empireAreaButton = {}
		self.empireAreaCurAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }
		self.empireAreaDestAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }
		self.empireAreaFlagCurAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }
		self.empireAreaFlagDestAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }
		self.empireFlagCurAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }
		self.empireFlagDestAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }
		self.kareSonZaman = None ## MOBIL (v76 kare->zaman): bkz. __GecenKareSayisi

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_EMPIRE, 0)
		print "---------------------------------------------------------------------------- DELETE EMPIRE WINDOW"

	def Close(self):
		print "---------------------------------------------------------------------------- CLOSE EMPIRE WINDOW"		

		self.ClearDictionary()
		self.leftButton = None
		self.rightButton = None
		self.selectButton = None
		self.exitButton = None
		self.textBoard = None
		self.descriptionBox = None
		self.empireArea = None
		self.empireAreaButton = None

		self.KillFocus()
		self.Hide()

		app.HideCursor()
		event.Destroy()

	def Open(self):
		print "OPEN EMPIRE WINDOW ----------------------------------------------------------------------------"

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("SelectEmpireWindow")
		self.Show()	

		if not self.__LoadScript(uiScriptLocale.LOCALE_UISCRIPT_PATH + "SelectEmpireWindow.py"):
			dbg.TraceError("SelectEmpireWindow.Open - __LoadScript Error")
			return

		self.OnSelectEmpire(self.empireID)
		self.__CreateButtons()
		self.__CreateDescriptionBox()
		app.ShowCursor()

	def __CreateButtons(self):
		for key, img in self.empireArea.items():

			img.SetAlpha(0.0)

			## MOBIL: harita en ustte ve dokunmayi yutuyor -> dokunma penceresi haritanin COCUGU
			atlas = getattr(self, "mobileAtlas", None)
			btn = self.EmpireButton(_weakref.proxy(self), key)
			if atlas:
				(lx, ly) = img.GetLocalPosition()
				btn.SetParent(atlas)
				btn.SetPosition(lx, ly)
			else:
				(x, y) = img.GetGlobalPosition()
				btn.SetParent(self)
				btn.SetPosition(x, y)
			btn.SetSize(img.GetWidth(), img.GetHeight())
			btn.Show()
			self.empireAreaButton[key] = btn

	def __CreateDescriptionBox(self):
		## MOBIL: event yazisi olcekli panoyla gelmiyor -> gizli; yazi panoda kendi TextLine sayfalarimiz
		self.descriptionBox = self.DescriptionBox()
		self.descriptionBox.Hide()
		try:
			self.__MobileBuildDesc()
			self.__MobileSetDesc(self.empireID)
		except:
			import traceback
			dbg.TraceError("MOBIL imparatorluk aciklamasi: " + traceback.format_exc())

	def OnOverInEmpire(self, arg):
		self.empireAreaDestAlpha[arg] = 1.0

	def OnOverOutEmpire(self, arg):
		if arg != self.empireID:
			self.empireAreaDestAlpha[arg] = 0.0

	def OnSelectEmpire(self, arg):
		for key in self.empireArea.keys():
			self.empireAreaDestAlpha[key] = 0.0
			self.empireAreaFlagDestAlpha[key] = 0.0
			self.empireFlagDestAlpha[key] = 0.0
		self.empireAreaDestAlpha[arg] = 1.0
		self.empireAreaFlagDestAlpha[arg] = 1.0
		self.empireFlagDestAlpha[arg] = 1.0
		self.empireID = arg
		
		event.ClearEventSet(self.descIndex)
		if self.EMPIRE_DESCRIPTION_TEXT_FILE_NAME.has_key(arg):
			self.descIndex = event.RegisterEventSet(self.EMPIRE_DESCRIPTION_TEXT_FILE_NAME[arg])

			if localeInfo.IsARABIC():
				event.SetEventSetWidth(self.descIndex, 170)
			else:
				event.SetRestrictedCount(self.descIndex, 35)
		if getattr(self, "mobileDescLines", None):
			self.__MobileSetDesc(arg)

	def PrevDescriptionPage(self):
		if getattr(self, "mobileDescPages", None):
			self.__MobileTurnPage(-1)
			return
		if True == event.IsWait(self.descIndex):
			if event.GetVisibleStartLine(self.descIndex)-5 >= 0:
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex)-5)
				event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)

	def NextDescriptionPage(self):
		if getattr(self, "mobileDescPages", None):
			self.__MobileTurnPage(1)
			return
		if True == event.IsWait(self.descIndex):
			event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex)+5)
			event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)

	def __LoadScript(self, fileName):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, fileName)	
		except:
			import exception
			exception.Abort("SelectEmpireWindow.__LoadScript.LoadObject")

		try:
			GetObject=self.GetChild
			self.leftButton		= GetObject("left_button")
			self.rightButton	= GetObject("right_button")
			self.selectButton	= GetObject("select_button")
			self.exitButton		= GetObject("exit_button")
			self.textBoard		= GetObject("text_board")
			self.empireArea[net.EMPIRE_A]	= GetObject("EmpireArea_A")
			self.empireArea[net.EMPIRE_B]	= GetObject("EmpireArea_B")
			self.empireArea[net.EMPIRE_C]	= GetObject("EmpireArea_C")
			self.empireAreaFlag[net.EMPIRE_A]	= GetObject("EmpireAreaFlag_A")
			self.empireAreaFlag[net.EMPIRE_B]	= GetObject("EmpireAreaFlag_B")
			self.empireAreaFlag[net.EMPIRE_C]	= GetObject("EmpireAreaFlag_C")
			self.empireFlag[net.EMPIRE_A]	= GetObject("EmpireFlag_A")
			self.empireFlag[net.EMPIRE_B]	= GetObject("EmpireFlag_B")
			self.empireFlag[net.EMPIRE_C]	= GetObject("EmpireFlag_C")
			GetObject("prev_text_button").SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
			GetObject("next_text_button").SetEvent(ui.__mem_func__(self.NextDescriptionPage))
		except:
			import exception
			exception.Abort("SelectEmpireWindow.__LoadScript.BindObject")					

		## MOBIL: pano + harita mobil boyut
		self.mobileBoardRoot = None
		self.mobileAtlasRoot = None
		self.mobileAtlas = None
		self.mobileAtlasScale = 1.0
		self.mobileDescLines = []
		self.mobileDescPages = []
		self.mobileDescPage = 0
		try:
			self.mobileBoardRoot = self.__MobileScaleBoard(GetObject, MOBILE_EMPIRE_BOARD_SCALE)
			self.mobileAtlasRoot = self.__MobileScaleAtlas(GetObject, MOBILE_ATLAS_SCALE, MOBILE_ATLAS_DX)
		except:
			import traceback
			dbg.TraceError("MOBIL imparatorluk ekrani: " + traceback.format_exc())

		self.selectButton.SetEvent(ui.__mem_func__(self.ClickSelectButton))
		self.exitButton.SetEvent(ui.__mem_func__(self.ClickExitButton))
		self.leftButton.SetEvent(ui.__mem_func__(self.ClickLeftButton))
		self.rightButton.SetEvent(ui.__mem_func__(self.ClickRightButton))
		## MOBIL: harita tasininca eski yerinde kalan kirmizi ok gorselleri gizlenir
		self.leftButton.Hide()
		self.rightButton.Hide()
		for flag in self.empireAreaFlag.values():
			flag.SetAlpha(0.0)
		for flag in self.empireFlag.values():
			flag.SetAlpha(0.0)

		return 1

	## ---------------- MOBIL yardimcilari ----------------
	def __MobileScaleBoard(self, GetObject, scale):
		board = GetObject("empire_board")
		root = ui.Window()
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(root.hWnd, scale)
		root.AddFlag("not_pick")
		root.SetWindowName("MobileEmpireBoardRoot")
		w = board.GetWidth()
		h = board.GetHeight()
		root.SetSize(w, h)
		board.SetParent(root)
		board.SetPosition(0, 0)
		root.SetPosition(40, max(8, int((wndMgr.GetScreenHeight() - h * scale) / 2)))
		root.Show()
		return root

	def __MobileScaleAtlas(self, GetObject, scale, dx):
		atlas = GetObject("Atlas")
		(gx, gy) = atlas.GetGlobalPosition()
		w = atlas.GetWidth()
		h = atlas.GetHeight()
		root = ui.Window()
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(root.hWnd, scale)
		root.AddFlag("not_pick")
		root.SetWindowName("MobileEmpireAtlasRoot")
		root.SetSize(w, h)
		atlas.SetParent(root)
		atlas.SetPosition(0, 0)
		root.SetPosition(int(gx - w * (scale - 1.0) / 2 + dx), int(max(0, gy - h * (scale - 1.0) / 2)))
		root.Show()
		self.mobileAtlas = atlas
		self.mobileAtlasScale = scale
		return root

	def __MobileBuildDesc(self):
		board = self.GetChild("text_board")
		self.mobileDescLines = []
		for i in xrange(MOBILE_DESC_LINES):
			t = ui.TextLine()
			t.SetParent(board)
			t.AddFlag("not_pick")
			t.SetFontName(MOBILE_DESC_FONT)
			t.SetFontColor(1.0, 1.0, 1.0)
			t.SetPosition(8, 8 + i * 18)
			t.SetText("")
			t.Show()
			self.mobileDescLines.append(t)

	def __MobileLoadPages(self, fileName):
		## metin dosyasi: [DELAY ...] / [WAIT] (sayfa sonu) / [ENTER] (satir sonu)
		data = ""
		try:
			import pack
			data = pack.Get(fileName)
		except:
			try:
				data = open(fileName, "r").read()
			except:
				return []
		pages = []
		lines = []
		for raw in data.replace(MOBILE_CR, "").split(MOBILE_LF):
			token = raw.strip()
			up = token.upper()
			if up.startswith("[WAIT"):
				if lines:
					pages.append(lines)
					lines = []
				continue
			if up.startswith("[DELAY") or up.startswith("[ESCAPE") or up.startswith("[CLOSE"):
				continue
			text = token
			while "[" in text and "]" in text:
				i = text.find("[")
				j = text.find("]", i)
				if j < 0:
					break
				text = text[:i] + text[j + 1:]
			text = text.strip()
			if not text:
				continue
			lines.append(text)
			if len(lines) >= MOBILE_DESC_LINES:
				pages.append(lines)
				lines = []
		if lines:
			pages.append(lines)
		return pages

	def __MobileSetDesc(self, empireID):
		fileName = self.EMPIRE_DESCRIPTION_TEXT_FILE_NAME.get(empireID, "")
		self.mobileDescPages = self.__MobileLoadPages(fileName) if fileName else []
		self.mobileDescPage = 0
		self.__MobileRefreshDesc()

	def __MobileRefreshDesc(self):
		if not self.mobileDescLines:
			return
		page = []
		if self.mobileDescPages:
			self.mobileDescPage = max(0, min(self.mobileDescPage, len(self.mobileDescPages) - 1))
			page = self.mobileDescPages[self.mobileDescPage]
		for (i, t) in enumerate(self.mobileDescLines):
			t.SetText(page[i] if i < len(page) else "")

	def __MobileTurnPage(self, delta):
		if not self.mobileDescPages:
			return
		self.mobileDescPage = (self.mobileDescPage + delta) % len(self.mobileDescPages)
		self.__MobileRefreshDesc()

	def ClickLeftButton(self):
		self.empireID-=1
		if self.empireID<1:
			self.empireID=3

		self.OnSelectEmpire(self.empireID)

	def ClickRightButton(self):
		self.empireID+=1
		if self.empireID>3:
			self.empireID=1

		self.OnSelectEmpire(self.empireID)

	def ClickSelectButton(self):
		net.SendSelectEmpirePacket(self.empireID)
		self.stream.SetSelectCharacterPhase()

	def ClickExitButton(self):
		self.stream.SetLoginPhase()

	def OnUpdate(self):
		## MOBIL: event yazisi kullanilmiyor (kendi TextLine sayfalarimiz)

		## MOBIL (v76 kare->zaman): kare basi /7 yaklasim -> k = 1 - (6/7) ** n (n=1 -> 1/7 = eski /7);
		## n bir kez olculur, uc sozluk ayni k ile ilerler.
		k = 1.0 - (6/7.0) ** self.__GecenKareSayisi()

		self.__UpdateAlpha(self.empireArea, self.empireAreaCurAlpha, self.empireAreaDestAlpha, k)
		self.__UpdateAlpha(self.empireAreaFlag, self.empireAreaFlagCurAlpha, self.empireAreaFlagDestAlpha, k)
		self.__UpdateAlpha(self.empireFlag, self.empireFlagCurAlpha, self.empireFlagDestAlpha, k)

	## MOBIL (v76 kare->zaman): son OnUpdate'ten beri gecen sure, 60 Hz mantik adimi (16.5 ms) cinsinden.
	## Motor saati (app.GetTime, CTimer ozel kip) 60 FPS'te kare basi 16/17 ms ilerler -> n tam 1.0
	## (eski kare basi davranis BIREBIR); FPS siniri 30'da ~33 ms -> n ~2.0. Ilk cagri / ust sinir 0.25 sn.
	def __GecenKareSayisi(self):
		now = app.GetTime()
		last = self.kareSonZaman
		self.kareSonZaman = now
		if last is None:
			return 1.0
		dt = min(0.25, max(0.0, now - last))
		n = dt / 0.0165
		## 0.8..1.2: app.GetTime float32 -> uzun oturumda dt 1-2 ms sapabilir; 45 FPS adimi (n~1.35) disarida.
		if 0.8 < n < 1.2:
			return 1.0
		return n

	def __UpdateAlpha(self, dict, curAlphaDict, destAlphaDict, k):
		for key, img in dict.items():

			curAlpha = curAlphaDict[key]
			destAlpha = destAlphaDict[key]

			if abs(destAlpha - curAlpha) / 10 > 0.0001:
				curAlpha += (destAlpha - curAlpha) * k
			else:
				curAlpha = destAlpha

			curAlphaDict[key] = curAlpha
			img.SetAlpha(curAlpha)

	def OnPressEscapeKey(self):
		self.ClickExitButton()
		return True

class ReselectEmpireWindow(SelectEmpireWindow):
	def ClickSelectButton(self):
		net.SendSelectEmpirePacket(self.empireID)
		self.stream.SetCreateCharacterPhase()

	def ClickExitButton(self):
		self.stream.SetSelectCharacterPhase()
