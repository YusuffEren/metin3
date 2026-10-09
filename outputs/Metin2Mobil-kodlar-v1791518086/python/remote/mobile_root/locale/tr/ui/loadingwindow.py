# MOBIL KAPLAMA: locale/tr/ui/LoadingWindow.py (pack surumu PC'de degismez).
# KULLANICI (2026-09-24): yeni yukleme ekrani (Desktop/Metin2-Loading-Ekrani) - gorseller ve
# animasyon uimobileloading.py'de kurulur; bu betik yalniz introloading.py'nin bekledigi
# iskeleti (BackGround / ErrorMessage / GageBoard-FullGage) verir, HICBIR doku yuklemez.
import uiScriptLocale

W = SCREEN_WIDTH
H = SCREEN_HEIGHT

window = {
	"name" : "LoginWindow",
	"sytle" : ("movable",),

	"x" : 0,
	"y" : 0,

	"width" : W,
	"height" : H,

	"children" :
	(
		{
			"name" : "BackGround",
			"type" : "window",
			"x" : 0,
			"y" : 0,
			"width" : W,
			"height" : H,
		},
		{
			"name":"ErrorMessage",
			"type":"text", "x":10, "y":10,
			"text": uiScriptLocale.LOAD_ERROR,
		},
		{
			"name" : "GageBoard",
			"type" : "window",
			"x" : 0,
			"y" : 0,
			"width" : 1,
			"height": 1,

			"children" :
			(
				{
					"name" : "FullGage",
					"type" : "window",
					"x" : 0,
					"y" : 0,
					"width" : 1,
					"height": 1,
				},
			),
		},
	),
}
