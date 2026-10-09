# MOBIL KAPLAMA (mobile_root/introloading.py): pack root/introloading.py BIREBIR kopyasi; farklar "MOBIL" yorumlu.
# KULLANICI (2026-09-14): (1) yukleme perdesi FLOAT + SetTop -> ayri kok ekipman penceresi (float) perdenin
# ustune cikmiyor; (2) yukleme ekrani: logo + donen halka + "Harita yukleniyor..." + Mobilserverler.com.
import ui
import uiScriptLocale
import net
import app
import dbg
import player
import background
import wndMgr

import localeInfo
import chrmgr
import colorInfo
import constInfo

import playerSettingModule
import stringCommander
import emotion
import uimobileloading	# MOBIL (2026-09-24): yeni yukleme ekrani

####################################
# 빠른 실행을 위한 모듈 로딩 분담
####################################
import uiRefine
import uiToolTip
import uiAttachMetin
import uiPickMoney
import uiChat
import uiMessenger
import uiHelp
import uiWhisper
import uiPointReset
import uiShop
import uiExchange
import uiSystem
import uiOption
import uiRestart
####################################

class LoadingWindow(ui.ScriptWindow):
	def __init__(self, stream):
		print "NEW LOADING WINDOW -------------------------------------------------------------------------------"
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, self)

		self.stream=stream
		self.loadingImage=0
		self.loadingGage=0
		self.errMsg=0
		self.update=0
		self.playerX=0
		self.playerY=0
		self.loadStepList=[]

	def __del__(self):
		print "---------------------------------------------------------------------------- DELETE LOADING WINDOW"
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, 0)
		ui.Window.__del__(self)

	def Open(self):
		print "OPEN LOADING WINDOW -------------------------------------------------------------------------------"
		#app.HideCursor()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			
			if localeInfo.IsYMIR() or localeInfo.IsWE_KOREA() or localeInfo.IsCANADA() or localeInfo.IsBRAZIL() or localeInfo.IsEUROPE() or localeInfo.IsJAPAN():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "LoadingWindow.py")
			else:			
				pyScrLoader.LoadScriptFile(self, "UIScript/LoadingWindow.py")
		except:
			import exception
			exception.Abort("LodingWindow.Open - LoadScriptFile Error")

		try:
			self.loadingImage=self.GetChild("BackGround")
			self.errMsg=self.GetChild("ErrorMessage")
			self.loadingGage=self.GetChild("FullGage")
		except:
			import exception
			exception.Abort("LodingWindow.Open - LoadScriptFile Error")

		self.errMsg.Hide()

		if constInfo.SUB2_LOADING_ENABLE:
			imgFileNameDict = {
				0 : "d:/ymir work/uiloading/background_loading_warrior.sub",
				1 : "d:/ymir work/uiloading/background_loading_assassin.sub",
				2 : "d:/ymir work/uiloading/background_loading_shaman.sub",
				3 : "d:/ymir work/uiloading/background_loading_sura.sub",
				4 : "d:/ymir work/uiloading/background_loading_assassin2.sub",
				5 : "d:/ymir work/uiloading/background_loading_sura2.sub",
				6 : "d:/ymir work/uiloading/background_loading_assassin3.sub",
				7 : "d:/ymir work/uiloading/background_loading_assassin3.sub",
			}
		else:
			imgFileNameDict = {
				0 : "d:/ymir work/ui/intro/pattern/background_loading_warrior.jpg",
				1 : "d:/ymir work/ui/intro/pattern/background_loading_assassin.jpg",
				2 : "d:/ymir work/ui/intro/pattern/background_loading_shaman.jpg",
			}

		## MOBIL (KULLANICI 2026-09-24): yeni yukleme ekrani (Desktop/Metin2-Loading-Ekrani) - uimobileloading.
		## Betikteki BackGround/GageBoard/FullGage artik doku yuklemeyen bos pencereler; ilerleme skin'e gider.
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: tam ekran, olceksiz
		self.AddFlag("float")	# MOBIL: perde HER float pencerenin (ekipman koku dahil) ustunde
		## MOBIL DUZELTME (2026-09-24): bu satirlar 2026-09-14 duzenlemesinde yanlislikla __MobileAnimate'in
		## icine kalmisti -> karakter secim paketi HER KAREDE sunucuya gidiyordu. Gercek client: Open() sonu.
		self.mobileOpenTime = app.GetTime()
		self.mobileSkin = None
		try:
			self.mobileSkin = uimobileloading.LoadingSkin(self)
		except:
			import exception
			exception.Abort("LoadingWindow.Open - uimobileloading.LoadingSkin")
		self.Show()
		self.SetTop()

		chrSlot=self.stream.GetCharacterSlot()
		net.SendSelectCharacterPacket(chrSlot)

		app.SetFrameSkip(0)

	def __MobileAnimate(self):
		skin = getattr(self, "mobileSkin", None)
		if skin:
			try:
				skin.Update(app.GetTime())
			except:
				import dbg
				dbg.TraceError("LoadingWindow: mobileSkin.Update hata")
				self.mobileSkin = None

	def Close(self):
		print "---------------------------------------------------------------------------- CLOSE LOADING WINDOW"

		app.SetFrameSkip(1)

		skin = getattr(self, "mobileSkin", None)	# MOBIL: dokular serbest kalsin
		if skin:
			## olcum (syserr): toplam yukleme, skin kurulumu (doku cozme), cubugun adim bekletmesi
			try:
				import dbg
				dbg.TraceError("LOADING SURE: toplam %.2fs | skin kurulum %.3fs | cubuk bekletme %.2fs | adimlar %s" % (
					app.GetTime() - getattr(self, "mobileOpenTime", app.GetTime()), skin.buildSec, skin.waitSec,
					" ".join(getattr(self, "stepTimes", []))))
			except:
				pass
			skin.Destroy()
			self.mobileSkin = None

		self.loadStepList=[]
		self.loadingImage=0
		self.loadingGage=0
		self.errMsg=0
		self.ClearDictionary()
		self.Hide()

	def OnPressEscapeKey(self):
		app.SetFrameSkip(1)
		self.stream.SetLoginPhase()
		return True

	def __SetNext(self, next):
		if next:
			self.update=ui.__mem_func__(next)
		else:
			self.update=0

	def __SetProgress(self, p):
		skin = getattr(self, "mobileSkin", None)	# MOBIL: gercek yukleme adimi -> yeni cubuk
		if skin:
			skin.SetProgress(p)

	def DEBUG_LoadData(self, playerX, playerY):
		self.playerX=playerX
		self.playerY=playerY

		self.__RegisterSkill() ## 로딩 중간에 실행 하면 문제 발생
		self.__RegisterTitleName()
		self.__RegisterColor()
		self.__InitData()
		self.__LoadMap()
		self.__LoadSound()
		self.__LoadEffect()
		self.__LoadWarrior()
		self.__LoadAssassin()
		self.__LoadSura()
		self.__LoadShaman()
		self.__LoadSkill()
		self.__LoadEnemy()
		self.__LoadNPC()
		self.__StartGame()

	def LoadData(self, playerX, playerY):
		self.playerX=playerX
		self.playerY=playerY

		self.__RegisterDungeonMapName()
		self.__RegisterSkill() ## 로딩 중간에 실행 하면 문제 발생
		self.__RegisterTitleName()
		self.__RegisterColor()
		self.__RegisterEmotionIcon()

		self.loadStepList=[
			(0, ui.__mem_func__(self.__InitData)),
			(10, ui.__mem_func__(self.__LoadMap)),
			(30, ui.__mem_func__(self.__LoadSound)),
			(40, ui.__mem_func__(self.__LoadEffect)),
			(45, ui.__mem_func__(self.__LoadWarriorA)),	# MOBIL (ANR): irk yarilari ayri karelerde
			(50, ui.__mem_func__(self.__LoadWarrior)),
			(55, ui.__mem_func__(self.__LoadAssassinA)),
			(60, ui.__mem_func__(self.__LoadAssassin)),
			(65, ui.__mem_func__(self.__LoadSuraA)),
			(70, ui.__mem_func__(self.__LoadSura)),
			(75, ui.__mem_func__(self.__LoadShamanA)),
			(80, ui.__mem_func__(self.__LoadShaman)),
			(90, ui.__mem_func__(self.__LoadSkill)),
			(93, ui.__mem_func__(self.__LoadEnemy)),
			(97, ui.__mem_func__(self.__LoadNPC)),

			# GUILD_BUILDING
			(98, ui.__mem_func__(self.__LoadGuildBuilding)),
			# END_OF_GUILD_BUILDING

			(100, ui.__mem_func__(self.__StartGame)),
		]

		self.__SetProgress(0)
		#self.__SetNext(self.__LoadMap)

	def OnUpdate(self):
		self.__MobileAnimate()	# MOBIL
		if len(self.loadStepList)>0:
			(progress, runFunc)=self.loadStepList[0]

			## MOBIL (KULLANICI 2026-09-24): cubuk gercek yuklemeyle bir olsun - adimin degeri once hedef olur,
			## cubuk gorsel olarak oraya ulasmadan adim calismaz. Son adim (100 = StartGame) boylece cubuk
			## TAM DOLDUKTAN sonra calisir; harita yuklenirken (uzun adim) cubuk %10'da bekler, sonra akar.
			## OLCUM (2026-09-24): her adim kapisi 0.83 s bekletiyordu -> yalniz SON adim (100 = StartGame) cubugu
			## bekler; ara adimlar hemen calisir, cubuk gercek yukleme surerken (harita/veri) zaten yetisir.
			skin = getattr(self, "mobileSkin", None)
			if skin:
				skin.SetProgress(progress)
				if progress >= 100 and not skin.Reached():
					return

			import time
			_t0 = time.time()
			try:
				runFunc()
			except:	
				self.errMsg.Show()
				self.loadStepList=[]

				## 이곳에서 syserr.txt 를 보낸다.

				import dbg
				dbg.TraceError(" !!! Failed to load game data : STEP [%d]" % (progress))

				#import shutil
				#import os
				#shutil.copyfile("syserr.txt", "errorlog.txt")
				#os.system("errorlog.exe")

				app.Exit()

				return

			self.loadStepList.pop(0)
			self.stepTimes = getattr(self, "stepTimes", []) + ["%d:%.2f" % (progress, time.time() - _t0)]	# olcum

			self.__SetProgress(progress)

	def __InitData(self):
		playerSettingModule.LoadGameData("INIT")

	def __RegisterDungeonMapName(self):
		background.RegisterDungeonMapName("metin2_map_spiderdungeon")
		background.RegisterDungeonMapName("metin2_map_monkeydungeon")
		background.RegisterDungeonMapName("metin2_map_monkeydungeon_02")
		background.RegisterDungeonMapName("metin2_map_monkeydungeon_03")
		background.RegisterDungeonMapName("metin2_map_deviltower1")

	def __RegisterSkill(self):

		race = net.GetMainActorRace()
		group = net.GetMainActorSkillGroup()
		empire = net.GetMainActorEmpire()

		playerSettingModule.RegisterSkill(race, group, empire)

	def __RegisterTitleName(self):
		for i in xrange(len(localeInfo.TITLE_NAME_LIST)):
			chrmgr.RegisterTitleName(i, localeInfo.TITLE_NAME_LIST[i])

	def __RegisterColor(self):

		## Name
		NAME_COLOR_DICT = {
			chrmgr.NAMECOLOR_PC : colorInfo.CHR_NAME_RGB_PC,
			chrmgr.NAMECOLOR_NPC : colorInfo.CHR_NAME_RGB_NPC,
			chrmgr.NAMECOLOR_MOB : colorInfo.CHR_NAME_RGB_MOB,
			chrmgr.NAMECOLOR_PVP : colorInfo.CHR_NAME_RGB_PVP,
			chrmgr.NAMECOLOR_PK : colorInfo.CHR_NAME_RGB_PK,
			chrmgr.NAMECOLOR_PARTY : colorInfo.CHR_NAME_RGB_PARTY,
			chrmgr.NAMECOLOR_WARP : colorInfo.CHR_NAME_RGB_WARP,
			chrmgr.NAMECOLOR_WAYPOINT : colorInfo.CHR_NAME_RGB_WAYPOINT,

			chrmgr.NAMECOLOR_EMPIRE_MOB : colorInfo.CHR_NAME_RGB_EMPIRE_MOB,
			chrmgr.NAMECOLOR_EMPIRE_NPC : colorInfo.CHR_NAME_RGB_EMPIRE_NPC,
			chrmgr.NAMECOLOR_EMPIRE_PC+1 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_A,
			chrmgr.NAMECOLOR_EMPIRE_PC+2 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_B,
			chrmgr.NAMECOLOR_EMPIRE_PC+3 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_C,
		}
		for name, rgb in NAME_COLOR_DICT.items():
			chrmgr.RegisterNameColor(name, rgb[0], rgb[1], rgb[2])

		## Title
		TITLE_COLOR_DICT = (	colorInfo.TITLE_RGB_GOOD_4,
								colorInfo.TITLE_RGB_GOOD_3,
								colorInfo.TITLE_RGB_GOOD_2,
								colorInfo.TITLE_RGB_GOOD_1,
								colorInfo.TITLE_RGB_NORMAL,
								colorInfo.TITLE_RGB_EVIL_1,
								colorInfo.TITLE_RGB_EVIL_2,
								colorInfo.TITLE_RGB_EVIL_3,
								colorInfo.TITLE_RGB_EVIL_4,	)
		count = 0
		for rgb in TITLE_COLOR_DICT:
			chrmgr.RegisterTitleColor(count, rgb[0], rgb[1], rgb[2])
			count += 1

	def __RegisterEmotionIcon(self):
		emotion.RegisterEmotionIcons()

	def __LoadMap(self):
		net.Warp(self.playerX, self.playerY)

	def __LoadSound(self):
		playerSettingModule.LoadGameData("SOUND")

	def __LoadEffect(self):
		playerSettingModule.LoadGameData("EFFECT")

	## MOBIL NOT (2026-09-24): ilk giriste 9.7 s yuklemenin 7.5 s'i 8 irkin ~1000 hareket dosyasinin onden
	## okunmasi (RegisterCacheMotionData). "Yalniz kendi irk onden, digerleri ilk kullanimda" sarmalayicisi denendi
	## (3.5 s, olculdu), KULLANICI KARARI ile geri alindi: "eski client neyse onu yap". Asagisi gercek client ile BIREBIR.
	## MOBIL (2026-09-24, ANR): logcat "Input dispatching timed out ... Waited 5000ms for MotionEvent" - yukleme sirasinda
	## ekrana dokununca Android 5 s icinde yanit alamayip oyunu kapatti (irk adimlari 1.9-3.0 s, sistem yuku altinda daha
	## uzun; dokunma olaylari yalniz kareler arasinda islenir). Cozum, kaynaktaki yuklemeyi DEGISTIRMEDEN: her irk adimi
	## kaynaktaki iki yarisina (erkek/kadin, ayni fonksiyonlar, ayni sira) bolunur ve yarilar ayri karelerde calisir ->
	## en uzun kesinti yariya iner, dokunma olaylari arada islenir. loadGameDataDict (bir kez yukle) korunur.
	MOBILE_RACE_HALVES = {
		"WARRIOR":  ("__LoadGameWarriorEx",  (("RACE_WARRIOR_M",  "d:/ymir work/pc/warrior/"),  ("RACE_WARRIOR_W",  "d:/ymir work/pc2/warrior/"))),
		"ASSASSIN": ("__LoadGameAssassinEx", (("RACE_ASSASSIN_W", "d:/ymir work/pc/assassin/"), ("RACE_ASSASSIN_M", "d:/ymir work/pc2/assassin/"))),
		"SURA":     ("__LoadGameSuraEx",     (("RACE_SURA_M",     "d:/ymir work/pc/sura/"),     ("RACE_SURA_W",     "d:/ymir work/pc2/sura/"))),
		"SHAMAN":   ("__LoadGameShamanEx",   (("RACE_SHAMAN_W",   "d:/ymir work/pc/shaman/"),   ("RACE_SHAMAN_M",   "d:/ymir work/pc2/shaman/"))),
	}

	def __MobileRaceHalf(self, name, half):
		P = playerSettingModule
		(fnName, halves) = self.MOBILE_RACE_HALVES[name]
		fn = getattr(P, fnName, None)
		(raceConst, path) = halves[half]
		race = getattr(P, raceConst, None)
		if fn is None or race is None or not hasattr(P, "loadGameDataDict"):
			if half == 0:
				P.LoadGameData(name)	# beklenmedik surum: birebir eski yol
			return
		if not P.loadGameDataDict.get(name, 0):
			return					# bu surecte zaten yuklendi (kaynaktaki LoadGameData kurali)
		fn(race, path)
		if half == 1:
			P.loadGameDataDict[name] = 0

	def __LoadWarriorA(self):
		self.__MobileRaceHalf("WARRIOR", 0)

	def __LoadAssassinA(self):
		self.__MobileRaceHalf("ASSASSIN", 0)

	def __LoadSuraA(self):
		self.__MobileRaceHalf("SURA", 0)

	def __LoadShamanA(self):
		self.__MobileRaceHalf("SHAMAN", 0)

	def __LoadWarrior(self):
		self.__MobileRaceHalf("WARRIOR", 1)

	def __LoadAssassin(self):
		self.__MobileRaceHalf("ASSASSIN", 1)

	def __LoadSura(self):
		self.__MobileRaceHalf("SURA", 1)

	def __LoadShaman(self):
		self.__MobileRaceHalf("SHAMAN", 1)

	def __LoadSkill(self):
		playerSettingModule.LoadGameData("SKILL")

	def __LoadEnemy(self):
		playerSettingModule.LoadGameData("ENEMY")

	def __LoadNPC(self):
		playerSettingModule.LoadGameData("NPC")

	# GUILD_BUILDING
	def __LoadGuildBuilding(self):
		playerSettingModule.LoadGuildBuildingList(localeInfo.GUILD_BUILDING_LIST_TXT)
	# END_OF_GUILD_BUILDING

	def __StartGame(self):
		background.SetViewDistanceSet(background.DISTANCE0, 25600)
		"""
		background.SetViewDistanceSet(background.DISTANCE1, 19200)
		background.SetViewDistanceSet(background.DISTANCE2, 12800)
		background.SetViewDistanceSet(background.DISTANCE3, 9600)
		background.SetViewDistanceSet(background.DISTANCE4, 6400)
		"""
		background.SelectViewDistanceNum(background.DISTANCE0)

		app.SetGlobalCenterPosition(self.playerX, self.playerY)

		net.StartGame()
