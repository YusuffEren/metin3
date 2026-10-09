/* Reconstructed by Ghidra from the ARM64 client; not original source.
 * Category: android-platform; selected functions: 250.
 */

/* ============================================================
 * CAndroidBgfxCallback::fatal @ 006bf7d0
 * ============================================================ */

/* CAndroidBgfxCallback::fatal(char const*, unsigned short, bgfx::Fatal::Enum, char const*) */

void __thiscall
CAndroidBgfxCallback::fatal
          (undefined8 param_1_00,undefined *param_1,uint param_3,ulong param_4,undefined1 *param_5)

{
  undefined *puVar1;
  undefined1 *puVar2;
  
  puVar1 = &DAT_0037b221;
  if (param_1 != (undefined *)0x0) {
    puVar1 = param_1;
  }
  puVar2 = &DAT_00378982;
  if (param_5 != (undefined1 *)0x0) {
    puVar2 = param_5;
  }
  __android_log_print(6,"sancak2","BGFX FATAL 0x%08x %s(%u): %s",param_4,puVar1,param_3 & 0xffff,
                      puVar2);
  TraceError("BGFX FATAL 0x%08x %s(%u): %s",param_4 & 0xffffffff,puVar1,(ulong)(param_3 & 0xffff),
             puVar2);
  return;
}

/* ============================================================
 * CAndroidBgfxCallback::traceVargs @ 006bf85c
 * ============================================================ */

/* CAndroidBgfxCallback::traceVargs(char const*, unsigned short, char const*, std::__va_list) */

void __thiscall
CAndroidBgfxCallback::traceVargs
          (undefined8 param_1_00,undefined *param_1,undefined2 param_2,char *param_3,
          undefined8 *param_5)

{
  undefined *puVar1;
  long lVar2;
  undefined8 local_460;
  undefined8 uStack_458;
  undefined8 uStack_450;
  undefined8 uStack_448;
  char acStack_438 [1024];
  long local_38;
  
  lVar2 = tpidr_el0;
  local_38 = *(long *)(lVar2 + 0x28);
  uStack_458 = param_5[1];
  local_460 = *param_5;
  uStack_448 = param_5[3];
  uStack_450 = param_5[2];
  vsnprintf(acStack_438,0x400,param_3,&local_460);
  puVar1 = &DAT_0037b221;
  if (param_1 != (undefined *)0x0) {
    puVar1 = param_1;
  }
  __android_log_print(2,"sancak2-bgfx","%s(%u): %s",puVar1,param_2,acStack_438);
  if (*(long *)(lVar2 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * CAndroidPlatform::CAndroidPlatform @ 006bf8fc
 * ============================================================ */

/* CAndroidPlatform::CAndroidPlatform(android_app*, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> > const&, bool) */

void __thiscall
CAndroidPlatform::CAndroidPlatform
          (CAndroidPlatform *this,android_app *param_1,basic_string *param_2,bool param_3)

{
  ulong uVar1;
  ulong uVar2;
  void *__src;
  long lVar3;
  undefined *puVar4;
  undefined *puVar5;
  CAndroidPlatform *__dest;
  CInputCore *this_00;
  undefined8 uVar6;
  undefined8 uVar7;
  CAndroidPlatform *local_80;
  undefined *puStack_78;
  undefined *local_70;
  undefined *puStack_68;
  undefined *local_60;
  long local_58;
  
  lVar3 = tpidr_el0;
  local_58 = *(long *)(lVar3 + 0x28);
  CAndroidApplicationPlatformBase::CAndroidApplicationPlatformBase
            ((CAndroidApplicationPlatformBase *)this);
  puVar4 = PTR_vtable_00d79908;
  this[0x40] = (CAndroidPlatform)0x0;
  *(undefined4 *)(this + 0x44) = 0;
  *(android_app **)(this + 0x48) = param_1;
  *(undefined **)this = puVar4 + 0x10;
  if (((byte)*param_2 & 1) == 0) {
    uVar7 = *(undefined8 *)(param_2 + 8);
    uVar6 = *(undefined8 *)param_2;
    *(undefined8 *)(this + 0x60) = *(undefined8 *)(param_2 + 0x10);
    *(undefined8 *)(this + 0x58) = uVar7;
    *(undefined8 *)(this + 0x50) = uVar6;
  }
  else {
    uVar2 = *(ulong *)(param_2 + 8);
    __src = *(void **)(param_2 + 0x10);
    if (uVar2 < 0x17) {
      __dest = this + 0x51;
      this[0x50] = SUB41((int)uVar2 << 1,0);
    }
    else {
      if (0xffffffffffffffef < uVar2) {
        if (*(long *)(lVar3 + 0x28) == local_58) {
                    /* WARNING: Subroutine does not return */
          FUN_006c1ae4(this + 0x50);
        }
        goto LAB_006bfb20;
      }
      uVar1 = (uVar2 | 0xf) + 1;
      __dest = operator_new(uVar1);
      *(ulong *)(this + 0x58) = uVar2;
      *(CAndroidPlatform **)(this + 0x60) = __dest;
      *(ulong *)(this + 0x50) = uVar1 | 1;
    }
    memmove(__dest,__src,uVar2 + 1);
  }
  this[0x6d] = (CAndroidPlatform)0x0;
  *(undefined8 *)(this + 0x81) = 0;
  this[0x68] = (CAndroidPlatform)0x8;
  *(undefined4 *)(this + 0x69) = 0x6b636170;
  this[0x80] = (CAndroidPlatform)param_3;
  puVar4 = PTR_vtable_00d79918;
  *(undefined8 *)(this + 0x91) = 0;
  *(undefined8 *)(this + 0x89) = 0;
  *(undefined4 *)(this + 0x98) = 0;
  *(undefined8 *)(this + 0x9c) = 0xffffffffffffffff;
  *(undefined8 *)(this + 0xa4) = 0xffffffffffffffff;
  *(undefined **)(this + 0xb0) = puVar4 + 0x10;
  puVar5 = PTR_OnAppCmdThunk_00d79928;
  puVar4 = PTR_OnInputEventThunk_00d79920;
  *(undefined2 *)(this + 0xac) = 0;
  *(CAndroidPlatform **)param_1 = this;
  *(undefined **)(param_1 + 8) = puVar5;
  puStack_78 = PTR_Listener_DeviceCreated_00d79930;
  *(undefined **)(param_1 + 0x10) = puVar4;
  local_70 = PTR_Listener_BackbufferResized_00d79940;
  puStack_68 = PTR_Listener_BeforeFrame_00d79938;
  local_60 = PTR_Listener_DeviceDestroying_00d79910;
  local_80 = this;
  BgfxDeviceBackend::SetAndroidSurfaceListener((SAndroidSurfaceListener *)&local_80);
  M2Android_SetSplashPresenter(FUN_006bfd3c,(void *)0x0);
  this_00 = (CInputCore *)M2Android_InputCore();
  m2input::CInputCore::SetUiHitTest
            (this_00,(_func_bool_void_ptr_int_int *)PTR_UiHitTestThunk_00d79948,this);
  M2Touch_SetOccluderTest
            ((_func_bool_void_ptr_float_float *)PTR_GameWindowOccluderThunk_00d79950,this);
  if (*(long *)(lVar3 + 0x28) == local_58) {
    return;
  }
LAB_006bfb20:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * CAndroidPlatform::OnAppCmdThunk @ 006bfb24
 * ============================================================ */

/* CAndroidPlatform::OnAppCmdThunk(android_app*, int) */

void CAndroidPlatform::OnAppCmdThunk(android_app *param_1,int param_2)

{
  if (*(CAndroidPlatform **)param_1 != (CAndroidPlatform *)0x0) {
    OnAppCmd(*(CAndroidPlatform **)param_1,param_2);
    return;
  }
  return;
}

/* ============================================================
 * CAndroidPlatform::OnInputEventThunk @ 006bfb34
 * ============================================================ */

/* CAndroidPlatform::OnInputEventThunk(android_app*, AInputEvent*) */

void CAndroidPlatform::OnInputEventThunk(android_app *param_1,AInputEvent *param_2)

{
  M2Android_HandleInputEvent(param_2);
  return;
}

/* ============================================================
 * CAndroidPlatform::Listener_DeviceCreated @ 006bfb3c
 * ============================================================ */

/* CAndroidPlatform::Listener_DeviceCreated(void*, unsigned int, unsigned int) */

void CAndroidPlatform::Listener_DeviceCreated(void *param_1,uint param_2,uint param_3)

{
  byte bVar1;
  
  if (*(char *)((long)param_1 + 0xad) == '\0') {
    *(undefined1 *)((long)param_1 + 0xad) = 1;
    WriteDeviceReport(param_1,param_2,param_3);
  }
  M2Touch_SetSurfaceSize(*(int *)((long)param_1 + 0x84),*(int *)((long)param_1 + 0x88));
  if (*(char *)((long)param_1 + 0xac) == '\0') {
    bVar1 = M2Touch_Create(param_2,param_3);
    *(byte *)((long)param_1 + 0xac) = bVar1 & 1;
    __android_log_print(4,"sancak2","M2Touch_Create(%u, %u) yuzey %dx%d -> %d",param_2,param_3,
                        *(undefined4 *)((long)param_1 + 0x84),*(undefined4 *)((long)param_1 + 0x88))
    ;
  }
  else {
    M2Touch_Resize(param_2,param_3);
  }
  SyncPresentation(param_1);
  return;
}

/* ============================================================
 * CAndroidPlatform::Listener_BackbufferResized @ 006bfbe4
 * ============================================================ */

/* CAndroidPlatform::Listener_BackbufferResized(void*, unsigned int, unsigned int) */

void CAndroidPlatform::Listener_BackbufferResized(void *param_1,uint param_2,uint param_3)

{
  byte bVar1;
  
  M2Touch_SetSurfaceSize(*(int *)((long)param_1 + 0x84),*(int *)((long)param_1 + 0x88));
  if (*(char *)((long)param_1 + 0xac) == '\0') {
    bVar1 = M2Touch_Create(param_2,param_3);
    *(byte *)((long)param_1 + 0xac) = bVar1 & 1;
    __android_log_print(4,"sancak2","M2Touch_Create(%u, %u) yuzey %dx%d -> %d",param_2,param_3,
                        *(undefined4 *)((long)param_1 + 0x84),*(undefined4 *)((long)param_1 + 0x88))
    ;
  }
  else {
    M2Touch_Resize(param_2,param_3);
  }
  SyncPresentation(param_1);
  return;
}

/* ============================================================
 * CAndroidPlatform::Listener_BeforeFrame @ 006bfc70
 * ============================================================ */

/* CAndroidPlatform::Listener_BeforeFrame(void*) */

void CAndroidPlatform::Listener_BeforeFrame(void *param_1)

{
  char cVar1;
  undefined *puVar2;
  long lVar3;
  float fVar4;
  
  UpdateKeyboardPan(param_1);
  lVar3 = M2Android_InputCore();
  puVar2 = PTR_ms_singleton_00d79958;
  cVar1 = *(char *)(lVar3 + 0x4dc);
  fVar4 = *(float *)(lVar3 + 0x4d8);
  if ((*(char *)((long)param_1 + 0x40) != cVar1) ||
     ((cVar1 != '\0' && (0.5 <= ABS(fVar4 - *(float *)((long)param_1 + 0x44)))))) {
    *(char *)((long)param_1 + 0x40) = cVar1;
    *(float *)((long)param_1 + 0x44) = fVar4;
    CPythonPlayer::NEW_SetTouchMoveState(*(CPythonPlayer **)puVar2,fVar4,cVar1 != '\0');
  }
  M2Video_UpdateAll();
  SyncPresentation(param_1);
  if (*(char *)((long)param_1 + 0xac) != '\0') {
    M2Touch_Render(0xf9);
    return;
  }
  return;
}

/* ============================================================
 * CAndroidPlatform::Listener_DeviceDestroying @ 006bfd04
 * ============================================================ */

/* CAndroidPlatform::Listener_DeviceDestroying(void*) */

void CAndroidPlatform::Listener_DeviceDestroying(void *param_1)

{
  if (*(char *)((long)param_1 + 0xac) != '\0') {
    M2Touch_Destroy();
    *(undefined1 *)((long)param_1 + 0xac) = 0;
  }
  *(undefined8 *)((long)param_1 + 0xa4) = 0xffffffffffffffff;
  *(undefined8 *)((long)param_1 + 0x9c) = 0xffffffffffffffff;
  return;
}

/* ============================================================
 * CAndroidPlatform::UiHitTestThunk @ 006bfd70
 * ============================================================ */

/* CAndroidPlatform::UiHitTestThunk(void*, int, int) */

void CAndroidPlatform::UiHitTestThunk(void *param_1,int param_2,int param_3)

{
  long lVar1;
  bool bVar2;
  int iVar3;
  CWindow *pCVar4;
  long lVar5;
  CWindow *this;
  CWindow *this_00;
  CWindowManager *this_01;
  long local_48;
  long lStack_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  this_01 = *(CWindowManager **)PTR_ms_singleton_00d79960;
  if (this_01 == (CWindowManager *)0x0) {
    bVar2 = false;
    goto LAB_006bfe40;
  }
  local_48 = 0;
  lStack_40 = 0;
  UI::CWindowManager::GetMousePosition(this_01,&lStack_40,&local_48);
  pCVar4 = (CWindow *)UI::CWindowManager::__PickWindow(this_01,lStack_40,local_48);
  bVar2 = false;
  if (pCVar4 == (CWindow *)0x0) goto LAB_006bfe40;
  lVar5 = UI::CWindow::GetParent(pCVar4);
  this_00 = pCVar4;
  if (lVar5 == 0) {
LAB_006bfe04:
    lVar5 = UI::CWindow::GetParent(pCVar4);
    bVar2 = false;
    if (lVar5 == 0) goto LAB_006bfe40;
  }
  else {
    do {
      this = (CWindow *)UI::CWindow::GetParent(this_00);
      lVar5 = UI::CWindow::GetParent(this);
      if (lVar5 == 0) break;
      this_00 = (CWindow *)UI::CWindow::GetParent(this_00);
      lVar5 = UI::CWindow::GetParent(this_00);
    } while (lVar5 != 0);
    if (this_00 == pCVar4) goto LAB_006bfe04;
  }
  pCVar4 = this_00 + 9;
  if (((byte)this_00[8] & 1) != 0) {
    pCVar4 = *(CWindow **)(this_00 + 0x18);
  }
  iVar3 = strcmp((char *)pCVar4,"GAME");
  bVar2 = iVar3 != 0;
LAB_006bfe40:
  if (*(long *)(lVar1 + 0x28) != local_38) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail(bVar2);
  }
  return;
}

/* ============================================================
 * CAndroidPlatform::GameWindowOccluderThunk @ 006bfe68
 * ============================================================ */

/* CAndroidPlatform::GameWindowOccluderThunk(void*, float, float) */

void CAndroidPlatform::GameWindowOccluderThunk(void *param_1,float param_2,float param_3)

{
  long lVar1;
  bool bVar2;
  int iVar3;
  ulong uVar4;
  CWindow *pCVar5;
  CWindow *this;
  CWindow *this_00;
  long lVar6;
  long lVar7;
  long lVar8;
  long lVar9;
  CWindowManager *this_01;
  undefined8 local_58;
  undefined8 local_50;
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  this_01 = *(CWindowManager **)PTR_ms_singleton_00d79960;
  if (this_01 == (CWindowManager *)0x0) {
    bVar2 = false;
  }
  else {
    local_58 = 0;
    local_50 = 0;
    uVar4 = BgfxDeviceBackend::GetAndroidPresentationRect
                      ((int *)((long)&local_50 + 4),(int *)&local_50,(int *)((long)&local_58 + 4),
                       (int *)&local_58);
    bVar2 = false;
    if ((((uVar4 & 1) != 0) && (0 < local_58._4_4_)) && (0 < (int)local_58)) {
      lVar8 = *(long *)(this_01 + 8);
      bVar2 = false;
      if ((0 < lVar8) && (lVar9 = *(long *)(this_01 + 0x10), 0 < lVar9)) {
        bVar2 = false;
        lVar6 = (long)(((param_2 - (float)local_50._4_4_) * (float)lVar8) / (float)local_58._4_4_);
        if (-1 < lVar6) {
          lVar7 = (long)(((param_3 - (float)(int)local_50) * (float)lVar9) / (float)(int)local_58);
          if ((-1 < lVar7) && (lVar6 < lVar8 && lVar7 < lVar9)) {
            pCVar5 = (CWindow *)UI::CWindowManager::__PickWindow(this_01,lVar6,lVar7);
            bVar2 = false;
            if (pCVar5 != (CWindow *)0x0) {
              lVar8 = UI::CWindow::GetParent(pCVar5);
              this_00 = pCVar5;
              while (lVar8 != 0) {
                this = (CWindow *)UI::CWindow::GetParent(this_00);
                lVar8 = UI::CWindow::GetParent(this);
                if (lVar8 == 0) break;
                this_00 = (CWindow *)UI::CWindow::GetParent(this_00);
                lVar8 = UI::CWindow::GetParent(this_00);
              }
              lVar8 = UI::CWindow::GetParent(pCVar5);
              bVar2 = false;
              if (lVar8 != 0) {
                pCVar5 = this_00 + 9;
                if (((byte)this_00[8] & 1) != 0) {
                  pCVar5 = *(CWindow **)(this_00 + 0x18);
                }
                iVar3 = strcmp((char *)pCVar5,"GAME");
                bVar2 = false;
                if (iVar3 != 0) {
                  iVar3 = strcmp((char *)pCVar5,"UI_BOTTOM");
                  bVar2 = iVar3 != 0;
                }
              }
            }
          }
        }
      }
    }
  }
  if (*(long *)(lVar1 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(bVar2);
}

/* ============================================================
 * CAndroidPlatform::~CAndroidPlatform @ 006c001c
 * ============================================================ */

/* CAndroidPlatform::~CAndroidPlatform() */

void __thiscall CAndroidPlatform::~CAndroidPlatform(CAndroidPlatform *this)

{
  CInputCore *this_00;
  undefined8 *puVar1;
  
  this_00 = (CInputCore *)M2Android_InputCore();
  m2input::CInputCore::SetUiHitTest(this_00,(_func_bool_void_ptr_int_int *)0x0,(void *)0x0);
  M2Touch_SetOccluderTest((_func_bool_void_ptr_float_float *)0x0,(void *)0x0);
  M2Android_SetSplashPresenter((_func_void_void_ptr_SM2AndroidSplashImage_ptr *)0x0,(void *)0x0);
  BgfxDeviceBackend::SetAndroidSurfaceListener((SAndroidSurfaceListener *)0x0);
  puVar1 = *(undefined8 **)(this + 0x48);
  puVar1[1] = 0;
  puVar1[2] = 0;
  *puVar1 = 0;
  if (((byte)this[0x68] & 1) != 0) {
    operator_delete(*(void **)(this + 0x78));
  }
  if (((byte)this[0x50] & 1) != 0) {
    operator_delete(*(void **)(this + 0x60));
  }
  CAndroidApplicationPlatformBase::~CAndroidApplicationPlatformBase
            ((CAndroidApplicationPlatformBase *)this);
  return;
}

/* ============================================================
 * CAndroidPlatform::~CAndroidPlatform @ 006c00ac
 * ============================================================ */

/* CAndroidPlatform::~CAndroidPlatform() */

void __thiscall CAndroidPlatform::~CAndroidPlatform(CAndroidPlatform *this)

{
  ~CAndroidPlatform(this);
  operator_delete(this);
  return;
}

/* ============================================================
 * CAndroidPlatform::IsDestroyRequested @ 006c00d0
 * ============================================================ */

/* CAndroidPlatform::IsDestroyRequested() const */

bool __thiscall CAndroidPlatform::IsDestroyRequested(CAndroidPlatform *this)

{
  return *(int *)(*(long *)(this + 0x48) + 100) != 0;
}

/* ============================================================
 * CAndroidPlatform::WaitForFirstWindow @ 006c00e4
 * ============================================================ */

/* CAndroidPlatform::WaitForFirstWindow() */

bool __thiscall CAndroidPlatform::WaitForFirstWindow(CAndroidPlatform *this)

{
  CAndroidPlatform CVar1;
  
  CVar1 = this[0x81];
  while( true ) {
    if (CVar1 != (CAndroidPlatform)0x0) {
      return *(int *)(*(long *)(this + 0x48) + 100) == 0;
    }
    if (*(int *)(*(long *)(this + 0x48) + 100) != 0) break;
    PumpPlatformEvents(this);
    CVar1 = this[0x81];
  }
  return false;
}

/* ============================================================
 * CAndroidPlatform::PumpPlatformEvents @ 006c013c
 * ============================================================ */

/* CAndroidPlatform::PumpPlatformEvents() */

void __thiscall CAndroidPlatform::PumpPlatformEvents(CAndroidPlatform *this)

{
  long lVar1;
  uint uVar2;
  int iVar3;
  CAndroidPlatform CVar4;
  undefined4 local_44;
  long local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  CVar4 = this[0x81];
  while( true ) {
    if (CVar4 == (CAndroidPlatform)0x0) {
      uVar2 = BgfxDeviceBackend::CanRunWithoutAndroidSurface();
      uVar2 = uVar2 ^ 1;
    }
    else {
      uVar2 = 0;
    }
    local_40 = 0;
    local_44 = 0;
    iVar3 = ALooper_pollOnce(-(uVar2 & 1),0,&local_44,&local_40);
    M2Android_DispatchQueuedInput();
    if ((-1 < iVar3) && (local_40 != 0)) {
      (**(code **)(local_40 + 0x10))(*(undefined8 *)(this + 0x48));
    }
    if (*(int *)(*(long *)(this + 0x48) + 100) != 0) break;
    CVar4 = this[0x81];
    if ((iVar3 < 0) && (((uVar2 ^ 1) & 1) != 0 || CVar4 != (CAndroidPlatform)0x0)) {
LAB_006c0210:
      if (*(long *)(lVar1 + 0x28) != local_38) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return;
    }
  }
  if (this[0x83] == (CAndroidPlatform)0x0) {
    this[0x83] = (CAndroidPlatform)0x1;
    __android_log_print(4,"sancak2","etkinlik yok ediliyor -> PostQuitMessage(0)");
    PostQuitMessage(0);
  }
  goto LAB_006c0210;
}

/* ============================================================
 * CAndroidPlatform::ShowSoftKeyboard @ 006c0238
 * ============================================================ */

/* CAndroidPlatform::ShowSoftKeyboard(bool) */

void __thiscall CAndroidPlatform::ShowSoftKeyboard(CAndroidPlatform *this,bool param_1)

{
  M2Android_JavaShowSoftKeyboard(param_1);
  return;
}

/* ============================================================
 * CAndroidPlatform::ResetSoftKeyboard @ 006c0240
 * ============================================================ */

/* CAndroidPlatform::ResetSoftKeyboard() */

void CAndroidPlatform::ResetSoftKeyboard(void)

{
  (*(code *)PTR_M2Android_JavaResetSoftKeyboard_00d7cda8)();
  return;
}

/* ============================================================
 * CAndroidPlatform::OnAppCmd @ 006c0244
 * ============================================================ */

/* CAndroidPlatform::OnAppCmd(int) */

void __thiscall CAndroidPlatform::OnAppCmd(CAndroidPlatform *this,int param_1)

{
  bool bVar1;
  char *pcVar2;
  char *pcVar3;
  
  pcVar3 = "WINDOW_RESIZED";
  pcVar2 = "INPUT_CHANGED";
  switch(param_1) {
  case 0:
    break;
  case 1:
    __android_log_print(4,"sancak2","APP_CMD_%s","INIT_WINDOW");
    OnWindowInit(this);
    return;
  case 2:
    __android_log_print(4,"sancak2","APP_CMD_%s","TERM_WINDOW");
    if (this[0xac] != (CAndroidPlatform)0x0) {
      M2Touch_Destroy();
      this[0xac] = (CAndroidPlatform)0x0;
      __android_log_print(4,"sancak2","M2Touch_Destroy (yuzey kaybi)");
    }
    M2Android_OnWindowLost();
    M2Android_SetNativeWindow((void *)0x0,0,0);
    BgfxDeviceBackend::SetAndroidNativeWindow((void *)0x0,0,0);
    this[0x81] = (CAndroidPlatform)0x0;
    return;
  case 3:
    goto switchD_006c0284_caseD_3;
  case 4:
    pcVar2 = "WINDOW_REDRAW_NEEDED";
    break;
  case 5:
    pcVar3 = "CONTENT_RECT_CHANGED";
    goto switchD_006c0284_caseD_3;
  case 6:
    __android_log_print(4,"sancak2","APP_CMD_%s","GAINED_FOCUS");
    bVar1 = true;
    goto LAB_006c03b4;
  case 7:
    __android_log_print(4,"sancak2","APP_CMD_%s","LOST_FOCUS");
    bVar1 = false;
LAB_006c03b4:
    M2Android_OnFocusChanged(bVar1);
    return;
  case 8:
    pcVar3 = "CONFIG_CHANGED";
switchD_006c0284_caseD_3:
    __android_log_print(4,"sancak2","APP_CMD_%s",pcVar3);
    OnSurfaceGeometryMaybeChanged(this,pcVar3);
    return;
  case 9:
    pcVar2 = "LOW_MEMORY";
    break;
  case 10:
    pcVar2 = "START";
    break;
  case 0xb:
    pcVar2 = "RESUME";
    break;
  case 0xc:
    pcVar2 = "SAVE_STATE";
    break;
  case 0xd:
    pcVar2 = "PAUSE";
    break;
  case 0xe:
    pcVar2 = "STOP";
    break;
  case 0xf:
    pcVar2 = "DESTROY";
    break;
  default:
    pcVar2 = "?";
    goto LAB_006c0458;
  }
LAB_006c0458:
  __android_log_print(4,"sancak2","APP_CMD_%s",pcVar2);
  return;
}

/* ============================================================
 * CAndroidPlatform::OnWindowInit @ 006c0468
 * ============================================================ */

/* CAndroidPlatform::OnWindowInit() */

void __thiscall CAndroidPlatform::OnWindowInit(CAndroidPlatform *this)

{
  char *pcVar1;
  uint uVar2;
  uint uVar3;
  long lVar4;
  
  lVar4 = *(long *)(*(long *)(this + 0x48) + 0x48);
  if (lVar4 != 0) {
    ANativeWindow_setBuffersGeometry(lVar4,0,0,0);
    uVar2 = ANativeWindow_getWidth(lVar4);
    uVar3 = ANativeWindow_getHeight(lVar4);
    if (0 < (int)uVar2) {
      if (0 < (int)uVar3) {
        pcVar1 = "ilk";
        if (this[0x82] != (CAndroidPlatform)0x0) {
          pcVar1 = "geri geldi";
        }
        *(uint *)(this + 0x84) = uVar2;
        *(uint *)(this + 0x88) = uVar3;
        __android_log_print(4,"sancak2","yuzey: %dx%d (%s)",uVar2,uVar3,pcVar1);
        RefreshSafeInsets(this);
        M2Android_SetNativeWindow(*(void **)(*(long *)(this + 0x48) + 0x48),uVar2,uVar3);
        BgfxDeviceBackend::SetAndroidNativeWindow
                  (*(void **)(*(long *)(this + 0x48) + 0x48),uVar2,uVar3);
        this[0x81] = (CAndroidPlatform)0x1;
        if (this[0x82] != (CAndroidPlatform)0x0) {
          M2Android_OnWindowRestored();
        }
        this[0x82] = (CAndroidPlatform)0x1;
        return;
      }
    }
  }
  __android_log_print(6,"sancak2","INIT_WINDOW: pencere boyutu olculemedi");
  return;
}

/* ============================================================
 * CAndroidPlatform::OnWindowTerm @ 006c0580
 * ============================================================ */

/* CAndroidPlatform::OnWindowTerm() */

void __thiscall CAndroidPlatform::OnWindowTerm(CAndroidPlatform *this)

{
  if (this[0xac] != (CAndroidPlatform)0x0) {
    M2Touch_Destroy();
    this[0xac] = (CAndroidPlatform)0x0;
    __android_log_print(4,"sancak2","M2Touch_Destroy (yuzey kaybi)");
  }
  M2Android_OnWindowLost();
  M2Android_SetNativeWindow((void *)0x0,0,0);
  BgfxDeviceBackend::SetAndroidNativeWindow((void *)0x0,0,0);
  this[0x81] = (CAndroidPlatform)0x0;
  return;
}

/* ============================================================
 * CAndroidPlatform::OnSurfaceGeometryMaybeChanged @ 006c05ec
 * ============================================================ */

/* CAndroidPlatform::OnSurfaceGeometryMaybeChanged(char const*) */

void __thiscall
CAndroidPlatform::OnSurfaceGeometryMaybeChanged(CAndroidPlatform *this,char *param_1)

{
  void *pvVar1;
  long lVar2;
  uint uVar3;
  uint uVar5;
  undefined8 uVar4;
  
  RefreshSafeInsets(this);
  if ((this[0x81] != (CAndroidPlatform)0x0) &&
     (lVar2 = *(long *)(this + 0x48), *(long *)(lVar2 + 0x48) != 0)) {
    uVar3 = (int)*(undefined8 *)(lVar2 + 0x58) - (int)*(undefined8 *)(lVar2 + 0x50);
    uVar5 = (int)((ulong)*(undefined8 *)(lVar2 + 0x58) >> 0x20) -
            (int)((ulong)*(undefined8 *)(lVar2 + 0x50) >> 0x20);
    uVar4 = CONCAT44(uVar5,uVar3);
    if (0 < (int)uVar3 && 0 < (int)uVar5) {
      if ((uVar3 != *(uint *)(this + 0x84)) || (uVar5 != *(uint *)(this + 0x88))) {
        __android_log_print(4,"sancak2","yuzey boyutu degisti (%s): %dx%d -> %dx%d",param_1,
                            *(uint *)(this + 0x84),*(uint *)(this + 0x88),uVar3,uVar5,uVar4,0);
        pvVar1 = *(void **)(*(long *)(this + 0x48) + 0x48);
        *(undefined8 *)(this + 0x84) = uVar4;
        M2Android_SetNativeWindow(pvVar1,uVar3,uVar5);
        BgfxDeviceBackend::SetAndroidNativeWindow
                  (*(void **)(*(long *)(this + 0x48) + 0x48),uVar3,uVar5);
        return;
      }
    }
  }
  return;
}

/* ============================================================
 * CAndroidPlatform::MeasureNewWindow @ 006c06d8
 * ============================================================ */

/* CAndroidPlatform::MeasureNewWindow(int*, int*) */

bool __thiscall CAndroidPlatform::MeasureNewWindow(CAndroidPlatform *this,int *param_1,int *param_2)

{
  bool bVar1;
  int iVar2;
  long lVar3;
  
  lVar3 = *(long *)(*(long *)(this + 0x48) + 0x48);
  if (lVar3 == 0) {
    bVar1 = false;
  }
  else {
    ANativeWindow_setBuffersGeometry(lVar3,0,0,0);
    iVar2 = ANativeWindow_getWidth(lVar3);
    *param_1 = iVar2;
    iVar2 = ANativeWindow_getHeight(lVar3);
    *param_2 = iVar2;
    bVar1 = (0 < *param_1 && iVar2 != 0) && (*param_1 < 1 || -1 < iVar2);
  }
  return bVar1;
}

/* ============================================================
 * CAndroidPlatform::RefreshSafeInsets @ 006c0750
 * ============================================================ */

/* CAndroidPlatform::RefreshSafeInsets() */

void __thiscall CAndroidPlatform::RefreshSafeInsets(CAndroidPlatform *this)

{
  long lVar1;
  int local_38 [4];
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  local_38[3] = 0;
  local_38[2] = 0;
  local_38[0] = 0;
  local_38[1] = 0;
  M2Shell_QuerySafeInsets(local_38 + 3,local_38 + 2,local_38 + 1,local_38);
  if ((((local_38[3] != *(int *)(this + 0x8c)) || (local_38[2] != *(int *)(this + 0x90))) ||
      (local_38[1] != *(int *)(this + 0x94))) || (local_38[0] != *(int *)(this + 0x98))) {
    *(int *)(this + 0x8c) = local_38[3];
    *(int *)(this + 0x90) = local_38[2];
    *(int *)(this + 0x94) = local_38[1];
    *(int *)(this + 0x98) = local_38[0];
    __android_log_print(4,"sancak2","guvenli alan (kesik) kenarlari: sol=%d ust=%d sag=%d alt=%d");
    BgfxDeviceBackend::SetAndroidSafeInsets(local_38[3],local_38[2],local_38[1],local_38[0]);
  }
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * CAndroidPlatform::SyncPresentation @ 006c0828
 * ============================================================ */

/* CAndroidPlatform::SyncPresentation() */

void __thiscall CAndroidPlatform::SyncPresentation(CAndroidPlatform *this)

{
  long lVar1;
  ulong uVar2;
  CInputCore *this_00;
  undefined8 local_38;
  int local_30;
  int local_2c;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  local_2c = 0;
  local_30 = 0;
  local_38 = 0;
  uVar2 = BgfxDeviceBackend::GetAndroidPresentationRect
                    (&local_2c,&local_30,(int *)((long)&local_38 + 4),(int *)&local_38);
  if ((uVar2 & 1) != 0) {
    if ((((local_2c != *(int *)(this + 0x9c)) || (local_30 != *(int *)(this + 0xa0))) ||
        (local_38._4_4_ != *(int *)(this + 0xa4))) || ((int)local_38 != *(int *)(this + 0xa8))) {
      *(int *)(this + 0x9c) = local_2c;
      *(int *)(this + 0xa0) = local_30;
      *(int *)(this + 0xa4) = local_38._4_4_;
      *(int *)(this + 0xa8) = (int)local_38;
      this_00 = (CInputCore *)M2Android_InputCore();
      m2input::CInputCore::SetPresentationViewport
                (this_00,local_2c,local_30,local_38._4_4_,(int)local_38);
      M2Shell_SetGamePresentationRect(local_2c,local_30,local_38._4_4_,(int)local_38);
      __android_log_print(4,"sancak2","sunum dikdortgeni: (%d,%d) %dx%d",local_2c,local_30,
                          local_38._4_4_,local_38 & 0xffffffff);
    }
  }
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * CAndroidPlatform::WriteDeviceReport @ 006c0924
 * ============================================================ */

/* CAndroidPlatform::WriteDeviceReport(unsigned int, unsigned int) */

void __thiscall
CAndroidPlatform::WriteDeviceReport(CAndroidPlatform *this,uint param_1,uint param_2)

{
  size_t __n;
  CAndroidPlatform *__src;
  CAndroidPlatform CVar1;
  long lVar2;
  ulong uVar3;
  FILE *__stream;
  undefined8 uVar4;
  char *pcVar5;
  char *pcVar6;
  uint uVar7;
  char *pcVar8;
  undefined8 local_80;
  undefined8 local_78;
  ulong local_70;
  ulong local_68;
  char *local_60;
  long local_58;
  
  lVar2 = tpidr_el0;
  local_58 = *(long *)(lVar2 + 0x28);
  CVar1 = this[0x50];
  __n = (ulong)((byte)CVar1 >> 1);
  if (((byte)CVar1 & 1) != 0) {
    __n = *(size_t *)(this + 0x58);
  }
  uVar3 = __n + 9;
  if (uVar3 < 0xfffffffffffffff0) {
    if (uVar3 < 0x17) {
      uVar7 = ((uint)uVar3 & 0xff) << 1;
      local_68 = 0;
      local_60 = (char *)0x0;
      local_70 = (ulong)(byte)uVar7;
    }
    else {
      local_60 = operator_new((uVar3 | 0xf) + 1);
      local_70 = (uVar3 | 0xf) + 2;
      uVar7 = (uint)local_70 & 0xff;
      local_68 = uVar3;
    }
    pcVar8 = (char *)((ulong)&local_70 | 1);
    pcVar6 = pcVar8;
    if ((uVar7 & 1) != 0) {
      pcVar6 = local_60;
    }
    __src = this + 0x51;
    if (((byte)CVar1 & 1) != 0) {
      __src = *(CAndroidPlatform **)(this + 0x60);
    }
    pcVar5 = pcVar6 + __n;
    memmove(pcVar6,__src,__n);
    uVar4 = s__caps_txt_003a8d55._0_8_;
    pcVar5[8] = 't';
    pcVar5[9] = '\0';
    *(undefined8 *)pcVar5 = uVar4;
    pcVar6 = pcVar8;
    if ((local_70 & 1) != 0) {
      pcVar6 = local_60;
    }
    uVar3 = BgfxDeviceBackend::WriteCapsReport(pcVar6);
    pcVar6 = pcVar8;
    if ((local_70 & 1) != 0) {
      pcVar6 = local_60;
    }
    if ((uVar3 & 1) == 0) {
      uVar4 = 6;
      pcVar5 = "caps raporu yazilamadi: %s";
    }
    else {
      __stream = fopen(pcVar6,"a");
      if (__stream != (FILE *)0x0) {
        local_80 = 0;
        local_78 = 0;
        BgfxDeviceBackend::GetAndroidPresentationRect
                  ((int *)((long)&local_78 + 4),(int *)&local_78,(int *)((long)&local_80 + 4),
                   (int *)&local_80);
        fprintf(__stream,"android.surface=%dx%d\n",(ulong)*(uint *)(this + 0x84),
                (ulong)*(uint *)(this + 0x88));
        fprintf(__stream,"android.backbuffer=%ux%u\n",(ulong)param_1,(ulong)param_2);
        fprintf(__stream,"android.presentation=%d,%d,%dx%d\n",local_78 >> 0x20,local_78 & 0xffffffff
                ,local_80 >> 0x20,local_80 & 0xffffffff);
        fprintf(__stream,"android.safe_insets=%d,%d,%d,%d\n",(ulong)*(uint *)(this + 0x8c),
                (ulong)*(uint *)(this + 0x90),(ulong)*(uint *)(this + 0x94),
                (ulong)*(uint *)(this + 0x98));
        if (*(long *)(*(long *)(this + 0x48) + 0x18) == 0) {
          uVar3 = 0;
        }
        else {
          uVar3 = (ulong)*(uint *)(*(long *)(*(long *)(this + 0x48) + 0x18) + 0x30);
        }
        fprintf(__stream,"android.sdk=%d\n",uVar3);
        fclose(__stream);
      }
      uVar4 = 4;
      pcVar5 = "caps raporu: %s";
      pcVar6 = pcVar8;
      if ((local_70 & 1) != 0) {
        pcVar6 = local_60;
      }
    }
    __android_log_print(uVar4,"sancak2",pcVar5,pcVar6);
    if ((local_70 & 1) != 0) {
      operator_delete(local_60);
    }
    if (*(long *)(lVar2 + 0x28) == local_58) {
      return;
    }
  }
  else if (*(long *)(lVar2 + 0x28) == local_58) {
                    /* WARNING: Subroutine does not return */
    FUN_006c1ae4(&local_70,(ulong)param_1,(ulong)param_2);
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * CAndroidPlatform::CreateOrResizeTouchOverlay @ 006c0ba0
 * ============================================================ */

/* CAndroidPlatform::CreateOrResizeTouchOverlay(unsigned int, unsigned int) */

void __thiscall
CAndroidPlatform::CreateOrResizeTouchOverlay(CAndroidPlatform *this,uint param_1,uint param_2)

{
  byte bVar1;
  
  M2Touch_SetSurfaceSize(*(int *)(this + 0x84),*(int *)(this + 0x88));
  if (this[0xac] != (CAndroidPlatform)0x0) {
    M2Touch_Resize(param_1,param_2);
    return;
  }
  bVar1 = M2Touch_Create(param_1,param_2);
  this[0xac] = (CAndroidPlatform)(bVar1 & 1);
  __android_log_print(4,"sancak2","M2Touch_Create(%u, %u) yuzey %dx%d -> %d",param_1,param_2,
                      *(undefined4 *)(this + 0x84),*(undefined4 *)(this + 0x88));
  return;
}

/* ============================================================
 * CAndroidPlatform::UpdateKeyboardPan @ 006c0c2c
 * ============================================================ */

/* CAndroidPlatform::UpdateKeyboardPan() */

void __thiscall CAndroidPlatform::UpdateKeyboardPan(CAndroidPlatform *this)

{
  int iVar1;
  long lVar2;
  undefined *puVar3;
  int iVar4;
  int iVar5;
  CWindow *this_00;
  ulong uVar6;
  int iVar7;
  long lVar8;
  _RECT a_Stack_68 [12];
  int local_5c;
  int local_58 [4];
  long local_48;
  
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  iVar4 = M2Shell_QueryImeInset();
  puVar3 = PTR_ms_singleton_00d79960;
  if (0 < iVar4) {
    this_00 = (CWindow *)
              UI::CWindowManager::GetActivateWindow(*(CWindowManager **)PTR_ms_singleton_00d79960);
    local_58[2] = 0;
    local_58[3] = 0;
    local_58[1] = 0;
    local_58[0] = 0;
    if (((this_00 != (CWindow *)0x0) && (this_00[0xa1] != (CWindow)0x0)) &&
       (uVar6 = BgfxDeviceBackend::GetAndroidPresentationRect
                          (local_58 + 3,local_58 + 2,local_58 + 1,local_58), (uVar6 & 1) != 0)) {
      iVar5 = BgfxDeviceBackend::GetAndroidPanY();
      iVar7 = 0;
      lVar8 = *(long *)(*(long *)puVar3 + 0x10);
      local_58[2] = local_58[2] + iVar5;
      if ((0 < lVar8) && (0 < local_58[0])) {
        UI::CWindow::GetVisualRect(this_00,a_Stack_68);
        iVar1 = (*(int *)(this + 0x88) - iVar4) + -0x18;
        iVar5 = local_58[2] + (int)(((float)local_58[0] / (float)lVar8) * (float)local_5c);
        iVar7 = iVar5 - iVar1;
        if (iVar7 == 0 || iVar5 < iVar1) {
          iVar7 = 0;
        }
      }
      goto LAB_006c0d28;
    }
  }
  iVar7 = 0;
LAB_006c0d28:
  iVar5 = BgfxDeviceBackend::GetAndroidPanY();
  if (iVar7 != iVar5) {
    BgfxDeviceBackend::SetAndroidPanY(iVar7);
    __android_log_print(4,"sancak2","klavye kaydirma: %d px (klavye %d px)",iVar7,iVar4);
  }
  if (*(long *)(lVar2 + 0x28) != local_48) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}

/* ============================================================
 * CAndroidPlatform::UpdateAnalogMove @ 006c0d88
 * ============================================================ */

/* CAndroidPlatform::UpdateAnalogMove() */

void __thiscall CAndroidPlatform::UpdateAnalogMove(CAndroidPlatform *this)

{
  CAndroidPlatform CVar1;
  undefined *puVar2;
  long lVar3;
  CPythonPlayer *this_00;
  float fVar4;
  
  lVar3 = M2Android_InputCore();
  puVar2 = PTR_ms_singleton_00d79958;
  CVar1 = *(CAndroidPlatform *)(lVar3 + 0x4dc);
  fVar4 = *(float *)(lVar3 + 0x4d8);
  if ((this[0x40] == CVar1) &&
     ((CVar1 == (CAndroidPlatform)0x0 || (ABS(fVar4 - *(float *)(this + 0x44)) < 0.5)))) {
    return;
  }
  this[0x40] = CVar1;
  this_00 = *(CPythonPlayer **)puVar2;
  *(float *)(this + 0x44) = fVar4;
  CPythonPlayer::NEW_SetTouchMoveState(this_00,fVar4,CVar1 != (CAndroidPlatform)0x0);
  return;
}

/* ============================================================
 * CAndroidPlatform::GetProcessSeed @ 006c0dfc
 * ============================================================ */

/* CAndroidPlatform::GetProcessSeed() */

void CAndroidPlatform::GetProcessSeed(void)

{
  (*(code *)PTR_getpid_00d7ce70)();
  return;
}

/* ============================================================
 * CAndroidPlatform::CheckPatcherRestart @ 006c0e00
 * ============================================================ */

/* CAndroidPlatform::CheckPatcherRestart() */

void CAndroidPlatform::CheckPatcherRestart(void)

{
  long lVar1;
  int iVar2;
  char *pcVar3;
  undefined1 auStack_1038 [4096];
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  pcVar3 = (char *)M2_ResolveWin32Path("perf_game_update.txt",auStack_1038,0x1000);
  iVar2 = access(pcVar3,0);
  if (iVar2 == 0) {
    remove("perf_game_update.txt");
  }
  pcVar3 = (char *)M2_ResolveWin32Path("newpatch.exe",auStack_1038,0x1000);
  iVar2 = access(pcVar3,0);
  if (iVar2 == 0) {
    TraceError(
              "newpatch.exe var - gercek istemci patchupdater.exe\'yi calistirip cikar (Android\'de yok)"
              );
  }
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(iVar2 != 0);
}

/* ============================================================
 * CAndroidPlatform::InitializeImageLibrary @ 006c0eb4
 * ============================================================ */

/* CAndroidPlatform::InitializeImageLibrary() */

void CAndroidPlatform::InitializeImageLibrary(void)

{
  (*(code *)PTR_ilInit_00d7ce90)();
  return;
}

/* ============================================================
 * CAndroidPlatform::LoadLocaleGlobal @ 006c0eb8
 * ============================================================ */

/* CAndroidPlatform::LoadLocaleGlobal() */

void CAndroidPlatform::LoadLocaleGlobal(void)

{
  LocaleService_LoadGlobal((HINSTANCE__ *)0x0);
  return;
}

/* ============================================================
 * CAndroidPlatform::ShowStartupSplash @ 006c0ec0
 * ============================================================ */

/* CAndroidPlatform::ShowStartupSplash() */

void __thiscall CAndroidPlatform::ShowStartupSplash(CAndroidPlatform *this)

{
  uchar *puVar1;
  CAndroidPlatform *pCVar2;
  uchar *puVar3;
  int *piVar4;
  int iVar5;
  int iVar6;
  size_t sVar7;
  CAndroidPlatform *pCVar8;
  int iVar9;
  int iVar10;
  CAndroidPlatform CVar11;
  long lVar12;
  undefined8 *puVar13;
  undefined *puVar14;
  undefined8 *puVar15;
  byte bVar16;
  int iVar17;
  uint uVar18;
  int iVar19;
  size_t __n;
  ulong uVar20;
  undefined1 *puVar21;
  CGraphicDevice *pCVar22;
  void *pvVar23;
  undefined8 *puVar24;
  ulong uVar25;
  long lVar26;
  undefined1 *puVar27;
  undefined1 *puVar29;
  ulong uVar30;
  undefined8 *puVar31;
  uchar *puVar32;
  undefined8 uVar33;
  undefined8 uVar34;
  undefined8 uVar35;
  ulong local_168;
  ulong local_160;
  void *local_158;
  undefined8 local_150;
  undefined1 *puStack_148;
  undefined1 *local_140;
  undefined8 uStack_138;
  undefined8 *local_128;
  undefined8 *local_120;
  undefined8 *local_118;
  CSplash aCStack_110 [48];
  ulong local_e0;
  uchar *puStack_d8;
  uchar *local_d0;
  undefined8 local_c0;
  uchar *puStack_b8;
  uchar *local_b0;
  undefined8 uStack_a8;
  long local_78;
  undefined1 *puVar28;
  
  lVar12 = tpidr_el0;
  local_78 = *(long *)(lVar12 + 0x28);
  CVar11 = this[0x50];
  sVar7 = (ulong)((byte)CVar11 >> 1);
  if (((byte)CVar11 & 1) != 0) {
    sVar7 = *(size_t *)(this + 0x58);
  }
  puVar1 = (uchar *)(sVar7 + 0x19);
  if (puVar1 < (uchar *)0xfffffffffffffff0) {
    if (puVar1 < (uchar *)0x17) {
      uVar18 = ((uint)puVar1 & 0xff) << 1;
      puStack_d8 = (uchar *)0x0;
      local_d0 = (uchar *)0x0;
      local_e0 = (ulong)(byte)uVar18;
    }
    else {
      local_d0 = operator_new(((ulong)puVar1 | 0xf) + 1);
      local_e0 = ((ulong)puVar1 | 0xf) + 2;
      uVar18 = (uint)local_e0 & 0xff;
      puStack_d8 = puVar1;
    }
    puVar32 = (uchar *)((ulong)&local_e0 | 1);
    puVar1 = puVar32;
    if ((uVar18 & 1) != 0) {
      puVar1 = local_d0;
    }
    pCVar2 = this + 0x51;
    pCVar8 = pCVar2;
    if (((byte)CVar11 & 1) != 0) {
      pCVar8 = *(CAndroidPlatform **)(this + 0x60);
    }
    puVar3 = puVar1 + sVar7;
    memmove(puVar1,pCVar8,sVar7);
    puVar3[0x19] = '\0';
    uVar33 = s__mobile_root_lib_logo_bmp_00397181._0_8_;
    *(ulong *)(puVar3 + 8) =
         CONCAT71(s__mobile_root_lib_logo_bmp_00397181._9_7_,s__mobile_root_lib_logo_bmp_00397181[8]
                 );
    *(undefined8 *)puVar3 = uVar33;
    uVar33 = CONCAT17(s__mobile_root_lib_logo_bmp_00397181[0x10],
                      s__mobile_root_lib_logo_bmp_00397181._9_7_);
    *(undefined8 *)(puVar3 + 0x11) = s__mobile_root_lib_logo_bmp_00397181._17_8_;
    *(undefined8 *)(puVar3 + 9) = uVar33;
    puVar1 = puVar32;
    if ((local_e0 & 1) != 0) {
      puVar1 = local_d0;
    }
    iVar17 = access((char *)puVar1,0);
    if (iVar17 != 0) {
      CVar11 = this[0x50];
      sVar7 = (ulong)((byte)CVar11 >> 1);
      if (((byte)CVar11 & 1) != 0) {
        sVar7 = *(size_t *)(this + 0x58);
      }
      puVar1 = (uchar *)(sVar7 + 0xd);
      if ((uchar *)0xffffffffffffffef < puVar1) {
        if (*(long *)(lVar12 + 0x28) == local_78) {
                    /* WARNING: Subroutine does not return */
          FUN_006c1ae4(&local_c0);
        }
        goto LAB_006c1680;
      }
      if (puVar1 < (uchar *)0x17) {
        uVar18 = ((uint)puVar1 & 0xff) << 1;
        puStack_b8 = (uchar *)0x0;
        local_b0 = (uchar *)0x0;
        local_c0 = (ulong)(byte)uVar18;
      }
      else {
        uVar20 = ((ulong)puVar1 | 0xf) + 1;
        local_b0 = operator_new(uVar20);
        local_c0 = uVar20 | 1;
        uVar18 = (uint)local_c0 & 0xff;
        puStack_b8 = puVar1;
      }
      puVar1 = (uchar *)((ulong)&local_c0 | 1);
      if ((uVar18 & 1) != 0) {
        puVar1 = local_b0;
      }
      pCVar8 = pCVar2;
      if (((byte)CVar11 & 1) != 0) {
        pCVar8 = *(CAndroidPlatform **)(this + 0x60);
      }
      puVar3 = puVar1 + sVar7;
      memmove(puVar1,pCVar8,sVar7);
      puVar3[0xd] = '\0';
      uVar33 = CONCAT53(s__lib_logo_bmp_0039719b._8_5_,s__lib_logo_bmp_0039719b._5_3_);
      *(ulong *)puVar3 = CONCAT35(s__lib_logo_bmp_0039719b._5_3_,s__lib_logo_bmp_0039719b._0_5_);
      *(undefined8 *)(puVar3 + 5) = uVar33;
      if ((local_e0 & 1) != 0) {
        operator_delete(local_d0);
      }
      puStack_d8 = puStack_b8;
      local_e0 = local_c0;
      local_d0 = local_b0;
    }
    if ((local_e0 & 1) != 0) {
      puVar32 = local_d0;
    }
    CSplash::CSplash(aCStack_110,(char *)puVar32,0x808080);
    CSplash::ShowSplash(aCStack_110);
    iVar17 = 0;
    local_128 = (undefined8 *)0x0;
    local_120 = (undefined8 *)0x0;
    local_118 = (undefined8 *)0x0;
    do {
      FUN_006c168c(&local_c0);
      CVar11 = this[0x50];
      sVar7 = (ulong)((byte)CVar11 >> 1);
      if (((byte)CVar11 & 1) != 0) {
        sVar7 = *(size_t *)(this + 0x58);
      }
      puStack_148 = (undefined1 *)0x0;
      local_150 = 0;
      uStack_138 = 0;
      local_140 = (undefined1 *)0x0;
      __n = strlen((char *)&local_c0);
      uVar20 = sVar7 + __n;
      if (0xffffffffffffffef < uVar20) {
        if (*(long *)(lVar12 + 0x28) == local_78) {
                    /* WARNING: Subroutine does not return */
          FUN_006c1ae4(&local_168);
        }
        goto LAB_006c1680;
      }
      if (uVar20 < 0x17) {
        uVar18 = ((uint)uVar20 & 0xff) << 1;
        local_160 = 0;
        local_158 = (void *)0x0;
        local_168 = (ulong)(byte)uVar18;
      }
      else {
        uVar25 = (uVar20 | 0xf) + 1;
        local_158 = operator_new(uVar25);
        local_168 = uVar25 | 1;
        uVar18 = (uint)local_168 & 0xff;
        local_160 = uVar20;
      }
      pvVar23 = (void *)((ulong)&local_168 | 1);
      if ((uVar18 & 1) != 0) {
        pvVar23 = local_158;
      }
      pCVar8 = pCVar2;
      if (((byte)CVar11 & 1) != 0) {
        pCVar8 = *(CAndroidPlatform **)(this + 0x60);
      }
      memmove(pvVar23,pCVar8,sVar7);
      memmove((void *)((long)pvVar23 + sVar7),&local_c0,__n);
      *(undefined1 *)((long)((long)pvVar23 + sVar7) + __n) = 0;
      uVar20 = m2bmp::LoadBmpFile((basic_string *)&local_168,(SImage *)&local_150);
      if ((local_168 & 1) != 0) {
        operator_delete(local_158);
      }
      puVar15 = local_120;
      if ((uVar20 & 1) == 0) {
        if (puStack_148 != (undefined1 *)0x0) {
          local_140 = puStack_148;
          operator_delete(puStack_148);
        }
        break;
      }
      if (3 < (ulong)((long)local_140 - (long)puStack_148)) {
        lVar26 = 0;
        do {
          if (((puStack_148[lVar26] == -1) && (puStack_148[lVar26 + 1] == '\0')) &&
             (puStack_148[lVar26 + 2] == -1)) {
            puStack_148[lVar26 + 3] = 0;
          }
          uVar20 = lVar26 + 7;
          lVar26 = lVar26 + 4;
        } while (uVar20 < (ulong)((long)local_140 - (long)puStack_148));
      }
      if (local_120 == local_118) {
        std::__ndk1::vector<m2bmp::SImage,std::__ndk1::allocator<m2bmp::SImage>>::
        __push_back_slow_path<m2bmp::SImage_const&>
                  ((vector<m2bmp::SImage,std::__ndk1::allocator<m2bmp::SImage>> *)&local_128,
                   (SImage *)&local_150);
        puVar21 = puStack_148;
        puVar29 = local_140;
      }
      else {
        local_120[2] = 0;
        local_120[3] = 0;
        *local_120 = local_150;
        local_120[1] = 0;
        uVar20 = (long)local_140 - (long)puStack_148;
        puVar21 = local_140;
        if (uVar20 != 0) {
          if ((long)uVar20 < 0) {
            if (*(long *)(lVar12 + 0x28) == local_78) {
                    /* WARNING: Subroutine does not return */
              FUN_006c1eb0(local_120 + 1);
            }
            goto LAB_006c1680;
          }
          puVar21 = operator_new(uVar20);
          puVar15[1] = puVar21;
          puVar15[2] = puVar21;
          puVar15[3] = puVar21 + uVar20;
          puVar29 = puVar21;
          if (puStack_148 != local_140) {
            uVar20 = (long)local_140 - (long)puStack_148;
            puVar28 = puStack_148;
            if ((0x1f < uVar20) && (0x1f < (ulong)((long)puVar21 - (long)puStack_148))) {
              uVar30 = uVar20 & 0xffffffffffffffe0;
              puVar31 = (undefined8 *)(puStack_148 + 0x10);
              puVar29 = puVar21 + uVar30;
              puVar24 = (undefined8 *)(puVar21 + 0x10);
              uVar25 = uVar30;
              do {
                puVar13 = puVar31 + -1;
                uVar33 = puVar31[-2];
                uVar35 = puVar31[1];
                uVar34 = *puVar31;
                puVar31 = puVar31 + 4;
                uVar25 = uVar25 - 0x20;
                puVar24[-1] = *puVar13;
                puVar24[-2] = uVar33;
                puVar24[1] = uVar35;
                *puVar24 = uVar34;
                puVar24 = puVar24 + 4;
              } while (uVar25 != 0);
              puVar28 = puStack_148 + uVar30;
              puVar21 = puVar29;
              if (uVar20 == uVar30) goto LAB_006c130c;
            }
            do {
              puVar27 = puVar28 + 1;
              *puVar21 = *puVar28;
              puVar28 = puVar27;
              puVar29 = puVar21 + 1;
              puVar21 = puVar21 + 1;
            } while (puVar27 != local_140);
          }
LAB_006c130c:
          puVar15[2] = puVar29;
          puVar21 = puStack_148;
        }
        local_120 = puVar15 + 4;
        puVar29 = local_140;
      }
      local_140 = puVar21;
      if (local_140 != (undefined1 *)0x0) {
        operator_delete(local_140);
        puVar29 = local_140;
      }
      local_140 = puVar29;
      iVar17 = iVar17 + 1;
    } while (iVar17 != 0x20);
    uVar20 = timeGetTime();
    puVar14 = PTR_s_active_00d79970;
    iVar17 = (int)uVar20;
    while (iVar19 = timeGetTime(uVar20), (uint)(iVar19 - iVar17) < 3000) {
      if (local_128 != local_120) {
        iVar19 = timeGetTime();
        uVar25 = (ulong)((uint)(iVar19 - iVar17) >> 1) / 0x23;
        uVar30 = (long)local_120 - (long)local_128 >> 5;
        uVar20 = 0;
        if (uVar30 != 0) {
          uVar20 = uVar25 / uVar30;
        }
        iVar19 = *(int *)(this + 0x84);
        piVar4 = (int *)(local_128 + (uVar25 - uVar20 * uVar30) * 4);
        if (iVar19 < 0) {
          iVar19 = iVar19 + 1;
        }
        iVar9 = *piVar4;
        iVar10 = piVar4[1];
        iVar5 = iVar9;
        if (iVar9 < 0) {
          iVar5 = iVar9 + 1;
        }
        iVar6 = iVar10;
        if (iVar10 < 0) {
          iVar6 = iVar10 + 1;
        }
        BgfxDeviceBackend::SetAndroidSplashOverlay
                  ((iVar19 >> 1) - (iVar5 >> 1),
                   (int)((float)*(int *)(this + 0x88) * 0.8) - (iVar6 >> 1),iVar9,iVar10,
                   *(uchar **)(piVar4 + 2));
      }
      pCVar22 = *(CGraphicDevice **)puVar14;
      if (pCVar22 != (CGraphicDevice *)0x0) {
        CGraphicDevice::Present(pCVar22);
      }
      uVar18 = usleep(33000);
      uVar20 = (ulong)uVar18;
    }
    BgfxDeviceBackend::SetAndroidSplashOverlay(0,0,0,0,(uchar *)0x0);
    CSplash::CloseSplash(aCStack_110);
    puStack_b8 = (uchar *)0x0;
    local_c0 = 0;
    uStack_a8 = 0;
    local_b0 = (uchar *)0x0;
    bVar16 = m2bmp::LoadBmpFile((basic_string *)&local_e0,(SImage *)&local_c0);
    if (((bVar16 & 0 < (int)local_c0) == 1) && (0 < local_c0._4_4_)) {
      iVar17 = *(int *)(this + 0x84) - (int)local_c0;
      iVar19 = *(int *)(this + 0x88) - local_c0._4_4_;
      if (iVar17 < 0) {
        iVar17 = iVar17 + 1;
      }
      if (iVar19 < 0) {
        iVar19 = iVar19 + 1;
      }
      BgfxDeviceBackend::SetAndroidSplashImage
                (iVar17 >> 1,iVar19 >> 1,(int)local_c0,local_c0._4_4_,puStack_b8);
      pCVar22 = *(CGraphicDevice **)puVar14;
      if (pCVar22 != (CGraphicDevice *)0x0) {
        CGraphicDevice::Present(pCVar22);
      }
    }
    if (puStack_b8 != (uchar *)0x0) {
      local_b0 = puStack_b8;
      operator_delete(puStack_b8);
    }
    puVar15 = local_128;
    puVar31 = local_120;
    if (local_128 != (undefined8 *)0x0) {
      while (puVar24 = puVar31, puVar24 != puVar15) {
        pvVar23 = (void *)puVar24[-3];
        puVar31 = puVar24 + -4;
        if (pvVar23 != (void *)0x0) {
          puVar24[-2] = pvVar23;
          operator_delete(pvVar23);
        }
      }
      local_120 = puVar15;
      operator_delete(local_128);
    }
    CSplash::~CSplash(aCStack_110);
    if ((local_e0 & 1) != 0) {
      operator_delete(local_d0);
    }
    if (*(long *)(lVar12 + 0x28) == local_78) {
      return;
    }
  }
  else if (*(long *)(lVar12 + 0x28) == local_78) {
                    /* WARNING: Subroutine does not return */
    FUN_006c1ae4(&local_e0);
  }
LAB_006c1680:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * CAndroidPlatform::GetClientRootDir @ 006c1684
 * ============================================================ */

/* CAndroidPlatform::GetClientRootDir() */

CAndroidPlatform * __thiscall CAndroidPlatform::GetClientRootDir(CAndroidPlatform *this)

{
  return this + 0x50;
}

/* ============================================================
 * CAndroidPlatform::DestroyWebBrowser @ 006c17a4
 * ============================================================ */

/* CAndroidPlatform::DestroyWebBrowser() */

void CAndroidPlatform::DestroyWebBrowser(void)

{
  WebBrowser_Destroy();
  M2Touch_ReleaseGraphics();
  return;
}

/* ============================================================
 * CAndroidPlatform::PrepareLauncherEnvironment @ 006c17b8
 * ============================================================ */

/* CAndroidPlatform::PrepareLauncherEnvironment() */

void CAndroidPlatform::PrepareLauncherEnvironment(void)

{
  long lVar1;
  int iVar2;
  FILE *pFVar3;
  stat sStack_e8;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  mkdir("pack",0x1fd);
  FUN_006c168c(sStack_e8.__unused + 1);
  iVar2 = stat((char *)(sStack_e8.__unused + 1),&sStack_e8);
  if (iVar2 != 0) {
    pFVar3 = fopen((char *)(sStack_e8.__unused + 1),"w");
    if (pFVar3 != (FILE *)0x0) {
      fclose(pFVar3);
    }
    __android_log_print(5,"sancak2","%s yoktu - bos olusturuldu",sStack_e8.__unused + 1);
  }
  FUN_006c168c(sStack_e8.__unused + 1);
  iVar2 = stat((char *)(sStack_e8.__unused + 1),&sStack_e8);
  if (iVar2 != 0) {
    pFVar3 = fopen((char *)(sStack_e8.__unused + 1),"w");
    if (pFVar3 != (FILE *)0x0) {
      fclose(pFVar3);
    }
    __android_log_print(5,"sancak2","%s yoktu - bos olusturuldu",sStack_e8.__unused + 1);
  }
  FUN_006c168c(sStack_e8.__unused + 1);
  iVar2 = stat((char *)(sStack_e8.__unused + 1),&sStack_e8);
  if (iVar2 != 0) {
    pFVar3 = fopen((char *)(sStack_e8.__unused + 1),"w");
    if (pFVar3 != (FILE *)0x0) {
      fclose(pFVar3);
    }
    __android_log_print(5,"sancak2","%s yoktu - bos olusturuldu",sStack_e8.__unused + 1);
  }
  FUN_006c168c(sStack_e8.__unused + 1);
  iVar2 = stat((char *)(sStack_e8.__unused + 1),&sStack_e8);
  if (iVar2 != 0) {
    pFVar3 = fopen((char *)(sStack_e8.__unused + 1),"w");
    if (pFVar3 != (FILE *)0x0) {
      fclose(pFVar3);
    }
    __android_log_print(5,"sancak2","%s yoktu - bos olusturuldu",sStack_e8.__unused + 1);
  }
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * CAndroidPlatform::CreateMainWindow @ 006c1968
 * ============================================================ */

/* CAndroidPlatform::CreateMainWindow(int, int, bool) */

uint __thiscall
CAndroidPlatform::CreateMainWindow(CAndroidPlatform *this,int param_1,int param_2,bool param_3)

{
  uint uVar1;
  
  uVar1 = CAndroidApplicationPlatformBase::CreateMainWindow
                    ((CAndroidApplicationPlatformBase *)this,param_1,param_2,param_3);
  if ((uVar1 & 1) != 0) {
    M2_Android_WebView_SetClientSize(param_1,param_2);
  }
  return uVar1 & 1;
}

/* ============================================================
 * CAndroidPlatform::AdjustWindowSize @ 006c19ac
 * ============================================================ */

/* CAndroidPlatform::AdjustWindowSize(int, int) */

void __thiscall CAndroidPlatform::AdjustWindowSize(CAndroidPlatform *this,int param_1,int param_2)

{
  CAndroidApplicationPlatformBase::AdjustWindowSize
            ((CAndroidApplicationPlatformBase *)this,param_1,param_2);
  M2_Android_WebView_SetClientSize(param_1,param_2);
  return;
}

/* ============================================================
 * CAndroidBgfxCallback::~CAndroidBgfxCallback @ 006c19d8
 * ============================================================ */

/* CAndroidBgfxCallback::~CAndroidBgfxCallback() */

void __thiscall CAndroidBgfxCallback::~CAndroidBgfxCallback(CAndroidBgfxCallback *this)

{
  (*(code *)PTR_operator_delete_00d7ccb0)();
  return;
}

/* ============================================================
 * CAndroidBgfxCallback::profilerBegin @ 006c19dc
 * ============================================================ */

/* CAndroidBgfxCallback::profilerBegin(char const*, unsigned int, char const*, unsigned short) */

void CAndroidBgfxCallback::profilerBegin(char *param_1,uint param_2,char *param_3,ushort param_4)

{
  return;
}

/* ============================================================
 * CAndroidBgfxCallback::profilerBeginLiteral @ 006c19e0
 * ============================================================ */

/* CAndroidBgfxCallback::profilerBeginLiteral(char const*, unsigned int, char const*, unsigned
   short) */

void CAndroidBgfxCallback::profilerBeginLiteral
               (char *param_1,uint param_2,char *param_3,ushort param_4)

{
  return;
}

/* ============================================================
 * CAndroidBgfxCallback::profilerEnd @ 006c19e4
 * ============================================================ */

/* CAndroidBgfxCallback::profilerEnd() */

void CAndroidBgfxCallback::profilerEnd(void)

{
  return;
}

/* ============================================================
 * CAndroidBgfxCallback::cacheReadSize @ 006c19e8
 * ============================================================ */

/* CAndroidBgfxCallback::cacheReadSize(unsigned long) */

undefined8 CAndroidBgfxCallback::cacheReadSize(ulong param_1)

{
  return 0;
}

/* ============================================================
 * CAndroidBgfxCallback::cacheRead @ 006c19f0
 * ============================================================ */

/* CAndroidBgfxCallback::cacheRead(unsigned long, void*, unsigned int) */

undefined8 CAndroidBgfxCallback::cacheRead(ulong param_1,void *param_2,uint param_3)

{
  return 0;
}

/* ============================================================
 * CAndroidBgfxCallback::cacheWrite @ 006c19f8
 * ============================================================ */

/* CAndroidBgfxCallback::cacheWrite(unsigned long, void const*, unsigned int) */

void CAndroidBgfxCallback::cacheWrite(ulong param_1,void *param_2,uint param_3)

{
  return;
}

/* ============================================================
 * CAndroidBgfxCallback::screenShot @ 006c19fc
 * ============================================================ */

/* CAndroidBgfxCallback::screenShot(char const*, unsigned int, unsigned int, unsigned int,
   bgfx::TextureFormat::Enum, void const*, unsigned int, bool) */

void CAndroidBgfxCallback::screenShot(void)

{
  return;
}

/* ============================================================
 * CAndroidBgfxCallback::captureBegin @ 006c1a00
 * ============================================================ */

/* CAndroidBgfxCallback::captureBegin(unsigned int, unsigned int, unsigned int,
   bgfx::TextureFormat::Enum, bool) */

void CAndroidBgfxCallback::captureBegin(void)

{
  return;
}

/* ============================================================
 * CAndroidBgfxCallback::captureEnd @ 006c1a04
 * ============================================================ */

/* CAndroidBgfxCallback::captureEnd() */

void CAndroidBgfxCallback::captureEnd(void)

{
  return;
}

/* ============================================================
 * CAndroidBgfxCallback::captureFrame @ 006c1a08
 * ============================================================ */

/* CAndroidBgfxCallback::captureFrame(void const*, unsigned int) */

void CAndroidBgfxCallback::captureFrame(void *param_1,uint param_2)

{
  return;
}

/* ============================================================
 * CAndroidPlatform::GetPackDir @ 006c1a0c
 * ============================================================ */

/* CAndroidPlatform::GetPackDir() */

CAndroidPlatform * __thiscall CAndroidPlatform::GetPackDir(CAndroidPlatform *this)

{
  return this + 0x68;
}

/* ============================================================
 * CAndroidPlatform::GetPythonHomeDir @ 006c1a14
 * ============================================================ */

/* CAndroidPlatform::GetPythonHomeDir() */

CAndroidPlatform * __thiscall CAndroidPlatform::GetPythonHomeDir(CAndroidPlatform *this)

{
  return this + 0x50;
}

/* ============================================================
 * CAndroidPlatform::ToNativePath @ 006c1a1c
 * ============================================================ */

/* CAndroidPlatform::ToNativePath(std::__ndk1::basic_string<char, std::__ndk1::char_traits<char>,
   std::__ndk1::allocator<char> > const&) */

void CAndroidPlatform::ToNativePath(basic_string *param_1)

{
  ulong uVar1;
  void *__src;
  byte *in_x1;
  long *in_x8;
  long lVar2;
  void *__dest;
  long lVar3;
  
  if ((*in_x1 & 1) == 0) {
    lVar3 = *(long *)in_x1;
    lVar2 = *(long *)(in_x1 + 0x10);
    in_x8[1] = *(long *)(in_x1 + 8);
    *in_x8 = lVar3;
    in_x8[2] = lVar2;
    return;
  }
  uVar1 = *(ulong *)(in_x1 + 8);
  __src = *(void **)(in_x1 + 0x10);
  if (uVar1 < 0x17) {
    __dest = (void *)((long)in_x8 + 1);
    *(char *)in_x8 = (char)((int)uVar1 << 1);
  }
  else {
    if (0xffffffffffffffef < uVar1) {
                    /* WARNING: Subroutine does not return */
      FUN_006c1ae4();
    }
    __dest = operator_new((uVar1 | 0xf) + 1);
    in_x8[1] = uVar1;
    in_x8[2] = (long)__dest;
    *in_x8 = (uVar1 | 0xf) + 2;
  }
  memmove(__dest,__src,uVar1 + 1);
  return;
}

/* ============================================================
 * CAndroidPlatform::BeginTimerPeriod @ 006c1ab8
 * ============================================================ */

/* CAndroidPlatform::BeginTimerPeriod() */

undefined8 CAndroidPlatform::BeginTimerPeriod(void)

{
  return 1;
}

/* ============================================================
 * CAndroidPlatform::EndTimerPeriod @ 006c1ac0
 * ============================================================ */

/* CAndroidPlatform::EndTimerPeriod() */

void CAndroidPlatform::EndTimerPeriod(void)

{
  return;
}

/* ============================================================
 * CAndroidPlatform::OpenDebugConsole @ 006c1ac4
 * ============================================================ */

/* CAndroidPlatform::OpenDebugConsole() */

void CAndroidPlatform::OpenDebugConsole(void)

{
  return;
}

/* ============================================================
 * CAndroidPlatform::IsVerboseLogRequested @ 006c1ac8
 * ============================================================ */

/* CAndroidPlatform::IsVerboseLogRequested() */

CAndroidPlatform __thiscall CAndroidPlatform::IsVerboseLogRequested(CAndroidPlatform *this)

{
  return this[0x80];
}

/* ============================================================
 * CAndroidPlatform::GetBgfxDebugCallback @ 006c1ad0
 * ============================================================ */

/* CAndroidPlatform::GetBgfxDebugCallback() */

CAndroidPlatform * __thiscall CAndroidPlatform::GetBgfxDebugCallback(CAndroidPlatform *this)

{
  return this + 0xb0;
}

/* ============================================================
 * CAndroidPlatform::CreateNetworkDevice @ 006c1ad8
 * ============================================================ */

/* CAndroidPlatform::CreateNetworkDevice() */

undefined8 CAndroidPlatform::CreateNetworkDevice(void)

{
  return 1;
}

/* ============================================================
 * CAndroidPlatform::DestroyNetworkDevice @ 006c1ae0
 * ============================================================ */

/* CAndroidPlatform::DestroyNetworkDevice() */

void CAndroidPlatform::DestroyNetworkDevice(void)

{
  return;
}

/* ============================================================
 * M2Android_NowMs @ 006c1f48
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_NowMs() */

ulong M2Android_NowMs(void)

{
  long lVar1;
  int iVar2;
  timespec local_38;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  local_38.tv_sec = 0;
  local_38.tv_nsec = 0;
  iVar2 = clock_gettime(1,&local_38);
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return (ulong)(local_38.tv_nsec + local_38.tv_sec * 1000000000) / 1000000;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(iVar2);
}

/* ============================================================
 * M2Android_NowUs @ 006c1fc0
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_NowUs() */

ulong M2Android_NowUs(void)

{
  long lVar1;
  int iVar2;
  timespec local_38;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  local_38.tv_sec = 0;
  local_38.tv_nsec = 0;
  iVar2 = clock_gettime(1,&local_38);
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return (ulong)(local_38.tv_nsec + local_38.tv_sec * 1000000000) / 1000;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(iVar2);
}

/* ============================================================
 * android_main @ 006c267c
 * ============================================================ */

void android_main(android_app *param_1)

{
  ulong uVar1;
  ulong uVar2;
  char *pcVar3;
  char *pcVar4;
  long lVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  int iVar8;
  int iVar9;
  size_t sVar10;
  ulong uVar11;
  uint uVar12;
  char *pcVar13;
  char *pcVar14;
  byte local_1d0 [16];
  char *local_1c0;
  ulong local_1b8;
  size_t local_1b0;
  char *local_1a8;
  undefined1 local_1a0 [128];
  stat sStack_120;
  long local_68;
  
  lVar5 = tpidr_el0;
  local_68 = *(long *)(lVar5 + 0x28);
  __android_log_print(4,"sancak2","android_main basladi (isaretci=%zu bayt, wchar_t=%zu bayt)",8,4);
  pcVar13 = *(char **)(*(long *)(param_1 + 0x18) + 0x20);
  pcVar14 = *(char **)(*(long *)(param_1 + 0x18) + 0x28);
  if (((pcVar14 == (char *)0x0) || (*pcVar14 == '\0')) && (pcVar14 = ".", pcVar13 != (char *)0x0)) {
    pcVar14 = pcVar13;
  }
  sVar10 = strlen(pcVar14);
  if (sVar10 < 0xfffffffffffffff0) {
    if (sVar10 < 0x17) {
      pcVar13 = (char *)((ulong)&local_1b8 | 1);
      local_1b8 = CONCAT71(local_1b8._1_7_,(char)((int)sVar10 << 1));
    }
    else {
      pcVar13 = operator_new((sVar10 | 0xf) + 1);
      local_1b8 = (sVar10 | 0xf) + 2;
      local_1b0 = sVar10;
      local_1a8 = pcVar13;
    }
    memmove(pcVar13,pcVar14,sVar10);
    pcVar13[sVar10] = '\0';
    pcVar14 = (char *)((ulong)&local_1b8 | 1);
    pcVar13 = pcVar14;
    if ((local_1b8 & 1) != 0) {
      pcVar13 = local_1a8;
    }
    iVar8 = chdir(pcVar13);
    if (iVar8 != 0) {
      pcVar13 = pcVar14;
      if ((local_1b8 & 1) != 0) {
        pcVar13 = local_1a8;
      }
      __android_log_print(6,"sancak2","calisma dizini ayarlanamadi: %s",pcVar13);
    }
    pcVar13 = pcVar14;
    if ((local_1b8 & 1) != 0) {
      pcVar13 = local_1a8;
    }
    M2_Android_SetFilesDirectory(pcVar13);
    pcVar13 = pcVar14;
    if ((local_1b8 & 1) != 0) {
      pcVar13 = local_1a8;
    }
    __android_log_print(4,"sancak2","veri koku (calisma dizini): %s",pcVar13);
    uVar11 = local_1b8;
    sVar10 = local_1b8 >> 1 & 0x7f;
    if ((local_1b8 & 1) != 0) {
      sVar10 = local_1b0;
    }
    uVar1 = sVar10 + 0xf;
    if (uVar1 < 0xfffffffffffffff0) {
      if (uVar1 < 0x17) {
        uVar12 = ((uint)uVar1 & 0xff) << 1;
        local_1a0._8_8_ = 0;
        local_1a0._16_8_ = (char *)0x0;
        local_1a0._1_7_ = 0;
        local_1a0[0] = (byte)uVar12;
      }
      else {
        uVar2 = (uVar1 | 0xf) + 1;
        local_1a0._16_8_ = operator_new(uVar2);
        local_1a0._0_8_ = uVar2 | 1;
        uVar12 = (uint)local_1a0._0_8_ & 0xff;
        local_1a0._8_8_ = uVar1;
      }
      pcVar13 = (char *)((ulong)local_1a0 | 1);
      if ((uVar12 & 1) != 0) {
        pcVar13 = (char *)local_1a0._16_8_;
      }
      pcVar4 = pcVar14;
      if ((uVar11 & 1) != 0) {
        pcVar4 = local_1a8;
      }
      pcVar3 = pcVar13 + sVar10;
      memmove(pcVar13,pcVar4,sVar10);
      pcVar3[0xf] = '\0';
      uVar6 = CONCAT17(s__m2_tani_pyboot_003738dc[7],s__m2_tani_pyboot_003738dc._0_7_);
      *(ulong *)(pcVar3 + 7) =
           CONCAT71(s__m2_tani_pyboot_003738dc._8_7_,s__m2_tani_pyboot_003738dc[7]);
      *(undefined8 *)pcVar3 = uVar6;
      pcVar13 = (char *)((ulong)local_1a0 | 1);
      if ((local_1a0._0_8_ & 1) != 0) {
        pcVar13 = (char *)local_1a0._16_8_;
      }
      iVar8 = stat(pcVar13,(stat *)(local_1a0 + 0x80));
      if ((local_1a0._0_8_ & 1) != 0) {
        operator_delete((void *)local_1a0._16_8_);
      }
      uVar11 = local_1b8;
      sVar10 = local_1b8 >> 1 & 0x7f;
      if ((local_1b8 & 1) != 0) {
        sVar10 = local_1b0;
      }
      uVar1 = sVar10 + 0x11;
      if (uVar1 < 0xfffffffffffffff0) {
        if (uVar1 < 0x17) {
          uVar12 = ((uint)uVar1 & 0xff) << 1;
          local_1a0._8_8_ = 0;
          local_1a0._16_8_ = (char *)0x0;
          local_1a0._1_7_ = 0;
          local_1a0[0] = (byte)uVar12;
        }
        else {
          uVar2 = (uVar1 | 0xf) + 1;
          local_1a0._16_8_ = operator_new(uVar2);
          local_1a0._0_8_ = uVar2 | 1;
          uVar12 = (uint)local_1a0._0_8_ & 0xff;
          local_1a0._8_8_ = uVar1;
        }
        pcVar13 = (char *)((ulong)local_1a0 | 1);
        if ((uVar12 & 1) != 0) {
          pcVar13 = (char *)local_1a0._16_8_;
        }
        pcVar4 = pcVar14;
        if ((uVar11 & 1) != 0) {
          pcVar4 = local_1a8;
        }
        pcVar3 = pcVar13 + sVar10;
        memmove(pcVar13,pcVar4,sVar10);
        uVar7 = s__m2_ayrintili_log_00376027._8_8_;
        uVar6 = s__m2_ayrintili_log_00376027._0_8_;
        pcVar3[0x10] = 'g';
        pcVar3[0x11] = '\0';
        *(undefined8 *)(pcVar3 + 8) = uVar7;
        *(undefined8 *)pcVar3 = uVar6;
        pcVar13 = (char *)((ulong)local_1a0 | 1);
        if ((local_1a0._0_8_ & 1) != 0) {
          pcVar13 = (char *)local_1a0._16_8_;
        }
        iVar9 = stat(pcVar13,(stat *)(local_1a0 + 0x80));
        if ((local_1a0._0_8_ & 1) != 0) {
          operator_delete((void *)local_1a0._16_8_);
        }
        CAndroidPlatform::CAndroidPlatform
                  ((CAndroidPlatform *)(local_1a0 + 0x80),param_1,(basic_string *)&local_1b8,
                   iVar9 == 0);
        M2Android_InstallJavaInputBridge
                  (*(_JavaVM **)(*(long *)(param_1 + 0x18) + 8),
                   *(_jobject **)(*(long *)(param_1 + 0x18) + 0x18));
        M2_Android_WebView_Attach
                  (*(undefined8 *)(*(long *)(param_1 + 0x18) + 8),
                   *(undefined8 *)(*(long *)(param_1 + 0x18) + 0x18));
        M2Shell_AttachJava(*(_JavaVM **)(*(long *)(param_1 + 0x18) + 8),
                           *(_jobject **)(*(long *)(param_1 + 0x18) + 0x18));
        FUN_006c2d84(local_1a0,&local_1b8,"/Documents");
        pcVar13 = (char *)((ulong)local_1a0 | 1);
        if ((local_1a0._0_8_ & 1) != 0) {
          pcVar13 = (char *)local_1a0._16_8_;
        }
        M2_Android_SetShellFolderPath(5,pcVar13);
        if ((local_1a0._0_8_ & 1) != 0) {
          operator_delete((void *)local_1a0._16_8_);
        }
        pcVar13 = pcVar14;
        if ((local_1b8 & 1) != 0) {
          pcVar13 = local_1a8;
        }
        BgfxDeviceBackend::SetShaderBaseDirectory(pcVar13);
        FUN_006c2d84(local_1a0,&local_1b8,"/m2font.gdibake");
        pcVar13 = (char *)((ulong)local_1a0 | 1);
        if ((local_1a0._0_8_ & 1) != 0) {
          pcVar13 = (char *)local_1a0._16_8_;
        }
        m2gdi::M2GdiFont_SetArchivePath(pcVar13);
        if ((local_1a0._0_8_ & 1) != 0) {
          operator_delete((void *)local_1a0._16_8_);
        }
        FUN_006c2d84(local_1a0,&local_1b8,"/mobile_layout.json");
        pcVar13 = (char *)((ulong)local_1a0 | 1);
        if ((local_1a0._0_8_ & 1) != 0) {
          pcVar13 = (char *)local_1a0._16_8_;
        }
        M2Touch_SetLayoutPath(pcVar13);
        if ((local_1a0._0_8_ & 1) != 0) {
          operator_delete((void *)local_1a0._16_8_);
        }
        FUN_006c2d84(local_1d0,&local_1b8,"/mobile_root");
        pcVar13 = (char *)((ulong)local_1d0 | 1);
        if ((local_1d0[0] & 1) != 0) {
          pcVar13 = local_1c0;
        }
        CEterPackManager::SetDefaultOverlayRoot(pcVar13);
        pcVar13 = (char *)((ulong)local_1d0 | 1);
        if ((local_1d0[0] & 1) != 0) {
          pcVar13 = local_1c0;
        }
        iVar9 = stat(pcVar13,(stat *)local_1a0);
        pcVar4 = "var";
        if (iVar9 != 0) {
          pcVar4 = "yok - kapali";
        }
        __android_log_print(4,"sancak2","kaplama koku: %s (%s)",pcVar13,pcVar4);
        if ((local_1d0[0] & 1) != 0) {
          operator_delete(local_1c0);
        }
        setenv("M2_UI_SCALE","1.6",0);
        setenv("M2_FONT_SS","2.67",0);
        FUN_006c2d84(local_1d0,&local_1b8,"/m2_ui_debug");
        pcVar13 = (char *)((ulong)local_1d0 | 1);
        if ((local_1d0[0] & 1) != 0) {
          pcVar13 = local_1c0;
        }
        iVar9 = stat(pcVar13,(stat *)local_1a0);
        if ((local_1d0[0] & 1) != 0) {
          operator_delete(local_1c0);
        }
        if (iVar9 == 0) {
          setenv("M2_UI_DEBUG","1",0);
        }
        uVar11 = CAndroidPlatform::WaitForFirstWindow((CAndroidPlatform *)(local_1a0 + 0x80));
        if ((uVar11 & 1) == 0) {
          __android_log_print(4,"sancak2","pencere gelmeden etkinlik yok edildi");
        }
        else if (iVar8 == 0) {
          __android_log_print(4,"sancak2","TANI KIPI: m2_tani_pyboot - yalniz F2-E Python dilimi");
          OpenLogFile(true);
          if ((local_1b8 & 1) != 0) {
            pcVar14 = local_1a8;
          }
          FUN_006c2e68(local_1a0 + 0x80,pcVar14);
        }
        else {
          FUN_006c3010(local_1a0 + 0x80);
        }
        uVar11 = CAndroidPlatform::IsDestroyRequested((CAndroidPlatform *)(local_1a0 + 0x80));
        if ((uVar11 & 1) == 0) {
          ANativeActivity_finish(*(undefined8 *)(param_1 + 0x18));
        }
        while (uVar11 = CAndroidPlatform::IsDestroyRequested((CAndroidPlatform *)(local_1a0 + 0x80))
              , (uVar11 & 1) == 0) {
          CAndroidPlatform::PumpPlatformEvents((CAndroidPlatform *)(local_1a0 + 0x80));
          usleep(10000);
        }
        M2_Android_WebView_Detach();
        M2Shell_DetachJava();
        __android_log_print(4,"sancak2","android_main bitti");
        fflush((FILE *)0x0);
        if (*(long *)(lVar5 + 0x28) == local_68) {
                    /* WARNING: Subroutine does not return */
          _exit(0);
        }
      }
      else if (*(long *)(lVar5 + 0x28) == local_68) {
                    /* WARNING: Subroutine does not return */
        FUN_006c1ae4(local_1a0);
      }
    }
    else if (*(long *)(lVar5 + 0x28) == local_68) {
                    /* WARNING: Subroutine does not return */
      FUN_006c1ae4(local_1a0);
    }
  }
  else if (*(long *)(lVar5 + 0x28) == local_68) {
                    /* WARNING: Subroutine does not return */
    FUN_006c1ae4(&local_1b8);
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * android_app_read_cmd @ 006d0aa8
 * ============================================================ */

void android_app_read_cmd(long param_1)

{
  long lVar1;
  ssize_t sVar2;
  void *__ptr;
  char local_3c [4];
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  sVar2 = read(*(int *)(param_1 + 0xc0),local_3c,1);
  if (sVar2 == 1) {
    if (local_3c[0] == '\f') {
      pthread_mutex_lock((pthread_mutex_t *)(param_1 + 0x68));
      __ptr = *(void **)(param_1 + 0x28);
      if (__ptr != (void *)0x0) {
        free(__ptr);
        *(undefined8 *)(param_1 + 0x28) = 0;
        *(undefined8 *)(param_1 + 0x30) = 0;
      }
      pthread_mutex_unlock((pthread_mutex_t *)(param_1 + 0x68));
      local_3c[0] = '\f';
    }
  }
  else {
    __android_log_print(6,"threaded_app","No data on command pipe!");
    local_3c[0] = -1;
  }
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(local_3c[0]);
}

/* ============================================================
 * android_app_pre_exec_cmd @ 006d0b60
 * ============================================================ */

ulong android_app_pre_exec_cmd(ulong param_1,char param_2)

{
  long lVar1;
  uint uVar2;
  long lVar3;
  pthread_mutex_t *__mutex;
  undefined1 auStack_40 [4];
  undefined1 auStack_3c [4];
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  switch((int)param_2) {
  case 0:
    pthread_mutex_lock((pthread_mutex_t *)(param_1 + 0x68));
    if (*(long *)(param_1 + 0x40) != 0) {
      AInputQueue_detachLooper();
    }
    lVar3 = *(long *)(param_1 + 0x110);
    *(long *)(param_1 + 0x40) = lVar3;
    if (lVar3 != 0) {
      AInputQueue_attachLooper(lVar3,*(undefined8 *)(param_1 + 0x38),2,0,param_1 + 0xe8);
    }
    break;
  case 1:
    pthread_mutex_lock((pthread_mutex_t *)(param_1 + 0x68));
    *(undefined8 *)(param_1 + 0x48) = *(undefined8 *)(param_1 + 0x118);
    break;
  case 2:
    if (*(long *)(lVar1 + 0x28) == local_38) {
      uVar2 = pthread_cond_broadcast((pthread_cond_t *)(param_1 + 0x90));
      return (ulong)uVar2;
    }
    goto LAB_006d0cc0;
  default:
    goto switchD_006d0ba4_caseD_3;
  case 8:
    AConfiguration_fromAssetManager
              (*(undefined8 *)(param_1 + 0x20),*(undefined8 *)(*(long *)(param_1 + 0x18) + 0x40));
    AConfiguration_getLanguage(*(undefined8 *)(param_1 + 0x20),auStack_3c);
    param_1 = AConfiguration_getCountry(*(undefined8 *)(param_1 + 0x20),auStack_40);
    goto switchD_006d0ba4_caseD_3;
  case 10:
  case 0xb:
  case 0xd:
  case 0xe:
    pthread_mutex_lock((pthread_mutex_t *)(param_1 + 0x68));
    *(int *)(param_1 + 0x60) = (int)param_2;
    break;
  case 0xf:
    *(undefined4 *)(param_1 + 100) = 1;
switchD_006d0ba4_caseD_3:
    if (*(long *)(lVar1 + 0x28) == local_38) {
      return param_1;
    }
    goto LAB_006d0cc0;
  }
  __mutex = (pthread_mutex_t *)(param_1 + 0x68);
  uVar2 = pthread_cond_broadcast((pthread_cond_t *)(param_1 + 0x90));
  param_1 = (ulong)uVar2;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    uVar2 = pthread_mutex_unlock(__mutex);
    return (ulong)uVar2;
  }
LAB_006d0cc0:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(param_1);
}

/* ============================================================
 * android_app_post_exec_cmd @ 006d0cc4
 * ============================================================ */

ulong android_app_post_exec_cmd(ulong param_1,char param_2)

{
  uint uVar1;
  void *__ptr;
  
  if (param_2 == '\f') {
    pthread_mutex_lock((pthread_mutex_t *)(param_1 + 0x68));
    *(undefined4 *)(param_1 + 0x104) = 1;
    pthread_cond_broadcast((pthread_cond_t *)(param_1 + 0x90));
  }
  else if (param_2 == '\v') {
    pthread_mutex_lock((pthread_mutex_t *)(param_1 + 0x68));
    __ptr = *(void **)(param_1 + 0x28);
    if (__ptr != (void *)0x0) {
      free(__ptr);
      *(undefined8 *)(param_1 + 0x28) = 0;
      *(undefined8 *)(param_1 + 0x30) = 0;
    }
  }
  else {
    if (param_2 != '\x02') {
      return param_1;
    }
    pthread_mutex_lock((pthread_mutex_t *)(param_1 + 0x68));
    *(undefined8 *)(param_1 + 0x48) = 0;
    pthread_cond_broadcast((pthread_cond_t *)(param_1 + 0x90));
  }
  uVar1 = pthread_mutex_unlock((pthread_mutex_t *)(param_1 + 0x68));
  return (ulong)uVar1;
}

/* ============================================================
 * CAndroidApplicationWindow::WindowProcedure @ 006d574c
 * ============================================================ */

/* CAndroidApplicationWindow::WindowProcedure(HWND__*, unsigned int, unsigned long, long) */

void __thiscall
CAndroidApplicationWindow::WindowProcedure
          (CAndroidApplicationWindow *this,HWND__ *param_1,uint param_2,ulong param_3,long param_4)

{
  if (*(CPythonApplicationAndroid **)(this + 0x28) != (CPythonApplicationAndroid *)0x0) {
    CPythonApplicationAndroid::WindowProcedure
              (*(CPythonApplicationAndroid **)(this + 0x28),param_1,param_2,param_3,param_4);
    return;
  }
  CMSApplication::WindowProcedure((CMSApplication *)this,param_1,param_2,param_3,param_4);
  return;
}

/* ============================================================
 * CPythonApplicationAndroid::WindowProcedure @ 006d5760
 * ============================================================ */

/* CPythonApplicationAndroid::WindowProcedure(HWND__*, unsigned int, unsigned long, long) */

void __thiscall
CPythonApplicationAndroid::WindowProcedure
          (CPythonApplicationAndroid *this,HWND__ *param_1,uint param_2,ulong param_3,long param_4)

{
  uint uVar1;
  undefined4 uVar2;
  uint uVar3;
  short sVar4;
  long lVar5;
  undefined *puVar6;
  int iVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  int iVar10;
  ulong uVar11;
  undefined8 uVar12;
  HWND__ *pHVar13;
  CPythonApplicationAndroid *pCVar14;
  CPythonApplicationAndroid CVar15;
  long lVar16;
  uint uVar17;
  int local_68;
  int local_60;
  int iStack_5c;
  
  puVar6 = PTR_ms_singleton_00d79a90;
  lVar5 = tpidr_el0;
  lVar16 = *(long *)(lVar5 + 0x28);
  uVar17 = (uint)param_4;
  sVar4 = (short)param_4;
  if ((int)param_2 < 0x105) {
    pCVar14 = (CPythonApplicationAndroid *)0x0;
    switch(param_2) {
    case 2:
      goto switchD_006d585c_caseD_2;
    case 3:
    case 4:
    case 6:
    case 7:
    case 8:
    case 9:
    case 10:
    case 0xb:
    case 0xc:
    case 0xd:
    case 0xe:
    case 0xf:
    case 0x11:
    case 0x12:
    case 0x13:
    case 0x14:
    case 0x15:
    case 0x16:
    case 0x17:
    case 0x18:
    case 0x19:
    case 0x1a:
    case 0x1b:
    case 0x1d:
    case 0x1e:
    case 0x1f:
      break;
    case 5:
      if (param_3 == 2) {
LAB_006d5874:
        CMSWindow::GetClientRect(*(_RECT **)(this + 0x398));
        CGraphicDevice::ResizeBackBuffer
                  (*(CGraphicDevice **)(this + 0x380),local_60 - local_68,iStack_5c - local_68);
        if (param_3 == 1) goto LAB_006d58a0;
LAB_006d5b18:
        CVar15 = (CPythonApplicationAndroid)0x0;
      }
      else {
        if (param_3 != 1) {
          if (param_3 == 0) goto LAB_006d5874;
          goto LAB_006d5b18;
        }
LAB_006d58a0:
        CVar15 = (CPythonApplicationAndroid)0x1;
      }
      this[0x189] = CVar15;
LAB_006d5b28:
      CPythonApplication::OnSizeChange((int)this,(int)sVar4);
      break;
    case 0x10:
      CPythonApplication::RunPressExitKey();
      pCVar14 = (CPythonApplicationAndroid *)0x0;
      goto switchD_006d585c_caseD_2;
    case 0x1c:
      this[0x18a] = (CPythonApplicationAndroid)(param_3 - 1 < 2);
      if (param_3 - 1 < 2) {
        CSoundManager::RestoreVolume(*(CSoundManager **)puVar6);
        if (*(int *)(this + 0x394) != 0) {
          uVar9 = *(undefined4 *)(this + 0x388);
          uVar2 = *(undefined4 *)(this + 0x38c);
          uVar8 = CPythonSystem::GetBPP(*(CPythonSystem **)PTR_ms_singleton_00d799e0);
          FUN_006d5ca4(uVar9,uVar2,uVar8);
        }
      }
      else {
        CSoundManager::SaveVolume(*(CSoundManager **)puVar6);
        if (*(int *)(this + 0x394) != 0) {
          FUN_006d5d1c(param_1,*(undefined4 *)(this + 0x388),*(undefined4 *)(this + 0x38c));
        }
      }
      break;
    case 0x20:
      uVar11 = CMSWindow::IsActive(*(CMSWindow **)(this + 0x398));
      if ((uVar11 & 1) == 0) break;
      if ((*(int *)(this + 0x120) == 0) || (*(int *)(this + 0x128) != 0)) {
        uVar12 = 0;
      }
      else {
        uVar12 = *(undefined8 *)(this + 0x118);
      }
      SetCursor(uVar12);
      pCVar14 = (CPythonApplicationAndroid *)0x0;
      goto switchD_006d585c_caseD_2;
    default:
      if (param_2 == 0x100) {
        CPythonApplication::OnIMEKeyDown((CPythonApplication *)this,(uint)param_3 & 0xffff);
      }
      else if (param_2 == 0x102) {
        if (*(long *)(lVar5 + 0x28) == lVar16) {
          CIME::WMChar((CIME *)(*(long *)PTR_ms_singleton_00d79ac8 + 8),param_1,0x102,param_3,
                       param_4);
          return;
        }
        goto LAB_006d5ba4;
      }
    }
    goto switchD_006d57c4_caseD_203;
  }
  if (0x31 < param_2 - 0x201) {
    if (param_2 == 0x105) {
      if ((param_3 & 0xffff) == 0x12) goto LAB_006d5ae4;
    }
    else if (param_2 == 0x281) {
      param_4 = param_4 & 0x7ffffff0;
    }
    goto switchD_006d57c4_caseD_203;
  }
  iVar10 = (int)uVar17 >> 0x10;
  switch(param_2) {
  case 0x201:
    CPythonApplication::SafeSetCapture((CPythonApplication *)this);
    iVar7 = ELTimer_GetMSec();
    if ((uint)(iVar7 - *(int *)(this + 0x138)) < 300) {
      uVar3 = (uVar17 & 0xffff) - DAT_00e07748;
      uVar1 = -uVar3;
      if (-1 < (int)uVar3) {
        uVar1 = uVar3;
      }
      if (4 < uVar1) goto LAB_006d5aec;
      uVar3 = ((uint)((ulong)param_4 >> 0x10) & 0xffff) - DAT_00e0774c;
      uVar1 = -uVar3;
      if (-1 < (int)uVar3) {
        uVar1 = uVar3;
      }
      if (4 < uVar1) goto LAB_006d5aec;
      *(undefined4 *)(this + 0x138) = 0;
      CPythonApplication::OnMouseLeftButtonDoubleClick
                ((CPythonApplication *)this,(int)sVar4,(int)(short)((ulong)param_4 >> 0x10));
    }
    else {
LAB_006d5aec:
      uVar9 = ELTimer_GetMSec();
      *(undefined4 *)(this + 0x138) = uVar9;
      CPythonApplication::OnMouseLeftButtonDown((CPythonApplication *)this,(int)sVar4,iVar10);
    }
    DAT_00e0774c = uVar17 >> 0x10;
    pCVar14 = (CPythonApplicationAndroid *)0x0;
    DAT_00e07748 = uVar17 & 0xffff;
    break;
  case 0x202:
    uVar9 = ELTimer_GetMSec();
    *(undefined4 *)(this + 0x13c) = uVar9;
    pHVar13 = (HWND__ *)GetCapture();
    if (pHVar13 == param_1) {
      CPythonApplication::SafeReleaseCapture();
      CPythonApplication::OnMouseLeftButtonUp((CPythonApplication *)this,(int)sVar4,iVar10);
      pCVar14 = (CPythonApplicationAndroid *)0x0;
    }
    else {
LAB_006d5ae4:
      pCVar14 = (CPythonApplicationAndroid *)0x0;
    }
    break;
  default:
    goto switchD_006d57c4_caseD_203;
  case 0x204:
    CPythonApplication::SafeSetCapture((CPythonApplication *)this);
    CPythonApplication::OnMouseRightButtonDown((CPythonApplication *)this,(int)sVar4,iVar10);
    pCVar14 = (CPythonApplicationAndroid *)0x0;
    break;
  case 0x205:
    pHVar13 = (HWND__ *)GetCapture();
    if (pHVar13 != param_1) goto LAB_006d5ae4;
    CPythonApplication::SafeReleaseCapture();
    CPythonApplication::OnMouseRightButtonUp((int)this,(int)sVar4);
    pCVar14 = (CPythonApplicationAndroid *)0x0;
    break;
  case 0x207:
    CPythonApplication::SafeSetCapture((CPythonApplication *)this);
    UI::CWindowManager::RunMouseMiddleButtonDown
              (*(CWindowManager **)PTR_ms_singleton_00d79960,(long)sVar4,(param_4 << 0x20) >> 0x30);
    goto switchD_006d57c4_caseD_203;
  case 0x208:
    pHVar13 = (HWND__ *)GetCapture();
    if (pHVar13 == param_1) {
      CPythonApplication::SafeReleaseCapture();
      UI::CWindowManager::RunMouseMiddleButtonUp
                (*(CWindowManager **)PTR_ms_singleton_00d79960,(long)sVar4,(param_4 << 0x20) >> 0x30
                );
    }
    goto switchD_006d57c4_caseD_203;
  case 0x20a:
    iVar10 = WebBrowser_IsVisible();
    if (iVar10 == 0) {
      CPythonApplication::OnMouseWheel((CPythonApplication *)this,(int)(uint)param_3 >> 0x10);
    }
switchD_006d57c4_caseD_203:
    pCVar14 = (CPythonApplicationAndroid *)
              CMSApplication::WindowProcedure
                        (*(CMSApplication **)(this + 0x398),param_1,param_2,param_3,param_4);
    break;
  case 0x232:
    CMSWindow::GetClientRect(*(_RECT **)(this + 0x398));
    CGraphicDevice::ResizeBackBuffer
              (*(CGraphicDevice **)(this + 0x380),local_60 - local_68,iStack_5c - local_68);
    goto LAB_006d5b28;
  }
switchD_006d585c_caseD_2:
  this = pCVar14;
  if (*(long *)(lVar5 + 0x28) == lVar16) {
    return;
  }
LAB_006d5ba4:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(this);
}

/* ============================================================
 * CPythonApplicationAndroid::CPythonApplicationAndroid @ 006d5ba8
 * ============================================================ */

/* CPythonApplicationAndroid::CPythonApplicationAndroid(app::IApplicationPlatform&,
   CAndroidApplicationWindow&, CScreen&, CGraphicDevice&) */

void __thiscall
CPythonApplicationAndroid::CPythonApplicationAndroid
          (CPythonApplicationAndroid *this,IApplicationPlatform *param_1,
          CAndroidApplicationWindow *param_2,CScreen *param_3,CGraphicDevice *param_4)

{
  undefined *puVar1;
  
  CPythonApplicationCore::CPythonApplicationCore
            ((CPythonApplicationCore *)this,param_1,param_3,param_4);
  puVar1 = PTR_vtable_00d79b08;
  *(CAndroidApplicationWindow **)(this + 0x398) = param_2;
  *(undefined **)this = puVar1 + 0x10;
  *(undefined **)(this + 8) = puVar1 + 0xd8;
  *(undefined **)(this + 0x10) = puVar1 + 0x108;
  *(CPythonApplicationAndroid **)(param_2 + 0x28) = this;
  return;
}

/* ============================================================
 * CPythonApplicationAndroid::~CPythonApplicationAndroid @ 006d5bf8
 * ============================================================ */

/* CPythonApplicationAndroid::~CPythonApplicationAndroid() */

void __thiscall
CPythonApplicationAndroid::~CPythonApplicationAndroid(CPythonApplicationAndroid *this)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  
  puVar1 = PTR_vtable_00d79b08 + 0x10;
  puVar2 = PTR_vtable_00d79b08 + 0xd8;
  puVar3 = PTR_vtable_00d79b08 + 0x108;
  *(undefined8 *)(*(long *)(this + 0x398) + 0x28) = 0;
  *(undefined **)this = puVar1;
  *(undefined **)(this + 8) = puVar2;
  *(undefined **)(this + 0x10) = puVar3;
  CPythonApplicationCore::~CPythonApplicationCore((CPythonApplicationCore *)this);
  return;
}

/* ============================================================
 * CPythonApplicationAndroid::~CPythonApplicationAndroid @ 006d5c20
 * ============================================================ */

/* non-virtual thunk to CPythonApplicationAndroid::~CPythonApplicationAndroid() */

void __thiscall
CPythonApplicationAndroid::~CPythonApplicationAndroid(CPythonApplicationAndroid *this)

{
  ~CPythonApplicationAndroid(this + -8);
  return;
}

/* ============================================================
 * CPythonApplicationAndroid::~CPythonApplicationAndroid @ 006d5c28
 * ============================================================ */

/* non-virtual thunk to CPythonApplicationAndroid::~CPythonApplicationAndroid() */

void __thiscall
CPythonApplicationAndroid::~CPythonApplicationAndroid(CPythonApplicationAndroid *this)

{
  ~CPythonApplicationAndroid(this + -0x10);
  return;
}

/* ============================================================
 * CPythonApplicationAndroid::~CPythonApplicationAndroid @ 006d5c30
 * ============================================================ */

/* CPythonApplicationAndroid::~CPythonApplicationAndroid() */

void __thiscall
CPythonApplicationAndroid::~CPythonApplicationAndroid(CPythonApplicationAndroid *this)

{
  ~CPythonApplicationAndroid(this);
  operator_delete(this);
  return;
}

/* ============================================================
 * CPythonApplicationAndroid::~CPythonApplicationAndroid @ 006d5c54
 * ============================================================ */

/* non-virtual thunk to CPythonApplicationAndroid::~CPythonApplicationAndroid() */

void __thiscall
CPythonApplicationAndroid::~CPythonApplicationAndroid(CPythonApplicationAndroid *this)

{
  ~CPythonApplicationAndroid(this + -8);
  operator_delete(this + -8);
  return;
}

/* ============================================================
 * CPythonApplicationAndroid::~CPythonApplicationAndroid @ 006d5c7c
 * ============================================================ */

/* non-virtual thunk to CPythonApplicationAndroid::~CPythonApplicationAndroid() */

void __thiscall
CPythonApplicationAndroid::~CPythonApplicationAndroid(CPythonApplicationAndroid *this)

{
  ~CPythonApplicationAndroid(this + -0x10);
  operator_delete(this + -0x10);
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::CAndroidApplicationPlatformBase @ 006d5d7c
 * ============================================================ */

/* CAndroidApplicationPlatformBase::CAndroidApplicationPlatformBase() */

void __thiscall
CAndroidApplicationPlatformBase::CAndroidApplicationPlatformBase
          (CAndroidApplicationPlatformBase *this)

{
  *(undefined **)this = PTR_vtable_00d79b10 + 0x10;
  CMSApplication::CMSApplication((CMSApplication *)(this + 8));
  *(undefined **)(this + 8) = PTR_vtable_00d79b18 + 0x10;
  *(undefined8 *)(this + 0x30) = 0;
  *(undefined8 *)(this + 0x38) = 0;
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::~CAndroidApplicationPlatformBase @ 006d5dc4
 * ============================================================ */

/* CAndroidApplicationPlatformBase::~CAndroidApplicationPlatformBase() */

void __thiscall
CAndroidApplicationPlatformBase::~CAndroidApplicationPlatformBase
          (CAndroidApplicationPlatformBase *this)

{
  *(undefined **)this = PTR_vtable_00d79b10 + 0x10;
  CMSApplication::~CMSApplication((CMSApplication *)(this + 8));
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::~CAndroidApplicationPlatformBase @ 006d5dd8
 * ============================================================ */

/* CAndroidApplicationPlatformBase::~CAndroidApplicationPlatformBase() */

void __thiscall
CAndroidApplicationPlatformBase::~CAndroidApplicationPlatformBase
          (CAndroidApplicationPlatformBase *this)

{
  code *pcVar1;
  
                    /* WARNING: Does not return */
  pcVar1 = (code *)SoftwareBreakpoint(1,0x6d5ddc);
  (*pcVar1)();
}

/* ============================================================
 * CAndroidApplicationPlatformBase::CreateMainWindow @ 006d5ddc
 * ============================================================ */

/* CAndroidApplicationPlatformBase::CreateMainWindow(int, int, bool) */

uint __thiscall
CAndroidApplicationPlatformBase::CreateMainWindow
          (CAndroidApplicationPlatformBase *this,int param_1,int param_2,bool param_3)

{
  uint uVar1;
  
  uVar1 = 0xca0000;
  if (!param_3) {
    uVar1 = 0x80000000;
  }
  uVar1 = CMSWindow::Create((CMSWindow *)(this + 8),"",4,0,uVar1,(HICON__ *)0x0,0x7f00);
  if ((uVar1 & 1) != 0) {
    CMSWindow::AdjustSize((CMSWindow *)(this + 8),param_1,param_2);
  }
  return uVar1 & 1;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::GetWindowHandle @ 006d5e54
 * ============================================================ */

/* CAndroidApplicationPlatformBase::GetWindowHandle() */

void __thiscall
CAndroidApplicationPlatformBase::GetWindowHandle(CAndroidApplicationPlatformBase *this)

{
  CMSWindow::GetWindowHandle((CMSWindow *)(this + 8));
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::IsAnotherApplicationWindowOpen @ 006d5e5c
 * ============================================================ */

/* CAndroidApplicationPlatformBase::IsAnotherApplicationWindowOpen(char const*) */

bool CAndroidApplicationPlatformBase::IsAnotherApplicationWindowOpen(char *param_1)

{
  long lVar1;
  
  lVar1 = FindWindow(0);
  return lVar1 != 0;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::SetWindowTitle @ 006d5e7c
 * ============================================================ */

/* CAndroidApplicationPlatformBase::SetWindowTitle(char const*) */

void CAndroidApplicationPlatformBase::SetWindowTitle(char *param_1)

{
  CMSWindow::SetText(param_1 + 8);
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::AdjustWindowSize @ 006d5e84
 * ============================================================ */

/* CAndroidApplicationPlatformBase::AdjustWindowSize(int, int) */

void __thiscall
CAndroidApplicationPlatformBase::AdjustWindowSize
          (CAndroidApplicationPlatformBase *this,int param_1,int param_2)

{
  CMSWindow::AdjustSize((CMSWindow *)(this + 8),param_1,param_2);
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::GetWindowClientRect @ 006d5e8c
 * ============================================================ */

/* CAndroidApplicationPlatformBase::GetWindowClientRect(_RECT*) */

void CAndroidApplicationPlatformBase::GetWindowClientRect(_RECT *param_1)

{
  CMSWindow::GetClientRect(param_1 + 8);
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::GetScreenWidth @ 006d5e94
 * ============================================================ */

/* CAndroidApplicationPlatformBase::GetScreenWidth() */

void CAndroidApplicationPlatformBase::GetScreenWidth(void)

{
  CMSWindow::GetScreenWidth();
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::GetScreenHeight @ 006d5e9c
 * ============================================================ */

/* CAndroidApplicationPlatformBase::GetScreenHeight() */

void CAndroidApplicationPlatformBase::GetScreenHeight(void)

{
  CMSWindow::GetScreenHeight();
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::SetWindowPosition @ 006d5ea4
 * ============================================================ */

/* CAndroidApplicationPlatformBase::SetWindowPosition(int, int) */

void __thiscall
CAndroidApplicationPlatformBase::SetWindowPosition
          (CAndroidApplicationPlatformBase *this,int param_1,int param_2)

{
  CMSWindow::SetPosition((CMSWindow *)(this + 8),param_1,param_2);
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::SetWindowVisibleMode @ 006d5eac
 * ============================================================ */

/* CAndroidApplicationPlatformBase::SetWindowVisibleMode(bool) */

void __thiscall
CAndroidApplicationPlatformBase::SetWindowVisibleMode
          (CAndroidApplicationPlatformBase *this,bool param_1)

{
  CMSWindow::SetVisibleMode((CMSWindow *)(this + 8),param_1);
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::IsWindowActive @ 006d5eb4
 * ============================================================ */

/* CAndroidApplicationPlatformBase::IsWindowActive() */

void __thiscall
CAndroidApplicationPlatformBase::IsWindowActive(CAndroidApplicationPlatformBase *this)

{
  CMSWindow::IsActive((CMSWindow *)(this + 8));
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::SetFullScreenWindow @ 006d5ebc
 * ============================================================ */

/* CAndroidApplicationPlatformBase::SetFullScreenWindow(unsigned int, unsigned int, unsigned int) */

void __thiscall
CAndroidApplicationPlatformBase::SetFullScreenWindow
          (CAndroidApplicationPlatformBase *this,uint param_1,uint param_2,uint param_3)

{
  long lVar1;
  int iVar2;
  undefined1 auStack_d8 [36];
  undefined2 local_b4;
  undefined4 local_b0;
  uint local_70;
  uint local_6c;
  uint uStack_68;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  CMSWindow::GetWindowHandle((CMSWindow *)(this + 8));
  local_b4 = 0x9c;
  local_b0 = 0x1c0000;
  local_70 = param_3;
  local_6c = param_1;
  uStack_68 = param_2;
  iVar2 = ChangeDisplaySettings(auStack_d8,4);
  if (iVar2 == 1) {
    ChangeDisplaySettings(0,0);
  }
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * CAndroidApplicationPlatformBase::ResizeFullScreenWindow @ 006d5f50
 * ============================================================ */

/* CAndroidApplicationPlatformBase::ResizeFullScreenWindow(int, int) */

void __thiscall
CAndroidApplicationPlatformBase::ResizeFullScreenWindow
          (CAndroidApplicationPlatformBase *this,int param_1,int param_2)

{
  undefined8 uVar1;
  
  uVar1 = CMSWindow::GetWindowHandle((CMSWindow *)(this + 8));
  SetWindowPos(uVar1,0,0,0,param_1,param_2,0x40);
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::CreateApplicationCursors @ 006d5f90
 * ============================================================ */

/* CAndroidApplicationPlatformBase::CreateApplicationCursors() */

void __thiscall
CAndroidApplicationPlatformBase::CreateApplicationCursors(CAndroidApplicationPlatformBase *this)

{
  if (*(CPythonApplication **)(this + 0x38) != (CPythonApplication *)0x0) {
    CPythonApplication::CreateCursors(*(CPythonApplication **)(this + 0x38));
    return;
  }
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::InitializeInput @ 006d5fa0
 * ============================================================ */

/* CAndroidApplicationPlatformBase::InitializeInput() */

undefined8 __thiscall
CAndroidApplicationPlatformBase::InitializeInput(CAndroidApplicationPlatformBase *this)

{
  undefined8 uVar1;
  
  if (*(long *)(this + 0x38) != 0) {
    uVar1 = CInputKeyboard::InitializeKeyboard((HWND__ *)(*(long *)(this + 0x38) + 8));
    return uVar1;
  }
  return 0;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::UpdateInput @ 006d5fbc
 * ============================================================ */

/* CAndroidApplicationPlatformBase::UpdateInput() */

void __thiscall CAndroidApplicationPlatformBase::UpdateInput(CAndroidApplicationPlatformBase *this)

{
  if (*(long *)(this + 0x38) != 0) {
    CInputKeyboard::UpdateKeyboard((CInputKeyboard *)(*(long *)(this + 0x38) + 8));
    return;
  }
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::GetMouseClientPosition @ 006d5fd0
 * ============================================================ */

/* CAndroidApplicationPlatformBase::GetMouseClientPosition(_POINT*) */

undefined8 __thiscall
CAndroidApplicationPlatformBase::GetMouseClientPosition
          (CAndroidApplicationPlatformBase *this,_POINT *param_1)

{
  CInputCore *this_00;
  undefined8 uVar1;
  
  this_00 = (CInputCore *)M2Android_InputCore();
  uVar1 = m2input::CInputCore::PollCursor(this_00);
  *(undefined8 *)param_1 = uVar1;
  uVar1 = CMSWindow::GetWindowHandle((CMSWindow *)(this + 8));
  ScreenToClient(uVar1,param_1);
  return 1;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::DisableStickyKeys @ 006d6014
 * ============================================================ */

/* CAndroidApplicationPlatformBase::DisableStickyKeys() */

void CAndroidApplicationPlatformBase::DisableStickyKeys(void)

{
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::RestoreStickyKeys @ 006d6018
 * ============================================================ */

/* CAndroidApplicationPlatformBase::RestoreStickyKeys() */

void CAndroidApplicationPlatformBase::RestoreStickyKeys(void)

{
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::HasPendingEvents @ 006d601c
 * ============================================================ */

/* CAndroidApplicationPlatformBase::HasPendingEvents() */

uint __thiscall
CAndroidApplicationPlatformBase::HasPendingEvents(CAndroidApplicationPlatformBase *this)

{
  long lVar1;
  uint uVar2;
  ulong uVar3;
  bool local_2c [4];
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  (**(code **)(*(long *)this + 0x150))();
  M2Android_Update();
  uVar3 = M2Android_ConsumeSoftKeyboardReset();
  if ((uVar3 & 1) != 0) {
    (**(code **)(*(long *)this + 0x160))(this);
  }
  local_2c[0] = false;
  uVar3 = M2Android_ConsumeSoftKeyboardRequest(local_2c);
  if ((uVar3 & 1) != 0) {
    (**(code **)(*(long *)this + 0x158))(this,local_2c[0]);
  }
  uVar2 = CMSApplication::IsMessage();
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return uVar2 & 1;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * CAndroidApplicationPlatformBase::ProcessEvents @ 006d60b8
 * ============================================================ */

/* CAndroidApplicationPlatformBase::ProcessEvents() */

void CAndroidApplicationPlatformBase::ProcessEvents(void)

{
  CMSApplication::MessageProcess();
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::CreateApplication @ 006d60c0
 * ============================================================ */

/* CAndroidApplicationPlatformBase::CreateApplication(CScreen&, CGraphicDevice&) */

CPythonApplicationAndroid * __thiscall
CAndroidApplicationPlatformBase::CreateApplication
          (CAndroidApplicationPlatformBase *this,CScreen *param_1,CGraphicDevice *param_2)

{
  CPythonApplicationAndroid *this_00;
  
  this_00 = operator_new(0x3a0);
  CPythonApplicationAndroid::CPythonApplicationAndroid
            (this_00,(IApplicationPlatform *)this,(CAndroidApplicationWindow *)(this + 8),param_1,
             param_2);
  *(CPythonApplicationAndroid **)(this + 0x38) = this_00;
  return this_00;
}

/* ============================================================
 * CAndroidApplicationWindow::~CAndroidApplicationWindow @ 006d6128
 * ============================================================ */

/* CAndroidApplicationWindow::~CAndroidApplicationWindow() */

void __thiscall
CAndroidApplicationWindow::~CAndroidApplicationWindow(CAndroidApplicationWindow *this)

{
  CMSApplication::~CMSApplication((CMSApplication *)this);
  operator_delete(this);
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::ShowSoftKeyboard @ 006d614c
 * ============================================================ */

/* CAndroidApplicationPlatformBase::ShowSoftKeyboard(bool) */

bool CAndroidApplicationPlatformBase::ShowSoftKeyboard(bool param_1)

{
  return param_1;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::ResetSoftKeyboard @ 006d6150
 * ============================================================ */

/* CAndroidApplicationPlatformBase::ResetSoftKeyboard() */

void CAndroidApplicationPlatformBase::ResetSoftKeyboard(void)

{
  return;
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidSurfaceListener @ 006f67a0
 * ============================================================ */

/* BgfxDeviceBackend::SetAndroidSurfaceListener(BgfxDeviceBackend::SAndroidSurfaceListener const*)
    */

void BgfxDeviceBackend::SetAndroidSurfaceListener(SAndroidSurfaceListener *param_1)

{
  long lVar1;
  int iVar2;
  long lVar3;
  undefined8 local_40;
  undefined8 uStack_38;
  undefined8 uStack_30;
  undefined8 uStack_28;
  undefined8 local_20;
  
  lVar1 = tpidr_el0;
  lVar3 = *(long *)(lVar1 + 0x28);
  if (param_1 == (SAndroidSurfaceListener *)0x0) {
    local_20 = 0;
    uStack_38 = 0;
    local_40 = 0;
    uStack_28 = 0;
    uStack_30 = 0;
  }
  else {
    uStack_38 = *(undefined8 *)(param_1 + 8);
    local_40 = *(undefined8 *)param_1;
    uStack_28 = *(undefined8 *)(param_1 + 0x18);
    uStack_30 = *(undefined8 *)(param_1 + 0x10);
    local_20 = *(undefined8 *)(param_1 + 0x20);
  }
  if ((DAT_00e0a340 & 1) == 0) {
    iVar2 = __cxa_guard_acquire(&DAT_00e0a340);
    if (iVar2 != 0) {
      __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e0a340);
    }
  }
  DAT_00e0a290 = uStack_38;
  DAT_00e0a288 = local_40;
  DAT_00e0a2a0 = uStack_28;
  DAT_00e0a298 = uStack_30;
  DAT_00e0a2a8 = local_20;
  if (*(long *)(lVar1 + 0x28) == lVar3) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidNativeWindow @ 006f686c
 * ============================================================ */

/* BgfxDeviceBackend::SetAndroidNativeWindow(void*, unsigned int, unsigned int) */

void BgfxDeviceBackend::SetAndroidNativeWindow(void *param_1,uint param_2,uint param_3)

{
  int iVar1;
  
  if ((DAT_00e0a340 & 1) == 0) {
    iVar1 = __cxa_guard_acquire(&DAT_00e0a340);
    if (iVar1 != 0) {
      __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e0a340);
    }
  }
  DAT_00e0a2b8 = param_1;
  if (((param_1 != (void *)0x0) && (param_2 != 0)) && (param_3 != 0)) {
    DAT_00e0a2c0 = param_2;
    DAT_00e0a2c4 = param_3;
  }
  if (DAT_00e0a2b0 != (BgfxDeviceBackend *)0x0) {
    ApplyAndroidSurface(DAT_00e0a2b0,param_1,param_2,param_3);
    return;
  }
  return;
}

/* ============================================================
 * BgfxDeviceBackend::ApplyAndroidSurface @ 006f6938
 * ============================================================ */

/* BgfxDeviceBackend::ApplyAndroidSurface(void*, unsigned int, unsigned int) */

void __thiscall
BgfxDeviceBackend::ApplyAndroidSurface
          (BgfxDeviceBackend *this,void *param_1,uint param_2,uint param_3)

{
  uint uVar1;
  uint uVar2;
  undefined4 uVar3;
  long lVar4;
  int iVar5;
  PlatformData aPStack_80 [8];
  void *local_78;
  long local_48;
  
  lVar4 = tpidr_el0;
  local_48 = *(long *)(lVar4 + 0x28);
  if (*this != (BgfxDeviceBackend)0x0) {
    if (param_1 == (void *)0x0) {
      this[0x1d] = (BgfxDeviceBackend)0x1;
    }
    else {
      bgfx::PlatformData::PlatformData(aPStack_80);
      local_78 = param_1;
      bgfx::setPlatformData(aPStack_80);
      if (*(short *)(this + 0x1e) == -1) {
        uVar1 = *(uint *)(this + 4);
        uVar2 = *(uint *)(this + 8);
        uVar3 = *(undefined4 *)(this + 0x18);
      }
      else {
        uVar3 = *(undefined4 *)(this + 0x18);
        uVar1 = *(uint *)(this + 0x10);
        if (param_2 != 0) {
          uVar1 = param_2;
        }
        uVar2 = *(uint *)(this + 0x14);
        if (param_3 != 0) {
          uVar2 = param_3;
        }
        *(uint *)(this + 0x10) = uVar1;
        *(uint *)(this + 0x14) = uVar2;
      }
      bgfx::reset(uVar1,uVar2,uVar3,0x69);
      if (*(short *)(this + 0x1e) != -1) {
        bgfx::setViewFrameBuffer(0);
        bgfx::setViewFrameBuffer(1,*(undefined2 *)(this + 0x1e));
        bgfx::setViewFrameBuffer(2,*(undefined2 *)(this + 0x1e));
      }
      this[0x1d] = (BgfxDeviceBackend)0x0;
      if (((DAT_00e0a340 & 1) == 0) && (iVar5 = __cxa_guard_acquire(&DAT_00e0a340), iVar5 != 0)) {
        __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
        __cxa_guard_release(&DAT_00e0a340);
      }
      M2_PlatformLog(4,"sancak2","EGL yuzeyi yeni pencereye tasindi: arka tampon %ux%u",
                     *(undefined4 *)(this + 0x10),*(undefined4 *)(this + 0x14));
      if (DAT_00e0a298 != (code *)0x0) {
        (*DAT_00e0a298)(DAT_00e0a288,*(undefined4 *)(this + 0x10),*(undefined4 *)(this + 0x14));
      }
    }
  }
  if (*(long *)(lVar4 + 0x28) == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidSafeInsets @ 006f6ab8
 * ============================================================ */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* BgfxDeviceBackend::SetAndroidSafeInsets(int, int, int, int) */

void BgfxDeviceBackend::SetAndroidSafeInsets(int param_1,int param_2,int param_3,int param_4)

{
  int iVar1;
  undefined1 auVar2 [16];
  
  if ((DAT_00e0a340 & 1) == 0) {
    iVar1 = __cxa_guard_acquire(&DAT_00e0a340);
    if (iVar1 != 0) {
      __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e0a340);
    }
  }
  auVar2._4_4_ = param_2;
  auVar2._0_4_ = param_1;
  auVar2._8_4_ = param_3;
  auVar2._12_4_ = param_4;
  auVar2 = NEON_smax(auVar2,ZEXT816(0),4);
  _DAT_00e0a2d0 = auVar2._8_8_;
  _DAT_00e0a2c8 = auVar2._0_8_;
  return;
}

/* ============================================================
 * BgfxDeviceBackend::GetAndroidPresentationRect @ 006f6b6c
 * ============================================================ */

/* BgfxDeviceBackend::GetAndroidPresentationRect(int*, int*, int*, int*) */

undefined8
BgfxDeviceBackend::GetAndroidPresentationRect(int *param_1,int *param_2,int *param_3,int *param_4)

{
  int iVar1;
  undefined8 uVar2;
  
  if ((DAT_00e0a340 & 1) == 0) {
    iVar1 = __cxa_guard_acquire(&DAT_00e0a340);
    if (iVar1 != 0) {
      __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e0a340);
    }
  }
  uVar2 = 0;
  if (DAT_00e0a2b0 != (BgfxDeviceBackend *)0x0) {
    if (*DAT_00e0a2b0 == (BgfxDeviceBackend)0x0) {
      uVar2 = 0;
    }
    else {
      ComputePresentationRect(DAT_00e0a2b0,param_1,param_2,param_3,param_4);
      if (((DAT_00e0a340 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_00e0a340), iVar1 != 0)) {
        __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
        __cxa_guard_release(&DAT_00e0a340);
      }
      uVar2 = 1;
      *param_2 = *param_2 - DAT_00e0a338;
    }
  }
  return uVar2;
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidPanY @ 006f6f24
 * ============================================================ */

/* BgfxDeviceBackend::SetAndroidPanY(int) */

void BgfxDeviceBackend::SetAndroidPanY(int param_1)

{
  int iVar1;
  
  if ((DAT_00e0a340 & 1) == 0) {
    iVar1 = __cxa_guard_acquire(&DAT_00e0a340);
    if (iVar1 != 0) {
      __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e0a340);
    }
  }
  DAT_00e0a338 = param_1;
  return;
}

/* ============================================================
 * BgfxDeviceBackend::GetAndroidPanY @ 006f6fa4
 * ============================================================ */

/* BgfxDeviceBackend::GetAndroidPanY() */

undefined4 BgfxDeviceBackend::GetAndroidPanY(void)

{
  int iVar1;
  
  if (((DAT_00e0a340 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_00e0a340), iVar1 != 0)) {
    __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e0a340);
  }
  return DAT_00e0a338;
}

/* ============================================================
 * BgfxDeviceBackend::GetAndroidUiSurfaceView @ 006f7008
 * ============================================================ */

/* BgfxDeviceBackend::GetAndroidUiSurfaceView(unsigned short*, int*, int*, float*, float*) */

void BgfxDeviceBackend::GetAndroidUiSurfaceView
               (ushort *param_1,int *param_2,int *param_3,float *param_4,float *param_5)

{
  long lVar1;
  BgfxDeviceBackend *pBVar2;
  bool bVar3;
  int iVar4;
  float fVar5;
  int local_68 [4];
  long local_58;
  
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  if (((DAT_00e0a340 & 1) == 0) && (iVar4 = __cxa_guard_acquire(&DAT_00e0a340), iVar4 != 0)) {
    __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e0a340);
  }
  pBVar2 = DAT_00e0a2b0;
  if ((((DAT_00e0a2b0 == (BgfxDeviceBackend *)0x0) || (*DAT_00e0a2b0 == (BgfxDeviceBackend)0x0)) ||
      (*(short *)(DAT_00e0a2b0 + 0x1e) == -1)) ||
     ((*(int *)(DAT_00e0a2b0 + 4) == 0 || (*(int *)(DAT_00e0a2b0 + 8) == 0)))) {
    bVar3 = false;
  }
  else {
    local_68[3] = 0;
    local_68[2] = 0;
    local_68[0] = 0;
    local_68[1] = 0;
    ComputePresentationRect(DAT_00e0a2b0,local_68 + 3,local_68 + 2,local_68 + 1,local_68);
    bVar3 = (0 < local_68[1] && local_68[0] != 0) && (local_68[1] < 1 || -1 < local_68[0]);
    if (0 < local_68[1] && 0 < local_68[0]) {
      *param_1 = 0xfa;
      *param_2 = local_68[3];
      *param_3 = local_68[2];
      fVar5 = (float)NEON_ucvtf(*(undefined4 *)(pBVar2 + 4));
      *param_4 = (float)local_68[1] / fVar5;
      fVar5 = (float)NEON_ucvtf(*(undefined4 *)(pBVar2 + 8));
      *param_5 = (float)local_68[0] / fVar5;
    }
  }
  if (*(long *)(lVar1 + 0x28) == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(bVar3);
}

/* ============================================================
 * BgfxDeviceBackend::CanRunWithoutAndroidSurface @ 006f7174
 * ============================================================ */

/* BgfxDeviceBackend::CanRunWithoutAndroidSurface() */

bool BgfxDeviceBackend::CanRunWithoutAndroidSurface(void)

{
  int iVar1;
  
  if (((DAT_00e0a340 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_00e0a340), iVar1 != 0)) {
    __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e0a340);
  }
  if ((DAT_00e0a2b0 != (char *)0x0) && (*DAT_00e0a2b0 != '\0')) {
    return *(short *)(DAT_00e0a2b0 + 0x1e) != -1;
  }
  return false;
}

/* ============================================================
 * BgfxDeviceBackend::GetAndroidBackbufferSize @ 006f71fc
 * ============================================================ */

/* BgfxDeviceBackend::GetAndroidBackbufferSize(unsigned int*, unsigned int*) */

undefined8 BgfxDeviceBackend::GetAndroidBackbufferSize(uint *param_1,uint *param_2)

{
  char *pcVar1;
  int iVar2;
  undefined8 uVar3;
  
  if ((DAT_00e0a340 & 1) == 0) {
    iVar2 = __cxa_guard_acquire(&DAT_00e0a340);
    if (iVar2 != 0) {
      __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e0a340);
    }
  }
  pcVar1 = DAT_00e0a2b0;
  if ((DAT_00e0a2b0 == (char *)0x0) || (*DAT_00e0a2b0 == '\0')) {
    uVar3 = 0;
  }
  else {
    *param_1 = *(uint *)(DAT_00e0a2b0 + 0x10);
    uVar3 = 1;
    *param_2 = *(uint *)(pcVar1 + 0x14);
  }
  return uVar3;
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidSplashOverlay @ 006f72a4
 * ============================================================ */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* BgfxDeviceBackend::SetAndroidSplashOverlay(int, int, int, int, unsigned char const*) */

void BgfxDeviceBackend::SetAndroidSplashOverlay
               (int param_1,int param_2,int param_3,int param_4,uchar *param_5)

{
  int iVar1;
  
  if ((DAT_00e0a340 & 1) == 0) {
    iVar1 = __cxa_guard_acquire(&DAT_00e0a340);
    if (iVar1 != 0) {
      __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e0a340);
    }
  }
  DAT_00e0a308 = 1;
  if (((0 < param_4) && (0 < param_3)) && (param_5 != (uchar *)0x0)) {
    _DAT_00e0a314 = CONCAT44(param_4,param_3);
    DAT_00e0a30c = param_1;
    DAT_00e0a310 = param_2;
    std::__ndk1::vector<unsigned_char,std::__ndk1::allocator<unsigned_char>>::
    assign<unsigned_char_const*,0>
              ((vector<unsigned_char,std::__ndk1::allocator<unsigned_char>> *)&DAT_00e0a320,param_5,
               param_5 + (ulong)(uint)param_3 * (ulong)(uint)param_4 * 4);
    return;
  }
  DAT_00e0a328 = DAT_00e0a320;
  _DAT_00e0a314 = 0;
  return;
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidSplashImage @ 006f760c
 * ============================================================ */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* BgfxDeviceBackend::SetAndroidSplashImage(int, int, int, int, unsigned char const*) */

void BgfxDeviceBackend::SetAndroidSplashImage
               (int param_1,int param_2,int param_3,int param_4,uchar *param_5)

{
  int iVar1;
  
  if ((DAT_00e0a340 & 1) == 0) {
    iVar1 = __cxa_guard_acquire(&DAT_00e0a340);
    if (iVar1 != 0) {
      __cxa_atexit(FUN_006f8ed4,&DAT_00e0a288,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e0a340);
    }
  }
  DAT_00e0a2d8 = 1;
  if (((0 < param_4) && (0 < param_3)) && (param_5 != (uchar *)0x0)) {
    _DAT_00e0a2e4 = CONCAT44(param_4,param_3);
    DAT_00e0a2dc = param_1;
    DAT_00e0a2e0 = param_2;
    std::__ndk1::vector<unsigned_char,std::__ndk1::allocator<unsigned_char>>::
    assign<unsigned_char_const*,0>
              ((vector<unsigned_char,std::__ndk1::allocator<unsigned_char>> *)&DAT_00e0a2f0,param_5,
               param_5 + (ulong)(uint)param_3 * (ulong)(uint)param_4 * 4);
    return;
  }
  DAT_00e0a2f8 = DAT_00e0a2f0;
  _DAT_00e0a2e4 = 0;
  return;
}

/* ============================================================
 * M2_Android_SetFilesDirectory @ 0071bed4
 * ============================================================ */

void M2_Android_SetFilesDirectory(char *param_1)

{
  char *pcVar1;
  
  if (param_1 != (char *)0x0) {
    pcVar1 = strncpy(&DAT_00e0c9c8,param_1,0x3ff);
    pcVar1[0x3ff] = '\0';
  }
  return;
}

/* ============================================================
 * M2_Android_SetShellFolderPath @ 007244a0
 * ============================================================ */

void M2_Android_SetShellFolderPath(int param_1,char *param_2)

{
  ulong *puVar1;
  long lVar2;
  undefined8 *puVar3;
  bool bVar4;
  int iVar5;
  size_t __n;
  undefined8 *puVar6;
  undefined8 *puVar7;
  ulong uVar8;
  void *pvVar9;
  undefined8 *puVar10;
  ulong local_68;
  ulong local_60;
  void *local_58;
  int local_4c;
  long local_48;
  
  lVar2 = tpidr_el0;
  local_48 = *(long *)(lVar2 + 0x28);
  local_4c = param_1;
  if (((DAT_00e11000 & 1) == 0) && (iVar5 = __cxa_guard_acquire(&DAT_00e11000), iVar5 != 0)) {
    __cxa_atexit(PTR__mutex_00d799a0,&DAT_00e10fd8,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e11000);
  }
  std::__ndk1::mutex::lock((mutex *)&DAT_00e10fd8);
  if ((param_2 == (char *)0x0) || (*param_2 == '\0')) {
    if (((DAT_00e11020 & 1) == 0) && (iVar5 = __cxa_guard_acquire(&DAT_00e11020), iVar5 != 0)) {
      DAT_00e11018 = 0;
      DAT_00e11010 = (undefined8 *)0x0;
      DAT_00e11008 = &DAT_00e11010;
      __cxa_atexit(FUN_00724c58,&DAT_00e11008,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e11020);
    }
    std::__ndk1::
    __tree<std::__ndk1::__value_type<int,std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>>,std::__ndk1::__map_value_compare<int,std::__ndk1::__value_type<int,std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>>,std::__ndk1::less<int>,true>,std::__ndk1::allocator<std::__ndk1::__value_type<int,std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>>>>
    ::__erase_unique<int>
              ((__tree<std::__ndk1::__value_type<int,std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>>,std::__ndk1::__map_value_compare<int,std::__ndk1::__value_type<int,std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>>,std::__ndk1::less<int>,true>,std::__ndk1::allocator<std::__ndk1::__value_type<int,std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>>>>
                *)&DAT_00e11008,&local_4c);
  }
  else {
    __n = strlen(param_2);
    if (0xffffffffffffffef < __n) {
      if (*(long *)(lVar2 + 0x28) == local_48) {
                    /* WARNING: Subroutine does not return */
        FUN_006c1ae4(&local_68);
      }
      goto LAB_00724840;
    }
    if (__n < 0x17) {
      pvVar9 = (void *)((ulong)&local_68 | 1);
      local_68 = CONCAT71(local_68._1_7_,(char)((int)__n << 1));
    }
    else {
      uVar8 = (__n | 0xf) + 1;
      pvVar9 = operator_new(uVar8);
      local_68 = uVar8 | 1;
      local_60 = __n;
      local_58 = pvVar9;
    }
    memcpy(pvVar9,param_2,__n);
    *(undefined1 *)((long)pvVar9 + __n) = 0;
    bVar4 = (local_68 & 1) == 0;
    uVar8 = local_68 >> 1 & 0x7f;
    if (!bVar4) {
      uVar8 = local_60;
    }
    if (1 < uVar8) {
      do {
        puVar1 = &local_68;
        if (!bVar4) {
          puVar1 = (ulong *)((long)local_58 - 1);
        }
        if (*(char *)((long)puVar1 + uVar8) != '/') break;
        uVar8 = uVar8 - 1;
        if (bVar4) {
          local_68 = CONCAT71(local_68._1_7_,(char)((int)uVar8 << 1));
          pvVar9 = (void *)((ulong)&local_68 | 1);
        }
        else {
          local_60 = uVar8;
          pvVar9 = local_58;
        }
        *(undefined1 *)((long)pvVar9 + uVar8) = 0;
        bVar4 = (local_68 & 1) == 0;
        uVar8 = local_68 >> 1 & 0x7f;
        if (!bVar4) {
          uVar8 = local_60;
        }
      } while (1 < uVar8);
    }
    if (((DAT_00e11020 & 1) == 0) && (iVar5 = __cxa_guard_acquire(&DAT_00e11020), iVar5 != 0)) {
      DAT_00e11018 = 0;
      DAT_00e11010 = (undefined8 *)0x0;
      DAT_00e11008 = &DAT_00e11010;
      __cxa_atexit(FUN_00724c58,&DAT_00e11008,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e11020);
    }
    iVar5 = local_4c;
    puVar7 = &DAT_00e11010;
    puVar3 = DAT_00e11010;
    puVar10 = puVar7;
    if (DAT_00e11010 != (undefined8 *)0x0) {
      do {
        while (puVar6 = puVar3, puVar7 = puVar6, local_4c < *(int *)(puVar6 + 4)) {
          puVar3 = (undefined8 *)*puVar6;
          puVar10 = puVar6;
          if ((undefined8 *)*puVar6 == (undefined8 *)0x0) goto LAB_00724664;
        }
        if (local_4c <= *(int *)(puVar6 + 4)) goto LAB_007246c0;
        puVar3 = (undefined8 *)puVar6[1];
      } while ((undefined8 *)puVar6[1] != (undefined8 *)0x0);
      puVar10 = puVar6 + 1;
    }
LAB_00724664:
    puVar6 = operator_new(0x40);
    *(int *)(puVar6 + 4) = iVar5;
    puVar6[6] = 0;
    puVar6[7] = 0;
    puVar6[5] = 0;
    *puVar6 = 0;
    puVar6[1] = 0;
    puVar6[2] = puVar7;
    *puVar10 = puVar6;
    puVar7 = puVar6;
    if ((undefined8 *)*DAT_00e11008 != (undefined8 *)0x0) {
      puVar7 = (undefined8 *)*puVar10;
      DAT_00e11008 = (undefined8 *)*DAT_00e11008;
    }
    FUN_006e42c8(DAT_00e11010,puVar7);
    DAT_00e11018 = DAT_00e11018 + 1;
LAB_007246c0:
    std::__ndk1::basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>>::
    operator=((basic_string<char,std::__ndk1::char_traits<char>,std::__ndk1::allocator<char>> *)
              (puVar6 + 5),(basic_string *)&local_68);
    if ((local_68 & 1) != 0) {
      operator_delete(local_58);
    }
  }
  std::__ndk1::mutex::unlock((mutex *)&DAT_00e10fd8);
  if (*(long *)(lVar2 + 0x28) == local_48) {
    return;
  }
LAB_00724840:
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * M2_Android_WebView_Attach @ 00724d8c
 * ============================================================ */

void M2_Android_WebView_Attach(long *param_1,long param_2)

{
  long lVar1;
  long *plVar2;
  char cVar3;
  uint uVar4;
  undefined8 uVar5;
  long *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  if ((param_1 == (long *)0x0) || (param_2 == 0)) goto LAB_00725144;
  local_40 = (long *)0x0;
  DAT_00e11028 = param_1;
  param_1 = (long *)(**(code **)(*param_1 + 0x30))(param_1,&local_40,0x10006);
  if ((int)param_1 == 0) {
LAB_00724e28:
    plVar2 = local_40;
    if (local_40 != (long *)0x0) {
      if (DAT_00e11030 != 0) {
        (**(code **)(*local_40 + 0xb0))(local_40);
        DAT_00e11030 = 0;
      }
      DAT_00e11030 = (**(code **)(*plVar2 + 0xa8))(plVar2,param_2);
      uVar5 = (**(code **)(*plVar2 + 0xf8))(plVar2,DAT_00e11030);
      DAT_00e11038 = (**(code **)(*plVar2 + 0x108))(plVar2,uVar5,"m2WebBrowserShow","([BIIIIIIII)V")
      ;
      cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
      if (cVar3 != '\0') {
        __android_log_print(6,"sancak2-web","%s: Java istisnasi","GetMethodID(m2WebBrowserShow)");
        (**(code **)(*plVar2 + 0x80))(plVar2);
        (**(code **)(*plVar2 + 0x88))(plVar2);
        DAT_00e11038 = 0;
      }
      DAT_00e11040 = (**(code **)(*plVar2 + 0x108))(plVar2,uVar5,"m2WebBrowserMove","(IIIIII)V");
      cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
      if (cVar3 != '\0') {
        __android_log_print(6,"sancak2-web","%s: Java istisnasi","GetMethodID(m2WebBrowserMove)");
        (**(code **)(*plVar2 + 0x80))(plVar2);
        (**(code **)(*plVar2 + 0x88))(plVar2);
        DAT_00e11040 = 0;
      }
      DAT_00e11048 = (**(code **)(*plVar2 + 0x108))(plVar2,uVar5,"m2WebBrowserHide",&DAT_003a8ec7);
      cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
      if (cVar3 != '\0') {
        __android_log_print(6,"sancak2-web","%s: Java istisnasi","GetMethodID(m2WebBrowserHide)");
        (**(code **)(*plVar2 + 0x80))(plVar2);
        (**(code **)(*plVar2 + 0x88))(plVar2);
        DAT_00e11048 = 0;
      }
      DAT_00e11050 = (**(code **)(*plVar2 + 0x108))(plVar2,uVar5,"m2PostNotification","([B[B)V");
      cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
      if (cVar3 != '\0') {
        __android_log_print(6,"sancak2-web","%s: Java istisnasi","GetMethodID(m2PostNotification)");
        (**(code **)(*plVar2 + 0x80))(plVar2);
        (**(code **)(*plVar2 + 0x88))(plVar2);
        DAT_00e11050 = 0;
      }
      DAT_00e11058 = (**(code **)(*plVar2 + 0x108))
                               (plVar2,uVar5,"m2GetSystemLanguage","()Ljava/lang/String;");
      cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
      if (cVar3 != '\0') {
        __android_log_print(6,"sancak2-web","%s: Java istisnasi","GetMethodID(m2GetSystemLanguage)")
        ;
        (**(code **)(*plVar2 + 0x80))(plVar2);
        (**(code **)(*plVar2 + 0x88))(plVar2);
        DAT_00e11058 = 0;
      }
      param_1 = (long *)(**(code **)(*plVar2 + 0xb8))(plVar2,uVar5);
      goto LAB_00725144;
    }
  }
  else if (((int)param_1 == -2) &&
          (param_1 = (long *)(**(code **)(*DAT_00e11028 + 0x20))(DAT_00e11028,&local_40,0),
          (int)param_1 == 0)) {
    pthread_once((pthread_once_t *)&DAT_00e11060,FUN_00725dd4);
    uVar4 = pthread_setspecific(DAT_00e11064,DAT_00e11028);
    param_1 = (long *)(ulong)uVar4;
    goto LAB_00724e28;
  }
  DAT_00e11028 = (long *)0x0;
LAB_00725144:
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(param_1);
}

/* ============================================================
 * M2_Android_WebView_Detach @ 0072516c
 * ============================================================ */

void M2_Android_WebView_Detach(void)

{
  long lVar1;
  int iVar2;
  long *local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  if (DAT_00e11028 != (long *)0x0) {
    local_40 = (long *)0x0;
    iVar2 = (**(code **)(*DAT_00e11028 + 0x30))(DAT_00e11028,&local_40,0x10006);
    if (iVar2 != 0) {
      if ((iVar2 != -2) ||
         (iVar2 = (**(code **)(*DAT_00e11028 + 0x20))(DAT_00e11028,&local_40,0), iVar2 != 0))
      goto LAB_00725220;
      pthread_once((pthread_once_t *)&DAT_00e11060,FUN_00725dd4);
      pthread_setspecific(DAT_00e11064,DAT_00e11028);
    }
    if ((local_40 != (long *)0x0) && (DAT_00e11030 != 0)) {
      (**(code **)(*local_40 + 0xb0))();
    }
  }
LAB_00725220:
  DAT_00e11030 = 0;
  DAT_00e11038 = 0;
  DAT_00e11040 = 0;
  DAT_00e11048 = 0;
  DAT_00e11050 = 0;
  DAT_00e11058 = 0;
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * M2_Android_PostNotification @ 00725274
 * ============================================================ */

void M2_Android_PostNotification(char *param_1,char *param_2)

{
  char *__s;
  char *__s_00;
  long lVar1;
  _jobject *p_Var2;
  char cVar3;
  int iVar4;
  size_t sVar5;
  long lVar6;
  long lVar7;
  undefined8 uVar8;
  _jobject *local_60;
  long local_58;
  
  lVar1 = tpidr_el0;
  local_58 = *(long *)(lVar1 + 0x28);
  if ((DAT_00e11028 != (long *)0x0 && DAT_00e11030 != (_jmethodID *)0x0) && DAT_00e11050 != 0) {
    local_60 = (_jobject *)0x0;
    iVar4 = (**(code **)(*DAT_00e11028 + 0x30))(DAT_00e11028,&local_60,0x10006);
    if (iVar4 != 0) {
      if ((iVar4 != -2) ||
         (iVar4 = (**(code **)(*DAT_00e11028 + 0x20))(DAT_00e11028,&local_60,0), iVar4 != 0))
      goto LAB_00725504;
      pthread_once((pthread_once_t *)&DAT_00e11060,FUN_00725dd4);
      pthread_setspecific(DAT_00e11064,DAT_00e11028);
    }
    p_Var2 = local_60;
    if (local_60 != (_jobject *)0x0) {
      __s = "";
      if (param_1 != (char *)0x0) {
        __s = param_1;
      }
      __s_00 = "";
      if (param_2 != (char *)0x0) {
        __s_00 = param_2;
      }
      sVar5 = strlen(__s);
      lVar6 = (**(code **)(*(long *)p_Var2 + 0x580))(p_Var2,sVar5 & 0xffffffff);
      if (lVar6 != 0) {
        if (0 < (int)sVar5) {
          (**(code **)(*(long *)p_Var2 + 0x680))(p_Var2,lVar6,0,sVar5 & 0xffffffff,__s);
        }
        sVar5 = strlen(__s_00);
        lVar7 = (**(code **)(*(long *)p_Var2 + 0x580))(p_Var2,sVar5 & 0xffffffff);
        if (lVar7 != 0) {
          if (0 < (int)sVar5) {
            (**(code **)(*(long *)p_Var2 + 0x680))(p_Var2,lVar7,0,sVar5 & 0xffffffff,__s_00);
          }
          _JNIEnv::CallVoidMethod(p_Var2,DAT_00e11030,DAT_00e11050,lVar6,lVar7);
          (**(code **)(*(long *)p_Var2 + 0xb8))(p_Var2,lVar6);
          (**(code **)(*(long *)p_Var2 + 0xb8))(p_Var2,lVar7);
          cVar3 = (**(code **)(*(long *)p_Var2 + 0x720))(p_Var2);
          if (cVar3 == '\0') {
            uVar8 = 1;
            goto LAB_00725508;
          }
          __android_log_print(6,"sancak2-web","%s: Java istisnasi","m2PostNotification");
          (**(code **)(*(long *)p_Var2 + 0x80))(p_Var2);
          (**(code **)(*(long *)p_Var2 + 0x88))(p_Var2);
          goto LAB_00725504;
        }
      }
      cVar3 = (**(code **)(*(long *)p_Var2 + 0x720))(p_Var2);
      if (cVar3 != '\0') {
        __android_log_print(6,"sancak2-web","%s: Java istisnasi","NewByteArray(notify)");
        (**(code **)(*(long *)p_Var2 + 0x80))(p_Var2);
        (**(code **)(*(long *)p_Var2 + 0x88))(p_Var2);
      }
      if (lVar6 != 0) {
        (**(code **)(*(long *)p_Var2 + 0xb8))(p_Var2,lVar6);
      }
    }
  }
LAB_00725504:
  uVar8 = 0;
LAB_00725508:
  if (*(long *)(lVar1 + 0x28) == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(uVar8);
}

/* ============================================================
 * M2_Android_GetSystemLanguage @ 00725540
 * ============================================================ */

undefined4 M2_Android_GetSystemLanguage(long *param_1,int param_2)

{
  uint uVar1;
  long lVar2;
  _jobject *p_Var3;
  char cVar4;
  uint uVar5;
  int iVar6;
  long *plVar7;
  long lVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  undefined8 local_50;
  long local_48;
  
  lVar2 = tpidr_el0;
  uVar9 = 0;
  local_48 = *(long *)(lVar2 + 0x28);
  plVar7 = param_1;
  if ((param_1 == (long *)0x0) || (param_2 < 3)) goto LAB_00725684;
  *(undefined1 *)param_1 = 0;
  uVar9 = 0;
  plVar7 = DAT_00e11028;
  if ((DAT_00e11028 == (long *)0x0) || ((DAT_00e11030 == (_jmethodID *)0x0 || (DAT_00e11058 == 0))))
  goto LAB_00725684;
  local_50 = (_jobject *)0x0;
  plVar7 = (long *)(**(code **)(*DAT_00e11028 + 0x30))(DAT_00e11028,&local_50,0x10006);
  if ((int)plVar7 == 0) {
LAB_0072560c:
    p_Var3 = local_50;
    if (local_50 != (_jobject *)0x0) {
      lVar8 = _JNIEnv::CallObjectMethod(local_50,DAT_00e11030,DAT_00e11058);
      plVar7 = (long *)(**(code **)(*(long *)p_Var3 + 0x720))(p_Var3);
      if (((ulong)plVar7 & 0xff) == 0) {
        if (lVar8 != 0) {
          iVar6 = (**(code **)(*(long *)p_Var3 + 0x520))(p_Var3,lVar8);
          if (iVar6 == 2) {
            local_50 = (_jobject *)((ulong)local_50 & 0xffffffff00000000);
            (**(code **)(*(long *)p_Var3 + 0x6e0))(p_Var3,lVar8,0,2,&local_50);
            cVar4 = (**(code **)(*(long *)p_Var3 + 0x720))(p_Var3);
            if (cVar4 != '\0') {
              __android_log_print(6,"sancak2-web","%s: Java istisnasi",
                                  "GetStringRegion(m2GetSystemLanguage)");
              (**(code **)(*(long *)p_Var3 + 0x80))(p_Var3);
              (**(code **)(*(long *)p_Var3 + 0x88))(p_Var3);
              goto LAB_0072574c;
            }
            uVar10 = 0;
            uVar5 = (ushort)local_50 + 0x20;
            if (0x19 < (ushort)local_50 - 0x41) {
              uVar5 = (uint)(ushort)local_50;
            }
            uVar1 = local_50._2_2_ + 0x20;
            if (0x19 < local_50._2_2_ - 0x41) {
              uVar1 = (uint)local_50._2_2_;
            }
            uVar9 = 0;
            if (((((ushort)local_50 < 0x80) && (uVar9 = uVar10, local_50._2_2_ < 0x80)) &&
                (0x60 < (uVar5 & 0xff))) &&
               ((((uVar5 & 0xff) < 0x7b && (0x60 < (uVar1 & 0xff))) && ((uVar1 & 0xff) < 0x7b)))) {
              uVar9 = 1;
              *(char *)param_1 = (char)uVar5;
              *(char *)((long)param_1 + 1) = (char)uVar1;
              *(undefined1 *)((long)param_1 + 2) = 0;
            }
          }
          else {
LAB_0072574c:
            uVar9 = 0;
          }
          plVar7 = (long *)(**(code **)(*(long *)p_Var3 + 0xb8))(p_Var3,lVar8);
          goto LAB_00725684;
        }
      }
      else {
        __android_log_print(6,"sancak2-web","%s: Java istisnasi","m2GetSystemLanguage");
        (**(code **)(*(long *)p_Var3 + 0x80))(p_Var3);
        plVar7 = (long *)(**(code **)(*(long *)p_Var3 + 0x88))(p_Var3);
      }
    }
  }
  else if (((int)plVar7 == -2) &&
          (plVar7 = (long *)(**(code **)(*DAT_00e11028 + 0x20))(DAT_00e11028,&local_50,0),
          (int)plVar7 == 0)) {
    pthread_once((pthread_once_t *)&DAT_00e11060,FUN_00725dd4);
    uVar5 = pthread_setspecific(DAT_00e11064,DAT_00e11028);
    plVar7 = (long *)(ulong)uVar5;
    goto LAB_0072560c;
  }
  uVar9 = 0;
LAB_00725684:
  if (*(long *)(lVar2 + 0x28) == local_48) {
    return uVar9;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(plVar7);
}

/* ============================================================
 * M2_Android_WebView_SetClientSize @ 007257e4
 * ============================================================ */

void M2_Android_WebView_SetClientSize(undefined4 param_1,undefined4 param_2)

{
  DAT_00e11068 = param_1;
  DAT_00e1106c = param_2;
  return;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::CAndroidInputAdapter @ 0072d170
 * ============================================================ */

/* m2input::CAndroidInputAdapter::CAndroidInputAdapter(m2input::CInputCore&) */

void __thiscall
m2input::CAndroidInputAdapter::CAndroidInputAdapter(CAndroidInputAdapter *this,CInputCore *param_1)

{
  *(CInputCore **)this = param_1;
  *(undefined8 *)(this + 0x10) = 0;
  *(undefined8 *)(this + 0x18) = 0;
  *(undefined4 *)(this + 0x20) = 0;
  this[8] = (CAndroidInputAdapter)0x1;
  return;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::SetUnicodeCharResolver @ 0072d188
 * ============================================================ */

/* m2input::CAndroidInputAdapter::SetUnicodeCharResolver(int (*)(void*, int, int, int, int), void*)
    */

void __thiscall
m2input::CAndroidInputAdapter::SetUnicodeCharResolver
          (CAndroidInputAdapter *this,_func_int_void_ptr_int_int_int_int *param_1,void *param_2)

{
  *(void **)(this + 0x18) = param_2;
  *(_func_int_void_ptr_int_int_int_int **)(this + 0x10) = param_1;
  return;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::HandleInputEvent @ 0072d19c
 * ============================================================ */

/* m2input::CAndroidInputAdapter::HandleInputEvent(AInputEvent const*) */

undefined4 __thiscall
m2input::CAndroidInputAdapter::HandleInputEvent(CAndroidInputAdapter *this,AInputEvent *param_1)

{
  long lVar1;
  undefined4 uVar2;
  CAndroidInputAdapter *this_00;
  SAndroidInputRecord local_128 [4];
  undefined8 local_124;
  undefined8 uStack_11c;
  undefined8 local_114;
  undefined8 uStack_10c;
  undefined8 local_104;
  undefined8 uStack_fc;
  undefined8 local_f4;
  undefined8 uStack_ec;
  undefined8 local_e4;
  undefined8 uStack_dc;
  undefined8 local_d4;
  undefined8 uStack_cc;
  undefined8 local_c4;
  undefined8 uStack_bc;
  undefined8 local_b4;
  undefined8 uStack_ac;
  undefined8 local_a4;
  undefined8 uStack_9c;
  undefined8 local_94;
  undefined8 uStack_8c;
  undefined8 local_84;
  undefined8 uStack_7c;
  undefined8 local_74;
  undefined8 uStack_6c;
  undefined8 local_64;
  undefined1 uStack_5c;
  undefined7 uStack_5b;
  undefined1 uStack_54;
  undefined8 uStack_53;
  undefined8 local_48;
  undefined4 local_40;
  long local_38;
  
  lVar1 = tpidr_el0;
  local_38 = *(long *)(lVar1 + 0x28);
  local_48 = 0;
  local_40 = 0;
  uStack_11c = 0;
  local_124 = 0;
  uStack_10c = 0;
  local_114 = 0;
  uStack_fc = 0;
  local_104 = 0;
  uStack_ec = 0;
  local_f4 = 0;
  uStack_dc = 0;
  local_e4 = 0;
  uStack_cc = 0;
  local_d4 = 0;
  uStack_bc = 0;
  local_c4 = 0;
  uStack_ac = 0;
  local_b4 = 0;
  uStack_9c = 0;
  local_a4 = 0;
  uStack_8c = 0;
  local_94 = 0;
  uStack_7c = 0;
  local_84 = 0;
  uStack_6c = 0;
  local_74 = 0;
  uStack_5c = 0;
  local_64 = 0;
  uStack_53 = 0;
  uStack_5b = 0;
  uStack_54 = 0;
  local_128[0] = (SAndroidInputRecord)0x0;
  uVar2 = 0;
  if (param_1 != (AInputEvent *)0x0) {
    this_00 = (CAndroidInputAdapter *)AInputEvent_getType(param_1);
    if ((int)this_00 == 1) {
      uVar2 = RecordKey(this,param_1,local_128);
    }
    else {
      if ((int)this_00 != 2) {
        uVar2 = 0;
        goto LAB_0072d26c;
      }
      uVar2 = RecordMotion(this_00,param_1,local_128);
    }
    if (local_128[0] != (SAndroidInputRecord)0x0) {
      DispatchRecord(this,local_128);
    }
  }
LAB_0072d26c:
  if (*(long *)(lVar1 + 0x28) == local_38) {
    return uVar2;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * m2input::CAndroidInputAdapter::RecordInputEvent @ 0072d298
 * ============================================================ */

/* m2input::CAndroidInputAdapter::RecordInputEvent(AInputEvent const*,
   m2input::SAndroidInputRecord*) const */

undefined8 __thiscall
m2input::CAndroidInputAdapter::RecordInputEvent
          (CAndroidInputAdapter *this,AInputEvent *param_1,SAndroidInputRecord *param_2)

{
  CAndroidInputAdapter *this_00;
  undefined8 uVar1;
  
  *param_2 = (SAndroidInputRecord)0x0;
  if (param_1 != (AInputEvent *)0x0) {
    this_00 = (CAndroidInputAdapter *)AInputEvent_getType(param_1);
    if ((int)this_00 == 1) {
      uVar1 = RecordKey(this,param_1,param_2);
      return uVar1;
    }
    if ((int)this_00 == 2) {
      uVar1 = RecordMotion(this_00,param_1,param_2);
      return uVar1;
    }
  }
  return 0;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::DispatchRecord @ 0072d31c
 * ============================================================ */

/* m2input::CAndroidInputAdapter::DispatchRecord(m2input::SAndroidInputRecord const&) */

void __thiscall
m2input::CAndroidInputAdapter::DispatchRecord
          (CAndroidInputAdapter *this,SAndroidInputRecord *param_1)

{
  uint uVar1;
  uint uVar2;
  SAndroidInputRecord SVar3;
  float fVar4;
  CInputCore *pCVar5;
  
  SVar3 = *param_1;
  if (SVar3 == (SAndroidInputRecord)0x3) {
    if (param_1[0xd9] == (SAndroidInputRecord)0x0) {
      if (param_1[0xda] != (SAndroidInputRecord)0x0) {
        if (param_1[0xdc] != (SAndroidInputRecord)0x0) {
          uVar1 = 0;
          if (param_1[0xd8] != (SAndroidInputRecord)0x0) {
            uVar1 = *(uint *)(param_1 + 0xe0);
          }
          CInputCore::KeyEvent
                    (*(CInputCore **)this,(uchar)param_1[0xdb],(uint)(byte)param_1[0xdc],uVar1,
                     (bool)param_1[0xd8],*(uint *)(param_1 + 0xe4),*(uint *)(param_1 + 4),
                     *(wchar32 *)(param_1 + 0xe8));
          return;
        }
        CInputCore::KeyEvent
                  (*(CInputCore **)this,(uchar)param_1[0xdb],0,0,(bool)param_1[0xd8],
                   *(uint *)(param_1 + 0xe4),*(uint *)(param_1 + 4),L'\0');
      }
      if (*(int *)(param_1 + 0xe8) != 0) {
        CInputCore::TextInput
                  (*(CInputCore **)this,(wchar32 *)(param_1 + 0xe8),1,*(uint *)(param_1 + 4));
        return;
      }
    }
    else if ((param_1[0xd8] != (SAndroidInputRecord)0x0) && (*(int *)(param_1 + 0xe4) == 0)) {
      CInputCore::RequestClose((uint)*(undefined8 *)this);
      return;
    }
  }
  else if (SVar3 == (SAndroidInputRecord)0x2) {
    switch(*(undefined4 *)(param_1 + 8)) {
    case 0:
    case 5:
      CInputCore::TouchDown
                (*(CInputCore **)this,*(int *)(param_1 + 0x10),*(float *)(param_1 + 0x50),
                 *(float *)(param_1 + 0x90),*(uint *)(param_1 + 4));
      return;
    case 1:
    case 6:
      CInputCore::TouchUp(*(CInputCore **)this,*(int *)(param_1 + 0x10),*(float *)(param_1 + 0x50),
                          *(float *)(param_1 + 0x90),*(uint *)(param_1 + 4));
      return;
    case 2:
      CInputCore::TouchMoveMany
                (*(CInputCore **)this,(int *)(param_1 + 0x10),(float *)(param_1 + 0x50),
                 (float *)(param_1 + 0x90),(ulong)*(uint *)(param_1 + 0xc),*(uint *)(param_1 + 4));
      return;
    case 3:
      CInputCore::TouchCancelAll(*(CInputCore **)this,*(uint *)(param_1 + 4));
      return;
    }
  }
  else if (SVar3 == (SAndroidInputRecord)0x1) {
                    /* WARNING: Load size is inaccurate */
    pCVar5._0_4_ = *(CInputCore **)(param_1 + 0x50);
    fVar4 = *(float *)(param_1 + 0x90);
    if (*(int *)(param_1 + 8) == 8) {
      CInputCore::MouseWheel
                (*(CInputCore **)this,(float)pCVar5._0_4_,fVar4,
                 (int)(long)(*(float *)(param_1 + 0xd0) * 120.0),*(uint *)(param_1 + 4));
      return;
    }
    CInputCore::MouseMove((float)pCVar5._0_4_,fVar4,(uint)*(undefined8 *)this);
    uVar2 = *(uint *)(param_1 + 0xd4);
    uVar1 = *(uint *)(this + 0x20) ^ uVar2;
    if ((uVar1 & 1) != 0) {
      CInputCore::MouseButton
                (pCVar5._0_4_,fVar4,*(undefined8 *)this,0,uVar2 & 1,*(undefined4 *)(param_1 + 4));
    }
    if ((uVar1 >> 1 & 1) != 0) {
      CInputCore::MouseButton
                (pCVar5._0_4_,fVar4,*(undefined8 *)this,1,uVar2 >> 1 & 1,
                 *(undefined4 *)(param_1 + 4));
    }
    if ((uVar1 >> 2 & 1) != 0) {
      CInputCore::MouseButton
                (pCVar5._0_4_,fVar4,*(undefined8 *)this,2,uVar2 >> 2 & 1,
                 *(undefined4 *)(param_1 + 4));
    }
    *(uint *)(this + 0x20) = uVar2;
  }
  return;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::RecordMotion @ 0072d5c4
 * ============================================================ */

/* m2input::CAndroidInputAdapter::RecordMotion(AInputEvent const*, m2input::SAndroidInputRecord*)
   const */

undefined8 __thiscall
m2input::CAndroidInputAdapter::RecordMotion
          (CAndroidInputAdapter *this,AInputEvent *param_1,SAndroidInputRecord *param_2)

{
  long lVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  int iVar5;
  undefined8 uVar6;
  ulong uVar7;
  long lVar8;
  undefined4 uVar9;
  
  uVar3 = AInputEvent_getSource(param_1);
  if ((uVar3 >> 1 & 1) == 0) {
    uVar6 = 0;
  }
  else {
    uVar4 = AMotionEvent_getAction(param_1);
    uVar2 = uVar4 & 0xff;
    uVar7 = AMotionEvent_getEventTime(param_1);
    *(int *)(param_2 + 4) = (int)(uVar7 / 1000000);
    *(uint *)(param_2 + 8) = uVar2;
    if ((((uVar3 ^ 0xffffffff) & 0x2002) == 0) &&
       (iVar5 = AMotionEvent_getToolType(param_1,0), iVar5 == 3)) {
      *param_2 = (SAndroidInputRecord)0x1;
      *(undefined4 *)(param_2 + 0xc) = 1;
      uVar9 = AMotionEvent_getX(param_1,0);
      *(undefined4 *)(param_2 + 0x50) = uVar9;
      uVar9 = AMotionEvent_getY(param_1,0);
      *(undefined4 *)(param_2 + 0x90) = uVar9;
      if (uVar2 == 8) {
        uVar9 = AMotionEvent_getAxisValue(param_1,9,0);
        uVar6 = 1;
        *(undefined4 *)(param_2 + 0xd0) = uVar9;
      }
      else {
        uVar9 = AMotionEvent_getButtonState(param_1);
        uVar6 = 1;
        *(undefined4 *)(param_2 + 0xd4) = uVar9;
      }
    }
    else {
      uVar6 = 0;
      if (uVar2 < 7) {
        if ((1 << (ulong)(uVar4 & 0x1f) & 99U) == 0) {
          if (uVar2 == 2) {
            lVar8 = AMotionEvent_getPointerCount(param_1);
            if (lVar8 == 0) {
              iVar5 = 0;
            }
            else {
              uVar7 = lVar8 - 1;
              if (0xe < uVar7) {
                uVar7 = 0xf;
              }
              lVar8 = 0;
              do {
                uVar9 = AMotionEvent_getPointerId(param_1,lVar8);
                *(undefined4 *)(param_2 + lVar8 * 4 + 0x10) = uVar9;
                uVar9 = AMotionEvent_getX(param_1,lVar8);
                *(undefined4 *)(param_2 + lVar8 * 4 + 0x50) = uVar9;
                uVar9 = AMotionEvent_getY(param_1,lVar8);
                lVar1 = lVar8 + 1;
                *(undefined4 *)(param_2 + lVar8 * 4 + 0x90) = uVar9;
                lVar8 = lVar1;
              } while (uVar7 + 1 != lVar1);
              iVar5 = (int)uVar7 + 1;
            }
            uVar6 = 1;
            *(int *)(param_2 + 0xc) = iVar5;
            *param_2 = (SAndroidInputRecord)0x2;
          }
          else if (uVar2 == 3) {
            uVar6 = 1;
            *(undefined4 *)(param_2 + 0xc) = 0;
            *param_2 = (SAndroidInputRecord)0x2;
          }
        }
        else {
          uVar3 = uVar4 >> 8 & 0xff;
          *(undefined4 *)(param_2 + 0xc) = 1;
          *param_2 = (SAndroidInputRecord)0x2;
          uVar9 = AMotionEvent_getPointerId(param_1,uVar3);
          *(undefined4 *)(param_2 + 0x10) = uVar9;
          uVar9 = AMotionEvent_getX(param_1,uVar3);
          *(undefined4 *)(param_2 + 0x50) = uVar9;
          uVar9 = AMotionEvent_getY(param_1,uVar3);
          uVar6 = 1;
          *(undefined4 *)(param_2 + 0x90) = uVar9;
        }
      }
    }
  }
  return uVar6;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::RecordKey @ 0072d7d0
 * ============================================================ */

/* m2input::CAndroidInputAdapter::RecordKey(AInputEvent const*, m2input::SAndroidInputRecord*) const
    */

void __thiscall
m2input::CAndroidInputAdapter::RecordKey
          (CAndroidInputAdapter *this,AInputEvent *param_1,SAndroidInputRecord *param_2)

{
  long lVar1;
  byte bVar2;
  uint uVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  int iVar7;
  undefined4 uVar8;
  uint uVar9;
  ulong uVar10;
  code *pcVar11;
  undefined8 uVar12;
  undefined2 local_70;
  byte local_6e;
  long local_68;
  
  lVar1 = tpidr_el0;
  local_68 = *(long *)(lVar1 + 0x28);
  uVar3 = AKeyEvent_getAction(param_1);
  if (uVar3 < 2) {
    iVar4 = AKeyEvent_getKeyCode(param_1);
    iVar5 = AKeyEvent_getScanCode(param_1);
    uVar6 = AKeyEvent_getMetaState(param_1);
    iVar7 = AKeyEvent_getRepeatCount(param_1);
    uVar10 = AKeyEvent_getEventTime(param_1);
    if (iVar7 < 1) {
      iVar7 = 0;
    }
    param_2[0xd8] = (SAndroidInputRecord)(uVar3 == 0);
    *(int *)(param_2 + 0xe4) = iVar7;
    *(int *)(param_2 + 4) = (int)(uVar10 / 1000000);
    if (iVar4 == 4) {
      if (this[8] == (CAndroidInputAdapter)0x0) {
        uVar12 = 1;
        *param_2 = (SAndroidInputRecord)0x3;
        param_2[0xd9] = (SAndroidInputRecord)0x1;
        goto LAB_0072d984;
      }
      iVar5 = 0;
      iVar4 = 0x6f;
    }
    local_70 = 0;
    local_6e = 0;
    bVar2 = MapAndroidKey(iVar4,iVar5,(SKeyMapping *)&local_70);
    iVar7 = 0;
    pcVar11 = *(code **)(this + 0x10);
    if ((((uVar3 == 0) && (pcVar11 != (code *)0x0)) && (local_6e == 0)) && ((uVar6 & 0x1002) == 0))
    {
      uVar12 = *(undefined8 *)(this + 0x18);
      uVar8 = AInputEvent_getDeviceId(param_1);
      iVar7 = (*pcVar11)(uVar12,uVar8,iVar4,iVar5,uVar6);
      if (iVar7 < 0x20) {
        iVar7 = 0;
      }
    }
    if (((SAndroidInputRecord)(bVar2 & 1) != (SAndroidInputRecord)0x0) || (iVar7 != 0)) {
      uVar9 = (uint)local_6e;
      if ((uVar3 == 0) && (local_6e == 0)) {
        if ((uVar6 >> 0xc & 1) == 0) {
          uVar9 = 0;
        }
        else {
          uVar9 = CtrlLetterChar(local_70._1_1_);
        }
      }
      uVar12 = 1;
      param_2[0xda] = (SAndroidInputRecord)(bVar2 & 1);
      *param_2 = (SAndroidInputRecord)0x3;
      *(undefined2 *)(param_2 + 0xdb) = local_70;
      *(uint *)(param_2 + 0xe0) = uVar9 & 0xff;
      *(int *)(param_2 + 0xe8) = iVar7;
      goto LAB_0072d984;
    }
  }
  uVar12 = 0;
LAB_0072d984:
  if (*(long *)(lVar1 + 0x28) != local_68) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail(uVar12);
  }
  return;
}

/* ============================================================
 * m2input::AndroidKeyCodeToDik @ 0072da08
 * ============================================================ */

/* m2input::AndroidKeyCodeToDik(int) */

undefined1 m2input::AndroidKeyCodeToDik(int param_1)

{
  long lVar1;
  
  lVar1 = 0;
  do {
    if (*(int *)((long)&DAT_003edf70 + lVar1) == param_1) {
      return (&UNK_003edf74)[lVar1];
    }
    lVar1 = lVar1 + 8;
  } while (lVar1 != 0x350);
  return 0;
}

/* ============================================================
 * m2input::AndroidKeyCodeToVk @ 0072da40
 * ============================================================ */

/* m2input::AndroidKeyCodeToVk(int) */

undefined1 m2input::AndroidKeyCodeToVk(int param_1)

{
  long lVar1;
  
  lVar1 = 0;
  do {
    if (*(int *)((long)&DAT_003edf70 + lVar1) == param_1) {
      return (&UNK_003edf75)[lVar1];
    }
    lVar1 = lVar1 + 8;
  } while (lVar1 != 0x350);
  return 0;
}

/* ============================================================
 * m2input::MapAndroidKey @ 0072da78
 * ============================================================ */

/* m2input::MapAndroidKey(int, int, m2input::SKeyMapping*) */

undefined8 m2input::MapAndroidKey(int param_1,int param_2,SKeyMapping *param_3)

{
  uint uVar1;
  long lVar2;
  ulong uVar3;
  SKeyMapping SVar4;
  SKeyMapping SVar5;
  
  lVar2 = 0;
  do {
    if (*(int *)((long)&DAT_003edf70 + lVar2) == param_1) {
      uVar3 = (long)&DAT_003edf70 + lVar2;
      if (param_2 < 1) goto LAB_0072db34;
      goto LAB_0072dab8;
    }
    lVar2 = lVar2 + 8;
  } while (lVar2 != 0x350);
  if (param_2 < 1) {
    return 0;
  }
  uVar3 = 0;
LAB_0072dab8:
  if ((param_2 - 1U < 0x53) || (param_2 - 0x56U < 3)) {
    SVar4 = SUB41(param_2,0);
LAB_0072db24:
    if (uVar3 != 0) {
LAB_0072db38:
      SVar5 = *(SKeyMapping *)(uVar3 + 5);
      uVar3 = (ulong)*(byte *)(uVar3 + 6);
      goto LAB_0072db40;
    }
  }
  else {
    uVar1 = param_2 - 0x60;
    if ((uVar1 < 0x20) && ((0xe2a0ffdfU >> (ulong)(uVar1 & 0x1f) & 1) != 0)) {
      SVar4 = *(SKeyMapping *)((&PTR_DAT_00d3bcd0)[(int)uVar1] + 4);
    }
    else {
      SVar4 = (SKeyMapping)0x0;
    }
    if ((uVar3 == 0) && (SVar4 == (SKeyMapping)0x0)) {
      return 0;
    }
    if (SVar4 != (SKeyMapping)0x0) goto LAB_0072db24;
    if (uVar3 != 0) {
LAB_0072db34:
      SVar4 = *(SKeyMapping *)(uVar3 + 4);
      goto LAB_0072db38;
    }
    SVar4 = (SKeyMapping)0x0;
  }
  SVar5 = (SKeyMapping)0x0;
LAB_0072db40:
  *param_3 = SVar4;
  param_3[1] = SVar5;
  param_3[2] = SUB81(uVar3,0);
  return 1;
}

/* ============================================================
 * M2Android_SetNativeWindow @ 00731b34
 * ============================================================ */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* M2Android_SetNativeWindow(void*, int, int) */

void M2Android_SetNativeWindow(void *param_1,int param_2,int param_3)

{
  int iVar1;
  CInputCore *this;
  
  if ((DAT_00e11608 & 1) == 0) {
    iVar1 = __cxa_guard_acquire(&DAT_00e11608);
    if (iVar1 != 0) {
      DAT_00e115a0 = 0;
      DAT_00e11568 = 0;
      DAT_00e11560 = &DAT_00e11568;
      DAT_00e11580 = 0;
      DAT_00e11570 = 0;
      DAT_00e11578 = &DAT_00e11580;
      DAT_00e11598 = 0;
      DAT_00e11588 = 0;
      DAT_00e11590 = &DAT_00e11598;
      DAT_00e115b0 = (void *)0x0;
      DAT_00e115a8 = 0;
      _DAT_00e115c0 = 0;
      _DAT_00e115b8 = 0;
      DAT_00e115c8 = 0;
      DAT_00e115d0 = 0x3c;
      DAT_00e115d4 = 0;
      uRam0000000000e115e0 = 0;
      _DAT_00e115d8 = 0;
      DAT_00e115f0._0_1_ = 0;
      DAT_00e115e8 = 0;
      ram0x00e115f9 = 0;
      DAT_00e115f0._1_7_ = 0;
      DAT_00e115f8._0_1_ = 0;
      __cxa_atexit(FUN_00733724,&DAT_00e11560,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e11608);
    }
  }
  DAT_00e115b0 = param_1;
  if ((0 < param_2) && (0 < param_3)) {
    _DAT_00e115b8 = CONCAT44(param_3,param_2);
    this = (CInputCore *)m2input::Core();
    m2input::CInputCore::SetSurfaceSize(this,param_2,param_3);
    return;
  }
  return;
}

/* ============================================================
 * M2Android_GetNativeWindow @ 00731c4c
 * ============================================================ */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_GetNativeWindow() */

undefined8 M2Android_GetNativeWindow(void)

{
  int iVar1;
  
  if (((DAT_00e11608 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_00e11608), iVar1 != 0)) {
    DAT_00e115a0 = 0;
    DAT_00e11568 = 0;
    DAT_00e11560 = &DAT_00e11568;
    DAT_00e11580 = 0;
    DAT_00e11570 = 0;
    DAT_00e11578 = &DAT_00e11580;
    DAT_00e11598 = 0;
    DAT_00e11588 = 0;
    DAT_00e11590 = &DAT_00e11598;
    DAT_00e115b0 = 0;
    DAT_00e115a8 = 0;
    _DAT_00e115c0 = 0;
    _DAT_00e115b8 = 0;
    DAT_00e115c8 = 0;
    DAT_00e115d0 = 0x3c;
    DAT_00e115d4 = 0;
    uRam0000000000e115e0 = 0;
    _DAT_00e115d8 = 0;
    DAT_00e115f0._0_1_ = 0;
    DAT_00e115e8 = 0;
    ram0x00e115f9 = 0;
    DAT_00e115f0._1_7_ = 0;
    DAT_00e115f8._0_1_ = 0;
    __cxa_atexit(FUN_00733724,&DAT_00e11560,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e11608);
  }
  return DAT_00e115b0;
}

/* ============================================================
 * M2Android_GetNativeWindowForHwnd @ 00731d00
 * ============================================================ */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* M2Android_GetNativeWindowForHwnd(HWND__*) */

undefined8 M2Android_GetNativeWindowForHwnd(HWND__ *param_1)

{
  int iVar1;
  undefined8 uVar2;
  
  if (((DAT_00e11608 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_00e11608), iVar1 != 0)) {
    DAT_00e115a0 = 0;
    DAT_00e11568 = 0;
    DAT_00e11560 = &DAT_00e11568;
    DAT_00e11580 = 0;
    DAT_00e11570 = 0;
    DAT_00e11578 = &DAT_00e11580;
    DAT_00e11598 = 0;
    DAT_00e11588 = 0;
    DAT_00e11590 = &DAT_00e11598;
    DAT_00e115b0 = 0;
    DAT_00e115a8 = (HWND__ *)0x0;
    _DAT_00e115c0 = 0;
    _DAT_00e115b8 = 0;
    DAT_00e115c8 = 0;
    DAT_00e115d0 = 0x3c;
    DAT_00e115d4 = 0;
    uRam0000000000e115e0 = 0;
    _DAT_00e115d8 = 0;
    DAT_00e115f0._0_1_ = 0;
    DAT_00e115e8 = 0;
    ram0x00e115f9 = 0;
    DAT_00e115f0._1_7_ = 0;
    DAT_00e115f8._0_1_ = 0;
    __cxa_atexit(FUN_00733724,&DAT_00e11560,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e11608);
  }
  if (DAT_00e115a8 == param_1) {
    uVar2 = DAT_00e115b0;
    if (((DAT_00e11608 & 1) == 0) &&
       (iVar1 = __cxa_guard_acquire(&DAT_00e11608), uVar2 = DAT_00e115b0, iVar1 != 0)) {
      DAT_00e115a0 = 0;
      DAT_00e11568 = 0;
      DAT_00e11560 = &DAT_00e11568;
      DAT_00e11580 = 0;
      DAT_00e11570 = 0;
      DAT_00e11578 = &DAT_00e11580;
      DAT_00e11598 = 0;
      DAT_00e11588 = 0;
      DAT_00e11590 = &DAT_00e11598;
      DAT_00e115b0 = 0;
      DAT_00e115a8 = (HWND__ *)0x0;
      _DAT_00e115c0 = 0;
      _DAT_00e115b8 = 0;
      DAT_00e115c8 = 0;
      DAT_00e115d0 = 0x3c;
      DAT_00e115d4 = 0;
      uRam0000000000e115e0 = 0;
      _DAT_00e115d8 = 0;
      DAT_00e115f0._0_1_ = 0;
      DAT_00e115e8 = 0;
      ram0x00e115f9 = 0;
      DAT_00e115f0._1_7_ = 0;
      DAT_00e115f8._0_1_ = 0;
      __cxa_atexit(FUN_00733724,&DAT_00e11560,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e11608);
      uVar2 = DAT_00e115b0;
    }
  }
  else {
    uVar2 = 0;
  }
  return uVar2;
}

/* ============================================================
 * M2Android_SetVirtualScreenSize @ 00731e8c
 * ============================================================ */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* M2Android_SetVirtualScreenSize(int, int) */

void M2Android_SetVirtualScreenSize(int param_1,int param_2)

{
  int iVar1;
  
  if ((DAT_00e11608 & 1) == 0) {
    iVar1 = __cxa_guard_acquire(&DAT_00e11608);
    if (iVar1 != 0) {
      DAT_00e115a0 = 0;
      DAT_00e11568 = 0;
      DAT_00e11560 = &DAT_00e11568;
      DAT_00e11580 = 0;
      DAT_00e11570 = 0;
      DAT_00e11578 = &DAT_00e11580;
      DAT_00e11598 = 0;
      DAT_00e11588 = 0;
      DAT_00e11590 = &DAT_00e11598;
      DAT_00e115b0 = 0;
      DAT_00e115a8 = 0;
      _DAT_00e115c0 = 0;
      _DAT_00e115b8 = 0;
      DAT_00e115c8 = 0;
      DAT_00e115d0 = 0x3c;
      DAT_00e115d4 = 0;
      uRam0000000000e115e0 = 0;
      _DAT_00e115d8 = 0;
      DAT_00e115f0._0_1_ = 0;
      DAT_00e115e8 = 0;
      ram0x00e115f9 = 0;
      DAT_00e115f0._1_7_ = 0;
      DAT_00e115f8._0_1_ = 0;
      __cxa_atexit(FUN_00733724,&DAT_00e11560,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e11608);
    }
  }
  _DAT_00e115c0 = CONCAT44(DAT_00e115c4,param_1);
  if ((DAT_00e11608 & 1) == 0) {
    iVar1 = __cxa_guard_acquire(&DAT_00e11608);
    if (iVar1 != 0) {
      DAT_00e115a0 = 0;
      DAT_00e11568 = 0;
      DAT_00e11560 = &DAT_00e11568;
      DAT_00e11580 = 0;
      DAT_00e11570 = 0;
      DAT_00e11578 = &DAT_00e11580;
      DAT_00e11598 = 0;
      DAT_00e11588 = 0;
      DAT_00e11590 = &DAT_00e11598;
      DAT_00e115b0 = 0;
      DAT_00e115a8 = 0;
      _DAT_00e115c0 = 0;
      _DAT_00e115b8 = 0;
      DAT_00e115c8 = 0;
      DAT_00e115d0 = 0x3c;
      DAT_00e115d4 = 0;
      uRam0000000000e115e0 = 0;
      _DAT_00e115d8 = 0;
      DAT_00e115f0._0_1_ = 0;
      DAT_00e115e8 = 0;
      ram0x00e115f9 = 0;
      DAT_00e115f0._1_7_ = 0;
      DAT_00e115f8._0_1_ = 0;
      __cxa_atexit(FUN_00733724,&DAT_00e11560,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e11608);
    }
  }
  _DAT_00e115c0 = CONCAT44(param_2,DAT_00e115c0);
  return;
}

/* ============================================================
 * M2Android_SetDisplayRefreshRate @ 00732020
 * ============================================================ */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* M2Android_SetDisplayRefreshRate(int) */

void M2Android_SetDisplayRefreshRate(int param_1)

{
  int iVar1;
  int iVar2;
  
  iVar1 = DAT_00e115d0;
  if (((0 < param_1) && (iVar1 = param_1, (DAT_00e11608 & 1) == 0)) &&
     (iVar2 = __cxa_guard_acquire(&DAT_00e11608), iVar1 = param_1, iVar2 != 0)) {
    DAT_00e115a0 = 0;
    DAT_00e11568 = 0;
    DAT_00e11560 = &DAT_00e11568;
    DAT_00e11580 = 0;
    DAT_00e11570 = 0;
    DAT_00e11578 = &DAT_00e11580;
    DAT_00e11598 = 0;
    DAT_00e11588 = 0;
    DAT_00e11590 = &DAT_00e11598;
    DAT_00e115b0 = 0;
    DAT_00e115a8 = 0;
    _DAT_00e115c0 = 0;
    _DAT_00e115b8 = 0;
    DAT_00e115c8 = 0;
    DAT_00e115d0 = 0x3c;
    DAT_00e115d4 = 0;
    uRam0000000000e115e0 = 0;
    _DAT_00e115d8 = 0;
    DAT_00e115f0._0_1_ = 0;
    DAT_00e115e8 = 0;
    ram0x00e115f9 = 0;
    DAT_00e115f0._1_7_ = 0;
    DAT_00e115f8._0_1_ = 0;
    __cxa_atexit(FUN_00733724,&DAT_00e11560,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e11608);
    iVar1 = param_1;
  }
  DAT_00e115d0 = iVar1;
  return;
}

/* ============================================================
 * M2Android_FullscreenGameSize @ 007320f8
 * ============================================================ */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* M2Android_FullscreenGameSize(int*, int*) */

undefined4 M2Android_FullscreenGameSize(int *param_1,int *param_2)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  int iVar5;
  undefined4 uVar6;
  ulong uVar7;
  ulong uVar8;
  ulong uVar9;
  
  if ((DAT_00e11608 & 1) == 0) {
    iVar5 = __cxa_guard_acquire(&DAT_00e11608);
    if (iVar5 != 0) {
      DAT_00e115a0 = 0;
      DAT_00e11568 = 0;
      DAT_00e11560 = &DAT_00e11568;
      DAT_00e11580 = 0;
      DAT_00e11570 = 0;
      DAT_00e11578 = &DAT_00e11580;
      DAT_00e11598 = 0;
      DAT_00e11588 = 0;
      DAT_00e11590 = &DAT_00e11598;
      DAT_00e115b0 = 0;
      DAT_00e115a8 = 0;
      _DAT_00e115c0 = 0;
      _DAT_00e115b8 = 0;
      DAT_00e115c8 = 0;
      DAT_00e115d0 = 0x3c;
      DAT_00e115d4 = 0;
      uRam0000000000e115e0 = 0;
      _DAT_00e115d8 = 0;
      DAT_00e115f0._0_1_ = 0;
      DAT_00e115e8 = 0;
      ram0x00e115f9 = 0;
      DAT_00e115f0._1_7_ = 0;
      DAT_00e115f8._0_1_ = 0;
      __cxa_atexit(FUN_00733724,&DAT_00e11560,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e11608);
    }
  }
  uVar6 = 0;
  if ((param_1 != (int *)0x0) && (param_2 != (int *)0x0)) {
    if (((int)DAT_00e115b8 < 1) ||
       ((((int)DAT_00e115bc < 1 || (uVar3 = *param_1, (int)uVar3 < 1)) ||
        (uVar4 = *param_2, (int)uVar4 < 1)))) {
      uVar6 = 0;
    }
    else {
      uVar1 = DAT_00e115b8;
      if (DAT_00e115b8 <= DAT_00e115bc) {
        uVar1 = DAT_00e115bc;
      }
      uVar9 = (ulong)uVar1;
      uVar2 = DAT_00e115b8;
      if (DAT_00e115bc <= DAT_00e115b8) {
        uVar2 = DAT_00e115bc;
      }
      uVar7 = (ulong)uVar2;
      uVar8 = 0;
      if (uVar7 != 0) {
        uVar8 = ((ulong)(uVar2 >> 1) + uVar4 * uVar9) / uVar7;
      }
      uVar8 = uVar8 + 1 & 0x7ffffffffffffffe;
      iVar5 = 0;
      if (uVar9 != 0) {
        iVar5 = (int)(((ulong)(uVar1 >> 1) + uVar3 * uVar7) / uVar9);
      }
      uVar9 = uVar8;
      if (uVar8 < 800) {
        uVar9 = (ulong)uVar3;
      }
      uVar6 = 1;
      *param_1 = (int)uVar9;
      if (uVar8 < 800) {
        uVar4 = iVar5 + 1U & 0xfffffffe;
      }
      *param_2 = uVar4;
    }
  }
  return uVar6;
}

/* ============================================================
 * M2Android_OnFocusChanged @ 0073225c
 * ============================================================ */

/* M2Android_OnFocusChanged(bool) */

void M2Android_OnFocusChanged(bool param_1)

{
  uint uVar1;
  CInputCore *this;
  
  FUN_0072f594();
  this = (CInputCore *)m2input::Core();
  uVar1 = timeGetTime();
  m2input::CInputCore::SetPlatformFocus(this,param_1,uVar1);
  return;
}

/* ============================================================
 * M2Android_OnWindowLost @ 00732294
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_OnWindowLost() */

void M2Android_OnWindowLost(void)

{
  uint uVar1;
  CInputCore *this;
  
  FUN_0072f594();
  this = (CInputCore *)m2input::Core();
  uVar1 = timeGetTime();
  m2input::CInputCore::WindowLost(this,uVar1);
  return;
}

/* ============================================================
 * M2Android_OnWindowRestored @ 007322c4
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_OnWindowRestored() */

void M2Android_OnWindowRestored(void)

{
  uint uVar1;
  
  FUN_0072f594();
  uVar1 = m2input::Core();
  timeGetTime();
  m2input::CInputCore::WindowRestored(uVar1);
  return;
}

/* ============================================================
 * M2Android_RequestClose @ 007322f4
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_RequestClose() */

void M2Android_RequestClose(void)

{
  uint uVar1;
  
  FUN_0072f594();
  uVar1 = m2input::Core();
  timeGetTime();
  m2input::CInputCore::RequestClose(uVar1);
  return;
}

/* ============================================================
 * M2Android_HandleInputEvent @ 00732324
 * ============================================================ */

/* M2Android_HandleInputEvent(AInputEvent const*) */

void M2Android_HandleInputEvent(AInputEvent *param_1)

{
  int iVar1;
  CInputCore *pCVar2;
  
  FUN_0072f594();
  if (((DAT_00e11638 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_00e11638), iVar1 != 0)) {
    pCVar2 = (CInputCore *)m2input::Core();
    m2input::CAndroidInputAdapter::CAndroidInputAdapter
              ((CAndroidInputAdapter *)&DAT_00e11610,pCVar2);
    __cxa_guard_release(&DAT_00e11638);
  }
  m2input::CAndroidInputAdapter::HandleInputEvent((CAndroidInputAdapter *)&DAT_00e11610,param_1);
  return;
}

/* ============================================================
 * M2Android_PostInputRecordFromAnyThread @ 007323ac
 * ============================================================ */

/* M2Android_PostInputRecordFromAnyThread(m2input::SAndroidInputRecord const&) */

void M2Android_PostInputRecordFromAnyThread(SAndroidInputRecord *param_1)

{
  undefined8 *puVar1;
  ulong uVar2;
  undefined8 *puVar3;
  int iVar4;
  void *pvVar5;
  long lVar6;
  ulong uVar7;
  undefined8 *puVar8;
  ulong uVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  undefined8 uVar18;
  
  if (*param_1 == (SAndroidInputRecord)0x0) {
    return;
  }
  if (((DAT_00e116b8 & 1) == 0) && (iVar4 = __cxa_guard_acquire(&DAT_00e116b8), iVar4 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  std::__ndk1::mutex::lock((mutex *)&DAT_00e11640);
  if (((DAT_00e116b8 & 1) == 0) && (iVar4 = __cxa_guard_acquire(&DAT_00e116b8), iVar4 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  puVar8 = DAT_00e116a0;
  puVar1 = DAT_00e11698;
  lVar6 = (long)DAT_00e116a0 - (long)DAT_00e11698 >> 2;
  uVar9 = lVar6 * -0x34115b1e5f75270d;
  if (((uVar9 < 0x2000) || (*param_1 != (SAndroidInputRecord)0x2)) || (*(int *)(param_1 + 8) != 2))
  {
    if (DAT_00e116a0 != DAT_00e116a8) {
      uVar12 = *(undefined8 *)(param_1 + 0x10);
      uVar11 = *(undefined8 *)(param_1 + 0x28);
      uVar10 = *(undefined8 *)(param_1 + 0x20);
      uVar14 = *(undefined8 *)(param_1 + 8);
      uVar13 = *(undefined8 *)param_1;
      DAT_00e116a0[3] = *(undefined8 *)(param_1 + 0x18);
      DAT_00e116a0[2] = uVar12;
      DAT_00e116a0[5] = uVar11;
      DAT_00e116a0[4] = uVar10;
      DAT_00e116a0[1] = uVar14;
      *DAT_00e116a0 = uVar13;
      uVar12 = *(undefined8 *)(param_1 + 0x50);
      uVar11 = *(undefined8 *)(param_1 + 0x68);
      uVar10 = *(undefined8 *)(param_1 + 0x60);
      uVar16 = *(undefined8 *)(param_1 + 0x38);
      uVar15 = *(undefined8 *)(param_1 + 0x30);
      uVar14 = *(undefined8 *)(param_1 + 0x48);
      uVar13 = *(undefined8 *)(param_1 + 0x40);
      DAT_00e116a0[0xb] = *(undefined8 *)(param_1 + 0x58);
      DAT_00e116a0[10] = uVar12;
      DAT_00e116a0[0xd] = uVar11;
      DAT_00e116a0[0xc] = uVar10;
      DAT_00e116a0[7] = uVar16;
      DAT_00e116a0[6] = uVar15;
      DAT_00e116a0[9] = uVar14;
      DAT_00e116a0[8] = uVar13;
      uVar12 = *(undefined8 *)(param_1 + 0x90);
      uVar11 = *(undefined8 *)(param_1 + 0xa8);
      uVar10 = *(undefined8 *)(param_1 + 0xa0);
      uVar16 = *(undefined8 *)(param_1 + 0x78);
      uVar15 = *(undefined8 *)(param_1 + 0x70);
      uVar14 = *(undefined8 *)(param_1 + 0x88);
      uVar13 = *(undefined8 *)(param_1 + 0x80);
      puVar1 = DAT_00e116a0 + 0x12;
      puVar3 = DAT_00e116a0 + 0x13;
      DAT_00e116a0 = (undefined8 *)((long)DAT_00e116a0 + 0xec);
      *puVar3 = *(undefined8 *)(param_1 + 0x98);
      *puVar1 = uVar12;
      puVar8[0x15] = uVar11;
      puVar8[0x14] = uVar10;
      puVar8[0xf] = uVar16;
      puVar8[0xe] = uVar15;
      puVar8[0x11] = uVar14;
      puVar8[0x10] = uVar13;
      uVar16 = *(undefined8 *)(param_1 + 200);
      uVar15 = *(undefined8 *)(param_1 + 0xc0);
      uVar11 = *(undefined8 *)(param_1 + 0xd8);
      uVar10 = *(undefined8 *)(param_1 + 0xd0);
      uVar12 = *(undefined8 *)(param_1 + 0xdc);
      uVar14 = *(undefined8 *)(param_1 + 0xb8);
      uVar13 = *(undefined8 *)(param_1 + 0xb0);
      *(undefined8 *)((long)puVar8 + 0xe4) = *(undefined8 *)(param_1 + 0xe4);
      *(undefined8 *)((long)puVar8 + 0xdc) = uVar12;
      puVar8[0x19] = uVar16;
      puVar8[0x18] = uVar15;
      puVar8[0x1b] = uVar11;
      puVar8[0x1a] = uVar10;
      puVar8[0x17] = uVar14;
      puVar8[0x16] = uVar13;
      goto LAB_00732670;
    }
    uVar2 = uVar9 + 1;
    if (uVar2 < 0x115b1e5f75270d1) {
      uVar7 = lVar6 * -0x6822b63cbeea4e1a;
      if (uVar7 < uVar2 || uVar7 - uVar2 == 0) {
        uVar7 = uVar2;
      }
      if (0x8ad8f2fba93867 < uVar9) {
        uVar7 = 0x115b1e5f75270d0;
      }
      if (uVar7 == 0) {
        pvVar5 = (void *)0x0;
      }
      else {
        if (0x115b1e5f75270d0 < uVar7) {
                    /* WARNING: Subroutine does not return */
          FUN_006c1b78();
        }
        pvVar5 = operator_new(uVar7 * 0xec);
      }
      uVar14 = *(undefined8 *)(param_1 + 0xe4);
      uVar13 = *(undefined8 *)(param_1 + 0xdc);
      uVar10 = *(undefined8 *)(param_1 + 0xc0);
      uVar12 = *(undefined8 *)(param_1 + 0xd8);
      uVar11 = *(undefined8 *)(param_1 + 0xd0);
      DAT_00e11698 = (undefined8 *)((long)pvVar5 + lVar6 * 4);
      DAT_00e116a8 = (undefined8 *)((long)pvVar5 + uVar7 * 0xec);
      DAT_00e116a0 = (undefined8 *)((long)DAT_00e11698 + 0xec);
      uVar16 = *(undefined8 *)(param_1 + 0x88);
      uVar15 = *(undefined8 *)(param_1 + 0x80);
      uVar18 = *(undefined8 *)(param_1 + 0x98);
      uVar17 = *(undefined8 *)(param_1 + 0x90);
      DAT_00e11698[0x19] = *(undefined8 *)(param_1 + 200);
      DAT_00e11698[0x18] = uVar10;
      DAT_00e11698[0x1b] = uVar12;
      DAT_00e11698[0x1a] = uVar11;
      *(undefined8 *)((long)DAT_00e11698 + 0xe4) = uVar14;
      *(undefined8 *)((long)DAT_00e11698 + 0xdc) = uVar13;
      uVar13 = *(undefined8 *)(param_1 + 0xa8);
      uVar12 = *(undefined8 *)(param_1 + 0xa0);
      uVar11 = *(undefined8 *)(param_1 + 0xb8);
      uVar10 = *(undefined8 *)(param_1 + 0xb0);
      DAT_00e11698[0x11] = uVar16;
      DAT_00e11698[0x10] = uVar15;
      DAT_00e11698[0x13] = uVar18;
      DAT_00e11698[0x12] = uVar17;
      uVar15 = *(undefined8 *)(param_1 + 0x48);
      uVar14 = *(undefined8 *)(param_1 + 0x40);
      uVar17 = *(undefined8 *)(param_1 + 0x58);
      uVar16 = *(undefined8 *)(param_1 + 0x50);
      DAT_00e11698[0x15] = uVar13;
      DAT_00e11698[0x14] = uVar12;
      DAT_00e11698[0x17] = uVar11;
      DAT_00e11698[0x16] = uVar10;
      uVar13 = *(undefined8 *)(param_1 + 0x68);
      uVar12 = *(undefined8 *)(param_1 + 0x60);
      uVar11 = *(undefined8 *)(param_1 + 0x78);
      uVar10 = *(undefined8 *)(param_1 + 0x70);
      DAT_00e11698[9] = uVar15;
      DAT_00e11698[8] = uVar14;
      DAT_00e11698[0xb] = uVar17;
      DAT_00e11698[10] = uVar16;
      uVar15 = *(undefined8 *)(param_1 + 8);
      uVar14 = *(undefined8 *)param_1;
      uVar17 = *(undefined8 *)(param_1 + 0x18);
      uVar16 = *(undefined8 *)(param_1 + 0x10);
      DAT_00e11698[0xd] = uVar13;
      DAT_00e11698[0xc] = uVar12;
      DAT_00e11698[0xf] = uVar11;
      DAT_00e11698[0xe] = uVar10;
      uVar13 = *(undefined8 *)(param_1 + 0x28);
      uVar12 = *(undefined8 *)(param_1 + 0x20);
      uVar11 = *(undefined8 *)(param_1 + 0x38);
      uVar10 = *(undefined8 *)(param_1 + 0x30);
      DAT_00e11698[1] = uVar15;
      *DAT_00e11698 = uVar14;
      DAT_00e11698[3] = uVar17;
      DAT_00e11698[2] = uVar16;
      DAT_00e11698[5] = uVar13;
      DAT_00e11698[4] = uVar12;
      DAT_00e11698[7] = uVar11;
      DAT_00e11698[6] = uVar10;
      puVar3 = puVar8;
      for (; puVar8 != puVar1; puVar8 = (undefined8 *)((long)puVar8 + -0xec)) {
        uVar10 = *(undefined8 *)((long)puVar8 + -0xcc);
        uVar12 = *(undefined8 *)((long)puVar8 + -0xd4);
        uVar11 = *(undefined8 *)((long)puVar8 + -0xdc);
        uVar14 = *(undefined8 *)((long)puVar8 + -0xe4);
        uVar13 = *(undefined8 *)((long)puVar8 + -0xec);
        *(undefined8 *)((long)DAT_00e11698 + -0xc4) = *(undefined8 *)((long)puVar8 + -0xc4);
        *(undefined8 *)((long)DAT_00e11698 + -0xcc) = uVar10;
        *(undefined8 *)((long)DAT_00e11698 + -0xd4) = uVar12;
        *(undefined8 *)((long)DAT_00e11698 + -0xdc) = uVar11;
        *(undefined8 *)((long)DAT_00e11698 + -0xe4) = uVar14;
        *(undefined8 *)((long)DAT_00e11698 + -0xec) = uVar13;
        uVar10 = *(undefined8 *)((long)puVar8 + -0x8c);
        uVar12 = *(undefined8 *)((long)puVar8 + -0x94);
        uVar11 = *(undefined8 *)((long)puVar8 + -0x9c);
        uVar14 = *(undefined8 *)((long)puVar8 + -0xa4);
        uVar13 = *(undefined8 *)((long)puVar8 + -0xac);
        uVar16 = *(undefined8 *)((long)puVar8 + -0xb4);
        uVar15 = *(undefined8 *)((long)puVar8 + -0xbc);
        *(undefined8 *)((long)DAT_00e11698 + -0x84) = *(undefined8 *)((long)puVar8 + -0x84);
        *(undefined8 *)((long)DAT_00e11698 + -0x8c) = uVar10;
        *(undefined8 *)((long)DAT_00e11698 + -0x94) = uVar12;
        *(undefined8 *)((long)DAT_00e11698 + -0x9c) = uVar11;
        *(undefined8 *)((long)DAT_00e11698 + -0xa4) = uVar14;
        *(undefined8 *)((long)DAT_00e11698 + -0xac) = uVar13;
        *(undefined8 *)((long)DAT_00e11698 + -0xb4) = uVar16;
        *(undefined8 *)((long)DAT_00e11698 + -0xbc) = uVar15;
        uVar10 = *(undefined8 *)((long)puVar8 + -0x4c);
        uVar12 = *(undefined8 *)((long)puVar8 + -0x54);
        uVar11 = *(undefined8 *)((long)puVar8 + -0x5c);
        uVar14 = *(undefined8 *)((long)puVar8 + -100);
        uVar13 = *(undefined8 *)((long)puVar8 + -0x6c);
        uVar16 = *(undefined8 *)((long)puVar8 + -0x74);
        uVar15 = *(undefined8 *)((long)puVar8 + -0x7c);
        *(undefined8 *)((long)DAT_00e11698 + -0x44) = *(undefined8 *)((long)puVar8 + -0x44);
        *(undefined8 *)((long)DAT_00e11698 + -0x4c) = uVar10;
        *(undefined8 *)((long)DAT_00e11698 + -0x54) = uVar12;
        *(undefined8 *)((long)DAT_00e11698 + -0x5c) = uVar11;
        *(undefined8 *)((long)DAT_00e11698 + -100) = uVar14;
        *(undefined8 *)((long)DAT_00e11698 + -0x6c) = uVar13;
        *(undefined8 *)((long)DAT_00e11698 + -0x74) = uVar16;
        *(undefined8 *)((long)DAT_00e11698 + -0x7c) = uVar15;
        uVar10 = puVar8[-2];
        uVar12 = *(undefined8 *)((long)puVar8 + -0x14);
        uVar11 = *(undefined8 *)((long)puVar8 + -0x1c);
        uVar14 = *(undefined8 *)((long)puVar8 + -0x34);
        uVar13 = *(undefined8 *)((long)puVar8 + -0x3c);
        uVar16 = *(undefined8 *)((long)puVar8 + -0x24);
        uVar15 = *(undefined8 *)((long)puVar8 + -0x2c);
        DAT_00e11698[-1] = puVar8[-1];
        DAT_00e11698[-2] = uVar10;
        *(undefined8 *)((long)DAT_00e11698 + -0x14) = uVar12;
        *(undefined8 *)((long)DAT_00e11698 + -0x1c) = uVar11;
        *(undefined8 *)((long)DAT_00e11698 + -0x34) = uVar14;
        *(undefined8 *)((long)DAT_00e11698 + -0x3c) = uVar13;
        *(undefined8 *)((long)DAT_00e11698 + -0x24) = uVar16;
        *(undefined8 *)((long)DAT_00e11698 + -0x2c) = uVar15;
        DAT_00e11698 = (undefined8 *)((long)DAT_00e11698 + -0xec);
        puVar3 = puVar1;
      }
      if (puVar3 != (undefined8 *)0x0) {
        operator_delete(puVar3);
      }
      goto LAB_00732670;
    }
    FUN_00733948(&DAT_00e11698);
LAB_0073274c:
    iVar4 = __cxa_guard_acquire(&DAT_00e116b8);
    if (iVar4 != 0) {
      __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e116b8);
    }
  }
  else {
    if (((DAT_00e116b8 & 1) == 0) && (iVar4 = __cxa_guard_acquire(&DAT_00e116b8), iVar4 != 0)) {
      __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e116b8);
    }
    if (DAT_00e116b0 != '\0') goto LAB_00732670;
    if ((DAT_00e116b8 & 1) == 0) goto LAB_0073274c;
  }
  DAT_00e116b0 = '\x01';
  __android_log_print(5,"sancak2",
                      "girdi kutusu dolu (%u kayit) - oyun is parcacigi takili, MOVE kayitlari dusuruluyor"
                      ,(int)((ulong)((long)DAT_00e116a0 - (long)DAT_00e11698) >> 2) * -0x5f75270d);
LAB_00732670:
  std::__ndk1::mutex::unlock((mutex *)&DAT_00e11640);
  return;
}

/* ============================================================
 * M2Android_DispatchQueuedInput @ 007327a4
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_DispatchQueuedInput() */

void M2Android_DispatchQueuedInput(void)

{
  SAndroidInputRecord *pSVar1;
  SAndroidInputRecord *pSVar2;
  SAndroidInputRecord *pSVar3;
  int iVar4;
  CInputCore *pCVar5;
  
  if (((DAT_00e116b8 & 1) == 0) && (iVar4 = __cxa_guard_acquire(&DAT_00e116b8), iVar4 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  std::__ndk1::mutex::lock((mutex *)&DAT_00e11640);
  if (((DAT_00e116b8 & 1) == 0) && (iVar4 = __cxa_guard_acquire(&DAT_00e116b8), iVar4 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  if (DAT_00e11698 != DAT_00e116a0) {
    if (((DAT_00e116b8 & 1) == 0) && (iVar4 = __cxa_guard_acquire(&DAT_00e116b8), iVar4 != 0)) {
      __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e116b8);
    }
    pSVar3 = DAT_00e116a0;
    pSVar2 = DAT_00e11698;
    DAT_00e11698 = (SAndroidInputRecord *)0x0;
    DAT_00e116a0 = (SAndroidInputRecord *)0x0;
    DAT_00e116a8 = 0;
    if (((DAT_00e116b8 & 1) == 0) && (iVar4 = __cxa_guard_acquire(&DAT_00e116b8), iVar4 != 0)) {
      __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e116b8);
    }
    DAT_00e116b0 = 0;
    std::__ndk1::mutex::unlock((mutex *)&DAT_00e11640);
    FUN_0072f594();
    pSVar1 = pSVar2;
    if (((DAT_00e11638 & 1) == 0) && (iVar4 = __cxa_guard_acquire(&DAT_00e11638), iVar4 != 0)) {
      pCVar5 = (CInputCore *)m2input::Core();
      m2input::CAndroidInputAdapter::CAndroidInputAdapter
                ((CAndroidInputAdapter *)&DAT_00e11610,pCVar5);
      __cxa_guard_release(&DAT_00e11638);
    }
    for (; pSVar1 != pSVar3; pSVar1 = pSVar1 + 0xec) {
      m2input::CAndroidInputAdapter::DispatchRecord((CAndroidInputAdapter *)&DAT_00e11610,pSVar1);
    }
    if (pSVar2 == (SAndroidInputRecord *)0x0) {
      return;
    }
    operator_delete(pSVar2);
    return;
  }
  std::__ndk1::mutex::unlock((mutex *)&DAT_00e11640);
  return;
}

/* ============================================================
 * M2Android_Update @ 007329f8
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_Update() */

void M2Android_Update(void)

{
  long lVar1;
  void *pvVar2;
  ulong *puVar3;
  ulong *puVar4;
  uint uVar5;
  int iVar6;
  CInputCore *pCVar7;
  ulong uVar8;
  long lVar9;
  ulong *puVar10;
  undefined2 local_70;
  byte local_6e;
  long local_68;
  
  lVar1 = tpidr_el0;
  local_68 = *(long *)(lVar1 + 0x28);
  FUN_0072f594();
  uVar5 = timeGetTime();
  if (((DAT_00e116b8 & 1) == 0) && (iVar6 = __cxa_guard_acquire(&DAT_00e116b8), iVar6 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  std::__ndk1::mutex::lock((mutex *)&DAT_00e11640);
  if (((DAT_00e116b8 & 1) == 0) && (iVar6 = __cxa_guard_acquire(&DAT_00e116b8), iVar6 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  pvVar2 = DAT_00e11668;
  DAT_00e11670 = 0;
  DAT_00e11678 = 0;
  DAT_00e11668 = (void *)0x0;
  if (((DAT_00e116b8 & 1) == 0) && (iVar6 = __cxa_guard_acquire(&DAT_00e116b8), iVar6 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  puVar4 = DAT_00e11688;
  puVar3 = DAT_00e11680;
  DAT_00e11680 = (ulong *)0x0;
  DAT_00e11688 = (ulong *)0x0;
  DAT_00e11690 = 0;
  std::__ndk1::mutex::unlock((mutex *)&DAT_00e11640);
  pCVar7 = (CInputCore *)m2input::Core();
  if (puVar3 != puVar4) {
    lVar9 = 0;
    puVar10 = puVar3;
    do {
      uVar8 = *puVar10;
      if ((long)uVar8 < 0) {
        local_70 = 0;
        local_6e = 0;
        uVar8 = m2input::MapAndroidKey(~(uint)uVar8,0,(SKeyMapping *)&local_70);
        if ((uVar8 & 1) != 0) {
          m2input::CInputCore::KeyPress
                    (pCVar7,(uchar)local_70._0_1_,(uint)local_70._1_1_,(uint)local_6e,uVar5);
        }
      }
      else {
        m2input::CInputCore::TextInput(pCVar7,(wchar32 *)((long)pvVar2 + lVar9 * 4),uVar8,uVar5);
        lVar9 = uVar8 + lVar9;
      }
      puVar10 = puVar10 + 1;
    } while (puVar10 != puVar4);
  }
  if (puVar3 != (ulong *)0x0) {
    operator_delete(puVar3);
  }
  if (pvVar2 != (void *)0x0) {
    operator_delete(pvVar2);
  }
  pCVar7 = (CInputCore *)m2input::Core();
  m2input::CInputCore::Update(pCVar7,uVar5);
  if (*(long *)(lVar1 + 0x28) == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * M2Android_InputCore @ 00732c50
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_InputCore() */

void M2Android_InputCore(void)

{
  FUN_0072f594();
  m2input::Core();
  return;
}

/* ============================================================
 * M2Android_InputAdapter @ 00732c64
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_InputAdapter() */

undefined * M2Android_InputAdapter(void)

{
  int iVar1;
  CInputCore *pCVar2;
  
  if (((DAT_00e11638 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_00e11638), iVar1 != 0)) {
    pCVar2 = (CInputCore *)m2input::Core();
    m2input::CAndroidInputAdapter::CAndroidInputAdapter
              ((CAndroidInputAdapter *)&DAT_00e11610,pCVar2);
    __cxa_guard_release(&DAT_00e11638);
  }
  return &DAT_00e11610;
}

/* ============================================================
 * M2Android_EnsureInputHooks @ 00732ce0
 * ============================================================ */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_EnsureInputHooks() */

void M2Android_EnsureInputHooks(void)

{
  int iVar1;
  CInputCore *this;
  
  if (((DAT_00e11608 & 1) == 0) && (iVar1 = __cxa_guard_acquire(&DAT_00e11608), iVar1 != 0)) {
    DAT_00e115a0 = 0;
    DAT_00e11568 = 0;
    DAT_00e11560 = &DAT_00e11568;
    DAT_00e11580 = 0;
    DAT_00e11570 = 0;
    DAT_00e11578 = &DAT_00e11580;
    DAT_00e11598 = 0;
    DAT_00e11588 = 0;
    DAT_00e11590 = &DAT_00e11598;
    DAT_00e115b0 = 0;
    DAT_00e115a8 = 0;
    _DAT_00e115c0 = 0;
    _DAT_00e115b8 = 0;
    DAT_00e115c8 = 0;
    DAT_00e115d0 = 0x3c;
    DAT_00e115d4 = 0;
    uRam0000000000e115e0 = 0;
    _DAT_00e115d8 = 0;
    DAT_00e115f0._0_1_ = 0;
    DAT_00e115e8 = 0;
    ram0x00e115f9 = 0;
    DAT_00e115f0._1_7_ = 0;
    DAT_00e115f8._0_1_ = 0;
    __cxa_atexit(FUN_00733724,&DAT_00e11560,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e11608);
  }
  if (DAT_00e11600 != '\0') {
    return;
  }
  ram0x00e115f9 = CONCAT17(1,DAT_00e115f8._1_7_);
  this = (CInputCore *)m2input::Core();
  m2input::CInputCore::SetSendHook(this,FUN_0073381c,(void *)0x0);
  *(code **)(this + 0xa0) = FUN_00733884;
  m2input::CInputCore::SetCharEncoder(this,FUN_007338a4,(void *)0x0);
  m2input::CInputCore::SetSurfaceSize(this,DAT_00e115b8,DAT_00e115bc);
  return;
}

/* ============================================================
 * M2Android_SetTouchOverlay @ 00732ce4
 * ============================================================ */

/* M2Android_SetTouchOverlay(m2input::ITouchOverlay*) */

void M2Android_SetTouchOverlay(ITouchOverlay *param_1)

{
  long lVar1;
  
  lVar1 = m2input::Core();
  *(ITouchOverlay **)(lVar1 + 0x430) = param_1;
  return;
}

/* ============================================================
 * M2Android_PostTextFromAnyThread @ 00732d08
 * ============================================================ */

/* M2Android_PostTextFromAnyThread(char32_t const*, unsigned long) */

void M2Android_PostTextFromAnyThread(wchar32 *param_1,ulong param_2)

{
  ulong *puVar1;
  ulong *puVar2;
  int iVar3;
  void *pvVar4;
  ulong uVar5;
  ulong uVar6;
  ulong uVar7;
  ulong *puVar8;
  ulong *puVar9;
  ulong *puVar10;
  long lVar11;
  long lVar12;
  ulong uVar13;
  ulong uVar14;
  ulong uVar15;
  
  if ((param_1 == (wchar32 *)0x0) || (param_2 == 0)) {
    return;
  }
  if (((DAT_00e116b8 & 1) == 0) && (iVar3 = __cxa_guard_acquire(&DAT_00e116b8), iVar3 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  std::__ndk1::mutex::lock((mutex *)&DAT_00e11640);
  if (((DAT_00e116b8 & 1) == 0) && (iVar3 = __cxa_guard_acquire(&DAT_00e116b8), iVar3 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  if (((DAT_00e116b8 & 1) == 0) && (iVar3 = __cxa_guard_acquire(&DAT_00e116b8), iVar3 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  std::__ndk1::vector<char32_t,std::__ndk1::allocator<char32_t>>::insert<char32_t_const*,0>
            ((vector<char32_t,std::__ndk1::allocator<char32_t>> *)&DAT_00e11668,DAT_00e11670,param_1
             ,param_1 + param_2);
  if (((DAT_00e116b8 & 1) == 0) && (iVar3 = __cxa_guard_acquire(&DAT_00e116b8), iVar3 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  puVar9 = DAT_00e11688;
  puVar2 = DAT_00e11680;
  if (DAT_00e11688 < DAT_00e11690) {
    *DAT_00e11688 = param_2;
    DAT_00e11688 = DAT_00e11688 + 1;
    goto LAB_00732eb4;
  }
  lVar12 = (long)DAT_00e11688 - (long)DAT_00e11680;
  lVar11 = lVar12 >> 3;
  uVar6 = lVar11 + 1;
  if (uVar6 >> 0x3d != 0) {
    FUN_00733970(&DAT_00e11680);
LAB_00732fcc:
                    /* WARNING: Subroutine does not return */
    FUN_006c1b78();
  }
  uVar5 = (ulong)((long)DAT_00e11690 - (long)DAT_00e11680) >> 2;
  if (uVar5 <= uVar6) {
    uVar5 = uVar6;
  }
  if (0x7ffffffffffffff7 < (ulong)((long)DAT_00e11690 - (long)DAT_00e11680)) {
    uVar5 = 0x1fffffffffffffff;
  }
  if (uVar5 == 0) {
    pvVar4 = (void *)0x0;
  }
  else {
    if (uVar5 >> 0x3d != 0) goto LAB_00732fcc;
    pvVar4 = operator_new(uVar5 << 3);
  }
  DAT_00e11680 = (ulong *)((long)pvVar4 + lVar11 * 8);
  DAT_00e11690 = (ulong *)((long)pvVar4 + uVar5 * 8);
  DAT_00e11688 = DAT_00e11680 + 1;
  *DAT_00e11680 = param_2;
  if ((long)puVar9 - (long)puVar2 != 0) {
    uVar6 = ((long)puVar9 - (long)puVar2) - 8;
    puVar10 = puVar9;
    if ((0x57 < uVar6) && (0x1f < (ulong)((long)puVar9 + (-lVar12 - (long)pvVar4)))) {
      uVar6 = (uVar6 >> 3) + 1;
      uVar7 = uVar6 & 0x3ffffffffffffffc;
      puVar10 = puVar9 + -uVar7;
      DAT_00e11680 = DAT_00e11680 + -uVar7;
      puVar8 = (ulong *)((long)pvVar4 + lVar11 * 8 + -0x10);
      puVar9 = puVar9 + -2;
      uVar5 = uVar7;
      do {
        puVar1 = puVar9 + -1;
        uVar15 = puVar9[-2];
        uVar14 = puVar9[1];
        uVar13 = *puVar9;
        puVar9 = puVar9 + -4;
        uVar5 = uVar5 - 4;
        puVar8[-1] = *puVar1;
        puVar8[-2] = uVar15;
        puVar8[1] = uVar14;
        *puVar8 = uVar13;
        puVar8 = puVar8 + -4;
      } while (uVar5 != 0);
      if (uVar6 == uVar7) goto LAB_00732e98;
    }
    do {
      puVar10 = puVar10 + -1;
      DAT_00e11680 = DAT_00e11680 + -1;
      *DAT_00e11680 = *puVar10;
    } while (puVar10 != puVar2);
  }
LAB_00732e98:
  if (puVar2 != (ulong *)0x0) {
    operator_delete(puVar2);
  }
LAB_00732eb4:
  std::__ndk1::mutex::unlock((mutex *)&DAT_00e11640);
  return;
}

/* ============================================================
 * M2Android_PostKeyPressFromAnyThread @ 00733330
 * ============================================================ */

/* M2Android_PostKeyPressFromAnyThread(int) */

void M2Android_PostKeyPressFromAnyThread(int param_1)

{
  long *plVar1;
  long *plVar2;
  int iVar3;
  void *pvVar4;
  ulong uVar5;
  ulong uVar6;
  ulong uVar7;
  long *plVar8;
  long *plVar9;
  long *plVar10;
  long lVar11;
  long lVar12;
  long lVar13;
  
  if (((DAT_00e116b8 & 1) == 0) && (iVar3 = __cxa_guard_acquire(&DAT_00e116b8), iVar3 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  std::__ndk1::mutex::lock((mutex *)&DAT_00e11640);
  if (((DAT_00e116b8 & 1) == 0) && (iVar3 = __cxa_guard_acquire(&DAT_00e116b8), iVar3 != 0)) {
    __cxa_atexit(FUN_007338f8,&DAT_00e11640,&PTR_LOOP_00d39970);
    __cxa_guard_release(&DAT_00e116b8);
  }
  plVar9 = DAT_00e11688;
  plVar2 = DAT_00e11680;
  if (DAT_00e11688 < DAT_00e11690) {
    *DAT_00e11688 = (long)~param_1;
    DAT_00e11688 = DAT_00e11688 + 1;
    goto LAB_0073349c;
  }
  lVar12 = (long)DAT_00e11688 - (long)DAT_00e11680;
  lVar11 = lVar12 >> 3;
  uVar6 = lVar11 + 1;
  if (uVar6 >> 0x3d != 0) {
    FUN_00733970(&DAT_00e11680);
LAB_0073353c:
                    /* WARNING: Subroutine does not return */
    FUN_006c1b78();
  }
  uVar5 = (ulong)((long)DAT_00e11690 - (long)DAT_00e11680) >> 2;
  if (uVar5 <= uVar6) {
    uVar5 = uVar6;
  }
  if (0x7ffffffffffffff7 < (ulong)((long)DAT_00e11690 - (long)DAT_00e11680)) {
    uVar5 = 0x1fffffffffffffff;
  }
  if (uVar5 == 0) {
    pvVar4 = (void *)0x0;
  }
  else {
    if (uVar5 >> 0x3d != 0) goto LAB_0073353c;
    pvVar4 = operator_new(uVar5 << 3);
  }
  DAT_00e11680 = (long *)((long)pvVar4 + lVar11 * 8);
  DAT_00e11690 = (long *)((long)pvVar4 + uVar5 * 8);
  DAT_00e11688 = DAT_00e11680 + 1;
  *DAT_00e11680 = (long)~param_1;
  if ((long)plVar9 - (long)plVar2 != 0) {
    uVar6 = ((long)plVar9 - (long)plVar2) - 8;
    plVar10 = plVar9;
    if ((0x57 < uVar6) && (0x1f < (ulong)((long)plVar9 + (-lVar12 - (long)pvVar4)))) {
      uVar6 = (uVar6 >> 3) + 1;
      uVar7 = uVar6 & 0x3ffffffffffffffc;
      plVar10 = plVar9 + -uVar7;
      DAT_00e11680 = DAT_00e11680 + -uVar7;
      plVar8 = (long *)((long)pvVar4 + lVar11 * 8 + -0x10);
      plVar9 = plVar9 + -2;
      uVar5 = uVar7;
      do {
        plVar1 = plVar9 + -1;
        lVar13 = plVar9[-2];
        lVar12 = plVar9[1];
        lVar11 = *plVar9;
        plVar9 = plVar9 + -4;
        uVar5 = uVar5 - 4;
        plVar8[-1] = *plVar1;
        plVar8[-2] = lVar13;
        plVar8[1] = lVar12;
        *plVar8 = lVar11;
        plVar8 = plVar8 + -4;
      } while (uVar5 != 0);
      if (uVar6 == uVar7) goto LAB_00733480;
    }
    do {
      plVar10 = plVar10 + -1;
      DAT_00e11680 = DAT_00e11680 + -1;
      *DAT_00e11680 = *plVar10;
    } while (plVar10 != plVar2);
  }
LAB_00733480:
  if (plVar2 != (long *)0x0) {
    operator_delete(plVar2);
  }
LAB_0073349c:
  std::__ndk1::mutex::unlock((mutex *)&DAT_00e11640);
  return;
}

/* ============================================================
 * M2Android_ConsumeSoftKeyboardRequest @ 00733558
 * ============================================================ */

/* M2Android_ConsumeSoftKeyboardRequest(bool*) */

void M2Android_ConsumeSoftKeyboardRequest(bool *param_1)

{
  CInputCore *this;
  
  this = (CInputCore *)m2input::Core();
  m2input::CInputCore::ConsumeTextInputChange(this,param_1);
  return;
}

/* ============================================================
 * M2Android_ConsumeSoftKeyboardReset @ 0073357c
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_ConsumeSoftKeyboardReset() */

undefined1 M2Android_ConsumeSoftKeyboardReset(void)

{
  undefined1 uVar1;
  long lVar2;
  
  lVar2 = m2input::Core();
  uVar1 = *(undefined1 *)(lVar2 + 0x4de);
  *(undefined1 *)(lVar2 + 0x4de) = 0;
  return uVar1;
}

/* ============================================================
 * M2Android_SetClipboardReader @ 0073359c
 * ============================================================ */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* M2Android_SetClipboardReader(bool (*)(void*, std::__ndk1::basic_string<char,
   std::__ndk1::char_traits<char>, std::__ndk1::allocator<char> >*), void*) */

void M2Android_SetClipboardReader(_func_bool_void_ptr_basic_string_ptr *param_1,void *param_2)

{
  int iVar1;
  
  if ((DAT_00e11608 & 1) == 0) {
    iVar1 = __cxa_guard_acquire(&DAT_00e11608);
    if (iVar1 != 0) {
      DAT_00e115a0 = 0;
      DAT_00e11568 = 0;
      DAT_00e11560 = &DAT_00e11568;
      DAT_00e11580 = 0;
      DAT_00e11570 = 0;
      DAT_00e11578 = &DAT_00e11580;
      DAT_00e11598 = 0;
      DAT_00e11588 = 0;
      DAT_00e11590 = &DAT_00e11598;
      DAT_00e115b0 = 0;
      DAT_00e115a8 = 0;
      _DAT_00e115c0 = 0;
      _DAT_00e115b8 = 0;
      DAT_00e115c8 = 0;
      DAT_00e115d0 = 0x3c;
      DAT_00e115d4 = 0;
      uRam0000000000e115e0 = 0;
      _DAT_00e115d8 = 0;
      DAT_00e115f0._0_1_ = 0;
      DAT_00e115e8 = 0;
      DAT_00e115f8._1_7_ = 0;
      DAT_00e11600 = 0;
      DAT_00e115f0._1_7_ = 0;
      DAT_00e115f8._0_1_ = 0;
      __cxa_atexit(FUN_00733724,&DAT_00e11560,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e11608);
    }
  }
  DAT_00e115f0._0_1_ = SUB81(param_1,0);
  DAT_00e115f0._1_7_ = (undefined7)((ulong)param_1 >> 8);
  if ((DAT_00e11608 & 1) == 0) {
    iVar1 = __cxa_guard_acquire(&DAT_00e11608);
    if (iVar1 != 0) {
      DAT_00e115a0 = 0;
      DAT_00e11568 = 0;
      DAT_00e11560 = &DAT_00e11568;
      DAT_00e11580 = 0;
      DAT_00e11570 = 0;
      DAT_00e11578 = &DAT_00e11580;
      DAT_00e11598 = 0;
      DAT_00e11588 = 0;
      DAT_00e11590 = &DAT_00e11598;
      DAT_00e115b0 = 0;
      DAT_00e115a8 = 0;
      _DAT_00e115c0 = 0;
      _DAT_00e115b8 = 0;
      DAT_00e115c8 = 0;
      DAT_00e115d0 = 0x3c;
      DAT_00e115d4 = 0;
      uRam0000000000e115e0 = 0;
      _DAT_00e115d8 = 0;
      DAT_00e115f0._0_1_ = 0;
      DAT_00e115e8 = 0;
      DAT_00e115f8._1_7_ = 0;
      DAT_00e11600 = 0;
      DAT_00e115f0._1_7_ = 0;
      DAT_00e115f8._0_1_ = 0;
      __cxa_atexit(FUN_00733724,&DAT_00e11560,&PTR_LOOP_00d39970);
      __cxa_guard_release(&DAT_00e11608);
    }
  }
  DAT_00e115f8._0_1_ = SUB81(param_2,0);
  DAT_00e115f8._1_7_ = (undefined7)((ulong)param_2 >> 8);
  return;
}

/* ============================================================
 * M2Android_InstallJavaInputBridge @ 00733984
 * ============================================================ */

/* M2Android_InstallJavaInputBridge(_JavaVM*, _jobject*) */

void M2Android_InstallJavaInputBridge(_JavaVM *param_1,_jobject *param_2)

{
  long lVar1;
  long *plVar2;
  char cVar3;
  int iVar4;
  long lVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  CAndroidInputAdapter *this;
  long *local_50;
  long local_48;
  
  lVar1 = tpidr_el0;
  local_48 = *(long *)(lVar1 + 0x28);
  DAT_00e116c0 = param_1;
  if (param_1 != (_JavaVM *)0x0) {
    local_50 = (long *)0x0;
    iVar4 = (**(code **)(*(long *)param_1 + 0x30))(param_1,&local_50,0x10006);
    if (((iVar4 == 0) ||
        (iVar4 = (**(code **)(*(long *)DAT_00e116c0 + 0x20))(DAT_00e116c0,&local_50,0), iVar4 == 0))
       && (plVar2 = local_50, local_50 != (long *)0x0)) {
      if (DAT_00e116c8 != 0) {
        (**(code **)(*local_50 + 0xb0))(local_50);
      }
      if (param_2 == (_jobject *)0x0) {
        DAT_00e116c8 = 0;
      }
      else {
        DAT_00e116c8 = (**(code **)(*plVar2 + 0xa8))(plVar2,param_2);
      }
      lVar5 = (**(code **)(*plVar2 + 0x30))(plVar2,"android/view/KeyEvent");
      cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
      if (cVar3 != '\0') {
        (**(code **)(*plVar2 + 0x88))(plVar2);
      }
      uVar6 = DAT_00e116e0;
      if (lVar5 != 0) {
        DAT_00e116d0 = (**(code **)(*plVar2 + 0xa8))(plVar2,lVar5);
        (**(code **)(*plVar2 + 0xb8))(plVar2,lVar5);
        uVar6 = (**(code **)(*plVar2 + 0x108))(plVar2,DAT_00e116d0,"<init>","(JJIIIIII)V");
        cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
        if (cVar3 != '\0') {
          (**(code **)(*plVar2 + 0x88))(plVar2);
        }
        DAT_00e116d8 = uVar6;
        uVar6 = (**(code **)(*plVar2 + 0x108))(plVar2,DAT_00e116d0,"getUnicodeChar",&DAT_003a3d70);
        cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
        if (cVar3 != '\0') {
          (**(code **)(*plVar2 + 0x88))(plVar2);
        }
      }
      DAT_00e116e0 = uVar6;
      if (DAT_00e116c8 != 0) {
        uVar6 = (**(code **)(*plVar2 + 0xf8))(plVar2);
        uVar7 = (**(code **)(*plVar2 + 0x108))(plVar2,uVar6,"showKeyboard",&DAT_003a8ec7);
        cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
        if (cVar3 != '\0') {
          (**(code **)(*plVar2 + 0x88))(plVar2);
        }
        DAT_00e116e8 = uVar7;
        uVar7 = (**(code **)(*plVar2 + 0x108))(plVar2,uVar6,"hideKeyboard",&DAT_003a8ec7);
        cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
        if (cVar3 != '\0') {
          (**(code **)(*plVar2 + 0x88))(plVar2);
        }
        DAT_00e116f0 = uVar7;
        uVar7 = (**(code **)(*plVar2 + 0x108))(plVar2,uVar6,"resetKeyboardInput",&DAT_003a8ec7);
        cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
        if (cVar3 != '\0') {
          (**(code **)(*plVar2 + 0x88))(plVar2);
        }
        DAT_00e116f8 = uVar7;
        uVar7 = (**(code **)(*plVar2 + 0x108))
                          (plVar2,uVar6,"getClipboardText","()Ljava/lang/String;");
        cVar3 = (**(code **)(*plVar2 + 0x720))(plVar2);
        if (cVar3 != '\0') {
          (**(code **)(*plVar2 + 0x88))(plVar2);
        }
        DAT_00e11700 = uVar7;
        (**(code **)(*plVar2 + 0xb8))(plVar2,uVar6);
      }
      this = (CAndroidInputAdapter *)M2Android_InputAdapter();
      m2input::CAndroidInputAdapter::SetUnicodeCharResolver(this,FUN_00733d44,(void *)0x0);
      M2Android_SetClipboardReader(FUN_00733f00,(void *)0x0);
    }
  }
  if (*(long *)(lVar1 + 0x28) != local_48) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}

/* ============================================================
 * M2Android_JavaShowSoftKeyboard @ 0073412c
 * ============================================================ */

/* M2Android_JavaShowSoftKeyboard(bool) */

void M2Android_JavaShowSoftKeyboard(bool param_1)

{
  long *plVar1;
  char *pcVar2;
  long lVar3;
  char cVar4;
  int iVar5;
  _jobject *p_Var6;
  long lVar7;
  _jobject *local_40;
  long local_38;
  
  lVar3 = tpidr_el0;
  local_38 = *(long *)(lVar3 + 0x28);
  if (DAT_00e116c0 == (long *)0x0) {
    p_Var6 = (_jobject *)0x0;
  }
  else {
    local_40 = (_jobject *)0x0;
    iVar5 = (**(code **)(*DAT_00e116c0 + 0x30))(DAT_00e116c0,&local_40,0x10006);
    p_Var6 = local_40;
    if ((iVar5 != 0) &&
       (iVar5 = (**(code **)(*DAT_00e116c0 + 0x20))(DAT_00e116c0,&local_40,0), p_Var6 = local_40,
       iVar5 != 0)) {
      p_Var6 = (_jobject *)0x0;
    }
  }
  plVar1 = &DAT_00e116e8;
  if (!param_1) {
    plVar1 = &DAT_00e116f0;
  }
  lVar7 = *plVar1;
  pcVar2 = "GOSTER";
  if (!param_1) {
    pcVar2 = "GIZLE";
  }
  __android_log_print(4,"sancak2","yazilim klavyesi istegi: %s (env=%d etkinlik=%d yontem=%d)",
                      pcVar2,p_Var6 != (_jobject *)0x0,DAT_00e116c8 != (_jmethodID *)0x0,lVar7 != 0)
  ;
  if (((p_Var6 != (_jobject *)0x0) && (DAT_00e116c8 != (_jmethodID *)0x0)) && (lVar7 != 0)) {
    _JNIEnv::CallVoidMethod(p_Var6,DAT_00e116c8,lVar7);
    cVar4 = (**(code **)(*(long *)p_Var6 + 0x720))(p_Var6);
    if (cVar4 != '\0') {
      (**(code **)(*(long *)p_Var6 + 0x88))(p_Var6);
    }
  }
  if (*(long *)(lVar3 + 0x28) != local_38) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}

/* ============================================================
 * M2Android_JavaResetSoftKeyboard @ 00734288
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* M2Android_JavaResetSoftKeyboard() */

void M2Android_JavaResetSoftKeyboard(void)

{
  _jobject *p_Var1;
  long lVar2;
  char cVar3;
  int iVar4;
  _jobject *local_30;
  long local_28;
  
  lVar2 = tpidr_el0;
  local_28 = *(long *)(lVar2 + 0x28);
  if (DAT_00e116c0 != (long *)0x0) {
    local_30 = (_jobject *)0x0;
    iVar4 = (**(code **)(*DAT_00e116c0 + 0x30))(DAT_00e116c0,&local_30,0x10006);
    p_Var1 = local_30;
    if ((iVar4 != 0) &&
       (iVar4 = (**(code **)(*DAT_00e116c0 + 0x20))(DAT_00e116c0,&local_30,0), p_Var1 = local_30,
       iVar4 != 0)) {
      p_Var1 = (_jobject *)0x0;
    }
    if (((p_Var1 != (_jobject *)0x0) && (DAT_00e116c8 != (_jmethodID *)0x0)) && (DAT_00e116f8 != 0))
    {
      _JNIEnv::CallVoidMethod(p_Var1,DAT_00e116c8);
      cVar3 = (**(code **)(*(long *)p_Var1 + 0x720))(p_Var1);
      if (cVar3 != '\0') {
        (**(code **)(*(long *)p_Var1 + 0x88))(p_Var1);
      }
    }
  }
  if (*(long *)(lVar2 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * playerRequestDeleteGlobalQuickSlot @ 007a547c
 * ============================================================ */

/* playerRequestDeleteGlobalQuickSlot(_object*, _object*) */

void playerRequestDeleteGlobalQuickSlot(_object *param_1,_object *param_2)

{
  long lVar1;
  ulong uVar2;
  uint local_2c;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  uVar2 = PyTuple_GetInteger(param_2,0,(int *)&local_2c);
  if ((uVar2 & 1) == 0) {
    Py_BuildException((char *)0x0);
  }
  else {
    CPythonPlayer::RequestDeleteGlobalQuickSlot
              (*(CPythonPlayer **)PTR_ms_singleton_00d79958,local_2c);
    Py_BuildNone();
  }
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * playerRequestMoveGlobalQuickSlotToLocalQuickSlot @ 007a54f4
 * ============================================================ */

/* playerRequestMoveGlobalQuickSlotToLocalQuickSlot(_object*, _object*) */

void playerRequestMoveGlobalQuickSlotToLocalQuickSlot(_object *param_1,_object *param_2)

{
  long lVar1;
  ulong uVar2;
  uint local_30;
  uint uStack_2c;
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  uVar2 = PyTuple_GetInteger(param_2,0,(int *)&uStack_2c);
  if (((uVar2 & 1) == 0) ||
     (uVar2 = PyTuple_GetInteger(param_2,1,(int *)&local_30), (uVar2 & 1) == 0)) {
    Py_BuildException((char *)0x0);
  }
  else {
    CPythonPlayer::RequestMoveGlobalQuickSlotToLocalQuickSlot
              (*(CPythonPlayer **)PTR_ms_singleton_00d79958,uStack_2c,local_30);
    Py_BuildNone();
  }
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

/* ============================================================
 * CPythonPlayer::RequestMoveGlobalQuickSlotToLocalQuickSlot @ 007c373c
 * ============================================================ */

/* CPythonPlayer::RequestMoveGlobalQuickSlotToLocalQuickSlot(unsigned int, unsigned int) */

void __thiscall
CPythonPlayer::RequestMoveGlobalQuickSlotToLocalQuickSlot
          (CPythonPlayer *this,uint param_1,uint param_2)

{
  CPythonNetworkStream::SendQuickSlotMovePacket
            (*(CPythonNetworkStream **)PTR_ms_singleton_00d79a80,(uchar)param_1,
             (char)param_2 + (char)(*(int *)(this + 0x1c9c0) << 3));
  return;
}

/* ============================================================
 * CPythonPlayer::RequestDeleteGlobalQuickSlot @ 007c38c0
 * ============================================================ */

/* CPythonPlayer::RequestDeleteGlobalQuickSlot(unsigned int) */

void __thiscall CPythonPlayer::RequestDeleteGlobalQuickSlot(CPythonPlayer *this,uint param_1)

{
                    /* try { // try from 007c38c0 to 008c3927 has its CatchHandler @ 007c3444 */
  if (0x1f < param_1) {
    return;
  }
  CPythonNetworkStream::SendQuickSlotDelPacket
            (*(CPythonNetworkStream **)PTR_ms_singleton_00d79a80,(uchar)param_1);
  return;
}

/* ============================================================
 * M2Android_SetSplashPresenter @ 0083ed4c
 * ============================================================ */

/* M2Android_SetSplashPresenter(void (*)(void*, SM2AndroidSplashImage const*), void*) */

void M2Android_SetSplashPresenter
               (_func_void_void_ptr_SM2AndroidSplashImage_ptr *param_1,void *param_2)

{
  DAT_00e157b0 = param_1;
  DAT_00e157b8 = param_2;
  return;
}

/* ============================================================
 * CEffectManager::SetEffectInstanceGlobalMatrix @ 0086ef70
 * ============================================================ */

/* CEffectManager::SetEffectInstanceGlobalMatrix(D3DXMATRIX const&) */

void __thiscall
CEffectManager::SetEffectInstanceGlobalMatrix(CEffectManager *this,D3DXMATRIX *param_1)

{
  if (*(CEffectInstance **)(this + 0x60) != (CEffectInstance *)0x0) {
    CEffectInstance::SetGlobalMatrix(*(CEffectInstance **)(this + 0x60),param_1);
    return;
  }
  return;
}

/* ============================================================
 * ma_android_sdk_version @ 008be994
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* ma_android_sdk_version() */

void ma_android_sdk_version(void)

{
  long lVar1;
  uint uVar2;
  ulong uVar3;
  char local_90 [104];
  long local_28;
  
  lVar1 = tpidr_el0;
  local_28 = *(long *)(lVar1 + 0x28);
  local_90[0x55] = '\0';
  local_90[0x56] = '\0';
  local_90[0x57] = '\0';
  local_90[0x58] = '\0';
  local_90[0x59] = '\0';
  local_90[0x5a] = '\0';
  local_90[0x5b] = '\0';
  local_90[0x5c] = '\0';
  local_90[0x50] = '\0';
  local_90[0x51] = '\0';
  local_90[0x52] = '\0';
  local_90[0x53] = '\0';
  local_90[0x54] = '\0';
  local_90[0x18] = '\0';
  local_90[0x19] = '\0';
  local_90[0x1a] = '\0';
  local_90[0x1b] = '\0';
  local_90[0x1c] = '\0';
  local_90[0x1d] = '\0';
  local_90[0x1e] = '\0';
  local_90[0x1f] = '\0';
  local_90[0x10] = '\0';
  local_90[0x11] = '\0';
  local_90[0x12] = '\0';
  local_90[0x13] = '\0';
  local_90[0x14] = '\0';
  local_90[0x15] = '\0';
  local_90[0x16] = '\0';
  local_90[0x17] = '\0';
  local_90[0x28] = '\0';
  local_90[0x29] = '\0';
  local_90[0x2a] = '\0';
  local_90[0x2b] = '\0';
  local_90[0x2c] = '\0';
  local_90[0x2d] = '\0';
  local_90[0x2e] = '\0';
  local_90[0x2f] = '\0';
  local_90[0x20] = '\0';
  local_90[0x21] = '\0';
  local_90[0x22] = '\0';
  local_90[0x23] = '\0';
  local_90[0x24] = '\0';
  local_90[0x25] = '\0';
  local_90[0x26] = '\0';
  local_90[0x27] = '\0';
  local_90[0x38] = '\0';
  local_90[0x39] = '\0';
  local_90[0x3a] = '\0';
  local_90[0x3b] = '\0';
  local_90[0x3c] = '\0';
  local_90[0x3d] = '\0';
  local_90[0x3e] = '\0';
  local_90[0x3f] = '\0';
  local_90[0x30] = '\0';
  local_90[0x31] = '\0';
  local_90[0x32] = '\0';
  local_90[0x33] = '\0';
  local_90[0x34] = '\0';
  local_90[0x35] = '\0';
  local_90[0x36] = '\0';
  local_90[0x37] = '\0';
  local_90[0x48] = '\0';
  local_90[0x49] = '\0';
  local_90[0x4a] = '\0';
  local_90[0x4b] = '\0';
  local_90[0x4c] = '\0';
  local_90[0x4d] = '\0';
  local_90[0x4e] = '\0';
  local_90[0x4f] = '\0';
  local_90[0x40] = '\0';
  local_90[0x41] = '\0';
  local_90[0x42] = '\0';
  local_90[0x43] = '\0';
  local_90[0x44] = '\0';
  local_90[0x45] = '\0';
  local_90[0x46] = '\0';
  local_90[0x47] = '\0';
  local_90[8] = '\0';
  local_90[9] = '\0';
  local_90[10] = '\0';
  local_90[0xb] = '\0';
  local_90[0xc] = '\0';
  local_90[0xd] = '\0';
  local_90[0xe] = '\0';
  local_90[0xf] = '\0';
  local_90[0] = '\0';
  local_90[1] = '\0';
  local_90[2] = '\0';
  local_90[3] = '\0';
  local_90[4] = '\0';
  local_90[5] = '\0';
  local_90[6] = '\0';
  local_90[7] = '\0';
  uVar3 = __system_property_get("ro.build.version.sdk",local_90);
  if ((int)uVar3 != 0) {
    uVar2 = atoi(local_90);
    uVar3 = (ulong)uVar2;
  }
  if (*(long *)(lVar1 + 0x28) == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(uVar3);
}

/* ============================================================
 * android_getCpuFamily @ 00ac6dac
 * ============================================================ */

undefined4 android_getCpuFamily(void)

{
  undefined4 uVar1;
  
  pthread_once((pthread_once_t *)&DAT_01031d58,FUN_00ac6de4);
  uVar1 = 4;
  if (DAT_01031d5c == '\0') {
    uVar1 = 0;
  }
  return uVar1;
}

/* ============================================================
 * android_getCpuFeatures @ 00ac7070
 * ============================================================ */

undefined8 android_getCpuFeatures(void)

{
  pthread_once((pthread_once_t *)&DAT_01031d58,FUN_00ac6de4);
  return DAT_01031d60;
}

/* ============================================================
 * android_getCpuCount @ 00ac709c
 * ============================================================ */

undefined4 android_getCpuCount(void)

{
  pthread_once((pthread_once_t *)&DAT_01031d58,FUN_00ac6de4);
  return DAT_01031d68;
}

/* ============================================================
 * android_setCpu @ 00ac70c8
 * ============================================================ */

undefined4 android_setCpu(int param_1,undefined8 param_2)

{
  undefined4 uVar1;
  
  if ((DAT_01031d6c & 1) == 0) {
    uVar1 = 1;
    if (param_1 < 2) {
      param_1 = 1;
    }
    DAT_01031d5c = 1;
    DAT_01031d60 = param_2;
    DAT_01031d68 = param_1;
    pthread_once((pthread_once_t *)&DAT_01031d58,FUN_00ac7130);
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::CAndroidApplicationPlatformBase @ 00d14d10
 * ============================================================ */

void __thiscall
CAndroidApplicationPlatformBase::CAndroidApplicationPlatformBase
          (CAndroidApplicationPlatformBase *this)

{
  (*(code *)PTR_CAndroidApplicationPlatformBase_00d7cc38)();
  return;
}

/* ============================================================
 * <EXTERNAL>::__android_log_print @ 00d14d50
 * ============================================================ */

void __android_log_print(void)

{
  (*(code *)PTR___android_log_print_00d7cc58)();
  return;
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidSurfaceListener @ 00d14db0
 * ============================================================ */

void BgfxDeviceBackend::SetAndroidSurfaceListener(SAndroidSurfaceListener *param_1)

{
  (*(code *)PTR_SetAndroidSurfaceListener_00d7cc88)();
  return;
}

/* ============================================================
 * M2Android_SetSplashPresenter @ 00d14dc0
 * ============================================================ */

void M2Android_SetSplashPresenter
               (_func_void_void_ptr_SM2AndroidSplashImage_ptr *param_1,void *param_2)

{
  (*(code *)PTR_M2Android_SetSplashPresenter_00d7cc90)();
  return;
}

/* ============================================================
 * M2Android_InputCore @ 00d14dd0
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void M2Android_InputCore(void)

{
  (*(code *)PTR_M2Android_InputCore_00d7cc98)();
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::~CAndroidApplicationPlatformBase @ 00d14e10
 * ============================================================ */

void __thiscall
CAndroidApplicationPlatformBase::~CAndroidApplicationPlatformBase
          (CAndroidApplicationPlatformBase *this)

{
  (*(code *)PTR__CAndroidApplicationPlatformBase_00d7ccb8)();
  return;
}

/* ============================================================
 * CAndroidPlatform::OnAppCmd @ 00d14e20
 * ============================================================ */

void __thiscall CAndroidPlatform::OnAppCmd(CAndroidPlatform *this,int param_1)

{
  (*(code *)PTR_OnAppCmd_00d7ccc0)(this,param_1);
  return;
}

/* ============================================================
 * M2Android_HandleInputEvent @ 00d14e30
 * ============================================================ */

void M2Android_HandleInputEvent(AInputEvent *param_1)

{
  (*(code *)PTR_M2Android_HandleInputEvent_00d7ccc8)();
  return;
}

/* ============================================================
 * CAndroidPlatform::WriteDeviceReport @ 00d14e40
 * ============================================================ */

void __thiscall
CAndroidPlatform::WriteDeviceReport(CAndroidPlatform *this,uint param_1,uint param_2)

{
  (*(code *)PTR_WriteDeviceReport_00d7ccd0)(this,param_1,param_2);
  return;
}

/* ============================================================
 * CAndroidPlatform::SyncPresentation @ 00d14e80
 * ============================================================ */

void __thiscall CAndroidPlatform::SyncPresentation(CAndroidPlatform *this)

{
  (*(code *)PTR_SyncPresentation_00d7ccf0)();
  return;
}

/* ============================================================
 * CAndroidPlatform::UpdateKeyboardPan @ 00d14e90
 * ============================================================ */

void __thiscall CAndroidPlatform::UpdateKeyboardPan(CAndroidPlatform *this)

{
  (*(code *)PTR_UpdateKeyboardPan_00d7ccf8)();
  return;
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidSplashImage @ 00d14ee0
 * ============================================================ */

void BgfxDeviceBackend::SetAndroidSplashImage
               (int param_1,int param_2,int param_3,int param_4,uchar *param_5)

{
  (*(code *)PTR_SetAndroidSplashImage_00d7cd20)(param_1,param_2,param_3,param_4);
  return;
}

/* ============================================================
 * BgfxDeviceBackend::GetAndroidPresentationRect @ 00d14f30
 * ============================================================ */

void BgfxDeviceBackend::GetAndroidPresentationRect
               (int *param_1,int *param_2,int *param_3,int *param_4)

{
  (*(code *)PTR_GetAndroidPresentationRect_00d7cd48)();
  return;
}

/* ============================================================
 * CAndroidPlatform::~CAndroidPlatform @ 00d14f60
 * ============================================================ */

void __thiscall CAndroidPlatform::~CAndroidPlatform(CAndroidPlatform *this)

{
  (*(code *)PTR__CAndroidPlatform_00d7cd60)();
  return;
}

/* ============================================================
 * CAndroidPlatform::IsDestroyRequested @ 00d14f70
 * ============================================================ */

void __thiscall CAndroidPlatform::IsDestroyRequested(CAndroidPlatform *this)

{
  (*(code *)PTR_IsDestroyRequested_00d7cd68)();
  return;
}

/* ============================================================
 * CAndroidPlatform::WaitForFirstWindow @ 00d14f80
 * ============================================================ */

void __thiscall CAndroidPlatform::WaitForFirstWindow(CAndroidPlatform *this)

{
  (*(code *)PTR_WaitForFirstWindow_00d7cd70)();
  return;
}

/* ============================================================
 * CAndroidPlatform::PumpPlatformEvents @ 00d14f90
 * ============================================================ */

void __thiscall CAndroidPlatform::PumpPlatformEvents(CAndroidPlatform *this)

{
  (*(code *)PTR_PumpPlatformEvents_00d7cd78)();
  return;
}

/* ============================================================
 * BgfxDeviceBackend::CanRunWithoutAndroidSurface @ 00d14fa0
 * ============================================================ */

void BgfxDeviceBackend::CanRunWithoutAndroidSurface(void)

{
  (*(code *)PTR_CanRunWithoutAndroidSurface_00d7cd80)();
  return;
}

/* ============================================================
 * M2Android_DispatchQueuedInput @ 00d14fc0
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void M2Android_DispatchQueuedInput(void)

{
  (*(code *)PTR_M2Android_DispatchQueuedInput_00d7cd90)();
  return;
}

/* ============================================================
 * M2Android_JavaShowSoftKeyboard @ 00d14fe0
 * ============================================================ */

void M2Android_JavaShowSoftKeyboard(bool param_1)

{
  (*(code *)PTR_M2Android_JavaShowSoftKeyboard_00d7cda0)(param_1);
  return;
}

/* ============================================================
 * M2Android_JavaResetSoftKeyboard @ 00d14ff0
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void M2Android_JavaResetSoftKeyboard(void)

{
  (*(code *)PTR_M2Android_JavaResetSoftKeyboard_00d7cda8)();
  return;
}

/* ============================================================
 * CAndroidPlatform::OnWindowInit @ 00d15000
 * ============================================================ */

void __thiscall CAndroidPlatform::OnWindowInit(CAndroidPlatform *this)

{
  (*(code *)PTR_OnWindowInit_00d7cdb0)();
  return;
}

/* ============================================================
 * M2Android_OnWindowLost @ 00d15010
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void M2Android_OnWindowLost(void)

{
  (*(code *)PTR_M2Android_OnWindowLost_00d7cdb8)();
  return;
}

/* ============================================================
 * M2Android_SetNativeWindow @ 00d15020
 * ============================================================ */

void M2Android_SetNativeWindow(void *param_1,int param_2,int param_3)

{
  (*(code *)PTR_M2Android_SetNativeWindow_00d7cdc0)(param_1,param_2,param_3);
  return;
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidNativeWindow @ 00d15030
 * ============================================================ */

void BgfxDeviceBackend::SetAndroidNativeWindow(void *param_1,uint param_2,uint param_3)

{
  (*(code *)PTR_SetAndroidNativeWindow_00d7cdc8)(param_1,param_2,param_3);
  return;
}

/* ============================================================
 * M2Android_OnFocusChanged @ 00d15040
 * ============================================================ */

void M2Android_OnFocusChanged(bool param_1)

{
  (*(code *)PTR_M2Android_OnFocusChanged_00d7cdd0)(param_1);
  return;
}

/* ============================================================
 * CAndroidPlatform::OnSurfaceGeometryMaybeChanged @ 00d15050
 * ============================================================ */

void __thiscall
CAndroidPlatform::OnSurfaceGeometryMaybeChanged(CAndroidPlatform *this,char *param_1)

{
  (*(code *)PTR_OnSurfaceGeometryMaybeChanged_00d7cdd8)();
  return;
}

/* ============================================================
 * CAndroidPlatform::RefreshSafeInsets @ 00d15090
 * ============================================================ */

void __thiscall CAndroidPlatform::RefreshSafeInsets(CAndroidPlatform *this)

{
  (*(code *)PTR_RefreshSafeInsets_00d7cdf8)();
  return;
}

/* ============================================================
 * M2Android_OnWindowRestored @ 00d150a0
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void M2Android_OnWindowRestored(void)

{
  (*(code *)PTR_M2Android_OnWindowRestored_00d7ce00)();
  return;
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidSafeInsets @ 00d150c0
 * ============================================================ */

void BgfxDeviceBackend::SetAndroidSafeInsets(int param_1,int param_2,int param_3,int param_4)

{
  (*(code *)PTR_SetAndroidSafeInsets_00d7ce10)(param_1,param_2,param_3,param_4);
  return;
}

/* ============================================================
 * BgfxDeviceBackend::GetAndroidPanY @ 00d15150
 * ============================================================ */

void BgfxDeviceBackend::GetAndroidPanY(void)

{
  (*(code *)PTR_GetAndroidPanY_00d7ce58)();
  return;
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidPanY @ 00d15170
 * ============================================================ */

void BgfxDeviceBackend::SetAndroidPanY(int param_1)

{
  (*(code *)PTR_SetAndroidPanY_00d7ce68)(param_1);
  return;
}

/* ============================================================
 * BgfxDeviceBackend::SetAndroidSplashOverlay @ 00d15250
 * ============================================================ */

void BgfxDeviceBackend::SetAndroidSplashOverlay
               (int param_1,int param_2,int param_3,int param_4,uchar *param_5)

{
  (*(code *)PTR_SetAndroidSplashOverlay_00d7ced8)(param_1,param_2,param_3,param_4);
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::CreateMainWindow @ 00d152d0
 * ============================================================ */

void __thiscall
CAndroidApplicationPlatformBase::CreateMainWindow
          (CAndroidApplicationPlatformBase *this,int param_1,int param_2,bool param_3)

{
  (*(code *)PTR_CreateMainWindow_00d7cf18)(this,param_1,param_2,param_3);
  return;
}

/* ============================================================
 * M2_Android_WebView_SetClientSize @ 00d152e0
 * ============================================================ */

void M2_Android_WebView_SetClientSize(void)

{
  (*(code *)PTR_M2_Android_WebView_SetClientSize_00d7cf20)();
  return;
}

/* ============================================================
 * CAndroidApplicationPlatformBase::AdjustWindowSize @ 00d152f0
 * ============================================================ */

void __thiscall
CAndroidApplicationPlatformBase::AdjustWindowSize
          (CAndroidApplicationPlatformBase *this,int param_1,int param_2)

{
  (*(code *)PTR_AdjustWindowSize_00d7cf28)(this,param_1,param_2);
  return;
}

/* ============================================================
 * CAndroidPlatform::CAndroidPlatform @ 00d15370
 * ============================================================ */

void __thiscall
CAndroidPlatform::CAndroidPlatform
          (CAndroidPlatform *this,android_app *param_1,basic_string *param_2,bool param_3)

{
  (*(code *)PTR_CAndroidPlatform_00d7cf68)();
  return;
}

/* ============================================================
 * M2Android_InputAdapter @ 00d154d0
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void M2Android_InputAdapter(void)

{
  (*(code *)PTR_M2Android_InputAdapter_00d7d018)();
  return;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::RecordInputEvent @ 00d15510
 * ============================================================ */

void __thiscall
m2input::CAndroidInputAdapter::RecordInputEvent
          (CAndroidInputAdapter *this,AInputEvent *param_1,SAndroidInputRecord *param_2)

{
  (*(code *)PTR_RecordInputEvent_00d7d038)();
  return;
}

/* ============================================================
 * android_main @ 00d15530
 * ============================================================ */

void android_main(void)

{
  (*(code *)PTR_android_main_00d7d048)();
  return;
}

/* ============================================================
 * M2_Android_SetFilesDirectory @ 00d15550
 * ============================================================ */

void M2_Android_SetFilesDirectory(void)

{
  (*(code *)PTR_M2_Android_SetFilesDirectory_00d7d058)();
  return;
}

/* ============================================================
 * M2Android_InstallJavaInputBridge @ 00d15560
 * ============================================================ */

void M2Android_InstallJavaInputBridge(_JavaVM *param_1,_jobject *param_2)

{
  (*(code *)PTR_M2Android_InstallJavaInputBridge_00d7d060)();
  return;
}

/* ============================================================
 * M2_Android_WebView_Attach @ 00d15570
 * ============================================================ */

void M2_Android_WebView_Attach(void)

{
  (*(code *)PTR_M2_Android_WebView_Attach_00d7d068)();
  return;
}

/* ============================================================
 * M2_Android_SetShellFolderPath @ 00d15590
 * ============================================================ */

void M2_Android_SetShellFolderPath(void)

{
  (*(code *)PTR_M2_Android_SetShellFolderPath_00d7d078)();
  return;
}

/* ============================================================
 * M2_Android_WebView_Detach @ 00d15610
 * ============================================================ */

void M2_Android_WebView_Detach(void)

{
  (*(code *)PTR_M2_Android_WebView_Detach_00d7d0b8)();
  return;
}

/* ============================================================
 * android_app_pre_exec_cmd @ 00d16250
 * ============================================================ */

void android_app_pre_exec_cmd(void)

{
  (*(code *)PTR_android_app_pre_exec_cmd_00d7d6d8)();
  return;
}

/* ============================================================
 * android_app_post_exec_cmd @ 00d16260
 * ============================================================ */

void android_app_post_exec_cmd(void)

{
  (*(code *)PTR_android_app_post_exec_cmd_00d7d6e0)();
  return;
}

/* ============================================================
 * CPythonApplicationAndroid::WindowProcedure @ 00d173a0
 * ============================================================ */

void __thiscall
CPythonApplicationAndroid::WindowProcedure
          (CPythonApplicationAndroid *this,HWND__ *param_1,uint param_2,ulong param_3,long param_4)

{
  (*(code *)PTR_WindowProcedure_00d7df80)(this,param_1,param_2);
  return;
}

/* ============================================================
 * CPythonApplicationAndroid::~CPythonApplicationAndroid @ 00d173b0
 * ============================================================ */

void __thiscall
CPythonApplicationAndroid::~CPythonApplicationAndroid(CPythonApplicationAndroid *this)

{
  (*(code *)PTR__CPythonApplicationAndroid_00d7df88)();
  return;
}

/* ============================================================
 * M2Android_Update @ 00d17660
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void M2Android_Update(void)

{
  (*(code *)PTR_M2Android_Update_00d7e0e0)();
  return;
}

/* ============================================================
 * M2Android_ConsumeSoftKeyboardReset @ 00d17670
 * ============================================================ */

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void M2Android_ConsumeSoftKeyboardReset(void)

{
  (*(code *)PTR_M2Android_ConsumeSoftKeyboardReset_00d7e0e8)();
  return;
}

/* ============================================================
 * M2Android_ConsumeSoftKeyboardRequest @ 00d17680
 * ============================================================ */

void M2Android_ConsumeSoftKeyboardRequest(bool *param_1)

{
  (*(code *)PTR_M2Android_ConsumeSoftKeyboardRequest_00d7e0f0)();
  return;
}

/* ============================================================
 * CPythonApplicationAndroid::CPythonApplicationAndroid @ 00d176b0
 * ============================================================ */

void __thiscall
CPythonApplicationAndroid::CPythonApplicationAndroid
          (CPythonApplicationAndroid *this,IApplicationPlatform *param_1,
          CAndroidApplicationWindow *param_2,CScreen *param_3,CGraphicDevice *param_4)

{
  (*(code *)PTR_CPythonApplicationAndroid_00d7e108)();
  return;
}

/* ============================================================
 * BgfxDeviceBackend::ApplyAndroidSurface @ 00d19a20
 * ============================================================ */

void __thiscall
BgfxDeviceBackend::ApplyAndroidSurface
          (BgfxDeviceBackend *this,void *param_1,uint param_2,uint param_3)

{
  (*(code *)PTR_ApplyAndroidSurface_00d7f2c0)(this,param_1,param_2,param_3);
  return;
}

/* ============================================================
 * BgfxDeviceBackend::GetAndroidUiSurfaceView @ 00d19a70
 * ============================================================ */

void BgfxDeviceBackend::GetAndroidUiSurfaceView
               (ushort *param_1,int *param_2,int *param_3,float *param_4,float *param_5)

{
  (*(code *)PTR_GetAndroidUiSurfaceView_00d7f2e8)();
  return;
}

/* ============================================================
 * M2Android_GetNativeWindowForHwnd @ 00d1ad70
 * ============================================================ */

void M2Android_GetNativeWindowForHwnd(HWND__ *param_1)

{
  (*(code *)PTR_M2Android_GetNativeWindowForHwnd_00d7fc68)();
  return;
}

/* ============================================================
 * M2_Android_PostNotification @ 00d1bf60
 * ============================================================ */

void M2_Android_PostNotification(void)

{
  (*(code *)PTR_M2_Android_PostNotification_00d80560)();
  return;
}

/* ============================================================
 * M2_Android_GetSystemLanguage @ 00d1bf70
 * ============================================================ */

void M2_Android_GetSystemLanguage(void)

{
  (*(code *)PTR_M2_Android_GetSystemLanguage_00d80568)();
  return;
}

/* ============================================================
 * m2input::MapAndroidKey @ 00d1c300
 * ============================================================ */

void m2input::MapAndroidKey(int param_1,int param_2,SKeyMapping *param_3)

{
  (*(code *)PTR_MapAndroidKey_00d80730)(param_1,param_2);
  return;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::SetUnicodeCharResolver @ 00d1c340
 * ============================================================ */

void __thiscall
m2input::CAndroidInputAdapter::SetUnicodeCharResolver
          (CAndroidInputAdapter *this,_func_int_void_ptr_int_int_int_int *param_1,void *param_2)

{
  (*(code *)PTR_SetUnicodeCharResolver_00d80750)();
  return;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::HandleInputEvent @ 00d1c350
 * ============================================================ */

void __thiscall
m2input::CAndroidInputAdapter::HandleInputEvent(CAndroidInputAdapter *this,AInputEvent *param_1)

{
  (*(code *)PTR_HandleInputEvent_00d80758)();
  return;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::RecordMotion @ 00d1c360
 * ============================================================ */

void __thiscall
m2input::CAndroidInputAdapter::RecordMotion
          (CAndroidInputAdapter *this,AInputEvent *param_1,SAndroidInputRecord *param_2)

{
  (*(code *)PTR_RecordMotion_00d80760)();
  return;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::RecordKey @ 00d1c370
 * ============================================================ */

void __thiscall
m2input::CAndroidInputAdapter::RecordKey
          (CAndroidInputAdapter *this,AInputEvent *param_1,SAndroidInputRecord *param_2)

{
  (*(code *)PTR_RecordKey_00d80768)();
  return;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::DispatchRecord @ 00d1c380
 * ============================================================ */

void __thiscall
m2input::CAndroidInputAdapter::DispatchRecord
          (CAndroidInputAdapter *this,SAndroidInputRecord *param_1)

{
  (*(code *)PTR_DispatchRecord_00d80770)();
  return;
}

/* ============================================================
 * m2input::CAndroidInputAdapter::CAndroidInputAdapter @ 00d1c4b0
 * ============================================================ */

void __thiscall
m2input::CAndroidInputAdapter::CAndroidInputAdapter(CAndroidInputAdapter *this,CInputCore *param_1)

{
  (*(code *)PTR_CAndroidInputAdapter_00d80808)();
  return;
}

/* ============================================================
 * M2Android_FullscreenGameSize @ 00d1c590
 * ============================================================ */

void M2Android_FullscreenGameSize(int *param_1,int *param_2)

{
  (*(code *)PTR_M2Android_FullscreenGameSize_00d80878)();
  return;
}

/* ============================================================
 * M2Android_PostTextFromAnyThread @ 00d1c5a0
 * ============================================================ */

void M2Android_PostTextFromAnyThread(wchar32 *param_1,ulong param_2)

{
  (*(code *)PTR_M2Android_PostTextFromAnyThread_00d80880)();
  return;
}

/* ============================================================
 * M2Android_PostKeyPressFromAnyThread @ 00d1c5c0
 * ============================================================ */

void M2Android_PostKeyPressFromAnyThread(int param_1)

{
  (*(code *)PTR_M2Android_PostKeyPressFromAnyThread_00d80890)(param_1);
  return;
}

/* ============================================================
 * M2Android_SetClipboardReader @ 00d1c5d0
 * ============================================================ */

void M2Android_SetClipboardReader(_func_bool_void_ptr_basic_string_ptr *param_1,void *param_2)

{
  (*(code *)PTR_M2Android_SetClipboardReader_00d80898)();
  return;
}

/* ============================================================
 * <EXTERNAL>::__android_log_write @ 00d1c600
 * ============================================================ */

void __android_log_write(void)

{
  (*(code *)PTR___android_log_write_00d808b0)();
  return;
}

/* ============================================================
 * <EXTERNAL>::__android_log_vprint @ 00d1c610
 * ============================================================ */

void __android_log_vprint(void)

{
  (*(code *)PTR___android_log_vprint_00d808b8)();
  return;
}

/* ============================================================
 * CEffectManager::SetEffectInstanceGlobalMatrix @ 00d1db00
 * ============================================================ */

void __thiscall
CEffectManager::SetEffectInstanceGlobalMatrix(CEffectManager *this,D3DXMATRIX *param_1)

{
  (*(code *)PTR_SetEffectInstanceGlobalMatrix_00d81330)();
  return;
}

/* ============================================================
 * CPythonPlayer::RequestDeleteGlobalQuickSlot @ 00d21020
 * ============================================================ */

void __thiscall CPythonPlayer::RequestDeleteGlobalQuickSlot(CPythonPlayer *this,uint param_1)

{
  (*(code *)PTR_RequestDeleteGlobalQuickSlot_00d82dc0)(this,param_1);
  return;
}

/* ============================================================
 * CPythonPlayer::RequestMoveGlobalQuickSlotToLocalQuickSlot @ 00d21030
 * ============================================================ */

void __thiscall
CPythonPlayer::RequestMoveGlobalQuickSlotToLocalQuickSlot
          (CPythonPlayer *this,uint param_1,uint param_2)

{
  (*(code *)PTR_RequestMoveGlobalQuickSlotToLocalQuickSlot_00d82dc8)(this,param_1,param_2);
  return;
}

/* ============================================================
 * android_getCpuFamily @ 00d307a0
 * ============================================================ */

void android_getCpuFamily(void)

{
  (*(code *)PTR_android_getCpuFamily_00d8a980)();
  return;
}

/* ============================================================
 * android_getCpuFeatures @ 00d307b0
 * ============================================================ */

void android_getCpuFeatures(void)

{
  (*(code *)PTR_android_getCpuFeatures_00d8a988)();
  return;
}

/* ============================================================
 * <EXTERNAL>::android_set_abort_message @ 00d358b0
 * ============================================================ */

void android_set_abort_message(void)

{
  (*(code *)PTR_android_set_abort_message_00d8d208)();
  return;
}

/* ============================================================
 * <EXTERNAL>::__android_log_print @ 01095018
 * ============================================================ */

/* WARNING: Control flow encountered bad instruction data */

void __android_log_print(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}

/* ============================================================
 * <EXTERNAL>::__android_log_write @ 01095618
 * ============================================================ */

/* WARNING: Control flow encountered bad instruction data */

void __android_log_write(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}

/* ============================================================
 * <EXTERNAL>::__android_log_vprint @ 01095620
 * ============================================================ */

/* WARNING: Control flow encountered bad instruction data */

void __android_log_vprint(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}

/* ============================================================
 * <EXTERNAL>::android_set_abort_message @ 010963b8
 * ============================================================ */

/* WARNING: Control flow encountered bad instruction data */

void android_set_abort_message(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* SUMMARY: selected=7978 success=7978 failed=0 */
