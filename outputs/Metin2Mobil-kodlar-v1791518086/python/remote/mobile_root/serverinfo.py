SERVER_1	= "Averos2"
SERVER_2	= "Averos2"
## v78 (2026-10-08): oyun sunucusu ADI. Yeni APK (motor app.HOSTNAME_DESTEK = 1: getaddrinfo + zaman asimi +
## sabit yedek IP) ADLA baglanir; ad cozulemezse motor ayni IP'ye (185.169.55.31) duser.
## ESKI APK (bayrak yok, ad cozumu zaman asimsiz/yedeksiz) IP ile baglanir - davranisi DEGISMEZ.
SERVER_IP_SABIT	= "185.169.55.31"
SERVER_AD	= "oyun.averos2.com"
try:
	import app as _app
	_HOSTNAME_DESTEK = getattr(_app, "HOSTNAME_DESTEK", 0)
except:
	_HOSTNAME_DESTEK = 0
SERVER_IP	= SERVER_AD if _HOSTNAME_DESTEK else SERVER_IP_SABIT
SERVER_IP2	= SERVER_IP
CH_1_NAME	= "CH1"
CH_2_NAME	= "CH2"
CH_3_NAME	= "CH3"
CH_4_NAME	= "CH4"
CH_5_NAME	= "CH5"
CH_6_NAME	= "CH6"
CH_1		= 12002
CH_2 		= 12102
CH_3 		= 12202
CH_4 		= 12302
CH_5 		= 12402
CH_6 		= 12502
AUTH 		= 11002
MARKADDR	= 12002

#MiniMap Social Butons
SERVER_DC = "mobilserverler.com" #Buraya Discord Linkinizi Yazın
SERVER_DC2 = "https://www.instagram.com/tmorhan"  #Buraya Facebook Linkinizi Yazın

SERVER_DC3 = "#" #Buraya Tiktok Linkinizi Yazın
SERVER_DC4 = "#" #Buraya Instagram Linkinizi Yazın
SERVER_DC5 = "#" #Buraya Youtube Linkinizi Yazın
#MiniMap Social Butons

STATE_NONE = "KAPALI"
					
STATE_DICT = {
	0 : "....",
	1 : "NORM",
	2 : "BUSY",
	3 : "FULL"
}

SERVER01_CHANNEL_DICT = {
	1:{"key":11,"name":CH_1_NAME,"ip":SERVER_IP,"tcp_port":CH_1,"udp_port":CH_1,"state":STATE_NONE,},
	2:{"key":12,"name":CH_2_NAME,"ip":SERVER_IP,"tcp_port":CH_2,"udp_port":CH_2,"state":STATE_NONE,},
	3:{"key":13,"name":CH_3_NAME,"ip":SERVER_IP,"tcp_port":CH_3,"udp_port":CH_3,"state":STATE_NONE,},
	4:{"key":14,"name":CH_4_NAME,"ip":SERVER_IP,"tcp_port":CH_4,"udp_port":CH_4,"state":STATE_NONE,},
	5:{"key":15,"name":CH_5_NAME,"ip":SERVER_IP,"tcp_port":CH_5,"udp_port":CH_5,"state":STATE_NONE,},
	6:{"key":16,"name":CH_6_NAME,"ip":SERVER_IP,"tcp_port":CH_6,"udp_port":CH_6,"state":STATE_NONE,},
}
SERVER02_CHANNEL_DICT = {
	1:{"key":11,"name":CH_1_NAME,"ip":SERVER_IP,"tcp_port":CH_1,"udp_port":CH_1,"state":STATE_NONE,},
	2:{"key":12,"name":CH_2_NAME,"ip":SERVER_IP,"tcp_port":CH_2,"udp_port":CH_2,"state":STATE_NONE,},
	3:{"key":13,"name":CH_3_NAME,"ip":SERVER_IP,"tcp_port":CH_3,"udp_port":CH_3,"state":STATE_NONE,},
	4:{"key":14,"name":CH_4_NAME,"ip":SERVER_IP,"tcp_port":CH_4,"udp_port":CH_4,"state":STATE_NONE,},
	5:{"key":15,"name":CH_5_NAME,"ip":SERVER_IP,"tcp_port":CH_5,"udp_port":CH_5,"state":STATE_NONE,},
	6:{"key":16,"name":CH_6_NAME,"ip":SERVER_IP,"tcp_port":CH_6,"udp_port":CH_6,"state":STATE_NONE,},
}

REGION_NAME_DICT = {
	0 : "",		
}

REGION_AUTH_SERVER_DICT = {
	0 : {
		1 : { "ip":SERVER_IP, "port":AUTH, },
		2 : { "ip":SERVER_IP2, "port":AUTH, },

	}		
}

REGION_DICT = {
	0 : {
		1 : { "name" :SERVER_1, "channel" : SERVER01_CHANNEL_DICT, },
		2 : { "name" :SERVER_2, "channel" : SERVER02_CHANNEL_DICT, },
	},
}

MARKADDR_DICT = {
	10 : { "ip" : SERVER_IP, "tcp_port" : MARKADDR, "mark" : "10.tga", "symbol_path" : "10", },
	20 : { "ip" : SERVER_IP2, "tcp_port" : MARKADDR, "mark" : "10.tga", "symbol_path" : "10", },
}