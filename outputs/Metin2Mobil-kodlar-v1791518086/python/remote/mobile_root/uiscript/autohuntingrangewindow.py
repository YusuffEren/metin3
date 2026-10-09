# MOBIL KAPLAMA (mobile_root/uiscript/autohuntingrangewindow.py): "metin2 otoav" paketi
# uiscript/autohuntingrangewindow.py'nin mobil kopyasi. KULLANICI (2026-09-15): "d:/ymir work/ui/game/windows/*.sub"
# gorselleri kaplanamaz -> mobile/ui/auto/*.tga; pano 230x110 -> 260x118; kaydiricinin iki yaninda -/+ dugmeleri
# (mobile/ui/edit_coin_*.tga, uiauto OnClickStep 5 m adim; kaydirici topuzu parmak icin kucuk); Onayla 29 px.
import uiScriptLocale

AUTO_IMG = "mobile/ui/auto/"
MU = "mobile/ui/"

BOARD_WIDTH						= 260
BOARD_HIGHT						= 118

PATTERN_PATH					= "d:/ymir work/ui/pattern/"
ACHIEV_LEFT_PATTERN_X_COUNT		= 12	# MOBIL: 10 -> 12 (26 + 12*16 = 218 < 230)
ACHIEV_LEFT_PATTERN_Y_COUNT		= 2	# MOBIL: 1 -> 2 (26..58; alt kenar 66)
ACHIEV_PATTERN_X_COUNT			= 12
ACHIEV_PATTERN_Y_COUNT			= 2

BORDER_RIGHT_X					= BOARD_WIDTH - 30	# 230
BORDER_BOTTOM_Y					= 66
SLIDER_Y						= 25
STEP_BUTTON						= 28	# MOBIL: 128 px para dugmesi 28/128 olcekli (uiauto)

window = {
	"name" : "AutoHuntingRangeWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("float",),

	"width"		: BOARD_WIDTH,
	"height"	: BOARD_HIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HIGHT,

			"title" : uiScriptLocale.AUTO_TITLE,

			"children" :
			(
				{ "name" : "auto_option_leftTop", "type" : "image", "style" : ("ltr",), "x" : 10, "y" : 10, "image" : PATTERN_PATH + "border_A_left_top.tga", },
				{ "name" : "auto_option_rightTop", "type" : "image", "style" : ("ltr",), "x" : BORDER_RIGHT_X, "y" : 10, "image" : PATTERN_PATH + "border_A_right_top.tga", },
				{ "name" : "auto_option_leftBottom", "type" : "image", "style" : ("ltr",), "x" : 10, "y" : BORDER_BOTTOM_Y, "image" : PATTERN_PATH + "border_A_left_bottom.tga", },
				{ "name" : "auto_option_rightBottom", "type" : "image", "style" : ("ltr",), "x" : BORDER_RIGHT_X, "y" : BORDER_BOTTOM_Y, "image" : PATTERN_PATH + "border_A_right_bottom.tga", },
				{ "name" : "auto_option_topCenterImg", "type" : "expanded_image", "style" : ("ltr",), "x" : 26, "y" : 10, "image" : PATTERN_PATH + "border_A_top.tga", "rect" : (0.0, 0.0, ACHIEV_LEFT_PATTERN_X_COUNT, 0), },
				{ "name" : "auto_option_leftCenterImg", "type" : "expanded_image", "style" : ("ltr",), "x" : 10, "y" : 26, "image" : PATTERN_PATH + "border_A_left.tga", "rect" : (0.0, 0.0, 0, ACHIEV_LEFT_PATTERN_Y_COUNT), },
				{ "name" : "auto_option_rightCenterImg", "type" : "expanded_image", "style" : ("ltr",), "x" : BORDER_RIGHT_X, "y" : 26, "image" : PATTERN_PATH + "border_A_right.tga", "rect" : (0.0, 0.0, 0, ACHIEV_LEFT_PATTERN_Y_COUNT), },
				{ "name" : "auto_option_bottomCenterImg", "type" : "expanded_image", "style" : ("ltr",), "x" : 26, "y" : BORDER_BOTTOM_Y, "image" : PATTERN_PATH + "border_A_bottom.tga", "rect" : (0.0, 0.0, ACHIEV_LEFT_PATTERN_X_COUNT, 0), },
				{ "name" : "auto_option_centerImg", "type" : "expanded_image", "style" : ("ltr",), "x" : 26, "y" : 26, "image" : PATTERN_PATH + "border_A_center.tga", "rect" : (0.0, 0.0, ACHIEV_PATTERN_X_COUNT, ACHIEV_PATTERN_Y_COUNT), },

				{
					"name" : "hunting_range_sliderbar",
					"type" : "sliderbar",

					"x" : 0,
					"y" : SLIDER_Y,

					"horizontal_align" : "center",
				},

				# MOBIL: -/+ dugmeleri (kaydiricinin solu/sagi; 175 px kaydirici ortada -> 42..217)
				{
					"name" : "RangeMinusButton",
					"type" : "button",

					"x" : 8,
					"y" : SLIDER_Y + 6 - STEP_BUTTON // 2,

					"default_image" : MU + "edit_coin_minus_up.tga",
					"over_image" : MU + "edit_coin_minus_up.tga",
					"down_image" : MU + "edit_coin_minus_down.tga",
				},
				{
					"name" : "RangePlusButton",
					"type" : "button",

					"x" : BOARD_WIDTH - 8 - STEP_BUTTON,
					"y" : SLIDER_Y + 6 - STEP_BUTTON // 2,

					"default_image" : MU + "edit_coin_plus_up.tga",
					"over_image" : MU + "edit_coin_plus_up.tga",
					"down_image" : MU + "edit_coin_plus_down.tga",
				},

				{
					"name" : "range_back_ui",
					"type" : "image",

					"x" : 0,
					"y" : SLIDER_Y + 20,

					"horizontal_align" : "center",
					"image" : AUTO_IMG + "auto_system_edit_line.tga",

					"children":
					(
						{
							"name" : "range_text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",
						},
					),
				},

				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : 0,
					"y" : BOARD_HIGHT - 37,

					"horizontal_align" : "center",

					"text" : uiScriptLocale.AUTO_RANGE_ACCEPT,

					"default_image" : AUTO_IMG + "auto_system_bottom_button_01.tga",
					"over_image" : AUTO_IMG + "auto_system_bottom_button_02.tga",
					"down_image" : AUTO_IMG + "auto_system_bottom_button_03.tga",
				},
			),
		},
	),
}
