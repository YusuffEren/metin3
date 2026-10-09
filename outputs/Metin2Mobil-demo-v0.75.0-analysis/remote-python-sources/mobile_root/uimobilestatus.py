# -*- coding: latin-1 -*-
# MOBIL: durum HUD'u (KULLANICI 2026-09-24 gece, tasarim Desktop/Metin2-Durum-HUD/durum-hud.html):
# 4 EXP kuresi (disli halka, alttan dolan altin sivi + yuzey dalgasi, Romen rakami, aktif kurede kirmizi nabiz,
# dokununca EXP yazisi) + altigen HP / SP / ENERJI satirlari (akan cizgili dolgu, uc parlamasi, ortali yazi).
#
# KULLANICI: "animasyonlarini ozellikle unutma tam takir olmali prototipteki gibi" - hepsi burada:
#   hudEnter (.8 s belirme + 45 px yukari kayma), runeSpin (aktif disli 4 s/tur), orbPulse (1.2 s), expWave
#   (1.7 s ileri-geri), expGain (.75 s kaldirma + buyume), flow (cizgiler 1.4 s / 24 px), barFlash (.45 s),
#   damage (.42 s sarsinti), dolum gecisleri (bar .7 s, kure 1.1 s, cubic-bezier(.16,.8,.2,1)), show-exp (.22 s).
#
# Dokular tools/status_hud_export.py -> mobile/ui/hud2/ (2x, tasarim 1280x705); geometri mobilestatusgeom.py
# (tasarim px, HUD kutusuna gore). Oyunda k = ekran yuksekligi / 705, dokular k/2 olcekle cizilir.
# Kirpma (dolumlar): wndMgr.SetRenderingRectScaled (APK v61+) ile olcekli gorselde piksel-dogru; yoksa
# ekran-dogru / UV-gergin yaklasim (eski APK'da gorunum biraz bozuk ama calisir).
# Kok pencere not_pick; yalniz kure dokunma alanlari secilebilir (EXP yazisi).
#
# KULLANICI (2026-10-03): EXP kureleri YENI TASARIM + SIVI DOLUM -> uiexpkure.ExpKureler (eski disli/altin kure
#   pencereleri ve alt cizgi kaldirildi; yedek tools/exp_kure/yedek_20261003). Ustteki "EXP %" yazisi ve dokununca
#   cikan yazi AYNI; yazi artik sivi ile birlikte sayar (F x 25).
import math
import ui
import wndMgr
import app
import player
import localeInfo
import mobilestatusgeom as G
import uiexpkure

DIR = "mobile/ui/hud2/"
TEX_S = 2.0
C_LABEL = 0xfff8ecd3
C_EXP1 = 0xfffff0c3
C_EXP2 = 0xffd1b878
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")
SCALE = 0.66			# tasarima gore kucultme (KULLANICI: cok buyuk)
FONT_BAR = "Tahoma:12"
FONT_EXP1 = "Tahoma:11"
FONT_EXP2 = "Tahoma:9"
# KULLANICI: "hero kafasindaki metin belirgin olsun, buyut, silik olmasin" -> 14 -> 20, parlak krem (d5c39e soluktu)
FONT_TOAST = "Tahoma:20"
FONT_EXPLBL = "Tahoma:17"		# kurelerin ustundeki sabit "EXP %xx.x"
EXPLBL_Y = -50.0
## KULLANICI (2026-09-27): "kutular dolunca tam sari olmuyor, icinde siyahlik var" - altin dolgu (62 px) ic koyu
## diskten (87 px) kucuktu; halkanin ic kenarina (~84 px) kadar buyutulur (merkez etrafinda, seviye kirpmasi oransal).
GOLD_FIT = 84.0 / 62.0
ORB_GRP_CX = (81.5 + 348.5 + 3 * 7.0) / 2.0	# eski kure grubunun (ve "EXP %" yazisinin) yatay merkezi, tasarim px
ORB_GAP = 7.0			# kureler arasi ek bosluk (tasarim px) - kenarlar birbirine degmesin			# tasarim px (kure grubu), aktif kurenin (orb_hot -23.75) ustu
C_TOAST = 0xfffff0c3
ROMAN = ("I", "II", "III", "IV")
DEBUG_EXP = 0		# test icin 0..1 (orn. 0.62); yayinda 0
## KULLANICI (2026-09-26): "eski hp sp enerjiyi ekrandan kaldir" - HP/SP artik mini haritadaki yaylarda
## (uiminimaphud.py). Satirlar kurulur (uitaskbar SetBar API'si ayni kalir) ama cizilmez.
SHOW_BARS = 0


def _ease_out3(t):
	t = max(0.0, min(1.0, t))
	return 1.0 - (1.0 - t) ** 3


def _ease_out2(t):
	t = max(0.0, min(1.0, t))
	return 1.0 - (1.0 - t) * (1.0 - t)


def _smooth(t):
	t = max(0.0, min(1.0, t))
	return t * t * (3.0 - 2.0 * t)


def _bump(t, peak):
	"""0 -> 1 (peak) -> 0, t 0..1."""
	if t <= 0.0 or t >= 1.0:
		return 0.0
	if t < peak:
		return t / peak
	return 1.0 - (t - peak) / (1.0 - peak)


def _fmt(n):
	"""41276 -> '41.276' (tasarim: toLocaleString tr-TR)."""
	try:
		n = int(n)
	except:
		return str(n)
	s = str(abs(n))
	out = ""
	while len(s) > 3:
		out = "." + s[-3:] + out
		s = s[:-3]
	return ("-" if n < 0 else "") + s + out


class _Tween(object):
	"""Sabit sureli, cubic-bezier(.16,.8,.2,1) benzeri ease-out gecis."""

	def __init__(self, value, dur):
		self.v0 = value
		self.v1 = value
		self.t0 = -1.0
		self.dur = dur

	def Set(self, target, t, instant=False):
		if instant:
			self.v0 = self.v1 = target
			self.t0 = -1.0
			return
		if abs(target - self.v1) < 1e-9:
			return
		self.v0 = self.Get(t)
		self.v1 = target
		self.t0 = t

	def Get(self, t):
		if self.t0 < 0.0:
			return self.v1
		p = (t - self.t0) / self.dur
		if p >= 1.0:
			self.t0 = -1.0
			return self.v1
		return self.v0 + (self.v1 - self.v0) * _ease_out3(p)


class _OrbTap(ui.Window):
	def __init__(self, parent, func):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.func = func

	def OnMouseLeftButtonDown(self):
		self.func()
		return True

	def OnMouseLeftButtonUp(self):
		return True


class MobileStatusHud(ui.Window):
	ROWS = ("HP", "SP", "EN")
	FILL_IMG = ("fill_hp.png", "fill_sp.png", "fill_en.png")
	CAP_W = 14.0			# dolgu sag ucu (bevel 6 + parlama) - tasarim px
	DUR_BAR = 0.7
	DUR_EXP = 1.1
	## KULLANICI (2026-09-26): "can barini (HP/SP/Enerji) en uste alalim, uzerindeki yaziyi kaldiralim, biraz
	## kucultelim cok uzun" + "expler ayni yerde, tam asagi yaklassin". Iki ayri yerlesim grubu (__Grp):
	##   bar: panel + 3 satir ekranin SOL USTUNDE (Gizle/Etkinlik sutununun sagi), yatay BAR_SX / dikey BAR_SY olcek
	##   orb: EXP kureleri + alt cizgi ekranin dibinde
	BAR_SX = 0.60
	BAR_SY = 0.90
	BAR_LEFT = 0.100		# ekran genisligi orani (sol ustteki buf ikonlari + Gizle/Etkinlik dugmelerinin sagi)
	BAR_TOP = 6.0			# ekran ust kenarindan (tasarim px * k)
	ORB_BOTTOM = 94.25 + 3.0	# kure govdesi alt kenari + bosluk (tasarim px)

	def __init__(self, parent):
		ui.Window.__init__(self)
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetParent(parent)
		self.SetWindowName("MobileStatusHud")
		self.AddFlag("not_pick")
		W = float(wndMgr.GetScreenWidth())
		H = float(wndMgr.GetScreenHeight())
		# KULLANICI: "cok buyuk, kucultmeliyiz" -> tasarim olceginin %66'si
		self.k = H / 705.0 * SCALE
		k = self.k
		# HUD kutusu: kamera kaydiricinin sagi (0.049 W), alt kenardan 8 px
		self.x0 = int(round(W * 0.049))
		self.y0 = int(round(H - self.ORB_BOTTOM * k))
		self.W = W
		self.H = H
		self.__Grp("orb")
		self.SetPosition(0, 0)
		# KULLANICI: "ustune tiklayinca animasyon oynamiyor" - CWindow::PickWindow cocuklara ancak nokta EBEVEYN
		# dikdortgenindeyse iner; 1x1 kok kure dokunma alanlarini hic secmiyordu. Tam ekran + not_pick.
		self.SetSize(int(W), int(H))
		self.keep = []
		self.parts = {}
		self.t = app.GetTime()
		self.tEnter = -1.0
		self.enterY = 0.0
		self.enterA = 1.0
		# --- barlar
		self.bar = []
		self.__BuildStatic()
		self.__Grp("bar")
		for i in xrange(3):
			self.bar.append(self.__BuildRow(i))
		# --- kureler: KULLANICI (2026-10-03) yeni tasarim + sivi dolum (uiexpkure). Eski kure grubunun merkezinde,
		# boyu eskisiyle ayni (64 birim x H/705 ~ eski 98 tasarim px x 0.66).
		self.__Grp("orb")
		kk = H / 705.0
		rowCX = self.x0 + ORB_GRP_CX * self.k
		rowCY = self.y0 + G.ORB_C[0][1] * self.k
		self.kure = None
		try:
			self.kure = uiexpkure.ExpKureler(self, kk, rowCX, rowCY)
		except:
			import dbg, traceback
			dbg.TraceError("MOBIL EXP kureleri kurulamadi: " + traceback.format_exc())
			self.kure = None
		d = int(round(64.0 * kk))
		for i in xrange(4):
			tap = _OrbTap(self, lambda i=i: self.__OnOrbTap(i))
			cx = rowCX + (i - 1.5) * uiexpkure.ORB_STEP * kk
			tap.SetPosition(int(round(cx - d / 2.0)), int(round(rowCY - d / 2.0)))
			tap.SetSize(d, d)
			tap.Show()
			self.keep.append(tap)
		self.expCur = 0
		self.expMax = 1
		self.expLv = -1
		self.expTap = -1
		self.expTapT = -1.0
		self._kEnter = None
		# .status bildirimi: ekran ortasi %43, dokununca "EXP I . %72" (1.1 s, .3 s gecis)
		self.toast = self.__Text(FONT_TOAST, C_TOAST)
		self.toast.Hide()
		self.toastT = -1.0
		self.toastText = ""
		## KULLANICI (2026-09-27): "kutularin ustunde yaziyla exp % kac sabit de yazsin" - toplam EXP yuzdesi
		self.expLabel = self.__Text(FONT_EXPLBL, C_TOAST)
		self.W = W
		self.H = H
		self.Show()

	# ------------------------------------------------------------------ kurulum
	def __Img(self, name, offset=None):
		w = ui.ExpandedImageBox()
		w.SetParent(self)
		w.AddFlag("not_pick")
		w.LoadImage(DIR + name)
		max(0, 0)	# LoadImage bekleyen hatasini burada tetikle
		# DOKU boyutu OLCEKTEN ONCE okunur (GetWidth olcekli doner; disli halkanin donme merkezi kaymisti)
		self.parts[w] = (float(w.GetWidth()), float(w.GetHeight()))
		w.SetScale(self.k / TEX_S, self.k / TEX_S)
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		self.keep.append(w)
		if offset is not None:
			w.SetPosition(self.__X(offset[0]), self.__Y(offset[1]))
		w.Show()
		return w

	def __Text(self, font, color):
		t = ui.TextLine()
		t.SetParent(self)
		t.AddFlag("not_pick")
		t.SetFontName(font)
		t.SetOutline()
		t.SetHorizontalAlignCenter()
		t.SetPackedFontColor(color)
		t.Show()
		self.keep.append(t)
		return t

	def __Grp(self, name):
		"""etkin yerlesim grubu: ekran kokeni (gx0, gy0) + tasarim px basina ekran px (gkx, gky)."""
		k = self.k
		if name == "bar":
			self.gkx = k * self.BAR_SX
			self.gky = k * self.BAR_SY
			self.gx0 = self.W * self.BAR_LEFT - G.panel[0] * self.gkx
			self.gy0 = self.BAR_TOP * k - G.panel[1] * self.gky
		else:
			self.gkx = k
			self.gky = k
			self.gx0 = float(self.x0)
			self.gy0 = float(self.y0)
		self.rsx = self.gkx / k
		self.rsy = self.gky / k

	def GetBarRight(self):
		"""bar panelinin sag kenari (ekran px) - game.py buff ikon satirini buradan baslatir."""
		kx = self.k * self.BAR_SX
		return int(round(self.W * self.BAR_LEFT + G.panel[2] * kx))

	def __X(self, dx):
		return int(round(self.gx0 + dx * self.gkx))

	def __Y(self, dy):
		return int(round(self.gy0 + dy * self.gky))

	def __BuildStatic(self):
		self.__Grp("bar")
		self.panel = self.__Img("panel.png", G.panel)
		self.__Grp("orb")
		self.line = self.__Img("line.png", G.line)
		self.line.Hide()		# KULLANICI (2026-10-03) yeni kure tasarimi: alt cizgi yok

	def __BuildRow(self, i):
		(rx, ry, rw, rh) = G.ROW[i]
		fg = getattr(G, ("fill_hp", "fill_sp", "fill_en")[i])
		r = {}
		r["off"] = (rx, ry)
		r["bg"] = self.__Img("row.png", (G.row[0], G.row[1] + (ry - G.ROW[0][1])))
		# PC HP/SPRecoveryGaugeBar (iksir bekleyen kismi)
		bar = ui.Bar()
		bar.SetParent(self)
		bar.AddFlag("not_pick")
		bar.SetColor(0x55ff0000)
		bar.SetPosition(self.__X(rx + G.FILL_INSET + 2), self.__Y(ry + G.FILL_INSET + 2))
		bar.SetSize(1, int((rh - 2 * G.FILL_INSET - 4) * self.gky))
		bar.Hide()
		self.keep.append(bar)
		r["rec"] = bar
		r["fillOff"] = (fg[0], fg[1])		# her satirin dolgusu kendi satirindan dilimlendi (ofset eklenmez)
		r["fillW"] = fg[2]
		r["mid"] = self.__Img(self.FILL_IMG[i])
		r["cap"] = self.__Img(self.FILL_IMG[i])
		r["stripes"] = self.__Img("stripes.png")
		r["flashMid"] = self.__Img("fill_flash.png")
		r["flashCap"] = self.__Img("fill_flash.png")
		r["head"] = self.__Img("head.png")
		r["label"] = self.__Text(FONT_BAR, C_LABEL)
		r["label"].Hide()		# KULLANICI: bar ustundeki yazi kaldirildi
		r["tw"] = _Tween(1.0, self.DUR_BAR)
		r["flashT"] = -1.0
		r["dmgT"] = -1.0
		r["cur"] = 0
		r["max"] = 0
		r["shown"] = False
		return r


	# ------------------------------------------------------------------ yerlestirme yardimcilari
	def __Put(self, w, dx, dy, alpha=1.0, sx=1.0, sy=1.0, rot=0.0, yoff=0.0):
		"""Tasarim ofsetine (HUD kutusu) koy; sx/sy ek olcek, rot derece (merkez etrafinda)."""
		(tw, th) = self.parts[w]
		fx = self.k / TEX_S * sx * self.rsx
		fy = self.k / TEX_S * sy * self.rsy
		ww = tw * fx
		hh = th * fy
		w.SetScale(fx, fy)
		if rot != 0.0 or sx != 1.0 or sy != 1.0:
			# olcek/donme merkez etrafinda: tasarim kutusunun merkezi sabit kalir
			cx = self.gx0 + (dx + tw / TEX_S / 2.0) * self.gkx
			cy = self.gy0 + (dy + th / TEX_S / 2.0) * self.gky + yoff * self.gky + self.enterY
			w.SetRotation(rot)
			w.SetOrigin(ww / 2.0, hh / 2.0)
			w.SetPosition(int(round(cx - ww / 2.0)), int(round(cy - hh / 2.0)))
		else:
			w.SetRotation(0.0)
			w.SetPosition(self.__X(dx), int(round(self.gy0 + (dy + yoff) * self.gky + self.enterY)))
		w.SetAlpha(max(0.0, min(1.0, alpha * self.enterA)))
		if not w.IsShow():
			w.Show()


	def __Clip(self, w, l, t, r, b):
		"""Kirpma oranlari (0..1, sol/ust/sag/alt kesilen pay). Olcekli bayrak yoksa ekran-dogru yaklasim."""
		s = 1.0 if HAS_RRS else self.k / TEX_S
		w.SetRenderingRect(-l * s, -t * s, -r * s, -b * s)

	def __TextAt(self, t, color, alpha, dx, dy, text, yoff=0.0):
		a = int(max(0.0, min(1.0, alpha * self.enterA)) * 255)
		t.SetPackedFontColor((a << 24) | (color & 0xffffff))
		t.SetText(text)
		t.SetPosition(self.__X(dx), int(round(self.gy0 + (dy + yoff) * self.gky + self.enterY)))
		if not t.IsShow():
			t.Show()

	# ------------------------------------------------------------------ dis API (uitaskbar)
	def SetBar(self, i, cur, maxv, label, recovery=0):
		r = self.bar[i]
		t = app.GetTime()
		cur = max(0, min(cur, maxv))
		if maxv <= 0:
			return
		pct = float(cur) / float(maxv)
		if r["shown"] and r["max"] > 0:
			if cur < r["cur"] and i == 0:
				r["dmgT"] = t		# hasar sarsintisi (yalniz HP azalinca; tasarim: hp && value < max)
			elif cur > r["cur"] or (i != 0 and cur != r["cur"]):
				r["flashT"] = t		# yenilenme parlamasi
		r["tw"].Set(pct, t, instant=not r["shown"])
		r["cur"] = cur
		r["max"] = maxv
		r["shown"] = True
		r["text"] = "%s %s / %s" % (label, _fmt(cur), _fmt(maxv))
		# iksir bekleyen kismi (PC __SetRecoveryBar)
		if recovery > 0 and SHOW_BARS:
			dest = min(maxv, cur + recovery)
			innerW = (G.ROW[i][2] - 2 * G.FILL_INSET - 4) * self.k
			r["rec"].SetSize(max(1, int(innerW * float(dest) / float(maxv))), int((G.ROW[i][3] - 2 * G.FILL_INSET - 4) * self.k))
			r["rec"].Show()
		else:
			r["rec"].Hide()

	def SetExperience(self, cur, maxv):
		t = app.GetTime()
		if DEBUG_EXP:
			cur = int(maxv * DEBUG_EXP)
		cur = max(0, min(cur, maxv))
		first = (self.expMax <= 1 and self.expCur == 0)
		self.expCur = cur
		self.expMax = max(1, maxv)
		## KULLANICI (2026-10-03) sivi dolum: seviye atlayinca kureler dolar -> parlar -> bosalir -> yeni EXP'e dolar.
		## Atlama oyuncu seviyesinden anlasilir (EXP/gereken paketleri ara degerlerle gelebilir).
		try:
			lv = player.GetStatus(player.LEVEL)
		except:
			lv = -1
		levelUp = (not first) and self.expLv > 0 and lv > self.expLv
		if lv > 0:
			self.expLv = lv
		if self.kure:
			self.kure.SetTarget(4.0 * float(cur) / float(self.expMax), t, instant=first, levelUp=levelUp)

	def OnEnter(self):
		"""hudEnter: HUD ilk belirdiginde .8 s belirme + 45 px yukari kayma."""
		self.tEnter = app.GetTime()

	# ------------------------------------------------------------------ kure dokunusu
	def __OnOrbTap(self, i):
		t = app.GetTime()
		self.expTap = i
		self.expTapT = t
		## KULLANICI (2026-09-27): "hangi kutuya tiklarsak tiklayalim hepsinde % ayni olsun" -> toplam EXP yuzdesi
		pct = 100.0 * float(self.expCur) / float(max(1, self.expMax))
		self.toastText = "EXP  \xb7  %%%.1f" % pct
		self.toastT = t

	# ------------------------------------------------------------------ kare
	def OnUpdate(self):
		t = app.GetTime()
		## HIZ (2026-10-01): TaskBar.OnUpdate bu pencereyi ELLE de cagiriyor, motor da (TaskBar'in gorunur cocugu)
		## -> ayni karede ikinci cagri atlanir. app.GetTime kare basina sabit.
		if t == getattr(self, "_frameT", -1.0):
			return
		self._frameT = t
		self.t = t
		# hudEnter: cubic-bezier(.16,1,.3,1) ~ guclu ease-out
		if self.tEnter >= 0.0:
			p = (t - self.tEnter) / 0.8
			if p >= 1.0:
				self.tEnter = -1.0
				self.enterY = 0.0
				self.enterA = 1.0
			else:
				e = _ease_out3(p)
				self.enterY = 45.0 * self.k * (1.0 - e)
				self.enterA = min(1.0, p * 2.5)
		if SHOW_BARS:
			self.__Grp("bar")
			self.__Put(self.panel, G.panel[0], G.panel[1])
			for i in xrange(3):
				self.__UpdateRow(i, t)
		elif self.panel.IsShow():
			self.panel.Hide()
			for r in self.bar:
				for key in ("bg", "mid", "cap", "stripes", "flashMid", "flashCap", "head", "rec", "label"):
					r[key].Hide()
		## KULLANICI (2026-10-03): kureler uiexpkure'de (kendi hizini ayarlar: yalniz dolan kure canli, ~20/30 Hz).
		## "EXP %" yazisi sivi ile birlikte sayar; yazi yalniz degisince yeniden dizilir.
		kure = self.kure
		if kure:
			ek = (self.enterY, self.enterA)
			if ek != self._kEnter:
				self._kEnter = ek
				kure.SetEnter(self.enterY, self.enterA)
			kure.Update(t)
			pct = kure.F * 25.0
		else:
			pct = 100.0 * float(self.expCur) / float(max(1, self.expMax))
		key = (self.enterY, self.enterA, round(pct, 1))
		if key != getattr(self, "_lastKey", None):
			self._lastKey = key
			self.__Grp("orb")
			self.__TextAt(self.expLabel, C_TOAST, 1.0, ORB_GRP_CX, EXPLBL_Y, "EXP  %%%.1f" % pct)
		self.__UpdateToast(t)

	def __UpdateToast(self, t):
		# .status: opacity 0 -> 1 ve translateY 0 -> -8 px (.3 s), 1.1 s sonra geri (.3 s)
		if self.toastT < 0.0:
			self.toast.Hide()
			return
		el = t - self.toastT
		if el >= 1.4:
			self.toastT = -1.0
			self.toast.Hide()
			return
		if el < 1.1:
			p = _ease_out2(el / 0.3)
		else:
			p = 1.0 - _ease_out2((el - 1.1) / 0.3)
		a = int(max(0.0, min(1.0, p)) * 255)
		self.toast.SetPackedFontColor((a << 24) | (C_TOAST & 0xffffff))
		self.toast.SetText(self.toastText)
		self.toast.SetPosition(int(self.W / 2), int(self.H * 0.43 - 8.0 * self.k * p))
		if not self.toast.IsShow():
			self.toast.Show()

	def __UpdateRow(self, i, t):
		r = self.bar[i]
		(rx, ry) = r["off"]
		(rw, rh) = (G.ROW[i][2], G.ROW[i][3])
		# damage sarsintisi: 30% -4px, 55% +3px, 75% -2px, 100% 0
		xo = 0.0
		dmg = 0.0
		if r["dmgT"] >= 0.0:
			p = (t - r["dmgT"]) / 0.42
			if p >= 1.0:
				r["dmgT"] = -1.0
			else:
				keys = ((0.0, 0.0), (0.30, -4.0), (0.55, 3.0), (0.75, -2.0), (1.0, 0.0))
				for j in xrange(1, len(keys)):
					if p <= keys[j][0]:
						(p0, v0) = keys[j - 1]
						(p1, v1) = keys[j]
						xo = v0 + (v1 - v0) * (p - p0) / (p1 - p0)
						break
				dmg = _bump(p, 0.30) * 0.30
		flash = 0.0
		if r["flashT"] >= 0.0:
			p = (t - r["flashT"]) / 0.45
			if p >= 1.0:
				r["flashT"] = -1.0
			else:
				flash = _bump(p, 0.40) * 0.32	# tasarim brightness(1.7): hafif parlama (0.7 dolguyu soluk gosteriyordu)
		flash = max(flash, dmg)
		self.__Put(r["bg"], G.row[0] + xo, G.row[1] + (ry - G.ROW[0][1]))
		pct = r["tw"].Get(t) if r["shown"] else 0.0
		(fx, fy) = r["fillOff"]
		fw = r["fillW"]
		visW = pct * fw
		capW = self.CAP_W
		if pct <= 0.001:
			for key in ("mid", "cap", "stripes", "flashMid", "flashCap", "head"):
				r[key].Hide()
		else:
			if visW < capW:
				visW = capW
			midW = visW - capW
			# govde: [0, midW] ; uc: dokunun son capW px'i, visW - capW'de
			self.__Put(r["mid"], fx + xo, fy)
			self.__Clip(r["mid"], 0.0, 0.0, 1.0 - midW / fw, 0.0)
			self.__Put(r["cap"], fx + xo + (visW - fw), fy)
			self.__Clip(r["cap"], 1.0 - capW / fw, 0.0, 0.0, 0.0)
			# akan cizgiler (flow 1.4 s / 24 px, saga): dolgunun ic bolgesi (bevel disari)
			ph = (t / 1.4) % 1.0
			sx0 = fx + G.BEVEL
			sx1 = fx + visW - G.BEVEL - 2
			sw = sx1 - sx0
			if sw > 4:
				p = 24.0 - ph * 24.0
				stw = G.stripes[2]
				# doku tam dolgu ic yuksekliginde (17 tasarim px): yalniz yatay kirpma
				self.__Put(r["stripes"], sx0 + xo - p, ry + G.FILL_INSET)
				self.__Clip(r["stripes"], p / stw, 0.0, (stw - sw - p) / stw, 0.0)
			else:
				r["stripes"].Hide()
			# yenilenme parlamasi / hasar parlamasi: beyaz maske
			if flash > 0.0:
				self.__Put(r["flashMid"], fx + xo, fy, flash)
				self.__Clip(r["flashMid"], 0.0, 0.0, 1.0 - midW / fw, 0.0)
				self.__Put(r["flashCap"], fx + xo + (visW - fw), fy, flash)
				self.__Clip(r["flashCap"], 1.0 - capW / fw, 0.0, 0.0, 0.0)
			else:
				r["flashMid"].Hide()
				r["flashCap"].Hide()
			# uc parlamasi (.fill:after): dolgunun sag ucunda
			hx = fx + visW - G.BEVEL - G.head[2] / 2.0
			hy = fy + (rh - 2 * G.FILL_INSET) / 2.0 - G.head[3] / 2.0
			self.__Put(r["head"], hx + xo, hy)
		# iksir bekleyen kismi (ui.Bar) satirla birlikte
		if r["rec"].IsShow():
			r["rec"].SetPosition(self.__X(rx + xo + G.FILL_INSET + 2), int(round(self.gy0 + (ry + G.FILL_INSET + 2) * self.gky + self.enterY)))
		# yazi: KULLANICI (2026-09-26) kaldirildi (r["label"] gizli)



	def Destroy(self):
		self.Hide()		# isinlanmada eski HUD bellekte kalirsa cizmesin (uiminimap 2026-09-27 olayi)
		if getattr(self, "kure", None):
			self.kure.Destroy()
		self.kure = None
		self.keep = []
		self.bar = []
		self.parts = {}
