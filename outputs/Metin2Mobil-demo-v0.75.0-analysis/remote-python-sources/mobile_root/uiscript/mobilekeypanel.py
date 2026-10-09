# H-HUD: KISAYOLLAR paneli (mobile_root/uiscript/mobilekeypanel.py).
# Onayli tasarim .panel: sol 0.3835 W, ust 0.1967 H, genislik 0.413 W; 8 sutun x 2 satir
# yuvarlak tus dugmesi (46 -> 53 px) + altinda etiket. Zemin gercek client ThinBoard.
# Tus -> islev eslemesi uimobilehud.py KeyPanel.LoadWindow'da (game.py __BuildKeyDict satirlari).
import uiScriptLocale

W = SCREEN_WIDTH
H = SCREEN_HEIGHT
MU = "mobile/ui/"
LABEL_FONT = "Tahoma:16"	# KULLANICI (2026-09-14): etiketler okunmuyordu (12 -> 16); panel 0.413 -> 0.50 W genisletildi

def PX(p):
	return int(round(p * W))

def PY(p):
	return int(round(p * H))

PW = PX(0.50)
PAD_X = 16
TITLE_Y = 12
TITLE_H = 17
BTN = 53
ROW1 = TITLE_Y + TITLE_H + 14
ROW_PITCH = BTN + 26
PH = ROW1 + 2 * ROW_PITCH - 22 + 16 + 12
COLS = 8
COL_W = (PW - 2 * PAD_X) / COLS

# (dosya adi, tus yazisi (gorselde), etiket)
KEYS = (
	("c", "Karakter"),
	("i", "Envanter"),
	("v", "Beceri"),
	("n", "G\xf6rev"),
	("b", "Duygu"),
	("g", "Lonca"),
	("m", "Harita"),
	("k", "\xd6zel Depo"),
	("l", "Sohbet Ge\xe7mi\xfei"),
	("h", "Yard\xfdm"),
	# ("f5", "Menu") -> KULLANICI 2026-09-15: ust siraya tasindi (MenuButton)
	# ("x", "Esya Sil") -> KULLANICI 2026-10-02: kaldirildi (toplu nesne islemleri yok)
	("alt", "\xddsimler"),
	("cq", "G\xf6rev D\xfc\xf0."),
	("cj", "At Komutlar\xfd"),
)

children = [
	{
		"name" : "board", "type" : "thinboard",
		"x" : 0, "y" : 0, "width" : PW, "height" : PH,
	},
	{
		"name" : "title", "type" : "image",
		"x" : (PW - 114) / 2, "y" : TITLE_Y,
		"image" : MU + "panel_title.tga",
	},
	{
		"name" : "CloseButton", "type" : "button",
		"x" : PW - 23 - 8, "y" : 8,
		"default_image" : MU + "tiny_close_up.tga",
		"over_image" : MU + "tiny_close_up.tga",
		"down_image" : MU + "tiny_close_down.tga",
	},
]

for i in xrange(len(KEYS)):
	fname, label = KEYS[i]
	col = i % COLS
	row = i / COLS
	x = PAD_X + col * COL_W + (COL_W - BTN) / 2
	y = ROW1 + row * ROW_PITCH
	children.append({
		"name" : "key_" + fname, "type" : "button",
		"x" : x, "y" : y,
		"default_image" : MU + "key_%s_up.tga" % fname,
		"over_image" : MU + "key_%s_up.tga" % fname,
		"down_image" : MU + "key_%s_down.tga" % fname,
	})
	children.append({
		"name" : "label_" + fname, "type" : "text",
		"x" : x + BTN / 2, "y" : y + BTN + 1,
		"text" : label, "fontname" : LABEL_FONT, "outline" : 1,
		"text_horizontal_align" : "center",
		"r" : 0.945, "g" : 0.902, "b" : 0.784,
	})

window = {
	"name" : "KeyPanel",
	"x" : PX(0.34),
	"y" : PY(0.1967),
	"width" : PW,
	"height" : PH,
	"children" : tuple(children),
}
