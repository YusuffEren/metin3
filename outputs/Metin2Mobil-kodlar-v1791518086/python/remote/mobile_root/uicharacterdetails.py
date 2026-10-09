# MOBIL KAPLAMA (mobile_root/uicharacterdetails.py): pack kopyasi; fark "MOBIL" satirlari (yanina konumlanma olcekli).
import ui
import localeInfo
import player
import item
import uiToolTip
import wndMgr
import app

## 2026-10-09 (KULLANICI: "efsunlar ayrintilara yansimali"): deger bicimi dile gore (TR "%20", EN "20%")
def _En():
	try:
		import dil
		return dil.Mevcut() == "en"
	except:
		return False

## yeni yazi anahtarlari: eski bir locale dosyasiyla acilirsa pencere bozulmasin
def _L(ad, yedek):
	return getattr(localeInfo, ad, yedek)

class CharacterDetailsUI(ui.ScriptWindow):
	def __init__(self, parent):
		self.mobileParent = parent	# MOBIL: AdjustPosition icin
		self.uiCharacterStatus = parent		
		ui.ScriptWindow.__init__(self)
		self.toolTip = uiToolTip.ToolTip()
		
		self.__LoadScript()
	
	def __del__(self):
		self.uiCharacterStatus = None
		self.toolTip = None
		ui.ScriptWindow.__del__(self)
		
	def __LoadScript(self):
		
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CharacterDetailsWindow.py")
		except:
			import exception
			exception.Abort("CharacterDetailsUI.__LoadScript")
		
		## CharacterWindow.py 의 width = 253
		self.Width = 253 - 3
					
		self.GetChild("TitleBar").CloseButtonHide()
		self.ScrollBar = self.GetChild("ScrollBar")
		self.ScrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		
		## 출력되는 UI 최대 숫자
		self.UI_MAX_COUNT = 15
		self.UI_MAX_VIEW_COUNT = 15
		
		## UI KEY & VALUE
		self.INFO_TEXT	= 0
		self.INFO_TOOLTIP = 1
		self.INFO_VALUE	= 2
		self.CATEGORY_STARTLINE	= -1
		self.CATEGORY_ENDLINE	= -2
		
		## Child 셋팅
		self.labelList		= []
		self.labelValueList	= []
		self.labelTextList	= []
		self.horizonBarList	= []
		self.horizonBarNameList = []
		
		for i in xrange(self.UI_MAX_COUNT):
			self.labelList.append( self.GetChild("label%s"%i) )
			self.labelValueList.append( self.GetChild("labelvalue%s"%i) )
			self.labelTextList.append( self.GetChild("labelname%s"%i) )
			self.horizonBarList.append( self.GetChild("horizontalbar%s"%i) )
			self.horizonBarNameList.append( self.GetChild("horizontalbarName%s"%i) )
			
		for i in xrange(self.UI_MAX_COUNT):
			self.labelTextList[i].SetOverEvent( ui.__mem_func__(self.__ButtonOverIn), i )
			self.labelTextList[i].SetOverOutEvent( ui.__mem_func__(self.__ButtonOverOut), i )
			
		self.bosses_kills_obj = self.GetChild("bosses_kills")
		self.stones_kills_obj = self.GetChild("stones_kills")
			
		self.__Initialize()
		
	def __Initialize(self):
		self.bosses_kills_obj.SetText(localeInfo.NumberToMoneyString2(player.GetBossPuan()))
		self.stones_kills_obj.SetText(localeInfo.NumberToMoneyString2(player.GetMetinPuan()))
		
		self.InfoList = []
		
		## 추가 데미지
		self.InfoList.append( [ localeInfo.DETAILS_CATE_1, "", self.CATEGORY_STARTLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_1, localeInfo.DETAILS_TOOLTIP_1, 43 ] )
		
		# if app.ENABLE_PVP_BALANCE or app.ENABLE_PENDANT:
			# self.InfoList.append( [ localeInfo.DETAILS_2, localeInfo.DETAILS_TOOLTIP_2, item.APPLY_RESIST_HUMAN ] )
		
		self.InfoList.append( [ localeInfo.DETAILS_3, localeInfo.DETAILS_TOOLTIP_3, 45 ] )
		self.InfoList.append( [ localeInfo.DETAILS_4, localeInfo.DETAILS_TOOLTIP_4, 47 ] )
		self.InfoList.append( [ localeInfo.DETAILS_5, localeInfo.DETAILS_TOOLTIP_5, 53 ] )
		
		self.InfoList.append( [ localeInfo.DETAILS_METIN, _L("DETAILS_TOOLTIP_METIN", localeInfo.DETAILS_TOOLTIP_5), 139 ] )
		self.InfoList.append( [ localeInfo.DETAILS_BOSS, _L("DETAILS_TOOLTIP_BOSS", localeInfo.DETAILS_TOOLTIP_5), 138 ] )
		
		# if app.ENABLE_ELEMENT_ADD:
			# self.InfoList.append( [ localeInfo.DETAILS_6, localeInfo.DETAILS_TOOLTIP_6, item.APPLY_ATTBONUS_CZ ] )
			
		self.InfoList.append( [ localeInfo.DETAILS_7, localeInfo.DETAILS_TOOLTIP_7, 44 ] )
		self.InfoList.append( [ localeInfo.DETAILS_8, localeInfo.DETAILS_TOOLTIP_8, 46 ] )
		self.InfoList.append( [ localeInfo.DETAILS_9, localeInfo.DETAILS_TOOLTIP_9, 48 ] )
		
		# if app.ENABLE_ELEMENT_ADD:
			# self.InfoList.append( [ localeInfo.DETAILS_10, localeInfo.DETAILS_TOOLTIP_10, item.APPLY_ATTBONUS_DESERT ] )
			# self.InfoList.append( [ localeInfo.DETAILS_11, localeInfo.DETAILS_TOOLTIP_11, item.APPLY_ATTBONUS_INSECT ] )
			
		self.InfoList.append( [ localeInfo.DETAILS_12, localeInfo.DETAILS_TOOLTIP_12, 95 ] )
		self.InfoList.append( [ localeInfo.DETAILS_13, localeInfo.DETAILS_TOOLTIP_13, 96 ] )
		self.InfoList.append( [ localeInfo.DETAILS_14, localeInfo.DETAILS_TOOLTIP_14, 122 ] )
		self.InfoList.append( [ _L("DETAILS_PVM_HIT", "PvM"), _L("DETAILS_TOOLTIP_PVM_HIT", ""), 140 ] )
		self.InfoList.append( [ localeInfo.DETAILS_15, localeInfo.DETAILS_TOOLTIP_15, 124 ] )
		self.InfoList.append( [ localeInfo.DETAILS_16, localeInfo.DETAILS_TOOLTIP_16, 121 ] )
		self.InfoList.append( [ localeInfo.DETAILS_17, localeInfo.DETAILS_TOOLTIP_17, 123 ] )
		self.InfoList.append( [ localeInfo.DETAILS_18, localeInfo.DETAILS_TOOLTIP_18, 132 ] )
		self.InfoList.append( [ localeInfo.DETAILS_19, localeInfo.DETAILS_TOOLTIP_19, 131 ] )
		self.InfoList.append( [ localeInfo.DETAILS_20, localeInfo.DETAILS_TOOLTIP_20, 40 ] )
		self.InfoList.append( [ localeInfo.DETAILS_21, localeInfo.DETAILS_TOOLTIP_21, 41 ] )
		self.InfoList.append( [ localeInfo.DETAILS_22, localeInfo.DETAILS_TOOLTIP_22, 136 ] )
		self.InfoList.append( [ localeInfo.DETAILS_23, localeInfo.DETAILS_TOOLTIP_23, 137 ] )
		self.InfoList.append( [ "", "", self.CATEGORY_ENDLINE ] )
		
		## 엘리멘탈 속성
		self.InfoList.append( [ localeInfo.DETAILS_CATE_2, "", self.CATEGORY_STARTLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_76, localeInfo.DETAILS_TOOLTIP_76, 77 ] )
		self.InfoList.append( [ localeInfo.DETAILS_24, localeInfo.DETAILS_TOOLTIP_24, 76 ] )
		self.InfoList.append( [ localeInfo.DETAILS_25, localeInfo.DETAILS_TOOLTIP_25, 133 ] )
		self.InfoList.append( [ localeInfo.DETAILS_26, localeInfo.DETAILS_TOOLTIP_26, 135 ] )
		self.InfoList.append( [ localeInfo.DETAILS_27, localeInfo.DETAILS_TOOLTIP_27, 75 ] )
		self.InfoList.append( [ localeInfo.DETAILS_28, localeInfo.DETAILS_TOOLTIP_28, 78 ] )
		self.InfoList.append( [ localeInfo.DETAILS_29, localeInfo.DETAILS_TOOLTIP_29, 134 ] )
		# self.InfoList.append( [ localeInfo.DETAILS_77, localeInfo.DETAILS_TOOLTIP_77, item.APPLY_RESIST_MAGIC_REDUCTION ] )
		
		# if app.ENABLE_ELEMENT_ADD:
			# self.InfoList.append( [ localeInfo.DETAILS_30, localeInfo.DETAILS_TOOLTIP_30, item.APPLY_ENCHANT_ELECT ] )
			# self.InfoList.append( [ localeInfo.DETAILS_31, localeInfo.DETAILS_TOOLTIP_31, item.APPLY_ENCHANT_ICE ] )
			# self.InfoList.append( [ localeInfo.DETAILS_32, localeInfo.DETAILS_TOOLTIP_32, item.APPLY_ENCHANT_DARK ] )
			# self.InfoList.append( [ localeInfo.DETAILS_33, localeInfo.DETAILS_TOOLTIP_33, item.APPLY_ENCHANT_FIRE ] )
			# self.InfoList.append( [ localeInfo.DETAILS_34, localeInfo.DETAILS_TOOLTIP_34, item.APPLY_ENCHANT_WIND ] )
			# self.InfoList.append( [ localeInfo.DETAILS_35, localeInfo.DETAILS_TOOLTIP_35, item.APPLY_ENCHANT_EARTH ] )
			
		self.InfoList.append( [ "", "", self.CATEGORY_ENDLINE ] )
		
		## 직업 속성
		self.InfoList.append( [ localeInfo.DETAILS_CATE_3, "", self.CATEGORY_STARTLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_36, localeInfo.DETAILS_TOOLTIP_36, 54 ] )
		self.InfoList.append( [ localeInfo.DETAILS_37, localeInfo.DETAILS_TOOLTIP_37, 55 ] )
		self.InfoList.append( [ localeInfo.DETAILS_38, localeInfo.DETAILS_TOOLTIP_38, 56 ] )
		self.InfoList.append( [ localeInfo.DETAILS_39, localeInfo.DETAILS_TOOLTIP_39, 57 ] )
		# self.InfoList.append( [ localeInfo.DETAILS_40, localeInfo.DETAILS_TOOLTIP_40, item.APPLY_ATTBONUS_WOLFMAN ] )
		self.InfoList.append( [ localeInfo.DETAILS_41, localeInfo.DETAILS_TOOLTIP_41, 59 ] )
		self.InfoList.append( [ localeInfo.DETAILS_42, localeInfo.DETAILS_TOOLTIP_42, 60 ] )
		self.InfoList.append( [ localeInfo.DETAILS_43, localeInfo.DETAILS_TOOLTIP_43, 61 ] )
		self.InfoList.append( [ localeInfo.DETAILS_44, localeInfo.DETAILS_TOOLTIP_44, 62 ] )
		# self.InfoList.append( [ localeInfo.DETAILS_45, localeInfo.DETAILS_TOOLTIP_45, item.APPLY_RESIST_WOLFMAN ] )
		self.InfoList.append( [ "", "", self.CATEGORY_ENDLINE ] )
		
		## 무기 속성
		self.InfoList.append( [ localeInfo.DETAILS_CATE_4, "", self.CATEGORY_STARTLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_46, localeInfo.DETAILS_TOOLTIP_46, 69 ] )
		self.InfoList.append( [ localeInfo.DETAILS_47, localeInfo.DETAILS_TOOLTIP_47, 70 ] )
		self.InfoList.append( [ localeInfo.DETAILS_48, localeInfo.DETAILS_TOOLTIP_48, 71 ] )
		# self.InfoList.append( [ localeInfo.DETAILS_49, localeInfo.DETAILS_TOOLTIP_49, item.APPLY_RESIST_CLAW ] )
		self.InfoList.append( [ localeInfo.DETAILS_50, localeInfo.DETAILS_TOOLTIP_50, 72 ] )
		self.InfoList.append( [ localeInfo.DETAILS_51, localeInfo.DETAILS_TOOLTIP_51, 73 ] )
		self.InfoList.append( [ localeInfo.DETAILS_52, localeInfo.DETAILS_TOOLTIP_52, 74 ] )
		# if app.ENABLE_PENDANT:
			# self.InfoList.append( [ localeInfo.DETAILS_ATTBONUS_SWORD,		localeInfo.DETAILS_TOOLTIP_ATTBONUS_SWORD	, item.APPLY_ATTBONUS_SWORD ] )
			# self.InfoList.append( [ localeInfo.DETAILS_ATTBONUS_TWOHAND,	localeInfo.DETAILS_TOOLTIP_ATTBONUS_TWOHAND, item.APPLY_ATTBONUS_TWOHAND ] )
			# self.InfoList.append( [ localeInfo.DETAILS_ATTBONUS_DAGGER,		localeInfo.DETAILS_TOOLTIP_ATTBONUS_DAGGER	, item.APPLY_ATTBONUS_DAGGER ] )
			# self.InfoList.append( [ localeInfo.DETAILS_ATTBONUS_BELL,			localeInfo.DETAILS_TOOLTIP_ATTBONUS_BELL	, item.APPLY_ATTBONUS_BELL ] )
			# self.InfoList.append( [ localeInfo.DETAILS_ATTBONUS_FAN	,			localeInfo.DETAILS_TOOLTIP_ATTBONUS_FAN	, item.APPLY_ATTBONUS_FAN ] )
			# self.InfoList.append( [ localeInfo.DETAILS_ATTBONUS_BOW,			localeInfo.DETAILS_TOOLTIP_ATTBONUS_BOW	, item.APPLY_ATTBONUS_BOW ] )
			# self.InfoList.append( [ localeInfo.DETAILS_ATTBONUS_CLAW,			localeInfo.DETAILS_TOOLTIP_ATTBONUS_CLAW	, item.APPLY_ATTBONUS_CLAW ] )
			# self.InfoList.append( [ localeInfo.DETAILS_RESIST_MOUNT_FALL,	localeInfo.DETAILS_TOOLTIP_RESIST_MOUNT_FALL	, item.APPLY_RESIST_MOUNT_FALL ] )
		self.InfoList.append( [ "", "", self.CATEGORY_ENDLINE ] )
		
		## 기타
		self.InfoList.append( [ localeInfo.DETAILS_CATE_5, "", self.CATEGORY_STARTLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_53, localeInfo.DETAILS_TOOLTIP_53, 38 ] )
		self.InfoList.append( [ localeInfo.DETAILS_54, localeInfo.DETAILS_TOOLTIP_54, 39 ] )
		self.InfoList.append( [ localeInfo.DETAILS_55, localeInfo.DETAILS_TOOLTIP_55, 37 ] )
		self.InfoList.append( [ localeInfo.DETAILS_56, localeInfo.DETAILS_TOOLTIP_56, 81 ] )
		# self.InfoList.append( [ localeInfo.DETAILS_57, localeInfo.DETAILS_TOOLTIP_57, item.APPLY_BLEEDING_PCT ] )
		# self.InfoList.append( [ localeInfo.DETAILS_58, localeInfo.DETAILS_TOOLTIP_58, item.APPLY_BLEEDING_REDUCE ] )
		self.InfoList.append( [ localeInfo.DETAILS_59, localeInfo.DETAILS_TOOLTIP_59, 63 ] )
		self.InfoList.append( [ localeInfo.DETAILS_60, localeInfo.DETAILS_TOOLTIP_60, 64 ] )
		self.InfoList.append( [ _L("DETAILS_MANA_BURN", "SP"), _L("DETAILS_TOOLTIP_MANA_BURN", ""), 65 ] )
		self.InfoList.append( [ localeInfo.DETAILS_61, localeInfo.DETAILS_TOOLTIP_61, 32 ] )
		self.InfoList.append( [ localeInfo.DETAILS_62, localeInfo.DETAILS_TOOLTIP_62, 33 ] )
		self.InfoList.append( [ localeInfo.DETAILS_63, localeInfo.DETAILS_TOOLTIP_63, 67 ] )
		self.InfoList.append( [ localeInfo.DETAILS_64, localeInfo.DETAILS_TOOLTIP_64, 68 ] )
		self.InfoList.append( [ localeInfo.DETAILS_65, localeInfo.DETAILS_TOOLTIP_65, 79 ] )
		self.InfoList.append( [ localeInfo.DETAILS_66, localeInfo.DETAILS_TOOLTIP_66, 87 ] )
		self.InfoList.append( [ localeInfo.DETAILS_67, localeInfo.DETAILS_TOOLTIP_67, 82 ] )
		self.InfoList.append( [ localeInfo.DETAILS_68, localeInfo.DETAILS_TOOLTIP_68, (83, 116) ] )
		self.InfoList.append( [ localeInfo.DETAILS_69, localeInfo.DETAILS_TOOLTIP_69, (84, 118) ] )
		self.InfoList.append( [ localeInfo.DETAILS_70, localeInfo.DETAILS_TOOLTIP_70, (85, 117, 126) ] )
		self.InfoList.append( [ _L("DETAILS_IMMUNE_STUN", "Stun"), _L("DETAILS_TOOLTIP_IMMUNE_STUN", ""), 88 ] )
		self.InfoList.append( [ _L("DETAILS_IMMUNE_SLOW", "Slow"), _L("DETAILS_TOOLTIP_IMMUNE_SLOW", ""), 89 ] )
		self.InfoList.append( [ "", "", self.CATEGORY_ENDLINE ] )
		
		## MALL
		self.InfoList.append( [ localeInfo.DETAILS_CATE_6, "", self.CATEGORY_STARTLINE ] )
		self.InfoList.append( [ _L("DETAILS_ATT_BONUS_PCT", "ATT"), _L("DETAILS_TOOLTIP_ATT_BONUS_PCT", ""), 93 ] )
		self.InfoList.append( [ localeInfo.DETAILS_71, localeInfo.DETAILS_TOOLTIP_71, 114 ] )
		self.InfoList.append( [ localeInfo.DETAILS_72, localeInfo.DETAILS_TOOLTIP_72, 115 ] )
		self.InfoList.append( [ _L("DETAILS_MAX_HP_PCT", "HP"), _L("DETAILS_TOOLTIP_MAX_HP_PCT", ""), 119 ] )
		self.InfoList.append( [ _L("DETAILS_MAX_SP_PCT", "SP"), _L("DETAILS_TOOLTIP_MAX_SP_PCT", ""), 120 ] )
		#self.InfoList.append( [ "", "", self.CATEGORY_ENDLINE ] )
		
		## 2026-10-09: kaydirma araligi SATIR sayilarak (baslik/bos 1 satir, deger girdisi 2 satir: ad + alt satirdaki
		## deger kutusu). Eskisi girdi sayiyordu -> son satirlar (Dusurme Sansi degeri, Ozel bonuslar) hic gorunmuyordu.
		rows = 0
		self.Diff = len(self.InfoList)
		while self.Diff > 0:
			t = self.InfoList[self.Diff - 1][self.INFO_VALUE]
			need = (t == self.CATEGORY_STARTLINE or t == self.CATEGORY_ENDLINE) and 1 or 2
			if rows + need > self.UI_MAX_COUNT:
				break
			rows += need
			self.Diff -= 1
		self.Diff = max(1, self.Diff)
		stepSize = 1.0 / self.Diff
		self.ScrollBar.SetScrollStep( stepSize )
		self.ScollPos = 0
		self.RefreshLabel()
		
	def Show(self):
		ui.ScriptWindow.Show(self)
		self.SetTop()
		
	def Close(self):
		self.Hide()
		
	def OnUpdate(self):
		## 2026-10-09: eskiden HER KAREDE __Initialize (liste + kaydirma bastan kuruluyordu, telefonda bos yuk).
		## Degerler saniyede 4 kez yenilenir (kaydirma OnScroll ile aninda).
		t = app.GetTime()
		if t < getattr(self, "_sonYenile", 0.0):
			return
		self._sonYenile = t + 0.25
		self.__Initialize()
	
	def AdjustPosition(self, x, y):
		## MOBIL: karakter penceresi olcekli (genel UI olcegi) - yaninda acilmasi icin
		## mantiksal genislik, o pencerenin ETKIN olcegiyle carpilir (sigdirma ile 1.6'dan kucuk olabilir).
		s = 1.0
		try:
			p = getattr(self, "mobileParent", None)
			if p:
				s = wndMgr.GetUIScale(p.hWnd)
		except:
			s = 1.0
		## KULLANICI (2026-09-14): saga sigmazsa SOLA acilir, ekran icinde kalir ("bazen acilmiyor" = ekran disi).
		try:
			ds = wndMgr.GetUIScale(self.hWnd)
		except:
			ds = 1.0
		myW = int(self.GetWidth() * ds)
		myH = int(self.GetHeight() * ds)
		rx = x + int(self.Width * s) + 4
		if rx + myW > wndMgr.GetScreenWidth():
			rx = x - myW - 4
		rx = max(0, min(rx, wndMgr.GetScreenWidth() - myW))
		ry = max(0, min(y, wndMgr.GetScreenHeight() - myH))
		self.SetPosition(rx, ry)
		self.SetTop()
	
	def OnScroll(self):
		self.RefreshLabel()
			
	def RefreshLabel(self):
		self.ScollPos = int(self.ScrollBar.GetPos() * self.Diff)
		en = _En()
		self.LabelLineCount = 0
		self.startline_endlinecount = 0
		for i in xrange(self.UI_MAX_COUNT) :
			idx = i + self.ScollPos
			
			if idx < len(self.InfoList) :
				text = self.InfoList[idx][self.INFO_TEXT]
				type = self.InfoList[idx][self.INFO_VALUE]
				
				if type == self.CATEGORY_STARTLINE:
					self.__LabelTitleLine(i+self.LabelLineCount, text)
					self.startline_endlinecount += 1
				elif type == self.CATEGORY_ENDLINE:
					self.__EmptyLine(i+self.LabelLineCount)
					self.startline_endlinecount += 1
				else:
					value = self.__Bicim(type, self.__Deger(type), en)
					self.__LabelLine(i+self.LabelLineCount, text, value)
					if i+self.LabelLineCount < self.UI_MAX_COUNT:
						self.labelTextList[i+self.LabelLineCount].SetOverEvent( ui.__mem_func__(self.__ButtonOverIn), self.LabelLineCount + self.startline_endlinecount )
						self.labelTextList[i+self.LabelLineCount].SetOverOutEvent( ui.__mem_func__(self.__ButtonOverOut), self.LabelLineCount + self.startline_endlinecount )
					self.LabelLineCount += 1
			else:
				self.__EmptyLine(i+self.LabelLineCount)

				
	## 2026-10-09: duz degerler (Saldiri/Savunma degeri) sayi, bagisikliklar Var/Yok, digerleri yuzde.
	## 85 (efsun esya dusurme) ve 117 (Hirsiz Eldiveni) sunucuda GetPoint ile en fazla 100.
	## 2026-10-09 (KULLANICI: "ayri ayri yazarsak anlami kalmiyor, toplami yazsin"): ayni seyin parcalari TEK satir,
	## deger = TOPLAM. Sunucu da ayni sekilde toplar (item_manager GetDropPct, char_battle GiveExp / RewardGold).
	def __Deger(self, type):
		if isinstance(type, tuple):
			toplam = 0
			for p in type:
				toplam += min(int(player.GetStatus(p)), 100)	# her parca sunucuda GetPoint ile en fazla 100
			return toplam
		return player.GetStatus(type)

	def __Bicim(self, type, value, en):
		try:
			value = int(value)
		except:
			return str(value)
		if type == 88 or type == 89:
			if value > 0:
				return _L("DETAILS_VAR", "+")
			return _L("DETAILS_YOK", "-")
		## 126 = takilan Hirsiz Eldiveni (3. asama)
		if type == 85 or type == 117 or type == 126:
			value = min(value, 100)
		if type == 95 or type == 96 or value == 0:
			return str(value)
		if en:
			return "%d%%" % value
		return "%%%d" % value

	def __LabelTitleLine(self, idx, text):
		if(idx < self.UI_MAX_COUNT):
			self.labelList[idx].Hide()
			self.labelTextList[idx].Hide()
			self.horizonBarList[idx].Show()
			self.horizonBarNameList[idx].SetText( text )
				
	def __EmptyLine(self, idx):
		if(idx < self.UI_MAX_COUNT):
			self.labelList[idx].Hide()
			self.labelTextList[idx].Hide()
			self.horizonBarList[idx].Hide()
		
	def __LabelLine(self, idx, text, value):
		if(idx < self.UI_MAX_COUNT):
			self.labelTextList[idx].Show()
			self.horizonBarList[idx].Hide()
			self.labelList[idx].Hide()
		
			self.labelTextList[idx].SetText( text )
		
			if(idx+1 < self.UI_MAX_COUNT):
				self.labelList[idx+1].Show()
				self.horizonBarList[idx+1].Hide()
				self.labelTextList[idx+1].Hide()
				self.labelValueList[idx+1].SetText( str(value) )
			else:
				self.labelTextList[idx].Hide()	## degeri sigmayan son satirda degersiz ad gosterme

	def __ButtonOverIn(self, i):
		idx = i + self.ScollPos
		tooltip = self.InfoList[idx][self.INFO_TOOLTIP]
		
		arglen = len(str(tooltip))
		pos_x, pos_y = wndMgr.GetMousePosition()
		
		self.toolTip.ClearToolTip()
		## 2026-10-09: SetThinBoardSize ToolTip'te YOK (AttributeError -> ipucu hic acilmiyordu); uzun metin sarilir
		self.toolTip.AppendDescription(str(tooltip), 30, 0xffffff00)
		self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
		self.toolTip.ShowToolTip()
		
	def __ButtonOverOut(self, idx):
		self.toolTip.Hide()
		
	def OnTop(self):
		if self.uiCharacterStatus:
			self.uiCharacterStatus.SetTop()