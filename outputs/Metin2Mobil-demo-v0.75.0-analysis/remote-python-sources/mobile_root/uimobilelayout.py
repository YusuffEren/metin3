# MOBIL (yalniz kaplama; PC'de yok): DUGME DUZENI - Ayarlar > "Butonlari Ozellestir".
# KULLANICI (2026-09-14): Unity projesi Metin2MobileUI.cs / Metin2UiEditHandle.cs ile AYNI tasarim:
#   * Panel ekranin UST ORTASINDA (240x60 Unity birimi): [Duzenle] [Sifirla]. "Duzenle"ye basinca
#     duzenleme baslar, dugme "Kaydet" olur; "Kaydet" duzenlemeyi bitirir ve paneli KAPATIR.
#   * Duzenleme ACIKKEN ekran %55 kararir (EditDim), her duzenlenebilir oge ARKASINDA 1.35x buyuklugunde
#     NEFES ALAN altin hale (3 sn periyot, alpha 0..0.5); secili ogede hale sabit (0.35*0.5).
#   * Surukleme tasir; SADECE SECILI ogenin yaninda, ogeden uzaga (dir yonunde) dikey istiflenmis iki
#     "madeni para" dugmesi (+ ustte, - altta, 46 birim): adim 0.12, 0.4..2.2.
#   * Sifirla: kodun hesapladigi GUNCEL varsayilan konum/boyut.
#   * Saldiri topu native dokunmatik katmandadir (view 249); ayni kipte app.SetTouchElementPos/Scale ile
#     tasinir/boyutlanir, konumu native mobile_layout.json'a yazilir (app.SetTouchEditMode(0) kaydeder).
# Unity birimi -> mantiksal px: x 705/525 = 1.343 (Unity canvas 525 yuksek, bizim HUD 705 mantiksal).
# Kayit: <veri koku>/mobile_hud_layout.cfg (satir: anahtar cx cy s; cihazda json paketi eksik) - guncellemede silinmez.
# Kayit birimi: oge MERKEZI ekran oranlari (cx, cy 0..1) + olcek carpani s.
import ui
import wndMgr
import app
import dbg
import math

LAYOUT_FILE = "mobile_hud_layout.cfg"
# KULLANICI (2026-09-15): baska telefonda eski kayitli duzen (Kisayol eski yerinde) yeni Menu dugmesiyle ust uste
# bindi -> varsayilan duzen degisince surum artar, eski surumlu kayit YOK SAYILIR (dosya silinir).
LAYOUT_VERSION = 5
## KULLANICI (2026-10-02): ust siradan "Sil" kalkti, soldaki 5 dugme bir saga kaydi -> v2/v3 kayitlarda ust sira
## ogeleri ATILIR (yeni varsayilan gecerli), diger kisisel duzen (beceri yayi, At, Z, Emoji...) korunur.
## KULLANICI (2026-10-03): ust siradan "Kisayol" da kalkti, soldaki 5 dugme yine bir saga kaydi -> v4 kayitlar da ayni
## sekilde okunur (surum 5).
## KULLANICI (2026-09-28): ust menu sirasi mini haritaya yaklastirildi (uiscript/mobilehud.py TOP_X, saga bagli).
## Duzenleyicide "Kaydet" TUM ogeleri yazdigindan eski (v2) kayitlarda ust sira ESKI konumda kalip yeni varsayilani
## eziyordu -> v2 kayit YALNIZ ust sira ogeleri atilarak okunur (becerit/At/Z/Emoji... kisisel duzen korunur).
LAYOUT_V2_DROP = ("chat", "chr", "inv", "msg", "sys", "del", "keys", "menu")
STEP = 0.12
SMIN = 0.4
SMAX = 2.2
U = 705.0 / 525.0		# Unity birimi -> mantiksal px
GLOW_PERIOD = 3.0		# sn
COIN = int(round(46 * U))		# 62 px madeni para
COIN_IMG = 128.0
COIN_GAP = int(round(3 * U))		# Unity: BTN_SIZE*0.5+3 -> dikey istif araligi
COIN_DIST = int(round(22 * U))		# oge kenari + para yaricapi + 22
## KULLANICI (2026-09-28): panele "Buton Ekle" / "Buton Sil" (ekrana ekstra hizli slot) -> 4 dugme, panel genisledi
PANEL_W = int(round(460 * U)); PANEL_H = int(round(60 * U))
PBTN_W = int(round(100 * U)); PBTN_H = int(round(40 * U))
PBTN_IMG_W = 268.0; PBTN_IMG_H = 108.0
MU = "mobile/ui/"

## KULLANICI (2026-09-26): "sag skill butonlari ve saldiri butonunu ayardan duzgunce yerlestirdim, bunu DEFAULT yap;
## isteyen sonradan degistirir". Kullanicinin telefonundaki kayit (2712x1220, en/boy 2.223): mobile_hud_layout.cfg
## arc0..5 + pick, mobile_layout.json att. Sag kenara baglidir: yatayda sag kenardan uzaklik EKRAN YUKSEKLIGI
## biriminde saklanir (baska en/boy oranli cihazda da kenara ayni uzaklikta), dikey oran aynen.
DEFAULT_ASPECT = 2712.0 / 1220.0
DEFAULTS = {
	# key: (cx, cy, s) - referans cihazdaki ekran oranlari
	## KULLANICI (2026-09-27): yeni varsayilan (gonderdigi ekran goruntusunden olculdu): beceriler saldiri topunun
	## sol-ustunden sol-altina uzanan yayda (2 en sagda ustte, 3 en altta), top buyudu (1.24 -> 1.49; top/beceri capi
	## orani 3.08), At ve Z yayin SOLUNDA alt alta. Top merkezi eskisiyle ayni.
	"arc0": (0.8984, 0.5920, 1.000),
	"arc1": (0.9506, 0.5797, 1.000),
	"arc2": (0.8037, 0.9059, 1.000),
	"arc3": (0.8532, 0.6265, 1.000),
	"arc4": (0.8202, 0.7037, 1.000),
	"arc5": (0.8084, 0.7995, 1.000),
	"pick": (0.7541, 0.8740, 1.080),
	"att": (0.90466, 0.78085, 1.490),		# native saldiri topu
	# KULLANICI (2026-09-26): tarih satiri kalkti -> Emoji / Oto Av / At "biraz asagi ve hafif saga"
	# (eski: y 0.3305, x 0.8469 / 0.8960 / 0.9452)
	# + "biraz daha saga yaklassin" (2. tur, +0.010)
	"emoji": (0.8649, 0.3655, 1.000),
	"autohunt": (0.9140, 0.3655, 1.000),
	"horse": (0.7541, 0.7713, 1.000),		# KULLANICI (2026-09-27): Z'nin ustunde (eski: 0.9632, 0.3655 ust sira)
}

def _Default(key):
	"""(cx, cy, s) bu ekran icin; tanimsizsa None."""
	v = DEFAULTS.get(key)
	if not v:
		return None
	A = _ScreenW() / max(1.0, _ScreenH())
	cx = 1.0 - (1.0 - v[0]) * DEFAULT_ASPECT / A
	return (cx, v[1], v[2])

def _ApplyTouchDefault():
	d = _Default("att")
	if not d:
		return
	try:
		app.SetTouchElementPos("att", d[0], d[1])
		app.SetTouchElementScale("att", d[2])
	except:
		pass

_elements = {}		# key -> dict
_order = []
_editor = None
_extraHandlers = [None, None]	# (ekle(), sil(key|None)) - uitaskbar.TaskBar kurar (ekstra hizli slot dugmeleri)


def SetExtraHandlers(add, remove):
	_extraHandlers[0] = add
	_extraHandlers[1] = remove


def Unregister(key):
	## ekstra dugme silinince duzenden cikar (kayitli konum bir sonraki Kaydet'te dosyadan duser)
	if key in _elements:
		del _elements[key]
	if key in _order:
		_order.remove(key)
_loaded = None		# dosyadan okunan {key: {cx,cy,s}}
_dimHost = None		# karartmanin ev sahibi: TaskBar koku (UI_BOTTOM). GAME katmani cizimi
			# telefonda gorunmedi (oyun karesine gidiyor) -> karartma HUD kokunun cocugu, duzenlenebilir
			# ogeler (yay, At, Yerden Al) SetParent hilesiyle karartmanin USTUNE tasinir; MobileHud koku
			# zaten sonra cizilir (ust sira dugmeleri).

def SetDimHost(wnd):
	global _dimHost
	_dimHost = wnd

def _ScreenW():
	return float(wndMgr.GetScreenWidth())

def _ScreenH():
	return float(wndMgr.GetScreenHeight())

def _Center(wnd):
	(x, y) = wnd.GetGlobalPosition()
	return (x + wnd.GetWidth() / 2.0, y + wnd.GetHeight() / 2.0)

def _Norm(dx, dy):
	l = math.sqrt(dx * dx + dy * dy)
	if l < 0.001:
		return (0.0, 1.0)
	return (dx / l, dy / l)

## kind: "button" (ui.Button; base = SetButtonScale temel olcegi), "slot" (ring ui.Button + slot ui.SlotWindow),
##       "touch" (native dokunmatik oge; wnd=None, key native anahtari: "att"),
##       "image" (ui.ExpandedImageBox; base = SetScale temel olcegi - KULLANICI 2026-09-16: Emoji dugmesi).
## follow: ogeden sonra cagrilir follow(wnd) - ogeye bagli gorunmez dokunma alanini tasir/boyutlar.
## label: ogenin altindaki yazi (ui.TextLine, yatay ortali) - ogeyle birlikte tasinir.
## dir: +/- madeni paralarin ogeden uzaklasacagi yon (ekran: y asagi) - komsu ogelerle cakismasin.
def Register(key, wnd, label = None, kind = "button", base = 1.0, ring = None, dir = (0.0, 1.0), follow = None):
	if key in _elements:
		e = _elements[key]
		e["wnd"] = wnd; e["label"] = label; e["ring"] = ring; e["dir"] = _Norm(dir[0], dir[1]); e["follow"] = follow
		return
	if kind == "touch":
		e = {"key": key, "wnd": None, "label": None, "kind": kind, "base": 1.0, "ring": None, "dir": _Norm(dir[0], dir[1]),
			 "dcx": 0.0, "dcy": 0.0, "cx": 0.0, "cy": 0.0, "s": 1.0, "phase": 0.0, "sizeH": 0.0}
		_SyncTouch(e)
	else:
		(cx, cy) = _Center(ring or wnd)
		e = {"key": key, "wnd": wnd, "label": label, "kind": kind, "base": base, "ring": ring, "dir": _Norm(dir[0], dir[1]),
			 "dcx": cx / _ScreenW(), "dcy": cy / _ScreenH(), "cx": cx / _ScreenW(), "cy": cy / _ScreenH(), "s": 1.0, "phase": 0.0,
			 "follow": follow}
		if kind == "image":
			# native CExpandedImageBox::SetScale pencere boyunu GUNCEL boyla carpar (birikir) -> once doku boyuna don
			e["tex"] = (int(round(wnd.GetWidth() / base)), int(round(wnd.GetHeight() / base)))
	d = _Default(key)
	if d:
		e["dcx"] = d[0]; e["dcy"] = d[1]; e["ds"] = d[2]
	_elements[key] = e
	_order.append(key)

def _SyncTouch(e):
	"""Native ogenin guncel merkez/olcegini okur (ekran orani)."""
	try:
		v = app.GetTouchElement(e["key"])
		if v:
			e["cx"] = float(v[0]); e["cy"] = float(v[1]); e["sizeH"] = float(v[2])
			e["s"] = float(app.GetTouchElementScale(e["key"]))
			return True
	except:
		pass
	return False

## Ogenin ekrandaki merkez ve (kare) boyutu - mantiksal px.
def _Geometry(e):
	W = _ScreenW(); H = _ScreenH()
	if e["kind"] == "touch":
		_SyncTouch(e)
		return (e["cx"] * W, e["cy"] * H, e.get("sizeH", 0.0) * H)
	main = (e["kind"] == "slot" and (e["ring"] or e["wnd"])) or e["wnd"]
	(x, y) = main.GetGlobalPosition()
	return (x + main.GetWidth() / 2.0, y + main.GetHeight() / 2.0, max(main.GetWidth(), main.GetHeight()))

def _IsVisible(e):
	if e["kind"] == "touch":
		return _SyncTouch(e) and e.get("sizeH", 0.0) > 0.0
	main = (e["kind"] == "slot" and (e["ring"] or e["wnd"])) or e["wnd"]
	try:
		return main.IsShow()
	except:
		return True

def _ApplyElement(e):
	W = _ScreenW(); H = _ScreenH()
	s = e["s"]
	try:
		if e["kind"] == "touch":
			app.SetTouchElementPos(e["key"], e["cx"], e["cy"])
			app.SetTouchElementScale(e["key"], s)
			_SyncTouch(e)
			return
		if e["kind"] == "slot":
			ring = e["ring"]; slot = e["wnd"]
			if hasattr(wndMgr, "SetButtonScale") and ring:
				wndMgr.SetButtonScale(ring.hWnd, e["base"] * s, e["base"] * s)
			if hasattr(wndMgr, "SetSlotScale"):
				wndMgr.SetSlotScale(slot.hWnd, s)
			cx = e["cx"] * W; cy = e["cy"] * H
			if ring:
				ring.SetPosition(int(cx - ring.GetWidth() / 2), int(cy - ring.GetHeight() / 2))
			slot.SetPosition(int(cx - slot.GetWidth() / 2), int(cy - slot.GetHeight() / 2))
			main = ring or slot
		else:
			wnd = e["wnd"]
			if e["kind"] == "image":
				wnd.SetSize(e["tex"][0], e["tex"][1])
				wnd.SetScale(e["base"] * s, e["base"] * s)
			elif hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(wnd.hWnd, e["base"] * s, e["base"] * s)
			cx = e["cx"] * W; cy = e["cy"] * H
			wnd.SetPosition(int(cx - wnd.GetWidth() / 2), int(cy - wnd.GetHeight() / 2))
			main = wnd
		if e["label"]:
			e["label"].SetPosition(int(cx) - 2, int(cy + main.GetHeight() / 2 + 1))
		if e.get("follow"):
			e["follow"](main)
	except:
		import traceback
		dbg.TraceError("MOBIL duzen uygula (%s): %s" % (e["key"], traceback.format_exc()))

def _Load():
	global _loaded
	if _loaded is not None:
		return _loaded
	_loaded = {}
	# Cihazdaki Python kutuphanesinde json paketi eksik (json.scanner yok) -> satir bicimi:
	#   <anahtar> <cx> <cy> <s>
	ver = 0
	try:
		f = open(LAYOUT_FILE, "r")
		for line in f.readlines():
			t = line.split()
			if len(t) == 2 and t[0] == "v":
				ver = int(t[1])
			elif len(t) == 4:
				_loaded[t[0]] = {"cx": float(t[1]), "cy": float(t[2]), "s": float(t[3])}
		f.close()
	except:
		_loaded = {}
	if ver in (2, 3, 4):
		for k in LAYOUT_V2_DROP:
			if k in _loaded:
				del _loaded[k]
		ver = LAYOUT_VERSION
	if ver != LAYOUT_VERSION:
		# eski (ya da surumsuz) kayit: varsayilan duzen degisti -> kullanma, sil
		_loaded = {}
		try:
			import os
			os.remove(LAYOUT_FILE)
		except:
			pass
	return _loaded

## Kayitli duzeni kayitli ogelere uygular (HUD yuklenince cagrilir; birden fazla cagri zararsiz).
def ApplySaved():
	d = _Load()
	for key in _order:
		e = _elements[key]
		if e["kind"] == "touch":
			# native kendi dosyasini (mobile_layout.json) okur; oyuncu hic duzen kaydetmediyse varsayilan
			if not d:
				_ApplyTouchDefault()
				_SyncTouch(e)
			continue
		v = d.get(key)
		if v:
			try:
				e["cx"] = float(v.get("cx", e["dcx"])); e["cy"] = float(v.get("cy", e["dcy"])); e["s"] = float(v.get("s", 1.0))
			except:
				pass
		elif "ds" in e:
			e["cx"] = e["dcx"]; e["cy"] = e["dcy"]; e["s"] = e["ds"]
		_ApplyElement(e)

def Save():
	global _loaded
	d = {}
	for key in _order:
		e = _elements[key]
		if e["kind"] == "touch":
			continue
		d[key] = {"cx": round(e["cx"], 4), "cy": round(e["cy"], 4), "s": round(e["s"], 3)}
	try:
		f = open(LAYOUT_FILE, "w")
		f.write("v %d\n" % LAYOUT_VERSION)
		for key in _order:
			if key in d:
				f.write("%s %.4f %.4f %.3f\n" % (key, d[key]["cx"], d[key]["cy"], d[key]["s"]))
		f.close()
		_loaded = d
	except:
		import traceback
		dbg.TraceError("MOBIL duzen kaydet: " + traceback.format_exc())

def ResetAll():
	global _loaded
	try:
		app.ResetTouchLayout()
	except:
		pass
	_ApplyTouchDefault()
	for key in _order:
		e = _elements[key]
		if e["kind"] == "touch":
			_SyncTouch(e)
			continue
		e["cx"] = e["dcx"]; e["cy"] = e["dcy"]; e["s"] = e.get("ds", 1.0)
		_ApplyElement(e)
	try:
		import os
		os.remove(LAYOUT_FILE)
	except:
		pass
	_loaded = {}

def IsEditing():
	return _editor is not None and _editor.editing

def Open():
	global _editor
	if _editor is None:
		_editor = LayoutEditor()
	_editor.Open()

## ---------------------------------------------------------------------------
class DragProxy(ui.Window):
	"""Ogenin ustunde duran GORUNMEZ tasima kutusu (Unity: elemanin kendisi suruklenir)."""
	def __init__(self, editor, e):
		ui.Window.__init__(self, "TOP_MOST")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)
		self.editor = editor
		self.e = e
		self.AddFlag("movable")
		self.AddFlag("float")
		self.AddFlag("drag_any")
		self.SetWindowName("MobileLayoutProxy_" + e["key"])
		self.Fit()

	def __del__(self):
		ui.Window.__del__(self)

	def Fit(self):
		(cx, cy, size) = _Geometry(self.e)
		w = int(size)
		self.SetSize(w, w)
		self.SetPosition(int(cx - w / 2), int(cy - w / 2))

	def OnMouseLeftButtonDown(self):
		self.editor.Select(self)
		return True

	def OnMoveWindow(self, x, y):
		e = self.e
		e["cx"] = (x + self.GetWidth() / 2.0) / _ScreenW()
		e["cy"] = (y + self.GetHeight() / 2.0) / _ScreenH()
		e["phase"] = 0.0
		_ApplyElement(e)
		if e["kind"] == "touch":
			# native kirpmis olabilir -> kutu ogeyi izlesin
			self.Fit()
		self.editor.OnProxyMoved(self)


class LayoutEditor(ui.Window):
	def __init__(self):
		ui.Window.__init__(self, "TOP_MOST")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("MobileLayoutEditor")
		self.SetSize(1, 1)
		self.proxies = []
		self.glows = {}
		self.selected = None
		self.editing = False
		self.lastTime = 0
		self.__BuildDim()
		self.__BuildPanel()
		self.__BuildCoins()

	def __del__(self):
		ui.Window.__del__(self)

	## ---- Unity EditDim: tam ekran siyah %55, ogelerin ARKASINDA (GAME katmani: UI'nin altinda,
	##      dunyanin ustunde; dunyaya dokunmayi yutar - Unity raycastTarget=true)
	def __BuildDim(self):
		W = int(_ScreenW()); H = int(_ScreenH())
		if _dimHost:
			# HUD kokunun cocugu (kok not_pick ama cocuk dokunmayi yutar -> dunyaya dokunma yok, Unity gibi)
			dim = ui.Bar()
			dim.SetParent(_dimHost)
		else:
			dim = ui.Bar("GAME")
			if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(dim.hWnd, 1.0)
		dim.SetWindowName("MobileLayoutDim")
		dim.SetSize(W, H)
		dim.SetPosition(0, 0)
		dim.SetColor(0x8C000000)
		dim.Hide()
		self.dim = dim
		self.dimReordered = False

	def __RaiseAboveDim(self):
		## TaskBar kokundeki duzenlenebilir ogeleri (halka, slot, At, Yerden Al + etiketler) karartmadan
		## SONRA cizilsin diye cocuk listesinin sonuna tasi (ayni ebeveyne SetParent siralamayi
		## degistirmez -> once editor kokune, sonra geri).
		if self.dimReordered or not _dimHost:
			return
		self.dimReordered = True
		for key in _order:
			e = _elements[key]
			# yalniz TaskBar kokundeki ogeler (yay slotlari, At, Yerden Al); ust sira MobileHud kokunde
			if not (key.startswith("arc") or key in ("horse", "pick")):
				continue
			for w in (e.get("ring"), e.get("wnd"), e.get("label")):
				if not w:
					continue
				try:
					(x, y) = w.GetLocalPosition()
					w.SetParent(self)
					w.SetParent(_dimHost)
					w.SetPosition(x, y)
				except:
					pass

	def __MakeGlow(self):
		g = ui.ExpandedImageBox()
		g.SetParent(self.dim)
		g.AddFlag("not_pick")
		g.LoadImage(MU + "edit_glow.tga")
		g.Show()
		return g

	def __PlaceGlow(self, e):
		g = self.glows.get(e["key"])
		if not g:
			return
		(cx, cy, size) = _Geometry(e)
		d = size * 1.35
		sc = d / 192.0
		g.SetScale(sc, sc)
		g.SetPosition(int(cx - d / 2), int(cy - d / 2))

	## ---- Unity ButonDuzenlePanel: ust orta 240x60, [Duzenle/Kaydet] (-60) ve [Sifirla] (+60), 100x40
	def __MakePanelButton(self, parent, text, x, y, event):
		b = ui.Button()
		b.SetParent(parent)
		b.SetUpVisual(MU + "edit_btn_up.tga")
		b.SetOverVisual(MU + "edit_btn_up.tga")
		b.SetDownVisual(MU + "edit_btn_down.tga")
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, PBTN_W / PBTN_IMG_W, PBTN_H / PBTN_IMG_H)
		b.SetPosition(x, y)
		b.SetText(text)
		if b.ButtonText:
			b.ButtonText.SetFontName("Tahoma:20")
			b.ButtonText.SetFontColor(1.0, 0.92, 0.7)
			b.ButtonText.SetPosition(b.GetWidth() / 2, b.GetHeight() / 2)
		b.SetEvent(event)
		b.Show()
		return b

	def __BuildPanel(self):
		W = int(_ScreenW())
		panel = ui.Window("TOP_MOST")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(panel.hWnd, 1.0)
		panel.AddFlag("float")
		panel.SetWindowName("MobileLayoutPanel")
		panel.SetSize(PANEL_W, PANEL_H)
		panel.SetPosition((W - PANEL_W) / 2, 100)	# KULLANICI 2026-09-15: ust sira dugmelerinin ALTINDA
		cx = PANEL_W / 2; cy = int(round(30 * U))
		off = int(round(55 * U)); off2 = int(round(165 * U))
		self.btnEdit = self.__MakePanelButton(panel, "D\xfczenle", cx - off2 - PBTN_W / 2, cy - PBTN_H / 2, ui.__mem_func__(self.ToggleEdit))
		self.btnReset = self.__MakePanelButton(panel, "S\xfdf\xfdrla", cx - off - PBTN_W / 2, cy - PBTN_H / 2, ui.__mem_func__(self.Reset))
		self.btnAdd = self.__MakePanelButton(panel, "Buton Ekle", cx + off - PBTN_W / 2, cy - PBTN_H / 2, ui.__mem_func__(self.AddExtra))
		self.btnDel = self.__MakePanelButton(panel, "Buton Sil", cx + off2 - PBTN_W / 2, cy - PBTN_H / 2, ui.__mem_func__(self.RemoveExtra))
		panel.Hide()
		self.panel = panel

	## ---- Unity MakeCoinButton: 46 birim, dikey istif (+ ustte, - altta), ogeyle OLCEKLENMEZ
	def __BuildCoins(self):
		self.btnPlus = self.__MakeCoin("plus", ui.__mem_func__(self.Bigger))
		self.btnMinus = self.__MakeCoin("minus", ui.__mem_func__(self.Smaller))

	def __MakeCoin(self, name, event):
		root = ui.Window("TOP_MOST")
		if hasattr(wndMgr, "SetUIScale"): wndMgr.SetUIScale(root.hWnd, 1.0)
		root.AddFlag("float")
		root.SetWindowName("MobileLayoutCoin_" + name)
		root.SetSize(COIN, COIN)
		b = ui.Button()
		b.SetParent(root)
		b.SetUpVisual(MU + "edit_coin_%s_up.tga" % name)
		b.SetOverVisual(MU + "edit_coin_%s_up.tga" % name)
		b.SetDownVisual(MU + "edit_coin_%s_down.tga" % name)
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(b.hWnd, COIN / COIN_IMG, COIN / COIN_IMG)
		b.SetPosition(0, 0)
		b.SetEvent(event)
		b.Show()
		root.button = b
		root.Hide()
		return root

	## ---- akis (Unity ButonlariOzellestir / EditModeBtn) ----
	def Open(self):
		# panel acilirken duzenleme KAPALI baslar, etiket "Duzenle"
		self.StopEdit()
		self.panel.Show()
		self.panel.SetTop()
		self.Show()

	def ToggleEdit(self):
		if not self.editing:
			self.StartEdit()
		else:
			# KAYDET: duzenlemeyi bitir + paneli kapat
			Save()
			self.StopEdit()
			self.panel.Hide()
			self.Hide()

	def StartEdit(self):
		self.editing = True
		self.btnEdit.SetText("Kaydet")
		try:
			app.SetTouchEditMode(1)
		except:
			pass
		self.dim.Show()
		self.__RaiseAboveDim()
		for key in _order:
			e = _elements[key]
			if not _IsVisible(e):
				continue
			e["phase"] = 0.0
			self.glows[key] = self.__MakeGlow()
			self.__PlaceGlow(e)
			p = DragProxy(self, e)
			p.Show()
			p.SetTop()
			self.proxies.append(p)
		self.panel.SetTop()
		self.lastTime = app.GetGlobalTime()

	def StopEdit(self):
		self.editing = False
		self.btnEdit.SetText("D\xfczenle")
		for p in self.proxies:
			p.Hide()
		self.proxies = []
		for g in self.glows.values():
			g.Hide()
		self.glows = {}
		self.selected = None
		self.btnPlus.Hide()
		self.btnMinus.Hide()
		self.dim.Hide()
		try:
			app.SetTouchEditMode(0)	# native duzeni (saldiri topu) dosyaya yazar
		except:
			pass

	def Close(self):
		self.StopEdit()
		self.panel.Hide()
		self.Hide()

	def AddExtra(self):
		## KULLANICI (2026-09-28): ekrana ekstra hizli slot (beceri/esya/duygu suruklenir). Yeni dugme duzenlemede
		## SECILI gelir, hemen tasinir; duzenleme kapaliysa acilir.
		add = _extraHandlers[0]
		if not add:
			return
		key = add()
		if key:
			self.__Rebuild(key)

	def RemoveExtra(self):
		## secili oge ekstra dugmeyse onu, degilse SON ekleneni siler
		rem = _extraHandlers[1]
		if not rem:
			return
		key = None
		if self.selected and self.selected.e["key"].startswith("ex"):
			key = self.selected.e["key"]
		if rem(key):
			self.__Rebuild(None)

	def __Rebuild(self, selectKey):
		## konumlar _elements'te kalir (kaydetmeden) - vekil/parilti listesi yeni oge kumesiyle yeniden kurulur
		self.StopEdit()
		self.StartEdit()
		if selectKey:
			for p in self.proxies:
				if p.e["key"] == selectKey:
					self.Select(p)
					break

	def Reset(self):
		ResetAll()
		for p in self.proxies:
			p.Fit()
		for key in self.glows:
			self.__PlaceGlow(_elements[key])
		self.__PlaceCoins()

	def Select(self, proxy):
		self.selected = proxy
		proxy.e["phase"] = 0.0
		proxy.SetTop()
		self.__PlaceCoins()

	def OnProxyMoved(self, proxy):
		self.__PlaceGlow(proxy.e)
		if proxy == self.selected:
			self.__PlaceCoins()

	def __PlaceCoins(self):
		p = self.selected
		if not p or not self.editing:
			self.btnPlus.Hide(); self.btnMinus.Hide()
			return
		e = p.e
		(cx, cy, size) = _Geometry(e)
		W = int(_ScreenW()); H = int(_ScreenH())
		dist = size / 2.0 + COIN / 2.0 + COIN_DIST
		(dx, dy) = e["dir"]
		mx = cx + dx * dist; my = cy + dy * dist
		gap = COIN / 2.0 + COIN_GAP
		# ekran icinde tut
		mx = max(COIN / 2.0, min(W - COIN / 2.0, mx))
		my = max(gap + COIN / 2.0, min(H - gap - COIN / 2.0, my))
		self.btnPlus.SetPosition(int(mx - COIN / 2), int(my - gap - COIN / 2))
		self.btnMinus.SetPosition(int(mx - COIN / 2), int(my + gap - COIN / 2))
		self.btnPlus.Show(); self.btnPlus.SetTop()
		self.btnMinus.Show(); self.btnMinus.SetTop()

	def __Rescale(self, delta):
		p = self.selected
		if not p:
			return
		e = p.e
		e["s"] = max(SMIN, min(SMAX, e["s"] + delta))
		e["phase"] = 0.0
		_ApplyElement(e)
		p.Fit()
		self.__PlaceGlow(e)
		self.__PlaceCoins()

	def Bigger(self):
		self.__Rescale(STEP)

	def Smaller(self):
		self.__Rescale(-STEP)

	def OnUpdate(self):
		if not self.editing:
			return
		now = app.GetGlobalTime()
		dt = (now - self.lastTime) / 1000.0
		self.lastTime = now
		if dt < 0 or dt > 0.5:
			dt = 0.0
		sel = self.selected and self.selected.e or None
		for key, g in self.glows.items():
			e = _elements[key]
			e["phase"] += dt
			if e is sel:
				wave = 0.35
			else:
				wave = (math.sin(e["phase"] * (2.0 * math.pi / GLOW_PERIOD)) + 1.0) * 0.5
			try:
				wndMgr.SetDiffuseColor(g.hWnd, 1.0, 0.85, 0.35, wave * 0.5)
			except:
				pass
			if e["kind"] == "touch" and e is not sel:
				# native surukleme (parmak dogrudan topa) -> hale/kutu izlesin
				self.__PlaceGlow(e)

	def OnPressEscapeKey(self):
		self.Close()
		return True
