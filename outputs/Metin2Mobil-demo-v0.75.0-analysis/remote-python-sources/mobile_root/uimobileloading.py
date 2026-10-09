# -*- coding: latin-1 -*-
# MOBIL: yeni yukleme ekrani (KULLANICI 2026-09-24, tasarim Desktop/Metin2-Loading-Ekrani/loading.html).
# Gorseller tools/loading_skin_export.py ile headless Chrome'dan 2x yakalandi (mobile/ui/loading2/),
# yerlesim mobileloadingskin.py (tasarim CSS px 1280x705). Olcek k = min(W/1280, H/705); doku olcegi k/2.
#
# PERFORMANS (KULLANICI: "profesyonel yaklas, oyunu agirlastirmasin, goruntu hic bozulmasin"):
#  - 14 doku, en buyugu 1920 px JPG arka plan (kaynak 1672 px; daha buyugu bosuna bellek).
#  - Animasyonlar (nefes alan sahne, logo belirmesi, 7 kor tanecigi, cubuk ucu parlama) yalniz
#    konum/olcek/alfa degistirir; kare basi doku uretimi / yeniden yukleme YOK.
#  - Yalniz yukleme perdesi acikken yasar: Destroy() ile tum pencereler birakilir, dokular
#    CResourceManager referans sayimiyla serbest kalir. Oyun icinde hicbir sey calismaz.
import math
import ui
import wndMgr
import app
import mobileloadingskin as SK

IMG = "mobile/ui/loading2/"
EMBER_IMG = "mobile/ui/login/ember.png"		# giris ekraniyla ayni kucuk parlama dokusu (32 px)
DW = float(SK.DESIGN_W)
DH = float(SK.DESIGN_H)
STATUS_STEPS = (0, 16, 38, 61, 82, 100)		# tasarimdaki messages[] esikleri (status_0..5.png)
## .embers i:nth-child(n): left %, sure (s), gecikme (s)
EMBERS = ((8, 6.0, -1.0), (19, 8.0, -5.0), (33, 7.0, -2.0), (54, 9.0, -6.0),
		  (69, 6.5, -3.0), (83, 8.5, -4.0), (94, 7.5, -1.5))
PERCENT_RGB = (0xF0 / 255.0, 0xCF / 255.0, 0x8F / 255.0)


class LoadingSkin(object):
	def __init__(self, parent):
		self.parent = parent
		self.keep = []
		self.sw = float(wndMgr.GetScreenWidth())
		self.sh = float(wndMgr.GetScreenHeight())
		self.k = min(self.sw / DW, self.sh / DH)
		self.ox = (self.sw - DW * self.k) / 2.0
		self.oy = (self.sh - DH * self.k) / 2.0
		self.ts = self.k / float(SK.TEX_SCALE)
		self.t0 = app.GetTime()
		self.tLast = self.t0
		self.progress = 0.0		# hedef (gercek yukleme adimi)
		self.shown = 0.0		# ekrandaki (yumusatilmis, tasarimdaki .35s gecis)
		self.statusIdx = -1
		self.pctText = None
		self.waitSec = 0.0		# cubugun adimlari bekletme toplami (olcum, syserr'e yazilir)
		import time
		_b0 = time.time()
		self.__Build()
		self.buildSec = time.time() - _b0	# doku cozme + pencere kurulumu suresi (app.GetTime kare icinde sabit, o yuzden time.time)
		self.Update(self.t0)

	# ------------------------------------------------------------------ yardimcilar
	def X(self, x):
		return self.ox + x * self.k

	def Y(self, y):
		return self.oy + y * self.k

	def __Img(self, name, file = None, show = True):
		img = ui.ExpandedImageBox()
		img.SetParent(self.parent)
		img.AddFlag("not_pick")
		img.LoadImage(IMG + (file or name + ".png"))
		max(0, 0)	# LoadImage'in bekleyen hatasini burada tetikle (Py_BuildException tuzagi)
		if name in SK.RECTS:
			(rx, ry, rw, rh) = SK.RECTS[name]
			img.SetScale(self.ts, self.ts)
			img.SetPosition(int(round(self.X(rx))), int(round(self.Y(ry))))
		if show:
			img.Show()
		else:
			img.Hide()
		self.keep.append(img)
		return img

	def __Build(self):
		## arka plan: kaplama (cover) olcegi; nefes animasyonu Update'te
		bg = ui.ExpandedImageBox()
		bg.SetParent(self.parent)
		bg.AddFlag("not_pick")
		bg.LoadImage(IMG + "bg.jpg")
		max(0, 0)
		self.bgW = float(max(1, bg.GetWidth()))
		self.bgH = float(max(1, bg.GetHeight()))
		self.bgBase = max(self.sw / self.bgW, self.sh / self.bgH)
		bg.Show()
		self.keep.append(bg)
		self.bg = bg

		## kor tanecikleri arka planin hemen ustunde (tasarim z 2), diger her sey ustte
		self.embers = []
		for (left, dur, delay) in EMBERS:
			e = ui.ExpandedImageBox()
			e.SetParent(self.parent)
			e.AddFlag("not_pick")
			e.LoadImage(EMBER_IMG)
			max(0, 0)
			e.Show()
			self.keep.append(e)
			self.embers.append({"img": e, "x": left / 100.0 * self.sw, "dur": dur, "d": delay,
				"w": float(max(1, e.GetWidth()))})

		self.topLine = self.__Img("top_line")
		self.logo = self.__Img("logo")
		(lx, ly, lw, lh) = SK.RECTS["logo"]
		self.logoCx = self.X(lx + lw / 2.0)
		self.logoCy = self.Y(ly + lh / 2.0)
		self.logoW = lw * self.k
		self.logoH = lh * self.k
		self.chapter = self.__Img("chapter")
		self.frame = self.__Img("bar_frame")
		self.fill = self.__Img("bar_fill")
		self.__SetFill(0.0)
		(tx, ty, tw, th) = SK.RECTS["a_bar_track"]
		self.trackX0 = self.X(tx)
		self.trackW = tw * self.k
		self.trackCy = self.Y(ty + th / 2.0)
		self.glow = self.__Img("tip_glow")
		self.glowW = 56 * self.k
		self.glowH = 64 * self.k
		self.tip = self.__Img("tip")
		self.status = []
		for i in xrange(len(STATUS_STEPS)):
			self.status.append(self.__Img("status_%d" % i, show = False))

		## yuzde: tasarim "bold 13px Georgia" #f0cf8f, saga yasli
		(px, py, pw, ph) = SK.RECTS["a_percent"]
		t = ui.TextLine()
		t.SetParent(self.parent)
		t.AddFlag("not_pick")
		t.SetFontName("Tahoma:%d" % max(10, int(round(14 * self.k))))
		t.SetFontColor(PERCENT_RGB[0], PERCENT_RGB[1], PERCENT_RGB[2])
		t.SetOutline(True)
		t.SetHorizontalAlignRight()
		t.SetVerticalAlignCenter()
		t.SetPosition(int(round(self.X(px + pw))), int(round(self.Y(py + ph / 2.0))))
		t.SetText("0%")
		t.Show()
		self.keep.append(t)
		self.percent = t

	def __SetFill(self, pct):
		## KULLANICI (2026-09-24): "dolgu parlamadan ayri gidiyor, once bos sonra birden doluyor".
		## KOK NEDEN (gercek client ile ayni, EterLib/GrpExpandedImageInstance): SetRenderingRect'in degeri
		## OLCEKSIZ doku genisligiyle carpilip piksel olarak saklanir, OnRender ise OLCEKLI genislige ekler.
		## 2x dokuyu ts (~0.5) ile cizdigimiz icin SetPercentage(p) gercekte %50'ye kadar hic gostermiyor,
		## sonra iki kat hizli doluyordu. Telafi: sag kenari ts ile carp -> piksel = -(1-p) * olcekli genislik.
		self.fill.SetRenderingRect(0.0, 0.0, -(1.0 - pct / 100.0) * self.ts, 0.0)

	# ------------------------------------------------------------------ dis arayuz
	def SetProgress(self, p):
		self.progress = max(0.0, min(100.0, float(p)))

	def Reached(self):
		## cubuk hedef degere gorsel olarak ulasti mi (introloading adim kapisi)
		return self.shown >= self.progress - 0.01

	def Update(self, t):
		dt = t - self.t0
		frame = max(0.0, min(0.1, t - self.tLast))
		self.tLast = t

		## sahne nefesi: 9 s ease-in-out, ileri-geri (scale 1.02 -> 1.07, -0.7% yukari)
		u = math.fmod(dt / 9.0, 2.0)
		if u > 1.0:
			u = 2.0 - u
		e = u * u * (3.0 - 2.0 * u)
		s = self.bgBase * (1.02 + 0.05 * e)
		dy = -0.007 * self.sh * e
		self.bg.SetScale(s, s)
		self.bg.SetPosition(int(round((self.sw - self.bgW * s) / 2.0)), int(round((self.sh - self.bgH * s) / 2.0 + dy)))

		## logo belirmesi: 1.2 s, ease-out; hafif yukaridan, %92'den buyuyerek
		a = min(1.0, dt / 1.2)
		ea = 1.0 - (1.0 - a) * (1.0 - a) * (1.0 - a)
		sc = 0.92 + 0.08 * ea
		self.logo.SetScale(self.ts * sc, self.ts * sc)
		self.logo.SetPosition(int(round(self.logoCx - self.logoW * sc / 2.0)),
			int(round(self.logoCy - self.logoH * sc / 2.0 - 18.0 * self.k * (1.0 - ea))))
		self.logo.SetAlpha(ea)

		## kor tanecikleri: alttan (-8%) yukari (-105vh), +45px saga, olcek .5 -> 1.3, alfa 0 -> .8 -> 0
		for em in self.embers:
			ph = math.fmod(dt - em["d"], em["dur"]) / em["dur"]
			if ph < 0.0:
				ph += 1.0
			es = (14.0 * self.k / em["w"]) * (0.5 + 0.8 * ph)
			em["img"].SetScale(es, es)
			em["img"].SetPosition(int(em["x"] + ph * 45.0 * self.k), int(self.sh * 1.08 - ph * 1.05 * self.sh))
			if ph < 0.15:
				al = ph / 0.15 * 0.8
			else:
				al = 0.8 * (1.0 - (ph - 0.15) / 0.85)
			em["img"].SetAlpha(max(0.0, al))

		## ilerleme: hedefe dogru sabit hizli akis (en az 140 %/s, buyuk farkta daha hizli); cubuk hic ziplamaz.
		## KULLANICI (2026-09-24): "bar tam dolmuyor, oyunun gercek yuklemesiyle bir olmali" -> introloading
		## bir sonraki yukleme adimini cubuk bu adimin degerine GORSEL olarak ulasmadan calistirmaz (Reached).
		diff = self.progress - self.shown
		if diff > 0.0:
			self.shown = min(self.progress, self.shown + max(140.0, diff * 8.0) * frame)
			self.waitSec += frame
		else:
			self.shown = self.progress
		vis = max(1.5, self.shown)		# bos cubukta bile kucuk bir kor gorunsun
		self.__SetFill(vis)
		gx = self.trackX0 + self.trackW * vis / 100.0
		pulse = 0.85 + 0.15 * math.sin(dt * 6.0)
		self.glow.SetPosition(int(round(gx - self.glowW / 2.0)), int(round(self.trackCy - self.glowH / 2.0)))
		self.glow.SetAlpha(pulse)
		txt = "%d%%" % int(self.shown)
		if txt != self.pctText:		# yazi dokusu yalniz deger degisince yeniden cizilsin
			self.pctText = txt
			self.percent.SetText(txt)

		## durum yazisi (tasarimdaki esikler)
		idx = 0
		for i in xrange(len(STATUS_STEPS)):
			if self.progress >= STATUS_STEPS[i]:
				idx = i
		if idx != self.statusIdx:
			if self.statusIdx >= 0:
				self.status[self.statusIdx].Hide()
			self.status[idx].Show()
			self.statusIdx = idx

	def Destroy(self):
		for w in self.keep:
			try:
				w.Hide()
			except:
				pass
		self.keep = []
		self.embers = []
		self.status = []
		self.bg = None
		self.logo = None
		self.fill = None
		self.glow = None
		self.percent = None
		self.parent = None
