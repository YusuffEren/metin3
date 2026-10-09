# H-HUD: mobil gorev cubugu yerlesimi (kaplama: mobile_root/uiscript/mobiletaskbar.py).
# PC'deki locale/tr/ui/TaskBar.py YERINE yalniz telefonda (ve M2_MOBILE_ROOT ile PC
# testinde) yuklenir. Konumlar onayli tasarim (sancak2_mobil_hud.html, 1356x610)
# yuzdeleri: x = W orani, y = H orani; boyutlar 705 px yukseklige gore pikseldir.
# Kok pencere tam ekran + "not_pick": kendisi tiklama YUTMAZ (CWindow::PickWindow
# once cocuklara bakar, FLAG_NOT_PICK olan kap NULL doner -> oyun penceresi alir).
import uiScriptLocale

W = SCREEN_WIDTH
H = SCREEN_HEIGHT
MU = "mobile/ui/"

def PX(p):
	return int(round(p * W))

def PY(p):
	return int(round(p * H))

# Yetenek yayi 6 kutu = gecerli sayfanin hizli slotlari 1 2 3 4 F1 F2 (yerel 0-5).
# KULLANICI (2026-09-13): 4 altin kure PC gorev cubugunun EXP kureleridir (EXPGauge_01..04),
# hizli slot DEGIL -> alttan dolar (PC uitaskbar.py SetExperience).
ARC = ((0.8547, 0.5443), (0.9078, 0.5049), (0.9609, 0.5230), (0.8201, 0.6443), (0.8127, 0.7607), (0.8296, 0.8787))
## KULLANICI (2026-10-09): "F1 F2 yazmasin, kac tane buton varsa 1 2 3 ... diye sirayla" -> 5, 6 (eklenenler 7..)
ARC_IMG = ("1", "2", "3", "4", "5", "6")
ARC_INDEX = (0, 1, 2, 3, 4, 5)
RING_ARC = 62
RING_GOLD = 46
ICON = 32

# Barlar: sol 0.087 W, genislik 0.184 W; 4 satir 12 px + 3 px bosluk. Mockup'taki
# ust (0.928 H) 4. satiri ekran disina tasirir (566+60 > 610) - alt kenara sigdirilir.
# KULLANICI (2026-09-13, arkadasinin client'i): barlar SOL ALT koseye yapisik ve kisa
# (4 kurenin toplam genisligi kadar), kureler birbirine yakin ve esit aralikli.
GOLD_GAP_X = 4
BAR_LEFT = PX(0.065)
BAR_W = 4 * RING_GOLD + 3 * GOLD_GAP_X		# 196 px
BAR_H = 12
BAR_GAP = 3
BAR_TOP = H - (3 * BAR_H + 2 * BAR_GAP) - 4	# 3 satir: HP / SP / Enerji
BAR_IMG_W = 289.0		# bar_bg.tga genisligi (telefon karesi 0.184*1568)

# EXP kureleri: KULLANICI (2026-09-13) - barlarin USTUNDE, sol/sag kenarlari barlarla
# ayni hizada, esit aralikli (onceden barlarin soluna tasiyordu).
GOLD_GAP = 6
GOLD_CY_PX = BAR_TOP - GOLD_GAP - RING_GOLD / 2
GOLD_STEP_PX = RING_GOLD + GOLD_GAP_X
GOLD = tuple(((BAR_LEFT + RING_GOLD / 2 + i * GOLD_STEP_PX) / float(W), GOLD_CY_PX / float(H)) for i in xrange(4))

# Kamera kaydirici: x 0.028-0.040 W (merkez 0.034), y 0.672-0.902 H
ZOOM_CX = PX(0.034)
ZOOM_TOP = PY(0.672) - 4

LABEL_FONT = "Tahoma:16"	# KULLANICI: yazilar okunmuyordu (10 -> 14; 2026-09-14: 16)
BAR_FONT = "Tahoma:14"	# 2026-09-14: 12 -> 14

def RingButton(name, image, cx, cy, size):
	return {
		"name" : name, "type" : "button",
		"x" : PX(cx) - size / 2, "y" : PY(cy) - size / 2,
		"default_image" : image, "over_image" : image, "down_image" : image,
	}

def IconSlot(name, index, cx, cy):
	return {
		"name" : name, "type" : "slot",
		"x" : PX(cx) - ICON / 2, "y" : PY(cy) - ICON / 2,
		"width" : ICON, "height" : ICON,
		"slot" : ({ "index" : index, "x" : 0, "y" : 0, "width" : ICON, "height" : ICON },),
	}

def Label(name, text, x, y):
	return {
		"name" : name, "type" : "text", "x" : x, "y" : y,
		"text" : text, "fontname" : LABEL_FONT, "outline" : 1,
		"text_horizontal_align" : "center",
		"r" : 0.945, "g" : 0.902, "b" : 0.784,
	}

def Bar(prefix, row, fill):
	y = BAR_TOP + row * (BAR_H + BAR_GAP)
	return {
		"name" : prefix + "Gauge_Board", "type" : "window",
		"x" : BAR_LEFT, "y" : y, "width" : BAR_W, "height" : BAR_H,
		"children" :
		(
			{
				"name" : prefix + "Gauge_Bg", "type" : "expanded_image", "x" : 0, "y" : 0,
				"image" : MU + "bar_bg.tga",
				"x_scale" : float(BAR_W) / BAR_IMG_W, "y_scale" : 1.0,
			},
			{
				# PC TaskBar.py HPRecoveryGaugeBar/SPRecoveryGaugeBar ile ayni tur/renk
				"name" : prefix + "RecoveryGaugeBar", "type" : "bar", "x" : 2, "y" : 2,
				"width" : BAR_W - 4, "height" : BAR_H - 4, "color" : 0x55ff0000,
			},
			{
				"name" : prefix + "Gauge", "type" : "expanded_image", "x" : 2, "y" : 2,
				"image" : MU + "bar_fill_" + fill + ".tga",
			},
			{
				# KULLANICI: HP/SP/Enerji yazisi cubugun ORTASINDA
				"name" : prefix + "Label", "type" : "text", "x" : BAR_W / 2, "y" : -2,
				"text" : "", "fontname" : BAR_FONT, "outline" : 1,
				"text_horizontal_align" : "center",
				"r" : 0.945, "g" : 0.902, "b" : 0.784,
			},
		),
	}

children = []

for i in xrange(len(ARC)):
	children.append(RingButton("arc_ring_%d" % i, MU + "slot_arc_%s.tga" % ARC_IMG[i], ARC[i][0], ARC[i][1], RING_ARC))
# KULLANICI (2026-09-24 gece): EXP kureleri + HP/SP/Enerji satirlari artik uimobilestatus.py (Durum HUD
# prototipi, mobile/ui/hud2) - uiscript'te yalniz yerlesim sabitleri kaldi.
for i in xrange(len(ARC)):
	children.append(IconSlot("arc_slot_%d" % i, ARC_INDEX[i], ARC[i][0], ARC[i][1]))

# Yerden al (Z) - cap 0.0623 H = 44 px
children.append({
	"name" : "PickButton", "type" : "button",
	"x" : PX(0.8768) - 22, "y" : PY(0.8836) - 22,
	"default_image" : MU + "btn_pick_up.tga", "over_image" : MU + "btn_pick_up.tga", "down_image" : MU + "btn_pick_down.tga",
})
children.append(Label("PickLabel", "Z", PX(0.8768), PY(0.8836) + 22 + 1))

# At (Ctrl+G) - cap 0.0852 H = 60 px
children.append({
	"name" : "HorseButton", "type" : "button",
	"x" : PX(0.9454) - 23, "y" : PY(0.3311) - 23,	# KULLANICI 2026-09-14: 64 -> 46 px
	"default_image" : MU + "hud_horse_up.tga", "over_image" : MU + "hud_horse_up.tga", "down_image" : MU + "hud_horse_down.tga",	# KULLANICI 2026-09-14: Unity at ikonu (2x, 0.5 olcek)
})
children.append(Label("HorseLabel", "At", PX(0.9454), PY(0.3311) + 23 + 1))

# Otomatik Av - KULLANICI (2026-09-15): At dugmesinin SOLUNDA, ayni boy (46 px), aralik 0.02 W;
# gorsel 128 px (hud_autohunt_*.tga, uitaskbar.py 46/128 olcekler), yesil = av suruyor (hud_autohunt_on)
AUTO_CX = 0.9454 - 0.02 - 46.0 / W
children.append({
	"name" : "AutoHuntButton", "type" : "button",
	"x" : PX(AUTO_CX) - 23, "y" : PY(0.3311) - 23,
	"default_image" : MU + "hud_autohunt_up.tga", "over_image" : MU + "hud_autohunt_up.tga", "down_image" : MU + "hud_autohunt_down.tga",
})
children.append(Label("AutoHuntLabel", "Oto Av", PX(AUTO_CX), PY(0.3311) + 23 + 1))

# Emoji - KULLANICI (2026-09-15): Oto Av'in SOLUNDA, ayni boy; basili tutup cekince emoji halkasi (uiemojiwheel.py)
EMOJI_CX = AUTO_CX - 0.02 - 46.0 / W
children.append({
	"name" : "EmojiButton", "type" : "expanded_image",
	"x" : PX(EMOJI_CX) - 23, "y" : PY(0.3311) - 23,
	"x_scale" : 46.0 / 128.0, "y_scale" : 46.0 / 128.0,
	"image" : MU + "hud_emoji_up.tga",
})
children.append(Label("EmojiLabel", "Emoji", PX(EMOJI_CX), PY(0.3311) + 23 + 1))

# HP / SP / Enerji + EXP kureleri: uimobilestatus.MobileStatusHud (uitaskbar.py kurar)

# Kamera kaydirici rayi (topuz uitaskbar.py icinde CameraKnob)
children.append({
	"name" : "ZoomTrack", "type" : "image",
	"x" : ZOOM_CX - 11, "y" : ZOOM_TOP,
	"image" : MU + "zoom_track.tga",
})

window = {
	"name" : "TaskBar",
	"x" : 0,
	"y" : 0,
	"width" : W,
	"height" : H,
	"style" : ("not_pick",),
	"children" : tuple(children),
}
