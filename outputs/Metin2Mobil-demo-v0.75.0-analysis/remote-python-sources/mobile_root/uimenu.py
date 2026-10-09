# MOBIL KAPLAMA (mobile_root/uimenu.py): pack root/uimenu.py yerine.
# KULLANICI (2026-10-02): "toplu nesne islemleri envanterini kaldir" -> SOL_MENU'den 'Toplu Islemler' kaldirildi.
# KULLANICI (2026-10-03): "Averos2 Hizli Menu" - klasik yeniden tasarim (prototip A: Desktop/Averos2-HizliMenu-Prototip/
#   hizli_menu.html, "mukemmel oldu uygula"). Pencere uiscript/menuwindow.py kaplamasi (304 x 280, ui.Board + ui.TitleBar).
#   Her satir TEK pisirilmis dugme: mobile/ui/hzm/satir<i>_up|down.png = middle_button kabartma + sekizgen yuva + HD ikon +
#   ad + kisa aciklama + altin ok (tools/hizlimenu/bake_hizlimenu.py). Gorseller 1 pencere birimi = 2.769 fiziksel px
#   (kok olcegi 1.6 x 1220/705) pisirildi; SetButtonScale ile 280 x 52 birime iner -> telefonda yazilar keskin.
#   Islevler (OpenGui) eskisiyle AYNI: Biyolog / Oto Bagirma / Offline Shop / Battle Pass; secince menu kapanir.
# Metinler cp1254 kacisli ASCII kaynak.
import ui
import net
import wndMgr

DIR = "mobile/ui/hzm/"
ROW_W, ROW_H = 280, 52				# pencere birimi
## TELEFONDA OLCULDU (2026-10-01, zindan/oyuncu karti): mobile/ .png icin GetWidth yukleme aninda 0 donebilir ->
## pisirilmis boyut SABIT (bake_hizlimenu.py ile AYNI).
ROW_TEX_W, ROW_TEX_H = 775, 144
ROW_X, ROW_Y, ROW_STEP = 12, 40, 58
## KULLANICI (2026-10-03): "Averos2 Hizli Menu yazisi kucuk, silik, net degil; 1 tik buyusun, okunakli olsun" -> seridin gri
## TextLine'i gizlenir, yerine pisirilmis baslik (kalin 15 birim, krem + koyu dis cizgi): serit boyunda tuval, yazi ortada.
TITLE_X, TITLE_Y, TITLE_W, TITLE_H = 8, 8, 288, 23
TITLE_TEX_W, TITLE_TEX_H = 797, 64

class MenuWindow(ui.ScriptWindow):

	# OpenGui sirasi (pisirilmis satir gorselleri de bu sirada: satir0..3)
	SOL_MENU = {
		0 : ["Biyolog", "icon/item/30006.tga"],
		1 : ["Oto Ba\xf0\xfdrma", "icon/item/70028.tga"],
		2 : ["Offline Shop", "icon/item/50200.tga"],
		3 : ["Battle Pass", "icon/item/70032.tga"],
		}

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.titleBar = None
		self.board = None
		self.titleImg = None
		self.interface = None
		self.tab = {}

	def __Load(self):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, "uiscript/menuwindow.py")
			self.titleBar = self.GetChild("titlebar")
			self.board = self.GetChild("board")
		except:
			import exception
			exception.Abort("MenuDialog.__Load")

		self.SetCenterPosition()
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		for i in xrange(len(self.SOL_MENU)):
			self.__MakeRow(i)
		self.__MakeTitle()

	def __MakeTitle(self):
		img = ui.ExpandedImageBox()
		img.SetParent(self.board)
		img.AddFlag("not_pick")			# X dugmesine dokunma gecsin
		img.LoadImage(DIR + "baslik.png")
		img.SetScale(float(TITLE_W) / TITLE_TEX_W, float(TITLE_H) / TITLE_TEX_H)
		img.SetPosition(TITLE_X, TITLE_Y)
		img.Show()
		self.titleImg = img
		try:
			self.GetChild("titlename").Hide()		# eski gri yazi (yerlesimde yedek olarak duruyor)
		except:
			pass

	def __MakeRow(self, index):
		b = ui.Button()
		b.SetParent(self.board)
		b.SetUpVisual(DIR + "satir%d_up.png" % index)
		b.SetOverVisual(DIR + "satir%d_up.png" % index)
		b.SetDownVisual(DIR + "satir%d_down.png" % index)
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, float(ROW_W) / ROW_TEX_W, float(ROW_H) / ROW_TEX_H)
		b.SetPosition(ROW_X, ROW_Y + ROW_STEP * index)
		b.SetEvent(ui.__mem_func__(self.OpenGui), index)
		b.Show()
		self.tab[index] = b

	def BindInterface(self, interface):
		self.interface = interface

	def OpenGui(self, arg):
		if not self.interface:
			return True
		if int(arg) == 0:
			self.interface.OpenBiyologTable()
		elif int(arg) == 1:
			self.interface.OpenShoutWindow()
		elif int(arg) == 2:
			self.interface.OpenOfflineShop()
		elif int(arg) == 3:
			net.SendChatPacket("/open_battlepass")
		self.Close()
		return True

	def Destroy(self):
		self.ClearDictionary()
		self.__Initialize()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		self.Hide()
