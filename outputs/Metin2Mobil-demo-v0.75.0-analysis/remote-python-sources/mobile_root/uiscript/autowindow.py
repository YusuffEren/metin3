# MOBIL KAPLAMA (mobile_root/uiscript/autowindow.py): "metin2 otoav" paketi uiscript/autowindow.py'nin mobil kopyasi.
# KULLANICI (2026-09-15): PC gorunumu korunur (Onizleme.jpg), dokunmaya uyarlandi:
#  - paketin "d:/ymir work/ui/game/..." .sub gorselleri kaplanamaz -> windows.dds'ten cikarilan mobile/ui/auto/*.tga
#  - pano 254x490 -> 264x514: ayar satirlari 27 -> 30 px araligi, alt dugmeler 29 px (uiauto SetButtonScale),
#    ok dugmeleri 18x25; pencere kok olceginde (M2_UI_SCALE, yuksekligi sigacak kadar ~1.37x) buyur
#  - metin cubuklari (Saldir/Odak/...) "button": satira dokunmak da acar/kapar (uiauto __MobileToggleRow)
#  - bekleme suresi kutulari dongu ile uretilir; editline hit alani kendi hucresine sinirli (paket 90 px tasiyordu)
import uiScriptLocale
import app

AUTO_IMG = "mobile/ui/auto/"

AUTO_UI_BOARD_WIDTH					= 264
ARROW_OUT_W						= 20	# ok dugmesi 11 px * 18/11 olcek = 18 px + 2
AUTO_UI_BOARD_HIGHT					= 514

ACTIVE_SKILL_SETTING_BAR_X			= 14
ACTIVE_SKILL_SETTING_BAR_Y			= 34
ACTIVE_SKILL_SETTING_BAR_WIDTH		= 233

CLEAR_BUTTON_X						= 213
CLEAR_BUTTON_Y						= 0

ACTIVE_SKILL_SETTING_TEXT_X			= 9
ACTIVE_SKILL_SETTING_TEXT_Y			= 2

ACTIVE_SKILL_SETTING_SLOT_X			= 15
ACTIVE_SKILL_SETTING_SLOT_Y			= 57

ACTIVE_SKILL_SETTING_SLOT_WIDTH		= 231
ACTIVE_SKILL_SETTING_SLOT_HEIGHT	= 241

SLOT_INDEX_INTERVAL_X				= 38
SLOT_INDEX_INTERVAL_Y				= 54
SLOT_INTERVAL_Y						= 29

SLOT_INDEX_WIDTH					= 32
SLOT_INDEX_HEIGHT					= 32

SLOT_COOL_TIME_BASE_X				= 15
SLOT_COOL_TIME_INTERVAL_X			= 38

SLOT_COOL_TIME_BASE_Y				= 89
SLOT_COOL_TIME_INTERVAL_Y			= 54
SLOT_COOL_TIME_LINE_INTERVAL_Y		= 83

SLOT_EDIT_LINE_X					= 3
SLOT_EDIT_LINE_Y					= 3
SLOT_EDIT_LINE_INPUT_LIMIT			= 4
SLOT_EDIT_LINE_ONLY_NUMBER			= 1
SLOT_EDIT_LINE_WIDTH				= 29	# MOBIL: hucre ici (paket 90: komsu hucrelere tasiyordu)
SLOT_EDIT_LINE_HEIGHT				= 15

POTION_SETTING_BAR_X				= 14
POTION_SETTING_BAR_Y				= 171
POTION_SETTING_BAR_WIDTH			= 233

POTION_SETTING_TEXT_X				= 9
POTION_SETTING_TEXT_Y				= 2

SETTING_BAR_X						= 14
SETTING_BAR_Y						= 308
SETTING_BAR_WIDTH					= 233

SETTING_AUTO_SETTING_TEXT_X			= 9
SETTING_AUTO_SETTING_TEXT_Y			= 2

SETTING_AUTO_BAR_X					= 3

SETTING_ROW_DY						= 30	# MOBIL: paket 27
SETTING_AUTO_ATTACK_BAR_Y			= 20
SETTING_AUTO_RANGE_BAR_Y			= SETTING_AUTO_ATTACK_BAR_Y + SETTING_ROW_DY
SETTING_AUTO_POTION_BAR_Y			= SETTING_AUTO_ATTACK_BAR_Y + SETTING_ROW_DY * 2
SETTING_AUTO_SKILL_BAR_Y			= SETTING_AUTO_ATTACK_BAR_Y + SETTING_ROW_DY * 3
SETTING_AUTO_RESTART_BAR_Y			= SETTING_AUTO_ATTACK_BAR_Y + SETTING_ROW_DY * 4

AUTO_BUTTON_X						= 196
AUTO_BUTTON_BASE_Y					= 325	# MOBIL: 26 px dugme, 18 px cubukla ortali
AUTO_BUTTON_ADD_Y					= SETTING_ROW_DY
AUTO_OPTION_BUTTON_DX				= 46	# MOBIL: 43 px dugme + 3 bosluk (ok dugmesi 18 px olcekli)

AUTO_BOTTOM_BUTTON_Y				= 478	# MOBIL: 29 px yukseklik (SetButtonScale)
AUTO_SAVE_BUTTON_X					= 10
AUTO_SAVE_BUTTON_Y					= AUTO_BOTTOM_BUTTON_Y

AUTO_START_BUTTON_X					= 93
AUTO_START_BUTTON_Y					= AUTO_BOTTOM_BUTTON_Y

AUTO_END_BUTTON_X					= 176
AUTO_END_BUTTON_Y					= AUTO_BOTTOM_BUTTON_Y

AUTO_TOOLTIP_BUTTON_X				= 22	# KULLANICI 2026-09-15: "?" basligin SOLUNA yakin (onceki 176, sag)
AUTO_TOOLTIP_BUTTON_Y				= 5	# KULLANICI 2026-09-15: carpi dugmesi gibi basligin icinde dikey ortali (onceki 8)

BOTTOM_BUTTON_IMG = (AUTO_IMG + "auto_system_bottom_button_01.tga", AUTO_IMG + "auto_system_bottom_button_02.tga", AUTO_IMG + "auto_system_bottom_button_03.tga")
CLEAR_BUTTON_IMG = (AUTO_IMG + "yenile_up.tga", AUTO_IMG + "yenile_over.tga", AUTO_IMG + "yenile_down.tga")	# KULLANICI 2026-09-15: masaustu yenile.png (64 px, uiauto 21 px olcek + nabiz animasyonu)
OPTION_BUTTON_IMG = (AUTO_IMG + "ac_up.tga", AUTO_IMG + "ac_over.tga", AUTO_IMG + "ac_down.tga")	# KULLANICI 2026-09-15: masaustu "ac" (36x50 doku, uiauto 0.5 olcek = 18x25)
SMALL_BUTTON_IMG = ("d:/ymir work/ui/public/Small_Button_01.sub", "d:/ymir work/ui/public/Small_Button_02.sub", "d:/ymir work/ui/public/Small_Button_03.sub")

def ImgButton(name, x, y, imgs, text = None):
	d = {
		"name" : name, "type" : "button",
		"x" : x, "y" : y,
		"default_image" : imgs[0], "over_image" : imgs[1], "down_image" : imgs[2],
	}
	if text is not None:
		d["text"] = text
	return d

def ToggleButton(name, x, y):
	return {
		"name" : name, "type" : "toggle_button",
		"x" : x, "y" : y,
		"text" : uiScriptLocale.AUTO_OFF,
		"default_image" : SMALL_BUTTON_IMG[0], "over_image" : SMALL_BUTTON_IMG[1], "down_image" : SMALL_BUTTON_IMG[2],
	}

# MOBIL: metin cubugu = dugme (satira dokunma acar/kapar); yazi dugme ortasinda
def TextBar(name, y, img, text):
	return {
		"name" : name, "type" : "button",
		"x" : SETTING_AUTO_BAR_X, "y" : y,
		"default_image" : img, "over_image" : img, "down_image" : img,
		"text" : text,
	}

def CoolTimeCell(idx, x, y):
	return {
		"name" : "cool_time_Image%d" % idx, "type" : "image",
		"x" : x, "y" : y,
		"image" : AUTO_IMG + "auto_system_edit_line.tga",
		"children" :
		(
			{
				"name" : "editline%d" % idx, "type" : "editline",
				"x" : SLOT_EDIT_LINE_X, "y" : SLOT_EDIT_LINE_Y,
				"input_limit" : SLOT_EDIT_LINE_INPUT_LIMIT,
				"only_number" : SLOT_EDIT_LINE_ONLY_NUMBER,
				"width" : SLOT_EDIT_LINE_WIDTH, "height" : SLOT_EDIT_LINE_HEIGHT,
			},
		),
	}

def Slot(index, col, row_y):
	return { "index" : index, "x" : SLOT_INDEX_INTERVAL_X * col, "y" : row_y, "width" : SLOT_INDEX_WIDTH, "height" : SLOT_INDEX_HEIGHT }

# Kutular: 0-11 beceri (2 satir), 13-24 iksir (2 satir); 12 ayrilmis (paket ile ayni)
slotList = []
for col in xrange(6):
	slotList.append(Slot(col, col, 0))
for col in xrange(6):
	slotList.append(Slot(6 + col, col, SLOT_INDEX_INTERVAL_Y))
for col in xrange(6):
	slotList.append(Slot(13 + col, col, SLOT_INTERVAL_Y + (SLOT_INDEX_INTERVAL_Y * 2)))
for col in xrange(6):
	slotList.append(Slot(19 + col, col, SLOT_INTERVAL_Y + (SLOT_INDEX_INTERVAL_Y * 3)))

# Bekleme suresi kutulari (4 satir x 6): satir y'leri paket ile ayni
coolRowY = (
	SLOT_COOL_TIME_BASE_Y,
	SLOT_COOL_TIME_BASE_Y + SLOT_COOL_TIME_INTERVAL_Y,
	SLOT_COOL_TIME_BASE_Y + SLOT_COOL_TIME_INTERVAL_Y + SLOT_COOL_TIME_LINE_INTERVAL_Y,
	SLOT_COOL_TIME_BASE_Y + (SLOT_COOL_TIME_INTERVAL_Y * 2) + SLOT_COOL_TIME_LINE_INTERVAL_Y,
)
coolCells = []
for row in xrange(4):
	for col in xrange(6):
		coolCells.append(CoolTimeCell(row * 6 + col, SLOT_COOL_TIME_BASE_X + (SLOT_COOL_TIME_INTERVAL_X * col), coolRowY[row]))

boardChildren = [
	{
		"name" : "SkillSettingBar",
		"type" : "horizontalbar",

		"x" : ACTIVE_SKILL_SETTING_BAR_X,
		"y" : ACTIVE_SKILL_SETTING_BAR_Y,

		"width" : ACTIVE_SKILL_SETTING_BAR_WIDTH,

		"children":
		(
			{
				"name" : "BaseInfo_1",
				"type" : "text",

				"x" : ACTIVE_SKILL_SETTING_TEXT_X,
				"y" : ACTIVE_SKILL_SETTING_TEXT_Y,

				"text" : uiScriptLocale.AUTO_SKILL_SETTING,
			},

			ImgButton("AutoSkillClearButton", CLEAR_BUTTON_X, CLEAR_BUTTON_Y, CLEAR_BUTTON_IMG),
		),
	},

	{
		"name" : "Auto_Active_Skill_Slot_Table",
		"type" : "slot",

		"x" : ACTIVE_SKILL_SETTING_SLOT_X,
		"y" : ACTIVE_SKILL_SETTING_SLOT_Y,

		"width" : ACTIVE_SKILL_SETTING_SLOT_WIDTH,
		"height" : ACTIVE_SKILL_SETTING_SLOT_HEIGHT,

		"image" : "d:/ymir work/ui/public/Slot_Base.sub",

		"slot" : tuple(slotList),
	},
]

boardChildren.extend(coolCells)

boardChildren.extend([
	{
		"name" : "PotionSettingBar",
		"type" : "horizontalbar",

		"x" : POTION_SETTING_BAR_X,
		"y" : POTION_SETTING_BAR_Y,

		"width" : POTION_SETTING_BAR_WIDTH,

		"children":
		(
			{
				"name" : "BaseInfo_2",
				"type" : "text",

				"x" : POTION_SETTING_TEXT_X,
				"y" : POTION_SETTING_TEXT_Y,

				"text" : uiScriptLocale.AUTO_POTION_SETTING,
			},

			ImgButton("AutoPotionClearButton", CLEAR_BUTTON_X, CLEAR_BUTTON_Y, CLEAR_BUTTON_IMG),
		),
	},

	{
		"name" : "AutoSettingBar",
		"type" : "horizontalbar",

		"x" : SETTING_BAR_X,
		"y" : SETTING_BAR_Y,

		"width" : SETTING_BAR_WIDTH,

		"children":
		(
			{
				"name" : "BaseInfo_3",
				"type" : "text",

				"x" : SETTING_AUTO_SETTING_TEXT_X,
				"y" : SETTING_AUTO_SETTING_TEXT_Y,

				"text" : uiScriptLocale.AUTO_SETTING,
			},

			TextBar("attack_text_bar", SETTING_AUTO_ATTACK_BAR_Y, AUTO_IMG + "auto_system_text_bar_01.tga", uiScriptLocale.AUTO_AUTO_ATTACK),
			TextBar("range_text_bar", SETTING_AUTO_RANGE_BAR_Y, AUTO_IMG + "auto_system_text_bar_01.tga", uiScriptLocale.AUTO_AUTO_RANGE),
			TextBar("potion_text_bar", SETTING_AUTO_POTION_BAR_Y, AUTO_IMG + "auto_system_text_bar_02.tga", uiScriptLocale.AUTO_AUTO_POTION),
			TextBar("skill_text_bar", SETTING_AUTO_SKILL_BAR_Y, AUTO_IMG + "auto_system_text_bar_02.tga", uiScriptLocale.AUTO_AUTO_SKILL),
			TextBar("restart_text_bar", SETTING_AUTO_RESTART_BAR_Y, AUTO_IMG + "auto_system_text_bar_02.tga", uiScriptLocale.AUTO_AUTO_RESTART),
		),
	},

	ToggleButton("AutoAttackButton", AUTO_BUTTON_X, AUTO_BUTTON_BASE_Y),

	ToggleButton("AutoRangeButton", AUTO_BUTTON_X, AUTO_BUTTON_BASE_Y + AUTO_BUTTON_ADD_Y),

	ToggleButton("AutoPotionButton", AUTO_BUTTON_X, AUTO_BUTTON_BASE_Y + (AUTO_BUTTON_ADD_Y * 2)),
	ToggleButton("AutoSkillButton", AUTO_BUTTON_X, AUTO_BUTTON_BASE_Y + (AUTO_BUTTON_ADD_Y * 3)),
	ToggleButton("AutoRestartHereButton", AUTO_BUTTON_X, AUTO_BUTTON_BASE_Y + (AUTO_BUTTON_ADD_Y * 4)),

	ImgButton("AutoSaveOnButton", AUTO_SAVE_BUTTON_X, AUTO_SAVE_BUTTON_Y, BOTTOM_BUTTON_IMG, uiScriptLocale.AUTO_SAVE),
	ImgButton("AutoStartOnButton", AUTO_START_BUTTON_X, AUTO_START_BUTTON_Y, BOTTOM_BUTTON_IMG, uiScriptLocale.AUTO_START),
	ImgButton("AutoStartOffButton", AUTO_END_BUTTON_X, AUTO_END_BUTTON_Y, BOTTOM_BUTTON_IMG, uiScriptLocale.AUTO_END),

	{
		"name" : "AutoToolTipButton",
		"type" : "button",

		"x" : AUTO_TOOLTIP_BUTTON_X,
		"y" : AUTO_TOOLTIP_BUTTON_Y,

		"default_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
		"over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
		"down_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
	},

	ImgButton("AutoAllClearButton", SETTING_BAR_X + CLEAR_BUTTON_X, SETTING_BAR_Y + CLEAR_BUTTON_Y, CLEAR_BUTTON_IMG),
])

window = {
	"name" : "AutoWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : AUTO_UI_BOARD_WIDTH + ARROW_OUT_W,	# KULLANICI 2026-09-15: ok dugmeleri cercevenin DISINDA (sag)
	"height" : AUTO_UI_BOARD_HIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : AUTO_UI_BOARD_WIDTH,
			"height" : AUTO_UI_BOARD_HIGHT,

			"title" : uiScriptLocale.AUTO_TITLE,

			"children" : tuple(boardChildren),
		},
		## KULLANICI (2026-09-15): Saldir/Odak ok dugmeleri ayni yukseklikte, sag cerceveye DISARIDAN yapisik
		ImgButton("AutoAttackOptionButton", AUTO_UI_BOARD_WIDTH, AUTO_BUTTON_BASE_Y, OPTION_BUTTON_IMG),
		ImgButton("AutoRangeSelectButton", AUTO_UI_BOARD_WIDTH, AUTO_BUTTON_BASE_Y + AUTO_BUTTON_ADD_Y, OPTION_BUTTON_IMG),
	),
}
