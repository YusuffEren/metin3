# MOBIL - mobile_root/uioyuncupaneli.py: OYUNCU KARTI v5 (klasik, kompakt).
# URETILIR: tools/oyuncukart/uioyuncupaneli_kaynak.py (UTF-8) -> tools/oyuncukart/gen_uioyuncupaneli.py -> bu dosya.
#
# KULLANICI (2026-10-01): "birinin ustune tiklayinca da eski tip tasarim" -> prototip
#   Desktop/Averos2-Oyuncu-Prototip/oyuncu_klasik.html: "mukemmel, bunu yap ama yazilar net olsun, okunakli olsun,
#   cozunurluk dusuk olmasin"; "lonca nickle ayni hizada solda; pencere uzunlamasina daralsin"; "cok buyuk" -> kompakt.
# Tasarim: metin/canavar karti (uihedefkarti) ile AYNI yuva (Gizle <-> ust menu arasi, ekranin en ustu; uihedefkarti.
#   HudGapOrFrac - HUD dugmelerinin GERCEK konumu), ayni klasik dil: ThinBoard cerceve (oyunun kendi dokulari, ui.ThinBoard
#   gibi DOSENIR - her genislikte dikissiz), tek satir baslik (bayrak \xb7 lonca hapi \xb7 ad \xb7 X), altta eylem dugmeleri
#   (klasik middle_button) YAZISI KADAR genis -> kart icerige gore (~500 px). Sigmazsa orantili kuculur, yeri DEGISMEZ.
# NETLIK: eylem yazilari, "yakin degil", simgeler, bayrak, X fiziksel pikselde pisirildi (tools/oyuncukart/
#   bake_oyuncukart.py -> mobile/ui/oyk/, olculer uioyuncukartveri.py); ad + lonca TextLine <= 18 pt (motor 32 px tavani).
# Mantik v4'ten BIREBIR: hangi dugme = uitarget.TargetBoard.RefreshButton (buttonDict); Ticaret/Zar menzil disinda
#   soluk "yakin degil"; duello/gozlemcide acilmaz (Blocked); kapatma mandali (closedVid, UserClose, ReopenByTap);
#   her eylemden sonra kapanir; 40 m'den uzaklasinca hedef birakilir. Dis arayuz (uitarget/game.py) degismedi.

import ui
import wndMgr
import app
import dbg
import player
import chr
import localeInfo

try:
	import uioyuncukartveri as V
except:
	V = None
try:
	import uihedefkarti as HK
except:
	HK = None

DIR = "mobile/ui/oyk/"
TB = "d:/ymir work/ui/pattern/ThinBoard_"
REF_H = 705.0
IMG_S = 705.0 / 1220.0
OPEN_SEC = 0.16
CLOSE_RANGE = 4000		# uitarget.MOBILE_CLOSE_RANGE ile ayni (40 m)
MAX_TILES = 10
CARD_TOP = 4			# metin karti ile ayni
TOP_FRAC = 0.135		# yalniz 4:3 tablette (arada yer yok) yedek
FIT_MIN = 0.5
# KULLANICI (2026-10-01): "konum ayni kalsin, hafif biraz buyusun" -> x1.1 (dokular bu olcekte pisirildi: bake_oyuncukart.py)
try:
	ZOOM = V.ZOOM
except:
	ZOOM = 1.0
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")

# ---- olculer (mantiksal px; prototip + bake_oyuncukart.py ile AYNI) ----
PAD_X, PAD_T, PAD_B = 12, 12, 10
HEAD_H = 28
FLAG_W, FLAG_H = 42, 28
PILL_H = 22
CLOSE = 24
SEP_T, SEP_B = 8, 6
BTN_H = 48
BTN_GAP = 5
ICON = 22
NAME_MAX = 300
TB_TEX = 16			# ThinBoard parca boyu (texel)
TB_SCALE = 1.15			# texel -> mantiksal px (metin karti kosesiyle ayni boy)
CARD_H = PAD_T + HEAD_H + SEP_T + 1 + SEP_B + BTN_H + PAD_B

C_NAME = 0xffffffff
C_SUB = 0xffc9b88f
C_PILL_BG = 0x8c000000
C_PILL_BORDER = 0xff6b5a3e
C_FILL = 0x82000000		# ui.ThinBoard BOARD_COLOR (0.51)

RED_KEYS = ("fight", "accept", "avenge")
# KULLANICI (2026-10-01): "uzaktayken ticarete tiklayinca bildirim dussun: uzaktayken ticaret yapamazsin, yaklas"
FAR_MSG = {
	"exchange": "Uzaktayken ticaret yapamazs\xfdn, oyuncuya yakla\xfe.",
	"dice": "Uzaktayken zar atamazs\xfdn, oyuncuya yakla\xfe.",
}
RANGE_TICK = 0.25		# kart acikken ticaret/zar menzili bu siklikla yeniden olculur
TOAST_SEC = 2.5			# gorunur kalma
TOAST_FADE = 0.35		# sonen kisim
TOAST_H = 30
TOAST_GAP = 6
C_TOAST_BG = 0xdc140f0a
C_TOAST_TXT = 0xffffd9b8


def _Actions():
	L = localeInfo
	return {
		L.TARGET_BUTTON_WHISPER: "whisper",
		L.TARGET_BUTTON_EXCHANGE: "exchange",
		L.TARGET_BUTTON_DICE: "dice",
		L.TARGET_BUTTON_FIGHT: "fight",
		L.TARGET_BUTTON_ACCEPT_FIGHT: "accept",
		L.TARGET_BUTTON_AVENGE: "avenge",
		L.TARGET_BUTTON_EMOTION_ALLOW: "emotion",
		L.TARGET_BUTTON_FRIEND: "friend",
		L.TARGET_BUTTON_INVITE_PARTY: "party",
		L.TARGET_BUTTON_LEAVE_PARTY: "party_leave",
		L.TARGET_BUTTON_EXCLUDE: "party_kick",
		L.TARGET_BUTTON_INVITE_GUILD: "guild",
		L.TARGET_BUTTON_VIEW_EQUIPMENT: "equip",
		L.TARGET_BUTTON_REQUEST_ENTER_PARTY: "party_join",
	}


def _Order():
	## sabit sira (v4 / prototip): her grup en fazla bir dugme; ailenin gorunen ilk uyesi cizilir
	L = localeInfo
	return (
		(L.TARGET_BUTTON_WHISPER,),
		(L.TARGET_BUTTON_EXCHANGE,),
		(L.TARGET_BUTTON_FIGHT, L.TARGET_BUTTON_ACCEPT_FIGHT, L.TARGET_BUTTON_AVENGE),
		(L.TARGET_BUTTON_FRIEND,),
		(L.TARGET_BUTTON_INVITE_PARTY, L.TARGET_BUTTON_LEAVE_PARTY, L.TARGET_BUTTON_EXCLUDE, L.TARGET_BUTTON_REQUEST_ENTER_PARTY),
		(L.TARGET_BUTTON_INVITE_GUILD,),
		(L.TARGET_BUTTON_EMOTION_ALLOW,),
		(L.TARGET_BUTTON_VIEW_EQUIPMENT,),
		(L.TARGET_BUTTON_DICE,),
	)


def _EaseOut(t):
	t = 1.0 - t
	return 1.0 - t * t * t


class _Root(ui.Window):
	"""kart koku: kendi boyutunda, icindeki dokunusu yutar (bos alana dokunmak dunyaya gecmez). Dunyaya dokunus ->
	OnOutsideTap (v4 ile ayni: TargetBoard.OnOutsideTap), baska arayuze dokunus -> OnOutsideTapUI (acik kalir)."""

	def __init__(self, owner):
		ui.Window.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.AddFlag("hide_on_outside")
		self.owner = owner

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonDown(self):
		return True

	def OnMouseLeftButtonUp(self):
		return True

	def OnOutsideTap(self):
		o = self.owner
		if o:
			o.OnOutsideTap()

	def OnOutsideTapUI(self):
		pass


class PlayerPanel(ui.Window):

	def __init__(self, board):
		ui.Window.__init__(self, "UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("MobilePlayerPanel")
		self.SetSize(1, 1)
		self.SetPosition(0, 0)
		self.board = board
		self.keep = []
		self.tiles = []
		self.entries = []		# [(name, enabled)]
		self.entrySig = None
		self.layoutSig = None
		self.state = "kapali"
		self.animT0 = 0.0
		self.suppressUntil = 0.0
		self.suppressVid = 0
		self.closedVid = 0		# kullanici zemine/x'e dokunup kapatti: ayni hedef icin sunucu paketleri paneli acamaz
		self.openVid = 0
		self.actions = _Actions()
		self.order = _Order()
		try:
			L = localeInfo
			self.always = (L.TARGET_BUTTON_EXCHANGE, L.TARGET_BUTTON_DICE)
		except:
			self.always = ()
		self.scrW = wndMgr.GetScreenWidth()
		self.scrH = wndMgr.GetScreenHeight()
		self.k = self.scrH / REF_H
		self.fit = 1.0
		self.cardW = 300
		self.cardX = 0
		self.cardY = int(round(CARD_TOP * self.k))
		self.nameStr = ""
		self.guildStr = ""
		box = _Root(self)
		box.Hide()
		self.keep.append(box)
		self.box = box
		self.toastT0 = -100.0
		self.nextRange = 0.0
		self.lastNear = None
		self.__Build()
		self.__BuildToast()
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.Hide()
		try:
			self.box.Hide()
			self.box.owner = None
			self.toastWnd.Hide()
		except:
			pass
		self.tiles = []
		self.keep = []
		self.board = None

	# ------------------------------------------------------------------ yardimci
	def S(self, v):
		return int(round(v * self.k * ZOOM * self.fit))

	def _ImgScale(self):
		return self.k * IMG_S * self.fit

	def _Img(self, path, parent=None):
		w = ui.ExpandedImageBox()
		w.SetParent(parent or self.box)
		w.AddFlag("not_pick")
		w.LoadImage(path)
		f = self._ImgScale()
		w.SetScale(f, f)
		w.Show()
		self.keep.append(w)
		return w

	def _Txt(self, color, outline=True, vcenter=True):
		t = ui.TextLine()
		t.SetParent(self.box)
		t.AddFlag("not_pick")
		if outline:
			t.SetOutline()
		if vcenter:
			t.SetVerticalAlignCenter()
		t.SetPackedFontColor(color)
		t.Show()
		self.keep.append(t)
		return t

	def _Font(self, pt):
		return "Tahoma:%d" % max(8, min(18, int(round(pt * self.k * ZOOM * self.fit))))

	def _TextW(self, t):
		try:
			(w, h) = t.GetTextSize()
			return w
		except:
			return 0

	def _Fit(self, t, text, maxw):
		t.SetText(text)
		if self._TextW(t) <= maxw:
			return
		s = text
		while len(s) > 1 and self._TextW(t) > maxw:
			s = s[:-1]
			t.SetText(s.rstrip() + "..")

	def _Lbl(self, name):
		"""pisirilmis yazi gorselinin MANTIKSAL boyu (olcu tablosu; GetWidth'e guvenilmez)"""
		try:
			(w, h) = V.LBL[name]
			return (w / V.B, h / V.B)
		except:
			return (0.0, 0.0)

	# ------------------------------------------------------------------ yapi
	def __Build(self):
		## cizim sirasi = yaratma sirasi: cerceve -> dugmeler -> baslik
		self.fill = ui.Bar()
		self.fill.SetParent(self.box)
		self.fill.AddFlag("not_pick")
		self.fill.SetColor(C_FILL)
		self.fill.Show()
		self.keep.append(self.fill)
		self.corners = {}
		for n in ("LeftTop", "RightTop", "LeftBottom", "RightBottom"):
			self.corners[n] = self._Img(TB + "Corner_" + n + ".tga")
		self.lines = {}
		for n in ("Left", "Right", "Top", "Bottom"):
			w = self._Img(TB + "Line_" + n + ".tga")
			if HAS_RRS:
				try:
					wndMgr.SetRenderingRectScaled(w.hWnd, 1)
				except:
					pass
			self.lines[n] = w
		self.sep = self._Img(DIR + "ayrac.png")
		for i in xrange(MAX_TILES):
			b = ui.Button()
			b.SetParent(self.box)
			b.SetUpVisual(DIR + "btn_58_up.png")
			b.SetOverVisual(DIR + "btn_58_up.png")
			b.SetDownVisual(DIR + "btn_58_down.png")
			b.SetEvent(lambda i0=i: self.__OnTile(i0))
			b.Hide()
			self.keep.append(b)
			ic = self._Img(DIR + "ic_whisper_n.png")
			lbl = self._Img(DIR + "lbl_whisper_n.png")
			off = self._Img(DIR + "yakin_degil.png")
			for w in (ic, lbl, off):
				w.Hide()
			self.tiles.append({"btn": b, "ic": ic, "lbl": lbl, "off": off, "w": 0, "icF": "", "lblF": "", "skin": 0})
		self.flag = self._Img(DIR + "flag.png")
		self.pillBg = ui.Bar()
		self.pillBg.SetParent(self.box)
		self.pillBg.AddFlag("not_pick")
		self.pillBg.SetColor(C_PILL_BG)
		self.keep.append(self.pillBg)
		self.pillFr = ui.Box()
		self.pillFr.SetParent(self.box)
		self.pillFr.AddFlag("not_pick")
		self.pillFr.SetColor(C_PILL_BORDER)
		self.keep.append(self.pillFr)
		self.pillT = self._Txt(C_SUB)
		self.nameT = self._Txt(C_NAME)
		cb = ui.Button()
		cb.SetParent(self.box)
		cb.SetUpVisual(DIR + "close_up.png")
		cb.SetOverVisual(DIR + "close_up.png")
		cb.SetDownVisual(DIR + "close_down.png")
		cb.SetEvent(ui.__mem_func__(self.__OnClose))
		cb.Show()
		self.keep.append(cb)
		self.closeBtn = cb

	def __BuildToast(self):
		"""menzil disi uyarisi: kartin hemen altinda kisa klasik kutu (dokunus gecirir)"""
		tw = ui.Window("UI")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(tw.hWnd, 1.0)
		tw.AddFlag("not_pick")
		tw.Hide()
		self.keep.append(tw)
		self.toastWnd = tw
		bg = ui.Bar()
		bg.SetParent(tw)
		bg.AddFlag("not_pick")
		bg.SetColor(C_TOAST_BG)
		bg.Show()
		fr = ui.Box()
		fr.SetParent(tw)
		fr.AddFlag("not_pick")
		fr.SetColor(C_PILL_BORDER)
		fr.Show()
		t = ui.TextLine()
		t.SetParent(tw)
		t.AddFlag("not_pick")
		t.SetOutline()
		t.SetHorizontalAlignCenter()
		t.SetVerticalAlignCenter()
		t.SetPackedFontColor(C_TOAST_TXT)
		t.Show()
		for w in (bg, fr, t):
			self.keep.append(w)
		self.toastBg = bg
		self.toastFr = fr
		self.toastT = t

	def __Toast(self, msg):
		t = self.toastT
		t.SetFontName(self._Font(13))
		t.SetText(msg)
		w = int(self._TextW(t)) + self.S(28)
		h = self.S(TOAST_H)
		self.toastWnd.SetSize(w, h)
		cx = self.cardX + self.S(self.cardW) // 2
		self.toastWnd.SetPosition(cx - w // 2, self.cardY + self.S(CARD_H) + self.S(TOAST_GAP))
		for x in (self.toastBg, self.toastFr):
			x.SetPosition(0, 0)
			x.SetSize(w, h)
		t.SetPosition(w // 2, h // 2)
		self.toastT0 = app.GetTime()
		self.__ToastAlpha(1.0)
		self.toastWnd.Show()
		self.toastWnd.SetTop()

	def __ToastAlpha(self, a):
		a = max(0.0, min(1.0, a))
		def mul(c):
			return (int(((c >> 24) & 0xff) * a) << 24) | (c & 0xffffff)
		self.toastBg.SetColor(mul(C_TOAST_BG))
		self.toastFr.SetColor(mul(C_PILL_BORDER))
		self.toastT.SetPackedFontColor(mul(C_TOAST_TXT))

	def __UpdateToast(self):
		if not self.toastWnd.IsShow():
			return
		dt = app.GetTime() - self.toastT0
		if dt >= TOAST_SEC:
			self.toastWnd.Hide()
		elif dt > TOAST_SEC - TOAST_FADE:
			self.__ToastAlpha((TOAST_SEC - dt) / TOAST_FADE)

	# ------------------------------------------------------------------ yerlesim
	def __Measure(self):
		"""(kart genisligi, satir genisligi, hap genisligi, ad genisligi) TASARIM px (fit = 1)"""
		ws = []
		for (name, enabled) in self.entries:
			key = self.actions.get(name)
			ws.append(V.BTN_W.get(key, 58))
		rowW = sum(ws) + BTN_GAP * max(0, len(ws) - 1)
		saved = self.fit
		self.fit = 1.0
		self.pillT.SetFontName(self._Font(12.5))
		self.nameT.SetFontName(self._Font(18))
		pillW = 0
		if self.guildStr:
			self.pillT.SetText("Lonca  |cffe8d08a%s|r" % self.guildStr)
			pillW = int(self._TextW(self.pillT) / max(self.k * ZOOM, 0.01)) + 16
		self.nameT.SetText(self.nameStr)
		nameW = min(NAME_MAX, int(self._TextW(self.nameT) / max(self.k * ZOOM, 0.01)) + 2)
		self.fit = saved
		headW = FLAG_W + 8 + nameW + 14 + (pillW and pillW + 10 or 0) + CLOSE
		return (2 * PAD_X + max(rowW, headW), ws, pillW, nameW)

	def __Layout(self):
		if not self.entries:
			return
		sig = (tuple(self.entries), self.nameStr, self.guildStr)
		if sig == self.layoutSig:
			return
		self.layoutSig = sig
		(W, ws, pillW, nameW) = self.__Measure()
		# yuva: metin karti ile AYNI (HUD dugmelerinin gercek konumu); sigmazsa orantili kucul, yeri degismez
		if HK:
			(gL, gR) = HK.HudGapOrFrac(self.scrW, self.scrH, self.k)
		else:
			(gL, gR) = (int(0.075 * self.scrW + 24 * self.k), self.scrW - int(736 * self.k))
		full = W * self.k * ZOOM
		fit = 1.0
		if gR - gL < full:
			fit = (gR - gL) / float(full)
		if fit >= FIT_MIN:
			self.fit = fit
			self.cardX = gL + max(0, (gR - gL - int(round(full * fit))) // 2)
			self.cardY = int(round(CARD_TOP * self.k))
		else:		# 4:3 tablet: ust menu Gizle'ye neredeyse degiyor, arada yer yok (bkz. uihedefkarti)
			self.fit = 1.0
			self.cardX = (self.scrW - int(round(full))) // 2
			self.cardY = int(round(self.scrH * TOP_FRAC))
		S = self.S
		self.cardW = W
		self.box.SetSize(S(W), S(CARD_H))
		if self.state != "aciliyor":
			self.box.SetPosition(self.cardX, self.cardY)
		self.__Frame(W, CARD_H)
		f = self._ImgScale()
		# baslik: bayrak \xb7 lonca hapi \xb7 ad \xb7 X
		hy = PAD_T
		self.flag.SetScale(f, f)
		self.flag.SetPosition(S(PAD_X) - S(V.FLAG_PAD / V.B), S(hy) - S(V.FLAG_PAD / V.B))
		# KULLANICI (2026-10-01): "nicki sola, loncayi saga al" -> bayrak \xb7 AD .......... [Lonca hapi] \xb7 X
		self.pillT.SetFontName(self._Font(12.5))
		self.nameT.SetFontName(self._Font(18))
		self._Fit(self.nameT, self.nameStr, S(NAME_MAX))
		self.nameT.SetPosition(S(PAD_X + FLAG_W + 8), S(hy + HEAD_H / 2.0))
		if pillW:
			px = W - PAD_X - CLOSE - 10 - pillW
			py = hy + (HEAD_H - PILL_H) / 2.0
			for w in (self.pillBg, self.pillFr):
				w.SetPosition(S(px), S(py))
				w.SetSize(S(pillW), S(PILL_H))
				w.Show()
			self.pillT.SetText("Lonca  |cffe8d08a%s|r" % self.guildStr)
			self.pillT.SetPosition(S(px + 8), S(hy + HEAD_H / 2.0))
			self.pillT.Show()
		else:
			for w in (self.pillBg, self.pillFr, self.pillT):
				w.Hide()
		self.closeBtn.SetPosition(S(W - PAD_X - CLOSE), S(hy + (HEAD_H - CLOSE) / 2.0))
		if hasattr(wndMgr, "SetButtonScale"):
			wndMgr.SetButtonScale(self.closeBtn.hWnd, f, f)
		# ayrac
		sy = hy + HEAD_H + SEP_T
		self.sep.SetPosition(S(PAD_X + 2), S(sy))
		self.sep.SetScale((W - 2 * PAD_X - 4) * self.k * ZOOM * self.fit / float(V.AYRAC_W), f)
		# dugmeler
		by = sy + 1 + SEP_B
		bx = PAD_X + (max(0, (W - 2 * PAD_X) - (sum(ws) + BTN_GAP * max(0, len(ws) - 1))) / 2.0)
		for i in xrange(MAX_TILES):
			t = self.tiles[i]
			if i >= len(self.entries):
				continue
			bw = ws[i]
			if t["skin"] != bw:
				t["skin"] = bw
				t["btn"].SetUpVisual(DIR + "btn_%d_up.png" % bw)
				t["btn"].SetOverVisual(DIR + "btn_%d_up.png" % bw)
				t["btn"].SetDownVisual(DIR + "btn_%d_down.png" % bw)
			if hasattr(wndMgr, "SetButtonScale"):
				wndMgr.SetButtonScale(t["btn"].hWnd, f, f)
			t["x"] = bx
			t["y"] = by
			t["w"] = bw
			t["btn"].SetPosition(S(bx), S(by))
			bx += bw + BTN_GAP
		self.__DrawTiles()

	def __Frame(self, W, H):
		"""ui.ThinBoard ile ayni birlesim: 4 kose + 4 DOSENEN kenar + dolgu; texel olcegi TB_SCALE (metin karti kosesi)"""
		s = TB_SCALE * self.k * self.fit		# texel -> ekran px
		c = TB_TEX * s
		Wp = W * self.k * ZOOM * self.fit
		Hp = H * self.k * ZOOM * self.fit
		ci = int(round(c))
		for n in ("LeftTop", "RightTop", "LeftBottom", "RightBottom"):
			self.corners[n].SetScale(s, s)
		self.corners["LeftTop"].SetPosition(0, 0)
		self.corners["RightTop"].SetPosition(int(round(Wp - c)), 0)
		self.corners["LeftBottom"].SetPosition(0, int(round(Hp - c)))
		self.corners["RightBottom"].SetPosition(int(round(Wp - c)), int(round(Hp - c)))
		lh = max(1.0, Wp - 2 * c)
		lv = max(1.0, Hp - 2 * c)
		for n in self.lines:
			self.lines[n].SetScale(s, s)
		if HAS_RRS:
			rh = lh / (TB_TEX * s) - 1.0
			rv = lv / (TB_TEX * s) - 1.0
		else:		# eski APK: kenar uzatmasi olceksiz texel -> uzunluk dogru, desen yogunlugu hafif farkli
			rh = (lh - TB_TEX * s) / TB_TEX
			rv = (lv - TB_TEX * s) / TB_TEX
		self.lines["Top"].SetPosition(ci, 0)
		self.lines["Bottom"].SetPosition(ci, int(round(Hp - c)))
		self.lines["Left"].SetPosition(0, ci)
		self.lines["Right"].SetPosition(int(round(Wp - c)), ci)
		self.lines["Top"].SetRenderingRect(0.0, 0.0, rh, 0.0)
		self.lines["Bottom"].SetRenderingRect(0.0, 0.0, rh, 0.0)
		self.lines["Left"].SetRenderingRect(0.0, 0.0, 0.0, rv)
		self.lines["Right"].SetRenderingRect(0.0, 0.0, 0.0, rv)
		self.fill.SetPosition(ci, ci)
		self.fill.SetSize(max(1, int(round(Wp - 2 * c))), max(1, int(round(Hp - 2 * c))))

	def __DrawTiles(self):
		S = self.S
		f = self._ImgScale()
		icL = V.IC_PX / V.B		# simge gorselinin mantiksal boyu (golge payi dahil)
		for i in xrange(MAX_TILES):
			t = self.tiles[i]
			if i >= len(self.entries):
				for w in (t["btn"], t["ic"], t["lbl"], t["off"]):
					w.Hide()
				continue
			(name, enabled) = self.entries[i]
			key = self.actions.get(name, "whisper")
			if key in RED_KEYS:
				lblF = "lbl_%s_r.png" % key
			elif not enabled:
				lblF = "lbl_%s_o.png" % key
			else:
				lblF = "lbl_%s_n.png" % key
			icd = V.IC.get(key, {})
			icF = (not enabled and icd.get("o")) or icd.get("n") or "ic_whisper_n.png"
			if t["icF"] != icF:
				t["icF"] = icF
				t["ic"].LoadImage(DIR + icF)
			if t["lblF"] != lblF:
				t["lblF"] = lblF
				t["lbl"].LoadImage(DIR + lblF)
			for w in (t["ic"], t["lbl"], t["off"]):
				w.SetScale(f, f)
			(lw, lh) = self._Lbl(lblF)
			(ow, oh) = self._Lbl("yakin_degil.png")
			# dikey yigin: simge (22) + 1 + yazi murekkebi (~12) [+ "yakin degil" (~10)]; gorsel paylari dusulur
			pad = 3.0 / V.B
			ink = lh - 2 * pad
			oink = oh - 2 * pad
			stack = ICON + 1 + ink + ((not enabled) and (oink) or 0)
			top = t["y"] + (BTN_H - stack) / 2.0
			cx = t["x"] + t["w"] / 2.0
			t["ic"].SetPosition(S(cx - icL / 2.0), S(top - (icL - ICON) / 2.0))
			t["lbl"].SetPosition(S(cx - lw / 2.0), S(top + ICON + 1 - pad))
			if enabled:
				t["off"].Hide()
			else:
				t["off"].SetPosition(S(cx - ow / 2.0), S(top + ICON + 1 + ink - pad))
				t["off"].Show()
			t["btn"].SetDownVisual(DIR + "btn_%d_%s.png" % (t["w"], enabled and "down" or "up"))
			t["btn"].Show()
			t["ic"].Show()
			t["lbl"].Show()

	# ------------------------------------------------------------------ eylemler
	def __Entries(self):
		b = self.board
		out = []
		for group in self.order:
			pick = None
			for name in group:
				try:
					btn = b.buttonDict.get(name)
				except:
					btn = None
				if btn and btn.IsShow() and name in self.actions:
					pick = (name, True)
					break
			if pick is None and len(group) == 1 and group[0] in self.always:
				pick = (group[0], False)	# menzil disi: yerinde, soluk
			if pick:
				out.append(pick)
		return out[:MAX_TILES]

	def Blocked(self, vid=None):
		## GERCEK CLIENT (root/uitarget.py RefreshButton): "if player.IsPVPInstance(self.vid) or player.IsObserverMode():
		## return" -> DUELLO/PVP sirasinda ya da gozlemcide HIC dugme yok. Mobilde bu durumda panel ACILMAZ.
		if vid is None:
			vid = self.board and self.board.vid or 0
		try:
			if player.IsObserverMode():
				return True
			if vid and player.IsPVPInstance(vid):
				return True
		except:
			pass
		return False

	def Rebuild(self, force=False):
		if self.Blocked():
			if self.box.IsShow():
				self.CloseNow()
			return
		entries = self.__Entries()
		if not [e for e in entries if e[1]]:
			## gercek client: gorunen dugme yoksa panelin anlami yok
			if self.box.IsShow():
				self.CloseNow()
			self.entries = []
			return
		if force:
			self.layoutSig = None
		self.entries = entries
		self.__Layout()

	def __OnTile(self, i):
		try:
			(name, enabled) = self.entries[i]
		except:
			return
		if not enabled:
			msg = FAR_MSG.get(self.actions.get(name))
			if msg:
				self.__Toast(msg)
			return
		b = self.board
		try:
			btn = b.buttonDict.get(name)
			if btn and btn.eventFunc:
				if btn.eventArgs:
					apply(btn.eventFunc, btn.eventArgs)
				else:
					btn.eventFunc()
		except:
			import traceback
			dbg.TraceError("PlayerPanel eylem %s: %s" % (name, traceback.format_exc()))
		## KULLANICI (2026-09-24): her eylemden sonra panel kapanir (mandalli)
		self.UserClose()

	def __OnClose(self):
		self.UserClose()

	def Toast(self, msg):
		pass

	# ------------------------------------------------------------------ oyuncu bilgisi
	def SetInfo(self, vid, name):
		self.nameStr = name or ""
		guildName = ""
		try:
			gid = chr.GetGuildID(vid)
			if gid:
				import guild
				guildName = guild.GetGuildName(gid)
				if guildName == "Noname":
					guildName = ""
		except:
			guildName = ""
		self.guildStr = guildName or ""
		self.__Layout()

	def SetHP(self, pct, cur, mx):
		return	# KULLANICI (2026-09-28): can cubugu kalkti

	# ------------------------------------------------------------------ ac/kapa
	def IsOpen(self):
		return self.box.IsShow()

	def Open(self):
		b = self.board
		if not b:
			return
		# kapatmadan hemen sonra yolda olan hedef paketi paneli yeniden acmasin (0.7 s)
		if app.GetTime() < self.suppressUntil and b.vid == self.suppressVid:
			return
		# kapatma = mandal (closedVid): hedef birakilmaz (ClearTarget bekleme suresinde yok sayilir - buyuk bug)
		if b.vid != self.closedVid:
			self.closedVid = 0
		elif self.closedVid:
			return
		if self.Blocked(b.vid) or not self.IsPlayerTarget(b.vid):
			self.CloseNow()
			return
		fresh = (not self.box.IsShow()) or self.openVid != b.vid
		if fresh:
			self.layoutSig = None
		self.Rebuild()
		if not self.entries:
			return		# gosterilecek dugme yok (Rebuild kapatti)
		self.SetInfo(b.vid, b.nameString)
		if not fresh:
			return
		self.openVid = b.vid
		self.lastNear = None
		self.state = "aciliyor"
		self.animT0 = app.GetTime()
		self.box.SetPosition(self.cardX, self.cardY - self.S(14))
		self.box.SetTop()
		self.box.Show()

	def UserClose(self):
		b = self.board
		if b and b.vid:
			self.closedVid = b.vid
		self.Close()

	## GERCEK CLIENT: oyuncu dugmeleri yalniz SetPCTargetBoard -> TargetBoard.Open'da (IsPC/IsBuilding) acilir.
	def IsPlayerTarget(self, vid):
		try:
			if not vid or player.IsMainCharacterIndex(vid):
				return False
			return chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_PLAYER
		except:
			return False

	def ReopenByTap(self, vid):
		b = self.board
		if not b or b.vid != vid:
			return False
		if not self.IsPlayerTarget(vid):
			return False
		if self.Blocked(vid):
			return False
		self.closedVid = 0
		self.suppressUntil = 0.0
		## gercek client her Open'da RefreshButton cagirir; yeniden dokunmada sunucu paketi gelmedigi icin burada tazelenir
		try:
			b.RefreshButton()
		except:
			pass
		self.Open()
		return True

	def Close(self):
		if not self.box.IsShow():
			return
		self.suppressUntil = app.GetTime() + 0.7
		self.suppressVid = self.openVid
		self.CloseNow()

	def CloseNow(self):
		self.state = "kapali"
		self.openVid = 0
		self.box.Hide()

	def OnOutsideTap(self):
		if self.IsOpen() and self.board:
			self.board.OnOutsideTap()

	def OnOutsideTapUI(self):
		pass

	def OnUpdate(self):
		self.__UpdateToast()		# kart kapansa da uyari suresini tamamlar
		if not self.box.IsShow():
			return
		if self.state == "aciliyor":
			p = (app.GetTime() - self.animT0) / OPEN_SEC
			if p >= 1.0:
				p = 1.0
				self.state = "acik"
			dy = int(round(self.S(14) * (1.0 - _EaseOut(p))))
			self.box.SetPosition(self.cardX, self.cardY - dy)
		b = self.board
		if self.state == "acik" and b and b.vid and not player.IsMainCharacterIndex(b.vid):
			try:
				dist = player.GetCharacterDistance(b.vid)
				if dist < 0 or dist > CLOSE_RANGE:
					player.ClearTarget()
					b.Close()
					return
				## KULLANICI (2026-10-01): "mesafeler yanlis" - Ticaret/Zar menzili kart ACIKKEN de canli: uzaklasinca
				## dugme aninda solar ("yakin degil" + uyari), yaklasinca acilir. TargetBoard gizli oldugu icin kendi
				## OnUpdate'i calismiyordu; menzil sinirini gecince RefreshButton (-> Rebuild) cagrilir.
				now = app.GetTime()
				if now >= self.nextRange:
					self.nextRange = now + RANGE_TICK
					near = dist <= getattr(b, "EXCHANGE_LIMIT_RANGE", 900)
					if self.lastNear is None:
						self.lastNear = near
					elif near != self.lastNear:
						self.lastNear = near
						b.RefreshButton()
			except:
				pass
