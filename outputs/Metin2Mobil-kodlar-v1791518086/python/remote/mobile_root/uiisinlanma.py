# MOBIL - YENI DOSYA (mobile_root/uiisinlanma.py): "RUH GECIDI" isinlanma haritasi (v2).
#
# Levi'nin Yuzugu (item 40002) kullanilinca sunucu gorev diyalogu acilir:
#   quest isinlanma_yuzugu
#   /usr/game/share/locale/turkey/quest/object/40002/use/isinlanma_yuzugu.start
# (DIKKAT: diskteki drake_list/draketeleporty.quest kaynagi ESKIDIR; canli menu
#  derlenmis .start dosyasindakidir - olcut odur.)
#
# Menu iki kademelidir:
#   1) Kategori : Koyler / Orman Bolgeleri / Orumcek Zindani / Surgun Magarasi
#                 Girisi / Diger Bolgeler / Etkinlik Bolgeleri / Kapat
#   2) Varis noktasi (kategoriye gore 1-6 secenek + Vazgec)
# Tasarimdaki 6 sekme ve 17 nokta bununla BIREBIR ayni.
#
# Bu modul o diyalogun YERINE tasarim ekranini gosterir. SUNUCU DEGISMEZ:
# diyalogun secenek listesi okunur, haritadan secilen yerin listedeki sirasi
# ADIYLA bulunur ve secim yine ayni gorevin cevap paketiyle (event.SelectAnswer)
# gonderilir - gercek isinlanma sunucuda olur. Secenek listesinde quest imzasi
# yakalanmazsa hicbir sey degismez: normal gorev penceresi acilir.
#
# Tasarim  : Desktop/Isinlanma-Haritasi/isinlanma-haritasi.html v2 (2026-09-21 19:45):
#            kategori basina ayri harita, uc krallik haritasi + kalkan krallik,
#            rotalar, KONUM, acilis animasyonu.
# Gorseller: mobile/ui/tp/v2/*  (scratchpad/bake_v2.py - headless Chrome'da
#            tasarimin kendi CSS'inden pisirilir), mobile/ui/tp/{icon,tab}_*
# Olcumler : tasarimin masaustu referans kutusu (.map-wrap 936x706) - koy
#            isaretcileri ve krallik kesimleri bu kutuya gore ayarlanmis.
# Baglanti : interfacemodule.OpenQuestWindow
#
# TUZAK (ilk surumde yasandi): ui.Window nesnesinin Python referansi dusunce
# __del__ -> wndMgr.Destroy ile C++ penceresi ANINDA silinir. Bu yuzden
# olusturulan HER cocuk self.keep listesinde tutulur.
#
# Turkce metinler cp1254 kacis dizileriyle yazildi (\xf6 = o-umlaut ...): kaynak
# saf ASCII kalir, calisma aninda oyunun bekledigi cp1254 baytlari olusur.

import ui
import app
import event
import wndMgr
import chat
import dbg
import math
import uiQuest

DIR = "mobile/ui/tp/"

# --------------------------------------------------------------------------
# bake_v2.py olcumleri (tasarimin referans kutusu, CSS px)
REF_W = 936.0
REF_H = 706.0
COVER_W = 1536.0
COVER_H = 1024.0
VILLAGE_MAP = (39.333, 76.0, 857.333, 587.333, 1.5)          # (x, y, w, h, doku olcegi) - .map.contain (filtre + scale .97)
KINGDOMS = {'yellow': (16.0, 66.667, 406.0, 335.333, 1.5), 'blue': (537.333, 100.667, 380.0, 412.0, 1.5), 'red': (68.0, 388.0, 622.667, 302.667, 1.5)}
KINGDOM_LAYER = (28, 56, 880, 628)        # .kingdom-layer kutusu (transform-origin merkezi)
PIN_SPRITE_CENTER = (136.5, 136.5)    # pin sprite'inda pin merkezi (px)
PIN_SPRITE_SCALE = 1.75
CORNERS = {'tl': (6.0, 6.0, 52.5, 54.0, 2.0, 1234.0, 794.0), 'tr': (1180.5, 6.0, 53.5, 52.5, 2.0, 59.5, 794.0), 'bl': (6.0, 741.5, 53.5, 52.5, 2.0, 1234.0, 58.5), 'br': (1181.5, 740.0, 52.5, 54.0, 2.0, 58.5, 60.0)}              # (x, y, w, h, olcek, sagdan, alttan) portala gore
RUNE = (82.0, 78.5, 2.0)
TITLE = (155.0, 25.5, 2.0)
CLOSE = (38.0, 38.0, 2.0)
SUMMON_RUNE = (101.0, 101.5, 2.0, 50.602, 45.5, 0.0)          # (w, h, olcek, merkez-x, merkez-y, ekran-merkezinden-dy)
SUMMON_TEXT = (189.0, 15.5, 2.0, 95.734, 7.5, 152.0)

CATEGORIES = (
    ("village", "K\xf6yler",                  "K\xd6YLER",                "koyler"),
    ("forest",  "Orman",                      "ORMAN B\xd6LGELER\xdd",    "ormanbolgeleri"),
    ("spider",  "\xd6r\xfcmcek Zindan\xfd",   "\xd6R\xdcMCEK Z\xddNDANI", "orumcekzindani"),
    ("exile",   "S\xfcrg\xfcn Ma\xf0aras\xfd", "S\xdcRG\xdcN MA\xd0ARASI", "surgunmagarasigirisi"),
    ("other",   "Di\xf0er B\xf6lgeler",       "D\xdd\xd0ER B\xd6LGELER",  "digerbolgeler"),
    ("event",   "Etkinlik",                   "ETK\xddNL\xddK B\xd6LGELER\xdd", "etkinlikbolgeleri"),
)










class _Dest:
    """x, y     : tasarimdaki yuzde (KONUM kutusu bunu gosterir)
    ref      : pin merkezi, referans kutuda (koy gorunumu esit olceklenir)
    fx, fy   : pin merkezinin kategori haritasi icindeki kesri (kaplama haritalar)
    kingdom  : koyler icin kalkan krallik (yellow/blue/red)"""

    def __init__(self, cat, name, x, y, color, region, level, status, desc, sub, kingdom,
                 ref, frac):
        self.cat = cat
        self.name = name
        self.x = x
        self.y = y
        self.color = color                  # 0xRRGGBB
        self.region = region
        self.level = level
        self.status = status
        self.desc = desc
        self.sub = sub                      # quest 2. menu anahtari
        self.kingdom = kingdom
        self.ref = ref
        (self.fx, self.fy) = frac


# Seviye degerleri quest'teki "(+NN)" etiketlerinden alindi (tasarimdaki ornek
# araliklar/ucretler degil). Quest bunlari KONTROL ETMEZ - istemci de engellemez.
DESTS = (
    _Dest('village', "K\xfdrm\xfdz\xfd 1. K\xf6y", 30, 74, 0xff5c51,
          "Krall\xfdk K\xf6y\xfc", "T\xfcm Seviyeler", "G\xfcvenli",
          "K\xfdrm\xfdz\xfd krall\xfd\xf0\xfdn ba\xfelang\xfd\xe7 k\xf6y\xfc ve g\xfcvenli ticaret merkezi.",
          'kirmizibayrak1koy', 'red',
          (280.79, 502.94), (0.32669, 0.70822)),
    _Dest('village', "Sar\xfd 1. K\xf6y", 23, 31, 0xf0c556,
          "Krall\xfdk K\xf6y\xfc", "T\xfcm Seviyeler", "G\xfcvenli",
          "Sar\xfd krall\xfd\xf0\xfdn ba\xfelang\xfd\xe7 k\xf6y\xfc ve kalabal\xfdk pazar alan\xfd.",
          'saribayrak1koy', 'yellow',
          (215.26, 199.36), (0.26602, 0.28665)),
    _Dest('village', "Mavi 1. K\xf6y", 76, 31, 0x5dcfff,
          "Krall\xfdk K\xf6y\xfc", "T\xfcm Seviyeler", "G\xfcvenli",
          "Mavi krall\xfd\xf0\xfdn ba\xfelang\xfd\xe7 k\xf6y\xfc ve g\xfcvenli toplanma noktas\xfd.",
          'mavibayrak1koy', 'blue',
          (711.36, 199.36), (0.72530, 0.28665)),
    _Dest('village', "Mavi 2. K\xf6y", 68, 45, 0x5dcfff,
          "\xddkinci K\xf6y", "T\xfcm Seviyeler", "Orta Tehlike",
          "Mavi krall\xfd\xf0\xfdn daha g\xfc\xe7l\xfc yarat\xfdklarla \xe7evrili ikinci k\xf6y\xfc.",
          'mavibayrak2koy', 'blue',
          (636.46, 298.19), (0.65596, 0.42389)),
    _Dest('village', "K\xfdrm\xfdz\xfd 2. K\xf6y", 40, 68, 0xff5c51,
          "\xddkinci K\xf6y", "T\xfcm Seviyeler", "Orta Tehlike",
          "K\xfdrm\xfdz\xfd krall\xfd\xf0\xfdn volkanik s\xfdn\xfdrlar\xfdndaki ikinci k\xf6y\xfc.",
          'kirmizibayrak2koy', 'red',
          (374.39, 460.58), (0.41334, 0.64939)),
    _Dest('village', "Sar\xfd 2. K\xf6y", 34, 28, 0xf0c556,
          "\xddkinci K\xf6y", "T\xfcm Seviyeler", "Orta Tehlike",
          "Sar\xfd krall\xfd\xf0\xfdn kadim yollar \xfczerindeki ikinci k\xf6y\xfc.",
          'saribayrak2koy', 'yellow',
          (318.23, 178.17), (0.36135, 0.25722)),
    _Dest('forest', "Hayalet Orman", 39, 30, 0x83e7b2,
          "Lanetli Orman", "60+", "Tehlikeli",
          "Sislerin i\xe7inde kaybolmu\xfe ruhlar\xfdn dola\xfet\xfd\xf0\xfd karanl\xfdk orman.",
          'hayaletorman', None,
          (365.03, 192.30), (0.40467, 0.27684)),
    _Dest('forest', "K\xfdz\xfdl Orman", 66, 44, 0xe05a45,
          "K\xfdz\xfdl Koruluk", "65+", "\xc7ok Tehlikeli",
          "K\xfdz\xfdl a\xf0a\xe7lar ve g\xfc\xe7l\xfc yarat\xfdklarla kapl\xfd y\xfcksek seviye b\xf6lgesi.",
          'kizilorman', None,
          (617.75, 291.12), (0.63863, 0.41407)),
    _Dest('spider', "\xd6r\xfcmcek Zindan\xfd Kat 1", 43, 61, 0xb983ff,
          "Yeralt\xfd Zindan\xfd", "30+", "Zindan",
          "Dev \xf6r\xfcmceklerin yuva yapt\xfd\xf0\xfd karanl\xfdk yeralt\xfd labirentinin ilk kat\xfd.",
          'orumcekzindani1katbasi', None,
          (402.47, 411.16), (0.43933, 0.58076)),
    _Dest('exile', "S\xfcrg\xfcn Ma\xf0aras\xfd Giri\xfe", 23, 23, 0x74ddff,
          "Kadim Ma\xf0ara", "T\xfcm Seviyeler", "\xc7ok Tehlikeli",
          "Buzlu kayalar\xfdn alt\xfdndaki kadim ma\xf0aran\xfdn m\xfch\xfcrl\xfc giri\xfe kap\xfds\xfd.",
          'surgunmagarasigirisi', None,
          (215.27, 142.88), (0.26603, 0.20822)),
    _Dest('other', "Seungryong Vadisi", 49, 48, 0x70d49c,
          "Vadi", "25+", "Orta Tehlike",
          "Krall\xfdk yollar\xfdn\xfd birbirine ba\xf0layan geni\xfe ve hareketli sava\xfe vadisi.",
          'seungryongvadisi', None,
          (458.62, 319.38), (0.49132, 0.45331)),
    _Dest('other', "Sohan Da\xf0\xfd", 28, 20, 0xbfe7ff,
          "Buz Da\xf0\xfd", "40+", "Tehlikeli",
          "Sonsuz karlarla kapl\xfd da\xf0 ge\xe7itleri ve buz yarat\xfdklar\xfd b\xf6lgesi.",
          'sohandagi', None,
          (262.08, 121.69), (0.30937, 0.17879)),
    _Dest('other', "Yongbi \xc7\xf6l\xfc", 29, 67, 0xefc66d,
          "B\xfcy\xfck \xc7\xf6l", "30+", "Orta Tehlike",
          "Kum f\xfdrt\xfdnalar\xfd ve akrep s\xfcr\xfcleriyle bilinen u\xe7suz bucaks\xfdz \xe7\xf6l.",
          'yongbicolu', None,
          (271.44, 453.52), (0.31803, 0.63959)),
    _Dest('other', "Doyyumhwan", 64, 67, 0xff784e,
          "Ate\xfe Diyar\xfd", "55+", "Tehlikeli",
          "Lav nehirleriyle \xe7evrili, ate\xfe yarat\xfdklar\xfdn\xfdn h\xfck\xfcm s\xfcrd\xfc\xf0\xfc topraklar.",
          'doyyumhwan', None,
          (599.02, 453.52), (0.62129, 0.63959)),
    _Dest('other', "Devler Diyar\xfd", 76, 28, 0xd0ab74,
          "Dev Ovas\xfd", "60+", "\xc7ok Tehlikeli",
          "Kadim devlerin ve ta\xfe sava\xfe\xe7\xfdlar\xfdn korudu\xf0u uzak diyar.",
          'devlerdiyari', None,
          (711.35, 178.17), (0.72529, 0.25722)),
    _Dest('other', "\xdeeytan Kulesi", 61, 31, 0xdc70ff,
          "Lanetli Kule", "40+", "Zindan",
          "Her kat\xfdnda daha g\xfc\xe7l\xfc d\xfc\xfemanlar\xfdn bekledi\xf0i karanl\xfdk kule.",
          'seytankulesi', None,
          (570.95, 199.36), (0.59531, 0.28665)),
    _Dest('event', "Bal\xfdk\xe7\xfd Haritas\xfd", 72, 75, 0x62d9e8,
          "Etkinlik Adas\xfd", "T\xfcm Seviyeler", "Etkinlik",
          "Bal\xfdk\xe7\xfdl\xfdk etkinli\xf0i s\xfcresince a\xe7\xfdlan sakin ve \xf6d\xfcll\xfc \xf6zel ada.",
          'balikciharitasi', None,
          (673.90, 510.00), (0.69062, 0.71802)),
)

CAT_QUEST_KEY = {}
for _c in CATEGORIES:
    CAT_QUEST_KEY[_c[0]] = _c[3]

# --------------------------------------------------------------------------
# Sunucu metinlerini karsilastirmak icin normallestirme.
# Quest cp1254 yazilmistir; adlarin sonunda "(+65)" gibi ekler, sekme ve
# bosluklar vardir. Turkce harfleri ASCII'ye katlayip yalniz harf/rakam
# birakiyoruz: "Yongbi \xc7\xf6l\xfc (+30) " -> "yongbicolu".
_FOLD = {
    "\xe7": "c", "\xc7": "c", "\xf6": "o", "\xd6": "o", "\xfc": "u", "\xdc": "u",
    "\xf0": "g", "\xd0": "g", "\xfe": "s", "\xde": "s", "\xfd": "i", "\xdd": "i",
}


def Normalize(s):
    s = s.split("(")[0]
    out = []
    for ch in s:
        c = _FOLD.get(ch)
        if c is None:
            c = ch.lower()
        if ("a" <= c <= "z") or ("0" <= c <= "9"):
            out.append(c)
    return "".join(out)


def _IsRingDialog(answers):
    """Secenek listesi isinlanma yuzugunun KATEGORI listesi mi?
    (6 kategoriden en az 4'u)"""
    if len(answers) < 4 or len(answers) > 16:
        return False
    keys = {}
    for a in answers:
        keys[Normalize(a)] = 1
    hit = 0
    for c in CATEGORIES:
        if c[3] in keys:
            hit = hit + 1
    return hit >= 4


def _IndexOf(answers, key):
    for i in xrange(len(answers)):
        if Normalize(answers[i]) == key:
            return i
    return -1


# --------------------------------------------------------------------------
# Kucuk yardimcilar

def _Rgb(c):
    return (((c >> 16) & 0xff) / 255.0, ((c >> 8) & 0xff) / 255.0, (c & 0xff) / 255.0)


def _Tint(imagebox, color, alpha=1.0):
    """ui.ImageBox'ta SetDiffuseColor METODU YOKTUR (yalniz SetAlpha); dogrudan
    wndMgr'a gidiyoruz - beyaz uretilmis gorsel bolge rengiyle carpilir."""
    (r, g, b) = _Rgb(color)
    wndMgr.SetDiffuseColor(imagebox.hWnd, r, g, b, alpha)


def _Mix(a, b, t):
    """CSS color-mix(a t%, b) karsiligi: a ve b (0xRRGGBB) -> 0xRRGGBB"""
    o = 0
    for sh in (16, 8, 0):
        ca = (a >> sh) & 0xff
        cb = (b >> sh) & 0xff
        o = o | (int(ca * t + cb * (1.0 - t)) << sh)
    return o


def _A(alpha, rgb):
    """alpha (0..255) + 0xRRGGBB -> 0xAARRGGBB"""
    return (int(alpha) << 24) | (rgb & 0xffffff)


class _Touch(ui.Window):
    """Gorunmez dokunma alani. Duz CWindow secilebilir (varsayilan FLAG_NOT_PICK
    yoktur), ust penceresinin dortgeni icinde kaldigi surece."""

    def __init__(self, func=None, arg=None):
        ui.Window.__init__(self)
        self.func = func
        self.arg = arg

    def __del__(self):
        ui.Window.__del__(self)
        self.func = None

    def Place(self, parent, x, y, w, h):
        self.SetParent(parent)
        self.SetPosition(int(x), int(y))
        self.SetSize(int(w), int(h))
        self.Show()
        return self

    def OnMouseLeftButtonDown(self):
        return True

    def OnMouseLeftButtonUp(self):
        if self.func:
            if self.arg is None:
                self.func()
            else:
                self.func(self.arg)
        return True


# --------------------------------------------------------------------------
# Gorev akisi
#
# Oyuncu haritadan bir yer secip "I\xfe\xfdnlan"a basinca once KATEGORI secimi
# gonderilir; sunucu ikinci listeyi gonderir, onu GORUNMEZ bir surucu yanitlar
# ve sunucu isinlanmayi yapar.
#
# TUZAK: yanit ProcessEventSet geri cagrisinin ICINDEN gonderilip olay seti ayni
# anda temizlenirse C++ tarafi hala o seti geziyor olur. Bu yuzden surucu yalniz
# NE GORDUGUNU kaydeder; gercek yanit pencerenin OnUpdate'inde (bir sonraki
# karede) gonderilir.

STAGE_PICK = 0      # harita acik, oyuncu seciyor
STAGE_CAT = 1       # kategori secimi gonderildi, alt liste bekleniyor
STAGE_DEST = 2      # varis secimi gonderildi (isinlanma sunucuda)

IDLE_TIMEOUT = 3.0      # son yanittan sonra sessizlik -> perdeyi kapat
PULSE_PERIOD = 2.0      # @keyframes pulse 2s infinite
PULSE_GROW = 0.70       # 70%: scale 1.5 / opacity 0, sonra 100%'e kadar gorunmez
HARD_TIMEOUT = 20.0     # mutlak ust sinir
MAX_NEXT = 6            # "Sonraki" dongusune karsi emniyet


class _Flow:
    def __init__(self, dialog, answers):
        self.dialog = dialog        # ilk (gizlenmis) gorev diyalogu
        self.answers = answers      # kategori listesindeki secenek adlari
        self.dest = None
        self.stage = STAGE_PICK
        self.nextCount = 0
        self.start = app.GetTime()
        self.last = app.GetTime()
        self.incoming = None
        self.driver = None


g_window = None
g_flow = None
g_pump = None


class _Pump(ui.Window):
    """Gorunmez (0x0) kok pencere: her kare gorunmez surucunun olay setini
    isler ve akisi ilerletir. Harita penceresi Isinlan'a basilinca HEMEN
    kapandigi icin (kullanici: normal yukleme ekrani gorunsun) pompa ayri bir
    pencerede yasamali - gizli pencerenin OnUpdate'i calismaz."""

    def __init__(self):
        ui.Window.__init__(self, "TOP_MOST")
        if hasattr(wndMgr, "SetUIScale"):
            wndMgr.SetUIScale(self.hWnd, 1.0)
        self.SetWindowName("TeleportPump")
        self.SetPosition(0, 0)
        self.SetSize(0, 0)
        self.Show()

    def __del__(self):
        ui.Window.__del__(self)

    def OnUpdate(self):
        # Gorev betigi komutlari YALNIZ event.UpdateEventSet cagrisinda islenir
        # (CPythonEventManager::UpdateEventSet -> ProcessEventSet); gercek
        # QuestDialog bunu kendi OnUpdate'inde yapar. Gorunmez surucunun seti
        # icin bunu BIZ yapmaliyiz, yoksa ikinci liste hic gelmez.
        # Yalniz bekleyen olay YOKKEN pompalanir: ayni karede ikinci bir _Post
        # tek yuvali flow.incoming'i ezmesin (denetim notu).
        flow = g_flow
        if flow is None:
            return
        if flow.driver is not None and flow.incoming is None:
            try:
                event.UpdateEventSet(flow.driver.idx, 0, 0)
            except:
                pass
        _PumpFlow()


def _Nop(*a, **k):
    return None


class _Driver:
    """Gorunmez gorev olay isleyicisi (akis surerken QuestDialog yerine gecer).
    Bilinmeyen geri cagrilar __getattr__ ile yutulur - C++ tarafi resim/solma
    gibi baska komutlar da gonderebilir."""

    def __init__(self, idx):
        self.idx = idx
        self.total = 0
        self.answers = []
        self.button = None

    def MakeQuestion(self, n):
        self.total = n
        self.answers = [""] * n

    def AppendQuestion(self, name, i):
        if 0 <= i < len(self.answers):
            self.answers[i] = name
        if self.total and i == self.total - 1:
            _Post(self, "answers")

    def MakeNextButton(self, button_type):
        self.button = button_type
        _Post(self, "button")

    def DoneEvent(self):
        _Post(self, "done")

    def CloseSelf(self):
        pass

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return _Nop


def _Post(driver, kind):
    if g_flow and g_flow.driver is driver:
        g_flow.incoming = kind
        g_flow.last = app.GetTime()


def _Answer(idx, value):
    try:
        event.SelectAnswer(idx, value)
    except:
        pass
    try:
        event.ClearEventSet(idx)
    except:
        pass


def _EndFlow(msg=None):
    global g_flow
    if g_flow:
        d = g_flow.driver
        if d is not None:
            # Yanitlanmamis olay seti kalmasin: C++ tarafinda poEventHandler
            # isaretcisi ve yuva sizardi (denetim bulgusu).
            try:
                event.ClearEventSet(d.idx)
            except:
                pass
        g_flow.driver = None
        g_flow.dialog = None
    g_flow = None
    if g_window:
        g_window.CloseSelf()
    if msg:
        chat.AppendChat(chat.CHAT_TYPE_INFO, msg)


def IsFlowActive():
    return g_flow is not None and g_flow.stage != STAGE_PICK


def OnQuestWindow(interface, skin, idx):
    """interfacemodule.OpenQuestWindow'un ilk satiri. Akis suruyorsa betigi
    gorunmez surucuye baglar ve True doner (normal gorev penceresi ACILMAZ)."""
    if not IsFlowActive():
        return False
    d = _Driver(idx)
    g_flow.driver = d
    g_flow.incoming = None
    try:
        event.SetRestrictedCount(idx, 60)
    except:
        pass
    event.SetEventHandler(idx, d)
    return True


def MakeQuestDialog(skin, idx):
    """interfacemodule.OpenQuestWindow icin: normal QuestDialog gibi davranan,
    ama isinlanma yuzugunun kategori listesini taniyinca haritaya donusen
    diyalog."""
    return _RingAwareDialog(skin, idx)


class _RingAwareDialog(uiQuest.QuestDialog):
    """Kullanici: eski gorev penceresi BIR KARE BILE gorunmesin. Karar ancak
    secenek listesi gelince verilebildiginden pano + metin + perde BASTAN
    gizlenir; yuzuk degilse geri acilir (tek kare gecikme, fark edilmez).
    Pencerenin kendisi GORUNUR kalir - OnUpdate'i (event.UpdateEventSet)
    calismali ki betik hic islensin."""

    RING_DECIDE_TIMEOUT = 0.6   # emniyet: bu sure icinde karar yoksa normal pencere

    def __init__(self, skin, idx):
        uiQuest.QuestDialog.__init__(self, skin, idx)
        self.ringAnswers = []
        self.ringTotal = 0
        self.ringTaken = False
        self.ringDecided = False
        self.ringStart = app.GetTime()
        board = getattr(self, "board", None)
        if board:
            board.Hide()
        desc = getattr(self, "descWindow", None)
        if desc:
            desc.Hide()
        try:
            uiQuest.QuestDialog.QuestCurtain.CurtainMode = 0   # siyah seritler girmesin
        except:
            pass

    def __Restore(self):
        """Yuzuk degilmis: gercek gorev penceresi gibi gorun."""
        if self.ringDecided:
            return
        self.ringDecided = True
        board = getattr(self, "board", None)
        if board:
            board.Show()
        desc = getattr(self, "descWindow", None)
        if desc:
            desc.Show()
        if self.skin:
            try:
                uiQuest.QuestDialog.QuestCurtain.CurtainMode = 1
            except:
                pass

    def OnUpdate(self):
        if not self.ringDecided and app.GetTime() - self.ringStart > self.RING_DECIDE_TIMEOUT:
            self.__Restore()
        uiQuest.QuestDialog.OnUpdate(self)

    def MakeQuestion(self, n):
        self.ringTotal = n
        self.ringAnswers = [""] * n
        if n < 4 or n > 16:
            self.__Restore()
        uiQuest.QuestDialog.MakeQuestion(self, n)

    def AppendQuestion(self, name, idx):
        if 0 <= idx < len(self.ringAnswers):
            self.ringAnswers[idx] = name
        uiQuest.QuestDialog.AppendQuestion(self, name, idx)
        if not self.ringTaken and not self.ringDecided and self.ringTotal and idx == self.ringTotal - 1:
            if _IsRingDialog(self.ringAnswers):
                self.ringTaken = True
                self.ringDecided = True
                try:
                    _TakeOver(self, self.ringAnswers)
                except:
                    import sys
                    dbg.TraceError("uiisinlanma._TakeOver basarisiz: %s" % (sys.exc_info()[1],))
                    # harita yarim kaldiysa kapat, akisi birak; gercek gorev penceresine don
                    try:
                        _EndFlow()
                    except:
                        pass
                    self.ringDecided = False
                    self.__Restore()
                    self.Show()
            else:
                self.__Restore()

    # Soru listesi olmayan betikler (metin + dugme, girdi, resim): yuzuk degil.
    def MakeNextButton(self, button_type):
        self.__Restore()
        uiQuest.QuestDialog.MakeNextButton(self, button_type)

    def OnInput(self):
        self.__Restore()
        uiQuest.QuestDialog.OnInput(self)

    def OnTitleImage(self, src):
        self.__Restore()
        uiQuest.QuestDialog.OnTitleImage(self, src)

    def OnLeftImage(self, src):
        self.__Restore()
        uiQuest.QuestDialog.OnLeftImage(self, src)

    def OnTopImage(self, src):
        self.__Restore()
        uiQuest.QuestDialog.OnTopImage(self, src)

    def OnBackgroundImage(self, src):
        self.__Restore()
        uiQuest.QuestDialog.OnBackgroundImage(self, src)


def _TakeOver(dialog, answers):
    """Gorev diyalogunu gizle, haritayi ac."""
    global g_flow, g_window, g_pump

    # Gorev penceresi gorunmez olsun ama YASASIN (cevap paketi onun uzerinden
    # gider). Perdeyi (siyah seritler) geri cek, kilidi ac ki bizim pencere
    # dokunma alabilsin (OpenQuestWindow diyalogu Lock'lar).
    dialog.Hide()
    dialog.Unlock()
    dialog.nextCurtainMode = -1
    try:
        uiQuest.QuestDialog.QuestCurtain.CurtainMode = -1
    except:
        pass

    g_flow = _Flow(dialog, answers)
    if g_pump is None:
        g_pump = _Pump()
    if g_window is None:
        g_window = TeleportMapWindow()
    g_window.Open()


# --------------------------------------------------------------------------
# Isinlanma istegi

def _RequestTeleport(dest):
    flow = g_flow
    if flow is None or flow.stage != STAGE_PICK or flow.dialog is None:
        return

    i = _IndexOf(flow.answers, CAT_QUEST_KEY.get(dest.cat, ""))
    if i < 0:
        chat.AppendChat(chat.CHAT_TYPE_INFO,
                        "Bu b\xf6lge \xfeu anda y\xfcz\xfckte tan\xfdml\xfd de\xf0il.")
        return

    d = flow.dialog
    if getattr(d, "descIndex", None) is None:
        # Diyalog bizden habersiz kapanmis ([DESTROY_ALL] / HideAllQuestWindow):
        # ClickAnswerEvent sessizce paket gondermezdi (denetim bulgusu).
        _EndFlow("Y\xfcz\xfck ba\xf0lant\xfds\xfd koptu, tekrar dene.")
        return
    flow.dest = dest
    flow.stage = STAGE_CAT
    flow.start = app.GetTime()
    flow.last = app.GetTime()
    g_window.CloseSelf()        # kullanici: perde yok, normal yukleme ekrani gelsin
    flow.dialog = None
    d.ClickAnswerEvent(i)       # SelectAnswer + CloseSelf (gercek istemcinin yolu)


def _Cancel():
    """Kapat dugmesi / ESC: gorevi listedeki son secenekle ("Kapat") bitir."""
    flow = g_flow
    if flow and flow.stage == STAGE_PICK and flow.dialog is not None:
        d = flow.dialog
        flow.dialog = None
        if getattr(d, "descIndex", None) is not None:
            d.ClickAnswerEvent(len(flow.answers) - 1)
    _EndFlow()


def _PumpFlow():
    """Pencerenin OnUpdate'inden cagrilir - surucunun gordugu betige cevap verir."""
    flow = g_flow
    if flow is None or flow.stage == STAGE_PICK:
        return

    now = app.GetTime()
    if now - flow.start > HARD_TIMEOUT:
        _EndFlow()
        return

    kind = flow.incoming
    if kind is None:
        if now - flow.last > IDLE_TIMEOUT:
            _EndFlow()      # isinlanma gerceklesti (ya da gorev sessizce bitti)
        return
    flow.incoming = None
    d = flow.driver
    if d is None:
        return

    if kind == "answers":
        if flow.stage == STAGE_CAT:
            i = _IndexOf(d.answers, flow.dest.sub)
            if i < 0:
                flow.driver = None
                iv = _IndexOf(d.answers, "vazgec")
                if iv >= 0:
                    _Answer(d.idx, iv)
                else:
                    try:
                        event.ClearEventSet(d.idx)
                    except:
                        pass
                _EndFlow("I\xfe\xfdnlanma noktas\xfd bulunamad\xfd.")
                return
            flow.stage = STAGE_DEST
            flow.last = now
            flow.driver = None
            _Answer(d.idx, i)
        else:
            # Beklenmeyen liste (alakasiz bir gorev araya girmis olabilir):
            # "Vazgec" varsa onu sec, yoksa yalnizca seti birak.
            flow.driver = None
            iv = _IndexOf(d.answers, "vazgec")
            if iv >= 0:
                _Answer(d.idx, iv)
            else:
                try:
                    event.ClearEventSet(d.idx)
                except:
                    pass
            _EndFlow()
        return

    if kind == "button":
        if d.button == event.BUTTON_TYPE_NEXT:
            flow.nextCount = flow.nextCount + 1
            if flow.nextCount > MAX_NEXT:
                _EndFlow("\xdeu an \xfd\xfe\xfdnlanam\xfdyorsun, biraz sonra tekrar dene.")
                return
            flow.last = now
            flow.driver = None
            _Answer(d.idx, 254)
        else:
            flow.driver = None
            _Answer(d.idx, 254)     # DONE / CANCEL -> gorev bitti
            _EndFlow()
        return

    if kind == "done":
        _EndFlow()


# --------------------------------------------------------------------------
# Pencere (v2) - olculer tasarimin CSS'inden, sprite'lar bake_v2.py ile
# Chrome'dan pisirildi (mobile/ui/tp/v2/). Tasarimdaki hareketler:
#   acilis (ruh muhru: donen halkalar + rune patlamasi + solma),
#   sekme degisiminde harita solup yakinlasmasi, isaretcilerin sirayla belirmesi,
#   secili pinin nabzi, pin halkasi, koy seciminde krallik parcasinin kalkip
#   suzulmesi, isaretciler arasi akan kesikli rotalar + ustunde kayan isik topu,
#   bilgi panelinin kayarak yenilenmesi, KONUM kutusu.
# Kullanicinin telefona ozel onceki kararlari korunur: portal TUM EKRAN,
# sekmeler buyuk (17 px), isaretci adlari okunakli (14 px), "Ruh gecidi
# aciliyor" perdesi YOK (Isinlan -> harita kapanir, oyunun yukleme ekrani).

V2 = DIR + "v2/"

TOPBAR_H = 74
INFO_W = 300
PAD = 24                    # .info padding
BORDER = 2                  # .portal border
PIN_D = 50                  # .pin 50x50
LABEL_GAP = 36              # pin merkezi -> etiket ustu (25 + margin 11)
LABEL_H = 30
LABEL_FONT = "Tahoma:14"    # kullanici: okunakli (tasarim 12)
TAB_FONT = "Tahoma:17"      # kullanici: buyuk sekmeler (tasarim 12)
TAB_ICON = 28
TAB_H = 56
TAB_TOP = 14

ROUTE_LIFT = 0.07           # routePath: my = (a.y+b.y)/2 - 7  (kutu yuksekliginin %7'si)
ROUTE_FLOW = True           # kesiklerin akmasi (stroke-dashoffset animasyonu)
DASH_ON = 10.0
DASH_OFF = 9.0
DASH_SPEED = 25.0           # -4.6 birim / 1.5 s
ORB_PERIOD = 2.6            # animateMotion dur
FLOAT_PERIOD = 2.6          # realmFloat
SEL_PERIOD = 1.4            # selectedPulse
MARKER_IN = 0.45            # markerIn
MARKER_STAGGER = 0.06
PANEL_SWAP = 0.32           # panelSwap
## PERFORMANS (KULLANICI 2026-09-27: "isinlanma penceresi cok agir aciliyor, icerigi de agir, oyunu yormasin"):
## acilis perdesi (_Summon, 2.3 s) kaldirildi, kategori isaretci/rotalari bir kez kurulup onbellekte tutulur,
## sekme gecisi kisaltildi.
MAP_OUT = 0.10              # renderCategory setTimeout (tasarim .26)
MAP_IN = 0.14
MAP_ZOOM_BACK = 0.7
SUMMON_HOLD = 1.75          # setTimeout(...done, 1750)
SUMMON_FADE = 0.55
RUNE_BURST = 1.7
# Kullanici (2026-09-21): "surgun magarasi yukarda kalmis, iconu ortaya al" -
# bu kategorilerin (tek noktali) isaretcisi harita alaninin ortasina konur.
CENTER_CATS = ("exile",)

C_PORTAL = 0xff080a0e
C_PORTAL_BORDER = 0xff725126
C_PORTAL_INSET = 0x33ffd88b
C_PORTAL_FRAME = 0x47deab4e
C_TOP1 = 0x17130d
C_TOP2 = 0x0b0c11
C_LINE = 0x1cffffff
C_SUB = 0xff777c8a
C_INFO1 = 0x111218
C_INFO2 = 0x090a0e
C_TABBG = 0xdb07090e
C_TABBORDER = 0x1fffffff
C_TABTXT = 0xff8c909c
C_NAME = 0xfff4e7c9
C_DESC = 0xff9599a5
C_STATL = 0xff888d9b
C_STATV = 0xffeae4d8
C_SAFE = 0xff82e6a8
C_RISK = 0xffff9b73
C_BTN_SMALL = 0xffd3d1cd
C_COORD_BG = 0xc7050609
C_COORD_BORDER = 0x59e7bd74
C_COORD_TXT = 0xff9aa0ae
C_ROUTE_SHADOW = 0x99000000


def _Clamp01(t):
    if t < 0.0:
        return 0.0
    if t > 1.0:
        return 1.0
    return t


def _EaseOut(t):
    """cubic-bezier(.2,.9,.2,1) yaklasigi"""
    t = _Clamp01(t)
    return 1.0 - (1.0 - t) ** 3


def _EaseInOut(t):
    t = _Clamp01(t)
    return t * t * (3.0 - 2.0 * t)


def _Wave(now, period):
    """ease-in-out ileri-geri 0..1..0 (keyframes 0%/50%/100%)"""
    return 0.5 - 0.5 * math.cos(2.0 * math.pi * ((now % period) / period))


def _AlphaColor(argb, a):
    return (int(((argb >> 24) & 0xff) * _Clamp01(a)) << 24) | (argb & 0xffffff)


def _SafeLoad(box, path):
    """wndMgr.LoadImage basarisizlikta Py_BuildException ile None doner ve istisna
    BEKLER; bir sonraki dongu sonunda alakasiz yerde patlar (__Build yarida kalir).
    max(0,0) bekleyen istisnayi burada, try icinde tetikler."""
    try:
        box.LoadImage(path)
        max(0, 0)
        return True
    except:
        dbg.TraceError("uiisinlanma: gorsel yuklenemedi %s" % path)
        return False


# Acilis perdesi (ruh muhru) tam ekrani kaplarken rota/isaretci guncellemesi bosa
# gider; animasyonlar zamana bagli oldugundan perde kalkinca dogru kareden devam eder.
g_summonUntil = [0.0]


class _Spr:
    """ExpandedImageBox sarmalayici: dokunma ALMAZ (not_pick), dogal boyutu bilir.
    Son yazilan donme/olcek/konum/renk onbellekte: degismeyen deger motora tekrar
    gonderilmez (denetim: kare basina ~500 gereksiz wndMgr cagrisi)."""

    def __init__(self, parent, path, keep):
        b = ui.ExpandedImageBox()
        b.SetParent(parent)
        b.AddFlag("not_pick")
        ok = _SafeLoad(b, path)
        self.w = b.GetWidth()
        self.h = b.GetHeight()
        if not ok or self.w <= 0:
            self.w = self.h = 1
        b.Show()
        keep.append(b)
        self.b = b
        self._rot = 0.0
        self._sc = None
        self._pos = None
        self._tint = None
        self._shown = True

    def Place(self, x, y, scale):
        if self._rot != 0.0:
            self.b.SetRotation(0.0)
            self._rot = 0.0
        if scale != self._sc:
            self.b.SetScale(scale, scale)
            self.b.SetSize(max(1, int(self.w * scale)), max(1, int(self.h * scale)))
            self._sc = scale
        p = (int(x), int(y))
        if p != self._pos:
            self.b.SetPosition(p[0], p[1])
            self._pos = p

    def Stretch(self, x, y, w, h):
        self.b.SetRotation(0.0)
        self._rot = 0.0
        self.b.SetScale(float(w) / self.w, float(h) / self.h)
        self.b.SetPosition(int(x), int(y))
        self.b.SetSize(max(1, int(w)), max(1, int(h)))
        self._sc = None
        self._pos = None

    def Center(self, cx, cy, scale, deg=0.0):
        """(cx,cy) merkezli, olcekli ve donuk cizim.
        TUZAK (cihazda goruldu: "ruh muhru ekrana sigmiyor"): donme dalinda cizim
        merkezi = konum + origin ve motor origin'i LoadImage'da gorselin OLCEKSIZ
        yari boyutuna kurar (CGraphicExpandedImageInstance::OnSetImagePointer).
        Konumu merkez sanmak halkalari (640 px) 320 px saga-asagi kaydiriyordu."""
        self.b.SetScale(scale, scale)
        if abs(deg) < 0.01:
            deg = 0.01
        self.b.SetRotation(deg)
        self._rot = deg
        self.b.SetPosition(int(round(cx - self.w / 2.0)), int(round(cy - self.h / 2.0)))
        self.b.SetSize(1, 1)
        self._sc = None
        self._pos = None

    def Alpha(self, a, color=0xffffff):
        key = (color, int(_Clamp01(a) * 255))
        if key != self._tint:
            _Tint(self.b, color, key[1] / 255.0)
            self._tint = key

    def Show(self):
        if not self._shown:
            self.b.Show()
            self._shown = True

    def Hide(self):
        if self._shown:
            self.b.Hide()
            self._shown = False


def _Line(parent, keep, color):
    l = ui.Line()
    l.SetParent(parent)
    l.AddFlag("not_pick")
    l.SetColor(color)
    l.Show()
    keep.append(l)
    return l


def _SetLine(l, x0, y0, x1, y1):
    xi = int(round(x0))
    yi = int(round(y0))
    l.SetPosition(xi, yi)
    l.SetSize(int(round(x1)) - xi, int(round(y1)) - yi)


class _Route:
    """Iki isaretci arasi egri (routePath: ikinci dereceden Bezier), golge + akan
    kesikler + uzerinde sabit hizla kayan isik topu (animateMotion paced)."""

    SAMPLES = 32

    def __init__(self, host, keep, a, b, lift, color):
        cx = (a[0] + b[0]) / 2.0
        cy = (a[1] + b[1]) / 2.0 - lift
        self.pts = []
        for i in xrange(self.SAMPLES + 1):
            t = float(i) / self.SAMPLES
            u = 1.0 - t
            self.pts.append((u * u * a[0] + 2 * u * t * cx + t * t * b[0],
                             u * u * a[1] + 2 * u * t * cy + t * t * b[1]))
        self.cum = [0.0]
        for i in xrange(1, len(self.pts)):
            (x0, y0) = self.pts[i - 1]
            (x1, y1) = self.pts[i]
            self.cum.append(self.cum[-1] + math.hypot(x1 - x0, y1 - y0))
        self.length = max(1.0, self.cum[-1])
        # golge (surekli, sabit)
        for i in xrange(1, len(self.pts), 2):
            j = min(len(self.pts) - 1, i + 1)
            _SetLine(_Line(host, keep, C_ROUTE_SHADOW), self.pts[i - 1][0], self.pts[i - 1][1] + 1,
                     self.pts[j][0], self.pts[j][1] + 1)
        # kesikler: 19 tam sayi fazin (DASH_ON + DASH_OFF) her biri icin dikdortgenler
        # bir kez hesaplanir; karede yalniz faz degisince ve yalniz degisen cizgi yazilir.
        period = int(DASH_ON + DASH_OFF)
        n = int(self.length / period) + 2
        dash_color = _AlphaColor(0xff000000 | color, 0.62)
        self.dashes = [_Line(host, keep, dash_color) for i in xrange(n)]
        self.cur = [None] * n
        self.phases = [self.__Rects(float(ph), n) for ph in xrange(period)]
        self.lastPhase = -1
        # isik topu
        self.glow = _Spr(host, V2 + "orb_glow.png", keep)
        self.core = _Spr(host, V2 + "orb_core.png", keep)
        self.glow.Alpha(0.9, color)
        (x, y) = self.pts[0]
        self.glow.Place(x - 16, y - 16, 0.5)
        self.core.Place(x - 4.5, y - 4.5, 0.375)
        self.color = color
        self.__Apply(0)

    def __At(self, s):
        """yay uzunlugu s -> nokta"""
        if s <= 0.0:
            return self.pts[0]
        if s >= self.length:
            return self.pts[-1]
        lo = 0
        hi = len(self.cum) - 1
        while hi - lo > 1:
            mid = (lo + hi) / 2
            if self.cum[mid] < s:
                lo = mid
            else:
                hi = mid
        seg = self.cum[hi] - self.cum[lo]
        f = 0.0 if seg <= 0 else (s - self.cum[lo]) / seg
        (x0, y0) = self.pts[lo]
        (x1, y1) = self.pts[hi]
        return (x0 + (x1 - x0) * f, y0 + (y1 - y0) * f)

    def __Rects(self, phase, n):
        period = DASH_ON + DASH_OFF
        out = []
        for i in xrange(n):
            s0 = i * period + phase - period
            s1 = s0 + DASH_ON
            if s1 <= 0.0 or s0 >= self.length:
                out.append(None)
                continue
            (x0, y0) = self.__At(max(0.0, s0))
            (x1, y1) = self.__At(min(self.length, s1))
            xi = int(round(x0))
            yi = int(round(y0))
            out.append((xi, yi, int(round(x1)) - xi, int(round(y1)) - yi))
        return out

    def __Apply(self, ph):
        if ph == self.lastPhase:
            return
        self.lastPhase = ph
        rects = self.phases[ph]
        for i in xrange(len(self.dashes)):
            r = rects[i]
            c = self.cur[i]
            if r == c:
                continue
            l = self.dashes[i]
            if r is None:
                l.Hide()
            else:
                if c is None or c[0] != r[0] or c[1] != r[1]:
                    l.SetPosition(r[0], r[1])
                if c is None or c[2] != r[2] or c[3] != r[3]:
                    l.SetSize(r[2], r[3])
                if c is None:
                    l.Show()
            self.cur[i] = r

    def Reset(self):
        """onbellekten yeniden gosterildi: gizli olmasi gereken kesikler dahil hepsi Show edilmisti -> sifirla."""
        for l in self.dashes:
            l.Hide()
        self.cur = [None] * len(self.dashes)
        self.lastPhase = -1
        self.__Apply(0)

    def Tick(self, now):
        if ROUTE_FLOW:
            self.__Apply(int(now * DASH_SPEED) % len(self.phases))
        (x, y) = self.__At(((now % ORB_PERIOD) / ORB_PERIOD) * self.length)
        self.glow.Place(x - 16, y - 16, 0.5)
        self.core.Place(x - 4.5, y - 4.5, 0.375)


class _Summon(ui.Window):
    """.summon: ruh muhru acilis perdesi (tasarim: 1.75 s bekler, .55 s solar).
    Tum ekrani kaplar ve dokunmayi yutar."""

    def __init__(self):
        ui.Window.__init__(self, "TOP_MOST")
        if hasattr(wndMgr, "SetUIScale"):
            wndMgr.SetUIScale(self.hWnd, 1.0)
        self.SetWindowName("TeleportSummon")
        self.AddFlag("float")
        self.keep = []
        SW = wndMgr.GetScreenWidth()
        SH = wndMgr.GetScreenHeight()
        self.SetPosition(0, 0)
        self.SetSize(SW, SH)
        self.cx = SW / 2.0
        self.cy = SH / 2.0
        self.bg = _Spr(self, V2 + "summon_bg.jpg", self.keep)
        self.bg.Stretch(0, 0, SW, SH)
        self.ringOut = _Spr(self, V2 + "summon_ring_out.png", self.keep)
        self.ringIn = _Spr(self, V2 + "summon_ring_in.png", self.keep)
        self.rune = _Spr(self, V2 + "summon_rune.png", self.keep)
        self.text = _Spr(self, V2 + "summon_text.png", self.keep)
        (tw, th, ts, tcx, tcy, tdy) = SUMMON_TEXT
        self.text.Place(self.cx - tcx, self.cy + tdy - tcy, 1.0 / ts)
        self.t0 = app.GetTime()

    def __del__(self):
        ui.Window.__del__(self)

    def Start(self):
        self.t0 = app.GetTime()
        self.Show()
        self.SetTop()
        self.OnUpdate()

    def OnUpdate(self):
        t = app.GetTime() - self.t0
        if t >= SUMMON_HOLD + SUMMON_FADE:
            self.Hide()
            return
        a = 1.0 - _Clamp01((t - SUMMON_HOLD) / SUMMON_FADE)
        self.bg.Alpha(a)
        self.text.Alpha(a)
        # :before 230 px kesikli halka 2.4 s saat yonu, :after 160 px 1.6 s ters
        self.ringOut.Center(self.cx, self.cy, 0.5, (t / 2.4) * 360.0 % 360.0)
        self.ringIn.Center(self.cx, self.cy, 0.5, 360.0 - (t / 1.6) * 360.0 % 360.0)
        self.ringOut.Alpha(a)
        self.ringIn.Alpha(a)
        # runeBurst 1.7 s: 0% scale .2 rot -120 op 0 / 45% scale 1 op 1 / 80%..100% scale 2.8 op 0
        p = _Clamp01(t / RUNE_BURST)
        if p < 0.45:
            e = _EaseInOut(p / 0.45)
            sc = 0.2 + 0.8 * e
            rot = -120.0 * (1.0 - e)
            op = e
        elif p < 0.8:
            e = _EaseInOut((p - 0.45) / 0.35)
            sc = 1.0 + 1.8 * e
            rot = 0.0
            op = 1.0 - e
        else:
            sc = 2.8
            rot = 0.0
            op = 0.0
        (rw, rh, rs, rcx, rcy, rdy) = SUMMON_RUNE
        self.rune.Center(self.cx, self.cy + rdy, sc / rs, rot)
        self.rune.Alpha(op * a)

    def OnMouseLeftButtonDown(self):
        return True

    def OnMouseLeftButtonUp(self):
        return True


class TeleportMapWindow(ui.Window):

    def __init__(self):
        ui.Window.__init__(self, "TOP_MOST")
        if hasattr(wndMgr, "SetUIScale"):
            wndMgr.SetUIScale(self.hWnd, 1.0)   # kendi geometrisi var, genel olcek disi
        self.SetWindowName("TeleportMapWindow")
        self.AddFlag("float")                    # SetTop yalniz FLAG_FLOAT ile calisir
        self.keep = []                           # TUM cocuklarin referansi (bkz. bastaki TUZAK)
        self.built = False
        self.markers = []
        self.routes = []
        self.routeKeep = []
        self.tabs = []
        self.touches = []
        self.cat = None
        self.cur = None
        self.curMarker = None
        self.measure = None
        self.summon = None
        self.trans = None           # ("out"|"in", t0, cat)
        self.mapBase = None         # (x, y, w, h, tex_scale)
        self.mapA = 1.0             # son yazilan harita alfasi / yakinlasmasi (gecis devri icin)
        self.mapZ = 1.0
        self.kingdom = None         # (anahtar, t0)
        self.kPose = (0.0, 0.0, 1.0)  # etkin parcanin son (alfa, ty, olcek)
        self.kLeave = None          # inen eski parca (anahtar, t0, a0, ty0, sc0)
        self.swapT0 = -10.0
        self.swapActive = False

    def __del__(self):
        ui.Window.__del__(self)

    # ---------------------------------------------------------------- yardimcilar
    def _Bar(self, x, y, w, h, color, parent=None):
        b = ui.Bar()
        b.SetParent(parent or self)
        b.AddFlag("not_pick")
        b.SetPosition(int(x), int(y))
        b.SetSize(int(w), int(h))
        b.SetColor(color)
        b.Show()
        self.keep.append(b)
        return b

    def _Box(self, x, y, w, h, color, parent=None):
        b = ui.Box()
        b.SetParent(parent or self)
        b.AddFlag("not_pick")
        b.SetPosition(int(x), int(y))
        b.SetSize(int(w), int(h))
        b.SetColor(color)
        b.Show()
        self.keep.append(b)
        return b

    def _Text(self, x, y, text, font, color, align="left", parent=None):
        t = ui.TextLine()
        t.SetParent(parent or self)
        t.AddFlag("not_pick")
        t.SetFontName(font)
        t.SetPackedFontColor(color)
        if align == "center":
            t.SetHorizontalAlignCenter()
        elif align == "right":
            t.SetHorizontalAlignRight()
        t.SetPosition(int(x), int(y))
        t.SetText(text)
        t.Show()
        self.keep.append(t)
        return t

    def _Host(self, x, y, w, h, parent=None):
        h_ = ui.Window()
        h_.SetParent(parent or self)
        h_.AddFlag("not_pick")
        h_.SetPosition(int(x), int(y))
        h_.SetSize(int(w), int(h))
        h_.Show()
        self.keep.append(h_)
        return h_

    def _Measure(self, text, font):
        if self.measure is None:
            self.measure = ui.TextLine()
            self.measure.SetParent(self)
            self.measure.Hide()
        self.measure.SetFontName(font)
        self.measure.SetText(text)
        return self.measure.GetTextSize()[0]

    def _VGradient(self, x, y, w, h, top, bottom, steps=6, parent=None):
        bars = []
        for i in xrange(steps):
            t = (i + 0.5) / steps
            y0 = y + (h * i) / steps
            y1 = y + (h * (i + 1)) / steps
            bars.append(self._Bar(x, y0, w, max(1, y1 - y0), 0xff000000 | _Mix(bottom, top, t), parent))
        return bars

    # ---------------------------------------------------------------- kurulum
    def __Build(self):
        SW = wndMgr.GetScreenWidth()
        SH = wndMgr.GetScreenHeight()
        self.SetPosition(0, 0)
        self.SetSize(SW, SH)
        B = BORDER
        bx = B
        by = B + TOPBAR_H
        bw = SW - 2 * B - INFO_W
        bh = SH - 2 * B - TOPBAR_H
        self.box = (bx, by, bw, bh)
        infoX = bx + bw
        infoY = by

        self._Bar(0, 0, SW, SH, C_PORTAL)

        # ---- harita kutusu (.map-wrap) katmanlari, z sirasiyla
        self.sprWrapBg = _Spr(self, V2 + "wrap_bg.jpg", self.keep)
        self.sprWrapBg.Stretch(bx, by, bw, bh)
        self.mapImg = ui.ExpandedImageBox()
        self.mapImg.SetParent(self)
        self.mapImg.AddFlag("not_pick")
        self.mapImg.Show()
        self.keep.append(self.mapImg)
        self.sprLight = _Spr(self, V2 + "wrap_light.png", self.keep)           # :before (z1)
        self.sprLight.Stretch(bx, by, bw, bh)
        self.routeHost = self._Host(0, 0, SW, SH)                                # rotalar (z3)
        self.kingSpr = {}
        for k in ("yellow", "blue", "red"):                                      # krallik (z4)
            s = _Spr(self, V2 + "kingdom_%s.png" % k, self.keep)
            s.Hide()
            self.kingSpr[k] = s
        self.sprVig = _Spr(self, V2 + "wrap_vignette.png", self.keep)           # :after (z6)
        self.sprVig.Stretch(bx, by, bw, bh)
        self.markerHost = self._Host(0, 0, SW, SH)                               # isaretciler (z7)

        # ---- sekmeler (.realm-tabs, z8) - kullanici boyutu
        tabY = by + TAB_TOP
        self.tabBottom = tabY + TAB_H
        self._Bar(bx + 16, tabY, bw - 32, TAB_H, C_TABBG)
        self._Box(bx + 16, tabY, bw - 32, TAB_H, C_TABBORDER)
        x = bx + 16 + 5
        self.tabs = []
        tabRects = []
        for (key, label, realm, qkey) in CATEGORIES:
            tw = 18 + TAB_ICON + 8 + self._Measure(label, TAB_FONT) + 18
            bar = self._Bar(x, tabY + 5, tw, TAB_H - 10, 0x00000000)
            box = self._Box(x, tabY + 5, tw, TAB_H - 10, 0x00000000)
            ic = _Spr(self, DIR + "tab_%s.png" % key, self.keep)
            ic.Place(x + 18, tabY + (TAB_H - TAB_ICON) / 2, TAB_ICON / 52.0)
            txt = self._Text(x + 18 + TAB_ICON + 8, tabY + (TAB_H - 21) / 2, label, TAB_FONT, C_TABTXT)
            self.tabs.append((key, bar, box, txt))
            tabRects.append((key, x, tw))
            x = x + tw + 5

        # ---- KONUM kutusu (.coordinates: left 17, bottom 15). Portal tam ekran oldugu
        # icin sol-alt kose susu kutunun ustune biniyordu ("KONUM" okunmuyordu):
        # susun sagina alindi.
        self.coordX = int(max(bx + 17, CORNERS["bl"][0] + CORNERS["bl"][2] + 6))
        self.coordY = by + bh - 15 - 29
        self.coordBg = self._Bar(self.coordX, self.coordY, 120, 29, C_COORD_BG)
        self.coordBox = self._Box(self.coordX, self.coordY, 120, 29, C_COORD_BORDER)
        self.coordLbl = self._Text(self.coordX + 11, self.coordY + 7, "KONUM", "Tahoma:11", C_COORD_TXT)
        self.coordVal = self._Text(self.coordX + 11, self.coordY + 7, "", "Tahoma:12", 0xff5dcfff)

        # ---- bilgi paneli (.info): zemin sabit, icerik infoHost'ta kayar
        self._VGradient(infoX, infoY, INFO_W, bh, C_INFO1, C_INFO2)
        self._Bar(infoX, infoY, 1, bh, C_LINE)
        self.infoX = infoX
        self.infoY = infoY
        self.infoHost = self._Host(infoX, infoY, INFO_W, bh)
        H = self.infoHost
        cx = (INFO_W - 86) / 2
        cy = PAD + 8
        self.crestRing = _Spr(H, DIR + "crest_ring.png", self.keep)
        self.crestRing.Place(cx, cy, 0.5)
        self.crestIcon = _Spr(H, DIR + "icon_00.png", self.keep)
        self.crestIcon.Place(cx + 21, cy + 21, 0.5)
        yy = cy + 86 + 17
        self.txtRealm = self._Text(INFO_W / 2, yy, "", "Tahoma:12", 0xff5dcfff, "center", H)
        yy = yy + 15 + 7
        self.txtName = self._Text(INFO_W / 2, yy, "", "Tahoma:25", C_NAME, "center", H)
        yy = yy + 30 + 10
        self.descLines = []
        for i in xrange(4):
            self.descLines.append(self._Text(INFO_W / 2, yy + i * 21, "", "Tahoma:13", C_DESC, "center", H))
        btnH = 62
        btnY = bh - PAD - btnH
        rowH = 38
        gap = 9
        statTop = btnY - 18 - (3 * rowH + 2 * gap)
        self.stats = []
        labels = ("B\xf6lge", "Seviye", "Durum")
        for i in xrange(3):
            ry = statTop + i * (rowH + gap)
            self._Text(PAD, ry + 11, labels[i], "Tahoma:13", C_STATL, "left", H)
            v = self._Text(INFO_W - PAD, ry + 11, "", "Tahoma:13", C_STATV, "right", H)
            self._Bar(PAD, ry + rowH - 1, INFO_W - 2 * PAD, 1, C_LINE, H)
            self.stats.append(v)
        self.btnBars = []
        for i in xrange(5):
            self.btnBars.append(self._Bar(PAD, btnY + (btnH * i) / 5, INFO_W - 2 * PAD,
                                          btnH / 5 + 1, 0xff202634, H))
        self.btnBox = self._Box(PAD, btnY, INFO_W - 2 * PAD, btnH, 0xff5dcfff, H)
        self.btnText = self._Text(INFO_W / 2, btnY + 14, "I\xfe\xfdnlan", "Tahoma:16", 0xffffffff, "center", H)
        self.btnCost = self._Text(INFO_W / 2, btnY + 38, "\xdccretsiz", "Tahoma:11", C_BTN_SMALL, "center", H)
        # panelSwap solmasi: panel zemini renginde ortu, alfa 1 -> 0
        self.infoFade = self._VGradient(infoX, infoY, INFO_W, bh, C_INFO1, C_INFO2, 6)
        for b in self.infoFade:
            b.Hide()

        # ---- ust bar (.topbar)
        self._VGradient(B, B, SW - 2 * B, TOPBAR_H, C_TOP1, C_TOP2, 4)
        self._Bar(B, B + TOPBAR_H - 1, SW - 2 * B, 1, C_LINE)
        rune = _Spr(self, V2 + "rune.png", self.keep)
        (rw, rh, rs) = RUNE
        rune.Place(B + 26 + 19.5 - rw / 2.0, B + TOPBAR_H / 2.0 - rh / 2.0, 1.0 / rs)
        (tw_, th_, ts_) = TITLE
        titleX = B + 26 + 39 + 13
        _Spr(self, V2 + "title.png", self.keep).Place(titleX, B + 19, 1.0 / ts_)
        self._Text(titleX, B + 45, "Var\xfd\xfe noktan\xfd haritadan se\xe7", "Tahoma:12", C_SUB)
        (cw_, ch_, cs_) = CLOSE
        closeX = SW - B - 26 - cw_
        closeY = B + (TOPBAR_H - ch_) / 2.0
        _Spr(self, V2 + "close.png", self.keep).Place(closeX, closeY, 1.0 / cs_)

        # ---- portal cercevesi (border 2px + inset + :before 10 px) ve kose susleri
        self._Box(0, 0, SW, SH, C_PORTAL_BORDER)
        self._Box(1, 1, SW - 2, SH - 2, C_PORTAL_BORDER)
        self._Box(2, 2, SW - 4, SH - 4, C_PORTAL_INSET)
        self._Box(10, 10, SW - 20, SH - 20, C_PORTAL_FRAME)
        for c in ("tl", "tr", "bl", "br"):
            (ox, oy, w_, h_, s_, fr, fb) = CORNERS[c]
            x_ = ox if c in ("tl", "bl") else SW - fr
            y_ = oy if c in ("tl", "tr") else SH - fb
            _Spr(self, V2 + "corner_%s.png" % c, self.keep).Place(x_, y_, 1.0 / s_)

        # ---- dokunma alanlari (en ustte)
        self.touches = []
        for (key, tx, tw) in tabRects:
            self.touches.append(_Touch(ui.__mem_func__(self.SelectCategory), key)
                                .Place(self, tx, tabY, tw, TAB_H))
        self.touches.append(_Touch(_Cancel).Place(self, closeX - 10, closeY - 10, cw_ + 20, ch_ + 20))
        self.touches.append(_Touch(ui.__mem_func__(self.OnTeleportButton))
                            .Place(self, infoX + PAD, infoY + btnY, INFO_W - 2 * PAD, btnH))
        self.built = True

    # ---------------------------------------------------------------- yerlesim
    def __Layout(self, cat):
        """Kategori icin (harita dosyasi, harita dortgeni, doku olcegi, pin merkezleri,
        rota egimi, krallik donusum bilgisi)."""
        (bx, by, bw, bh) = self.box
        dests = [(i, DESTS[i]) for i in xrange(len(DESTS)) if DESTS[i].cat == cat]
        if cat == "village":
            # koy gorunumu: tasarimin referans kutusu (REF_W x REF_H) ESIT olcekle
            # kutuya sigdirilir (tasarimda da harita "contain")
            k = min(bw / REF_W, bh / REF_H)
            ox = bx + (bw - REF_W * k) / 2.0
            oy = by + (bh - REF_H * k) / 2.0
            (vx, vy, vw, vh, vs) = VILLAGE_MAP
            mapRect = (ox + vx * k, oy + vy * k, vw * k, vh * k, k / vs)
            pins = [(ox + d.ref[0] * k, oy + d.ref[1] * k) for (i, d) in dests]
            self.villageK = (ox, oy, k)
            return (V2 + "village_map.png", mapRect, pins, ROUTE_LIFT * REF_H * k)
        # kaplama haritalari: "cover" x 1.02 (tasarim .map transform)
        s = max(bw / COVER_W, bh / COVER_H) * 1.02
        W = COVER_W * s
        H = COVER_H * s
        left = bx + (bw - W) / 2.0
        top = by + (bh - H) / 2.0
        pins = [(left + d.fx * W, top + d.fy * H) for (i, d) in dests]
        # dikey kaydirma: isaretciler sekme seridinin altinda / kutunun icinde
        # kalsin ama gorsel kutuyu ortmeye devam etsin - cografya kaymaz.
        minY = self.tabBottom + PIN_D / 2 + 8
        maxY = by + bh - (LABEL_GAP + LABEL_H + 10)
        dy = 0.0
        if pins:
            hi = min([p[1] for p in pins])
            lo = max([p[1] for p in pins])
            if hi < minY:
                dy = minY - hi
            if lo + dy > maxY:
                dy = maxY - lo
            dy = max(by + bh - (top + H), min(by - top, dy))
        pins = [(p[0], p[1] + dy) for p in pins]
        if cat in CENTER_CATS:
            dy = 0.0
            mid = (self.tabBottom + by + bh) / 2.0
            # isaretci blogu (pin ustu -25 .. etiket alti +66) dikeyde ortalanir
            pins = [(bx + bw / 2.0, mid - (LABEL_GAP + LABEL_H - PIN_D / 2.0) / 2.0) for p in pins]
        return (V2 + "map_%s.jpg" % cat, (left, top + dy, W, H, s), pins, ROUTE_LIFT * bh)

    def __PlaceMap(self, zoom, alpha):
        if not self.mapBase:
            return
        (x, y, w, h, ts) = self.mapBase
        (bx, by, bw, bh) = self.box
        cx = bx + bw / 2.0
        cy = by + bh / 2.0
        x2 = cx + (x - cx) * zoom
        y2 = cy + (y - cy) * zoom
        self.mapImg.SetScale(ts * zoom, ts * zoom)
        self.mapImg.SetPosition(int(x2), int(y2))
        self.mapImg.SetSize(1, 1)
        _Tint(self.mapImg, 0xffffff, _Clamp01(alpha))
        self.mapZ = zoom
        self.mapA = _Clamp01(alpha)

    def __ApplyCategory(self, cat, anim=False):
        (path, rect, pins, lift) = self.__Layout(cat)
        _SafeLoad(self.mapImg, path)
        self.mapBase = rect
        self.__PlaceMap(1.0, 1.0)
        # eski isaretci/rotalar: gizlenir (silinmez - onbellekte)
        for m in self.markers:
            m.Hide()
        for r in self.routeKeep:
            r.Hide()
        self.__SetKingdom(None)
        cache = self.__dict__.setdefault("catCache", {})
        if cat in cache:
            (self.markers, self.routes, self.routeKeep) = cache[cat]
            for m in self.markers:
                m.Show()
            for r in self.routeKeep:
                r.Show()
            for rt in self.routes:
                rt.Reset()
            if self.markers:
                self.SelectMarker(self.markers[0], anim)
            return
        self.markers = []
        self.routeKeep = []
        self.routes = []
        dests = [(i, DESTS[i]) for i in xrange(len(DESTS)) if DESTS[i].cat == cat]
        # rotalar (isaretcilerin ALTINDA, route-layer z3)
        for j in xrange(len(pins) - 1):
            self.routes.append(_Route(self.routeHost, self.routeKeep, pins[j], pins[j + 1], lift,
                                      dests[j + 1][1].color))
        now = app.GetTime()
        order = 0
        for ((i, d), p) in zip(dests, pins):
            self.markers.append(_Marker(self, d, i, p[0], p[1], now + order * MARKER_STAGGER))
            order = order + 1
        cache[cat] = (self.markers, self.routes, self.routeKeep)
        if self.markers:
            self.SelectMarker(self.markers[0], anim)

    def __SetKingdom(self, key):
        if key is not None and self.kingdom and self.kingdom[0] == key:
            return
        if key is None:
            # sert sifirlama (kategori degisimi): hepsi aninda gizlenir
            for s in self.kingSpr.values():
                s.Hide()
            self.kingdom = None
            self.kLeave = None
            return
        # tasarim: 'active' kalkinca eski parca .38 s solarak, .5 s'de yerine iner
        if self.kLeave:
            self.kingSpr[self.kLeave[0]].Hide()
            self.kLeave = None
        if self.kingdom and self.kingdom[0] != key:
            (a0, ty0, sc0) = self.kPose
            self.kLeave = (self.kingdom[0], app.GetTime(), a0, ty0, sc0)
        for (k, s) in self.kingSpr.items():
            if k != key and not (self.kLeave and k == self.kLeave[0]):
                s.Hide()
        self.kingdom = (key, app.GetTime())
        self.kingSpr[key].Show()
        self.__TickKingdom(app.GetTime())

    def __PlaceKingdom(self, key, ty, sc, a):
        (ox, oy, k) = self.villageK
        (kx, ky, kw, kh, ks) = KINGDOMS[key]
        (lx, ly, lw, lh) = KINGDOM_LAYER
        ccx = ox + (lx + lw / 2.0) * k
        ccy = oy + (ly + lh / 2.0) * k
        px = ox + kx * k
        py = oy + ky * k
        spr = self.kingSpr[key]
        spr.Place(ccx + (px - ccx) * sc, ccy + (py - ccy) * sc + ty * k, (k / ks) * sc)
        spr.Alpha(a)

    def __TickKingdom(self, now):
        if self.cat != "village":
            return
        if self.kLeave:
            (lk, t0, a0, ty0, sc0) = self.kLeave
            dt = now - t0
            e = _EaseOut(dt / 0.5)
            self.__PlaceKingdom(lk, ty0 * (1.0 - e), 1.0 + (sc0 - 1.0) * (1.0 - e),
                                a0 * (1.0 - _Clamp01(dt / 0.38)))
            if dt >= 0.5:
                self.kingSpr[lk].Hide()
                self.kLeave = None
        if not self.kingdom:
            return
        (key, t0) = self.kingdom
        # etkinlesme gecisi (opacity .38s, transform .5s) + realmFloat 2.6s; dalga t0'dan
        # baslar (Chrome'da da faz 0) - lift(0)=0 oldugundan hareket sureklidir.
        a = _Clamp01((now - t0) / 0.38)
        lift = _EaseOut((now - t0) / 0.5)
        w = _Wave(now - t0, FLOAT_PERIOD)
        ty = (-10.0 - 4.0 * w) * lift
        sc = 1.0 + (0.025 + 0.007 * w) * lift
        self.__PlaceKingdom(key, ty, sc, a)
        self.kPose = (a, ty, sc)

    # ---------------------------------------------------------------- secim
    def SelectMarker(self, marker, anim=True):
        for m in self.markers:
            m.SetSelected(m is marker)
        self.cur = marker.dest
        self.curMarker = marker
        d = marker.dest
        if d.cat == "village":
            self.__SetKingdom(d.kingdom)
        self.__RefreshInfo(d, marker.index)
        self.__RefreshTabs(d.color)
        if anim:
            self.swapT0 = app.GetTime()
            self.__TickSwap(self.swapT0)

    def __RefreshTabs(self, col):
        for (key, bar, box, txt) in self.tabs:
            if key == self.cat:
                bar.SetColor(0xff000000 | _Mix(col, 0x15161b, 0.26))
                box.SetColor(_A(140, col))          # inset 0 0 0 1px color-mix(realm 55%)
                txt.SetPackedFontColor(0xffffffff)
            else:
                bar.SetColor(0x00000000)
                box.SetColor(0x00000000)
                txt.SetPackedFontColor(C_TABTXT)

    def __RefreshInfo(self, d, index):
        col = 0xff000000 | d.color
        _Tint(self.crestRing.b, _Mix(d.color, 0x604921, 0.6))
        _SafeLoad(self.crestIcon.b, DIR + "icon_%02d.png" % index)
        self.crestIcon.b.SetScale(0.5, 0.5)
        self.crestIcon.b.SetSize(44, 44)
        self.txtRealm.SetPackedFontColor(col)
        for (key, label, realm, qkey) in CATEGORIES:
            if key == d.cat:
                self.txtRealm.SetText(realm)
                break
        self.txtName.SetText(d.name)
        self.__SetDesc(d.desc)
        self.stats[0].SetText(d.region)
        self.stats[1].SetText(d.level)
        self.stats[2].SetText(d.status)
        if d.status == "G\xfcvenli" or d.status == "Etkinlik":
            self.stats[2].SetPackedFontColor(C_SAFE)
        else:
            self.stats[2].SetPackedFontColor(C_RISK)
        # .teleport: gradient(color-mix(realm 33%,#282015) -> color-mix(realm 12%,#0d0e12))
        top = _Mix(d.color, 0x282015, 0.33)
        bot = _Mix(d.color, 0x0d0e12, 0.12)
        n = len(self.btnBars)
        for i in xrange(n):
            self.btnBars[i].SetColor(0xff000000 | _Mix(bot, top, (i + 0.5) / n))
        self.btnBox.SetColor(0xff000000 | _Mix(d.color, 0xb7893c, 0.75))
        # KONUM  xx : yy  (tasarimdaki yuzdeler, iki haneli)
        if d.cat in CENTER_CATS:
            val = "50 : 50"
        else:
            val = "%02d : %02d" % (d.x, d.y)
        self.coordVal.SetText(val)
        self.coordVal.SetPackedFontColor(col)
        w1 = self._Measure("KONUM", "Tahoma:11")
        w2 = self._Measure(val, "Tahoma:12")
        self.coordVal.SetPosition(int(self.coordX + 11 + w1 + 7), int(self.coordY + 7))
        self.coordBg.SetSize(11 + w1 + 7 + w2 + 11, 29)
        self.coordBox.SetSize(11 + w1 + 7 + w2 + 11, 29)

    def __SetDesc(self, text):
        width = INFO_W - 2 * PAD
        lines = []
        cur = ""
        for w in text.split(" "):
            cand = (cur + " " + w) if cur else w
            if not cur or self._Measure(cand, "Tahoma:13") <= width:
                cur = cand
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for i in xrange(len(self.descLines)):
            self.descLines[i].SetText(lines[i] if i < len(lines) else "")

    def __TickSwap(self, now):
        """panelSwap .32s: icerik 12 px sagdan kayarak ve belirerek gelir"""
        p = (now - self.swapT0) / PANEL_SWAP
        if p >= 1.0:
            if self.swapActive:
                for b in self.infoFade:
                    b.Hide()
                self.infoHost.SetPosition(self.infoX, self.infoY)
                self.swapActive = False
            return
        self.swapActive = True
        e = _EaseOut(p)
        self.infoHost.SetPosition(int(self.infoX + 12 * (1.0 - e)), self.infoY)
        a = 1.0 - e
        for i in xrange(len(self.infoFade)):
            t = (i + 0.5) / len(self.infoFade)
            self.infoFade[i].SetColor(_AlphaColor(0xff000000 | _Mix(C_INFO2, C_INFO1, t), a))
            self.infoFade[i].Show()

    def SelectCategory(self, cat):
        if cat == self.cat:
            return                      # zaten gosteriliyor ya da yukleniyor
        now = app.GetTime()
        if self.trans and self.trans[0] == "out":
            t0 = self.trans[1]          # solmaya devam, yalniz hedef degisir
        elif self.trans:
            # "in" evresi: mevcut alfadan geriye solmaya baslanir (sicrama yok)
            t0 = now - (1.0 - self.mapA) * MAP_OUT
        else:
            t0 = now
        self.cat = cat
        self.__RefreshTabs(self.cur.color if self.cur else 0x5dcfff)
        # renderCategory: harita solar/yakinlasir, isaretciler + krallik gizlenir;
        # rotalar (route-layer) tasarimda 260 ms boyunca yerinde kalir.
        for m in self.markers:
            m.Hide()
        self.__SetKingdom(None)
        self.trans = ("out", t0, cat)

    def OnTeleportButton(self):
        # yalniz eski harita solarken engellenir; "in" evresinde yeni hedef zaten secili
        if self.cur and not (self.trans and self.trans[0] == "out"):
            _RequestTeleport(self.cur)

    # ---------------------------------------------------------------- kare
    def OnUpdate(self):
        now = app.GetTime()
        if now < self.__dict__.get("lastNow", 0.0) - 0.5:
            self.__Rebase(now)
        self.lastNow = now
        if self.trans:
            (phase, t0, cat) = self.trans
            if phase == "out":
                p = _Clamp01((now - t0) / MAP_OUT)
                self.__PlaceMap(1.0 + 0.07 * _EaseOut(p), 1.0 - p)
                if p >= 1.0:
                    self.__ApplyCategory(cat, True)
                    self.trans = ("in", now, cat)
                    self.__PlaceMap(1.07, 0.0)
            else:
                pa = _Clamp01((now - t0) / MAP_IN)
                pz = _EaseOut((now - t0) / MAP_ZOOM_BACK)
                self.__PlaceMap(1.07 - 0.07 * pz, pa)
                if pa >= 1.0 and pz >= 1.0:
                    self.trans = None
                    self.__PlaceMap(1.0, 1.0)
        if now >= g_summonUntil[0]:
            for r in self.routes:
                r.Tick(now)
        self.__TickKingdom(now)
        self.__TickSwap(now)

    # ---------------------------------------------------------------- yasam
    ## KULLANICI (2026-09-28): "isinlanma yerleri yok" (bazen). app.GetTime() her yeni sunucu baglantisinda
    ## SIFIRDAN baslar (handshake -> CTimer::SetBaseTime); bu pencere ve isaretci onbellegi (catCache) ise
    ## isinlanmalar arasinda yasiyor. Eski zamanlar (isaretci tIn, panel swapT0) "gelecekte" kalinca isaretciler
    ## alfa 0'da takiliyor, bilgi paneli yarim kayik/soluk kaliyordu. Zaman geri gidince hepsi simdiye cekilir.
    def __Rebase(self, now):
        for (markers, routes, keep) in self.__dict__.get("catCache", {}).values():
            for m in markers:
                if m.tIn > now:
                    m.tIn = now - MARKER_IN
                    m.settled = False
        if self.swapT0 > now:
            self.swapT0 = -10.0
        if self.trans and self.trans[1] > now:
            self.trans = (self.trans[0], now, self.trans[2])
        if self.kingdom and self.kingdom[1] > now:
            self.kingdom = (self.kingdom[0], now - 1.0)
        if self.kLeave and self.kLeave[1] > now:
            self.kLeave = None

    def Open(self):
        if not self.built:
            self.__Build()
        self.__Rebase(app.GetTime())
        self.lastNow = app.GetTime()
        self.trans = None
        self.cat = "village"
        self.__RefreshTabs(0x5dcfff)
        self.__ApplyCategory("village")
        self.Show()
        self.SetTop()
        g_summonUntil[0] = 0.0		# acilis perdesi (2.3 s) kaldirildi - pencere aninda

    def CloseSelf(self):
        self.Hide()
        if self.summon:
            self.summon.Hide()

    def OnPressEscapeKey(self):
        if g_flow and g_flow.stage == STAGE_PICK:
            _Cancel()
        return True

    def OnMouseLeftButtonDown(self):
        return True

    def OnMouseLeftButtonUp(self):
        return True


class _Marker(ui.Window):
    """.marker: pin (3 sprite: normal / secili / secili-parlak) + halka nabzi +
    cerceveli ad. Tum dortgen dokunulabilir; cocuklar not_pick."""

    def __init__(self, owner, dest, index, cx, cy, tIn):
        ui.Window.__init__(self)
        self.SetParent(owner.markerHost)
        self.onClick = ui.__mem_func__(owner.SelectMarker)
        self.dest = dest
        self.index = index
        self.cx = cx
        self.cy = cy
        self.tIn = tIn
        self.selected = False
        self.keep = []
        self.labelW = owner._Measure(dest.name, LABEL_FONT) + 22
        w = max(PIN_D + 16, self.labelW)
        self.ox = cx - w / 2.0
        self.oy = cy - PIN_D / 2.0 - 8
        self.SetPosition(int(self.ox), int(self.oy))
        self.SetSize(int(w), int(PIN_D / 2.0 + 8 + LABEL_GAP + LABEL_H))

        self.halo = _Spr(self, DIR + "pulse.png", self.keep)
        self.pinN = _Spr(self, V2 + "pin_%02d_n.png" % index, self.keep)
        self.pinS = _Spr(self, V2 + "pin_%02d_s.png" % index, self.keep)
        self.pinB = _Spr(self, V2 + "pin_%02d_b.png" % index, self.keep)
        self.pinS.Hide()
        self.pinB.Hide()
        self.lblBars = []
        for i in xrange(2):
            b = ui.Bar()
            b.SetParent(self)
            b.AddFlag("not_pick")
            b.Show()
            self.keep.append(b)
            self.lblBars.append(b)
        self.lblBox = ui.Box()
        self.lblBox.SetParent(self)
        self.lblBox.AddFlag("not_pick")
        self.lblBox.Show()
        self.keep.append(self.lblBox)
        self.label = ui.TextLine()
        self.label.SetParent(self)
        self.label.AddFlag("not_pick")
        self.label.SetFontName(LABEL_FONT)
        self.label.SetHorizontalAlignCenter()
        self.label.SetText(dest.name)
        self.label.Show()
        self.keep.append(self.label)
        # Dis hat (outline) motorda HER ZAMAN opak siyah cizilir, yazi alfasindan
        # etkilenmez: giris animasyonunda pinden once siyah "hayalet" ad beliriyordu.
        # Yalniz tam gorunurken acilir.
        self.outlined = False
        self.settled = False
        self.haloOn = True
        self.Show()
        self.__Frame(app.GetTime())

    def __del__(self):
        ui.Window.__del__(self)
        self.onClick = None
        self.keep = []

    def SetSelected(self, on):
        self.selected = on
        self.settled = False
        if on:
            self.pinN.Hide()
            self.pinS.Show()
            self.pinB.Show()
        else:
            self.pinS.Hide()
            self.pinB.Hide()
            self.pinN.Show()
        self.__Frame(app.GetTime())

    def __Frame(self, now):
        # markerIn: opacity 0, translateY +18, scale .7 -> 1 (gecikmeli)
        p = _EaseOut((now - self.tIn) / MARKER_IN) if now >= self.tIn else 0.0
        a = p
        if p >= 1.0 and self.settled:
            self.__Live(now)
            return
        dy = 18.0 * (1.0 - p)
        sIn = 0.7 + 0.3 * p
        # yerel koordinatlar
        pcx = self.cx - self.ox
        pcy = self.cy - self.oy + dy
        (sx, sy) = PIN_SPRITE_CENTER
        base = sIn / PIN_SPRITE_SCALE
        if self.selected:
            u = _Wave(now, SEL_PERIOD)                   # selectedPulse
            ps = 1.2 + 0.08 * u
            self.pinS.Place(pcx - sx * base * ps, pcy - sy * base * ps, base * ps)
            self.pinB.Place(pcx - sx * base * ps, pcy - sy * base * ps, base * ps)
            self.pinS.Alpha(a)
            self.pinB.Alpha(a * u)
        else:
            ps = 1.0
            self.pinN.Place(pcx - sx * base, pcy - sy * base, base)
            self.pinN.Alpha(a)
        self.__Halo(now, pcx, pcy, ps * sIn, a)
        # etiket
        lw = self.labelW
        lx = pcx - lw / 2.0
        ly = pcy + LABEL_GAP
        half = LABEL_H / 2
        self.lblBars[0].SetPosition(int(lx), int(ly))
        self.lblBars[0].SetSize(int(lw), half)
        self.lblBars[0].SetColor(_AlphaColor(0xeb0d0f14, a))
        self.lblBars[1].SetPosition(int(lx), int(ly) + half)
        self.lblBars[1].SetSize(int(lw), LABEL_H - half)
        self.lblBars[1].SetColor(_AlphaColor(0xf0030407, a))
        self.lblBox.SetPosition(int(lx), int(ly))
        self.lblBox.SetSize(int(lw), LABEL_H)
        self.lblBox.SetColor(_AlphaColor(_A(140, self.dest.color), a))
        self.label.SetPosition(int(pcx), int(ly) + 7)
        col = (0xff000000 | self.dest.color) if self.selected else 0xffffffff
        self.label.SetPackedFontColor(_AlphaColor(col, a))
        on = a >= 0.999
        if on != self.outlined:
            self.outlined = on
            self.label.SetOutline(on)
        if p >= 1.0:
            self.settled = True

    def __Halo(self, now, pcx, pcy, ps, a):
        # .pin:before halkasi (inset -10 -> cap 70, pulse 2s: 70%'te scale 1.55 op 0)
        t = (now % PULSE_PERIOD) / (PULSE_PERIOD * PULSE_GROW)
        if t >= 1.0 or a <= 0.0:
            if self.haloOn:
                self.halo.Hide()
                self.haloOn = False
            return
        hs = (70.0 / 136.0) * ps * (1.0 + 0.55 * t)
        self.halo.Place(pcx - 80.0 * hs, pcy - 80.0 * hs, hs)
        self.halo.Alpha(0.45 * (1.0 - t) * a, self.dest.color)
        if not self.haloOn:
            self.halo.Show()
            self.haloOn = True

    def __Live(self, now):
        """Giris animasyonu bitmis isaretci: yalniz halka ve (seciliyse) nabiz."""
        pcx = self.cx - self.ox
        pcy = self.cy - self.oy
        if self.selected:
            (sx, sy) = PIN_SPRITE_CENTER
            base = 1.0 / PIN_SPRITE_SCALE
            u = _Wave(now, SEL_PERIOD)
            ps = 1.2 + 0.08 * u
            self.pinS.Place(pcx - sx * base * ps, pcy - sy * base * ps, base * ps)
            self.pinB.Place(pcx - sx * base * ps, pcy - sy * base * ps, base * ps)
            self.pinB.Alpha(u)
        else:
            ps = 1.0
        self.__Halo(now, pcx, pcy, ps, 1.0)

    def OnUpdate(self):
        now = app.GetTime()
        if now < g_summonUntil[0]:
            return
        self.__Frame(now)

    def OnMouseLeftButtonDown(self):
        return True

    def OnMouseLeftButtonUp(self):
        if self.onClick:
            self.onClick(self)
        return True
