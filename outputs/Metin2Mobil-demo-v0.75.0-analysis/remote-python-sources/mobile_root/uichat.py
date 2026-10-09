# MOBIL KAPLAMA: mobile_root/uichat.py - pack'teki root/uichat.py'nin telefon surumu.
# Android'de (ve Windows'ta M2_MOBILE_ROOT verilince) pack'teki uichat.py'yi GOLGELER;
# PC pack'i ve PC gorunumu degismez. interfacemodule.py'nin uichat'ten kullandigi API
# aynen korunur (grep uiChat. interfacemodule.py):
#   uiChat.ChatWindow()          -> CHAT_WINDOW_WIDTH, EDIT_LINE_HEIGHT, SetSize, SetPosition,
#                                   SetHeight, Refresh, Show, Hide, BindInterface,
#                                   SetSendWhisperEvent, SetOpenChatLogEvent, IsEditMode,
#                                   OpenChat, CloseChat, SetChatFocus, Destroy, OnChangeChatMode
#   uiChat.ChatLogWindow()       -> pack ile BIREBIR (L tusu / kisayollar paneli acar)
#   uiChat.DestroyChatInputSetWindow()
# Mobil ChatWindow:
#   - Pencere KAPALIYKEN: kisa akis (chat.CHAT_SET_CHAT_WINDOW seti, BOARD_STATE_VIEW) ekranin
#     altinda PC'deki gibi surer (LAYOUT: sol 0.295 W, ust 0.816 H, alt 0.975 H).
#   - Sohbet dugmesi -> interface.ToggleChat() -> OpenChat(): ekranin ortasinda pencere
#     (LAYOUT: sol 0.2478 W, ust 0.0754 H, genislik 0.5177 W, yukseklik 0.7115 H).
#     Baslik (secili sekme adi), zarf = interface.OpenWhisperDialogWithoutTarget
#     (SetSendWhisperEvent - pack ChatWindow.btnSendWhisper ile ayni), "Durdur" = akan
#     mesajlari dondurur (chat.SetEndPos ile gorunen son satir sabit tutulur), disli =
#     gercek Oyun Ayarlari penceresi (uisystem.py:140-146 ile ayni uiGameOption.OptionDialog:
#     sohbet gorunumu ac/kapa, fisilti engelleme), carpi = CloseChat.
#     Sekmeler Genel/Normal/Bagirmak/Bilgi/Sunucu/Grup/Lonca = ChatLogWindow.ToggleChatMode
#     ile ayni chat.EnableChatMode/DisableChatMode filtreleri (kendi BOARD_STATE_LOG seti).
#     Mesaj listesi gercek chat setidir (chat.Render), kaydirma cubugu chat.SetEndPos,
#     altta ChatLine (dokununca EditLine.OnSetFocus -> ime.EnableCaptureInput -> telefon
#     klavyesi; Enter = OnIMEReturn = gonder) + gonder dugmesi (chatLine.OnIMEReturn,
#     pack ChatInputSet.btnSend ile ayni).
# Gorseller: mobile/ui/chat/*.tga (spike/sohbet/gen_chat_ui.py ile PIL uretimi).
import ui
import grp
import chat
import wndMgr
import net
import app
import ime
import localeInfo
import colorInfo
import constInfo
import systemSetting
import player
import sys
from _weakref import proxy

ENABLE_CHAT_COMMAND = True
ENABLE_LAST_SENTENCE_STACK = True
ENABLE_INSULT_CHECK = True

if localeInfo.IsHONGKONG():
	ENABLE_LAST_SENTENCE_STACK = True

if localeInfo.IsEUROPE():
	ENABLE_CHAT_COMMAND = False

if localeInfo.IsCANADA():
	ENABLE_LAST_SENTENCE_STACK = False

# ---- MOBIL ayarlar ----------------------------------------------------------------
# Gorsel klasoru (kaplama icinde pack yolu gibi cozulur). Test betigi Windows'ta kaplama
# mekanizmasi olmadan da calistirabilsin diye modul degiskeni (mutlak yol verilebilir).
MOBILE_UI_DIR = "mobile/ui/chat/"
# Mobil pencerenin sohbet seti kimligi (pack: CHAT_SET_CHAT_WINDOW=0, CHAT_SET_LOG_WINDOW=1).
CHAT_SET_MOBILE_WINDOW = 2
# Yazilim klavyesi acikken pencere ekranin ust yarisina cekilir (giris satiri klavyenin
# altinda kalmasin). Windows'ta donanim klavyesi: gerek yok.
KEYBOARD_COMPACT = (sys.platform != "win32")
# Pencere acilinca giris satirina odak: yalniz donanim klavyeli PC'de (telefonda odak =
# klavye acilir; kullanici satira dokununca acilsin).
AUTO_FOCUS_ON_OPEN = (sys.platform == "win32")
CHAT_PLACEHOLDER = "mesaj yaz..."

COLOR_GOLD = 0xffd3a94c
COLOR_GOLD_DEEP = 0xff7f5f22
COLOR_PANEL_FILL = 0xf7171310
COLOR_FIELD_FILL = 0xff1a1510
COLOR_TRACK = 0xff2a2118
COLOR_TITLE = 0xfff1e6c8

chatInputSetList = []
def InsertChatInputSetWindow(wnd):
	global chatInputSetList
	chatInputSetList.append(wnd)
def RefreshChatMode():
	global chatInputSetList
	map(lambda wnd:wnd.OnRefreshChatMode(), chatInputSetList)
def DestroyChatInputSetWindow():
	global chatInputSetList
	chatInputSetList = []

## ChatModeButton (pack ile ayni)
class ChatModeButton(ui.Window):

	OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
	OVER_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.3)
	BUTTON_STATE_UP = 0
	BUTTON_STATE_OVER = 1
	BUTTON_STATE_DOWN = 2

	def __init__(self):
		ui.Window.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.state = None
		self.buttonText = None
		self.event = None
		self.SetWindowName("ChatModeButton")

		net.EnableChatInsultFilter(ENABLE_INSULT_CHECK)

	def __del__(self):
		ui.Window.__del__(self)

	def SAFE_SetEvent(self, event):
		self.event=ui.__mem_func__(event)

	def SetText(self, text):
		if None == self.buttonText:
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetWindowVerticalAlignCenter()
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.SetPackedFontColor(self.OUTLINE_COLOR)
			textLine.SetFontName("Tahoma:15")	# MOBIL (2026-09-14): kip dugmesi yazisi okunur boyutta
			textLine.Show()
			self.buttonText = textLine

		self.buttonText.SetText(text)

	def SetSize(self, width, height):
		self.width = width
		self.height = height
		ui.Window.SetSize(self, width, height)

	def OnMouseOverIn(self):
		self.state = self.BUTTON_STATE_OVER

	def OnMouseOverOut(self):
		self.state = self.BUTTON_STATE_UP

	def OnMouseLeftButtonDown(self):
		self.state = self.BUTTON_STATE_DOWN

	def OnMouseLeftButtonUp(self):
		self.state = self.BUTTON_STATE_UP
		if self.IsIn():
			self.state = self.BUTTON_STATE_OVER

		if None != self.event:
			self.event()

	def OnRender(self):

		(x, y) = self.GetGlobalPosition()

		grp.SetColor(self.OUTLINE_COLOR)
		grp.RenderRoundBox(x, y, self.width, self.height)

		if self.state >= self.BUTTON_STATE_OVER:
			grp.RenderRoundBox(x+1, y, self.width-2, self.height)
			grp.RenderRoundBox(x, y+1, self.width, self.height-2)

			if self.BUTTON_STATE_DOWN == self.state:
				grp.SetColor(self.OVER_COLOR)
				grp.RenderBar(x+1, y+1, self.width-2, self.height-2)

## ChatLine (pack ile ayni; MOBIL ek: ApplyChatMode, overLay metni yer tutucu)
class ChatLine(ui.EditLine):

	CHAT_MODE_NAME = {	chat.CHAT_TYPE_TALKING : localeInfo.CHAT_NORMAL,
						chat.CHAT_TYPE_PARTY : localeInfo.CHAT_PARTY,
						chat.CHAT_TYPE_GUILD : localeInfo.CHAT_GUILD,
						chat.CHAT_TYPE_SHOUT : localeInfo.CHAT_SHOUT, }

	# ChangeChatMode / __ResetChat ile ayni on-ek kurali
	CHAT_MODE_PREFIX = {	chat.CHAT_TYPE_PARTY : "#",
							chat.CHAT_TYPE_GUILD : "%",
							chat.CHAT_TYPE_SHOUT : "!", }

	def __init__(self):
		ui.EditLine.__init__(self)
		self.SetWindowName("Chat Line")
		self.lastShoutTime = 0
		self.eventEscape = lambda *arg: None
		self.eventReturn = lambda *arg: None
		self.eventTab = None
		self.chatMode = chat.CHAT_TYPE_TALKING
		self.bCodePage = True

		self.overTextLine = ui.TextLine()
		self.overTextLine.SetParent(self)
		self.overTextLine.SetPosition(-1, 0)
		self.overTextLine.SetFontColor(1.0, 1.0, 0.0)
		self.overTextLine.SetOutline()
		self.overTextLine.Hide()

		# pack: hesap guvenligi uyarisi; mobilde bos satir yer tutucusu ("mesaj yaz...")
		WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.5)
		self.overLay = ui.TextLine()
		self.overLay.SetParent(self)
		self.overLay.SetPosition(5, 0)
		self.overLay.SetPackedFontColor(WHITE_COLOR)
		self.overLay.SetText(CHAT_PLACEHOLDER)
		self.overLay.Show()

		self.lastSentenceStack = []
		self.lastSentencePos = 0

	def SetChatMode(self, mode):
		self.chatMode = mode

	def GetChatMode(self):
		return self.chatMode

	def ChangeChatMode(self):
		if chat.CHAT_TYPE_TALKING == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_PARTY)
			self.SetText("#")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_PARTY == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_GUILD)
			self.SetText("%")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_GUILD == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_SHOUT)
			self.SetText("!")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_SHOUT == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_TALKING)
			self.SetText("")

		self.__CheckChatMark()

	# MOBIL: sekme secimi gonderim kipini dogrudan ayarlar (ChangeChatMode dongusunun
	# tek adimda hedefe gitmis hali; on-ek ve isaret kurali ayni).
	def ApplyChatMode(self, mode):
		if not self.CHAT_MODE_NAME.has_key(mode):
			return
		self.SetChatMode(mode)
		prefix = self.CHAT_MODE_PREFIX.get(mode, "")
		self.SetText(prefix)
		if prefix:
			self.SetEndPosition()
		self.__CheckChatMark()

	def GetCurrentChatModeName(self):
		try:
			return self.CHAT_MODE_NAME[self.chatMode]
		except:
			import exception
			exception.Abort("ChatLine.GetCurrentChatModeName")

	def SAFE_SetEscapeEvent(self, event):
		self.eventReturn = ui.__mem_func__(event)

	def SAFE_SetReturnEvent(self, event):
		self.eventEscape = ui.__mem_func__(event)

	def SAFE_SetTabEvent(self, event):
		self.eventTab = ui.__mem_func__(event)

	def SetTabEvent(self, event):
		self.eventTab = event

	def OpenChat(self):
		self.SetFocus()
		self.__ResetChat()

	def __ClearChat(self):
		self.SetText("")
		self.lastSentencePos = 0

	def __ResetChat(self):
		if chat.CHAT_TYPE_PARTY == self.GetChatMode():
			self.SetText("#")
			self.SetEndPosition()
		elif chat.CHAT_TYPE_GUILD == self.GetChatMode():
			self.SetText("%")
			self.SetEndPosition()
		elif chat.CHAT_TYPE_SHOUT == self.GetChatMode():
			self.SetText("!")
			self.SetEndPosition()
		else:
			self.__ClearChat()

		self.__CheckChatMark()


	## MOBIL SOHBET FRENI (2026-09-21, SUNUCU DUZELTILDIKTEN SONRA GEVSETILDI).
	## Sunucudaki asil hata giderildi: sohbet sayaci artik CHARACTER_MANAGER::Update'in
	## pulse-modulo dalina degil, input_main.cpp icinde KARAKTER BASINA gercek zamana
	## bagli (5 sn / 10 mesaj). Yani 18 saniyeye yayilmis mesajlar artik atilmaya yol acmaz.
	## Burada kalan fren yalniz bir nezaket tamponu: kayan 5 saniyede en fazla 8 mesaj
	## gonderilir, 9.'su bekletilir. Boylece oyuncu sunucunun 10 esigine HIC ulasmaz ve
	## hic dusurulmez; normal sohbet hizi (saniyede 1-2 mesaj) hic etkilenmez.
	## Komutlar ('/...') sunucuda sayilmadigi icin frene girmez.
	MOBILE_CHAT_WINDOW_SEC = 5.0
	MOBILE_CHAT_MAX_IN_WINDOW = 8
	mobileSendTimes = []

	def __SendChatPacket(self, text, type):
		if net.IsChatInsultIn(text):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHAT_INSULT_STRING)
			return True
		if not text.startswith("/"):
			now = app.GetTime()
			self.mobileSendTimes = [t for t in self.mobileSendTimes if now - t < self.MOBILE_CHAT_WINDOW_SEC]
			if len(self.mobileSendTimes) >= self.MOBILE_CHAT_MAX_IN_WINDOW:
				kalan = int(self.MOBILE_CHAT_WINDOW_SEC - (now - self.mobileSendTimes[0])) + 1
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Çok hýzlý yazýyorsun, %d saniye bekle." % kalan)
				return False
			self.mobileSendTimes.append(now)
		net.SendChatPacket(text, type)
		return True

	def __SendPartyChatPacket(self, text):

		if 1 == len(text):
			self.RunCloseEvent()
			return

		if self.__SendChatPacket(text[1:], chat.CHAT_TYPE_PARTY):
			self.__ResetChat()

	def __SendGuildChatPacket(self, text):

		if 1 == len(text):
			self.RunCloseEvent()
			return

		if self.__SendChatPacket(text[1:], chat.CHAT_TYPE_GUILD):
			self.__ResetChat()

	def __SendShoutChatPacket(self, text):

		if 1 == len(text):
			self.RunCloseEvent()
			return

		if app.GetTime() < self.lastShoutTime + 15:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHAT_SHOUT_LIMIT)
			self.__ResetChat()
			return

		if self.__SendChatPacket(text[1:], chat.CHAT_TYPE_SHOUT):
			self.__ResetChat()
			self.lastShoutTime = app.GetTime()

	def __SendTalkingChatPacket(self, text):
		if self.__SendChatPacket(text, chat.CHAT_TYPE_TALKING):
			self.__ResetChat()

	def OnIMETab(self):
		return False

	def OnIMEUpdate(self):
		ui.EditLine.OnIMEUpdate(self)
		self.__CheckChatMark()

	def __CheckChatMark(self):

		self.overTextLine.Hide()

		text = self.GetText()
		if len(text) > 0:
			if '#' == text[0]:
				self.overTextLine.SetText("#")
				self.overTextLine.Show()
			elif '%' == text[0]:
				self.overTextLine.SetText("%")
				self.overTextLine.Show()
			elif '!' == text[0]:
				self.overTextLine.SetText("!")
				self.overTextLine.Show()

	def OnIMEKeyDown(self, key):
		# LAST_SENTENCE_STACK
		if app.VK_UP == key:
			self.__PrevLastSentenceStack()
			return True

		if app.VK_DOWN == key:
			self.__NextLastSentenceStack()
			return True
		# END_OF_LAST_SENTENCE_STACK

		ui.EditLine.OnIMEKeyDown(self, key)

	# LAST_SENTENCE_STACK
	def __PrevLastSentenceStack(self):
		global ENABLE_LAST_SENTENCE_STACK
		if not ENABLE_LAST_SENTENCE_STACK:
			return

		if self.lastSentenceStack and self.lastSentencePos < len(self.lastSentenceStack):
			self.lastSentencePos += 1
			lastSentence = self.lastSentenceStack[-self.lastSentencePos]
			self.SetText(lastSentence)
			self.SetEndPosition()

	def __NextLastSentenceStack(self):
		global ENABLE_LAST_SENTENCE_STACK
		if not ENABLE_LAST_SENTENCE_STACK:
			return

		if self.lastSentenceStack and self.lastSentencePos > 1:
			self.lastSentencePos -= 1
			lastSentence = self.lastSentenceStack[-self.lastSentencePos]
			self.SetText(lastSentence)
			self.SetEndPosition()

	def __PushLastSentenceStack(self, text):
		global ENABLE_LAST_SENTENCE_STACK
		if not ENABLE_LAST_SENTENCE_STACK:
			return

		if len(text) <= 0:
			return

		LAST_SENTENCE_STACK_SIZE = 32
		if len(self.lastSentenceStack) > LAST_SENTENCE_STACK_SIZE:
			self.lastSentenceStack.pop(0)

		self.lastSentenceStack.append(text)
	# END_OF_LAST_SENTENCE_STACK

	def OnIMEReturn(self):
		text = self.GetText()
		textLen=len(text)

		# LAST_SENTENCE_STACK
		self.__PushLastSentenceStack(text)
		# END_OF_LAST_SENTENCE_STACK

		textSpaceCount=text.count(' ')

		if (textLen > 0) and (textLen != textSpaceCount):
			if '#' == text[0]:
				self.__SendPartyChatPacket(text)
			elif '%' == text[0]:
				self.__SendGuildChatPacket(text)
			elif '!' == text[0]:
				self.__SendShoutChatPacket(text)
			else:
				self.__SendTalkingChatPacket(text)
		else:
			self.__ClearChat()
			self.eventReturn()

		return True

	def OnPressEscapeKey(self):
		self.__ClearChat()
		self.eventEscape()
		return True

	def RunCloseEvent(self):
		self.eventEscape()

	def BindInterface(self, interface):
		self.interface = interface

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			if app.IsPressed(app.DIK_LALT):
				link = chat.GetLinkFromHyperlink(hyperlink)
				ime.PasteString(link)
			else:
				self.interface.MakeHyperlinkTooltip(hyperlink)
		else:
			ui.EditLine.OnMouseLeftButtonDown(self)

## ChatInputSet (pack ile ayni; ChatLogWindow kullanir)
class ChatInputSet(ui.Window):

	CHAT_OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

	def __init__(self):
		ui.Window.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.SetWindowName("ChatInputSet")
		InsertChatInputSetWindow(self)
		self.__Create()

	def __del__(self):
		ui.Window.__del__(self)

	def __Create(self):
		chatModeButton = ChatModeButton()
		chatModeButton.SetParent(self)
		chatModeButton.SetSize(40, 17)
		chatModeButton.SetText(localeInfo.CHAT_NORMAL)
		chatModeButton.SetPosition(7, 2)
		chatModeButton.SAFE_SetEvent(self.OnChangeChatMode)
		self.chatModeButton = chatModeButton

		chatLine = ChatLine()
		chatLine.SetParent(self)
		chatLine.SetMax(512)
		chatLine.SetUserMax(76)
		chatLine.SetText("")
		chatLine.SAFE_SetTabEvent(self.OnChangeChatMode)
		chatLine.x = 0
		chatLine.y = 0
		chatLine.width = 0
		chatLine.height = 0
		self.chatLine = chatLine

		btnSend = ui.Button()
		btnSend.SetParent(self)
		btnSend.SetUpVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_01.sub")
		btnSend.SetOverVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_02.sub")
		btnSend.SetDownVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_03.sub")
		btnSend.SetToolTipText(localeInfo.CHAT_SEND_CHAT)
		btnSend.SAFE_SetEvent(self.chatLine.OnIMEReturn)
		self.btnSend = btnSend

	def Destroy(self):
		self.chatModeButton = None
		self.chatLine = None
		self.btnSend = None

	def Open(self):
		self.chatLine.Show()
		self.chatLine.SetPosition(57, 5)
		self.chatLine.SetFocus()
		self.chatLine.OpenChat()

		self.chatModeButton.SetPosition(7, 2)
		self.chatModeButton.Show()

		self.btnSend.Show()
		self.Show()

		self.RefreshPosition()
		return True

	def Close(self):
		self.chatLine.KillFocus()
		self.chatLine.Hide()
		self.chatModeButton.Hide()
		self.btnSend.Hide()
		self.Hide()
		return True

	def SetEscapeEvent(self, event):
		self.chatLine.SetEscapeEvent(event)

	def SetReturnEvent(self, event):
		self.chatLine.SetReturnEvent(event)

	def OnChangeChatMode(self):
		RefreshChatMode()

	def OnRefreshChatMode(self):
		self.chatLine.ChangeChatMode()
		self.chatModeButton.SetText(self.chatLine.GetCurrentChatModeName())

	def SetChatFocus(self):
		self.chatLine.SetFocus()

	def KillChatFocus(self):
		self.chatLine.KillFocus()

	def SetChatMax(self, max):
		self.chatLine.SetUserMax(max)

	def RefreshPosition(self):
		if localeInfo.IsARABIC():
			self.chatLine.SetSize(self.GetWidth() - 93, 18)
		else:
			self.chatLine.SetSize(self.GetWidth() - 93, 13)

		self.btnSend.SetPosition(self.GetWidth() - 25, 2)

		(self.chatLine.x, self.chatLine.y, self.chatLine.width, self.chatLine.height) = self.chatLine.GetRect()

	def BindInterface(self, interface):
		self.chatLine.BindInterface(interface)

	def OnRender(self):
		(x, y, width, height) = self.chatLine.GetRect()
		ui.RenderRoundBox(x-4, y-3, width+7, height+4, self.CHAT_OUTLINE_COLOR)

###################################################################################################
## MOBIL: yardimci pencereler
###################################################################################################

## Dokunmatik kaydirma cubugu: ui.ScrollBar ile ayni arayuz (SetScrollBarSize/SetPos/GetPos/
## SetScrollEvent/LockScroll/UnlockScroll), topuz ui.DragButton (SetRestrictMovementArea),
## ray ui.Bar. PC'nin kucuk .sub gorselleri yerine dokunmaya uygun 16x48 altin topuz.
class MobileScrollBar(ui.Window):

	THUMB_WIDTH = 16
	THUMB_HEIGHT = 48
	TRACK_WIDTH = 6

	def __init__(self):
		ui.Window.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.SetWindowName("MobileScrollBar")
		self.curPos = 1.0
		self.pageSize = 1
		self.lockFlag = False
		self.eventScroll = lambda *arg: None

		track = ui.Bar()
		track.SetParent(self)
		track.AddFlag("not_pick")
		track.SetColor(COLOR_TRACK)
		track.Show()
		self.track = track

		thumb = ui.DragButton()
		thumb.SetParent(self)
		thumb.SetUpVisual(MOBILE_UI_DIR + "scroll_thumb.tga")
		thumb.SetOverVisual(MOBILE_UI_DIR + "scroll_thumb.tga")
		thumb.SetDownVisual(MOBILE_UI_DIR + "scroll_thumb.tga")
		thumb.SetMoveEvent(ui.__mem_func__(self.OnMove))
		thumb.Show()
		self.thumb = thumb

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.thumb = None
		self.track = None
		self.eventScroll = lambda *arg: None

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetScrollBarSize(self, height):
		height = max(self.THUMB_HEIGHT + 1, height)
		self.SetSize(self.THUMB_WIDTH, height)
		self.track.SetPosition((self.THUMB_WIDTH - self.TRACK_WIDTH) / 2, 0)
		self.track.SetSize(self.TRACK_WIDTH, height)
		self.pageSize = height - self.THUMB_HEIGHT
		self.thumb.SetRestrictMovementArea(0, 0, self.THUMB_WIDTH, height)
		self.SetPos(self.curPos)

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)
		self.thumb.SetPosition(0, int(float(self.pageSize) * pos))
		self.OnMove()

	def OnMove(self):
		if self.lockFlag:
			return
		if 0 == self.pageSize:
			return
		(xLocal, yLocal) = self.thumb.GetLocalPosition()
		self.curPos = float(yLocal) / float(self.pageSize)
		self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouse, yMouse) = self.GetMouseLocalPosition()
		self.SetPos(float(yMouse - self.THUMB_HEIGHT / 2) / float(self.pageSize))

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False

## Odak degisimini pencereye bildiren ChatLine (klavye acilinca pencere yukari cekilir)
class MobileChatLine(ChatLine):

	MOBILE_INPUT_FONT = "Tahoma:18"	# KULLANICI (2026-09-14): yazilan mesaj kutuda gorunmuyordu (varsayilan Tahoma:12 cok kucuk)

	def __init__(self):
		ChatLine.__init__(self)
		self.focusOwner = None
		self.SetFontName(self.MOBILE_INPUT_FONT)
		self.overLay.SetFontName(self.MOBILE_INPUT_FONT)
		self.overTextLine.SetFontName(self.MOBILE_INPUT_FONT)

	def __del__(self):
		ChatLine.__del__(self)

	def SetFocusOwner(self, owner):
		self.focusOwner = proxy(owner)

	def OnSetFocus(self):
		ui.EditLine.OnSetFocus(self)
		if self.focusOwner:
			self.focusOwner.OnChatLineFocus(True)

	def OnKillFocus(self):
		ui.EditLine.OnKillFocus(self)
		if self.focusOwner:
			self.focusOwner.OnChatLineFocus(False)

## Mobil giris satiri: kip dugmesi (pack ChatModeButton) + ChatLine + gonder dugmesi.
## ChatInputSet ile ayni arayuz; RefreshChatMode listesine kaydolur (Tab ile kip dongusu).
class MobileChatInputSet(ui.Window):

	SEND_WIDTH = 80
	SEND_GAP = 10
	MODE_WIDTH = 60
	MODE_HEIGHT = 26
	LINE_HEIGHT = 24	# Tahoma:18 giris satiri

	def __init__(self, owner):
		ui.Window.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.SetWindowName("MobileChatInputSet")
		InsertChatInputSetWindow(self)

		chatModeButton = ChatModeButton()
		chatModeButton.SetParent(self)
		chatModeButton.SetSize(self.MODE_WIDTH, self.MODE_HEIGHT)
		chatModeButton.SetText(localeInfo.CHAT_NORMAL)
		chatModeButton.SAFE_SetEvent(self.OnChangeChatMode)
		self.chatModeButton = chatModeButton

		chatLine = MobileChatLine()
		chatLine.SetParent(self)
		chatLine.SetMax(512)
		chatLine.SetUserMax(76)
		chatLine.SetText("")
		chatLine.SAFE_SetTabEvent(self.OnChangeChatMode)
		chatLine.SetFocusOwner(owner)
		self.chatLine = chatLine

		btnSend = ui.Button()
		btnSend.SetParent(self)
		btnSend.SetUpVisual(MOBILE_UI_DIR + "send_up.tga")
		btnSend.SetOverVisual(MOBILE_UI_DIR + "send_up.tga")
		btnSend.SetDownVisual(MOBILE_UI_DIR + "send_down.tga")
		btnSend.SetToolTipText(localeInfo.CHAT_SEND_CHAT)
		btnSend.SAFE_SetEvent(self.chatLine.OnIMEReturn)
		self.btnSend = btnSend

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.chatModeButton = None
		self.chatLine = None
		self.btnSend = None

	def Open(self):
		self.chatLine.Show()
		self.chatModeButton.Show()
		self.btnSend.Show()
		self.Show()
		self.RefreshPosition()
		return True

	def Close(self):
		self.chatLine.KillFocus()
		self.chatLine.Hide()
		self.chatModeButton.Hide()
		self.btnSend.Hide()
		self.Hide()
		return True

	def SetEscapeEvent(self, event):
		self.chatLine.SetEscapeEvent(event)

	def SetReturnEvent(self, event):
		self.chatLine.SetReturnEvent(event)

	def OnChangeChatMode(self):
		RefreshChatMode()

	def OnRefreshChatMode(self):
		self.chatLine.ChangeChatMode()
		self.chatModeButton.SetText(self.chatLine.GetCurrentChatModeName())

	# MOBIL: sekmeden gelen gonderim kipi (yalniz Normal/Grup/Lonca/Bagirmak)
	def SetChatMode(self, mode):
		if not ChatLine.CHAT_MODE_NAME.has_key(mode):
			return
		self.chatLine.ApplyChatMode(mode)
		self.chatModeButton.SetText(self.chatLine.GetCurrentChatModeName())

	def SetChatFocus(self):
		self.chatLine.SetFocus()

	def KillChatFocus(self):
		self.chatLine.KillFocus()

	def IsChatFocus(self):
		return self.chatLine.IsFocus()

	def SetChatMax(self, max):
		self.chatLine.SetUserMax(max)

	def GetFieldWidth(self):
		return self.GetWidth() - self.SEND_WIDTH - self.SEND_GAP

	def RefreshPosition(self):
		width = self.GetWidth()
		height = self.GetHeight()
		fieldWidth = self.GetFieldWidth()

		self.chatModeButton.SetPosition(8, (height - self.MODE_HEIGHT) / 2)

		lineX = 8 + self.MODE_WIDTH + 8
		self.chatLine.SetPosition(lineX, (height - self.LINE_HEIGHT) / 2)
		self.chatLine.SetSize(max(10, fieldWidth - lineX - 8), self.LINE_HEIGHT)

		self.btnSend.SetPosition(width - self.SEND_WIDTH, (height - self.btnSend.GetHeight()) / 2)

	def BindInterface(self, interface):
		self.chatLine.BindInterface(interface)

	## KULLANICI (2026-09-22, iPhone): "kutucuga bazen 2-3 kez dokunmak gerekiyor; en basina
	## ya da sonuna dokununca da klavye hemen acilmali". Altin cerceveli alan (OnRender) yazi
	## satirindan (EditLine, 24 px yukseklik, kip dugmesinden sonra baslar, sagda 8 px once biter)
	## buyuk; bosluga dusen dokunma EditLine'a degmedigi icin klavye acilmiyordu.
	## Cerceve icindeki her dokunma yazi satirina yonlendirilir: odak + ime.SetCursorPosition
	## (klavyeyi yeniden gosteren tetikleyici, bkz. PythonIMEModule imeSetCursorPosition).
	## Satirin solundaki bosluk imleci BASA, sagi/ustu/alti metindeki yerine (sona) koyar.
	## Kip ve gonder dugmeleri ustte oldugu icin kendi olaylarini alir, buraya dusmez.
	def OnMouseLeftButtonDown(self):
		(mx, my) = wndMgr.GetMouseLocalPosition(self.hWnd)
		if mx < 0 or my < 0 or mx >= self.GetFieldWidth() or my >= self.GetHeight():
			return False
		line = self.chatLine
		if not line or not line.IsShow():
			return False
		line.SetFocus()
		(lx, ly) = wndMgr.GetMouseLocalPosition(line.hWnd)
		if lx <= 0:
			pos = 0
		else:
			pos = wndMgr.GetCursorPosition(line.hWnd)
		ime.SetCursorPosition(pos)
		return True

	def OnRender(self):
		(x, y, width, height) = self.GetRect()
		fieldWidth = self.GetFieldWidth()
		grp.SetColor(COLOR_FIELD_FILL)
		grp.RenderBar(x, y, fieldWidth, height)
		ui.RenderRoundBox(x, y, fieldWidth - 1, height - 1, COLOR_GOLD)

## Mesaj listesi alani: her karede gercek chat setini konumlar ve cizer (ChatLogWindow.OnRender
## ile ayni cagri sirasi); baglantiya (item link) dokununca ChatLogWindow ile ayni davranis.
class MobileChatLogArea(ui.Window):

	def __init__(self, owner):
		ui.Window.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.SetWindowName("MobileChatLogArea")
		self.owner = proxy(owner)
		self.interface = None

	def __del__(self):
		ui.Window.__del__(self)

	def BindInterface(self, interface):
		self.interface = interface

	def OnRender(self):
		(x, y, width, height) = self.GetRect()
		chatID = self.owner.logID
		step = chat.GetLineStep(chatID)
		chat.SetPosition(chatID, x, y + height)
		chat.SetHeight(chatID, height - step)
		self.owner.UpdateFreeze()
		chat.ArrangeShowingChat(chatID)
		chat.Update(chatID)
		chat.Render(chatID)

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			if app.IsPressed(app.DIK_LALT):
				link = chat.GetLinkFromHyperlink(hyperlink)
				ime.PasteString(link)
			elif self.interface:
				self.interface.MakeHyperlinkTooltip(hyperlink)

## Pencere zemini: dolgu + altin cerceve (duz kenarlar grp ile, koseler .tga cocuk resimleri)
class MobileChatPanel(ui.Window):

	CORNER = 20

	def __init__(self):
		ui.Window.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.AddFlag("float")
		self.AddFlag("movable")	# MOBIL: sohbet paneli baslik seridinden surukle (kullanici 2026-09-13); OpenChat her acilista yerine koyar
		self.SetWindowName("MobileChatPanel")

	def __del__(self):
		ui.Window.__del__(self)

	def OnRender(self):
		(x, y, width, height) = self.GetRect()
		r = self.CORNER

		grp.SetColor(COLOR_PANEL_FILL)
		grp.RenderBar(x + r, y, width - 2*r, height)
		grp.RenderBar(x, y + r, r, height - 2*r)
		grp.RenderBar(x + width - r, y + r, r, height - 2*r)

		grp.SetColor(COLOR_GOLD_DEEP)
		grp.RenderBar(x + r, y, width - 2*r, 1)
		grp.RenderBar(x + r, y + height - 1, width - 2*r, 1)
		grp.RenderBar(x, y + r, 1, height - 2*r)
		grp.RenderBar(x + width - 1, y + r, 1, height - 2*r)

		grp.SetColor(COLOR_GOLD)
		grp.RenderBar(x + r, y + 1, width - 2*r, 3)
		grp.RenderBar(x + r, y + height - 4, width - 2*r, 3)
		grp.RenderBar(x + 1, y + r, 3, height - 2*r)
		grp.RenderBar(x + width - 4, y + r, 3, height - 2*r)

###################################################################################################
## ChatWindow (MOBIL)
###################################################################################################
class ChatWindow(ui.Window):

	BOARD_START_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.0)
	BOARD_END_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
	BOARD_MIDDLE_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.5)
	CHAT_OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

	# pack sabitleri (interfacemodule.__MakeChatWindow bunlari kullanir)
	EDIT_LINE_HEIGHT = 25
	CHAT_WINDOW_WIDTH = 600+25

	# LAYOUT (mockup 1356x610'dan yuzde): pencere
	PANEL_X = 0.2478
	PANEL_Y = 0.0754
	PANEL_W = 0.5177
	PANEL_H = 0.7115
	# yazilim klavyesi acikken (giris satiri ~0.47 H'de kalsin)
	PANEL_COMPACT_Y = 0.01
	PANEL_COMPACT_H = 0.47
	# kisa akis (pencere kapaliyken)
	FLOW_X = 0.255
	FLOW_TOP = 0.76
	FLOW_BOTTOM = 0.985
	FLOW_W = 0.49
	MOBILE_CHAT_FONT = "Tahoma:18"	# KULLANICI (2026-09-14): sohbet yazilari biraz daha buyuk (16 -> 18)
	MOBILE_CHAT_STEP = 22
	MOBILE_TEXTTAIL_OFFSET = 20
	FLOW_BG_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.45)
	# mockup pencere yuksekligi (ic yerlesim bu olcege gore)
	MOCK_PANEL_HEIGHT = 434.0

	TAB_WIDTH = 84
	TAB_HEIGHT = 30
	TAB_GAP = 6
	ICON_SIZE = 36
	STOP_WIDTH = 84
	INPUT_HEIGHT = 38
	PAD = 14

	# Sekmeler: (baslik, chat kipi). None = Genel (ChatLogWindow.ToggleAllChatMode).
	# "Sunucu" = chat.CHAT_TYPE_NOTICE (pack ChatLogWindow'da localeInfo.CHAT_NOTICE "Duyuru").
	TAB_LIST = (	(localeInfo.CHAT_ALL,			None),
					(localeInfo.CHAT_NORMAL,		chat.CHAT_TYPE_TALKING),
					(localeInfo.CHAT_SHOUT,			chat.CHAT_TYPE_SHOUT),
					(localeInfo.CHAT_INFORMATION,	chat.CHAT_TYPE_INFO),
					("Sunucu",						chat.CHAT_TYPE_NOTICE),
					(localeInfo.CHAT_PARTY,			chat.CHAT_TYPE_PARTY),
					(localeInfo.CHAT_GUILD,			chat.CHAT_TYPE_GUILD), )
	# ChatLogWindow.CHAT_MODE_INDEX ile ayni kume (filtre ac/kapa bu kume uzerinde)
	CHAT_MODE_INDEX = (	chat.CHAT_TYPE_TALKING,
						chat.CHAT_TYPE_PARTY,
						chat.CHAT_TYPE_GUILD,
						chat.CHAT_TYPE_SHOUT,
						chat.CHAT_TYPE_INFO,
						chat.CHAT_TYPE_NOTICE, )
	STOP_TEXT_GO = "Durdur"
	STOP_TEXT_HALT = "Devam"

	def __init__(self):
		# ui.Window.__init__ icinde Hide() cagrilir; Hide() override'i bunlara bakar
		self.boardState = chat.BOARD_STATE_VIEW
		self.panel = None
		self.chatInputSet = None

		ui.Window.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.AddFlag("float")

		self.SetWindowName("ChatWindow")
		self.__RegisterChatColorDict()

		# KULLANICI (2026-09-13): telefonda sohbet/isim yazilari okunmuyordu (PC Tahoma:12 = ~20 fiziksel
		# piksel). Mobilde ayri yazi tipi (native ChatFont; PC'de cagrilmaz) + buyuk satir araligi +
		# karakter ustu yazilar biraz yukari.
		if hasattr(app, "SetMobileChatFontName"):
			app.SetMobileChatFontName(self.MOBILE_CHAT_FONT)
			app.SetTextTailScreenOffset(self.MOBILE_TEXTTAIL_OFFSET)

		self.chatID = chat.CreateChatSet(chat.CHAT_SET_CHAT_WINDOW)
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_VIEW)
		chat.SetStep(self.chatID, self.MOBILE_CHAT_STEP)

		self.logID = chat.CreateChatSet(CHAT_SET_MOBILE_WINDOW)
		chat.SetBoardState(self.logID, chat.BOARD_STATE_LOG)
		chat.SetStep(self.logID, self.MOBILE_CHAT_STEP)
		for i in self.CHAT_MODE_INDEX:
			chat.EnableChatMode(self.logID, i)

		self.interface = None
		self.compact = False
		self.frozen = False
		self.frozenEndLine = 0
		self.scrollBarPos = 1.0
		self.eventOpenChatLog = None
		self.gameOptionDlg = None
		self.curTab = 0

		self.__CreatePanel()
		self.Refresh()

	def __del__(self):
		ui.Window.__del__(self)

	def __RegisterChatColorDict(self):
		CHAT_COLOR_DICT = {
			chat.CHAT_TYPE_TALKING : colorInfo.CHAT_RGB_TALK,
			chat.CHAT_TYPE_INFO : colorInfo.CHAT_RGB_INFO,
			chat.CHAT_TYPE_NOTICE : colorInfo.CHAT_RGB_NOTICE,
			chat.CHAT_TYPE_PARTY : colorInfo.CHAT_RGB_PARTY,
			chat.CHAT_TYPE_GUILD : colorInfo.CHAT_RGB_GUILD,
			chat.CHAT_TYPE_COMMAND : colorInfo.CHAT_RGB_COMMAND,
			chat.CHAT_TYPE_SHOUT : colorInfo.CHAT_RGB_SHOUT,
			chat.CHAT_TYPE_WHISPER : colorInfo.CHAT_RGB_WHISPER,
		}

		for colorItem in CHAT_COLOR_DICT.items():
			type=colorItem[0]
			rgb=colorItem[1]
			chat.SetChatColor(type, rgb[0], rgb[1], rgb[2])

	def __MakeRoundButton(self, name, event):
		btn = ui.Button()
		btn.SetParent(self.panel)
		btn.SetUpVisual(MOBILE_UI_DIR + "btn_%s_up.tga" % name)
		btn.SetOverVisual(MOBILE_UI_DIR + "btn_%s_up.tga" % name)
		btn.SetDownVisual(MOBILE_UI_DIR + "btn_%s_down.tga" % name)
		if event:
			btn.SetEvent(event)
		btn.Show()
		return btn

	def __CreatePanel(self):
		panel = MobileChatPanel()
		panel.Hide()
		self.panel = panel

		self.corners = []
		for name in ("lt", "rt", "lb", "rb"):
			img = ui.ImageBox()
			img.SetParent(panel)
			img.AddFlag("not_pick")
			img.LoadImage(MOBILE_UI_DIR + "corner_%s.tga" % name)
			img.Show()
			self.corners.append(img)

		titleName = ui.TextLine()
		titleName.SetParent(panel)
		titleName.SetVerticalAlignCenter()
		titleName.SetPackedFontColor(COLOR_TITLE)
		titleName.SetText(self.TAB_LIST[0][0])
		titleName.Show()
		self.titleName = titleName

		# zarf: fisilti (interface.OpenWhisperDialogWithoutTarget, SetSendWhisperEvent ile baglanir)
		self.btnSendWhisper = self.__MakeRoundButton("env", None)
		self.btnSendWhisper.SetToolTipText(localeInfo.CHAT_SEND_MEMO)

		# Durdur: akan mesajlari dondur
		btnStop = ui.Button()
		btnStop.SetParent(panel)
		btnStop.SetEvent(ui.__mem_func__(self.OnClickStop))
		btnStop.Show()
		self.btnStop = btnStop
		self.__RefreshStopButton()

		# disli: gercek Oyun Ayarlari (sohbet gorunumu / fisilti engelleme)
		self.btnSettings = self.__MakeRoundButton("gear", ui.__mem_func__(self.OnClickSettings))

		# carpi
		self.btnClose = self.__MakeRoundButton("x", ui.__mem_func__(self.CloseChat))
		self.btnClose.SetToolTipText(localeInfo.UI_CLOSE)

		# sekmeler
		self.tabButtonList = []
		i = 0
		for (name, mode) in self.TAB_LIST:
			btn = ui.RadioButton()
			btn.SetParent(panel)
			btn.SetUpVisual(MOBILE_UI_DIR + "tab_up.tga")
			btn.SetOverVisual(MOBILE_UI_DIR + "tab_up.tga")
			btn.SetDownVisual(MOBILE_UI_DIR + "tab_down.tga")
			btn.SetText(name)
			if btn.ButtonText:
				btn.ButtonText.SetFontName("Tahoma:16")	# MOBIL (2026-09-14): sekme yazilari buyuk
			btn.SetEvent(ui.__mem_func__(self.OnClickTab), i)
			btn.Show()
			self.tabButtonList.append(btn)
			i += 1
		self.tabButtonList[0].Down()

		# mesaj listesi
		logArea = MobileChatLogArea(self)
		logArea.SetParent(panel)
		logArea.Show()
		self.logArea = logArea

		# kaydirma cubugu
		scrollBar = MobileScrollBar()
		scrollBar.SetParent(panel)
		scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		scrollBar.Show()
		self.scrollBar = scrollBar

		# giris satiri
		chatInputSet = MobileChatInputSet(self)
		chatInputSet.SetParent(panel)
		chatInputSet.SetEscapeEvent(ui.__mem_func__(self.CloseChat))
		chatInputSet.SetReturnEvent(ui.__mem_func__(self.OnEmptyReturn))
		chatInputSet.Hide()
		self.chatInputSet = chatInputSet

	def Destroy(self):
		if self.chatInputSet:
			self.chatInputSet.Destroy()
		self.chatInputSet = None
		if self.scrollBar:
			self.scrollBar.Destroy()
		self.scrollBar = None
		self.logArea = None
		self.tabButtonList = []
		self.btnSendWhisper = None
		self.btnStop = None
		self.btnSettings = None
		self.btnClose = None
		self.titleName = None
		self.corners = []
		self.gameOptionDlg = None
		self.panel = None

	################
	## Yerlesim
	def __ArrangeFlow(self):
		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()
		chat.SetPosition(self.chatID, int(screenWidth * self.FLOW_X), int(screenHeight * self.FLOW_BOTTOM))
		chat.SetHeight(self.chatID, int(screenHeight * (self.FLOW_BOTTOM - self.FLOW_TOP)))

	def __ArrangePanel(self, compact):
		self.compact = compact
		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		panelX = int(screenWidth * self.PANEL_X)
		panelWidth = int(screenWidth * self.PANEL_W)
		if compact:
			panelY = int(screenHeight * self.PANEL_COMPACT_Y)
			panelHeight = int(screenHeight * self.PANEL_COMPACT_H)
		else:
			panelY = int(screenHeight * self.PANEL_Y)
			panelHeight = int(screenHeight * self.PANEL_H)

		self.panel.SetPosition(panelX, panelY)
		self.panel.SetSize(panelWidth, panelHeight)

		r = MobileChatPanel.CORNER
		self.corners[0].SetPosition(0, 0)
		self.corners[1].SetPosition(panelWidth - r, 0)
		self.corners[2].SetPosition(0, panelHeight - r)
		self.corners[3].SetPosition(panelWidth - r, panelHeight - r)

		s = float(panelHeight) / self.MOCK_PANEL_HEIGHT
		pad = self.PAD
		headHeight = max(40, int(44 * s))

		self.titleName.SetPosition(pad + 4, headHeight / 2)

		x = panelWidth - pad - self.ICON_SIZE
		iconY = (headHeight - self.ICON_SIZE) / 2
		self.btnClose.SetPosition(x, iconY)
		x -= self.ICON_SIZE + 8
		self.btnSettings.SetPosition(x, iconY)
		x -= self.STOP_WIDTH + 8
		self.btnStop.SetPosition(x, (headHeight - self.btnStop.GetHeight()) / 2)
		x -= self.ICON_SIZE + 8
		self.btnSendWhisper.SetPosition(x, iconY)

		tabY = headHeight + int(8 * s)
		tabStep = min(self.TAB_WIDTH + self.TAB_GAP, (panelWidth - 2 * pad) / len(self.tabButtonList))
		i = 0
		for btn in self.tabButtonList:
			btn.SetPosition(pad + i * tabStep, tabY)
			i += 1

		inputY = panelHeight - 12 - self.INPUT_HEIGHT
		logTop = tabY + self.TAB_HEIGHT + int(10 * s)
		logBottom = inputY - int(10 * s)
		logHeight = max(30, logBottom - logTop)
		scrollWidth = MobileScrollBar.THUMB_WIDTH

		self.logArea.SetPosition(pad, logTop)
		self.logArea.SetSize(panelWidth - pad - scrollWidth - 8 - 8, logHeight)

		self.scrollBar.SetPosition(panelWidth - 8 - scrollWidth, logTop)
		self.scrollBar.LockScroll()
		self.scrollBar.SetScrollBarSize(logHeight)
		self.scrollBar.UnlockScroll()

		self.chatInputSet.SetPosition(pad, inputY)
		self.chatInputSet.SetSize(panelWidth - 2 * pad, self.INPUT_HEIGHT)
		self.chatInputSet.RefreshPosition()
		self.chatInputSet.SetChatMax(max(20, self.chatInputSet.GetFieldWidth() / 8))

	def __RefreshStopButton(self):
		if self.frozen:
			name = "stop_halt"
			text = self.STOP_TEXT_HALT
		else:
			name = "stop_go"
			text = self.STOP_TEXT_GO
		self.btnStop.SetUpVisual(MOBILE_UI_DIR + name + "_up.tga")
		self.btnStop.SetOverVisual(MOBILE_UI_DIR + name + "_up.tga")
		self.btnStop.SetDownVisual(MOBILE_UI_DIR + name + "_down.tga")
		self.btnStop.SetText(text)
		# yazi yesil/kirmizi noktanin sagina (dugme metni varsayilan ortalanir)
		self.btnStop.ButtonText.SetPosition(self.btnStop.GetWidth() / 2 + 8, self.btnStop.GetHeight() / 2)
		self.btnStop.SetToolTipText(localeInfo.STOP_CHAT)

	################
	## pack API
	def SetPosition(self, x, y):
		ui.Window.SetPosition(self, x, y)

	def SetSize(self, width, height):
		ui.Window.SetSize(self, width, height)

	def SetHeight(self, height):
		pass

	def Refresh(self):
		self.__ArrangeFlow()
		if self.panel and self.panel.IsShow():
			self.__ArrangePanel(self.compact)

	def Show(self):
		ui.Window.Show(self)

	def Hide(self):
		# interfacemodule.HideAllWindows wndChat.Hide() cagirir: acik pencere de kapansin.
		# ui.Window.__init__ kurucuda da Hide() cagirir - boardState henuz yok (bkz. uitaskbar.py).
		if hasattr(self, "boardState") and self.IsEditMode():
			self.CloseChat()
		ui.Window.Hide(self)

	def SetSendWhisperEvent(self, event):
		self.btnSendWhisper.SetEvent(event)

	def SetOpenChatLogEvent(self, event):
		# PC'de sohbet gecmisi (L) dugmesi; mobilde L kisayollar panelinden acilir, API korunur
		self.eventOpenChatLog = event

	def IsEditMode(self):
		if chat.BOARD_STATE_EDIT == self.boardState:
			return True

		return False

	################
	## Open & Close
	def OpenChat(self):
		self.boardState = chat.BOARD_STATE_EDIT
		self.__ArrangePanel(False)
		self.panel.Show()
		self.panel.SetTop()
		self.chatInputSet.Open()
		self.chatInputSet.SetTop()
		if not self.frozen:
			self.__ScrollToEnd()
		if AUTO_FOCUS_ON_OPEN:
			self.chatInputSet.SetChatFocus()
		self.SetTop()

	def CloseChat(self):
		self.boardState = chat.BOARD_STATE_VIEW
		self.chatInputSet.Close()
		self.panel.Hide()
		self.compact = False

	def SetChatFocus(self):
		if self.IsEditMode():
			self.chatInputSet.SetChatFocus()

	def BindInterface(self, interface):
		self.interface = interface
		self.chatInputSet.BindInterface(interface)
		self.logArea.BindInterface(interface)

	def OnChangeChatMode(self):
		self.chatInputSet.OnChangeChatMode()

	################
	## Olaylar
	def OnChatLineFocus(self, flag):
		# yazilim klavyesi: pencereyi ust yariya cek / geri getir
		if not KEYBOARD_COMPACT:
			return
		if not self.IsEditMode():
			return
		if flag != self.compact:
			self.__ArrangePanel(flag)

	def OnEmptyReturn(self):
		# bos satirda Enter: PC sohbet satirini kapatir; mobilde yalniz klavye kapanir
		self.chatInputSet.KillChatFocus()

	def OnClickTab(self, index):
		self.curTab = index
		i = 0
		for btn in self.tabButtonList:
			if i != index:
				btn.SetUp()
			i += 1

		(name, mode) = self.TAB_LIST[index]
		if None == mode:
			for eachMode in self.CHAT_MODE_INDEX:
				chat.EnableChatMode(self.logID, eachMode)
		else:
			for eachMode in self.CHAT_MODE_INDEX:
				chat.DisableChatMode(self.logID, eachMode)
			chat.EnableChatMode(self.logID, mode)
			# sekme gonderilebilir bir kipse yazma kipi de o olsun
			self.chatInputSet.SetChatMode(mode)

		self.titleName.SetText(name)
		if not self.frozen:
			self.__ScrollToEnd()

	def OnClickStop(self):
		self.frozen = not self.frozen
		if self.frozen:
			self.frozenEndLine = self.__GetEndLine(self.scrollBar.GetPos())
		else:
			self.__ScrollToEnd()
		self.__RefreshStopButton()

	def OnClickSettings(self):
		# uisystem.py SystemDialog.__ClickGameOptionButton ile ayni pencere
		try:
			if not self.gameOptionDlg:
				import uiGameOption
				self.gameOptionDlg = uiGameOption.OptionDialog()
			self.gameOptionDlg.Show()
			self.gameOptionDlg.SetTop()
		except:
			import dbg
			dbg.TraceError("ChatWindow.OnClickSettings - uiGameOption.OptionDialog acilamadi")

	def OnScroll(self):
		self.scrollBarPos = self.scrollBar.GetPos()
		chat.SetEndPos(self.logID, self.scrollBarPos)
		if self.frozen:
			self.frozenEndLine = self.__GetEndLine(self.scrollBarPos)

	def OnTop(self):
		if self.panel and self.panel.IsShow():
			self.panel.SetTop()

	################
	## Dondurma (chat.ArrangeShowingChat'in iEndLine hesabinin tersi ile son satir sabit)
	def __GetFitLineCount(self):
		# ArrangeShowingChat: (m_iHeight + m_iStep) / m_iStep, m_iHeight = alan yuksekligi - step
		height = self.logArea.GetHeight()
		step = chat.GetLineStep(self.logID)
		return height / step

	def __GetEndLine(self, pos):
		lineCount = chat.GetLineCount(self.logID)
		visible = min(lineCount, self.__GetFitLineCount())
		return visible + int(float(lineCount - visible - 1) * pos)

	def __ScrollToEnd(self):
		chat.SetEndPos(self.logID, 1.0)
		self.scrollBar.LockScroll()
		self.scrollBar.SetPos(1.0)
		self.scrollBar.UnlockScroll()
		self.scrollBarPos = 1.0

	def UpdateFreeze(self):
		if not self.frozen:
			return
		lineCount = chat.GetLineCount(self.logID)
		visible = min(lineCount, self.__GetFitLineCount())
		denom = lineCount - visible - 1
		if denom <= 0:
			pos = 1.0
		else:
			pos = float(self.frozenEndLine - visible) / float(denom)
		pos = max(0.0, min(1.0, pos))
		chat.SetEndPos(self.logID, pos)
		self.scrollBar.LockScroll()
		self.scrollBar.SetPos(pos)
		self.scrollBar.UnlockScroll()
		self.scrollBarPos = pos

	##########
	## Kisa akis (pack ChatWindow BOARD_STATE_VIEW ile ayni: systemSetting.IsViewChat)
	def OnUpdate(self):
		if systemSetting.IsViewChat():
			chat.Update(self.chatID)

	def OnRender(self):
		if systemSetting.IsViewChat():
			if chat.GetVisibleLineCount(self.chatID) > 0:
				screenWidth = wndMgr.GetScreenWidth()
				screenHeight = wndMgr.GetScreenHeight()
				lines = chat.GetVisibleLineCount(self.chatID)
				bottom = int(screenHeight * self.FLOW_BOTTOM)
				top = bottom - lines * self.MOBILE_CHAT_STEP - 6
				grp.SetColor(self.FLOW_BG_COLOR)
				grp.RenderBar(int(screenWidth * self.FLOW_X) - 6, top, int(screenWidth * self.FLOW_W), bottom - top + 2)
			chat.Render(self.chatID)

## ChatLogWindow (pack ile ayni)
class ChatLogWindow(ui.Window):

	BLOCK_WIDTH = 32
	CHAT_MODE_NAME = ( localeInfo.CHAT_NORMAL, localeInfo.CHAT_PARTY, localeInfo.CHAT_GUILD, localeInfo.CHAT_SHOUT, localeInfo.CHAT_INFORMATION, localeInfo.CHAT_NOTICE, )
	CHAT_MODE_INDEX = ( chat.CHAT_TYPE_TALKING,
						chat.CHAT_TYPE_PARTY,
						chat.CHAT_TYPE_GUILD,
						chat.CHAT_TYPE_SHOUT,
						chat.CHAT_TYPE_INFO,
						chat.CHAT_TYPE_NOTICE, )

	CHAT_LOG_WINDOW_MINIMUM_WIDTH = 450
	CHAT_LOG_WINDOW_MINIMUM_HEIGHT = 120

	class ResizeButton(ui.DragButton):

		def __init__(self):
			ui.DragButton.__init__(self)

		def __del__(self):
			ui.DragButton.__del__(self)

		def OnMouseOverIn(self):
			app.SetCursor(app.HVSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

	def __init__(self):

		self.allChatMode = True
		self.chatInputSet = None

		ui.Window.__init__(self)
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)	# MOBIL: bu pencere zaten mobil geometrili, genel olcek disi
		self.AddFlag("float")
		self.AddFlag("movable")
		self.SetWindowName("ChatLogWindow")
		self.__CreateChatInputSet()
		self.__CreateWindow()
		self.__CreateButton()
		self.__CreateScrollBar()

		self.chatID = chat.CreateChatSet(chat.CHAT_SET_LOG_WINDOW)
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_LOG)
		for i in self.CHAT_MODE_INDEX:
			chat.EnableChatMode(self.chatID, i)

		self.SetPosition(20, 20)
		self.SetSize(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH, self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT)
		self.btnSizing.SetPosition(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH-self.btnSizing.GetWidth(), self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT-self.btnSizing.GetHeight()+2)

		self.OnResize()

	def __CreateChatInputSet(self):
		chatInputSet = ChatInputSet()
		chatInputSet.SetParent(self)
		chatInputSet.SetEscapeEvent(ui.__mem_func__(self.Close))
		chatInputSet.SetWindowVerticalAlignBottom()
		chatInputSet.Open()
		self.chatInputSet = chatInputSet

	def __CreateWindow(self):
		imgLeft = ui.ImageBox()
		imgLeft.AddFlag("not_pick")
		imgLeft.SetParent(self)

		imgCenter = ui.ExpandedImageBox()
		imgCenter.AddFlag("not_pick")
		imgCenter.SetParent(self)

		imgRight = ui.ImageBox()
		imgRight.AddFlag("not_pick")
		imgRight.SetParent(self)

		if localeInfo.IsARABIC():
			imgLeft.LoadImage("locale/ae/ui/pattern/titlebar_left.tga")
			imgCenter.LoadImage("locale/ae/ui/pattern/titlebar_center.tga")
			imgRight.LoadImage("locale/ae/ui/pattern/titlebar_right.tga")
		else:
			imgLeft.LoadImage("d:/ymir work/ui/pattern/chatlogwindow_titlebar_left.tga")
			imgCenter.LoadImage("d:/ymir work/ui/pattern/chatlogwindow_titlebar_middle.tga")
			imgRight.LoadImage("d:/ymir work/ui/pattern/chatlogwindow_titlebar_right.tga")

		imgLeft.Show()
		imgCenter.Show()
		imgRight.Show()

		btnClose = ui.Button()
		btnClose.SetParent(self)
		btnClose.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		btnClose.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		btnClose.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		btnClose.SetToolTipText(localeInfo.UI_CLOSE, 0, -23)
		btnClose.SetEvent(ui.__mem_func__(self.Close))
		btnClose.Show()

		btnSizing = self.ResizeButton()
		btnSizing.SetParent(self)
		btnSizing.SetMoveEvent(ui.__mem_func__(self.OnResize))
		btnSizing.SetSize(16, 16)
		btnSizing.Show()

		titleName = ui.TextLine()
		titleName.SetParent(self)

		if localeInfo.IsARABIC():
			titleName.SetPosition(self.GetWidth()-20, 6)
		else:
			titleName.SetPosition(20, 6)

		titleName.SetText(localeInfo.CHAT_LOG_TITLE)
		titleName.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.btnClose = btnClose
		self.btnSizing = btnSizing
		self.titleName = titleName

	def __CreateButton(self):

		if localeInfo.IsARABIC():
			bx = 20
		else:
			bx = 13

		btnAll = ui.RadioButton()
		btnAll.SetParent(self)
		btnAll.SetPosition(bx, 24)
		btnAll.SetUpVisual("d:/ymir work/ui/public/xsmall_button_01.sub")
		btnAll.SetOverVisual("d:/ymir work/ui/public/xsmall_button_02.sub")
		btnAll.SetDownVisual("d:/ymir work/ui/public/xsmall_button_03.sub")
		btnAll.SetText(localeInfo.CHAT_ALL)
		btnAll.SetEvent(ui.__mem_func__(self.ToggleAllChatMode))
		btnAll.Down()
		btnAll.Show()
		self.btnAll = btnAll

		x = bx + 48
		i = 0
		self.modeButtonList = []
		for name in self.CHAT_MODE_NAME:
			btn = ui.ToggleButton()
			btn.SetParent(self)
			btn.SetPosition(x, 24)
			btn.SetUpVisual("d:/ymir work/ui/public/xsmall_button_01.sub")
			btn.SetOverVisual("d:/ymir work/ui/public/xsmall_button_02.sub")
			btn.SetDownVisual("d:/ymir work/ui/public/xsmall_button_03.sub")
			btn.SetText(name)
			btn.Show()

			mode = self.CHAT_MODE_INDEX[i]
			btn.SetToggleUpEvent(lambda arg=mode: self.ToggleChatMode(arg))
			btn.SetToggleDownEvent(lambda arg=mode: self.ToggleChatMode(arg))
			self.modeButtonList.append(btn)

			x += 48
			i += 1

	def __CreateScrollBar(self):
		scrollBar = ui.SmallThinScrollBar()
		scrollBar.SetParent(self)
		scrollBar.Show()
		scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.scrollBar = scrollBar
		self.scrollBarPos = 1.0

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.imgLeft = None
		self.imgCenter = None
		self.imgRight = None
		self.btnClose = None
		self.btnSizing = None
		self.modeButtonList = []
		self.scrollBar = None
		self.chatInputSet = None

	def ToggleAllChatMode(self):
		if self.allChatMode:
			return

		self.allChatMode = True

		for i in self.CHAT_MODE_INDEX:
			chat.EnableChatMode(self.chatID, i)
		for btn in self.modeButtonList:
			btn.SetUp()

	def ToggleChatMode(self, mode):
		if self.allChatMode:
			self.allChatMode = False
			for i in self.CHAT_MODE_INDEX:
				chat.DisableChatMode(self.chatID, i)
			chat.EnableChatMode(self.chatID, mode)
			self.btnAll.SetUp()

		else:
			chat.ToggleChatMode(self.chatID, mode)

	def SetSize(self, width, height):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)

		if localeInfo.IsARABIC():
			self.titleName.SetPosition(self.GetWidth()-20, 3)
			self.btnClose.SetPosition(3, 3)
			self.scrollBar.SetPosition(1, 45)
		else:
			self.btnClose.SetPosition(width - self.btnClose.GetWidth() - 5, 5)
			self.scrollBar.SetPosition(width - 15, 45)

		self.scrollBar.SetScrollBarSize(height - 45 - 12)
		self.scrollBar.SetPos(self.scrollBarPos)
		ui.Window.SetSize(self, width, height)

	def Open(self):
		self.OnResize()
		self.chatInputSet.SetChatFocus()
		self.Show()

	def Close(self):
		if self.chatInputSet:
			self.chatInputSet.KillChatFocus()
		self.Hide()

	def OnResize(self):
		x, y = self.btnSizing.GetLocalPosition()
		width = self.btnSizing.GetWidth()
		height = self.btnSizing.GetHeight()

		if x < self.CHAT_LOG_WINDOW_MINIMUM_WIDTH - width:
			self.btnSizing.SetPosition(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH - width, y)
			return
		if y < self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT - height:
			self.btnSizing.SetPosition(x, self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT - height)
			return

		self.scrollBar.LockScroll()
		self.SetSize(x + width, y + height)
		self.scrollBar.UnlockScroll()

		if localeInfo.IsARABIC():
			self.chatInputSet.SetPosition(20, 25)
		else:
			self.chatInputSet.SetPosition(0, 25)

		self.chatInputSet.SetSize(self.GetWidth() - 20, 20)
		self.chatInputSet.RefreshPosition()
		self.chatInputSet.SetChatMax(self.GetWidth() / 8)

	def OnScroll(self):
		self.scrollBarPos = self.scrollBar.GetPos()

		lineCount = chat.GetLineCount(self.chatID)
		visibleLineCount = chat.GetVisibleLineCount(self.chatID)
		endLine = visibleLineCount + int(float(lineCount - visibleLineCount) * self.scrollBarPos)

		chat.SetEndPos(self.chatID, self.scrollBarPos)

	def OnRender(self):
		(x, y, width, height) = self.GetRect()

		if localeInfo.IsARABIC():
			grp.SetColor(0x77000000)
			grp.RenderBar(x+2, y+45, 13, height-45)

			grp.SetColor(0x77000000)
			grp.RenderBar(x, y, width, height)
			grp.SetColor(0x77000000)
			grp.RenderBox(x, y, width-2, height)
			grp.SetColor(0x77000000)
			grp.RenderBox(x+1, y+1, width-2, height)

			grp.SetColor(0xff989898)
			grp.RenderLine(x+width-13, y+height-1, 11, -11)
			grp.RenderLine(x+width-9, y+height-1, 7, -7)
			grp.RenderLine(x+width-5, y+height-1, 3, -3)
		else:
			grp.SetColor(0x77000000)
			grp.RenderBar(x+width-15, y+45, 13, height-45)

			grp.SetColor(0x77000000)
			grp.RenderBar(x, y, width, height)
			grp.SetColor(0x77000000)
			grp.RenderBox(x, y, width-2, height)
			grp.SetColor(0x77000000)
			grp.RenderBox(x+1, y+1, width-2, height)

			grp.SetColor(0xff989898)
			grp.RenderLine(x+width-13, y+height-1, 11, -11)
			grp.RenderLine(x+width-9, y+height-1, 7, -7)
			grp.RenderLine(x+width-5, y+height-1, 3, -3)

		#####

		chat.ArrangeShowingChat(self.chatID)

		if localeInfo.IsARABIC():
			chat.SetPosition(self.chatID, x + width - 10, y + height - 25)
		else:
			chat.SetPosition(self.chatID, x + 10, y + height - 25)

		chat.SetHeight(self.chatID, height - 45 - 25)
		chat.Update(self.chatID)
		chat.Render(self.chatID)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def BindInterface(self, interface):
		self.interface = interface

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			if app.IsPressed(app.DIK_LALT):
				link = chat.GetLinkFromHyperlink(hyperlink)
				ime.PasteString(link)
			else:
				self.interface.MakeHyperlinkTooltip(hyperlink)
