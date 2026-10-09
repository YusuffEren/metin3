# H-HUD: mobil HUD dugmeleri (ust sag dizi, sol ust kume) - mobile_root/uiscript/mobilehud.py.
# Kok tam ekran + "not_pick" (bkz. mobiletaskbar.py). Konumlar onayli tasarim yuzdeleri.
# Metinler cp1254 (client yerel kod sayfasi) kacislariyla ASCII kaynak: \xfd=i-siz, \xb7=orta nokta.
import uiScriptLocale

W = SCREEN_WIDTH
H = SCREEN_HEIGHT
MU = "mobile/ui/"
LABEL_FONT = "Tahoma:16"	# KULLANICI: yazilar okunmuyordu (10 -> 14; 2026-09-14: 16)

def PX(p):
	return int(round(p * W))

def PY(p):
	return int(round(p * H))

# KULLANICI (2026-09-14): Unity projesindeki yuksek cozunurluklu ikonlar (hud_*.tga, 2x boyut;
# uimobilehud.py LoadWindow wndMgr.SetButtonScale 0.5 ile mantiksal boyuta indirir - cihazda keskin).
# Karakter/Envanter/Sohbet kalkan-kurdele ikonlari (etiket gorselde), digerleri bos-slot cercevesi + simge.
# KULLANICI (2026-09-14, duzeltme): Unity ust sirasi Metin2'nin GERCEK gorev cubugu ikonlarini kullanir
# (d:/ymir work/ui/game/taskbar/*_button_01..03.sub, 32 px; uimobilehud.py 1.875 olcek = 60) +
# sohbet balonu (hud_chat, Unity chatbtn_v2). Kalkan ikonlar (hud_chr/hud_inv) kullanilmiyor.
TB = "d:/ymir work/ui/game/taskbar/"

def SubButton(name, sub, cx, cy, size):
	return {
		"name" : name, "type" : "button",
		"x" : PX(cx) - size / 2, "y" : PY(cy) - size / 2,
		"default_image" : TB + sub + "_button_01.sub",
		"over_image" : TB + sub + "_button_02.sub",
		"down_image" : TB + sub + "_button_03.sub",
	}

def RoundButton(name, image, cx, cy, size):
	return {
		"name" : name, "type" : "button",
		"x" : PX(cx) - size / 2, "y" : PY(cy) - size / 2,
		"default_image" : MU + image + "_up.tga",
		"over_image" : MU + image + "_up.tga",
		"down_image" : MU + image + "_down.tga",
	}

def Label(name, text, cx, cy, size):
	return {
		"name" : name, "type" : "text",
		"x" : PX(cx) - 2, "y" : PY(cy) + size / 2 + 1,	# KULLANICI 2026-09-15: yazi 2 px sagda gorunuyordu
		"text" : text, "fontname" : LABEL_FONT, "outline" : 1,
		"text_horizontal_align" : "center",
		"r" : 0.945, "g" : 0.902, "b" : 0.784,
	}

MD = 46		# KULLANICI (2026-09-14): 60 -> 46 (Unity 32 birim ~43 px; "cok buyuk")
TINY = 23	# 0.0328 H
TOP_Y = 0.0623	# KULLANICI (2026-09-14): ust sag sira 0.045 W sola (EVENT/mini haritadan uzak)
# KULLANICI (2026-09-15): dugmeler arasi bosluk YARIYA (merkez araligi 0.0531 W -> 0.041 W), sira ayni merkezde (0.6293 W)
TOP_STEP = 0.044	# 2026-09-15: Kisayol/Menu yazilari degiyordu
TOP_X0 = 0.6293 - 3.5 * TOP_STEP	# 8 dugme (Menu eklendi 2026-09-15)

## KULLANICI (2026-09-28): "ust menu (karakter, envanter, kisayollar...) biraz saga, mini haritaya yaklassin".
## Sira artik SAG KENARA bagli (mini harita da saga bagli, boyu ekran YUKSEKLIGIyle olcekli): referans cihazda
## (2712x1220) merkez 0.6293 W -> 0.6793 W (+0.05 W); Menu merkezi sag kenardan 0.3705 H, adim 0.0978 H
## (= eski 0.044 W). Baska en/boy oraninda da mini haritaya ayni uzaklikta kalir.
TOP_RIGHT_H = 0.326		# 2026-09-28 2. tur: "biraz daha yaklastir" (0.3705 -> 0.326, ~54 px saga)
TOP_STEP_H = 0.0978

def TOP_X(i):
	return (W - (TOP_RIGHT_H + (7 - i) * TOP_STEP_H) * H) / float(W)
LEFT_Y = 0.135	# KULLANICI: sol ust kume buff ikon satirinin altina; 2026-09-13: +0.03 W saga (kose/kesikten uzak)

children = [
	# Sol ust kume (KULLANICI 2026-09-13: ESC kaldirildi; ekran goruntusu ve isimler koseden
	# saga alindi, digerleriyle ayni boy). Kamera deligi (sol kenar ~%4) disinda.
	# KULLANICI (2026-09-14): sol ust kume (Ekran / Isimler / Kamera) KALDIRILDI.
	# "Hedef" (en yakin hedef secme): gercek client'ta karsiligi YOK (yalniz chrmgr.GetPickedVID) -> konmadi.

	# Ust sag dizi 6 dugme
	# Ust sag sira (Unity sirasi): Sohbet, Karakter, Envanter, Arkadas, Sistem + bizim Menu
	# KULLANICI (2026-10-03): "Kisayol" dugmesi kaldirildi (kalici gizli, uimobilehud.py); soldaki 5 dugme bir saga
	# kaydi (Menu yerinde), bosluk kalmadi. Kayitli eski duzenler: uimobilelayout.py LAYOUT_VERSION 5 (ust sira atilir).
	RoundButton("ChatButton", "hud_chat", TOP_X(2), TOP_Y, MD),
	Label("ChatLabel", "Sohbet", TOP_X(2), TOP_Y, MD),
	SubButton("CharacterButton", "character", TOP_X(3), TOP_Y, MD),
	Label("CharacterLabel", "Karakter", TOP_X(3), TOP_Y, MD),
	SubButton("InventoryButton", "inventory", TOP_X(4), TOP_Y, MD),
	Label("InventoryLabel", "Envanter", TOP_X(4), TOP_Y, MD),
	SubButton("MessengerButton", "community", TOP_X(5), TOP_Y, MD),
	Label("MessengerLabel", "Arkada\xfe", TOP_X(5), TOP_Y, MD),
	SubButton("SystemButton", "system", TOP_X(6), TOP_Y, MD),
	Label("SystemLabel", "Ayarlar", TOP_X(6), TOP_Y, MD),
	# KULLANICI (2026-10-02): "Sil" kaldirildi (kalici gizli); 2026-10-03 "Kisayol" da (ikisi de Ayarlar'in altinda, gizli)
	RoundButton("DeleteItemButton", "hud_del", TOP_X(6), TOP_Y, MD),
	Label("DeleteItemLabel", "Sil", TOP_X(6), TOP_Y, MD),
	RoundButton("KeyPanelButton", "hud_keys", TOP_X(6), TOP_Y, MD),
	Label("KeyPanelLabel", "K\xfdsayol", TOP_X(6), TOP_Y, MD),
	# KULLANICI (2026-09-15): Menu (F5) kisayol panelinden ust siraya
	RoundButton("MenuButton", "hud_menu", TOP_X(7), TOP_Y, MD),
	Label("MenuLabel", "Men\xfc", TOP_X(7), TOP_Y, MD),
	# KULLANICI (2026-09-14): "Butonlari Gizle" - joystick, yetenek yayi, saldiri ve At DISINDA kalan
	# dugmeleri (ust sira + Yerden Al) gizler; dugmenin kendisi kalir ve "Goster" olur (uimobilehud.py).
	# KULLANICI (2026-09-15): Gizle dugmesi ekranin SOL UST kosesinde, yalniz ust sira dugmelerini gizler/gosterir
	# 2026-09-15: buff ikon satirinin (AffectShower 10,10 kok olcek -> y 16..56) ALTINA
	RoundButton("HideButton", "hud_hide", 0.075, 0.135, MD),
	Label("HideLabel", "Gizle", 0.075, 0.135, MD),

	# PC TaskBar API uyumu: interfacemodule.__MakeTaskBar bu dugmelere olay baglar
	# (BUTTON_MESSENGER / BUTTON_UMUT / BUTTON_ANTI_EXP); mobil tasarimda gorunmezler.
	{ "name" : "UmutBalikButton", "type" : "button", "x" : 0, "y" : 0 },
	{ "name" : "AntiexpButton", "type" : "button", "x" : 0, "y" : 0 },
]

window = {
	"name" : "MobileHud",
	"x" : 0,
	"y" : 0,
	"width" : W,
	"height" : H,
	"style" : ("not_pick",),
	"children" : tuple(children),
}
