# MOBIL KAPLAMA (mobile_root/locale/tr/ui/systemdialog.py): pack kopyasi + "Butonlari Ozellestir" dugmesi
# (KULLANICI 2026-09-14, Unity Metin2SystemMenu gibi). Yukseklik 288 -> 318.
# MOBIL GRAFIK AYARLARI (KULLANICI 2026-10-07): "Sistem Secenekleri" ile "Oyun Secenekleri" ARASINA "Grafik Ayarlari"
# (uisystem.py -> uigrafik.Ac); alttaki dugmeler 30 px asagi, pencere 348 -> 378 ve tam ortali (motor ortalar + sigdirir).
import uiScriptLocale

ROOT = "d:/ymir work/ui/public/"

try:
	import dil
	_GRAFIK = "Graphics Settings" if dil.Mevcut() == "en" else "Grafik Ayarlar\xfd"
except:
	_GRAFIK = "Grafik Ayarlar\xfd"

window = {
	"name" : "SystemDialog",
	"style" : ("float",),

	"x" : (SCREEN_WIDTH  - 200) /2,
	"y" : (SCREEN_HEIGHT - 378) /2,

	"width" : 200,
	"height" : 318+60,

	"children" :
	(
		{
			"name" : "board",
			"type" : "thinboard",

			"x" : 0,
			"y" : 0,

			"width" : 200,
			"height" : 318+60,

			"children" :
			(
				{
					"name" : "help_button",
					"type" : "button",

					"x" : 10,
					"y" : 17,

					"text" : uiScriptLocale.SYSTEM_HELP,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "mall_button",
					"type" : "button",

					"x" : 10,
					"y" : 57,

					"text" : uiScriptLocale.SYSTEM_MALL,
					"text_color" : 0xffF8BF24,

					"default_image" : ROOT + "XLarge_Button_02.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_02.sub",
				},

				{
					"name" : "system_option_button",
					"type" : "button",

					"x" : 10,
					"y" : 87,

					"text" : uiScriptLocale.SYSTEMOPTION_TITLE,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "graphic_option_button",
					"type" : "button",

					"x" : 10,
					"y" : 117,

					"text" : _GRAFIK,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "game_option_button",
					"type" : "button",

					"x" : 10,
					"y" : 147,

					"text" : uiScriptLocale.GAMEOPTION_TITLE,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "change_button",
					"type" : "button",

					"x" : 10,
					"y" : 177,

					"text" : uiScriptLocale.SYSTEM_CHANGE,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "change_ch_button",
					"type" : "button",


					"x" : 10,
					"y" : 207,


					"text" : uiScriptLocale.SYSTEM_MOVE_CHANNEL,
					"text_color" : 0xffF8BF24,


					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
					"disable_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "logout_button",
					"type" : "button",

					"x" : 10,
					"y" : 247,

					"text" : uiScriptLocale.SYSTEM_LOGOUT,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "exit_button",
					"type" : "button",

					"x" : 10,
					"y" : 277,

					"text" : uiScriptLocale.SYSTEM_EXIT,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "custom_button",
					"type" : "button",

					"x" : 10,
					"y" : 307,

					"text" : "Butonlar\xfd \xd6zelle\xfetir",

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "cancel_button",
					"type" : "button",

					"x" : 10,
					"y" : 337,

					"text" : uiScriptLocale.CANCEL,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
			),
		},
	),
}

## MOBIL GRAFIK AYARLARI: dugme yalniz yeni motorda (0.76+, app.GRAFIK_V76). Eski APK'da dugme kaldirilir, alttakiler
## 30 px yukari kayar, pencere eski boyuna (348) doner -> eski APK'li oyuncu hicbir degisiklik gormez.
def _GrafikEskiYerlesim(w):
	try:
		import app as _app
		if getattr(_app, "GRAFIK_V76", 0):
			return
	except:
		pass
	kart = w["children"][0]
	gy = None
	kalan = []
	for c in kart["children"]:
		if c.get("name") == "graphic_option_button":
			gy = c["y"]
			continue
		kalan.append(c)
	if gy is None:
		return
	for c in kalan:
		if c["y"] > gy:
			c["y"] -= 30
	kart["children"] = tuple(kalan)
	kart["height"] -= 30
	w["height"] -= 30
	w["y"] = (SCREEN_HEIGHT - w["height"]) / 2

_GrafikEskiYerlesim(window)
