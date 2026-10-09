# -*- coding: latin-1 -*-
# MOBIL: Minimap + HP/SP yay HUD'u (KULLANICI 2026-09-26, tasarim Desktop/Metin2-Minimap-HUD/minimap-hud.html):
# "bunu oyuna yerlestirelim birebir. eski hp sp enerjiyi ekrandan kaldirip bu mini mapta olan hp sp yi aktif et".
#
# Parcalar tools/minimap_hud_export.py -> mobile/ui/minimap/ (1x, tasarim 1280x705); geometri mobileminimapgeom.py
# (tasarim px, .hud kutusuna gore). Olcek k: tasarimdaki harita gorunumu (226 px) = gercek mini harita (miniMap.Render,
# 128 px daire) -> native koda dokunmadan birebir oturur.
#
# Cizim sirasi (tasarim z-sirasi): kabuk | (gercek harita: MiniMap.OnRender, cocuklardan ONCE) | tarama | vinyet |
# pusula | ic halka golgesi (:after) | dis kasa + hp izi | hp dolgu | hp parlama | ic kasa + sp izi | sp dolgu |
# penceler/percinler | dugmeler.
# Animasyonlar: hudIn (.85 s: 35,-20 px kayma + belirme), dolum gecisi (.7 s, cubic-bezier(.16,.8,.2,1)),
# arcFlow (parlama kesikleri 2.4 s), dugme basma (scale .96).
# Tum gorseller MiniMap penceresinin COCUGU (gercek haritanin ustunde cizilsin); MiniMap koku not_pick, dugme
# alanlari secilebilir (parmak icin tasarim kutusundan genis).
import math
import ui
import wndMgr
import app
import player
import mobileminimapgeom as G

DIR = "mobile/ui/minimap/"
TEX_S = 1.0			# dokular 1x (tools/minimap_hud_export.py DPR 1) - bkz. "pixel pixel" notu
NOTE_TEX = (426.0, 132.0)		# not_*.png boyutu (GetWidth yuklenmede 0 olabilir -> SABIT)
NOTE_W = 142.0				# notun tasarim genisligi (bake W)
MAP_PX = 128.0			# miniMap.Render daire capi (PythonMiniMap m_fWidth)
_os = __import__("os")
MOBILE_IOS = ("/Containers/Data/Application/" in _os.getcwd())


def Layout():
	"""(x0, y0, k): HUD kutusunun ekran kokeni + tasarim px basina ekran px. Tasarim: right max(3vw,18px), top max(4vh,18px)."""
	W = float(wndMgr.GetScreenWidth())
	H = float(wndMgr.GetScreenHeight())
	k = MAP_PX / float(G.VIEW[2])
	## KULLANICI (2026-09-26): "mini mapi hafif saga yaklastir" (tasarim 3vw -> %1.8)
	right = max(W * 0.018, 14.0) + (14.0 if MOBILE_IOS else 0.0)
	top = max(H * 0.04, 18.0) + (10.0 if MOBILE_IOS else 0.0)
	x0 = int(round(W - right - G.HUD[2] * k))
	y0 = int(round(top))
	return (x0, y0, k)


def MapCenter():
	(x0, y0, k) = Layout()
	return (x0 + (G.VIEW[0] + G.VIEW[2] / 2.0) * k, y0 + (G.VIEW[1] + G.VIEW[3] / 2.0) * k)


def Bottom():
	"""yaylarin alt kenari (ekran px) - tarih satiri bunun altina."""
	(x0, y0, k) = Layout()
	return y0 + (G.arcback1[1] + G.arcback1[3]) * k


def _ease_bar(t):
	# cubic-bezier(.16,.8,.2,1) ~ guclu ease-out
	return 1.0 - (1.0 - t) ** 3


class _Tween:
	def __init__(self, v, dur):
		self.v0 = v
		self.v1 = v
		self.t0 = -1.0
		self.dur = dur

	def Set(self, v, t):
		if abs(v - self.v1) < 1e-6:
			return
		self.v0 = self.Get(t)
		self.v1 = v
		self.t0 = t

	def Get(self, t):
		if self.t0 < 0.0:
			return self.v1
		p = (t - self.t0) / self.dur
		if p >= 1.0:
			self.t0 = -1.0
			return self.v1
		return self.v0 + (self.v1 - self.v0) * _ease_bar(p)


class _Tap(ui.Window):
	def __init__(self, parent, func):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.func = func

	def OnMouseLeftButtonDown(self):
		self.func()
		return True

	def OnMouseLeftButtonUp(self):
		return True


def _hex(c):
	return ((c >> 16) & 255) / 255.0, ((c >> 8) & 255) / 255.0, (c & 255) / 255.0


def _grad(stops, t):
	t = max(0.0, min(1.0, t))
	for i in xrange(1, len(stops)):
		if t <= stops[i][0]:
			(t0, c0) = stops[i - 1]
			(t1, c1) = stops[i]
			q = (t - t0) / max(1e-6, t1 - t0)
			a = _hex(c0)
			b = _hex(c1)
			return (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q, a[2] + (b[2] - a[2]) * q)
	return _hex(stops[-1][1])


class _ArcFill:
	"""HP / SP yay dolgusu KODLA (KULLANICI 2026-09-26: "hp sp pixel pixel, resmi kaldir, kodla renkleri ver").
	Yay boyunca N kisa serit (kesit profili dokusu arcprof_*: beyaz, alfa = cekirdek + isima), her biri teget yonde
	dondurulup ALT-PIKSEL konumla uc uca dizilir; rengi svg'deki capraz gradyan (objectBoundingBox 0,0 -> 1,1)
	seridin konumundan hesaplanip wndMgr.SetDiffuseColor ile verilir. Dolum ucu yuvarlak (arccap_*, linecap round)."""
	N = 56
	## KULLANICI (2026-09-26): "hp ve sp'ye canli guzel bir animasyon" -
	##   akis: dolu yay boyunca bastan uca giden isik dalgasi (FLOW_SEC surede gecer, FLOW_REST bekler; HP/SP farkli faz)
	##   Flash(): deger degisince tum yay kisa parlar (hasar / yenilenme)
	##   low: HP %25 altinda cekirdek nabiz (0.55 s)
	FLOW_SEC = 1.6
	FLOW_REST = 0.9
	FLOW_W = 22.0		# isik dalgasi genisligi (derece)

	def __init__(self, hud, key, stops, phase=0.0, low=False):
		self.hud = hud
		self.key = key
		self.stops = stops
		self.C = getattr(G, key + "_C")
		(self.a0, self.span) = getattr(G, key + "_A")
		self.r = getattr(G, key + "_R")
		self.span_px = getattr(G, key + "_SPAN")
		self.bb = getattr(G, key + "_BB")
		self.seg = []
		for i in xrange(self.N):
			self.seg.append(hud._MakeRaw("arcprof_%s.png" % key.lower()))
		self.cap = hud._MakeRaw("arccap_%s.png" % key.lower())
		# KULLANICI: "hp sp cok solu, canli olsun" -> dis kenara ince parlaklik cizgisi (acik renk, seritlerin ustu)
		self.hi = []
		for i in xrange(self.N):
			self.hi.append(hud._MakeRaw("archi_%s.png" % key.lower()))
		self.col = []
		d = self.span / float(self.N)
		self.colHi = []
		for i in xrange(self.N):
			c = self.__Color(self.a0 + (i + 0.5) * d)
			self.col.append(c)
			self.colHi.append((0.55 + 0.45 * c[0], 0.55 + 0.45 * c[1], 0.55 + 0.45 * c[2]))
		self.lastP = -1.0
		self.lastK = None
		self.phase = phase
		self.low = low
		self.flashT = -1.0
		self.lastPulse = False
		self.mids = [0.0] * self.N
		## HIZ (2026-10-01): her kare 2 yay x 56 serit x (yerlestirme + renk) ~1400 motor cagrisiydi. Serit yalniz
		## parametresi (orta aci, boy) DEGISINCE yeniden yerlesir; renk yalniz 1/255 adimi degisince yazilir.
		## Ekrana giden deger AYNI (1/255 alti fark gorunmez).
		self.place = [None] * self.N
		self.hiQ = [None] * self.N
		self.segQ = [None] * self.N

	def Flash(self, t):
		self.flashT = t

	def __Color(self, deg):
		r = math.radians(deg)
		x = self.C[0] + self.r * math.cos(r)
		y = self.C[1] + self.r * math.sin(r)
		(bx, by, bw, bh) = self.bb
		t = ((x - bx) / bw + (y - by) / bh) / 2.0
		return _grad(self.stops, t)

	def Update(self, pct, t, force=False):
		hud = self.hud
		key = (hud.dx, hud.dy, hud.alpha)
		if not force and abs(pct - self.lastP) < 0.0005 and key == self.lastK:
			self.__Animate(pct, t)
			return
		if key != self.lastK:
			self.place = [None] * self.N
			self.hiQ = [None] * self.N
			self.segQ = [None] * self.N
		self.lastP = pct
		self.lastK = key
		k = hud.k
		d = self.span / float(self.N)
		fill = pct * self.span
		th = self.span_px * k
		for i in xrange(self.N):
			w = self.seg[i]
			h = self.hi[i]
			s0 = i * d
			if s0 >= fill - 1e-6:
				if w.IsShow():
					w.Hide()
				if h.IsShow():
					h.Hide()
				self.place[i] = None
				continue
			s1 = min(fill, s0 + d)
			mid = self.a0 + (s0 + s1) / 2.0
			ln = math.radians(s1 - s0) * self.r * k
			if s1 < fill:
				ln += 0.35		# opak cekirdekte komsuyla ince bindirme (dikis kalmasin)
			st = (round(mid, 4), round(ln, 3))
			if st == self.place[i] and w.IsShow():
				continue
			self.place[i] = st
			self.hiQ[i] = None
			self.segQ[i] = None
			hud._PutRaw(w, self.C, self.r, mid, ln, th, self.col[i])
			hud._PutRaw(h, self.C, self.r, mid, ln, th, self.colHi[i], 0.75)
			self.mids[i] = (s0 + s1) / 2.0
		self.lastPulse = True		# seritlerin rengi yeniden yazildi; __Animate taban rengi de verir
		self.__Animate(pct, t)
		if fill > 0.05:
			c = self.__Color(self.a0 + fill)
			hud._PutRaw(self.cap, self.C, self.r, self.a0 + fill, th, th, c)
		elif self.cap.IsShow():
			self.cap.Hide()

	def __Animate(self, pct, t):
		"""her kare: isik akisi + parlama + dusuk can nabzi (yalniz renk/alfa)."""
		fill = pct * self.span
		if fill <= 0.05:
			return
		a0 = self.hud.alpha
		per = self.FLOW_SEC + self.FLOW_REST
		q = ((t + self.phase) % per) / self.FLOW_SEC
		gp = -self.FLOW_W + q * (fill + 2.0 * self.FLOW_W) if q <= 1.0 else -1e9
		fl = 0.0
		if self.flashT >= 0.0:
			e = (t - self.flashT) / 0.45
			if e >= 1.0:
				self.flashT = -1.0
			else:
				fl = (1.0 - e) ** 2
		pulse = 0.0
		if self.low and pct < 0.25:
			pulse = abs(math.sin(t * math.pi / 0.55))
		d = self.span / float(self.N)
		n = min(self.N, int(math.ceil(fill / d)))
		hot = (pulse > 0.0 or fl > 0.0)
		aq = int(a0 * 255.0 + 0.5)
		W3 = 3.0 * self.FLOW_W		# exp(-9) ~ 1e-4: dalganin 3 genislik otesi sifir
		for i in xrange(n):
			dm = self.mids[i] - gp
			g = math.exp(-(dm / self.FLOW_W) ** 2) if (gp > -1e8 and -W3 < dm < W3) else 0.0
			g = max(g, fl)
			q = (int(g * 255.0 + 0.5), aq)
			if q != self.hiQ[i]:
				self.hiQ[i] = q
				c = self.colHi[i]
				m = 0.65 * g
				wndMgr.SetDiffuseColor(self.hi[i].hWnd, c[0] + (1.0 - c[0]) * m, c[1] + (1.0 - c[1]) * m, c[2] + (1.0 - c[2]) * m,
					max(0.0, min(1.0, (0.55 + 0.45 * g) * a0)))
			b = 0.35 * max(pulse, fl) if hot else 0.0
			q = (int(b * 255.0 + 0.5), aq)
			if q != self.segQ[i]:
				self.segQ[i] = q
				k = self.col[i]
				wndMgr.SetDiffuseColor(self.seg[i].hWnd, k[0] + (1.0 - k[0]) * b, k[1] + (1.0 - k[1]) * b, k[2] + (1.0 - k[2]) * b, a0)
		self.lastPulse = hot


class MinimapHud:
	"""MiniMap penceresine (ui.ScriptWindow, kok olcegi 1.0) baglanan cizim katmani."""
	## KULLANICI (2026-09-26): "+ ve - kalksin, buyutme (buyuk harita) dugmesi ortada buyuk"
	## KULLANICI (2026-09-26): "haritayi buyult butonunu kaldir, direkt minimapin ustune tiklayinca buyuk harita acilsin"
	BUTTONS = (("btn_close", "close"),)

	def __init__(self, owner, events):
		self.owner = owner
		self.events = events		# {"close": f, "world": f, "zin": f, "zout": f}
		(self.x0, self.y0, self.k) = Layout()
		self.keep = []
		self.tex = {}
		self.t = app.GetTime()
		self.tEnter = self.t
		self.dx = 0.0
		self.dy = 0.0
		self.alpha = 1.0
		self.mapOn = True
		self.press = {}
		self.collapsed = False
		self.taps = []
		k = self.k
		owner.SetPosition(self.x0, self.y0)
		owner.SetSize(int(math.ceil(G.HUD[2] * k)), int(math.ceil(G.HUD[3] * k)))
		# --- katmanlar (olusturma sirasi = cizim sirasi)
		self.shell = self.__Img("shell.png", G.shell)
		self.mapoff = self.__Img("mapoff.png", G.mapoff)
		self.mapoff.Hide()
		## KULLANICI (2026-10-02): orijinal kural geregi minimap gizli haritalarda (maymun zindani, katakomb) bos daire
		## yerine aciklama; buyuk harita olmayan yerde dokununca kisa uyari. Iki satir, dairenin ortasi.
		self.noteLines = None		# kalici not (minimap gizli)
		self.flashLines = None		# gecici uyari
		self.flashUntil = -1.0
		self.note = {}		# not gorselleri: butonlardan SONRA olusturulur (en ustte cizilsin)
		## KULLANICI (2026-09-26): "radari kaldir, oyunun kendi radari/oku var" -> tarama cizilmez
		self.vignette = self.__Img("vignette.png", G.vignette)
		self.compass = self.__Img("compass.png", G.compass)
		self.shellafter = self.__Img("shellafter.png", G.shellafter)
		self.arcback1 = self.__Img("arcback1.png", G.arcback1)
		## renkler: minimap-hud-oyun.html svg gradyanlari (hpArc / spArc) birebir
		## KULLANICI (2026-09-26): "renkleri koru kirmizi mavi, ama canli" -> doygun, parlak duraklar
		self.hpArc = _ArcFill(self, "HP", ((0.0, 0xff2410), (0.45, 0xff5a34), (0.68, 0xff3018), (1.0, 0xff2210)), 0.0, True)
		self.shine = []
		for i in xrange(6):
			w = self.__Img("shine.png", G.shine)
			w.Hide()
			self.shine.append(w)
		self.arcback2 = self.__Img("arcback2.png", G.arcback2)
		self.spArc = _ArcFill(self, "SP", ((0.0, 0x1e8cff), (0.45, 0x5cd0ff), (0.7, 0x2aa0ff), (1.0, 0x1e8cff)), 1.2, False)
		self.arcfront = self.__Img("arcfront.png", G.arcfront)
		self.btn = {}
		for (name, key) in self.BUTTONS:
			self.btn[key] = self.__Img(name + ".png", getattr(G, name))
		## KULLANICI (2026-10-02): "yazi cok kotu, okunur degil, silik" -> 10 pt TextLine golge katmanlarinin ALTINDA
		## kaliyordu. Pisirilmis NET doku (tools/minimap_not_bake.py: kalin + kontur + koyu serit, 3x), EN USTTE.
		for key in ("kucuk", "buyuk"):
			w = ui.ExpandedImageBox()
			w.SetParent(owner)
			w.AddFlag("not_pick")
			w.LoadImage(DIR + "not_%s.png" % key)
			w.Hide()
			self.keep.append(w)
			self.note[key] = w
		# dokunma alanlari: tasarim kutusu 44 px (KULLANICI: "butonlar cok kucuk" -> 31'den buyutuldu), araliklar 48-49 px;
		# parmak icin dikeyde komsuya kadar (+2), yatayda +8
		for (name, key) in self.BUTTONS:
			(bx, by, bw, bh) = getattr(G, name.upper() + "_BOX")
			pad = 2.0
			tap = _Tap(owner, lambda key=key: self.__OnButton(key))
			tap.SetPosition(int((bx - 8.0) * k), int((by - pad) * k))
			tap.SetSize(int((bw + 16.0) * k), int((bh + 2 * pad) * k))
			tap.Show()
			self.keep.append(tap)
			self.taps.append(tap)
		# harita dairesine dokunus -> buyuk harita (kare dokunma alani, dairenin icine sigan)
		vx, vy, vw, vh = G.VIEW
		inset = vw * 0.12
		mt = _Tap(owner, lambda: self.__OnButton("world"))
		mt.SetPosition(int((vx + inset) * k), int((vy + inset) * k))
		mt.SetSize(int((vw - 2 * inset) * k), int((vh - 2 * inset) * k))
		mt.Show()
		self.keep.append(mt)
		self.taps.append(mt)
		## KULLANICI (2026-09-26): "X'e basinca UI komple kapansin; geri acmak icin sag kosede onun gibi bir + belirsin,
		## basinca eski haline donsun" -> ayni sekizgen tarzda "+" (btn_open), HUD kutusunun sag ust kosesinde
		(ow, oh) = (G.btn_open[2], G.btn_open[3])
		self.openG = (G.HUD[2] - ow - 2.0, 2.0, ow, oh)
		self.openBtn = self.__Img("btn_open.png", self.openG)
		self.openBtn.Hide()
		self.openTap = _Tap(owner, lambda: self.__OnButton("open"))
		self.openTap.SetPosition(int((self.openG[0] - 8.0) * k), 0)
		self.openTap.SetSize(int((ow + 10.0) * k), int((oh + 10.0) * k))
		self.openTap.Hide()
		self.keep.append(self.openTap)
		# yaylar
		self.hpT = _Tween(0.0, 0.7)
		self.spT = _Tween(0.0, 0.7)
		self.__Apply(self.t)

	# ------------------------------------------------------------------ kurulum
	def __Img(self, name, g):
		w = ui.ExpandedImageBox()
		w.SetParent(self.owner)
		w.AddFlag("not_pick")
		w.LoadImage(DIR + name)
		max(0, 0)	# LoadImage bekleyen hatasini burada tetikle
		self.tex[w] = (float(w.GetWidth()), float(w.GetHeight()), g)	# doku boyutu OLCEKTEN ONCE
		s = self.k / TEX_S
		w.SetScale(s, s)
		w.SetPosition(int(round(g[0] * self.k)), int(round(g[1] * self.k)))
		w.Show()
		self.keep.append(w)
		return w

	def _MakeRaw(self, name):
		w = ui.ExpandedImageBox()
		w.SetParent(self.owner)
		w.AddFlag("not_pick")
		w.LoadImage(DIR + name)
		max(0, 0)
		self.tex[w] = (float(w.GetWidth()), float(w.GetHeight()), None)
		w.Hide()
		self.keep.append(w)
		return w

	def _PutRaw(self, w, C, r, deg, ln, th, col, a=1.0):
		"""serit/uc: yay (merkez C, yaricap r tasarim px) uzerinde 'deg' acisinda, teget yonde ln x th ekran px."""
		(tw, th0, g) = self.tex[w]
		k = self.k
		rad = math.radians(deg)
		cx = (C[0] + r * math.cos(rad)) * k + self.dx
		cy = (C[1] + r * math.sin(rad)) * k + self.dy
		ix = int(math.floor(cx))
		iy = int(math.floor(cy))
		w.SetScale(ln / tw, th / th0)
		w.SetPosition(ix, iy)
		w.SetOrigin(cx - ix, cy - iy)
		w.SetRotation(deg + 90.0)
		wndMgr.SetDiffuseColor(w.hWnd, col[0], col[1], col[2], max(0.0, min(1.0, a * self.alpha)))
		if not w.IsShow():
			w.Show()

	# ------------------------------------------------------------------ yerlestirme
	def __Place(self, w, a=1.0):
		"""ALT-PIKSEL yerlesim: tam sayiya yuvarlanan konumlar komsu yay dilimlerini yarim px kaydirip kenarda centik
		birakiyordu (KULLANICI: "hp sp pixel pixel"). Native doner yol (SetRotation != 0) merkezi (konum + origin)
		ondalikli koyar -> cok kucuk aci ile o yol kullanilir."""
		(tw, th, g) = self.tex[w]
		cx = (g[0] + g[2] / 2.0) * self.k + self.dx
		cy = (g[1] + g[3] / 2.0) * self.k + self.dy
		ix = int(math.floor(cx))
		iy = int(math.floor(cy))
		w.SetPosition(ix, iy)
		w.SetOrigin(cx - ix, cy - iy)
		w.SetRotation(1e-4)
		w.SetAlpha(max(0.0, min(1.0, a * self.alpha)))

	def __Rot(self, w, pivot, deg, a=1.0, sc=1.0):
		"""gorseli tasarim noktasi 'pivot' etrafinda deg derece (saat yonu) dondur. Native doner gorseli KENDI merkezi
		etrafinda cevirir ve merkezi (konum + origin)'e koyar -> merkezi pivot etrafinda biz dondururuz."""
		(tw, th, g) = self.tex[w]
		k = self.k
		s = k / TEX_S * sc
		cx = (g[0] + g[2] / 2.0) * k
		cy = (g[1] + g[3] / 2.0) * k
		px = pivot[0] * k
		py = pivot[1] * k
		r = math.radians(deg)
		c = math.cos(r)
		sn = math.sin(r)
		ncx = px + (cx - px) * c - (cy - py) * sn * 1.0
		ncy = py + (cx - px) * sn + (cy - py) * c
		# olcek (sc) pivot etrafinda
		ncx = px + (ncx - px) * sc + self.dx
		ncy = py + (ncy - py) * sc + self.dy
		ix = int(math.floor(ncx))
		iy = int(math.floor(ncy))
		w.SetScale(s, s)
		w.SetPosition(ix, iy)
		w.SetOrigin(ncx - ix, ncy - iy)
		w.SetRotation(deg if abs(deg) > 1e-4 else 1e-4)
		w.SetAlpha(max(0.0, min(1.0, a * self.alpha)))

	# ------------------------------------------------------------------ olaylar
	def __OnButton(self, key):
		self.press[key] = app.GetTime()
		f = self.events.get(key)
		if f:
			f()

	def SetMapOn(self, on):
		self.mapOn = on
		if on:
			self.mapoff.Hide()
		else:
			self.mapoff.Show()

	def SetNote(self, lines):
		"""kalici not (None = yok): minimap bu haritada orijinal kural geregi gizli"""
		self.noteLines = lines
		self.__ShowNote()

	def Flash(self, lines, sec=2.5):
		"""gecici uyari (ornek: bu bolgede buyuk harita yok)"""
		self.flashLines = lines
		self.flashUntil = app.GetTime() + sec
		self.__ShowNote()

	def __ShowNote(self):
		key = self.noteLines
		if self.flashLines and app.GetTime() < self.flashUntil:
			key = self.flashLines
		for k in self.note:
			if k != key or self.collapsed:
				self.note[k].Hide()
		if self.collapsed or not key or key not in self.note:
			return
		w = self.note[key]
		vx, vy, vw, vh = G.VIEW
		lw = NOTE_W * self.k * (226.0 / 142.0) * 0.78		# dairenin ~%78'i
		sc = lw / float(NOTE_TEX[0])
		cx = (vx + vw / 2.0) * self.k + self.dx
		cy = (vy + vh / 2.0) * self.k + self.dy
		w.SetScale(sc, sc)
		w.SetPosition(int(round(cx - NOTE_TEX[0] * sc / 2.0)), int(round(cy - NOTE_TEX[1] * sc / 2.0)))
		w.Show()

	def Replay(self):
		self.tEnter = app.GetTime()

	def Destroy(self):
		"""sahip (MiniMap) yok edilince: gorselleri gizle, donguleri kir (eski pencere bellekte kalip cizmesin)."""
		for w in self.keep:
			try:
				w.Hide()
			except:
				pass
		self.keep = []
		self.taps = []
		self.tex = {}
		self.events = {}
		self.owner = None
		self.hpArc = None
		self.spArc = None

	def Collapse(self):
		"""X: tum HUD gizlenir, yalniz sag ustte "+" kalir."""
		self.collapsed = True
		for w in self.keep:
			w.Hide()
		self.openBtn.Show()
		self.openTap.Show()
		self.__Place(self.openBtn)

	def Expand(self):
		"""+: HUD giris animasyonuyla geri gelir."""
		self.collapsed = False
		self.openBtn.Hide()
		self.openTap.Hide()
		for w in (self.shell, self.vignette, self.compass, self.shellafter, self.arcback1, self.arcback2, self.arcfront):
			w.Show()
		for (name, key) in self.BUTTONS:
			self.btn[key].Show()
		for tp in self.taps:
			tp.Show()
		if not self.mapOn:
			self.mapoff.Show()
		for arc in (self.hpArc, self.spArc):
			arc.lastP = -1.0
			arc.lastK = None
		self._placeKey = None
		self.Replay()
		self.__ShowNote()
		self.__Apply(app.GetTime())

	# ------------------------------------------------------------------ kare
	def Update(self):
		t = app.GetTime()
		self.t = t
		# hudIn: .85 s cubic-bezier(.16,1,.3,1): translate(35px,-20px) -> 0, opacity 0 -> 1
		if self.tEnter >= 0.0:
			p = (t - self.tEnter) / 0.85
			if p >= 1.0:
				self.tEnter = -1.0
				self.dx = self.dy = 0.0
				self.alpha = 1.0
			else:
				e = 1.0 - (1.0 - p) ** 4
				self.dx = 35.0 * self.k * (1.0 - e)
				self.dy = -20.0 * self.k * (1.0 - e)
				self.alpha = min(1.0, p * 1.6)
		# gercek HP / SP
		try:
			hp = float(player.GetStatus(player.HP))
			mhp = float(max(1, player.GetStatus(player.MAX_HP)))
			sp = float(player.GetStatus(player.SP))
			msp = float(max(1, player.GetStatus(player.MAX_SP)))
			nh = max(0.0, min(1.0, hp / mhp))
			ns = max(0.0, min(1.0, sp / msp))
			if abs(nh - self.hpT.v1) > 0.004 and self.tEnter < 0.0 and not self.collapsed:
				self.hpArc.Flash(t)
			if abs(ns - self.spT.v1) > 0.004 and self.tEnter < 0.0 and not self.collapsed:
				self.spArc.Flash(t)
			self.hpT.Set(nh, t)
			self.spT.Set(ns, t)
		except:
			pass
		if self.collapsed:
			# yalniz "+" dugmesinin basma olcegi
			p0 = self.press.get("open", -1.0)
			sc = 1.0
			if p0 >= 0.0:
				q = (t - p0) / 0.16
				if q >= 1.0:
					self.press["open"] = -1.0
				else:
					sc = 1.0 - 0.04 * math.sin(q * math.pi)
			g = self.openG
			self.__Rot(self.openBtn, (g[0] + g[2] / 2.0, g[1] + g[3] / 2.0), 0.0, 1.0, sc)
			return
		self.__Apply(t)

	def __Apply(self, t):
		## HIZ (2026-10-01): 8 sabit gorsel her kare yeniden yerlesiyordu -> yalniz giris kaymasi/alfa degisince
		pk = (self.dx, self.dy, self.alpha, self.k)
		placeAll = (pk != getattr(self, "_placeKey", None))
		self._placeKey = pk
		if placeAll or (self.flashLines and t >= self.flashUntil):
			if self.flashLines and t >= self.flashUntil:
				self.flashLines = None
			self.__ShowNote()
		if placeAll:
			for w in (self.shell, self.mapoff, self.vignette, self.compass, self.shellafter, self.arcback1,
					self.arcback2, self.arcfront):
				self.__Place(w)
		# yay dolgulari (kodla)
		self.hpArc.Update(self.hpT.Get(t), t)
		self.spArc.Update(self.spT.Get(t), t)
		# parlama: 8/13 kesik (pathLength 100), dashoffset 0 -> -20 / 2.4 s; tek kesik yay merkezi etrafinda doner
		off = (t / 2.4 % 1.0) * 20.0
		span = G.HP_A[1]
		j = 0
		for n in xrange(-1, 6):
			if j >= len(self.shine):
				break
			s0 = 21.0 * n + off
			if s0 < -0.01 or s0 + 8.0 > 100.01:
				continue
			self.__Rot(self.shine[j], G.HP_C, s0 / 100.0 * span)
			if not self.shine[j].IsShow():
				self.shine[j].Show()
			j += 1
		while j < len(self.shine):
			self.shine[j].Hide()
			j += 1
		# dugmeler: basinca scale(.96) ~.16 s
		for (name, key) in self.BUTTONS:
			w = self.btn[key]
			p0 = self.press.get(key, -1.0)
			sc = 1.0
			if p0 >= 0.0:
				q = (t - p0) / 0.16
				if q >= 1.0:
					self.press[key] = -1.0
				else:
					sc = 1.0 - 0.04 * math.sin(q * math.pi)
			last = self.btnSc.get(key) if hasattr(self, "btnSc") else None
			if not hasattr(self, "btnSc"):
				self.btnSc = {}
			if sc == last and not placeAll:
				continue
			self.btnSc[key] = sc
			if sc != 1.0:
				(tw, th, g) = self.tex[w]
				self.__Rot(w, (g[0] + g[2] / 2.0, g[1] + g[3] / 2.0), 0.0, 1.0, sc)
			else:
				w.SetScale(self.k / TEX_S, self.k / TEX_S)
				self.__Place(w)
