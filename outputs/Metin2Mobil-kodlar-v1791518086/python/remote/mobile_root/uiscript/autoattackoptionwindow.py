# MOBIL KAPLAMA (mobile_root/uiscript/autoattackoptionwindow.py): "metin2 otoav" paketi
# uiscript/autoattackoptionwindow.py'nin mobil kopyasi. KULLANICI (2026-09-15): "d:/ymir work/ui/game/auto_hunting/*.sub"
# gorselleri kaplanamaz -> mobile/ui/auto/*.tga; secenek satirlari 16 -> 24 px (uiauto AutoHuntingOptionWindow),
# seviye satiri 133 -> 190, pano 190 -> 276 yuksek, alt dugmeler 29 px. Pencere kok olceginde (1.6x) buyur.
import uiScriptLocale

AUTO_IMG = "mobile/ui/auto/"

BOARD_WIDTH						= 192
BOARD_HIGHT						= 276

PATTERN_PATH					= "d:/ymir work/ui/pattern/"
ACHIEV_LEFT_PATTERN_X_COUNT		= 8
ACHIEV_LEFT_PATTERN_Y_COUNT		= 12	# MOBIL: 6 -> 12 (26 + 12*16 = 218)
ACHIEV_PATTERN_X_COUNT			= 7
ACHIEV_PATTERN_Y_COUNT			= 12

BORDER_BOTTOM_Y					= 26 + ACHIEV_LEFT_PATTERN_Y_COUNT * 16	# 218
LEVEL_ROW_Y						= 190	# MOBIL: 7 satir x 24 + 20 -> 188
BOTTOM_BUTTON_Y					= BOARD_HIGHT - 37	# 29 px dugme + 8 kenar

window = {
	"name" : "AutoAttackOptionWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width"		: BOARD_WIDTH,
			"height"	: BOARD_HIGHT,

			"children" :
			(
				{ "name" : "auto_option_leftTop", "type" : "image", "style" : ("ltr",), "x" : 10, "y" : 10, "image" : PATTERN_PATH + "border_A_left_top.tga", },
				{ "name" : "auto_option_rightTop", "type" : "image", "style" : ("ltr",), "x" : 165, "y" : 10, "image" : PATTERN_PATH + "border_A_right_top.tga", },
				{ "name" : "auto_option_leftBottom", "type" : "image", "style" : ("ltr",), "x" : 10, "y" : BORDER_BOTTOM_Y, "image" : PATTERN_PATH + "border_A_left_bottom.tga", },
				{ "name" : "auto_option_rightBottom", "type" : "image", "style" : ("ltr",), "x" : 165, "y" : BORDER_BOTTOM_Y, "image" : PATTERN_PATH + "border_A_right_bottom.tga", },
				{ "name" : "auto_option_topCenterImg", "type" : "expanded_image", "style" : ("ltr",), "x" : 26, "y" : 10, "image" : PATTERN_PATH + "border_A_top.tga", "rect" : (0.0, 0.0, ACHIEV_LEFT_PATTERN_X_COUNT, 0), },
				{ "name" : "auto_option_leftCenterImg", "type" : "expanded_image", "style" : ("ltr",), "x" : 10, "y" : 26, "image" : PATTERN_PATH + "border_A_left.tga", "rect" : (0.0, 0.0, 0, ACHIEV_LEFT_PATTERN_Y_COUNT), },
				{ "name" : "auto_option_rightCenterImg", "type" : "expanded_image", "style" : ("ltr",), "x" : 165, "y" : 26, "image" : PATTERN_PATH + "border_A_right.tga", "rect" : (0.0, 0.0, 0, ACHIEV_LEFT_PATTERN_Y_COUNT), },
				{ "name" : "auto_option_bottomCenterImg", "type" : "expanded_image", "style" : ("ltr",), "x" : 26, "y" : BORDER_BOTTOM_Y, "image" : PATTERN_PATH + "border_A_bottom.tga", "rect" : (0.0, 0.0, ACHIEV_LEFT_PATTERN_X_COUNT, 0), },
				{ "name" : "auto_option_centerImg", "type" : "expanded_image", "style" : ("ltr",), "x" : 26, "y" : 26, "image" : PATTERN_PATH + "border_A_center.tga", "rect" : (0.0, 0.0, ACHIEV_PATTERN_X_COUNT, ACHIEV_PATTERN_Y_COUNT), },

				{
					"name" : "level_range",
					"type" : "image",

					"x" : 16,
					"y" : LEVEL_ROW_Y,

					"image" : AUTO_IMG + "auto_attack_level_range_back_img.tga",

					"children":
					(
						{
							"name" : "level_range_text",
							"type" : "text",

							"x" : 16,
							"y" : 0,

							"horizontal_align" : "left",
							"text" : uiScriptLocale.AUTO_OPTION_RANGE,
						},
					),
				},

				{
					"name" : "level_range_min_img",
					"type" : "image",

					"x" : 89,
					"y" : LEVEL_ROW_Y + 7,

					"image" : AUTO_IMG + "auto_attack_level_range_min_img.tga",
				},

				{
					"name" : "level_range_min",
					"type" : "image",

					"x" : 98,
					"y" : LEVEL_ROW_Y - 1,

					"image" : AUTO_IMG + "auto_attack_level_range_edit_img.tga",

					"children":
					(
						{
							"name" : "auto_attack_level_min",
							"type" : "editline",

							"x" : 3,
							"y" : 2,

							"input_limit" : 3,
							"only_number" : 1,

							"width" : 24,
							"height" : 16,
						},
					),
				},

				{
					"name" : "level_range_sign",
					"type" : "text",

					"x" : 126,
					"y" : LEVEL_ROW_Y,

					"text" : "~",
				},

				{
					"name" : "level_range_max_img",
					"type" : "image",

					"x" : 140,
					"y" : LEVEL_ROW_Y + 5,

					"image" : AUTO_IMG + "auto_attack_level_range_max_img.tga",
				},

				{
					"name" : "level_range_max",
					"type" : "image",

					"x" : 148,
					"y" : LEVEL_ROW_Y - 1,

					"image" : AUTO_IMG + "auto_attack_level_range_edit_img.tga",

					"children":
					(
						{
							"name" : "auto_attack_level_max",
							"type" : "editline",

							"x" : 3,
							"y" : 2,

							"input_limit" : 3,
							"only_number" : 1,

							"width" : 24,
							"height" : 16,
						},
					),
				},

				{
					"name" : "ClearButton",
					"type" : "button",

					"x" : 19,
					"y" : BOTTOM_BUTTON_Y,

					"text" : uiScriptLocale.AUTO_OPTION_CLEAR,

					"default_image" : AUTO_IMG + "auto_system_bottom_button_01.tga",
					"over_image" : AUTO_IMG + "auto_system_bottom_button_02.tga",
					"down_image" : AUTO_IMG + "auto_system_bottom_button_03.tga",
				},

				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : 97,
					"y" : BOTTOM_BUTTON_Y,

					"text" : uiScriptLocale.AUTO_OPTION_ACCEPT,

					"default_image" : AUTO_IMG + "auto_system_bottom_button_01.tga",
					"over_image" : AUTO_IMG + "auto_system_bottom_button_02.tga",
					"down_image" : AUTO_IMG + "auto_system_bottom_button_03.tga",
				},
			),
		},
	),
}
