# MOBIL KAPLAMA (mobile_root/uimobilelogin.py) - yalniz telefon.
# KULLANICI (2026-09-16): giris + sunucu/kanal secim ekrani yeni tasarim (Desktop/login_tasarim/index.html).
# Gorseller tools/login_skin_export.py ile tasarimdan 2x cozunurlukte cikarilir (mobile/ui/login/*),
# yerlesim mobileloginskin.py (tasarim CSS px 1356x610). Olcek k = min(W/1356, H/610); sol ogeler sola,
# sag ogeler saga yapisik (farkli ekran oranlarinda paneller ust uste binmez).
# Mantik intrologin.py'de kalir (sunucu/kanal ListBox'lari, Connect, ServerStateChecker); bu sinif
# yalniz cizer ve LoginWindow geri cagrilarini tetikler.
import ui
import wndMgr
import app
import snd
import systemSetting
import serverInfo
import localeInfo
import mobileLoginSkin as SK

IMG = "mobile/ui/login/"
## KULLANICI (2026-10-06): COK DIL. dil=en iken yazili gorsellerin Ingilizcesi mobile/ui/login/en/ altinda
## (tools/dil/bake_login_en.py: Turkce yazi silinip ayni font/renk/golgeyle Ingilizce cizildi).
EN_GORSEL = ("srv_panel.png", "ch_panel.png", "login_panel.png", "acc_empty.png",
	"btn_login.png", "btn_login_down.png", "btn_change.png", "btn_change_down.png", "btn_delacc.png", "btn_delacc_down.png") + tuple(["btn_continue_%d%s.png" % (n, e) for n in range(7) for e in ("", "_down")])
## KULLANICI (2026-10-07): 6 KANAL. Tasarimda yalniz ch0..ch3 (2x2) var; 5. ve 6. kart ayni sutun/satir
## adimiyla ucuncu satira konur (tasarim y 332..425; devam dugmesi 480'de). Devam gorseli btn_continue_1..6
## (5/6: tools/kanal6/kanal_dugme_bake.py, TR + en/).
KANAL_KART = 6
CH_BASLIK_EN_DX = 60.0		# "Select Channel \xb7" basligi "Kanal Se\xe7 \xb7"tan bu kadar (tasarim px) uzun: sunucu adi saga kayar


def _Dil():
	try:
		import dil
		return dil.Mevcut()
	except:
		return "tr"


def _Y(tr, en):
	return en if _Dil() == "en" else tr


def _IP(f):
	if f in EN_GORSEL and _Dil() == "en":
		return IMG + "en/" + f
	return IMG + f

## KULLANICI (2026-09-16): hareketli arka plan. Video YALNIZ destegi olan APK'da denenir
## (app.ENABLE_VIDEO_BACKGROUND - eski surumlerde bu sabit yok); acilamazsa duragan resme duser.
VIDEO_FILE = "arkaplan.mp4"
VIDEO_FAILED = False
DW = float(SK.DESIGN_W)
DH = float(SK.DESIGN_H)

INK = (0.953, 0.902, 0.788)
INK_DIM = (0.725, 0.655, 0.541)
BRONZE_HI = (0.941, 0.804, 0.541)

ACCOUNT_FILE = "pack/hesap%d.cfg"
REMEMBER_FILE = "pack/mobile_login.cfg"

SERVER_SUBTITLE = "T\xfcrkiye \xb7 105 seviye \xb7 Oto av"
SERVER_SUBTITLE_EN = "Turkey \xb7 Level 105 \xb7 Auto hunt"
NEWS = (
	("16.09", "Emoji halkas\xfd ve joystick kilidi eklendi."),
	("15.09", "Envanter 6\xd78 \xb7 4 sekme oldu."),
	("15.09", "Otomatik av \xfccretsiz ve s\xfcresiz."),
)
NEWS_EN = (
	"Emoji ring and joystick lock added.",
	"Inventory is now 6\xd78 with 4 tabs.",
	"Auto hunt is free and unlimited.",
)
YER_TUTUCU = {"id_edit": ("Hesap ad\xfdn", "Username"), "pwd_edit": ("\xdeifre", "Password")}
DURUM_EN = {"Normal": "Normal", "Yo\xf0un": "Busy", "Dolu": "Full"}

STATE_MAP = {
	"NORM": ("ok", "Normal", 0.38),
	"BUSY": ("warn", "Yo\xf0un", 0.74),
	"FULL": ("full", "Dolu", 1.0),
}
## v78 (2026-10-08): DOLU (FULL) kanal SECILEMEZ - kart soluk (kartin kendi gorseli siyah, yari saydam ortu olarak
## ustune), dokununca kisa uyari; secim degismez. Durum bilgisi ayni yerden: ServerStateChecker ->
## intrologin.NotifyChannelState -> serverInfo...["state"] ("FULL"). Devam dugmesi zaten engelliyordu
## (intrologin __OnClickSelectServerButton: CHANNEL_NOTIFY_FULL) - o yol aynen kalir.
DOLU_DURUM = "FULL"
DOLU_UYARI = ("Kanal dolu, ba\xfeka kanal se\xe7in.", "Channel is full, please choose another one.")
DOLU_ORTU_ALFA = 0.55


class ClickArea(ui.Window):
	def __init__(self, event):
		ui.Window.__init__(self)
		self.event = event

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseLeftButtonUp(self):
		if self.event:
			self.event()
		return True


class LoginSkin(object):
	def __init__(self, cb):
		## cb: "id_edit", "pwd_edit", "login", "open_server", "exit", "select_server_line",
		##     "select_channel_line", "continue", "back", "popup", "server_list", "channel_list",
		##     "server_id", "channel_id"
		self.cb = cb
		self.sw = float(wndMgr.GetScreenWidth())
		self.sh = float(wndMgr.GetScreenHeight())
		self.k = min(self.sw / DW, self.sh / DH)
		self.oy = (self.sh - DH * self.k) / 2.0
		self.keep = []
		self.btnEvents = []
		self.editLines = []
		self.accChips = []
		self.srvCards = []
		self.chCards = []
		self.embers = []
		self.accountSel = -1
		self.remember = self.__LoadRemember()
		self.pwdVisible = False

		root = ui.Window()
		if hasattr(wndMgr, "SetUIScale"):
			wndMgr.SetUIScale(root.hWnd, 1.0)
		root.AddFlag("not_pick")
		root.SetSize(int(self.sw), int(self.sh))
		root.SetPosition(0, 0)
		root.Show()
		self.root = root

		self.loginScr = self.__Container()
		self.serverScr = self.__Container()
		self.__BuildLogin()
		self.__BuildServer()
		self.loginScr.Hide()
		self.serverScr.Hide()

	def Destroy(self):
		try:
			import uidil
			uidil.Kapat()
		except:
			pass
		for (btn, ev) in self.btnEvents:
			try:
				btn.SetEvent(None)
			except:
				pass
		self.btnEvents = []
		if self.root:
			self.root.Hide()
		self.embers = []
		self.editLines = []
		self.keep = []
		self.cb = {}
		self.srvCards = []
		self.chCards = []
		self.accChips = []
		self.loginScr = None
		self.serverScr = None
		self.root = None

	# ------------------------------------------------------------------ yardimcilar
	def __Container(self):
		c = ui.Window()
		c.SetParent(self.root)
		c.AddFlag("not_pick")
		c.SetSize(int(self.sw), int(self.sh))
		c.SetPosition(0, 0)
		c.Show()
		self.keep.append(c)
		return c

	def X(self, x, side):
		if side == "R":
			return self.sw - (DW - x) * self.k
		return x * self.k

	def Y(self, y):
		return self.oy + y * self.k

	def __Rect(self, name, side):
		(x, y, w, h) = SK.RECTS[name]
		return (int(round(self.X(x, side))), int(round(self.Y(y))), w, h)

	def __Anchor(self, name, side):
		(x, y, w, h) = SK.ANCHORS[name]
		return (self.X(x, side), self.Y(y), w * self.k, h * self.k)

	def __Image(self, parent, name, side, file = None, rectName = None):
		img = ui.ExpandedImageBox()
		img.SetParent(parent)
		img.AddFlag("not_pick")
		img.LoadImage(_IP((file or name + ".png")))
		s = self.k / float(SK.TEX_SCALE)
		img.SetScale(s, s)
		(x, y, w, h) = self.__Rect(rectName or name, side)
		img.SetPosition(x, y)
		img.Show()
		self.keep.append(img)
		return img

	def __Dot(self, parent, kind, x, y):
		img = ui.ExpandedImageBox()
		img.SetParent(parent)
		img.AddFlag("not_pick")
		img.LoadImage(_IP("dot_" + kind + ".png"))
		s = self.k / float(SK.TEX_SCALE)
		img.SetScale(s, s)
		img.SetPosition(int(round(x)), int(round(y)))
		img.Hide()
		self.keep.append(img)
		return img

	def __DotSet(self, parent, cx, cy):
		## cx, cy = noktanin MERKEZI (ekran px)
		(rx, ry, rw, rh) = SK.RECTS["dot_ok"]
		half = rw * self.k / 2.0
		halfY = rh * self.k / 2.0
		d = {}
		for kind in ("ok", "warn", "full"):
			d[kind] = self.__Dot(parent, kind, cx - half, cy - halfY)
		return d

	def __ShowDot(self, dots, kind):
		for (k, img) in dots.items():
			if k == kind:
				img.Show()
			else:
				img.Hide()

	def __Button(self, parent, name, side, event, rectName = None, down = True, pos = None):
		btn = ui.Button()
		btn.SetParent(parent)
		btn.SetUpVisual(_IP(name + ".png"))
		btn.SetOverVisual(_IP(name + ".png"))
		btn.SetDownVisual(_IP((name + "_down.png" if down else name + ".png")))
		if hasattr(wndMgr, "SetButtonScale"):
			s = self.k / float(SK.TEX_SCALE)
			wndMgr.SetButtonScale(btn.hWnd, s, s)
		if pos:
			btn.SetPosition(pos[0], pos[1])
		else:
			(x, y, w, h) = self.__Rect(rectName or name, side)
			btn.SetPosition(x, y)
		btn.SetEvent(event)
		btn.Show()
		self.keep.append(btn)
		self.btnEvents.append((btn, event))
		return btn

	def __Text(self, parent, text, x, y, size, color = INK, align = "L"):
		t = ui.TextLine()
		t.SetParent(parent)
		t.AddFlag("not_pick")
		t.SetFontName("Tahoma:%d" % max(8, int(round(size * self.k))))
		t.SetFontColor(color[0], color[1], color[2])
		if align == "C":
			t.SetHorizontalAlignCenter()
		elif align == "R":
			t.SetHorizontalAlignRight()
		t.SetVerticalAlignCenter()
		t.SetPosition(int(round(x)), int(round(y)))
		t.SetText(text)
		t.Show()
		self.keep.append(t)
		return t

	def __ClickArea(self, parent, x, y, w, h, event, top = False):
		area = ClickArea(event)
		area.SetParent(parent)
		area.SetPosition(int(round(x)), int(round(y)))
		area.SetSize(int(round(w)), int(round(h)))
		area.Show()
		if top:
			area.SetTop()
		self.keep.append(area)
		return area

	def __Background(self, parent, file):
		img = ui.ExpandedImageBox()
		img.SetParent(parent)
		img.AddFlag("not_pick")
		## VIDEO_FILE doluysa once hareketli arka plan denenir (Android donanim cozucusu);
		## acilamazsa / kapaliysa duragan resim.
		## DIKKAT: wndMgr.LoadImage acilamayan dosyada ISTISNA firlatir ("Failed to load image").
		## Cozucusu kare uretmeyen telefonlarda bu istisna butun yeni tasarimi iptal edip
		## ESKI giris ekranini getiriyordu - video denemesi mutlaka yakalanir.
		## KOK NEDEN (arkadas telefonu): wndMgr.LoadImage basarisizlikta hatayi ANINDA firlatmaz -
		## Py_BuildException None dondurup C hata bayragini beklemede birakir; hata try disinda,
		## ilk PyErr_Occurred kontrol eden yerde (asagidaki float/max) patlar. max() bu bekleyen
		## hatayi try ICINDE tetikler. Basarisizlik bir kez gorulunce ikinci ekran hic denemez.
		global VIDEO_FAILED
		if VIDEO_FILE and not VIDEO_FAILED and getattr(app, "ENABLE_VIDEO_BACKGROUND", 0):
			try:
				img.LoadImage(_IP(VIDEO_FILE))
				max(0, 0)
			except:
				VIDEO_FAILED = True
			if img.GetWidth() <= 0 or img.GetHeight() <= 0:
				VIDEO_FAILED = True
		if img.GetWidth() <= 0 or img.GetHeight() <= 0:
			img.LoadImage(_IP(file))
		w = float(max(1, img.GetWidth()))
		h = float(max(1, img.GetHeight()))
		## kaplama (cover): ekran orani farkli olsa da bosluk kalmaz
		s = max(self.sw / w, self.sh / h)
		img.SetScale(s, s)
		img.SetPosition(int(round((self.sw - w * s) / 2.0)), int(round((self.sh - h * s) / 2.0)))
		img.Show()
		self.keep.append(img)
		return img

	def __BuildEmbers(self, parent):
		## tasarimdaki kivilcimlar: sol tarafta asagidan yukari suzulen parcaciklar
		self.embers = []
		for i in xrange(22):
			img = ui.ExpandedImageBox()
			img.SetParent(parent)
			img.AddFlag("not_pick")
			img.LoadImage(_IP("ember.png"))
			s = (9.0 * self.k) / 32.0
			img.SetScale(s, s)
			img.Show()
			self.keep.append(img)
			seed = ((i * 7919) % 1000) / 1000.0
			self.embers.append({
				"img": img,
				"x": seed * 0.62 * self.sw,
				"dur": 6.0 + (((i * 3571) % 1000) / 1000.0) * 7.0,
				"t0": -(((i * 1543) % 1000) / 1000.0) * 10.0,
			})

	# ------------------------------------------------------------------ GIRIS EKRANI
	def __BuildLogin(self):
		p = self.loginScr
		self.__Background(p, "bg_login.jpg")
		self.__BuildEmbers(p)
		self.__Image(p, "brand", "L")
		self.__Image(p, "status_chip", "L")
		self.loginPanelImg = self.__Image(p, "login_panel", "R")

		## durum cipi: nokta + yazi
		(cx, cy, cw, ch) = self.__Anchor("status_chip", "L")
		self.chipDots = self.__DotSet(p, cx + 21 * self.k, cy + ch / 2.0)
		(tx, ty, tw, th) = self.__Anchor("status_text", "L")
		self.chipText = self.__Text(p, "", tx, ty + th / 2.0, 15)

		## sunucu satiri (panel icinde): nokta + ad + alt yazi + Degistir
		(dx, dy, dw, dh) = self.__Anchor("server_row", "R")
		self.rowDots = self.__DotSet(p, dx + 26 * self.k, dy + dh / 2.0)
		(nx, ny, nw, nh) = self.__Anchor("server_name", "R")
		self.rowName = self.__Text(p, "", nx, ny + 10 * self.k, 16)
		self.rowSub = self.__Text(p, "", nx, ny + 29 * self.k, 12, INK_DIM)
		self.btnChange = self.__Button(p, "btn_change", "R", self.__OnChange)

		## giris kutulari: intrologin'in gercek EditLine'lari buraya tasinir
		for (key, anchorName, holder) in (("id_edit", "uid", _Y(*YER_TUTUCU["id_edit"])), ("pwd_edit", "pwd", _Y(*YER_TUTUCU["pwd_edit"]))):
			ed = self.cb.get(key)
			if not ed:
				continue
			(ex, ey, ew, eh) = self.__Anchor(anchorName, "R")
			ed.SetParent(p)
			fs = max(8, int(round(17 * self.k)))
			ed.SetFontName("Tahoma:%d" % fs)
			ed.SetFontColor(INK[0], INK[1], INK[2])
			ed.SetPosition(int(round(ex + 46 * self.k)), int(round(ey + eh / 2.0 - fs * 0.62)))
			ed.SetSize(int(round(ew - 98 * self.k)), int(round(fs * 1.4)))
			try:
				ed.overLay.SetFontName("Tahoma:%d" % fs)
				ed.overLay.SetFontColor(0.45, 0.40, 0.33)
				ed.SetOverlayText(holder)
			except:
				pass
			ed.Show()
			## kutunun tamamina dokununca odak + telefon klavyesi; alan EditLine'in USTUNDE
			self.__ClickArea(p, ex, ey, ew - 52 * self.k, eh, lambda ed = ed: self.__FocusEdit(ed), True)
			self.editLines.append(ed)
		self.__Button(p, "btn_eye", "R", self.__OnEye)

		## "Hesabi kaydet" anahtari (yazisi panele gomulu; tum satir dokunulabilir)
		self.swOn = self.__Image(p, "sw_on", "R")
		self.swOff = self.__Image(p, "sw_off", "R")
		(rx, ry, rw, rh) = self.__Anchor("remember", "R")
		self.__ClickArea(p, rx, ry, rw, rh, self.__OnRemember)
		(sx, sy, sw2, sh2) = self.__Anchor("saved_count", "R")
		self.savedCount = self.__Text(p, "", sx + sw2, sy + sh2 / 2.0, 14, INK_DIM, "R")

		self.btnLogin = self.__Button(p, "btn_login", "R", self.__OnLogin)
		self.btnDelacc = self.__Button(p, "btn_delacc", "R", self.__OnDeleteAccount)

		## kayitli hesap cipleri
		(r0x, r0y, r0w, r0h) = SK.RECTS["acc_filled"]
		(b0x, b0y, b0w, b0h) = SK.ANCHORS["acc0"]
		padX = (b0x - r0x) * self.k
		padY = (b0y - r0y) * self.k
		for i in xrange(4):
			(ax, ay, aw, ah) = self.__Anchor("acc%d" % i, "R")
			btn = self.__Button(p, "acc_empty", "R", lambda i = i: self.__OnAccount(i), down = False,
				pos = (int(round(ax - padX)), int(round(ay - padY))))
			name = self.__Text(p, "", ax + aw / 2.0, ay + 22 * self.k, 14, INK, "C")
			sub = self.__Text(p, "", ax + aw / 2.0, ay + 40 * self.k, 11, INK_DIM, "C")
			self.accChips.append({"btn": btn, "name": name, "sub": sub, "id": "", "pwd": "", "vis": "acc_empty"})

		## KULLANICI (2026-10-06): giris ekranindaki ayar (muzik) dugmesi KALDIRILDI - muzik oyun ici Ayarlar'dan kapatilir
		## self.__Button(p, "btn_settings", "R", self.__OnSettings)
		self.__Button(p, "btn_exit", "R", self.__OnExit)
		self.__RefreshRemember()

	def __FocusEdit(self, ed):
		ed.SetFocus()
		try:
			import ime
			## -1 klavyeyi ACMAZ (native: yalniz piksel konumu "yaziya dokunuldu" sayilir); metin sonu
			ime.SetCursorPosition(100000)
		except:
			pass

	def OnUpdate(self):
		if self.root and self.serverScr and self.serverScr.IsShow() and getattr(self, "dilBayrak", None):
			self.__DilDondur()
		if not self.root or not self.loginScr or not self.loginScr.IsShow():
			return
		## ipucu yazisi: kutu doluysa gizli (SetText odaksizken ipucunu tazelemiyor - sifreyle ust uste binerdi)
		for ed in self.editLines:
			try:
				if len(ed.GetText()):
					if ed.overLay.IsShow():
						ed.overLay.Hide()
				elif not ed.overLay.IsShow():
					ed.overLay.Show()
			except:
				pass
		## kivilcimlar
		t = app.GetTime()
		for e in self.embers:
			ph = ((t - e["t0"]) % e["dur"]) / e["dur"]
			y = self.sh + 10 - ph * 640.0 * self.k
			x = e["x"] + ph * 40.0 * self.k
			e["img"].SetPosition(int(x), int(y))
			if hasattr(wndMgr, "SetDiffuseColor"):
				if ph < 0.1:
					a = ph / 0.1 * 0.9
				else:
					a = max(0.0, 0.9 * (1.0 - (ph - 0.1) / 0.9))
				wndMgr.SetDiffuseColor(e["img"].hWnd, 1.0, 1.0, 1.0, a)

	# --- giris olaylari
	def __OnChange(self):
		self.cb["open_server"]()

	def __OnEye(self):
		ed = self.cb.get("pwd_edit")
		if not ed:
			return
		self.pwdVisible = not self.pwdVisible
		ed.SetSecret(not self.pwdVisible)
		## SetSecret yalniz bayragi degistirir; ayni yaziyi tekrar vermek motorda "degismedi" sayilip yeniden
		## cizilmiyordu (KULLANICI 2026-10-06: "goz calismiyor") -> once bosaltip geri ver
		t = ed.GetText()
		ed.SetText("")
		ed.SetText(t)

	def __LoadRemember(self):
		try:
			return open(REMEMBER_FILE, "r").read().strip() != "0"
		except:
			return True

	def __OnRemember(self):
		self.remember = not self.remember
		try:
			open(REMEMBER_FILE, "w").write("1" if self.remember else "0")
		except:
			pass
		self.__RefreshRemember()

	def __RefreshRemember(self):
		if self.remember:
			self.swOn.Show()
			self.swOff.Hide()
		else:
			self.swOn.Hide()
			self.swOff.Show()

	def __ReadAccount(self, i):
		try:
			parts = open(ACCOUNT_FILE % (i + 1), "r").read().split("|")
			if len(parts) >= 3 and parts[1]:
				return (parts[1], parts[2])
		except:
			pass
		return ("", "")

	def RefreshAccounts(self):
		count = 0
		for i in xrange(4):
			(uid, pwd) = self.__ReadAccount(i)
			c = self.accChips[i]
			c["id"] = uid
			c["pwd"] = pwd
			if uid:
				count += 1
				vis = "acc_sel" if self.accountSel == i else "acc_filled"
				c["name"].SetText(uid)
				c["sub"].SetText(_Y("%d. hesap", "Account %d") % (i + 1))
			else:
				vis = "acc_empty"
				c["name"].SetText("")
				c["sub"].SetText("")
				if self.accountSel == i:
					self.accountSel = -1
			if c["vis"] != vis:
				c["btn"].SetUpVisual(_IP(vis + ".png"))
				c["btn"].SetOverVisual(_IP(vis + ".png"))
				c["btn"].SetDownVisual(_IP(vis + ".png"))
				c["vis"] = vis
			c["name"].SetTop()
			c["sub"].SetTop()
		self.savedCount.SetText(_Y("Kay\xfdtl\xfd: %d / 4", "Saved: %d / 4") % count)

	def __OnAccount(self, i):
		c = self.accChips[i]
		if not c["id"]:
			return
		self.accountSel = i
		if self.cb.get("id_edit"):
			self.cb["id_edit"].SetText(c["id"])
		if self.cb.get("pwd_edit"):
			self.cb["pwd_edit"].SetText(c["pwd"])
		self.RefreshAccounts()

	def __OnDeleteAccount(self):
		i = self.accountSel
		if i < 0 or not self.accChips[i]["id"]:
			self.cb["popup"](_Y("Silmek i\xe7in \xf6nce kay\xfdtl\xfd bir hesaba dokun.", "Tap a saved account first to delete it."))
			return
		try:
			open(ACCOUNT_FILE % (i + 1), "w").close()
		except:
			pass
		self.accountSel = -1
		self.RefreshAccounts()
		self.cb["popup"](localeInfo.ACCOUNT_DELETE_SUCCESS)

	def __OnLogin(self):
		idEd = self.cb.get("id_edit")
		pwdEd = self.cb.get("pwd_edit")
		uid = idEd.GetText() if idEd else ""
		pwd = pwdEd.GetText() if pwdEd else ""
		if self.remember and uid and pwd:
			slot = -1
			for i in xrange(4):
				if self.accChips[i]["id"] == uid:
					slot = i
					break
			if slot < 0:
				for i in xrange(4):
					if not self.accChips[i]["id"]:
						slot = i
						break
			if slot >= 0:
				try:
					open(ACCOUNT_FILE % (slot + 1), "w").write("|" + str(uid) + "|" + str(pwd) + "|")
				except:
					pass
				self.accountSel = slot
				self.RefreshAccounts()
		self.cb["login"]()

	def __OnSettings(self):
		## giris muzigini ac / kapat (giris ekraninda baska ayar yok).
		## ESKI HATA (KULLANICI 2026-10-06 "ayarlar calismiyor"): snd modulunde GetMusicVolume YOK (systemSetting'te);
		## istisna sessizce yutuluyordu -> dugme hicbir sey yapmiyordu. Durum kendi bayragimizda tutulur.
		try:
			if not getattr(self, "musicOff", False):
				self.musicOff = True
				snd.SetMusicVolume(0.0)
				self.cb["popup"](_Y("Giri\xfe m\xfczi\xf0i kapat\xfdld\xfd.", "Login music off."))
			else:
				self.musicOff = False
				v = 1.0
				try:
					v = systemSetting.GetMusicVolume() or 1.0
				except:
					pass
				snd.SetMusicVolume(v)
				self.cb["popup"](_Y("Giri\xfe m\xfczi\xf0i a\xe7\xfdld\xfd.", "Login music on."))
		except:
			import dbg, traceback
			dbg.TraceError("giris ayar dugmesi: " + traceback.format_exc())

	def __OnExit(self):
		self.cb["exit"]()

	def __CurrentServerChannel(self):
		name = "Averos2"
		ch = 0
		stateKey = ""
		try:
			sid = self.cb["server_id"]()
			cid = self.cb["channel_id"]()
			srv = serverInfo.REGION_DICT[0][sid]
			name = srv["name"]
			if cid in srv["channel"]:
				ch = cid
				stateKey = srv["channel"][cid]["state"]
		except:
			pass
		return (name, ch, stateKey)

	def RefreshLoginInfo(self):
		(name, ch, stateKey) = self.__CurrentServerChannel()
		if stateKey in STATE_MAP:
			(kind, label, pct) = STATE_MAP[stateKey]
			label = _Y(label, DURUM_EN.get(label, label))
			sub = _Y("%s yo\xf0unluk", "Load: %s") % label
		elif stateKey == "....":
			kind = "warn"
			label = _Y("Kontrol ediliyor", "Checking")
			sub = label
		else:
			kind = "full"
			label = _Y("Kapal\xfd", "Closed")
			sub = label
		self.__ShowDot(self.rowDots, kind)
		self.__ShowDot(self.chipDots, kind)
		if ch:
			self.rowName.SetText(_Y("%s \xb7 Kanal %d", "%s \xb7 Channel %d") % (name, ch))
			self.chipText.SetText("%s \xb7 CH%d \xb7 %s" % (name, ch, label))
		else:
			self.rowName.SetText(name)
			self.chipText.SetText(name)
		self.rowSub.SetText(sub)

	def ShowLogin(self):
		self.serverScr.Hide()
		self.loginScr.Show()
		self.RefreshAccounts()
		self.RefreshLoginInfo()

	# ------------------------------------------------------------------ SUNUCU / KANAL EKRANI
	def __BuildServer(self):
		p = self.serverScr
		self.__Background(p, "bg_server.jpg")
		self.srvPanelImg = self.__Image(p, "srv_panel", "L")
		self.chPanelImg = self.__Image(p, "ch_panel", "R")
		(tx, ty, tw, th) = self.__Anchor("srv_name_title", "R")
		self.chTitleXY = (tx, ty + th / 2.0)
		self.chTitle = self.__Text(p, "", tx + _Y(0, CH_BASLIK_EN_DX) * self.k, ty + th / 2.0, 22, INK)

		## duyurular
		(nx, ny, nw, nh) = self.__Anchor("news_list", "L")
		step = 20.0 * self.k
		self.newsText = []
		for (i, (date, text)) in enumerate(NEWS):
			en = i < len(NEWS_EN) and NEWS_EN[i] or text
			self.__Text(p, date, nx, ny + 8 * self.k + i * step, 13, INK_DIM)
			t = self.__Text(p, _Y(text, en), nx + 54 * self.k, ny + 8 * self.k + i * step, 13, INK)
			self.newsText.append((t, text, en))

		## sunucu kartlari (en fazla 4)
		(s0x, s0y, s0w, s0h) = SK.ANCHORS["srv0"]
		(s1x, s1y, s1w, s1h) = SK.ANCHORS["srv1"]
		(c0x, c0y, c0w, c0h) = SK.RECTS["srv_card"]
		self.srvStep = (s1y - s0y) * self.k
		em = SK.ANCHORS["srv0_emblem"]
		ti = SK.ANCHORS["srv0_title"]
		stt = SK.ANCHORS["srv0_state"]
		std = SK.ANCHORS["srv0_state_dot"]
		for i in xrange(4):
			oy = i * self.srvStep
			btn = self.__Button(p, "srv_card", "L", lambda i = i: self.__OnServerCard(i), down = False,
				pos = (int(round(self.X(c0x, "L"))), int(round(self.Y(c0y) + oy))))
			emb = self.__Text(p, "", self.X(em[0] + em[2] / 2.0, "L"), self.Y(em[1] + em[3] / 2.0) + oy, 20, BRONZE_HI, "C")
			## KULLANICI (2026-10-06): "A2" yazisi yerine oyunun simgesi (Averos2 sunucusunda)
			ikon = ui.ExpandedImageBox()
			ikon.SetParent(p)
			ikon.AddFlag("not_pick")
			ikon.LoadImage(_IP("srv_ikon.png"))
			ks = (em[2] + 4) * self.k / 144.0
			ikon.SetScale(ks, ks)
			ikon.SetPosition(int(round(self.X(em[0] - 2, "L"))), int(round(self.Y(em[1] - 2) + oy)))
			ikon.Hide()
			self.keep.append(ikon)
			title = self.__Text(p, "", self.X(ti[0], "L"), self.Y(ti[1] + 11) + oy, 18, INK)
			sub = self.__Text(p, "", self.X(ti[0], "L"), self.Y(ti[1] + 32) + oy, 12, INK_DIM)
			dots = self.__DotSet(p, self.X(std[0] + std[2] / 2.0, "L"), self.Y(std[1] + std[3] / 2.0) + oy)
			state = self.__Text(p, "", self.X(std[0] + std[2] + 8, "L"), self.Y(stt[1] + stt[3] / 2.0) + oy, 13, INK_DIM)
			self.srvCards.append({"btn": btn, "emb": emb, "ikon": ikon, "title": title, "sub": sub, "dots": dots,
				"state": state, "line": -1, "vis": "srv_card"})

		## kanal kartlari (2 sutun x 3 satir; ch4/ch5 tasarimda yok -> adimla turetilir)
		(h0x, h0y, h0w, h0h) = SK.ANCHORS["ch0"]
		(rcx, rcy, rcw, rch) = SK.RECTS["ch_card_sel"]
		nm = SK.ANCHORS["ch0_name"]
		dt = SK.ANCHORS["ch0_dot"]
		ld = SK.ANCHORS["ch0_load"]
		mt = SK.ANCHORS["ch0_meta"]
		h1x = SK.ANCHORS["ch1"][0]
		h2y = SK.ANCHORS["ch2"][1]
		for i in xrange(KANAL_KART):
			if SK.ANCHORS.has_key("ch%d" % i):
				(ax, ay, aw, ah) = SK.ANCHORS["ch%d" % i]
			else:
				(ax, ay, aw, ah) = (h0x + (i % 2) * (h1x - h0x), h0y + (i // 2) * (h2y - h0y), h0w, h0h)
			dx = ax - h0x
			dy = ay - h0y
			btn = self.__Button(p, "ch_card", "R", lambda i = i: self.__OnChannelCard(i), down = False,
				pos = (int(round(self.X(rcx + dx, "R"))), int(round(self.Y(rcy + dy)))))
			name = self.__Text(p, "", self.X(nm[0] + dx, "R"), self.Y(nm[1] + nm[3] / 2.0 + dy), 18, INK)
			dots = self.__DotSet(p, self.X(dt[0] + dt[2] / 2.0 + dx, "R"), self.Y(dt[1] + dt[3] / 2.0 + dy))
			fills = {}
			for kind in ("ok", "warn", "full"):
				img = ui.ExpandedImageBox()
				img.SetParent(p)
				img.AddFlag("not_pick")
				img.LoadImage(_IP("load_" + kind + ".png"))
				s = self.k / float(SK.TEX_SCALE)
				img.SetScale(s, s)
				img.SetPosition(int(round(self.X(ld[0] + dx, "R"))), int(round(self.Y(ld[1] + dy))))
				img.Hide()
				self.keep.append(img)
				fills[kind] = img
			stateT = self.__Text(p, "", self.X(mt[0] + dx, "R"), self.Y(mt[1] + mt[3] / 2.0 + dy), 12, INK_DIM)
			metaR = self.__Text(p, "", self.X(mt[0] + mt[2] + dx, "R"), self.Y(mt[1] + mt[3] / 2.0 + dy), 12, INK_DIM, "R")
			## v78: dolu kanal ortusu (kart gorselinin kendisi, siyah + yari saydam -> koseler kartla ayni)
			ortu = ui.ExpandedImageBox()
			ortu.SetParent(p)
			ortu.AddFlag("not_pick")
			ortu.LoadImage(_IP("ch_card.png"))
			os_ = self.k / float(SK.TEX_SCALE)
			ortu.SetScale(os_, os_)
			ortu.SetPosition(int(round(self.X(rcx + dx, "R"))), int(round(self.Y(rcy + dy))))
			wndMgr.SetDiffuseColor(ortu.hWnd, 0.0, 0.0, 0.0, DOLU_ORTU_ALFA)
			ortu.Hide()
			self.keep.append(ortu)
			self.chCards.append({"btn": btn, "name": name, "dots": dots, "fills": fills, "state": stateT,
				"meta": metaR, "line": -1, "vis": "ch_card", "ortu": ortu, "dolu": False})

		## KULLANICI (2026-09-16): kanal secim ekraninda Geri dugmesi YOK; devam dugmesinin yazisi
		## gorselin icinde (motor kalin/golgeli yazi cizemiyor) - kanala gore gorsel degisir.
		self.continueBtn = self.__Button(p, "btn_continue_1", "R", self.__OnContinue, rectName = "btn_continue")
		self.continueVis = "btn_continue_1"

		## KULLANICI (2026-10-06): DIL SECIMI karti - sunucu kartiyla Duyurular arasinda, sunucu kartiyla ayni gorsel.
		## Dokununca uidil penceresi (modal); hata sunucu ekranini bozmasin.
		try:
			self.__BuildDil(p)
		except:
			import dbg, traceback
			dbg.TraceError("dil karti: " + traceback.format_exc())

	DIL_KART = (82, 338, 444, 64)		# tasarim px (sunucu karti srv0 ile ayni x / genislik)

	def __BuildDil(self, p):
		(x, y, w, h) = self.DIL_KART
		k = self.k
		X = self.X(x, "L")
		Yy = self.Y(y)
		bg = ui.ExpandedImageBox()
		bg.SetParent(p)
		bg.AddFlag("not_pick")
		bg.LoadImage(_IP("srv_card.png"))
		bg.SetScale(w * k / 896.0, h * k / 164.0)
		bg.SetPosition(int(round(X)), int(round(Yy)))
		bg.Show()
		self.keep.append(bg)
		fr = ui.Bar()
		fr.SetParent(p)
		fr.AddFlag("not_pick")
		fr.SetColor(0xff6b5a3e)
		fr.SetPosition(int(round(X + 18 * k)), int(round(Yy + (h - 38) / 2.0 * k)))
		fr.SetSize(int(round(56 * k)), int(round(38 * k)))
		fr.Show()
		self.keep.append(fr)
		fl = ui.ExpandedImageBox()
		fl.SetParent(p)
		fl.AddFlag("not_pick")
		fl.Show()
		self.keep.append(fl)
		self.dilBayrak = fl
		self.dilBayrakPos = (int(round(X + 19 * k)), int(round(Yy + ((h - 38) / 2.0 + 1) * k)))
		self.__Text(p, "Dil \xb7 Language", X + 92 * k, Yy + 21 * k, 12, INK_DIM)
		self.dilAd = self.__Text(p, "", X + 92 * k, Yy + 43 * k, 18, INK)
		self.dilIpucu = self.__Text(p, "", X + (w - 20) * k, Yy + h / 2.0 * k, 14, BRONZE_HI, "R")
		self.__ClickArea(p, X, Yy, w * k, h * k, self.__OnDil, True)
		self.__DilYenile()

	def __DilBayrakKur(self, img, d):
		img.LoadImage("mobile/ui/dil/flag_%s.png" % d)
		if hasattr(wndMgr, "SetRenderingRectScaled"):
			wndMgr.SetRenderingRectScaled(img.hWnd, 1)	# LoadImage bayragi sifirlar: kirpma olcekli
		s = 54 * self.k / 144.0
		img.SetScale(s, s)

	def __DilSabitle(self, d):
		"""secili dilin bayragi sabit (animasyon durur); yalniz degisince calisir"""
		if getattr(self, "dilSabit", None) == d:
			return
		self.dilSabit = d
		self.dilDurum = None
		imgs = getattr(self, "dilImg", None)
		if imgs:
			for (k0, img) in imgs.items():
				img.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
				img.SetPosition(*self.dilBayrakPos)
				if k0 == d:
					img.Show()
				else:
					img.Hide()
			return
		self.__DilBayrakKur(self.dilBayrak, d)
		self.dilBayrak.SetPosition(*self.dilBayrakPos)
		self.dilBayrak.Show()

	def __DilDondur(self):
		## KULLANICI (2026-10-06): "bayrak otomatik degissin 2 sn'de bir, insanlar dil secim yerini gorsun" + "dil degismeyecek,
		## animasyon gibi" + "yana dogru diger bayrak gozukecek" -> YALNIZ GORSEL (secili dil degismez): bayrak 1.6 sn durur,
		## 0.4 sn'de sola kayarak cikar, digeri sagdan girer. Iki resim cerceve icinde kirpilir (RenderingRect), tasma yok.
		try:
			import dil
			if dil.Secildi():
				self.__DilSabitle(dil.Mevcut())		# oyuncu dilini sectiyse animasyon yok
				return
		except:
			pass
		self.dilSabit = None
		if not getattr(self, "dilBayrak2", None):
			try:
				b = ui.ExpandedImageBox()
				b.SetParent(self.serverScr)
				b.AddFlag("not_pick")
				b.Hide()
				self.keep.append(b)
				self.dilBayrak2 = b
				self.dilImg = {"tr": self.dilBayrak, "en": b}
				for (d, img) in self.dilImg.items():
					self.__DilBayrakKur(img, d)
				self.dilDurum = None
			except:
				self.dilBayrak2 = None
				return
		BEKLE, KAY = 1.6, 0.4
		T = BEKLE + KAY
		t = app.GetTime()
		n = int(t // T)
		f = (t - n * T - BEKLE) / KAY		# <0: bekleme, 0..1: kayma
		cur = "tr" if n % 2 == 0 else "en"
		nxt = "en" if cur == "tr" else "tr"
		(x0, y0) = self.dilBayrakPos
		W = int(round(54 * self.k))
		if f <= 0.0:
			if self.dilDurum == ("dur", cur):
				return
			self.dilDurum = ("dur", cur)
			a = self.dilImg[cur]
			a.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
			a.SetPosition(x0, y0)
			a.Show()
			self.dilImg[nxt].Hide()
			return
		f = min(1.0, f)
		f = f * f * (3.0 - 2.0 * f)		# yumusak hizlanma / yavaslama
		px = int(round(W * f))
		if self.dilDurum == ("kay", cur, px):
			return
		self.dilDurum = ("kay", cur, px)
		fr = px / float(W)
		a = self.dilImg[cur]			# cikan: sol parcasi kirpilir, sola kayar
		a.SetPosition(x0 - px, y0)
		a.SetRenderingRect(-fr, 0.0, 0.0, 0.0)
		a.Show()
		b = self.dilImg[nxt]			# giren: sag parcasi kirpilir, sagdan gelir
		b.SetPosition(x0 + W - px, y0)
		b.SetRenderingRect(0.0, 0.0, -(1.0 - fr), 0.0)
		if px > 0:
			b.Show()
		else:
			b.Hide()

	def __DilYenile(self, d = None):
		try:
			import dil
			d = dil.Mevcut() if dil.Secildi() else dil.Oneri()
			if not getattr(self, "dilBayrak2", None):
				self.dilBayrak.LoadImage("mobile/ui/dil/flag_%s.png" % d)
				s = 54 * self.k / 144.0
				self.dilBayrak.SetScale(s, s)
				self.dilBayrak.SetPosition(*self.dilBayrakPos)
			self.dilAd.SetText({"tr": "T\xfcrk\xe7e", "en": "English"}.get(d, d))
			self.dilIpucu.SetText({"tr": "De\xf0i\xfetir \x9b", "en": "Change \x9b"}.get(d, "\x9b"))
		except:
			import dbg, traceback
			dbg.TraceError("dil karti yenile: " + traceback.format_exc())

	def __DilSecildi(self, d = None):
		try:
			import dil
			dil.Uygula()		# oyun ici yazilar (localeInfo/uiScriptLocale) + gomulu yazi cevirisi yeni dile
		except:
			import dbg, traceback
			dbg.TraceError("dil.Uygula: " + traceback.format_exc())
		self.__DilYenile(d)
		self.__DilUygula()

	def __DilUygula(self):
		"""dil degisince yazili gorseller + kodla cizilen yazilar yeni dile doner (ekran yeniden kurulmaz)"""
		try:
			s = self.k / float(SK.TEX_SCALE)
			for (img, f) in ((self.srvPanelImg, "srv_panel.png"), (self.chPanelImg, "ch_panel.png")):
				img.LoadImage(_IP(f))
				img.SetScale(s, s)
			for (t, tr, en) in self.newsText:
				t.SetText(_Y(tr, en))
			(x, y) = self.chTitleXY
			self.chTitle.SetPosition(int(round(x + _Y(0, CH_BASLIK_EN_DX) * self.k)), int(round(y)))
			self.continueVis = None		# RefreshServer devam dugmesi gorselini yeniden yukler
			## giris ekrani (sunucu ekraniyla birlikte onceden kurulu)
			self.loginPanelImg.LoadImage(_IP("login_panel.png"))
			self.loginPanelImg.SetScale(s, s)
			for (btn, ad) in ((self.btnLogin, "btn_login"), (self.btnChange, "btn_change"), (self.btnDelacc, "btn_delacc")):
				btn.SetUpVisual(_IP(ad + ".png"))
				btn.SetOverVisual(_IP(ad + ".png"))
				btn.SetDownVisual(_IP(ad + "_down.png"))
			for (key, yazi) in YER_TUTUCU.items():
				ed = self.cb.get(key)
				if ed:
					try:
						ed.SetOverlayText(_Y(*yazi))
					except:
						pass
			for c in self.accChips:
				c["vis"] = None		# RefreshAccounts cip gorsellerini yeniden yukler
			self.RefreshAccounts()
			self.RefreshServer()
			self.RefreshLoginInfo()
		except:
			import dbg, traceback
			dbg.TraceError("dil uygula: " + traceback.format_exc())

	def __OnDil(self):
		try:
			import uidil
			uidil.Ac(ui.__mem_func__(self.__DilSecildi))
		except:
			import dbg, traceback
			dbg.TraceError("dil penceresi: " + traceback.format_exc())

	def __SetVis(self, card, vis):
		if card["vis"] != vis:
			card["btn"].SetUpVisual(_IP(vis + ".png"))
			card["btn"].SetOverVisual(_IP(vis + ".png"))
			card["btn"].SetDownVisual(_IP(vis + ".png"))
			card["vis"] = vis

	def RefreshServer(self):
		if not self.serverScr:
			return
		serverList = self.cb["server_list"]()
		selServer = self.cb["server_id"]()

		## sunucular: ListBox satirlari (keyDict: satir -> sunucu id); ayni adli tekrarlar gizlenir
		shown = []
		names = {}
		for line in sorted(serverList.keyDict.keys()):
			sid = serverList.keyDict[line]
			try:
				srv = serverInfo.REGION_DICT[0][sid]
			except:
				continue
			if srv["name"] in names and sid != selServer:
				continue
			names[srv["name"]] = 1
			shown.append((line, sid, srv))

		for (i, card) in enumerate(self.srvCards):
			if i >= len(shown):
				card["line"] = -1
				card["btn"].Hide()
				for w in (card["emb"], card["title"], card["sub"], card["state"]):
					w.Hide()
				if card.get("ikon"):
					card["ikon"].Hide()
				self.__ShowDot(card["dots"], None)
				continue
			(line, sid, srv) = shown[i]
			card["line"] = line
			card["btn"].Show()
			self.__SetVis(card, "srv_card_sel" if sid == selServer else "srv_card")
			nm = srv["name"]
			card["emb"].SetText("A2" if "averos" in nm.lower() else nm[:2].upper())
			if card.get("ikon"):
				if "averos" in nm.lower():
					card["emb"].Hide()
					card["ikon"].Show()
				else:
					card["ikon"].Hide()
			card["title"].SetText(nm)
			card["sub"].SetText(_Y(SERVER_SUBTITLE, SERVER_SUBTITLE_EN))
			states = [c.get("state", "") for c in srv["channel"].values()]
			anyOpen = len([s for s in states if s in STATE_MAP]) > 0
			checking = len([s for s in states if s == "...."]) > 0
			if anyOpen:
				self.__ShowDot(card["dots"], "ok")
				card["state"].SetText(_Y("A\xe7\xfdk", "Open"))
			elif checking:
				self.__ShowDot(card["dots"], "warn")
				card["state"].SetText(_Y("Kontrol", "Checking"))
			else:
				self.__ShowDot(card["dots"], "full")
				card["state"].SetText(_Y("Kapal\xfd", "Closed"))
			## v78: Averos2 kartinda simge varken "A2" yazisi GOSTERILMEZ (eskiden bu dongu yaziyi simgenin ustune
			## geri aciyor + SetTop ile one aliyordu: "A2" simgenin ustunde gorunuyordu)
			ikonda = bool(card.get("ikon")) and "averos" in nm.lower()
			for w in (card["emb"], card["title"], card["sub"], card["state"]):
				if ikonda and w is card["emb"]:
					w.Hide()
					continue
				w.Show()
				w.SetTop()
			for img in card["dots"].values():
				img.SetTop()

		try:
			self.chTitle.SetText(serverInfo.REGION_DICT[0][selServer]["name"])
		except:
			self.chTitle.SetText("")

		## kanallar
		channelList = self.cb["channel_list"]()
		selCh = self.cb["channel_id"]()
		lines = sorted(channelList.keyDict.keys())
		try:
			chDict = serverInfo.REGION_DICT[0][selServer]["channel"]
		except:
			chDict = {}
		for (i, card) in enumerate(self.chCards):
			if i >= len(lines):
				card["line"] = -1
				card["btn"].Hide()
				for w in (card["name"], card["state"], card["meta"]):
					w.Hide()
				self.__ShowDot(card["dots"], None)
				self.__ShowDot(card["fills"], None)
				if card.get("ortu"):
					card["ortu"].Hide()
				card["dolu"] = False
				continue
			line = lines[i]
			cid = channelList.keyDict[line]
			card["line"] = line
			card["btn"].Show()
			self.__SetVis(card, "ch_card_sel" if cid == selCh else "ch_card")
			stateKey = chDict.get(cid, {}).get("state", "")
			if stateKey in STATE_MAP:
				(kind, label, pct) = STATE_MAP[stateKey]
				label = _Y(label, DURUM_EN.get(label, label))
			elif stateKey == "....":
				kind = "warn"
				label = _Y("Kontrol ediliyor", "Checking")
				pct = 0.15
			else:
				kind = "full"
				label = _Y("Kapal\xfd", "Closed")
				pct = 1.0
			card["name"].SetText(_Y("Kanal %d", "Channel %d") % cid)
			card["state"].SetText(label)
			card["meta"].SetText(chDict.get(cid, {}).get("name", "CH%d" % cid))
			self.__ShowDot(card["dots"], kind)
			self.__ShowDot(card["fills"], kind)
			## RenderingRect olceksiz doku genisligiyle carpilir (cizim = doku*olcek + doku*r)
			card["fills"][kind].SetRenderingRect(0.0, 0.0, -(1.0 - pct) * (self.k / float(SK.TEX_SCALE)), 0.0)
			for w in (card["name"], card["state"], card["meta"]):
				w.Show()
				w.SetTop()
			for img in card["dots"].values() + card["fills"].values():
				img.SetTop()
			card["dolu"] = (stateKey == DOLU_DURUM)
			if card.get("ortu"):
				if card["dolu"]:
					card["ortu"].Show()
					card["ortu"].SetTop()
				else:
					card["ortu"].Hide()

		vis = "btn_continue_%d" % (selCh if 1 <= selCh <= KANAL_KART else 0)
		if vis != self.continueVis:
			self.continueBtn.SetUpVisual(_IP(vis + ".png"))
			self.continueBtn.SetOverVisual(_IP(vis + ".png"))
			self.continueBtn.SetDownVisual(_IP(vis + "_down.png"))
			self.continueVis = vis

	def __OnServerCard(self, i):
		card = self.srvCards[i]
		if card["line"] < 0:
			return
		self.cb["select_server_line"](card["line"])
		self.RefreshServer()

	def __OnChannelCard(self, i):
		card = self.chCards[i]
		if card["line"] < 0:
			return
		if card.get("dolu"):
			try:
				self.cb["popup"](_Y(DOLU_UYARI[0], DOLU_UYARI[1]))
			except:
				pass
			return
		self.cb["select_channel_line"](card["line"])
		self.RefreshServer()

	def __OnContinue(self):
		self.cb["continue"]()

	def ShowServer(self):
		self.loginScr.Hide()
		self.serverScr.Show()
		self.RefreshServer()

	def IsServerShown(self):
		return self.serverScr and self.serverScr.IsShow()
