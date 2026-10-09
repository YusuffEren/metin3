# MOBIL KAPLAMA: locale/tr/ui/InventoryWindow.py (pack surumu PC'de degismez).
# URETILIR: tools/envanter/inventorywindow_kaynak.py (UTF-8) -> tools/envanter/gen_envanter.py -> cp1254.
#
# TEK PENCERE ENVANTER (KULLANICI 2026-10-05, prototip Desktop/Averos2-Envanter-Prototip onaylandi):
#   - envanter + ekipman AYNI klasik pencerede: solda Ekipman / Kostum sekmeleri + bebek + karakter bilgisi, sagda 6x8 envanter
#   - baslikta "Ekipman" dugmesi sol tarafi katlar: pencere SADECE envanter genisligine iner (sag kenar sabit)
#   - envanter HER ACILISTA ekipman KAPALI (ince) acilir (normal, markete / pazara tiklayinca); ekipmani dugme acar
#   - yang kutusu + Yukseltme dugmesi yuvalarin altinda tek satir
# Cocuk adlari eskisiyle AYNI (uiinventory.py / uitoplusat.py / uitooltip.py GetChild ile baglaniyor). Bu dosya INCE
# (katli) yerlesimi tanimlar; genis yerlesimi uiinventory.py __MobileGenislik kurar (sol panel MobileLeftPanel'de).
# Slot pencereleri OLCEKSIZ degerlerle tanimlanir, uiinventory.py yuklemeden sonra wndMgr.SetSlotScale cagirir.
import uiScriptLocale
import item

EQUIPMENT_START_INDEX = 192	## 6x8x4 envanter (sunucu INVENTORY_MAX_NUM 192)
COSTUME_START_INDEX = item.COSTUME_SLOT_START
SCALE = 1.9375		# envanter kutusu 32 px -> 62 px (KULLANICI 2026-10-05 "biraz buyut"; prototip 62 px. uiinventory
			# MOBILE_SLOT_SCALE ve uitoplusat YUVA_OLCEK ile AYNI)
EQ_SCALE = 1.7			# ekipman bebegi (prototip: equipment_base 156x188 x 1.7)
CO_SCALE = 1.62			# kostum zemini new_costume_bg 113x193 x 1.62


def S(v):
	return int(round(v * SCALE))


def E(v):
	return int(round(v * EQ_SCALE))


def C(v):
	return int(round(v * CO_SCALE))


# ---- Envanter (sag) ----
IW = 10 + S(32 * 6) + 10		# 366 (6 sutun)
TITLE_Y = 7
TITLE_H = 37
TAB_Y = TITLE_Y + TITLE_H + 4		# 48
TAB_H = 27
GRID_Y = TAB_Y + TAB_H + 4		# 79
GRID_H = S(32 * 8)			# 461
ROW_Y = GRID_Y + GRID_H + 3		# 543
ROW_H = 44			# yang kutusu + Yukseltme dugmesi satiri
STBTN_W = 127			# Yukseltme (tbbtn 106x23 x 1.2 / 1.74)
MONEY_X = 7
MONEY_W = IW - MONEY_X - 7 - STBTN_W - 5
STBTN_X = MONEY_X + MONEY_W + 5
IH = ROW_Y + ROW_H + 7			# 594
TAB_W = (IW - 20) / 4

# ---- Sol panel (genis yerlesimde; uiinventory __MobileGenislik bu kadar saga iter) ----
LW = 342			# sol panelin genisligi (envanter LW kadar saga kayar)
DOLL_X, DOLL_Y, DOLL_W, DOLL_H = 14, 79, 324, 330
EQ_X = DOLL_X + (DOLL_W - E(156)) / 2		# bebek ortali
EQ_Y = DOLL_Y + (DOLL_H - E(188)) / 2
CO_X = DOLL_X + (DOLL_W - C(113)) / 2
CO_Y = DOLL_Y + (DOLL_H - C(193)) / 2

# ince yerlesim: sag kenar ekrandan 144 px iceride (mini harita ve sag kenar dugmeleri acikta kalir)
ROOT_W = IW
ROOT_H = IH


def InvTab(n, label, tooltip):
	return {
		"name" : "Inventory_Tab_0%d" % n, "type" : "radio_button",
		"x" : 10 + (n - 1) * TAB_W, "y" : TAB_Y,
		"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
		"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
		"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
		"tooltip_text" : tooltip,
		"children" : ( { "name" : "Inventory_Tab_0%d_Print" % n, "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "fontname" : "Tahoma:16", "text" : label }, ),
	}


def EquipTab(n, label, x):
	return {
		"name" : "Equipment_Tab_0%d" % n, "type" : "radio_button",
		"x" : x, "y" : EQ_Y + E(161),
		"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
		"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
		"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",
		"children" : ( { "name" : "Equipment_Tab_0%d_Print" % n, "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "text" : label }, ),
	}


window = {
	"name" : "InventoryWindow",
	"x" : SCREEN_WIDTH - ROOT_W - 144,
	"y" : 4,
	"style" : ("not_pick", "movable", "float"),	# float: SetTop FLAG_FLOAT ister; movable: baslik "attach" ile GetRoot()'u surukler
	"width" : ROOT_W,
	"height" : ROOT_H,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"x" : 0,
			"y" : 0,
			"width" : IW,
			"height" : IH,

			"children" :
			(
				## ---------------- Sol panel (genis yerlesim; ince iken gizli) ----------------
				{
					"name" : "MobileLeftPanel",
					"type" : "window",
					"style" : ("not_pick",),
					"x" : 0,
					"y" : 0,
					"width" : LW,
					"height" : IH,
					"children" :
					(
						{
							"name" : "Equipment_Base",
							"type" : "expanded_image",
							"x" : EQ_X,
							"y" : EQ_Y,
							"x_scale" : EQ_SCALE,
							"y_scale" : EQ_SCALE,
							"image" : "d:/ymir work/ui/game/windows/equipment_base.sub",
						},
						{
							"name" : "EquipmentSlot",
							"type" : "slot",
							"x" : EQ_X + E(3),
							"y" : EQ_Y + E(3),
							"width" : 150,
							"height" : 182,
							"slot" : (
								{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},
								{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+2, "x":39, "y":145, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+4, "x":3, "y":3, "width":32, "height":96},
								{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":84, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":52, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+7, "x":2, "y":113, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+8, "x":75, "y":113, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+9, "x":114, "y":1, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+10, "x":75, "y":35, "width":32, "height":32},
								{"index":item.EQUIPMENT_BELT, "x":39, "y":106, "width":32, "height":32},
							),
						},
						{
							"name" : "RingButton",
							"type" : "button",
							"x" : EQ_X + E(118),
							"y" : EQ_Y + E(115),
						},
						{
							"name" : "MallButton",
							"type" : "button",
							"x" : EQ_X + E(118),
							"y" : EQ_Y + E(148),
							"tooltip_text" : uiScriptLocale.MALL_TITLE,
							"default_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_01.tga",
							"over_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_02.tga",
							"down_image" : "d:/ymir work/ui/game/TaskBar/Mall_Button_03.tga",
						},
						{
							"name" : "CostumeButton",
							"type" : "button",
							"x" : EQ_X + E(78),
							"y" : EQ_Y + E(5),
							"tooltip_text" : uiScriptLocale.COSTUME_TITLE,
							"default_image" : "d:/ymir work/ui/game/taskbar/costume_Button_01.tga",
							"over_image" : "d:/ymir work/ui/game/taskbar/costume_Button_02.tga",
							"down_image" : "d:/ymir work/ui/game/taskbar/costume_Button_03.tga",
						},
						EquipTab(1, "I", EQ_X + E(86)),
						EquipTab(2, "II", EQ_X + E(86) + 34),
						## Kostum sekmesi (KULLANICI 2026-10-05: eski ayri Kostum penceresi yerine ayni pencerede sekme)
						{
							"name" : "MobileCostumeBase",
							"type" : "expanded_image",
							"x" : CO_X,
							"y" : CO_Y,
							"x_scale" : CO_SCALE,
							"y_scale" : CO_SCALE,
							"image" : uiScriptLocale.LOCALE_UISCRIPT_PATH + "costume/new_costume_bg.jpg",
						},
						{
							"name" : "MobileCostumeSlot",
							"type" : "slot",
							"x" : CO_X + C(3),
							"y" : CO_Y + C(3),
							"width" : 127,
							"height" : 180,
							"slot" : (
								{"index":COSTUME_START_INDEX+0, "x":61, "y":45, "width":32, "height":64},
								{"index":COSTUME_START_INDEX+1, "x":61, "y":8, "width":32, "height":32},
								{"index":COSTUME_START_INDEX+2, "x":13, "y":116, "width":32, "height":32},
								{"index":COSTUME_START_INDEX+3, "x":13, "y":14, "width":32, "height":96},
								{"index":item.EQUIPMENT_RING1, "x":13, "y":153, "width":32, "height":32},
								{"index":item.EQUIPMENT_RING2, "x":62, "y":153, "width":32, "height":32},
							),
						},
					),
				},

				## ---------------- Baslik (genislik uiinventory'de ayarlanir) ----------------
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"x" : 8,
					"y" : TITLE_Y,
					"width" : IW - 15,
					"color" : "yellow",
					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":(IW - 15) / 2, "y":1, "fontname":"Tahoma:16", "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center" },
					),
				},
				## Ekipman ac / kapa (baslik cubugunda, carpinin solunda; konum + olcek uiinventory'de)
				{
					"name" : "MobileEquipButton", "type" : "button",
					"x" : IW - 175, "y" : 9,
					"default_image" : "mobile/ui/tbbtn_up.tga",
					"over_image" : "mobile/ui/tbbtn_over.tga",
					"down_image" : "mobile/ui/tbbtn_down.tga",
					"text" : "Ekipman \xbb",
				},

				## ---------------- Envanter (sag; genis yerlesimde LW kadar saga kayar) ----------------
				InvTab(1, "I", uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_1),
				InvTab(2, "II", uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2),
				InvTab(3, "III", uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_3),
				InvTab(4, "IV", uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_4),
				{
					"name" : "ItemSlot",
					"type" : "grid_table",
					"x" : 10,
					"y" : GRID_Y,
					"start_index" : 0,
					"x_count" : 6,
					"y_count" : 8,
					"x_step" : 32,
					"y_step" : 32,
					"image" : "d:/ymir work/ui/public/Slot_Base.sub"
				},
				{
					"name":"Money_Slot",
					"type":"button",
					"x":MONEY_X,
					"y":ROW_Y,
					"width":MONEY_W,
					"height":ROW_H,
					"children" :
					(
						## yang kesesi (masaustu yangkutusu.png 704x124) satir boyuna olceklenir
						{ "name":"Money_Box", "type":"expanded_image", "x":0, "y":0, "x_scale":float(MONEY_W) / 704, "y_scale":float(ROW_H) / 124, "image":"mobile/ui/yang_box.tga" },
						{ "name" : "Money", "type" : "text", "x" : 14, "y" : -1, "vertical_align" : "center", "text_vertical_align" : "center", "fontname" : "Tahoma:19", "horizontal_align" : "right", "text_horizontal_align" : "right", "text" : "123456789" },
					),
				},
				{
					"name" : "MobileStorageButton", "type" : "button",
					"x" : STBTN_X, "y" : ROW_Y + 2,
					"default_image" : "mobile/ui/tbbtn_up.tga",
					"over_image" : "mobile/ui/tbbtn_over.tga",
					"down_image" : "mobile/ui/tbbtn_down.tga",
					"text" : "Y\xfckseltme",
				},
			),
		},
	),
}
