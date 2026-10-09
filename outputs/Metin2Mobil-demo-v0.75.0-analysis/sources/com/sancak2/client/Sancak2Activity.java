package com.sancak2.client;
public class Sancak2Activity extends android.app.NativeActivity {
    private static final String SALE_CHANNEL_ID = "averos2_pazar";
    private volatile int[] mGameRect;
    private volatile int mImeBottom;
    private com.sancak2.client.Sancak2Activity$InputView mInputView;
    private volatile boolean mKeyboardWanted;
    private final Runnable mRehideBars;
    private volatile int mSafeBottom;
    private volatile int mSafeLeft;
    private volatile int mSafeRight;
    private volatile int mSafeTop;
    private int mSaleNotifyId;
    private com.sancak2.client.M2WebBrowser mWebBrowser;

    static bridge synthetic com.sancak2.client.Sancak2Activity$InputView -$$Nest$fgetmInputView(com.sancak2.client.Sancak2Activity p0)
    {
        return p0.mInputView;
    }

    static bridge synthetic Runnable -$$Nest$fgetmRehideBars(com.sancak2.client.Sancak2Activity p0)
    {
        return p0.mRehideBars;
    }

    static bridge synthetic void -$$Nest$mhideSystemBars(com.sancak2.client.Sancak2Activity p0)
    {
        p0.hideSystemBars();
        return;
    }

    static bridge synthetic void -$$Nest$mupdateSafeInsets(com.sancak2.client.Sancak2Activity p0, android.view.WindowInsets p1)
    {
        p0.updateSafeInsets(p1);
        return;
    }

    static Sancak2Activity()
    {
        System.loadLibrary("sancak2client");
        return;
    }

    public Sancak2Activity()
    {
        this.mImeBottom = 0;
        this.mKeyboardWanted = 0;
        this.mSaleNotifyId = 2000;
        this.mRehideBars = new com.sancak2.client.Sancak2Activity$5(this);
        return;
    }

    private void hideSystemBars()
    {
        int v0_4 = this.getWindow().getDecorView();
        if (android.os.Build$VERSION.SDK_INT >= 30) {
            this.getWindow().setDecorFitsSystemWindows(0);
            int v1_0 = v0_4.getWindowInsetsController();
            if (v1_0 != 0) {
                v1_0.hide((android.view.WindowInsets$Type.statusBars() | android.view.WindowInsets$Type.navigationBars()));
                v1_0.setSystemBarsBehavior(2);
                return;
            }
        }
        v0_4.setSystemUiVisibility(5894);
        return;
    }

    private void updateSafeInsets(android.view.WindowInsets p6)
    {
        int v1_1;
        int v4;
        int v0_1;
        int v3;
        int v2 = 0;
        if ((android.os.Build$VERSION.SDK_INT < 28) || (p6 == null)) {
            v0_1 = 0;
            v1_1 = 0;
            v3 = 0;
            v4 = 0;
        } else {
            int v0_6 = p6.getDisplayCutout();
            if (v0_6 == 0) {
            } else {
                v1_1 = v0_6.getSafeInsetLeft();
                v3 = v0_6.getSafeInsetTop();
                v4 = v0_6.getSafeInsetRight();
                v0_1 = v0_6.getSafeInsetBottom();
            }
        }
        this.mSafeLeft = v1_1;
        this.mSafeTop = v3;
        this.mSafeRight = v4;
        this.mSafeBottom = v0_1;
        if ((android.os.Build$VERSION.SDK_INT >= 30) && ((p6 != null) && (p6.isVisible(android.view.WindowInsets$Type.ime())))) {
            v2 = p6.getInsets(android.view.WindowInsets$Type.ime()).bottom;
        }
        this.mImeBottom = v2;
        return;
    }

    public String getClipboardText()
    {
        CharSequence v0_5 = ((android.content.ClipboardManager) this.getSystemService("clipboard"));
        String v1 = 0;
        if ((v0_5 != null) && (v0_5.hasPrimaryClip())) {
            CharSequence v0_1 = v0_5.getPrimaryClip();
            if ((v0_1 != null) && (v0_1.getItemCount() != 0)) {
                CharSequence v0_3 = v0_1.getItemAt(0).coerceToText(this);
                if (v0_3 != null) {
                    v1 = v0_3.toString();
                }
            }
        }
        return v1;
    }

    int[] getGamePresentationRect()
    {
        return this.mGameRect;
    }

    public void hideKeyboard()
    {
        this.mKeyboardWanted = 0;
        com.sancak2.client.Sancak2Activity$3 v0_4 = this.getWindow().getDecorView();
        v0_4.removeCallbacks(this.mRehideBars);
        v0_4.postDelayed(this.mRehideBars, 500);
        this.runOnUiThread(new com.sancak2.client.Sancak2Activity$3(this));
        return;
    }

    public int m2GetImeInset()
    {
        return this.mImeBottom;
    }

    public int[] m2GetSafeInsets()
    {
        return new int[] {this.mSafeLeft, this.mSafeTop, this.mSafeRight, this.mSafeBottom});
    }

    public String m2GetSystemLanguage()
    {
        try {
            String v1_2;
            String v1_1 = java.util.Locale.getDefault();
        } catch (Exception) {
            return "";
        }
        if (v1_1 != null) {
            v1_2 = v1_1.getLanguage();
        } else {
            v1_2 = 0;
        }
        if (v1_2 != null) {
            String v1_0 = v1_2.toLowerCase(java.util.Locale.ROOT);
            if (!v1_0.equals("iw")) {
                if (!v1_0.equals("in")) {
                    if (v1_0.equals("ji")) {
                        v1_0 = "yi";
                    }
                } else {
                    v1_0 = "id";
                }
            } else {
                v1_0 = "he";
            }
            if (v1_0.length() == 2) {
                return v1_0;
            } else {
                return "";
            }
        } else {
            return "";
        }
    }

    public void m2PostNotification(byte[] p6, byte[] p7)
    {
        try {
            android.app.Notification$BigTextStyle v1_6 = java.nio.charset.Charset.forName("windows-1254");
        } catch (int v6_4) {
            android.util.Log.w("sancak2", new StringBuilder("pazar bildirimi gosterilemedi: ").append(v6_4).toString());
            return;
        }
        int v2_2 = new String(p6, v1_6);
        int v6_1 = new String(p7, v1_6);
        String v7_3 = ((android.app.NotificationManager) this.getSystemService("notification"));
        if (v7_3 != null) {
            if (v7_3.getNotificationChannel("averos2_pazar") == null) {
                android.app.Notification$BigTextStyle v1_3 = new android.app.NotificationChannel("averos2_pazar", "Pazar sat\u0131\u015flar\u0131", 4);
                v1_3.setDescription("Pazara koydu\u011funuz e\u015fya sat\u0131l\u0131nca bildirim");
                v7_3.createNotificationChannel(v1_3);
            }
            android.app.Notification$BigTextStyle v1_5 = new android.content.Intent(this, com.sancak2.client.Sancak2Activity);
            v1_5.setFlags(805306368);
            android.app.Notification$BigTextStyle v1_7 = android.app.PendingIntent.getActivity(this, 1, v1_5, 201326592);
            android.app.Notification$Builder v4_3 = new android.app.Notification$Builder(this, "averos2_pazar");
            v4_3.setContentTitle(v2_2).setContentText(v6_1).setSmallIcon(com.sancak2.client.R$mipmap.ic_launcher).setContentIntent(v1_7).setAutoCancel(1).setStyle(new android.app.Notification$BigTextStyle().bigText(v6_1));
            int v6_3 = this.mSaleNotifyId;
            this.mSaleNotifyId = (v6_3 + 1);
            v7_3.notify(v6_3, v4_3.build());
            return;
        } else {
            return;
        }
    }

    public void m2SetGamePresentationRect(int p1, int p2, int p3, int p4)
    {
        this.mGameRect = new int[] {p1, p2, p3, p4});
        return;
    }

    public void m2WebBrowserHide()
    {
        this.mWebBrowser.hide();
        return;
    }

    public void m2WebBrowserMove(int p8, int p9, int p10, int p11, int p12, int p13)
    {
        this.mWebBrowser.move(p8, p9, p10, p11, p12, p13);
        return;
    }

    public void m2WebBrowserShow(byte[] p12, int p13, int p14, int p15, int p16, int p17, int p18, int p19, int p20)
    {
        this.mWebBrowser.show(p12, p13, p14, p15, p16, p17, p18, p19, p20);
        return;
    }

    native void nativeCommitText(String p0);

    native void nativeKeyDown(int p0);

    protected void onCreate(android.os.Bundle p3)
    {
        super.onCreate(p3);
        this.mWebBrowser = new com.sancak2.client.M2WebBrowser(this);
        this.getWindow().addFlags(128);
        if (android.os.Build$VERSION.SDK_INT >= 28) {
            this.getWindow().getAttributes().layoutInDisplayCutoutMode = 1;
        }
        this.hideSystemBars();
        this.getWindow().getDecorView().setOnApplyWindowInsetsListener(new com.sancak2.client.Sancak2Activity$1(this));
        int v3_8 = new com.sancak2.client.Sancak2Activity$InputView(this, this);
        this.mInputView = v3_8;
        this.addContentView(v3_8, new android.view.ViewGroup$LayoutParams(1, 1));
        if ((android.os.Build$VERSION.SDK_INT >= 33) && (this.checkSelfPermission("android.permission.POST_NOTIFICATIONS") != 0)) {
            String[] v0_6 = new String[1];
            v0_6[0] = "android.permission.POST_NOTIFICATIONS";
            this.requestPermissions(v0_6, 7001);
        }
        com.sancak2.client.KeepAliveService.start(this);
        return;
    }

    protected void onDestroy()
    {
        com.sancak2.client.KeepAliveService.stop(this);
        com.sancak2.client.M2WebBrowser v0 = this.mWebBrowser;
        if (v0 != null) {
            v0.destroy();
        }
        super.onDestroy();
        return;
    }

    public void onWindowFocusChanged(boolean p3)
    {
        super.onWindowFocusChanged(p3);
        if (p3 != null) {
            this.hideSystemBars();
            if (this.mInputView != null) {
                com.sancak2.client.Sancak2Activity$InputView v3_6 = ((android.view.inputmethod.InputMethodManager) this.getSystemService("input_method"));
                if (v3_6 != null) {
                    v3_6.hideSoftInputFromWindow(this.mInputView.getWindowToken(), 0);
                }
                if (!this.mKeyboardWanted) {
                    this.mInputView.dropFocus();
                }
            }
        }
        return;
    }

    public void resetKeyboardInput()
    {
        this.runOnUiThread(new com.sancak2.client.Sancak2Activity$4(this));
        return;
    }

    public void showKeyboard()
    {
        this.mKeyboardWanted = 1;
        this.runOnUiThread(new com.sancak2.client.Sancak2Activity$2(this));
        return;
    }
}
