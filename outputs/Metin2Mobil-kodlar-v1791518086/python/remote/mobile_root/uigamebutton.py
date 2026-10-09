# MOBIL KAPLAMA (mobile_root/uigamebutton.py): pack root/uigamebutton.py BIREBIR kopyasi; tek fark
# KULLANICI (2026-09-13): telefonda "Becerileri Gelistir" (SKILL) ve "Bakim" (ADMPANEL) dugmeleri
# gosterilmez (ekranda saldiri topu/iksir kutularinin ustune biniyordu; beceriler V ile acilir).
import app
import ui
import wndMgr
import player
import net
if app.ENABLE_MAINTENANCE_SYSTEM:
	import constInfo
	import chr
	
class GameButtonWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.__LoadWindow("UIScript/gamewindow.py")

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self, filename):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, filename)
		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return False

		try:
			self.gameButtonDict={
				"STATUS" : self.GetChild("StatusPlusButton"),
				"SKILL" : self.GetChild("SkillPlusButton"),
				"QUEST" : self.GetChild("QuestButton"),
				"HELP" : self.GetChild("HelpButton"),
				"BUILD" : self.GetChild("BuildGuildBuilding"),
				"EXIT_OBSERVER" : self.GetChild("ExitObserver"),
			}
			
			if app.ENABLE_MAINTENANCE_SYSTEM:
				self.gameButtonDict.update({
				"ADMPANEL" : self.GetChild("AdmPanel"),
			})

			self.gameButtonDict["EXIT_OBSERVER"].SetEvent(ui.__mem_func__(self.__OnClickExitObserver))
			if app.ENABLE_MAINTENANCE_SYSTEM:
				self.gameButtonDict["ADMPANEL"].SetEvent(ui.__mem_func__(self.MaintenanceAdmin))

		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return False

		self.__HideAllGameButton()
		self.SetObserverMode(player.IsObserverMode())
		return True

	def Destroy(self):
		for key in self.gameButtonDict:
			self.gameButtonDict[key].SetEvent(0)

		self.gameButtonDict={}

	def SetButtonEvent(self, name, event):
		try:
			self.gameButtonDict[name].SetEvent(event)
		except Exception, msg:
			print "GameButtonWindow.LoadScript - %s" % (msg)
			app.Abort()
			return

	def ShowBuildButton(self):
		self.gameButtonDict["BUILD"].Show()

	def HideBuildButton(self):
		self.gameButtonDict["BUILD"].Hide()

	def CheckGameButton(self):

		if not self.IsShow():
			return

		statusPlusButton=self.gameButtonDict["STATUS"]
		skillPlusButton=self.gameButtonDict["SKILL"]
		helpButton=self.gameButtonDict["HELP"]
		if app.ENABLE_MAINTENANCE_SYSTEM:
			admpanel1=self.gameButtonDict["ADMPANEL"]

		## MOBIL (KULLANICI 2026-09-26): Statu Gelistir dugmesi EXP kurelerinin ustune biniyordu -> mobilde
		## gosterilmez; statu puanlari Karakter penceresinden dagitilir.
		statusPlusButton.Hide()
		## MOBIL: Statu Gelistir dugmesi EXP kurelerinin USTUNDE (kurelere biniyordu):
		## hedef mantiksal (0.065 W + 2, kure ustu - 40) - kok konumu cikarilarak yerel konum
		try:
			(rx, ry) = self.GetGlobalPosition()
			sw = wndMgr.GetScreenWidth()
			sh = wndMgr.GetScreenHeight()
			orbTop = sh - (3 * 12 + 2 * 3) - 4 - 6 - 46
			statusPlusButton.SetPosition(int(sw * 0.065) + 2 - rx, orbTop - statusPlusButton.GetHeight() - 6 - ry)
		except:
			pass

		skillPlusButton.Hide()

		# Mobil: Yardim dugmesi kamera kaydiricisinin ustune biniyordu; yardim Kisayollar > H ile acilir.
		helpButton.Hide()
			
		if app.ENABLE_MAINTENANCE_SYSTEM:
			admpanel1.Hide()

	def __IsSkillStat(self):
		if player.GetStatus(player.SKILL_ACTIVE) > 50:
			return True

		return False

	def __OnClickExitObserver(self):
		net.SendChatPacket("/observer_exit")
		
	def __HideAllGameButton(self):
		for btn in self.gameButtonDict.values():
			btn.Hide()

	if app.ENABLE_MAINTENANCE_SYSTEM:
		def MaintenanceAdmin(self):
			constInfo.MAINTENANCEADMIN_OPEN = 1

	def SetObserverMode(self, isEnable):
		if isEnable:
			self.gameButtonDict["EXIT_OBSERVER"].Show()
		else:
			self.gameButtonDict["EXIT_OBSERVER"].Hide()
