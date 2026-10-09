# MOBIL (yalniz kaplama; PC'de yok): BECERI PENCERESI YAN DUGMELERI - "Duzenle" + "Hizli Aktar".
# KULLANICI (2026-09-28): "beceri penceresinin sag cercevesine yapisik 'Duzenle' dugmesi; basinca sagdaki beceri
#   kutulari animasyonlu ipucu gibi yer degistirsin, yanlarinda yer degistir isareti ciksin; Hizli Aktar da yanina,
#   calisir olsun" (onceki Hizli Aktar 'Standart Beceriler' seridinin icindeydi - serit dokunus almiyordu).
# Dugmeler karakter penceresinin DISINDA (sag cerceveye yapisik) -> cocuk olsalardi kok dikdortgeni disinda
# secilemezlerdi; bu yuzden AYRI kok pencere, her kare pencereyi izler. Yalniz Yetenekler sekmesinde gorunur.
# Yer degistirme modu uitaskbar.TaskBar.MobileSwapMode (dokun-dokun: once kaynak, sonra hedef kutu).
import ui
import wndMgr

BTN_IMG = ("mobile/ui/tbbtn_up.tga", "mobile/ui/tbbtn_over.tga", "mobile/ui/tbbtn_down.tga")	# 106x23 topuzlu deri
BTN_SCALE = 2.0		# KULLANICI (2026-09-28): "dugmeler cok kucuk, gozukmuyor" (1.25 -> 2.0)
FONT = "Tahoma:21"


class SkillSideBar(ui.Window):

	def __init__(self, charWnd):
		ui.Window.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("MobileSkillSideBar")
		self.AddFlag("float")
		self.charWnd = charWnd
		self.btns = []
		self.btnEdit = self.__Btn("D\xfczenle", self.__OnEdit)
		self.btnFill = self.__Btn("H\xfdzl\xfd Aktar", self.__OnFill)
		## KULLANICI (2026-09-28): "kutuya ekledigimiz beceriyi kaldiramiyoruz" -> Duzenle modunda 3. dugme "Kaldir":
		## once kutuya dokun (secilir), sonra Kaldir -> kutu bosalir
		self.btnDel = self.__Btn("Kald\xfdr", self.__OnDel)
		w = self.btnEdit.GetWidth()
		h = self.btnEdit.GetHeight()
		self.btnEdit.SetPosition(0, 0)
		self.btnFill.SetPosition(0, h + 8)
		self.btnDel.SetPosition(0, 2 * (h + 8))
		self.btnDel.Hide()
		self.SetSize(w, 3 * h + 16)
		self.Hide()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.__ExitSwap()
		self.Hide()
		self.btns = []
		self.charWnd = None

	def __Btn(self, text, fn):
		b = ui.Button()
		b.SetParent(self)
		b.SetUpVisual(BTN_IMG[0])
		b.SetOverVisual(BTN_IMG[1])
		b.SetDownVisual(BTN_IMG[2])
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, BTN_SCALE, BTN_SCALE)
		b.SetText(text)
		if b.ButtonText:
			b.ButtonText.SetFontName(FONT)
			b.ButtonText.SetFontColor(1.0, 0.93, 0.78)
			b.ButtonText.SetVerticalAlignCenter()
			b.ButtonText.SetHorizontalAlignCenter()
			b.ButtonText.SetPosition(b.GetWidth() / 2, b.GetHeight() / 2 - 2)
		b.SetEvent(ui.__mem_func__(fn))
		b.Show()
		self.btns.append(b)
		return b

	def __TaskBar(self):
		try:
			import uiTaskBar
			return uiTaskBar.MOBILE_TASKBAR[0]
		except:
			return None

	def __OnEdit(self):
		tb = self.__TaskBar()
		if not tb:
			return
		on = not tb.MobileIsSwapMode()
		tb.MobileSwapMode(on)
		self.btnEdit.SetText(on and "Bitti" or "D\xfczenle")
		if on:
			self.btnDel.Show()
		else:
			self.btnDel.Hide()

	def __OnDel(self):
		tb = self.__TaskBar()
		if tb and tb.MobileIsSwapMode():
			tb.MobileSwapRemoveSelected()

	def __ExitSwap(self):
		tb = self.__TaskBar()
		if tb and tb.MobileIsSwapMode():
			tb.MobileSwapMode(False)
		try:
			self.btnEdit.SetText("D\xfczenle")
			self.btnDel.Hide()
		except:
			pass

	def __OnFill(self):
		try:
			self.charWnd.MobileQuickTransfer()
		except:
			import dbg, traceback
			dbg.TraceError("MOBIL Hizli Aktar: " + traceback.format_exc())

	def OnUpdate(self):
		self.Follow()		# karakter penceresi kapaninca (onun OnUpdate'i durur) burada gizlenir

	def Follow(self):
		## karakter penceresinin OnUpdate'inden her kare cagrilir
		c = self.charWnd
		if not c:
			return
		show = False
		try:
			show = c.IsShow() and c.state == "SKILL"
		except:
			show = False
		if not show:
			if self.IsShow():
				self.Hide()
				self.__ExitSwap()
			return
		try:
			sc = wndMgr.GetUIScale(c.hWnd)
		except:
			sc = 1.0
		(x, y) = c.GetGlobalPosition()
		self.SetPosition(x + int(c.GetWidth() * sc) - 4, y + int(56 * sc))
		if not self.IsShow():
			self.Show()
			self.SetTop()
