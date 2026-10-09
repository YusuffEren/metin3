# -*- coding: latin-1 -*-
# MOBIL: EXP kureleri - SIVI DOLUM (KULLANICI 2026-10-03).
#   Tasarim: Desktop/Metin2-EXP-Kutulari/exp-kutulari.html (kullanicinin yeni kure tasarimi) + sivi prototipi
#   exp-kutulari-sivi.html ("kutularin sivi gibi dolmasini istiyorum" -> "uygula / oyuna / devam et bitir").
#   Prototipteki sayilar AYNEN: SIN_A, AMP_*, K1/K2, W1/W2, SLOSH_*, akinti/sicrama/kabarcik kurallari.
#
# KULLANICI: "oyunu agirlastirmasin, daha sonra donmaya sebep olmasin":
#   - butun pencereler BIR KEZ kurulur (havuz); karede pencere/nesne YARATILMAZ
#   - yalniz DOLMAKTA olan kure canli (24 yuz + 12 govde seridi); dolu/bos kure hic islem yapmaz
#   - yuzey sakinken ~20 Hz, dolarken ~30 Hz; cam nefesi 15 Hz; degismeyen degerde motor cagrisi YOK (_W onbellegi)
#
# Cizim (motor kisitlari):
#   - Daire kirpmasi yok -> kenar.png (taban'in r 28..31.5 halkasi) sivinin daire disina tasan her seyini ORTER.
#   - Sivi govdesi (govde.png) ve yuzey elipsi (yuz.png) dikey SERITLERE kirpilir: CGraphicExpandedImageInstance
#     m_RenderingRect TAM SAYI doku px'i (LONG) -> kesimler doku px'inde hesaplanip +0.5 ile gonderilir.
#   - Govde serit ust kenari yuz bandinin ICINDE kalir (yuz opak, ustunu orter) -> az serit yeter.
#   - Kayan kucuk parcalar (kabarcik, damla, akinti, isik...) donme yoluyla ALT-PIKSEL (SetRotation != 0:
#     merkez = konum + koken; minimap yaylariyla ayni). Donme yolu kirpmayi yok sayar -> o parcalar kirpilmaz.
#   - nefes / flas SCREEN kipi (INVDESTCOLOR+ONE, alfa yok sayilir): dokular on-carpimli, solma (a,a,a,a).
# Dokular + olculer: tools/exp_kure/bake_exp_kure.py -> mobile/ui/expkure/*.png + expkuregeom.py.
# Birim = tasarim CSS px (kure 64, dolgu 56); oyunda 1 birim = k mantiksal px (k = ekran yuksekligi / 705).
import math
import ui
import wndMgr
import expkuregeom as G

DIR = "mobile/ui/expkure/"
HAS_RRS = hasattr(wndMgr, "SetRenderingRectScaled")
MODE_SCREEN = getattr(wndMgr, "RENDERING_MODE_SCREEN", 1)

_sin = math.sin
_cos = math.cos
_sqrt = math.sqrt
_exp = math.exp
_atan = math.atan
_floor = math.floor
DEG = 180.0 / math.pi
PI2 = 2.0 * math.pi
PHASE_WRAP = 40.0 * math.pi		# p1*0.45 ve p2*0.7 de tam tur -> faz sinirli kalir, desen kopmaz

# ---- prototip (exp-kutulari-sivi.html) ile AYNI ----
D = 56.0
R = 28.0
SIN_A = 0.16
AMP_IDLE = 0.9
AMP_POUR = 2.8
K1 = PI2 / (0.95 * D)
K2 = PI2 / (0.42 * D)
W1 = PI2 / 1.9
W2 = PI2 / 1.25
SLOSH_W = PI2 / 0.95
SLOSH_Z = 0.16
GRAV = 140.0
ORB_STEP = 68.0			# kure merkezleri arasi (64 kure + .exp-row gap 4)
FILL_OFF = (G.ORB_C - D) / 2.0	# kure tuvalinde dolgu kutusunun sol-ustu (birim)

# ---- hiz ayarlari (KULLANICI: agirlastirmasin) ----
NF = 36				# yuz seridi (uclarda sik: yuzey elipsi prototipteki gibi sivri biter)
NB = 18				# govde seridi (her biri 2 yuz seridi)
COL_BETA = 0.55			# serit dagilimi: 0 = esit, 1 = tam sinus (uclar sik, orta seyrek)
TICK_IDLE = 0.048		# ~20 Hz sakin yuzey
TICK_LIVE = 0.030		# ~30 Hz dolum/calkalanma (30 FPS'te her kare)
TICK_BREATH = 1.0 / 15.0
N_BUB = 10
N_DROP = 8
N_RING = 4
N_POP = 6
ROT_EPS = 0.001			# donme yolu (alt-piksel konum); gorunur donme degil
FLASH_TINT = (1.0, 0.78, 0.22)	# seviye parlamasi: tasarim brightness(1.45) altini sarartir, beyazlatmaz


def _clamp(v, a, b):
	if v < a:
		return a
	if v > b:
		return b
	return v


def _topY(x):
	return R - _sqrt(max(0.0, R * R - (x - R) * (x - R)))


def _botY(x):
	return R + _sqrt(max(0.0, R * R - (x - R) * (x - R)))


def _cols():
	"""kiris uzerinde serit sinirlari (-1..1): g(s) = (1-b)s + b sin(pi s / 2) -> uclarda dar, ortada genis."""
	out = []
	for j in xrange(NF + 1):
		u = -1.0 + 2.0 * j / NF
		out.append((1.0 - COL_BETA) * u + COL_BETA * math.sin(math.pi * u / 2.0))
	return out

COLS = _cols()
COLM = [(COLS[j] + COLS[j + 1]) / 2.0 for j in xrange(NF)]


def _bez(x1, y1, x2, y2):
	"""CSS cubic-bezier zamanlama egrisi."""
	ax = 1.0 + 3.0 * x1 - 3.0 * x2
	bx = 3.0 * x2 - 6.0 * x1
	cx = 3.0 * x1
	ay = 1.0 + 3.0 * y1 - 3.0 * y2
	by = 3.0 * y2 - 6.0 * y1
	cy = 3.0 * y1

	def f(x):
		if x <= 0.0:
			return 0.0
		if x >= 1.0:
			return 1.0
		t = x
		for _i in xrange(8):
			xt = ((ax * t + bx) * t + cx) * t - x
			d = (3.0 * ax * t + 2.0 * bx) * t + cx
			if abs(xt) < 1e-5 or abs(d) < 1e-6:
				break
			t -= xt / d
		t = _clamp(t, 0.0, 1.0)
		return ((ay * t + by) * t + cy) * t
	return f

EASE_OUT = _bez(0.0, 0.0, 0.58, 1.0)
EASE_IN_OUT = _bez(0.42, 0.0, 0.58, 1.0)


def _key(p, at, peak):
	"""CSS anahtar kare: 0% 0 -> at% peak -> 100% 0, her aralik ease-out."""
	if p <= 0.0 or p >= 1.0:
		return 0.0
	if p < at:
		return peak * EASE_OUT(p / at)
	return peak * (1.0 - EASE_OUT((p - at) / (1.0 - at)))


def _trap(p, a, b):
	"""prototip hiz yamugu: kisa ivme, sabit akis, yumusak durus."""
	if p <= 0.0:
		return 0.0
	if p >= 1.0:
		return 1.0
	k = 1.0 / (1.0 - (a + b) / 2.0)
	if p < a:
		return k * p * p / (2.0 * a)
	if p <= 1.0 - b:
		return k * (a / 2.0 + (p - a))
	q = 1.0 - p
	return k * (a / 2.0 + (1.0 - a - b) + b / 2.0 - q * q / (2.0 * b))


class _Rnd(object):
	"""kucuk LCG (random modulune bagimli olmayalim)."""

	def __init__(self, seed):
		self.s = int(seed) & 0x7fffffff

	def __call__(self, a, b):
		self.s = (self.s * 1103515245 + 12345) & 0x7fffffff
		return a + (b - a) * (self.s / 2147483648.0)


# sprite meta: canvas merkezinin capaya uzakligi (birim) + birim/doku px
def _SprMeta():
	m = {}
	for (name, (x0, y0, w, h, anchor, tex)) in G.SPR.items():
		m[name] = (x0 + w / 2.0 - anchor[0], y0 + h / 2.0 - anchor[1], w / float(tex[0]), h / float(tex[1]), tex)
	return m

SPR = _SprMeta()


class _W(object):
	"""tek ExpandedImageBox + son yazilan degerler (ayni deger tekrar motora gitmez)."""
	__slots__ = ("w", "h", "tw", "th", "x", "y", "sx", "sy", "rr", "dc", "rot", "ox", "oy", "on", "scr")

	def __init__(self, parent, name, tw, th, screen=False):
		w = ui.ExpandedImageBox()
		w.SetParent(parent)
		w.AddFlag("not_pick")
		w.LoadImage(DIR + name + ".png")
		max(0, 0)	# LoadImage bekleyen hatasini burada tetikle
		if HAS_RRS:
			wndMgr.SetRenderingRectScaled(w.hWnd, 1)
		if screen:
			w.SetRenderingMode(MODE_SCREEN)
		w.Hide()
		self.w = w
		self.h = w.hWnd
		self.tw = float(tw)
		self.th = float(th)
		self.x = None
		self.y = None
		self.sx = None
		self.sy = None
		self.rr = (0, 0, 0, 0)
		self.dc = 255
		self.rot = 0.0
		self.ox = None
		self.oy = None
		self.on = False
		self.scr = screen

	def show(self, on):
		if on != self.on:
			self.on = on
			if on:
				wndMgr.Show(self.h)
			else:
				wndMgr.Hide(self.h)

	def place(self, x, y, sx, sy=None):
		"""donmesiz yol (kirpma calisir): sol-ust TAM SAYI mantiksal px, olcek (mantiksal px / doku px)."""
		if sy is None:
			sy = sx
		if self.rot != 0.0:
			self.rot = 0.0
			wndMgr.SetRotation(self.h, 0.0)
		if x != self.x or y != self.y:
			self.x = x
			self.y = y
			wndMgr.SetWindowPosition(self.h, x, y)
		if sx != self.sx or sy != self.sy:
			self.sx = sx
			self.sy = sy
			wndMgr.SetScale(self.h, sx, sy)

	def center(self, cx, cy, sx, sy, rot):
		"""donme yolu (alt-piksel): goruntu merkezi = konum + koken. Kirpma yok sayilir."""
		fx = int(_floor(cx))
		fy = int(_floor(cy))
		if fx != self.x or fy != self.y:
			self.x = fx
			self.y = fy
			wndMgr.SetWindowPosition(self.h, fx, fy)
		ox = cx - fx
		oy = cy - fy
		if ox != self.ox or oy != self.oy:
			self.ox = ox
			self.oy = oy
			wndMgr.SetOrigin(self.h, ox, oy)
		if sx != self.sx or sy != self.sy:
			self.sx = sx
			self.sy = sy
			wndMgr.SetScale(self.h, sx, sy)
		if rot == 0.0:
			rot = ROT_EPS
		if rot != self.rot:
			self.rot = rot
			wndMgr.SetRotation(self.h, rot)

	def crop(self, l, t, r, b):
		"""kesilen doku px'i (sol, ust, sag, alt; tam sayi). +0.5: motor LONG'a keserken bir eksik vermesin."""
		key = (l, t, r, b)
		if key != self.rr:
			self.rr = key
			wndMgr.SetRenderingRect(self.h, -(l + 0.5) / self.tw, -(t + 0.5) / self.th, -(r + 0.5) / self.tw, -(b + 0.5) / self.th)

	def alpha(self, a, tint=None):
		q = int(_clamp(a, 0.0, 1.0) * 255.0 + 0.5)
		if q != self.dc:
			self.dc = q
			f = q / 255.0
			if self.scr:
				if tint:
					wndMgr.SetDiffuseColor(self.h, f * tint[0], f * tint[1], f * tint[2], f)
				else:
					wndMgr.SetDiffuseColor(self.h, f, f, f, f)	# on-carpimli SCREEN
			else:
				wndMgr.SetDiffuseColor(self.h, 1.0, 1.0, 1.0, f)


class ExpKureler(object):
	"""4 EXP kuresi. F = 0..4 (her kure 1); kureler sirayla dolar/bosalir (prototipteki F modeli)."""

	def __init__(self, parent, k, rowCX, rowCY):
		self.k = k = float(k)
		self.rnd = _Rnd(int(rowCX * 131 + rowCY * 17) + 4242)
		self.oy = 0
		self.aAll = 1.0
		(otw, oth) = G.ORB_TEX
		self.sc = G.ORB_C * k / float(otw)		# kure tuvali: mantiksal px / doku px
		self.tpu = otw / G.ORB_C			# kure tuvali: doku px / birim
		self.half = G.ORB_C / 2.0 * k
		self.home = []
		for i in xrange(4):
			cx = rowCX + (i - 1.5) * ORB_STEP * k
			self.home.append((int(round(cx - self.half)), int(round(rowCY - self.half))))
		P = parent
		OT = G.ORB_TEX
		FT = G.YUZ_TEX
		GT = G.PARILTI_TEX
		LT = G.LVPARILTI_TEX
		# ---- pencereler: kurulus sirasi = cizim sirasi ----
		self.base = [_W(P, "taban", OT[0], OT[1]) for i in xrange(4)]
		self.full = [_W(P, "govde", OT[0], OT[1]) for i in xrange(4)]
		self.glowTop = self.__Spr(P, "ustparilti")
		self.sides = [_W(P, "govde", OT[0], OT[1]) for i in xrange(2)]
		self.bcol = [_W(P, "govde", OT[0], OT[1]) for i in xrange(NB)]
		self.bubPool = [self.__Spr(P, "kabarcik") for i in xrange(N_BUB)]
		self.faceGlow = self.__Spr(P, "yuzparilti")
		self.face = [_W(P, "yuz", FT[0], FT[1]) for i in xrange(NF)]
		self.glint = self.__Spr(P, "isik")
		self.ringPool = [self.__Spr(P, "halka") for i in xrange(N_RING)]
		self.stream = self.__Spr(P, "akinti")
		self.foam = self.__Spr(P, "kopuk")
		self.dropPool = [self.__Spr(P, "damla") for i in xrange(N_DROP)]
		self.popPool = [self.__Spr(P, "patla") for i in xrange(N_POP)]
		self.rim = [_W(P, "kenar", OT[0], OT[1]) for i in xrange(4)]
		self.hi = [_W(P, "cam", OT[0], OT[1]) for i in xrange(4)]
		self.glow = [_W(P, "parilti", GT[0], GT[1]) for i in xrange(4)]
		self.lvglow = [_W(P, "lvparilti", LT[0], LT[1]) for i in xrange(4)]
		self.flash = [_W(P, "flas", OT[0], OT[1], True) for i in xrange(4)]
		self.breath = [_W(P, "nefes", OT[0], OT[1], True) for i in xrange(4)]
		self.liquidW = [self.glowTop, self.faceGlow, self.glint, self.stream, self.foam] + self.sides + self.bcol + self.face
		# ---- durum ----
		self.F = 0.0
		self.target = -1.0
		self.started = False
		self.aFrom = 0.0
		self.aTo = 0.0
		self.aT0 = 0.0
		self.aDur = 0.0
		self.aA = 0.12
		self.aB = 0.26
		self.seq = []
		self.waitT = -1.0
		self.lv = [0.0] * 4
		self.st = ["e"] * 4		# e bos / f dolu / a dolmakta
		self.act = -1
		self.kick = [None] * 4
		self.kickS = [1.0] * 4
		self.kickOn = False
		self.amp = AMP_IDLE
		self.th = 0.0
		self.thv = 0.0
		self.side = -1.0
		self.p1 = self.rnd(0.0, 6.3)
		self.p2 = self.rnd(0.0, 6.3)
		self.wasFill = False
		self.strm = None			# [on, kuyruk, on hiz, kuyruk hizi, genislik, bitiyor]
		self.bubbles = []
		self.drops = []
		self.rings = []
		self.pops = []
		self.ringT = 0.0
		self.dropT = 0.0
		self.bubT = 0.0
		self.idleT = [self.rnd(0.4, 2.0) for i in xrange(4)]
		self.fars = [0.0] * NF
		self.nears = [0.0] * NF
		self.fmap = None
		self.geo = None			# aktif kurenin bu tikteki yuzeyi: (a, L, rc, A, tilt, fx0, fy0)
		self.tTick = -1.0
		self.tBreath = -1.0
		self.tKick = -1.0
		self.dirty = True
		self.force = False
		for i in xrange(4):
			self.__PlaceOrb(i)
			self.base[i].show(True)
			self.rim[i].show(True)
			self.hi[i].show(True)

	def __Spr(self, parent, name):
		tex = SPR[name][4]
		return _W(parent, name, tex[0], tex[1])

	# ------------------------------------------------------------------ dis API
	def SetTarget(self, Ft, t, instant=False, levelUp=False):
		"""Ft = 4 * EXP / gereken. Ilk cagri aninda; seviye atlayinca: dolar -> parlar -> bosalir -> yeni deger."""
		Ft = _clamp(float(Ft), 0.0, 4.0)
		if instant or not self.started:
			self.started = True
			self.target = Ft
			self.seq = []
			self.waitT = -1.0
			self.aFrom = Ft
			self.aTo = Ft
			self.aDur = 0.0
			self.aT0 = t
			self.F = Ft
			self.dirty = True
			return
		if levelUp:
			self.target = Ft
			self.seq = [("to", 4.0), ("lv", 0.7), ("to", 0.0), ("to", Ft)]
			self.waitT = -1.0
			self.__Step(t)
			self.dirty = True
			return
		if abs(Ft - self.target) < 1e-9:
			return			# ayni deger (RefreshStatus her puan degisiminde cagirir) -> dolumu bozma
		self.target = Ft
		if self.seq:
			self.seq[-1] = ("to", Ft)	# seviye atlama suruyor: yalniz son hedef
			return
		self.__AnimTo(Ft, t)
		self.force = True

	def SetEnter(self, dy, alpha):
		"""HUD giris animasyonu (asagidan kayma + belirme)."""
		oy = int(round(dy))
		if oy != self.oy or alpha != self.aAll:
			self.oy = oy
			self.aAll = alpha
			for i in xrange(4):
				self.__PlaceOrb(i)
			if self.act >= 0:
				self.__ActivePlace(self.act)
			self.dirty = True
			self.tBreath = -1.0

	def Destroy(self):
		for lst in (self.base, self.full, self.sides, self.bcol, self.bubPool, self.face, self.ringPool, self.dropPool,
				self.popPool, self.rim, self.hi, self.glow, self.lvglow, self.flash, self.breath):
			for w in lst:
				w.show(False)
		for w in (self.glowTop, self.faceGlow, self.glint, self.stream, self.foam):
			w.show(False)
		self.base = self.full = self.sides = self.bcol = self.bubPool = self.face = []
		self.ringPool = self.dropPool = self.popPool = self.rim = self.hi = []
		self.glow = self.lvglow = self.flash = self.breath = self.liquidW = []
		self.glowTop = self.faceGlow = self.glint = self.stream = self.foam = None
		self.bubbles = []
		self.drops = []
		self.rings = []
		self.pops = []

	# ------------------------------------------------------------------ F animasyonu
	def __Fat(self, t):
		if self.aDur <= 0.0:
			return self.aTo
		if t <= self.aT0:
			return self.aFrom
		p = (t - self.aT0) / self.aDur
		if p >= 1.0:
			return self.aTo
		return self.aFrom + (self.aTo - self.aFrom) * _trap(p, self.aA, self.aB)

	def __AnimTo(self, target, t):
		cur = _clamp(self.__Fat(t), 0.0, 4.0)
		dF = target - cur
		self.aFrom = cur
		self.aTo = target
		self.aT0 = t
		if abs(dF) < 1e-6:
			self.aDur = 0.0
			return
		if dF > 0.0:
			self.aDur = _clamp(0.55 + 0.9 * dF, 0.55, 3.2)
			self.aA = 0.12
			self.aB = 0.26
			self.aT0 = t + 0.1		# akinti once iner (prototip)
		else:
			self.aDur = _clamp(0.4 + 0.45 * -dF, 0.4, 1.8)
			self.aA = 0.22
			self.aB = 0.3

	def __Step(self, t):
		while self.seq:
			(kind, v) = self.seq.pop(0)
			if kind == "to":
				self.__AnimTo(v, t)
				if self.aDur > 0.0:
					return
			else:		# "lv": hepsi parlar, bekle
				for i in xrange(4):
					self.__Kick(i, "l", t)
				self.waitT = t + v
				return

	# ------------------------------------------------------------------ kare
	def Update(self, t):
		if self.tTick < 0.0:
			self.tTick = t - 1.0
		inProg = t < self.aT0 + self.aDur
		live = (inProg or self.seq or self.waitT >= 0.0 or self.strm is not None or self.drops or self.rings or self.pops
			or self.amp > AMP_IDLE + 0.03 or abs(self.th) > 0.003 or abs(self.thv) > 0.02)
		dt = t - self.tTick
		if self.dirty or self.force or dt >= (TICK_LIVE if live else TICK_IDLE):
			self.tTick = t
			self.force = False
			self.__Tick(t, _clamp(dt, 0.0, 0.1))
		if self.kickOn and t - self.tKick >= TICK_LIVE:
			self.tKick = t
			self.__Kicks(t)
		if t - self.tBreath >= TICK_BREATH:
			self.tBreath = t
			self.__Breath(t)

	def __Tick(self, t, dt):
		F = _clamp(self.__Fat(t), 0.0, 4.0)
		vF = (F - self.F) / dt if dt > 1e-4 else 0.0
		self.F = F
		inProg = t < self.aT0 + self.aDur
		if self.waitT >= 0.0:
			if t >= self.waitT:
				self.waitT = -1.0
				self.__Step(t)
		elif not inProg and self.seq:
			self.__Step(t)
		inProg = t < self.aT0 + self.aDur
		pouring = inProg and self.aTo > self.aFrom
		draining = inProg and self.aTo < self.aFrom
		pourIdx = min(3, int(F + 1e-9)) if (pouring and F < 4.0) else -1	# F 4'e 1e-9 yakinken 4 olmasin (denetim)
		dirty = self.dirty
		a = -1
		for i in xrange(4):
			lv = _clamp(F - i, 0.0, 1.0)
			self.lv[i] = lv
			s = "e" if lv <= 0.0005 else ("f" if lv >= 0.9995 else "a")
			old = self.st[i]
			if s != old or dirty:
				self.st[i] = s
				self.full[i].show(s == "f")
				if s == "f":
					self.__PlaceOrb(i)
					if old != "f" and vF > 0.0 and not dirty:
						self.__Kick(i, "p", t)		# dolunca parlama (tasarim .pulse)
				if s == "e":
					self.__DropOrbParticles(i)
			if s == "a":
				a = i
		if a < 0 and 0 <= pourIdx < 4 and self.st[pourIdx] == "e":
			a = pourIdx			# bos kureye dokulmeye baslandi: akinti once iner
		if a != self.act:
			self.__Activate(a)
		if a >= 0:
			self.__Liquid(a, t, dt, vF, a == pourIdx, draining)
		self.__IdleBubbles(dt)
		self.__Particles(dt)
		self.dirty = False

	# ------------------------------------------------------------------ kure katmanlari
	def __PlaceOrb(self, i):
		(hx, hy) = self.home[i]
		hy += self.oy
		s = self.kickS[i]
		lay = [self.base[i], self.rim[i], self.hi[i], self.full[i]]
		if s == 1.0:
			for w in lay:
				w.place(hx, hy, self.sc)
		else:
			cx = hx + self.half
			cy = hy + self.half
			sc = self.sc * s
			for w in lay:
				w.center(cx, cy, sc, sc, 0.0)
		a = self.aAll
		for w in lay:
			w.alpha(a)

	def __Kick(self, i, kind, t):
		cur = self.kick[i]
		# seviye atlama tepkisi oncelikli (prototipte .orb.lvup kurali .pulse'u ezer): dolum nabzi onu bozmasin
		if kind == "p" and cur is not None and cur[0] == "l":
			return
		if cur is not None and cur[0] != kind:
			(self.glow[i] if cur[0] == "p" else self.lvglow[i]).show(False)
		self.kick[i] = (kind, t)
		self.kickOn = True
		self.tKick = -1.0

	def __Kicks(self, t):
		on = False
		for i in xrange(4):
			kk = self.kick[i]
			if kk is None:
				continue
			(kind, t0) = kk
			el = t - t0
			if kind == "p":		# .orb.pulse: orbKick .38 s (50% 1.045) + goldGlow .55 s (50%)
				ps = el / 0.38
				s = 1.0 + _key(ps, 0.5, 0.045)
				pg = el / 0.55
				g = _key(pg, 0.5, 1.0)
				gw = self.glow[i]
				fl = 0.0
			else:			# seviye atlama: lvKick .7 s (30% 1.08) + lvGlow .7 s (30%, parlaklik 1.45)
				ps = el / 0.7
				s = 1.0 + _key(ps, 0.3, 0.08)
				pg = ps
				g = _key(pg, 0.3, 1.0)
				gw = self.lvglow[i]
				fl = 0.45 * g
			(hx, hy) = self.home[i]
			cx = hx + self.half
			cy = hy + self.oy + self.half
			if ps >= 1.0 and pg >= 1.0:
				self.kick[i] = None
				self.kickS[i] = 1.0
				self.__PlaceOrb(i)
				self.glow[i].show(False)
				self.lvglow[i].show(False)
				self.flash[i].show(False)
				continue
			on = True
			self.kickS[i] = s
			self.__PlaceOrb(i)
			gs = (G.PARILTI_C if gw is self.glow[i] else G.LVPARILTI_C) * self.k / gw.tw * s
			gw.center(cx, cy, gs, gs, 0.0)
			gw.alpha(g * self.aAll)
			gw.show(g > 0.004)
			f = self.flash[i]
			if fl > 0.004:
				f.center(cx, cy, self.sc * s, self.sc * s, 0.0)
				f.alpha(fl * self.aAll, FLASH_TINT)
				f.show(True)
			else:
				f.show(False)
		self.kickOn = on

	def __Breath(self, t):
		"""tasarim .orb::after glassBreath 2.4 s ease-in-out alternate: opaklik .28->.62, olcek .97->1.015 (SCREEN)."""
		q = (t / 2.4) % 2.0
		if q > 1.0:
			q = 2.0 - q
		v = EASE_IN_OUT(q)
		o = (0.28 + 0.34 * v) * self.aAll
		s = 0.97 + 0.045 * v
		for i in xrange(4):
			(hx, hy) = self.home[i]
			b = self.breath[i]
			sc = self.sc * s * self.kickS[i]
			b.center(hx + self.half, hy + self.oy + self.half, sc, sc, 0.0)
			b.alpha(o)
			b.show(True)

	# ------------------------------------------------------------------ sivi (yalniz aktif kure)
	def __Activate(self, a):
		for w in self.liquidW:
			w.show(False)
		for r in self.rings:
			r[2].show(False)
			self.ringPool.append(r[2])
		self.rings = []
		for d in self.drops:
			d[7].show(False)
			self.dropPool.append(d[7])
		self.drops = []
		for p in self.pops:
			p[4].show(False)
			self.popPool.append(p[4])
		self.pops = []
		self.strm = None
		self.fmap = None
		self.geo = None
		self.amp = AMP_IDLE
		self.th = 0.0
		self.thv = 0.0
		self.wasFill = False
		self.act = a
		if a >= 0:
			self.__ActivePlace(a)

	def __ActivePlace(self, a):
		(hx, hy) = self.home[a]
		hy += self.oy
		for w in self.sides:
			w.place(hx, hy, self.sc)
		for w in self.bcol:
			w.place(hx, hy, self.sc)
		self.fmap = None

	def __Surf(self, x):
		"""aktif kurenin (arka kenar, on kenar) y'si - prototip far()/near()."""
		(a, L, rc, A, tilt, fx0, fy0) = self.geo
		if rc > 0.0:
			u = (x - R) / rc
			hh = _sqrt(max(0.0, 1.0 - u * u))
		else:
			hh = 0.0
		wf = A * (0.62 * _sin(K1 * x - self.p1) + 0.38 * _sin(K2 * x + self.p2 + 1.3))
		wn = A * (0.62 * _sin(K1 * x - self.p1 + 1.1) + 0.38 * _sin(K2 * x + self.p2 + 3.4))
		mean = L + tilt * (x - R)
		e = SIN_A * rc * hh
		fa = mean - wf - e
		ne = mean - (wf + (wn - wf) * hh * 0.6) + e
		if ne < fa + 0.05:
			ne = fa + 0.05
		return (fa, ne)

	def __Liquid(self, a, t, dt, vF, filling, draining):
		k = self.k
		level = self.lv[a]
		drainHere = draining and 0.0 < level < 1.0
		rate = max(abs(vF), 0.25) if filling else abs(vF)
		# calkanti genligi: dokulurken hizla artar, sonra yavasca durulur
		target = AMP_IDLE + ((AMP_POUR * min(1.0, rate / 0.45)) if (filling or drainHere) else 0.0)
		tau = 0.12 if target > self.amp else 1.1
		self.amp += (target - self.amp) * (1.0 - _exp(-dt / tau))
		# calkalanma: sonumlu yay (yuzey saga sola yatar)
		if filling and not self.wasFill:
			self.side = -self.side
			self.thv += self.side * 0.30
		if (not filling) and self.wasFill:
			self.thv -= (1.0 if self.th >= 0.0 else -1.0) * 0.16
		self.wasFill = filling
		if filling:
			self.thv += (self.rnd(0.0, 1.0) - 0.5) * 2.2 * dt
		n = int(dt / 0.034) + 1
		h = dt / n
		for _i in xrange(n):
			self.thv += (-SLOSH_W * SLOSH_W * self.th - 2.0 * SLOSH_Z * SLOSH_W * self.thv) * h
			self.th += self.thv * h
		self.th = _clamp(self.th, -0.22, 0.22)
		m = 1.0 + 1.3 * (self.amp - AMP_IDLE) / AMP_POUR
		self.p1 = (self.p1 + W1 * dt * m) % PHASE_WRAP
		self.p2 = (self.p2 + W2 * dt * m) % PHASE_WRAP
		# geometri: seviye L (yukaridan), yuzeyin kureyi kestigi kiris yaricapi rc
		L = D * (1.0 - level)
		dy = L - R
		rc = _sqrt(max(0.0, R * R - dy * dy))
		cf = rc / R
		A = self.amp * (cf ** 0.8) if cf > 0.0 else 0.0
		tilt = self.th * cf
		(hx, hy) = self.home[a]
		hy += self.oy
		fx0 = hx + FILL_OFF * k
		fy0 = hy + FILL_OFF * k
		self.geo = (a, L, rc, A, tilt, fx0, fy0)
		hasFace = level > 0.0005 and rc > 0.4
		alpha = self.aAll
		if hasFace:
			self.__Surface(L, rc, A, tilt, fx0, fy0, alpha)
		else:
			for w in self.liquidW:
				if w is not self.stream:
					w.show(False)
		self.__Stream(a, t, dt, rate, filling, level, hasFace, fx0, fy0, alpha)

	def __Surface(self, L, rc, A, tilt, fx0, fy0, alpha):
		k = self.k
		p1 = self.p1
		p2 = self.p2
		fars = self.fars
		nears = self.nears
		xa = R - rc
		e0 = SIN_A * rc
		minFar = 1e9
		maxNear = -1e9
		wsum = 0.0
		for j in xrange(NF):
			u = COLM[j]
			x = R + rc * u
			hh = _sqrt(max(0.0, 1.0 - u * u))
			wf = A * (0.62 * _sin(K1 * x - p1) + 0.38 * _sin(K2 * x + p2 + 1.3))
			wn = A * (0.62 * _sin(K1 * x - p1 + 1.1) + 0.38 * _sin(K2 * x + p2 + 3.4))
			mean = L + tilt * (x - R)
			fa = mean - wf - e0 * hh
			ne = mean - (wf + (wn - wf) * hh * 0.6) + e0 * hh
			if ne < fa + 0.05:
				ne = fa + 0.05
			fars[j] = fa
			nears[j] = ne
			wsum += wf
			if fa < minFar:
				minFar = fa
			if ne > maxNear:
				maxNear = ne
		# yuz gecisi: prototipte objectBoundingBox (kiris x bandin dikey sinirlari). Kucuk oynamada yeniden
		# olceklenmez (cagri az); band esnek payin (+-1.5 ey) disina tasarsa ya da kiris degisirse yeniden.
		Yc = (minFar + maxNear) / 2.0
		ey = max(0.3, (maxNear - minFar) / 2.0)
		fm = self.fmap
		if (fm is None or fm[0] != rc or abs(ey - fm[2]) > 0.12 * fm[2] or abs(Yc - fm[1]) > 0.15 * fm[2]
				or minFar < fm[1] - 1.45 * fm[2] or maxNear > fm[1] + 1.45 * fm[2]):
			fm = self.fmap = (rc, Yc, ey)
		(mrc, mYc, mey) = fm
		(FW, FH) = G.YUZ_TEX
		V = G.YUZ_V
		sxf = 2.0 * mrc * k / FW
		syf = 2.0 * V * mey * k / FH
		iX0 = int(round(fx0 + (R - mrc) * k))
		iY0 = int(round(fy0 + (mYc - V * mey) * k))
		face = self.face
		prev = int(round((fx0 + xa * k - iX0) / sxf))
		if prev < 0:
			prev = 0
		for j in xrange(NF):
			w = face[j]
			tx = int(round((fx0 + (R + rc * COLS[j + 1]) * k - iX0) / sxf))
			if tx > FW:
				tx = FW
			tt = int(round((fy0 + fars[j] * k - iY0) / syf))
			tb = int(round((fy0 + nears[j] * k - iY0) / syf))
			if tt < 0:
				tt = 0
			if tb > FH:
				tb = FH
			if tx > prev and tb > tt:
				w.place(iX0, iY0, sxf, syf)
				w.crop(prev, tt, FW - tx, FH - tb)
				w.alpha(alpha)
				w.show(True)
			else:
				w.show(False)
			prev = tx
		# govde seritleri: ust kenar yuz bandinin icinde (yuz opak, ustunu orter)
		bt = self.tpu
		(BW, BH) = G.ORB_TEX
		bcol = self.bcol
		prev = int(round((FILL_OFF + xa) * bt))
		for b in xrange(NB):
			j0 = 2 * b
			mf = fars[j0] if fars[j0] > fars[j0 + 1] else fars[j0 + 1]
			mn = nears[j0] if nears[j0] < nears[j0 + 1] else nears[j0 + 1]
			yb = mf + 0.6
			if yb > mn:
				yb = mn if mn > mf else mf
			tx = int(round((FILL_OFF + R + rc * COLS[j0 + 2]) * bt))
			ty = int(round((FILL_OFF + yb) * bt))
			w = bcol[b]
			if tx > prev and ty < BH:
				w.crop(prev, ty, BW - tx, 0)
				w.alpha(alpha)
				w.show(True)
			else:
				w.show(False)
			prev = tx
		# yarinin ustunde: kirisin disinda kalan yanlar tamamen sivi
		if L < R:
			txa = int(round((FILL_OFF + xa) * bt))
			txb = int(round((FILL_OFF + R + rc) * bt))
			self.sides[0].crop(0, 0, BW - txa, 0)
			self.sides[1].crop(txb, 0, 0, 0)
			for w in self.sides:
				w.alpha(alpha)
				w.show(True)
		else:
			for w in self.sides:
				w.show(False)
		# yuzey parlamalari (sabit yay sprite'i, ortadaki dalga + egimi izler)
		# DENETIM: merkezdeki dalga turevi uzun yayi uclarda yuzeyden koparip kure disina tasiyordu ->
		# kiris boyunca kesen egimi (+-0.07) ve ortalama dalga yuksekligi; uc noktasi r 31'i gecmesin.
		cf = rc / R
		xb = R + rc
		xl = R - rc
		wr = A * (0.62 * _sin(K1 * xb - p1) + 0.38 * _sin(K2 * xb + p2 + 1.3))
		wl = A * (0.62 * _sin(K1 * xl - p1) + 0.38 * _sin(K2 * xl + p2 + 1.3))
		sl = _clamp(tilt - (wr - wl) / (2.0 * rc), -0.07, 0.07)
		dyc = L - R
		if dyc * sl > 0.0:
			lim = (31.0 * 31.0 - R * R) / (2.0 * abs(dyc) * rc + 1e-6)
			if abs(sl) > lim:
				sl = lim if sl > 0.0 else -lim
		ang = _atan(sl) * DEG
		ax = fx0 + R * k
		ay = fy0 + (L - wsum / NF) * k
		self.__PutSpr(self.glowTop, "ustparilti", ax, ay, cf, cf, ang, alpha)
		self.__PutSpr(self.faceGlow, "yuzparilti", ax, ay, cf, cf, ang, alpha)
		# yuzeyde kayan isik cizgisi
		if rc >= 8.0:
			a = self.geo[0]
			gc = R + rc * 0.5 * _sin(p1 * 0.45 + a * 1.7)
			(f0, n0) = self.__Surf(gc)
			(f1, n1) = self.__Surf(gc - 1.0)
			(f2, n2) = self.__Surf(gc + 1.0)
			gy = f0 + (n0 - f0) * 0.32
			sl = ((f2 + (n2 - f2) * 0.32) - (f1 + (n1 - f1) * 0.32)) / 2.0
			# prototipte isik yuz bandina kirpilir: bant inceldikce (dalga tepesinde) soner, disari tasmaz
			ga = (0.35 + 0.3 * _sin(p2 * 0.7 + a)) * _clamp((n0 - f0 - 1.2) / 2.0, 0.0, 1.0)
			self.__PutSpr(self.glint, "isik", fx0 + gc * k, fy0 + gy * k, 0.42 * rc / 20.0, 1.0, _atan(sl) * DEG, ga * alpha)
		else:
			self.glint.show(False)

	def __PutSpr(self, w, name, ax, ay, sxu, syu, ang, alpha):
		"""sprite'i capasindan yerlestir: (ax, ay) mantiksal px, sxu/syu birim olcegi, ang derece (capa etrafinda)."""
		(ocx, ocy, ux, uy, tex) = SPR[name]
		k = self.k
		ox = ocx * sxu * k
		oy = ocy * syu * k
		if ang != 0.0:
			r = ang / DEG
			c = _cos(r)
			s = _sin(r)
			(ox, oy) = (ox * c - oy * s, ox * s + oy * c)
		w.center(ax + ox, ay + oy, sxu * k * ux, syu * k * uy, ang)
		w.alpha(alpha)
		w.show(alpha > 0.004)

	def __Stream(self, a, t, dt, rate, filling, level, hasFace, fx0, fy0, alpha):
		k = self.k
		sx = R - 2.5 + 1.2 * _sin(t * 1.7 + a)
		if hasFace:
			(fa, ne) = self.__Surf(sx)
			surfY = (fa + ne) / 2.0
		else:
			surfY = D
		st = self.strm
		if filling and level < 0.9995:
			if st is None:
				t0 = _topY(sx) + 0.3
				st = self.strm = [t0, t0, 120.0, 0.0, 0.4, False]
			st[5] = False
		elif st is not None:
			st[5] = True
		hitting = False
		if st is not None:
			t0 = _topY(sx) + 0.3
			if st[0] < surfY:
				st[2] += 1200.0 * dt
				st[0] = min(surfY, st[0] + st[2] * dt)
			else:
				st[0] = surfY
			if st[5]:
				st[3] += 1200.0 * dt
				st[1] += st[3] * dt
			else:
				st[1] = t0
			wT = 0.6 if st[5] else 0.9 + 1.5 * min(1.0, rate / 0.45)
			st[4] += (wT - st[4]) * (1.0 - _exp(-dt / 0.08))
			if st[1] >= st[0] - 0.2:
				self.strm = None
				self.stream.show(False)
			else:
				ln = st[0] - st[1]
				self.__PutSpr(self.stream, "akinti", fx0 + sx * k, fy0 + st[1] * k, st[4] / 2.0, ln / 30.0, 0.0, alpha)
				hitting = (not st[5]) and st[0] >= surfY - 0.5 and hasFace
		else:
			self.stream.show(False)
		# kopuk + halkalar + damlalar + kabarcik (carpma noktasi)
		if hitting:
			fw = 1.6 + st[4] * 1.2
			self.__PutSpr(self.foam, "kopuk", fx0 + sx * k, fy0 + surfY * k, fw / 4.0, fw * 0.42 / 4.0, 0.0,
				(0.75 + 0.25 * _sin(t * 23.0)) * alpha)
			self.ringT -= dt
			if self.ringT <= 0.0:
				self.ringT = 0.15
				if self.ringPool:
					self.rings.append([sx, 0.0, self.ringPool.pop()])
			self.dropT -= dt
			while self.dropT <= 0.0:
				self.dropT += 1.0 / 20.0
				if self.dropPool:
					r = self.rnd(0.4, 0.85)
					w = self.dropPool.pop()
					self.drops.append([sx + self.rnd(-0.8, 0.8), surfY - 0.4, self.rnd(-13.0, 13.0), -self.rnd(9.0, 24.0), r, 0.0, a, w])
			self.bubT -= dt
			while self.bubT <= 0.0:
				self.bubT += 1.0 / 12.0
				self.__SpawnBubble(a, sx + self.rnd(-3.0, 3.0), surfY + self.rnd(3.0, 11.0))
		else:
			self.foam.show(False)

	# ------------------------------------------------------------------ parcaciklar
	def __SpawnBubble(self, i, x, y):
		if not self.bubPool:
			return
		r = self.rnd(0.9, 2.0)
		x = _clamp(x, R - R * 0.8, R + R * 0.8)
		y = min(y, _botY(x) - r - 0.8)
		if self.st[i] != "f":
			if i != self.act or self.geo is None:
				return
			(fa, ne) = self.__Surf(x)
			if y - r <= ne + 0.5:
				return
		if (x - R) * (x - R) + (y - R) * (y - R) > (R - r - 0.8) * (R - r - 0.8):
			return
		w = self.bubPool.pop()
		# [kure, x, y, r, hiz, frekans, faz, salinim, yas, pencere]
		self.bubbles.append([i, x, y, r, self.rnd(9.0, 16.0), self.rnd(5.0, 9.0), self.rnd(0.0, 6.3), self.rnd(2.0, 6.0), 0.0, w])

	def __IdleBubbles(self, dt):
		for i in xrange(4):
			s = self.st[i]
			if s == "e":
				continue
			self.idleT[i] -= dt
			if self.idleT[i] <= 0.0:
				self.idleT[i] = self.rnd(2.5, 5.0) if s == "f" else self.rnd(1.1, 2.8)
				x = R + self.rnd(-0.55, 0.55) * R
				self.__SpawnBubble(i, x, _botY(x) - 2.4)

	def __DropOrbParticles(self, i):
		keep = []
		for b in self.bubbles:
			if b[0] == i:
				b[9].show(False)
				self.bubPool.append(b[9])
			else:
				keep.append(b)
		self.bubbles = keep

	def __Particles(self, dt):
		k = self.k
		alpha = self.aAll
		geo = self.geo
		act = self.act
		# kabarciklar (her kurede; dolu kurede tepeye kadar cikar)
		if self.bubbles:
			keep = []
			for b in self.bubbles:
				i = b[0]
				b[8] += dt
				b[4] = min(b[4] + 6.0 * dt, 24.0)
				b[2] -= b[4] * dt
				b[1] += _sin(b[8] * b[5] + b[6]) * b[7] * dt
				x = b[1]
				y = b[2]
				r = b[3]
				full = self.st[i] == "f"
				if full:
					lim = _topY(x) + 1.2
				elif i == act and geo is not None:
					lim = self.__Surf(x)[1]
				else:
					lim = 1e9
				out = (x - R) * (x - R) + (y - R) * (y - R) > (R - r - 0.6) * (R - r - 0.6)
				if y - r <= lim or out:
					if (not full) and (not out) and i == act and self.popPool:
						self.pops.append([x, y, r, 0.0, self.popPool.pop()])
					b[9].show(False)
					self.bubPool.append(b[9])
					continue
				(hx, hy) = self.home[i]
				s = r / 1.45
				self.__PutSpr(b[9], "kabarcik", hx + (FILL_OFF + x) * k, hy + self.oy + (FILL_OFF + y) * k, s, s, 0.0, alpha)
				keep.append(b)
			self.bubbles = keep
		if act < 0 or geo is None:
			return
		(a, L, rc, A, tilt, fx0, fy0) = geo
		hasFace = 0.0005 < self.lv[a] and rc > 0.4
		# damlalar
		if self.drops:
			keep = []
			for p in self.drops:
				p[5] += dt
				p[3] += GRAV * dt
				p[0] += p[2] * dt
				p[1] += p[3] * dt
				if hasFace:
					(fa, ne) = self.__Surf(p[0])
					land = (fa + ne) / 2.0
				else:
					land = D
				out = (p[0] - R) * (p[0] - R) + (p[1] - R) * (p[1] - R) > 29.5 * 29.5
				if (p[3] > 0.0 and p[1] >= land) or p[5] > 1.5 or p[1] > D or out:
					if hasFace and p[3] > 0.0 and not out and self.popPool:
						self.pops.append([p[0], land, 0.3, 0.0, self.popPool.pop()])
					p[7].show(False)
					self.dropPool.append(p[7])
					continue
				s = p[4] / 0.65
				self.__PutSpr(p[7], "damla", fx0 + p[0] * k, fy0 + p[1] * k, s, s, 0.0, alpha)
				keep.append(p)
			self.drops = keep
		# carpma halkalari (yuzeyde, basik elips)
		if self.rings:
			keep = []
			for r in self.rings:
				r[1] += dt
				if r[1] >= 0.6 or not hasFace:
					r[2].show(False)
					self.ringPool.append(r[2])
					continue
				rx = min(1.0 + r[1] * 18.0, 0.9 * rc)
				(fa, ne) = self.__Surf(r[0])
				s = rx / 10.0
				self.__PutSpr(r[2], "halka", fx0 + r[0] * k, fy0 + (fa + ne) / 2.0 * k, s, s, 0.0, 0.8 * (1.0 - r[1] / 0.6) * alpha)
				keep.append(r)
			self.rings = keep
		# patlama halkalari
		if self.pops:
			keep = []
			for p in self.pops:
				p[3] += dt
				if p[3] >= 0.25:
					p[4].show(False)
					self.popPool.append(p[4])
					continue
				s = (p[2] + p[3] * 7.0) / 4.0
				self.__PutSpr(p[4], "patla", fx0 + p[0] * k, fy0 + p[1] * k, s, s, 0.0, 0.9 * (1.0 - p[3] / 0.25) * alpha)
				keep.append(p)
			self.pops = keep
