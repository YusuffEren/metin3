# MOBIL KAPLAMA (mobile_root/uiemojiwheel.py) - yalniz telefon.
# KULLANICI (2026-09-15): PC'de CTRL + 1..9 ile kafa ustu emoji (game.py __PressNumKey ->
# chrmgr.SetEmoticon + net.SendEmoticon); mobilde tus yok. HUD'da "Emoji" dugmesi: basili tutup
# herhangi bir yone cekince emoji halkasi acilir, parmagi bir emojinin ustunde birakinca gonderilir.
# Dokunup birakinca halka acik kalir; emojiye dokun = gonder, disari/ortaya dokun = kapat.
# Emoji listesi playersettingmodule.py EFFECT_EMOTICON+0..11 sirasi (sweat .. fish).
import ui
import wndMgr
import chrmgr
import net
import math

IMG = "mobile/ui/emo/"
COUNT = 12
WHEEL_R = 150			# halka dis yaricapi (ekran px, gorev cubugu olcegi 1.0)
BG_TEX = 512.0			# wheel_bg.tga (dis yaricap 250, ic 100 doku px)
INNER_R = int(100 * WHEEL_R * 2 / BG_TEX)	# ~58
ICON_RING = (INNER_R + WHEEL_R - 4) / 2		# ikon merkezlerinin yaricapi
ICON = 54
DRAG_START = 18			# bu kadar cekilmeden birakilirsa "dokunma" sayilir (halka acik kalir)


def SendEmoticon(index):
	## game.py __PressNumKey ile birebir
	if chrmgr.IsPossibleEmoticon(-1):
		chrmgr.SetEmoticon(-1, index)
		net.SendEmoticon(index)


class EmojiWheel(ui.Window):
	def __init__(self):
		ui.Window.__init__(self, "TOP_MOST")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetPosition(0, 0)
		self.cx = 0
		self.cy = 0
		self.sel = -1
		self.tapMode = False

		bg = ui.ExpandedImageBox()
		bg.SetParent(self)
		bg.AddFlag("not_pick")
		bg.LoadImage(IMG + "wheel_bg.tga")
		s = WHEEL_R * 2 / BG_TEX
		bg.SetScale(s, s)
		bg.Show()
		self.bg = bg

		glow = ui.ExpandedImageBox()
		glow.SetParent(self)
		glow.AddFlag("not_pick")
		glow.LoadImage(IMG + "glow.tga")
		gs = (ICON + 26) / 128.0
		glow.SetScale(gs, gs)
		glow.Hide()
		self.glow = glow

		self.icons = []
		for i in xrange(COUNT):
			ic = ui.ExpandedImageBox()
			ic.SetParent(self)
			ic.AddFlag("not_pick")
			ic.LoadImage(IMG + "emo_%02d.tga" % i)
			ic.SetScale(ICON / 128.0, ICON / 128.0)
			ic.Show()
			self.icons.append(ic)

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.Hide()
		self.icons = []
		self.bg = None
		self.glow = None

	def __IconPos(self, i):
		a = math.radians(-90 + 30 * i)
		return (self.cx + math.cos(a) * ICON_RING, self.cy + math.sin(a) * ICON_RING)

	def OpenAt(self, x, y):
		sw = wndMgr.GetScreenWidth()
		sh = wndMgr.GetScreenHeight()
		m = WHEEL_R + 6
		self.cx = int(max(m, min(sw - m, x)))
		self.cy = int(max(m, min(sh - m, y)))
		self.bg.SetPosition(self.cx - WHEEL_R, self.cy - WHEEL_R)
		for i in xrange(COUNT):
			(ix, iy) = self.__IconPos(i)
			self.icons[i].SetPosition(int(ix - ICON / 2), int(iy - ICON / 2))
		self.sel = -1
		self.tapMode = False
		self.glow.Hide()
		self.Show()
		self.SetTop()

	def Close(self):
		self.sel = -1
		self.tapMode = False
		self.Hide()

	def PickAt(self, x, y):
		## parmak konumundan emoji dilimi; ic daire (iptal) ve halka disinin cok uzagi -1
		dx = x - self.cx
		dy = y - self.cy
		d = math.sqrt(dx * dx + dy * dy)
		if d < INNER_R:
			return -1
		if self.tapMode and d > WHEEL_R + 20:
			return -1
		ang = math.degrees(math.atan2(dy, dx)) + 90.0	# 0 = yukari, saat yonu
		return int(math.floor((ang + 15.0) / 30.0)) % COUNT

	def SetSelected(self, sel):
		if sel == self.sel:
			return
		self.sel = sel
		if sel < 0:
			self.glow.Hide()
			return
		(ix, iy) = self.__IconPos(sel)
		gw = int((ICON + 26))
		self.glow.SetPosition(int(ix - gw / 2), int(iy - gw / 2))
		self.glow.Show()
		self.icons[sel].SetTop()

	## dokunma kipi: halka acik, emojiye dokun -> gonder, baska yere -> kapat
	def OnMouseLeftButtonDown(self):
		if self.tapMode:
			(x, y) = wndMgr.GetMousePosition()
			self.SetSelected(self.PickAt(x, y))
		return True

	def OnMouseLeftButtonUp(self):
		if not self.tapMode:
			return True
		(x, y) = wndMgr.GetMousePosition()
		sel = self.PickAt(x, y)
		self.Close()
		if sel >= 0:
			SendEmoticon(sel)
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True


class EmojiTouchArea(ui.Window):
	"""HUD Emoji dugmesinin ustunde gorunmez dokunma alani (ZoomTouchArea ile ayni desen: sol tus
	yakalamasi bu pencerede kalir, parmak disari kaysa da OnMouseLeftButtonUp gelir)."""

	def __init__(self, image, upImage, downImage):
		ui.Window.__init__(self, "UI_BOTTOM")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.image = image
		self.upImage = upImage
		self.downImage = downImage
		self.wheel = EmojiWheel()
		self.wheel.Hide()
		self.pressed = False
		self.startX = 0
		self.startY = 0
		self.dragged = False
		self.imgScale = 46.0 / 128.0

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		if self.wheel:
			self.wheel.Destroy()
		self.wheel = None
		self.image = None

	def __SetDown(self, down):
		if self.image:
			self.image.LoadImage(self.downImage if down else self.upImage)	# LoadImage boyu doku boyuna (128) dondurur
			self.image.SetScale(self.imgScale, self.imgScale)	# LoadImage olcegi sifirliyor (buton 128 px'e buyuyordu)

	def OnMouseLeftButtonDown(self):
		if not self.wheel:
			return True
		if self.wheel.IsShow():
			self.wheel.Close()
		(x, y) = wndMgr.GetMousePosition()
		self.startX = x
		self.startY = y
		self.pressed = True
		self.dragged = False
		self.__SetDown(True)
		(gx, gy) = self.GetGlobalPosition()
		self.wheel.OpenAt(gx + self.GetWidth() / 2, gy + self.GetHeight() / 2)
		return True

	def OnMouseLeftButtonUp(self):
		if not self.pressed:
			return True
		self.pressed = False
		self.__SetDown(False)
		if not self.wheel:
			return True
		(x, y) = wndMgr.GetMousePosition()
		if not self.dragged:
			self.wheel.tapMode = True	# dokundu, cekmedi: halka acik kalir
			return True
		sel = self.wheel.PickAt(x, y)
		self.wheel.Close()
		if sel >= 0:
			SendEmoticon(sel)
		return True

	def OnUpdate(self):
		if not self.pressed or not self.wheel:
			return
		(x, y) = wndMgr.GetMousePosition()
		dx = x - self.startX
		dy = y - self.startY
		if not self.dragged and dx * dx + dy * dy > DRAG_START * DRAG_START:
			self.dragged = True
		if self.dragged:
			self.wheel.SetSelected(self.wheel.PickAt(x, y))

	## "Butonlari Ozellestir" (uiMobileLayout follow): dokunma alani gorselin ustunde, 6 px pay; olcek korunur
	def FollowImage(self, img):
		self.image = img
		try:
			self.imgScale = img.GetWidth() / 128.0
		except:
			pass
		(ix, iy) = img.GetGlobalPosition()
		self.SetPosition(ix - 6, iy - 6)
		self.SetSize(img.GetWidth() + 12, img.GetHeight() + 12)
