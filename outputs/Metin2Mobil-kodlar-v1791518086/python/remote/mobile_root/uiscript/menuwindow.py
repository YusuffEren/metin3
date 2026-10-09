## MOBIL KAPLAMA (mobile_root/uiscript/menuwindow.py; pack uiscript/menuwindow.py yerine).
## KULLANICI (2026-10-03): Menu dugmesinin penceresi klasik yeniden tasarim - prototip A (Desktop/Averos2-HizliMenu-Prototip,
## "mukemmel oldu uygula"); baslik "F5 Hizli Menu" yerine "Averos2 Hizli Menu". Zemin + baslik serit oyunun klasik
## parcalari (ui.Board / ui.TitleBar, motor doser); 4 satir uimenu.py'de pisirilmis dugmeler (mobile/ui/hzm).
## Olculer pencere birimi: 304 x 280, serit (8, 8) 288 genis; satirlar (12, 40 + 58 i) 280 x 52.
## Metinler cp1254 kacisli ASCII kaynak: \xfd = i-siz, \xfc = u-noktali.
import uiScriptLocale

BOARD_WIDTH = 304
BOARD_HEIGHT = 280

window = {
	"name" : "MenuDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			(
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : BOARD_WIDTH - 16,
					"color" : "gray",

					"children" :
					(
						{ "name":"titlename", "type":"text", "x":0, "y":3,
						"text" : "Averos2 H\xfdzl\xfd Men\xfc",
						"horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},
			),
		},
	),
}
