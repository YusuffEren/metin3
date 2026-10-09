# MOBIL KAPLAMA (mobile_root/uimessenger.py): pack root/uimessenger.py kopyasi. KULLANICI (2026-09-15):
# arkadas listesi PC "Topluluk" penceresi gibi: ad yaninda (Sv. N), online YESIL / offline KIRMIZI kare,
# konum dugmesi -> arkadasin bulundugu haritanin adi. Seviye/harita sunucu paketinde YOK (messenger paketi
# yalniz ad + online); sunucudaki friends.tsv (15 sn'de bir player.player'dan) arka plan is parcaciginda okunur.
import math
import wndMgr
import threading
import urllib2

MOBILE_INFO_URL = "http://185.169.55.31/averos2/friends.tsv"
## v78 (2026-10-08): friends.tsv DINAMIK (sunucu 15 sn'de bir yazar) -> R2'de (dl.averos2.com) YOK, oyun sunucusundaki
## darkhttpd'de. Yeni APK (app.HOSTNAME_DESTEK) once ADLA (oyun.averos2.com), olmazsa IP; ad bir kez basarisiz
## olursa oturumda IP one gecer. Eski APK yalniz IP (davranis ayni).
MOBILE_INFO_URL_AD = "http://oyun.averos2.com/averos2/friends.tsv"
_MOBILE_INFO_SIRA = []

def _MobileInfoUrls():
	if not _MOBILE_INFO_SIRA:
		try:
			import app
			ad = getattr(app, "HOSTNAME_DESTEK", 0)
		except:
			ad = 0
		_MOBILE_INFO_SIRA.extend((MOBILE_INFO_URL_AD, MOBILE_INFO_URL) if ad else (MOBILE_INFO_URL,))
	return list(_MOBILE_INFO_SIRA)

def _MobileInfoOku():
	"""sirayla dener; calisan adres oturumda one alinir. Hepsi basarisizsa son hatayi firlatir."""
	son = None
	for url in _MobileInfoUrls():
		try:
			data = urllib2.urlopen(url, timeout=6).read()
		except Exception, e:
			son = e
			continue
		if _MOBILE_INFO_SIRA and _MOBILE_INFO_SIRA[0] != url and url in _MOBILE_INFO_SIRA:
			_MOBILE_INFO_SIRA.remove(url)
			_MOBILE_INFO_SIRA.insert(0, url)
		return data
	raise son or IOError("friends.tsv")
MOBILE_INFO_PERIOD = 20.0	# saniye (pencere acikken)
MOBILE_ROW_H = 30
MOBILE_ROW_H2 = 48	# konum satiri acikken

MOBILE_MAP_NAMES = {
	1:"K\xfdrm\xfdz\xfd 1.K\xf6y", 3:"K\xfdrm\xfdz\xfd 2.K\xf6y", 21:"Sar\xfd 1.K\xf6y", 23:"Sar\xfd 2.K\xf6y",
	41:"Mavi 1.K\xf6y", 43:"Mavi 2.K\xf6y", 4:"Lonca Alan\xfd", 24:"Lonca Alan\xfd", 44:"Lonca Alan\xfd",
	5:"Maymun Zindan\xfd 1", 25:"Maymun Zindan\xfd 1", 45:"Maymun Zindan\xfd 1", 27:"Bal\xfdk\xe7\xfd Haritas\xfd",
	61:"Sohan Da\xf0\xfd", 62:"Doyyumhwan", 63:"Yongbi \xc7\xf6l\xfc", 64:"Seungryong Vadisi", 65:"Tap\xfdnak",
	66:"\xdeeytan Kulesi", 67:"Hayalet Orman", 68:"K\xfdz\xfdl Orman", 69:"Kurt Vadisi", 70:"Devler Diyar\xfd",
	71:"\xd6r\xfcmcek Zindan\xfd 2", 72:"S\xfcrg\xfcn Ma\xf0aras\xfd 1", 73:"S\xfcrg\xfcn Ma\xf0aras\xfd 2",
	81:"D\xfc\xf0\xfcn Salonu", 103:"Boss Zindan\xfd", 104:"\xd6r\xfcmcek Zindan\xfd", 108:"Maymun Zindan\xfd 2",
	109:"Maymun Zindan\xfd 3", 112:"D\xfcello Arenas\xfd", 113:"OX Etkinli\xf0i", 200:"Etkinlik Haritas\xfd",
	208:"S\xfcrg\xfcn Ma\xf0aras\xfd Boss", 216:"\xdeeytan Katakombu", 217:"\xd6r\xfcmcek Zindan\xfd 3",
	301:"Ejderha Burnu", 302:"\xdeafak Sisi Orman\xfd", 303:"Kara Kum Koyu", 304:"G\xf6k G\xfcr\xfclt\xfcs\xfc Da\xf0\xfd",
	351:"Alev Zindan\xfd", 352:"Kar Zindan\xfd",
}

def MobileMapName(idx):
	try:
		idx = int(idx)
	except:
		return "?"
	base = idx
	if idx >= 10000:
		base = idx % 10000	# zindan kopyalari (dungeon instance)
	return MOBILE_MAP_NAMES.get(base, "Harita %d" % idx)

class MobileFriendInfo:
	"""friends.tsv -> {ad: (seviye, harita)}; okuma arka plan is parcaciginda, sonuc ana dongude alinir."""
	def __init__(self):
		self.info = {}
		self.pending = None
		self.busy = False
		self.lastFetch = 0.0
		self.version = 0
	def Fetch(self):
		if self.busy:
			return
		self.busy = True
		self.lastFetch = app.GetGlobalTimeStamp()
		t = threading.Thread(target=self.__Worker)
		t.setDaemon(True)
		t.start()
	def __Worker(self):
		try:
			data = _MobileInfoOku()
			d = {}
			for line in data.split("\n"):
				p = line.rstrip("\r").split("\t")
				if len(p) >= 3:
					d[p[0]] = (p[1], p[2])
			self.pending = d
		except:
			self.pending = None
		self.busy = False
	def Poll(self):
		"""ana dongu: yeni veri geldiyse uygula, True doner"""
		if self.pending is None:
			return False
		self.info = self.pending
		self.pending = None
		self.version += 1
		return True
	def Get(self, name):
		return self.info.get(name)

MOBILE_FRIEND_INFO = MobileFriendInfo()

import app
import ui
import grp
import net
import guild
import messenger
import localeInfo
import constInfo
import uiToolTip
import uiGameOption

import uiCommon
from _weakref import proxy

FRIEND = 0
GUILD = 1

class MessengerItem(ui.Window):

	def __init__(self, getParentEvent):
		ui.Window.__init__(self)

		self.SetParent(getParentEvent())
		self.AddFlag("float")

		self.name = ""
		self.image = ui.ImageBox()
		self.image.AddFlag("not_pick")
		self.image.SetParent(self)
		self.image.Show()
		self.text = ui.TextLine()
		self.text.SetParent(self)
		self.text.SetPosition(20, 2)
		self.text.Show()
		self.mobileRowW = 200	# MOBIL: satir genisligi (pencere - kenarlar), MessengerWindow verir

		self.lovePoint = -1
		self.lovePointToolTip = None

		self.isSelected = False

		self.getParentEvent = getParentEvent

	def SetName(self, name):
		self.name = name
		if name:
			self.text.SetText(name)
			self.SetSize(self.mobileRowW, 20)	# MOBIL: satir tam genislik (dokunmasi kolay)

			if localeInfo.IsARABIC():
				self.text.SetPosition(20 + 6*len(name) + 4, 2)

	def SetLovePoint(self, lovePoint):
		self.lovePoint = lovePoint

	def Select(self):
		self.isSelected = True

	def UnSelect(self):
		self.isSelected = False

	def GetName(self):
		return self.name

	def GetStepWidth(self):
		return 0

	# Whisper
	def CanWhisper(self):
		return False

	def IsOnline(self):
		return False

	def IsMobile(self):
		return False

	def OnWhisper(self):
		pass

	def OnMobileMessage(self):
		pass

	# Remove
	def CanRemove(self):
		return False

	def OnRemove(self):
		return False

	# Warp
	def CanWarp(self):
		return False

	def OnWarp(self):
		pass

	def OnMouseOverIn(self):
		if -1 != self.lovePoint:
			if not self.lovePointToolTip:
				self.lovePointToolTip = uiToolTip.ToolTip(100)
				self.lovePointToolTip.SetTitle(self.name)
				self.lovePointToolTip.AppendTextLine(localeInfo.AFF_LOVE_POINT % (self.lovePoint))
				self.lovePointToolTip.ResizeToolTip()
			self.lovePointToolTip.ShowToolTip()

	def OnMouseOverOut(self):
		if self.lovePointToolTip:
			self.lovePointToolTip.HideToolTip()

	def OnMouseLeftButtonDown(self):
		self.getParentEvent().OnSelectItem(self)

	def OnMouseLeftButtonDoubleClick(self):
		self.getParentEvent().OnDoubleClickItem(self)

	def OnRender(self):
		if self.isSelected:
			x, y = self.GetGlobalPosition()
			grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.7, 0.7))
			grp.RenderBar(x, y, self.GetWidth(), self.GetHeight())

class MessengerMemberItem(MessengerItem):

	STATE_OFFLINE = 0
	STATE_ONLINE = 1
	STATE_MOBILE = 2

	IMAGE_FILE_NAME = {	"ONLINE" : "d:/ymir work/ui/game/windows/messenger_list_online.sub",
						"OFFLINE" : "d:/ymir work/ui/game/windows/messenger_list_offline.sub",
						"MOBILE" : "d:/ymir work/ui/game/windows/messenger_list_mobile.sub", }

	def __init__(self, getParentEvent):
		MessengerItem.__init__(self, getParentEvent)
		self.key = None
		self.state = self.STATE_OFFLINE
		self.mobileFlag = False
		## MOBIL: online/offline simgesi yerine renkli kare (OnRender), ad yaninda seviye, sagda konum dugmesi
		self.image.Hide()
		## KULLANICI: yuvarlak nokta; online yesil + nefes alan hale (OnUpdate), offline kirmizi
		self.glow = ui.ExpandedImageBox()
		self.glow.SetParent(self)
		self.glow.AddFlag("not_pick")
		self.glow.LoadImage("mobile/ui/msg_dot_glow.tga")
		self.glow.Hide()
		self.dot = ui.ExpandedImageBox()
		self.dot.SetParent(self)
		self.dot.AddFlag("not_pick")
		self.dot.LoadImage("mobile/ui/msg_dot_red.tga")
		self.dot.SetPosition(4, 9)
		self.dot.Show()
		self.text.SetPosition(22, 8)
		self.lvText = ui.TextLine()
		self.lvText.SetParent(self)
		self.lvText.SetFontColor(0.35, 0.95, 0.35)
		self.lvText.Show()
		self.mapText = ui.TextLine()
		self.mapText.SetParent(self)
		self.mapText.SetPosition(22, 28)
		self.mapText.SetFontColor(0.95, 0.85, 0.45)
		self.mapText.Hide()
		self.mapOpen = False
		self.pinButton = ui.Button()
		self.pinButton.SetParent(self)
		self.pinButton.SetUpVisual("mobile/ui/msg_pin_up.tga")
		self.pinButton.SetOverVisual("mobile/ui/msg_pin_down.tga")
		self.pinButton.SetDownVisual("mobile/ui/msg_pin_down.tga")
		self.pinButton.SetEvent(ui.__mem_func__(self.OnMobileTogglePin))
		self.pinButton.Show()
		self.Offline()

	def GetStepWidth(self):
		return 15

	## MOBIL ------------------------------------------------------------------
	def SetName(self, name):
		MessengerItem.SetName(self, name)
		self.MobileLayout()

	def MobileLayout(self):
		h = self.mapOpen and MOBILE_ROW_H2 or MOBILE_ROW_H
		self.SetSize(self.mobileRowW, h)
		self.lvText.SetPosition(22 + self.text.GetTextSize()[0] + 6, 8)
		self.pinButton.SetPosition(self.mobileRowW - self.pinButton.GetWidth() - 2, 1)
		if self.mapOpen:
			self.mapText.Show()
		else:
			self.mapText.Hide()

	def MobileApplyInfo(self):
		info = MOBILE_FRIEND_INFO.Get(self.name)
		if info:
			self.lvText.SetText("(Sv. %s)" % info[0])
			if self.IsOnline():
				self.mapText.SetText("Konum: " + MobileMapName(info[1]))
			else:
				self.mapText.SetText("Son konum: " + MobileMapName(info[1]) + " (\xe7evrimd\xfd\xfe\xfd)")
		else:
			self.lvText.SetText("")
			self.mapText.SetText("Konum: bilinmiyor")
		self.MobileLayout()

	def OnMobileTogglePin(self):
		self.mapOpen = not self.mapOpen
		self.MobileApplyInfo()
		self.getParentEvent().OnRefreshList()

	def MobileSetDot(self):
		if self.IsOnline():
			self.dot.LoadImage("mobile/ui/msg_dot_green.tga")
			self.glow.Show()
		else:
			self.dot.LoadImage("mobile/ui/msg_dot_red.tga")
			self.glow.Hide()

	def OnUpdate(self):
		if not self.glow.IsShow():
			return
		## hafif nefes: 2.4 sn periyot, olcek 0.8-1.15, alpha 0.25-0.75
		w = 0.5 + 0.5 * math.sin(app.GetGlobalTime() * 0.0026)
		sc = 0.8 + 0.35 * w
		self.glow.SetScale(sc, sc)
		gw = 32 * sc
		self.glow.SetPosition(int(4 + 7 - gw / 2), int(9 + 7 - gw / 2))
		if hasattr(wndMgr, "SetDiffuseColor"):
			wndMgr.SetDiffuseColor(self.glow.hWnd, 1.0, 1.0, 1.0, 0.25 + 0.5 * w)
	## ----------------------------------------------------------------------

	def SetKey(self, key):
		self.key = key

	def IsSameKey(self, key):
		return self.key == key

	def IsOnline(self):
		if self.STATE_ONLINE == self.state:
			return True

		return False

	def IsMobile(self):
		if self.STATE_MOBILE == self.state:
			return True

		return False

	def Online(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["ONLINE"])
		self.state = self.STATE_ONLINE
		self.MobileSetDot()

	def Offline(self):
		if self.mobileFlag:
			self.image.LoadImage(self.IMAGE_FILE_NAME["MOBILE"])
			self.state = self.STATE_MOBILE

		else:
			self.image.LoadImage(self.IMAGE_FILE_NAME["OFFLINE"])
			self.state = self.STATE_OFFLINE
		self.MobileSetDot()

	def SetMobile(self, flag):
		self.mobileFlag = flag

		if not self.IsOnline():
			self.Offline()

	def CanWhisper(self):
		if self.IsOnline():
			return True

		return False

	def OnWhisper(self):
		if self.IsOnline():
			self.getParentEvent().whisperButtonEvent(self.GetName())

	def OnMobileMessage(self):
		if not uiGameOption.MOBILE:
			return

		if not self.IsMobile():
			return

		self.getParentEvent().SendMobileMessage(self.GetName())

	def Select(self):
		MessengerItem.Select(self)

class MessengerGroupItem(MessengerItem):

	IMAGE_FILE_NAME = {	"OPEN" : "d:/ymir work/ui/game/windows/messenger_list_open.sub",
						"CLOSE" : "d:/ymir work/ui/game/windows/messenger_list_close.sub", }

	def __init__(self, getParentEvent):
		self.isOpen = False
		self.memberList = []

		MessengerItem.__init__(self, getParentEvent)

	def AppendMember(self, member, key, name):
		member.SetKey(key)
		member.SetName(name)
		self.memberList.append(member)
		return member

	def RemoveMember(self, item):
		for i in xrange(len(self.memberList)):
			if item == self.memberList[i]:
				del self.memberList[i]
				return

	def ClearMember(self):
		self.memberList = []

	def FindMember(self, key):
		list = filter(lambda argMember, argKey=key: argMember.IsSameKey(argKey), self.memberList)
		if list:
			return list[0]

		return None

	def GetLoginMemberList(self):
		return filter(MessengerMemberItem.IsOnline, self.memberList)

	def GetLogoutMemberList(self):
		return filter(lambda arg: not arg.IsOnline(), self.memberList)

	def IsOpen(self):
		return self.isOpen

	def Open(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["OPEN"])
		self.isOpen = True

	def Close(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["CLOSE"])
		self.isOpen = False

		map(ui.Window.Hide, self.memberList)

	def Select(self):

		if self.IsOpen():
			self.Close()
		else:
			self.Open()

		MessengerItem.Select(self)
		self.getParentEvent().OnRefreshList()

class MessengerFriendItem(MessengerMemberItem):

	def __init__(self, getParentEvent):
		MessengerMemberItem.__init__(self, getParentEvent)

	def CanRemove(self):
		return True

	def OnRemove(self):
		messenger.RemoveFriend(self.key)
		net.SendMessengerRemovePacket(self.key, self.name)
		return True

class MessengerGuildItem(MessengerMemberItem):

	def __init__(self, getParentEvent):
		MessengerMemberItem.__init__(self, getParentEvent)

	def CanWarp(self):
		if not self.IsOnline():
			return False
		return True

	def OnWarp(self):
		net.SendGuildUseSkillPacket(155, self.key)

	def CanRemove(self):
		for i in xrange(guild.ENEMY_GUILD_SLOT_MAX_COUNT):
			if guild.GetEnemyGuildName(i) != "":
				return False

		if guild.MainPlayerHasAuthority(guild.AUTH_REMOVE_MEMBER):
			if guild.IsMemberByName(self.name):
				return True

		return False

	def OnRemove(self):
		net.SendGuildRemoveMemberPacket(self.key)
		return True

class MessengerFriendGroup(MessengerGroupItem):

	def __init__(self, getParentEvent):
		MessengerGroupItem.__init__(self, getParentEvent)
		self.SetName(localeInfo.MESSENGER_FRIEND)

	def AppendMember(self, key, name):
		item = MessengerFriendItem(self.getParentEvent)
		return MessengerGroupItem.AppendMember(self, item, key, name)

class MessengerGuildGroup(MessengerGroupItem):

	def __init__(self, getParentEvent):
		MessengerGroupItem.__init__(self, getParentEvent)
		self.SetName(localeInfo.MESSENGER_GUILD)
		self.AddFlag("float")

	def AppendMember(self, key, name):
		item = MessengerGuildItem(self.getParentEvent)
		return MessengerGroupItem.AppendMember(self, item, key, name)

class MessengerFamilyGroup(MessengerGroupItem):

	def __init__(self, getParentEvent):
		MessengerGroupItem.__init__(self, getParentEvent)
		self.SetName(localeInfo.MESSENGER_FAMILY)
		self.AddFlag("float")

		self.lover = None

	def AppendMember(self, key, name):
		item = MessengerGuildItem(self.getParentEvent)
		self.lover = item
		return MessengerGroupItem.AppendMember(self, item, key, name)

	def GetLover(self):
		return self.lover

###################################################################################################
###################################################################################################
###################################################################################################

class MessengerWindow(ui.ScriptWindow):

	START_POSITION = 40

	class ResizeButton(ui.DragButton):

		def OnMouseOverIn(self):
			app.SetCursor(app.VSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		messenger.SetMessengerHandler(self)

		self.board = None
		self.groupList = []
		self.showingItemList = []
		self.selectedItem = None
		self.whisperButtonEvent = lambda *arg: None
		self.familyGroup = None

		self.guildButtonEvent = None

		self.showingPageSize = 0
		self.startLine = 0
		self.hasMobilePhoneNumber = True

		self.isLoaded = 0

		self.__AddGroup()
		messenger.RefreshGuildMember()

	def Show(self):
		if self.isLoaded==0:
			self.isLoaded=1

			self.__LoadWindow()
			self.OnRefreshList()
			self.OnResizeDialog()

		ui.ScriptWindow.Show(self)
		MOBILE_FRIEND_INFO.Fetch()	# MOBIL

	def OnUpdate(self):
		## MOBIL: arka planda gelen seviye/harita bilgisini uygula, pencere acikken periyodik yenile
		if MOBILE_FRIEND_INFO.Poll():
			for group in self.groupList:
				for m in group.memberList:
					m.MobileApplyInfo()
			if self.familyGroup and self.familyGroup.GetLover():
				self.familyGroup.GetLover().MobileApplyInfo()
			self.OnRefreshList()
		elif app.GetGlobalTimeStamp() - MOBILE_FRIEND_INFO.lastFetch > MOBILE_INFO_PERIOD:
			MOBILE_FRIEND_INFO.Fetch()

	def __LoadWindow(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "UIScript/MessengerWindow.py")		

		try:
			self.board = self.GetChild("board")
			self.scrollBar = self.GetChild("ScrollBar")
			self.whisperButton = self.GetChild("WhisperButton")
			self.mobileButton = self.GetChild("MobileButton")
			self.removeButton = self.GetChild("RemoveButton")
			self.addFriendButton = self.GetChild("AddFriendButton")
			self.guildButton = self.GetChild("GuildButton")
		except:
			import exception
			exception.Abort("MessengerWindow.__LoadWindow.__Bind")

		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.whisperButton.SetEvent(ui.__mem_func__(self.OnPressWhisperButton))
		self.mobileButton.SetEvent(ui.__mem_func__(self.OnPressMobileButton))
		self.removeButton.SetEvent(ui.__mem_func__(self.OnPressRemoveButton))
		self.addFriendButton.SetEvent(ui.__mem_func__(self.OnPressAddFriendButton))
		self.guildButton.SetEvent(ui.__mem_func__(self.OnPressGuildButton))

		if not uiGameOption.MOBILE: #constInfo.SEND_MOBILE_PHONE_MESSAGE_ENABLE:
			self.mobileButton.Hide()
			width = self.GetWidth()
			height = self.GetHeight()
			self.addFriendButton.SetPosition(-60, 30)
			self.whisperButton.SetPosition(-20, 30)
			self.removeButton.SetPosition(20, 30)
			self.guildButton.SetPosition(60, 30)

		self.whisperButton.Disable()
		self.mobileButton.Disable()
		self.removeButton.Disable()

		resizeButton = self.ResizeButton()
		resizeButton.AddFlag("restrict_x")
		resizeButton.SetParent(self)
		resizeButton.SetSize(self.GetWidth(), 10)
		resizeButton.SetWindowVerticalAlignBottom()
		resizeButton.SetPosition(0, 0)
		resizeButton.Show()
		self.resizeButton = resizeButton
		self.resizeButton.SetMoveEvent(ui.__mem_func__(self.OnResizeDialog))
		self.resizeButton.SetPosition(0, 380)	# MOBIL: daha uzun liste

		for list in self.groupList:
			list.SetTop()

	def __del__(self):
		messenger.SetMessengerHandler(None)
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.board = None
		self.scrollBar = None
		self.resizeButton = None
		self.friendNameBoard = None
		self.questionDialog = None
		self.popupDialog = None
		self.inputDialog = None
		self.familyGroup = None

		self.whisperButton = None
		self.mobileButton = None
		self.removeButton = None

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def Close(self):
		self.questionDialog = None
		self.Hide()

	def SetSize(self, width, height):
		ui.ScriptWindow.SetSize(self, width, height)
		if self.board:
			self.board.SetSize(width, height)

	def OnResizeDialog(self):
		x, y = self.resizeButton.GetLocalPosition()
		if y < 140:
			self.resizeButton.SetPosition(x, 140)
			return
		self.SetSize(self.GetWidth(), y + self.resizeButton.GetHeight())

		self.showingPageSize = y - (self.START_POSITION + 26)
		self.scrollBar.SetScrollBarSize(self.showingPageSize)

		self.__LocateMember()

		self.resizeButton.TurnOffCallBack()
		self.UpdateRect()
		self.resizeButton.TurnOnCallBack()

	def __LocateMember(self):

		if self.isLoaded==0:
			return

		for item in self.showingItemList:	# MOBIL: satir genisligi pencereye gore
			item.mobileRowW = self.GetWidth() - 48 - item.GetStepWidth()
			if isinstance(item, MessengerMemberItem):
				item.MobileLayout()
			else:
				item.SetSize(item.mobileRowW, 20)
		if self.showingPageSize/20 >= len(self.showingItemList):
			self.scrollBar.Hide()
			self.startLine = 0
		else:
			if self.showingItemList:
				self.scrollBar.SetMiddleBarSize(float(self.showingPageSize/20) / float(len(self.showingItemList)))
			self.scrollBar.Show()

		#####

		yPos = self.START_POSITION
		heightLimit = self.GetHeight() - (self.START_POSITION + 13)

		map(ui.Window.Hide, self.showingItemList)

		for item in self.showingItemList[self.startLine:]:
			item.SetPosition(20 + item.GetStepWidth(), yPos)
			item.SetTop()
			item.Show()

			yPos += item.GetHeight() + 2	# MOBIL: satir yuksekligi degisken
			if yPos > heightLimit:
				break

	def __AddGroup(self):
		member = MessengerFriendGroup(ui.__mem_func__(self.GetSelf))
		member.Open()
		member.Show()
		self.groupList.append(member)

		member = MessengerGuildGroup(ui.__mem_func__(self.GetSelf))
		member.Open()
		member.Show()
		self.groupList.append(member)

	def __AddFamilyGroup(self):
		member = MessengerFamilyGroup(ui.__mem_func__(self.GetSelf))
		member.Open()
		member.Show()

		self.familyGroup = member

	def ClearGuildMember(self):
		self.groupList[GUILD].ClearMember()

	def SetWhisperButtonEvent(self, event):
		self.whisperButtonEvent=event

	def SetGuildButtonEvent(self, event):
		self.guildButtonEvent=event

	def SendMobileMessage(self, name):
		if not uiGameOption.MOBILE:
			return

		if not self.hasMobilePhoneNumber:
			questionDialog = uiCommon.QuestionDialog2()
			questionDialog.SetText1(localeInfo.MESSENGER_INPUT_MOBILE_PHONE_NUMBER_1)
			questionDialog.SetText2(localeInfo.MESSENGER_INPUT_MOBILE_PHONE_NUMBER_2)
			questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnAcceptInputMobilePhoneNumber))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCancelInputMobilePhoneNumber))
			questionDialog.SetWidth(400)
			questionDialog.Open()
			self.questionDialog = questionDialog
			return

		## Input Sending Mobile Message
		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.MESSENGER_SEND_MOBILE_MESSAGE_TITLE)
		inputDialog.SetMaxLength(50)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OnInputMobileMessage))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseInputDialog))
		inputDialog.name = name
		inputDialog.Open()
		self.inputDialog = inputDialog

	def OnAcceptInputMobilePhoneNumber(self):
		if not uiGameOption.MOBILE:
			return

		## Input Mobile Phone Number
		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.MESSENGER_INPUT_MOBILE_PHONE_NUMBER_TITLE)
		inputDialog.SetMaxLength(13)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OnInputMobilePhoneNumber))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseInputDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog
		self.OnCancelInputMobilePhoneNumber()

	def OnCancelInputMobilePhoneNumber(self):
		if not uiGameOption.MOBILE:
			return
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def OnInputMobilePhoneNumber(self):
		if not uiGameOption.MOBILE:
			return

		text = self.inputDialog.GetText()

		if not text:
			return

		text.replace('-', '')
		net.SendChatPacket("/mobile " + text)
		self.OnCloseInputDialog()
		return True

	def OnInputMobileMessage(self):
		if not uiGameOption.MOBILE:
			return

		text = self.inputDialog.GetText()

		if not text:
			return

		net.SendMobileMessagePacket(self.inputDialog.name, text)
		self.OnCloseInputDialog()
		return True

	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnPressGuildButton(self):
		self.guildButtonEvent()

	def OnPressAddFriendButton(self):
		friendNameBoard = uiCommon.InputDialog()
		friendNameBoard.SetTitle(localeInfo.MESSENGER_ADD_FRIEND)
		friendNameBoard.SetAcceptEvent(ui.__mem_func__(self.OnAddFriend))
		friendNameBoard.SetCancelEvent(ui.__mem_func__(self.OnCancelAddFriend))
		friendNameBoard.Open()
		self.friendNameBoard = friendNameBoard

	def OnAddFriend(self):
		text = self.friendNameBoard.GetText()
		if text:
			net.SendMessengerAddByNamePacket(text)
		self.friendNameBoard.Close()
		self.friendNameBoard = None
		return True

	def OnCancelAddFriend(self):
		self.friendNameBoard.Close()
		self.friendNameBoard = None
		return True

	def OnPressWhisperButton(self):
		if self.selectedItem:
			self.selectedItem.OnWhisper()

	def OnPressMobileButton(self):
		if self.selectedItem:
			self.selectedItem.OnMobileMessage()

	def OnPressRemoveButton(self):
		if self.selectedItem:
			if self.selectedItem.CanRemove():
				self.questionDialog = uiCommon.QuestionDialog()
				self.questionDialog.SetText(localeInfo.MESSENGER_DO_YOU_DELETE)
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnRemove))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
				self.questionDialog.Open()

	def OnRemove(self):
		if self.selectedItem:
			if self.selectedItem.CanRemove():
				map(lambda arg, argDeletingItem=self.selectedItem: arg.RemoveMember(argDeletingItem), self.groupList)
				self.selectedItem.OnRemove()
				self.selectedItem.UnSelect()
				self.selectedItem = None
				self.OnRefreshList()

		self.OnCloseQuestionDialog()

	def OnScroll(self):
		scrollLineCount = len(self.showingItemList) - (self.showingPageSize/20)
		startLine = int(scrollLineCount * self.scrollBar.GetPos())

		if startLine != self.startLine:
			self.startLine = startLine
			self.__LocateMember()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	## CallBack
	def OnSelectItem(self, item):

		if self.selectedItem:
			if item != self.selectedItem:
				self.selectedItem.UnSelect()

		self.selectedItem = item

		if self.selectedItem:
			self.selectedItem.Select()

			if self.selectedItem.CanWhisper():
				self.whisperButton.Enable()
			else:
				self.whisperButton.Disable()

			if self.selectedItem.IsMobile():
				self.mobileButton.Enable()
			else:
				self.mobileButton.Disable()

			if self.selectedItem.CanRemove():
				self.removeButton.Enable()
			else:
				self.removeButton.Disable()

	def OnDoubleClickItem(self, item):

		if not self.selectedItem:
			return

		if self.selectedItem.IsOnline():
			self.OnPressWhisperButton()

		elif self.selectedItem.IsMobile():
			self.OnPressMobileButton()

	def GetSelf(self):
		return self

	def OnRefreshList(self):
		self.showingItemList = []

		if self.familyGroup:
			self.showingItemList.append(self.familyGroup)
			if self.familyGroup.GetLover():
				self.showingItemList.append(self.familyGroup.GetLover())

		for group in self.groupList:

			self.showingItemList.append(group)

			if group.IsOpen():

				loginMemberList = group.GetLoginMemberList()
				logoutMemberList = group.GetLogoutMemberList()

				if loginMemberList or logoutMemberList:
					for member in loginMemberList:
						self.showingItemList.append(member)
					for member in logoutMemberList:
						self.showingItemList.append(member)

				else:
					item = MessengerItem(ui.__mem_func__(self.GetSelf))
					item.SetName(localeInfo.MESSENGER_EMPTY_LIST)
					self.showingItemList.append(item)

		self.__MobileFitHeight()	# MOBIL: pencere icerik kadar
		self.__LocateMember()

	def __MobileFitHeight(self):
		## KULLANICI (2026-09-15): pencere icerige gore boyutlansin, bosluk kalmasin
		if self.isLoaded == 0:
			return
		total = 0
		for item in self.showingItemList:
			if isinstance(item, MessengerMemberItem):
				total += (item.mapOpen and MOBILE_ROW_H2 or MOBILE_ROW_H) + 2
			else:
				total += 22
		## KULLANICI: en fazla 10 arkadas + 2 grup basligi gorunur, sonrasi kaydirma cubugu
		hMax = self.START_POSITION + 2 * 22 + 10 * (MOBILE_ROW_H + 2) + 92
		h = max(230, min(hMax, self.START_POSITION + total + 92))
		y = h - self.resizeButton.GetHeight()
		if self.resizeButton.GetLocalPosition()[1] != y:
			self.resizeButton.SetPosition(0, y)
			self.OnResizeDialog()

	def RefreshMessenger(self):
		self.OnRefreshList()

	## EventHandler
	def __AddList(self, groupIndex, key, name):
		group = self.groupList[groupIndex]
		member = group.FindMember(key)
		if not member:
			member = group.AppendMember(key, name)
			self.OnSelectItem(None)
			member.MobileApplyInfo()	# MOBIL
		return member

	def OnRemoveList(self, groupIndex, key):
		group = self.groupList[groupIndex]
		group.RemoveMember(group.FindMember(key))
		self.OnRefreshList()

	def OnRemoveAllList(self, groupIndex):
		group = self.groupList[groupIndex]
		group.ClearMember()
		self.OnRefreshList()

	def OnLogin(self, groupIndex, key, name=None):
		if not name:
			name = key
		group = self.groupList[groupIndex]
		member = self.__AddList(groupIndex, key, name)
		member.SetName(name)
		member.Online()
		member.MobileApplyInfo()	# MOBIL
		self.OnRefreshList()

	def OnLogout(self, groupIndex, key, name=None):
		group = self.groupList[groupIndex]
		member = self.__AddList(groupIndex, key, name)
		if not name:
			name = key
		member.SetName(name)
		member.Offline()
		member.MobileApplyInfo()	# MOBIL
		self.OnRefreshList()

	def OnMobile(self, groupIndex, key, mobileFlag):
		group = self.groupList[groupIndex]
		member = group.FindMember(key)
		if not member:
			return
		member.SetMobile(mobileFlag)
		self.OnRefreshList()

	def OnAddLover(self, name, lovePoint):
		if not self.familyGroup:
			self.__AddFamilyGroup()

		member = self.familyGroup.AppendMember(0, name)

		member.SetName(name)
		member.SetLovePoint(lovePoint)
		member.Offline()
		self.OnRefreshList()

	def OnUpdateLovePoint(self, lovePoint):
		if not self.familyGroup:
			return

		lover = self.familyGroup.GetLover()
		if not lover:
			return

		lover.SetLovePoint(lovePoint)

	def OnLoginLover(self):
		if not self.familyGroup:
			return

		lover = self.familyGroup.GetLover()
		if not lover:
			return

		lover.Online()

	def OnLogoutLover(self):
		if not self.familyGroup:
			return

		lover = self.familyGroup.GetLover()
		if not lover:
			return

		lover.Offline()

	def ClearLoverInfo(self):
		if not self.familyGroup:
			return

		self.familyGroup.ClearMember()
		self.familyGroup = None
		self.OnRefreshList()
