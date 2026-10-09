package com.sancak2.client;
final class M2WebBrowser {
    private static final String TAG = "sancak2-web";
    private final com.sancak2.client.Sancak2Activity mActivity;
    private com.sancak2.client.M2WebBrowser$GamePopup mPopup;
    private android.webkit.WebView mWebView;

    public static synthetic void $r8$lambda$IS5f4Kcig7-TtrDaeKhP5aT5Lz8(com.sancak2.client.M2WebBrowser p0, String p1, String p2, String p3, String p4, long p5)
    {
        p0.lambda$createWebView$3(p1, p2, p3, p4, p5);
        return;
    }

    public static synthetic void $r8$lambda$KzRwa5TVjwGs7d2OKM74_ami9eQ(com.sancak2.client.M2WebBrowser p0, int p1, int p2, int p3, int p4, int p5, int p6)
    {
        p0.lambda$move$1(p1, p2, p3, p4, p5, p6);
        return;
    }

    public static synthetic void $r8$lambda$o3MD4tGNrJBsNxj6pvlUOq4k0DM(com.sancak2.client.M2WebBrowser p0, byte[] p1, int p2, int p3, int p4, int p5, int p6, int p7, int p8, int p9)
    {
        p0.lambda$show$0(p1, p2, p3, p4, p5, p6, p7, p8, p9);
        return;
    }

    public static synthetic void $r8$lambda$oUBq4w5x5Te62lhkzv-eAIITocE(com.sancak2.client.M2WebBrowser p0)
    {
        p0.hideOnUiThread();
        return;
    }

    static bridge synthetic com.sancak2.client.Sancak2Activity -$$Nest$fgetmActivity(com.sancak2.client.M2WebBrowser p0)
    {
        return p0.mActivity;
    }

    static bridge synthetic void -$$Nest$mopenExternally(com.sancak2.client.M2WebBrowser p0, String p1)
    {
        p0.openExternally(p1);
        return;
    }

    static bridge synthetic boolean -$$Nest$smisInBrowserScheme(android.net.Uri p0)
    {
        return com.sancak2.client.M2WebBrowser.isInBrowserScheme(p0);
    }

    M2WebBrowser(com.sancak2.client.Sancak2Activity p1)
    {
        this.mActivity = p1;
        return;
    }

    private android.webkit.WebView createWebView()
    {
        android.webkit.WebView v0_1 = new android.webkit.WebView(this.mActivity);
        com.sancak2.client.M2WebBrowser$$ExternalSyntheticLambda2 v1_10 = v0_1.getSettings();
        v1_10.setJavaScriptEnabled(1);
        v1_10.setDomStorageEnabled(1);
        v1_10.setSupportMultipleWindows(1);
        v1_10.setJavaScriptCanOpenWindowsAutomatically(1);
        v1_10.setBuiltInZoomControls(0);
        v1_10.setDisplayZoomControls(0);
        v1_10.setUseWideViewPort(0);
        v1_10.setLoadWithOverviewMode(0);
        v1_10.setMixedContentMode(2);
        android.webkit.CookieManager.getInstance().setAcceptCookie(1);
        v0_1.setLongClickable(0);
        v0_1.setHapticFeedbackEnabled(0);
        v0_1.setOnLongClickListener(new com.sancak2.client.M2WebBrowser$$ExternalSyntheticLambda1());
        v0_1.setWebViewClient(new com.sancak2.client.M2WebBrowser$1(this));
        v0_1.setWebChromeClient(new com.sancak2.client.M2WebBrowser$2(this));
        v0_1.setDownloadListener(new com.sancak2.client.M2WebBrowser$$ExternalSyntheticLambda2(this));
        return v0_1;
    }

    private static String decodeAnsi(byte[] p5, int p6)
    {
        String[] v1 = new String[3];
        int v3_1 = 0;
        v1[0] = new StringBuilder("windows-").append(p6).toString();
        v1[1] = new StringBuilder("cp").append(p6).toString();
        v1[2] = new StringBuilder("x-windows-").append(p6).toString();
        while (v3_1 < 3) {
            java.nio.charset.Charset v6_5 = v1[v3_1];
            try {
                if (!java.nio.charset.Charset.isSupported(v6_5)) {
                    v3_1++;
                } else {
                    return new String(p5, java.nio.charset.Charset.forName(v6_5));
                }
            } catch (RuntimeException) {
            }
        }
        return new String(p5, java.nio.charset.Charset.forName("ISO-8859-1"));
    }

    private int[] gameViewport()
    {
        int[] v0_5 = this.mActivity.getGamePresentationRect();
        if ((v0_5 == null) || ((v0_5[2] <= 0) || (v0_5[3] <= 0))) {
            int[] v0_3 = this.mActivity.getWindow().getDecorView();
            return new int[] {0, 0, v0_3.getWidth(), v0_3.getHeight()});
        } else {
            return v0_5;
        }
    }

    private void hideOnUiThread()
    {
        android.webkit.WebView v0_0 = this.mPopup;
        if (v0_0 != null) {
            v0_0.dismissFromGame();
            this.mPopup = 0;
        }
        android.webkit.WebView v0_1 = this.mWebView;
        if (v0_1 != null) {
            v0_1.stopLoading();
            this.mWebView.destroy();
            this.mWebView = 0;
        }
        return;
    }

    private static boolean isInBrowserScheme(android.net.Uri p4)
    {
        boolean v4_1 = p4.getScheme();
        if (v4_1) {
            boolean v4_8 = v4_1.toLowerCase(java.util.Locale.ROOT);
            v4_8.hashCode();
            int v3 = -1;
            switch (v4_8.hashCode()) {
                case 3076010:
                    if (v4_8.equals("data")) {
                        v3 = 0;
                    } else {
                    }
                    break;
                case 3143036:
                    if (v4_8.equals("file")) {
                        v3 = 1;
                    } else {
                    }
                    break;
                case 3213448:
                    if (v4_8.equals("http")) {
                        v3 = 2;
                    } else {
                    }
                    break;
                case 92611469:
                    if (v4_8.equals("about")) {
                        v3 = 3;
                    } else {
                    }
                    break;
                case 99617003:
                    if (v4_8.equals("https")) {
                        v3 = 4;
                    } else {
                    }
                    break;
                case 188995949:
                    if (v4_8.equals("javascript")) {
                        v3 = 5;
                    } else {
                    }
                    break;
                default:
            }
            switch (v3) {
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                    return 1;
                default:
                    return 0;
            }
        } else {
            return 1;
        }
    }

    static synthetic boolean lambda$createWebView$2(android.view.View p0)
    {
        return 1;
    }

    private synthetic void lambda$createWebView$3(String p1, String p2, String p3, String p4, long p5)
    {
        this.openExternally(p1);
        return;
    }

    private synthetic void lambda$move$1(int p1, int p2, int p3, int p4, int p5, int p6)
    {
        this.moveOnUiThread(p1, p2, p3, p4, p5, p6);
        return;
    }

    private synthetic void lambda$show$0(byte[] p1, int p2, int p3, int p4, int p5, int p6, int p7, int p8, int p9)
    {
        this.showOnUiThread(p1, p2, p3, p4, p5, p6, p7, p8, p9);
        return;
    }

    private int[] mapRect(int p5, int p6, int p7, int p8, int p9, int p10)
    {
        float v2_0;
        int v0_0 = this.gameViewport();
        float v1 = 1065353216;
        if (p9 <= 0) {
            v2_0 = 1065353216;
        } else {
            float v2_2 = v0_0[2];
            if (v2_2 <= 0) {
            } else {
                v2_0 = (((float) v2_2) / ((float) p9));
            }
        }
        if (p10 > 0) {
            float v9_2 = v0_0[3];
            if (v9_2 > 0) {
                v1 = (((float) v9_2) / ((float) p10));
            }
        }
        return new int[] {(v0_0[0] + Math.round((((float) p5) * v2_0))), (v0_0[1] + Math.round((((float) p6) * v1))), Math.max(0, Math.round((((float) (p7 - p5)) * v2_0))), Math.max(0, Math.round((((float) (p8 - p6)) * v1)))});
    }

    private void moveOnUiThread(int p2, int p3, int p4, int p5, int p6, int p7)
    {
        if (this.mPopup != null) {
            int v2_2 = this.mapRect(p2, p3, p4, p5, p6, p7);
            this.mPopup.update(v2_2[0], v2_2[1], v2_2[2], v2_2[3]);
            return;
        } else {
            return;
        }
    }

    private static native void nativeOnShowFailed(int p0);

    private void openExternally(String p4)
    {
        try {
            android.content.ActivityNotFoundException v0_1 = new android.content.Intent("android.intent.action.VIEW", android.net.Uri.parse(p4));
            v0_1.addFlags(268435456);
            this.mActivity.startActivity(v0_1);
        } catch (android.content.ActivityNotFoundException v0_2) {
            android.util.Log.w("sancak2-web", new StringBuilder("harici acilamadi: ").append(p4).toString(), v0_2);
        }
        return;
    }

    private void showOnUiThread(byte[] p11, int p12, int p13, int p14, int p15, int p16, int p17, int p18, int p19)
    {
        this.hideOnUiThread();
        try {
            int v3_3;
            android.view.View v9 = this.mActivity.getWindow().getDecorView();
            String v1_0 = this.mapRect(p13, p14, p15, p16, p17, p18);
            String v2_0 = this.createWebView();
            this.mWebView = v2_0;
            int[] vtmp5 = this.gameViewport();
        } catch (String v0_8) {
            android.util.Log.e("sancak2-web", "web tarayici olusturulamadi", v0_8);
            this.hideOnUiThread();
            com.sancak2.client.M2WebBrowser.nativeOnShowFailed(p19);
            return;
        }
        if (p17 <= 0) {
            v3_3 = 1065353216;
        } else {
            int v3_2 = vtmp5[2];
            if (v3_2 <= 0) {
            } else {
                v3_3 = (((float) v3_2) / ((float) p17));
            }
        }
        v2_0.setInitialScale(Math.max(1, Math.round((v3_3 * 1120403456))));
        String v0_6 = new com.sancak2.client.M2WebBrowser$GamePopup(v2_0, v1_0[2], v1_0[3]);
        this.mPopup = v0_6;
        v0_6.setClippingEnabled(0);
        v0_6.setOutsideTouchable(0);
        v0_6.setTouchable(1);
        v0_6.setInputMethodMode(1);
        v0_6.setFocusable(0);
        v2_0.setSystemUiVisibility(v9.getSystemUiVisibility());
        v0_6.showAtLocation(v9, 8388659, v1_0[0], v1_0[1]);
        v0_6.setFocusable(1);
        v0_6.update();
        String v0_7 = com.sancak2.client.M2WebBrowser.decodeAnsi(p11, p12);
        if (android.net.Uri.parse(v0_7).getScheme() == null) {
            v0_7 = android.webkit.URLUtil.guessUrl(v0_7);
        }
        v2_0.loadUrl(v0_7);
        v2_0.requestFocus();
        return;
    }

    void destroy()
    {
        this.hideOnUiThread();
        return;
    }

    void hide()
    {
        this.mActivity.runOnUiThread(new com.sancak2.client.M2WebBrowser$$ExternalSyntheticLambda0(this));
        return;
    }

    void move(int p12, int p13, int p14, int p15, int p16, int p17)
    {
        com.sancak2.client.Sancak2Activity v9 = this.mActivity;
        com.sancak2.client.M2WebBrowser$$ExternalSyntheticLambda3 v10 = new com.sancak2.client.M2WebBrowser$$ExternalSyntheticLambda3;
        v10(this, p12, p13, p14, p15, p16, p17);
        v9.runOnUiThread(v10);
        return;
    }

    void show(byte[] p15, int p16, int p17, int p18, int p19, int p20, int p21, int p22, int p23)
    {
        com.sancak2.client.Sancak2Activity v12 = this.mActivity;
        com.sancak2.client.M2WebBrowser$$ExternalSyntheticLambda4 v13 = new com.sancak2.client.M2WebBrowser$$ExternalSyntheticLambda4;
        v13(this, p15, p16, p17, p18, p19, p20, p21, p22, p23);
        v12.runOnUiThread(v13);
        return;
    }
}
