# -*- coding: cp1254 -*-
# ejderveri.py - Ejder Uyelik istemci sabitleri. tools/ejder/ejder_veri.py URETIR - elle duzenleme.
# Odul tablosu SUNUCUDAN gelir (Ejder T); burada yalniz gorev adlari / fiyatlar / ozel seviyeler.
MAKS = 30
SV_PUAN = 180
PUAN_MAKS = 5220
FIYAT_KART = 300
FIYAT_PLUS = 700
FIYAT_YUKSELT = 400
PLUS_SEVIYE = 10
ANA_ODUL = 71139
KART = 71180
KART_PLUS = 71181
# (tur 0 gunluk / 1 haftalik, ad, hedef, puan)
GOREV = [
	(0, "100 canavar \xf6ld\xfcr", 100, 40),
	(0, "3 Metin ta\xfe\xfd k\xfdr", 3, 40),
	(0, "30 dakika oyunda kal", 30, 30),
	(0, "\xdeans \xc7ark\xfd'n\xfd \xe7evir", 1, 20),
	(1, "1000 canavar \xf6ld\xfcr", 1000, 120),
	(1, "20 Metin ta\xfe\xfd k\xfdr", 20, 150),
	(1, "5 g\xfcn oyuna gir", 5, 100),
	(1, "3 saat oyunda kal", 180, 130),
]
OZEL = {10: "Kost\xfcm", 20: "Sa\xe7", 27: "Binek", 30: "Ay \xf6d\xfcl\xfc"}
# varsayilan tablo (sunucu Ejder T gonderene kadar): sv -> (fv, fa, yv, ya, yk)
ODUL = [
	(27001, 20, 70005, 1, 0),
	(27004, 20, 71027, 2, 0),
	(70102, 1, 71016, 1, 0),
	(25040, 2, 71028, 2, 0),
	(53504, 1, 53504, 1, 0),
	(71084, 2, 71029, 2, 0),
	(27001, 50, 71030, 2, 0),
	(25100, 1, 72703, 1, 0),
	(70038, 10, 53505, 1, 0),
	(50621, 1, 41117, 1, 41118),
	(27004, 50, 70005, 1, 0),
	(25040, 3, 71084, 5, 0),
	(70102, 1, 71027, 3, 0),
	(53504, 1, 53505, 2, 0),
	(71084, 3, 71051, 1, 0),
	(27001, 100, 71028, 3, 0),
	(25100, 2, 72706, 1, 0),
	(70038, 20, 53505, 2, 0),
	(50621, 1, 71029, 3, 0),
	(53504, 2, 45053, 1, 45054),
	(27004, 100, 71030, 3, 0),
	(25040, 5, 53506, 1, 0),
	(70102, 2, 71016, 1, 0),
	(71084, 5, 71051, 2, 0),
	(25100, 3, 71143, 1, 0),
	(70038, 30, 53506, 1, 0),
	(53504, 2, 71138, 1, 0),
	(50621, 2, 71051, 3, 0),
	(71084, 5, 71149, 1, 0),
	(38052, 1, 71139, 1, 0),
]
SURUM = 1
