# -*- coding: latin-1 -*-
# MOBIL: dokunma geri bildirim efekti (KULLANICI 2026-09-24, tasarim Desktop/Tiklama-Geri-Bildirim-Efekti/
# tiklama-efekti.html). Her dokunusta (UI ya da dunya) dokunulan noktada: hale, neon halka (+ic halka), kose
# parantezli donen dis halka, cekirdek, arti isinlari, disari ucan kivilcimlar, zeminde yayilan elips.
# Hedefe (NPC/mob/metin) dokununca altin halka + "HEDEF" yazisi + 10 kivilcim (tasarim .target-hit).
#
# Kanca: wndMgr.SetTapHandler(self) -> OnTapDown(x, y) (native, pencere dagitimindan once; APK v58+).
# Dokular tools/bake_tapfx.py (2x). Parlamalar SCREEN kipinde (premultiplied doku, solma SetDiffuseColor),
# cizgiler normal alfa (solma SetAlpha). PERFORMANS: 2 efekt havuzu BIR kez yaratilir, bosta gizlidir; kare
# basi is yalniz aktif efekt icin konum/olcek/alfa. Kok pencere not_pick: dokunusu yutmaz, TOP_MOST ustunde.
#
# KULLANICI (2026-09-24): "baska yere tiklayinca iz kaliyor sonradan kayboluyor ... elini kesmeyle bitmesi
# gerek": efekt parmak kalkinca (wndMgr.IsLeftButtonDown 0) hemen soner (FADE_UP), yeni dokunus eskisini aninda
# keser (FADE_NEW). Cok kisa dokunusta patlama yine okunsun diye en az MIN_LIFE gosterilir.
import math
import ui
import wndMgr
import app
import chrmgr
import chr
import player

DIR = "mobile/ui/tapfx/"
TEX_S = 2.0				# doku pisirme carpani
POOL = 2				# biri sonerken yenisi baslar
## KULLANICI (2026-09-26): "biraz fazla slow, hizlansin hemen gecsin" -> sureler ~%35 kisa (tasarim .86 / .95 s)
DUR = 0.56
DUR_RIPPLE = 0.62
DUR_LABEL = 0.65
MIN_LIFE = 0.18			# parmak hemen kalksa bile en az bu kadar gorunur
FADE_UP = 0.08			# parmak kalkinca sonme suresi
FADE_NEW = 0.04			# yeni dokunus eskisini bu surede keser
## KULLANICI (2026-09-26): "biraz belirgin olsun, ton olarak kirmizi" - SCREEN parlamalari beyaz diffuse ile ekrana
## her renkten isik ekliyordu (acik zeminde soluk/seffaf). Yesil/maviyi kisip kirmiziyi tam birak -> doygun kirmizi.
TINT = (1.0, 0.42, 0.32)
TINT_CORE = (1.0, 0.78, 0.7)	# cekirdek beyaz kalsin ama sicak
C_LABEL = 0xfff0c59a
SCREEN = getattr(wndMgr, "RENDERING_MODE_SCREEN", 1)
SIZE = 0.75				# KULLANICI (2026-09-26): "dokununca cikan seffaf geri bildirimi biraz kucultelim"


def _ease_out(t):
	t = max(0.0, min(1.0, t))
	return 1.0 - (1.0 - t) * (1.0 - t)


def _spark_ease(t):
	# cubic-bezier(.15,.6,.2,1): hizli cikis, yumusak varis
	t = max(0.0, min(1.0, t))
	return 1.0 - (1.0 - t) ** 3


def _k(t, keys):
	"""keys: [(t0, v0), (t1, v1), ...] dogrusal kare arasi (0..1 normalize sure)."""
	if t <= keys[0][0]:
		return keys[0][1]
	for i in range(1, len(keys)):
		(t0, v0) = keys[i - 1]
		(t1, v1) = keys[i]
		if t <= t1:
			q = (t - t0) / max(1e-6, (t1 - t0))
			return v0 + (v1 - v0) * q
	return keys[-1][1]


class _Fx(object):
	"""Bir efekt seti (havuz elemani)."""

	RAYS = 10

	def __init__(self, parent, k):
		self.k = k
		self.t0 = -1.0
		self.tCut = -1.0
		self.fadeDur = FADE_UP
		self.fade = 1.0
		self.strong = False
		self.x = 0
		self.y = 0
		self.parts = {}
		self.screen = {}
		self.keep = []
		mk = self.__Mk
		# cizim sirasi: ripple, aura, cross x2, bracket, ring glow, ring, kivilcimlar, cekirdek (ustte)
		self.rippleGlow = mk(parent, "ripple_glow.png", True)
		self.ripple = mk(parent, "ripple.png", False)
		self.aura = mk(parent, "aura.png", True)
		self.auraHot = mk(parent, "aura_hot.png", True)
		self.crossX = mk(parent, "cross.png", True)
		self.crossY = mk(parent, "cross.png", True)
		self.bracket = mk(parent, "bracket.png", False)
		self.bracketHot = mk(parent, "bracket_hot.png", False)
		self.ringGlow = mk(parent, "ring_glow.png", True)
		self.ringGlowHot = mk(parent, "ring_glow_hot.png", True)
		self.ring = mk(parent, "ring.png", False)
		self.ringHot = mk(parent, "ring_hot.png", False)
		self.rays = [mk(parent, "ray.png", True) for i in xrange(self.RAYS)]
		self.core = mk(parent, "core.png", True)
		t = ui.TextLine()
		t.SetParent(parent)
		t.AddFlag("not_pick")
		t.SetFontName("Tahoma:%d" % max(9, int(round(11 * max(k, 1.0)))))
		t.SetOutline()
		t.SetHorizontalAlignCenter()
		t.SetPackedFontColor(C_LABEL)
		t.SetText("H E D E F")
		t.Hide()
		self.label = t
		self.keep.append(t)
		self.all = [self.rippleGlow, self.ripple, self.aura, self.auraHot, self.crossX, self.crossY, self.bracket,
					self.bracketHot, self.ringGlow, self.ringGlowHot, self.ring, self.ringHot, self.core] + self.rays

	def __Mk(self, parent, name, screen):
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(DIR + name)
		max(0, 0)		# LoadImage bekleyen hatasini burada tetikle
		if screen:
			# parlama: SCREEN karisimi (alfa yok sayilir, doku premultiplied); solma diffuse RGB ile
			w.SetRenderingMode(SCREEN)
		w.Hide()
		self.keep.append(w)
		self.parts[w] = (float(w.GetWidth()), float(w.GetHeight()))
		self.screen[w] = screen
		return w

	def IsActive(self):
		return self.t0 >= 0.0

	def Start(self, x, y, strong, t):
		self.t0 = t
		self.tCut = -1.0
		self.fade = 1.0
		self.strong = strong
		self.x = x
		self.y = y
		for w in self.all:
			w.Hide()
		self.label.Hide()
		self.Update(t)

	def Cut(self, t, dur):
		"""Efekti bitir: t aninda (en erken t0+MIN_LIFE) dur suresinde sondur."""
		if not self.IsActive():
			return
		tc = max(t, self.t0 + MIN_LIFE)
		if self.tCut < 0.0 or tc < self.tCut:
			self.tCut = tc
			self.fadeDur = dur
		elif dur < self.fadeDur:
			self.fadeDur = dur

	def Stop(self):
		self.t0 = -1.0
		self.tCut = -1.0
		for w in self.all:
			w.Hide()
		self.label.Hide()

	def __Put(self, w, cx, cy, scale, alpha, rot=0.0, sx=None, sy=None):
		"""Gorseli merkezi (cx, cy) olacak sekilde, tasarim px olcegiyle koy (scale = tasarim px / doku px * k)."""
		(tw, th) = self.parts[w]
		fx = (sx if sx is not None else scale) * self.k / TEX_S
		fy = (sy if sy is not None else scale) * self.k / TEX_S
		ww = tw * fx
		hh = th * fy
		w.SetScale(fx, fy)
		w.SetRotation(rot)
		w.SetOrigin(ww / 2.0, hh / 2.0)
		w.SetPosition(int(round(cx - ww / 2.0)), int(round(cy - hh / 2.0)))
		a = max(0.0, min(1.0, alpha * self.fade))
		if self.screen[w]:
			tn = TINT_CORE if w is self.core else TINT
			wndMgr.SetDiffuseColor(w.hWnd, a * tn[0], a * tn[1], a * tn[2], a)
		else:
			w.SetAlpha(a)
		if not w.IsShow():
			w.Show()

	def Update(self, t):
		el = t - self.t0
		if self.tCut >= 0.0 and t >= self.tCut:
			self.fade = 1.0 - (t - self.tCut) / max(0.01, self.fadeDur)
			if self.fade <= 0.0:
				self.Stop()
				return
		else:
			self.fade = 1.0
		if el > max(DUR, DUR_RIPPLE, DUR_LABEL) + 0.05:
			self.Stop()
			return
		x = self.x
		y = self.y
		p = min(1.0, el / DUR)		# tasarim: tum parcalar .86 s
		strong = self.strong
		# --- zemin dalgasi (ripple): olcek .4 -> 5, alfa .9 -> 0, .95 s
		pr = min(1.0, el / DUR_RIPPLE)
		rs = _k(pr, [(0.0, 0.4), (1.0, 5.0)])
		ra = 0.9 * (1.0 - _ease_out(pr))
		self.__Put(self.rippleGlow, x, y, rs, ra)
		self.__Put(self.ripple, x, y, rs, ra)
		# --- hale (aura): olcek .25 -> 1.35, alfa 0 -> 1 (%35) -> 0; hedefte genis doku
		au = strong and self.auraHot or self.aura
		(self.auraHot if not strong else self.aura).Hide()
		self.__Put(au, x, y, _k(p, [(0.0, 0.25), (1.0, 1.35)]), _k(p, [(0.0, 0.0), (0.35, 1.0), (1.0, 0.0)]))
		# --- arti isinlari: X olcek .1 -> 1 (alfa 0 -> .9 (%35) -> 0); Y aynisi dikey
		sc = _k(p, [(0.0, 0.1), (1.0, 1.0)])
		ac = _k(p, [(0.0, 0.0), (0.35, 0.9), (1.0, 0.0)])
		self.__Put(self.crossX, x, y, 1.0, ac, 0.0, sx=sc, sy=1.0)
		self.__Put(self.crossY, x, y, 1.0, ac, 90.0, sx=sc, sy=1.0)
		# --- kose parantezli dis halka: olcek .7 -> 1.14, donme -55 -> +35, alfa 0 -> 1 (%45) -> 0
		br = strong and self.bracketHot or self.bracket
		(self.bracketHot if not strong else self.bracket).Hide()
		self.__Put(br, x, y, _k(p, [(0.0, 0.7), (1.0, 1.14)]), _k(p, [(0.0, 0.0), (0.45, 1.0), (1.0, 0.0)]),
				   _k(p, [(0.0, -55.0), (1.0, 35.0)]))
		# --- halka (+parlamasi): olcek .2 -> 1.1 (%38) -> .82, donme -20 -> 4, alfa 0 -> 1 (%38) -> 0
		rsc = _k(p, [(0.0, 0.2), (0.38, 1.1), (1.0, 0.82)])
		ral = _k(p, [(0.0, 0.0), (0.38, 1.0), (1.0, 0.0)])
		rro = _k(p, [(0.0, -20.0), (0.38, 4.0), (1.0, 4.0)])
		gl = strong and self.ringGlowHot or self.ringGlow
		(self.ringGlowHot if not strong else self.ringGlow).Hide()
		rg = strong and self.ringHot or self.ring
		(self.ringHot if not strong else self.ring).Hide()
		self.__Put(gl, x, y, rsc, ral, rro)
		self.__Put(rg, x, y, rsc, ral, rro)
		# --- kivilcimlar: her biri merkezden 8 -> 57 px uzaga ucar, boy .3 -> .75, alfa 0 -> 1 (%30) -> 0
		n = strong and 10 or 7
		q = _spark_ease(p)
		dist = (8.0 + 49.0 * q) * self.k
		sy = 0.3 + 0.45 * q
		sa = _k(p, [(0.0, 0.0), (0.3, 1.0), (1.0, 0.0)])
		for i in xrange(self.RAYS):
			w = self.rays[i]
			if i >= n:
				w.Hide()
				continue
			ang = i * (360.0 / n)
			rad = math.radians(ang)
			self.__Put(w, x + math.sin(rad) * dist, y - math.cos(rad) * dist, 1.0, sa, ang, sx=1.0, sy=sy)
		# --- cekirdek: olcek 3 -> 1 (%25) -> .2, alfa 0 -> 1 (%25) -> 0
		self.__Put(self.core, x, y, _k(p, [(0.0, 3.0), (0.25, 1.0), (1.0, 0.2)]),
				   _k(p, [(0.0, 0.0), (0.25, 1.0), (1.0, 0.0)]))
		# --- HEDEF yazisi (yalniz hedef): 105 px altinda, -8 -> +7 px, alfa 0 -> 1 (%35) -> 0
		if strong:
			pl = min(1.0, el / DUR_LABEL)
			self.label.SetPosition(int(x), int(y + (105 + _k(pl, [(0.0, -8.0), (1.0, 7.0)])) * self.k))
			al = _k(pl, [(0.0, 0.0), (0.35, 1.0), (1.0, 0.0)]) * self.fade
			# TextLine'da SetAlpha yok: alfa paketli renk ustunden (0xAARRGGBB)
			self.label.SetPackedFontColor((int(max(0.0, min(1.0, al)) * 255) << 24) | (C_LABEL & 0xffffff))
			if not self.label.IsShow():
				self.label.Show()


class TapFx(ui.Window):
	def __init__(self):
		ui.Window.__init__(self, "TOP_MOST")
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(self.hWnd, 1.0)
		self.SetWindowName("MobileTapFx")
		self.AddFlag("not_pick")
		self.SetSize(1, 1)
		self.SetPosition(0, 0)
		H = float(wndMgr.GetScreenHeight())
		W = float(wndMgr.GetScreenWidth())
		# tasarim 705 px yuksek ekran; dokunma efekti telefonda ~90 px gorunecek (min(H/705, W/1280))
		self.k = max(0.7, min(H / 705.0, W / 1280.0)) * SIZE
		self.pool = []
		self.next = 0
		self.enabled = True
		self.wasDown = False
		try:
			for i in xrange(POOL):
				self.pool.append(_Fx(self, self.k))
		except:
			import dbg, traceback
			dbg.TraceError("TapFx kurulamadi: " + traceback.format_exc())
			self.pool = []
		self.Show()
		try:
			wndMgr.SetTapHandler(self)
		except:
			pass

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		try:
			wndMgr.SetTapHandler(None)
		except:
			pass
		for f in self.pool:
			f.Stop()
			f.keep = []
		self.pool = []
		self.Hide()		# isinlanmada eski efekt kok penceresi bellekte kalirsa cizmesin

	def SetEnabled(self, flag):
		self.enabled = flag

	# native: her sol tus basisi (mantiksal koordinat)
	def OnTapDown(self, x, y):
		if not self.enabled or not self.pool:
			return
		strong = False
		try:
			vid = chrmgr.GetPickedVID()
			if vid > 0 and not player.IsMainCharacterIndex(vid):
				# KULLANICI (2026-09-24): "npc'ye tiklayinca bu geri bildirim gozukmesin" - NPC dokunusunda efekt yok
				# (NPC diyalogu zaten acilir). Mob/metin/oyuncu dokunusu altin "HEDEF" surumu.
				if chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC:
					return
				strong = True
		except:
			strong = False
		t = app.GetTime()
		for f in self.pool:
			f.Cut(t, FADE_NEW)		# eski iz kalmasin
		f = self.pool[self.next]
		self.next = (self.next + 1) % len(self.pool)
		f.Start(x, y, strong, t)
		self.wasDown = True

	def OnUpdate(self):
		t = app.GetTime()
		down = wndMgr.IsLeftButtonDown()
		if self.wasDown and not down:
			# parmak kalkti: efekt hemen soner
			self.wasDown = False
			for f in self.pool:
				f.Cut(t, FADE_UP)
		for f in self.pool:
			if f.IsActive():
				f.Update(t)
