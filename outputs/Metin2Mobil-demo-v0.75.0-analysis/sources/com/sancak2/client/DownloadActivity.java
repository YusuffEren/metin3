package com.sancak2.client;
public class DownloadActivity extends android.app.Activity {
    private static final String APK_VERSION_FILE = "apk/version.json";
    private static final int CONNECT_TIMEOUT_MS = 8000;
    private static final String DEFAULT_BASE_URL = "http://185.169.55.31/averos2/";
    private static final String LOCAL_MANIFEST = "bundle_manifest.json";
    private static final int READ_TIMEOUT_MS = 20000;
    private static final String TAG = "m2download";
    private static final String URL_OVERRIDE = "bundle_url.txt";
    private android.widget.ProgressBar mBar;
    private volatile boolean mCancelled;
    private android.widget.TextView mDetail;
    private volatile java.io.File mPendingApk;
    private android.widget.Button mRetry;
    private android.widget.TextView mStatus;
    private final android.os.Handler mUi;

    static bridge synthetic android.widget.ProgressBar -$$Nest$fgetmBar(com.sancak2.client.DownloadActivity p0)
    {
        return p0.mBar;
    }

    static bridge synthetic android.widget.TextView -$$Nest$fgetmDetail(com.sancak2.client.DownloadActivity p0)
    {
        return p0.mDetail;
    }

    static bridge synthetic java.io.File -$$Nest$fgetmPendingApk(com.sancak2.client.DownloadActivity p0)
    {
        return p0.mPendingApk;
    }

    static bridge synthetic android.widget.Button -$$Nest$fgetmRetry(com.sancak2.client.DownloadActivity p0)
    {
        return p0.mRetry;
    }

    static bridge synthetic android.widget.TextView -$$Nest$fgetmStatus(com.sancak2.client.DownloadActivity p0)
    {
        return p0.mStatus;
    }

    static bridge synthetic void -$$Nest$mstartInstall(com.sancak2.client.DownloadActivity p0)
    {
        p0.startInstall();
        return;
    }

    static bridge synthetic void -$$Nest$mstartWork(com.sancak2.client.DownloadActivity p0)
    {
        p0.startWork();
        return;
    }

    static bridge synthetic void -$$Nest$mwork(com.sancak2.client.DownloadActivity p0)
    {
        p0.work();
        return;
    }

    public DownloadActivity()
    {
        this.mUi = new android.os.Handler(android.os.Looper.getMainLooper());
        this.mCancelled = 0;
        this.mPendingApk = 0;
        return;
    }

    private void animateFooter(android.view.View p9)
    {
        p9.setAlpha(0);
        android.animation.AnimatorSet v3_6 = new float[2];
        v3_6 = {0, 1065353216};
        android.animation.ObjectAnimator v1_1 = android.animation.ObjectAnimator.ofFloat(p9, android.view.View.ALPHA, v3_6);
        v1_1.setDuration(1200);
        v1_1.setStartDelay(400);
        v1_1.setInterpolator(new android.view.animation.DecelerateInterpolator());
        android.animation.AnimatorSet v3_3 = new android.animation.PropertyValuesHolder[2];
        int v5_0 = new float[2];
        v5_0 = {1065353216, 1055286886};
        v3_3[0] = android.animation.PropertyValuesHolder.ofFloat(android.view.View.ALPHA, v5_0);
        float v6_2 = ((float) this.dp(1077936128));
        float[] v7 = new float[2];
        v7[0] = 0;
        v7[1] = v6_2;
        v3_3[1] = android.animation.PropertyValuesHolder.ofFloat(android.view.View.TRANSLATION_Y, v7);
        android.animation.ObjectAnimator v9_1 = android.animation.ObjectAnimator.ofPropertyValuesHolder(p9, v3_3);
        v9_1.setDuration(1300);
        v9_1.setRepeatCount(-1);
        v9_1.setRepeatMode(2);
        v9_1.setInterpolator(new android.view.animation.AccelerateDecelerateInterpolator());
        android.animation.AnimatorSet v3_10 = new android.animation.AnimatorSet();
        android.animation.Animator[] v2_1 = new android.animation.Animator[2];
        v2_1[0] = v1_1;
        v2_1[1] = v9_1;
        v3_10.playSequentially(v2_1);
        v3_10.start();
        return;
    }

    private void animateLogo(android.view.View p10)
    {
        p10.setAlpha(0);
        p10.setScaleX(1064011039);
        p10.setScaleY(1064011039);
        android.animation.ObjectAnimator v2_1 = new android.animation.PropertyValuesHolder[3];
        int v5_1 = new float[2];
        v5_1 = {0, 1065353216};
        v2_1[0] = android.animation.PropertyValuesHolder.ofFloat(android.view.View.ALPHA, v5_1);
        int v6_0 = new float[2];
        v6_0 = {1064011039, 1065353216};
        v2_1[1] = android.animation.PropertyValuesHolder.ofFloat(android.view.View.SCALE_X, v6_0);
        float v7_0 = new float[2];
        v7_0 = {1064011039, 1065353216};
        v2_1[2] = android.animation.PropertyValuesHolder.ofFloat(android.view.View.SCALE_Y, v7_0);
        android.animation.ObjectAnimator v2_0 = android.animation.ObjectAnimator.ofPropertyValuesHolder(p10, v2_1);
        v2_0.setDuration(900);
        v2_0.setInterpolator(new android.view.animation.DecelerateInterpolator());
        android.animation.Animator[] v1_1 = new android.animation.PropertyValuesHolder[3];
        float v7_2 = new float[2];
        v7_2 = {1065353216, 1065688760};
        v1_1[0] = android.animation.PropertyValuesHolder.ofFloat(android.view.View.SCALE_X, v7_2);
        float v7_3 = new float[2];
        v7_3 = {1065353216, 1065688760};
        v1_1[1] = android.animation.PropertyValuesHolder.ofFloat(android.view.View.SCALE_Y, v7_3);
        float v7_7 = ((float) (- this.dp(1086324736)));
        float[] v8 = new float[2];
        v8[0] = 0;
        v8[1] = v7_7;
        v1_1[2] = android.animation.PropertyValuesHolder.ofFloat(android.view.View.TRANSLATION_Y, v8);
        android.animation.ObjectAnimator v10_1 = android.animation.ObjectAnimator.ofPropertyValuesHolder(p10, v1_1);
        v10_1.setDuration(1900);
        v10_1.setRepeatCount(-1);
        v10_1.setRepeatMode(2);
        v10_1.setInterpolator(new android.view.animation.AccelerateDecelerateInterpolator());
        android.animation.AnimatorSet v0_7 = new android.animation.AnimatorSet();
        android.animation.Animator[] v1_3 = new android.animation.Animator[2];
        v1_3[0] = v2_0;
        v1_3[1] = v10_1;
        v0_7.playSequentially(v1_3);
        v0_7.start();
        return;
    }

    private String baseUrl()
    {
        String v0_8 = new java.io.File(this.dataDir(), "bundle_url.txt");
        if (v0_8.exists()) {
            String v0_2 = new String(com.sancak2.client.DownloadActivity.readAll(new java.io.FileInputStream(v0_8)), java.nio.charset.StandardCharsets.UTF_8).trim();
        }
        try {
            String v0_7 = this.getString(com.sancak2.client.R$string.m2_base_url).trim();
        } catch (Exception) {
            return "http://185.169.55.31/averos2/";
        }
        if (v0_7.length() <= 0) {
            return "http://185.169.55.31/averos2/";
        } else {
            if (!v0_7.endsWith("/")) {
                v0_7 = new StringBuilder().append(v0_7).append("/").toString();
            } else {
            }
            return v0_7;
        }
        return v0_2;
    }

    private android.view.View buildUi()
    {
        android.widget.LinearLayout v0_1 = new android.widget.LinearLayout(this);
        v0_1.setOrientation(1);
        v0_1.setGravity(17);
        v0_1.setBackground(new android.graphics.drawable.GradientDrawable(android.graphics.drawable.GradientDrawable$Orientation.TOP_BOTTOM, new int[] {-12971512, -14939642, -16251644})));
        v0_1.setPadding(this.dp(1107296256), this.dp(1098907648), this.dp(1107296256), this.dp(1098907648));
        int v3_26 = new android.widget.ImageView(this);
        v3_26.setImageResource(com.sancak2.client.R$drawable.download_logo);
        v3_26.setAdjustViewBounds(1);
        v3_26.setScaleType(android.widget.ImageView$ScaleType.FIT_CENTER);
        int v6_15 = new android.widget.LinearLayout$LayoutParams(Math.min(((int) (((float) this.getResources().getDisplayMetrics().widthPixels) * 1055286886)), this.dp(1140981760)), -2);
        v6_15.gravity = 1;
        v6_15.bottomMargin = this.dp(1094713344);
        v0_1.addView(v3_26, v6_15);
        this.animateLogo(v3_26);
        int v3_28 = new android.widget.TextView(this);
        this.mStatus = v3_28;
        v3_28.setTextColor(-2858);
        this.mStatus.setTextSize(2, 1101004800);
        this.mStatus.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        this.mStatus.setGravity(17);
        this.mStatus.setText("Averos2 haz\u0131rlan\u0131yor...");
        v0_1.addView(this.mStatus, this.wrap());
        int v3_36 = new android.widget.ProgressBar(this, 0, 16842872);
        this.mBar = v3_36;
        v3_36.setMax(1000);
        this.mBar.setProgress(0);
        this.mBar.setIndeterminate(1);
        int v3_40 = new android.widget.LinearLayout$LayoutParams(this.dp(1137836032), this.dp(1096810496));
        v3_40.gravity = 1;
        v3_40.topMargin = this.dp(1096810496);
        v0_1.addView(this.mBar, v3_40);
        this.mBar.setProgressTintList(android.content.res.ColorStateList.valueOf(-2056144));
        this.mBar.setProgressBackgroundTintList(android.content.res.ColorStateList.valueOf(-2143281136));
        this.mBar.setIndeterminateTintList(android.content.res.ColorStateList.valueOf(-2056144));
        int v3_4 = new android.widget.TextView(this);
        this.mDetail = v3_4;
        v3_4.setTextColor(-1917320);
        this.mDetail.setTextSize(2, 1096810496);
        this.mDetail.setGravity(17);
        this.mDetail.setText("Sunucuya ba\u011flan\u0131l\u0131yor...");
        int v3_9 = this.wrap();
        v3_9.topMargin = this.dp(1090519040);
        v0_1.addView(this.mDetail, v3_9);
        int v3_11 = new android.widget.Button(this);
        this.mRetry = v3_11;
        v3_11.setText("Tekrar Dene");
        this.mRetry.setTextColor(-2858);
        int v3_14 = new android.graphics.drawable.GradientDrawable();
        v3_14.setColor(-10868212);
        v3_14.setCornerRadius(((float) this.dp(1090519040)));
        v3_14.setStroke(this.dp(1065353216), -4158928);
        this.mRetry.setBackground(v3_14);
        this.mRetry.setVisibility(8);
        this.mRetry.setOnClickListener(new com.sancak2.client.DownloadActivity$1(this));
        int v3_19 = new android.widget.LinearLayout$LayoutParams(this.dp(1128792064), this.dp(1111490560));
        v3_19.gravity = 1;
        v3_19.topMargin = this.dp(1098907648);
        v0_1.addView(this.mRetry, v3_19);
        android.widget.TextView v1_3 = new android.widget.TextView(this);
        v1_3.setTextColor(-4681640);
        v1_3.setTextSize(2, 1095761920);
        v1_3.setGravity(17);
        v1_3.setText("Mobilserverler.com g\u00fcvencesi ile...");
        android.widget.LinearLayout$LayoutParams v2_1 = this.wrap();
        v2_1.topMargin = this.dp(1105199104);
        v0_1.addView(v1_3, v2_1);
        this.animateFooter(v1_3);
        return v0_1;
    }

    private boolean checkApkUpdate(String p26)
    {
        void v1 = this;
        String v3_9 = ")";
        String v7 = "G\u00fcncelleme indiriliyor... (s\u00fcr\u00fcm ";
        if (this.getResources().getBoolean(com.sancak2.client.R$bool.m2_self_update)) {
            try {
                boolean v8_13 = ((java.net.HttpURLConnection) new java.net.URL(new StringBuilder().append(p26).append("apk/version.json").toString()).openConnection());
                v8_13.setConnectTimeout(8000);
                v8_13.setReadTimeout(20000);
                v8_13.setUseCaches(0);
                v8_13.setRequestProperty("Cache-Control", "no-cache");
            } catch (Exception v0_26) {
                android.util.Log.w("m2download", new StringBuilder("apk surum bilgisi alinamadi: ").append(v0_26).toString());
                return 0;
            }
            if (v8_13.getResponseCode() == 200) {
                boolean v12_9 = new org.json.JSONObject(new String(com.sancak2.client.DownloadActivity.readAll(v8_13.getInputStream()), java.nio.charset.StandardCharsets.UTF_8));
                try {
                    boolean v8_19 = v12_9.getInt("versionCode");
                    String v14_3 = v12_9.getString("url");
                    String v15_2 = v12_9.getString("sha1");
                    long v10_6 = v12_9.getLong("size");
                    try {
                        String v9_3 = v12_9.optString("versionName", String.valueOf(v8_19));
                        boolean v12_10 = this.installedVersionCode();
                    } catch (Exception) {
                        String v2_14 = 0;
                        return v2_14;
                    }
                    if (v8_19 > v12_10) {
                        Exception v0_1;
                        android.util.Log.i("m2download", new StringBuilder("apk guncelleme: kurulu ").append(v12_10).append(" -> sunucu ").append(v8_19).toString());
                        java.io.BufferedInputStream v5_20 = new java.io.File(this.dataDir(), "apk");
                        v5_20.mkdirs();
                        boolean v8_14 = new java.io.File(v5_20, "update.apk");
                        if ((v8_14.exists()) && ((v8_14.length() == v10_6) && (v15_2.equalsIgnoreCase(com.sancak2.client.DownloadActivity.sha1Of(v8_14))))) {
                            v0_1 = v8_14;
                        } else {
                            boolean v12_5 = new java.io.File(v5_20, "update.apk.part");
                            try {
                                String v18;
                                v1 = this.post(new StringBuilder("G\u00fcncelleme indiriliyor... (s\u00fcr\u00fcm ").append(v9_3).append(")").toString(), new StringBuilder("0 / ").append(com.sancak2.client.DownloadActivity.fmtMb(v10_6)).append(" MB").toString(), 0);
                                Exception v0_6 = ((java.net.HttpURLConnection) new java.net.URL(new StringBuilder().append(p26).append(v14_3).toString()).openConnection());
                                v0_6.setConnectTimeout(8000);
                                v0_6.setReadTimeout(20000);
                                v0_6.setUseCaches(0);
                                try {
                                    if (v0_6.getResponseCode() != 200) {
                                        v18 = "m2download";
                                        throw new Exception(new StringBuilder("HTTP ").append(v0_6.getResponseCode()).toString());
                                    } else {
                                        java.io.BufferedInputStream v5_12 = new java.io.BufferedInputStream(v0_6.getInputStream(), 65536);
                                        Exception v0_13 = new java.io.FileOutputStream(v12_5, 0);
                                        long v6_8 = new byte[65536];
                                        long v13_5 = 0;
                                        v18 = "m2download";
                                        long v16 = 0;
                                        while(true) {
                                            int v4_1 = v5_12.read(v6_8);
                                            if (v4_1 <= 0) {
                                                break;
                                            }
                                            boolean v20_1 = v8_14;
                                            if (!v1.mCancelled) {
                                                String v24;
                                                String v21_1;
                                                long v19_0;
                                                v0_13.write(v6_8, 0, v4_1);
                                                java.io.BufferedInputStream v26_2 = v5_12;
                                                v13_5 += ((long) v4_1);
                                                int v4_3 = System.currentTimeMillis();
                                                if ((v4_3 - v16) <= 200) {
                                                    v21_1 = v3_9;
                                                    v19_0 = v6_8;
                                                    v24 = v7;
                                                } else {
                                                    v21_1 = v3_9;
                                                    long v22 = v4_3;
                                                    v19_0 = v6_8;
                                                    v24 = v7;
                                                    v1 = v1.post(new StringBuilder().append(v7).append(v9_3).append(v3_9).toString(), new StringBuilder().append(com.sancak2.client.DownloadActivity.fmtMb(v13_5)).append(" / ").append(com.sancak2.client.DownloadActivity.fmtMb(v10_6)).append(" MB").toString(), ((int) ((100 * v13_5) / Math.max(1, v10_6))));
                                                    v16 = v22;
                                                }
                                                v5_12 = v26_2;
                                                v6_8 = v19_0;
                                                v8_14 = v20_1;
                                                v3_9 = v21_1;
                                                v7 = v24;
                                            } else {
                                                try {
                                                    v0_13.close();
                                                    v5_12.close();
                                                    v12_5.delete();
                                                    return 0;
                                                } catch (Exception v0_7) {
                                                    android.util.Log.w(v18, new StringBuilder("apk guncelleme indirilemedi: ").append(v0_7).toString());
                                                    v12_5.delete();
                                                    return 0;
                                                }
                                            }
                                        }
                                        java.io.BufferedInputStream v26_1 = v5_12;
                                        boolean v20_0 = v8_14;
                                        v0_13.close();
                                        v26_1.close();
                                        if ((v12_5.length() != v10_6) || (!v15_2.equalsIgnoreCase(com.sancak2.client.DownloadActivity.sha1Of(v12_5)))) {
                                            v12_5.delete();
                                            throw new Exception("sha1 uyusmuyor");
                                        } else {
                                            if (v20_0.exists()) {
                                                v20_0.delete();
                                            }
                                            v0_1 = v20_0;
                                            if (!v12_5.renameTo(v0_1)) {
                                                throw new Exception("dosya tasinamadi");
                                            }
                                        }
                                    }
                                } catch (Exception v0_7) {
                                }
                            } catch (Exception v0_7) {
                                v18 = "m2download";
                            }
                        }
                        v1.mPendingApk = v0_1;
                        v1.mUi.post(new com.sancak2.client.DownloadActivity$3(v1));
                        return 1;
                    } else {
                        return 0;
                    }
                } catch (Exception) {
                    v2_14 = 0;
                    return v2_14;
                }
            } else {
                return 0;
            }
        } else {
            return 0;
        }
    }

    private java.io.File dataDir()
    {
        java.io.File v0_1 = this.getExternalFilesDir(0);
        if (v0_1 == null) {
            v0_1 = this.getFilesDir();
        }
        return v0_1;
    }

    private int dp(float p3)
    {
        return ((int) android.util.TypedValue.applyDimension(1, p3, this.getResources().getDisplayMetrics()));
    }

    private static String encodePath(String p7)
    {
        StringBuilder v0_1 = new StringBuilder();
        String v7_1 = p7.split("/");
        int v1_1 = v7_1.length;
        int v2 = 0;
        while (v2 < v1_1) {
            String v3 = v7_1[v2];
            if (v0_1.length() > 0) {
                v0_1.append(47);
            }
            try {
                v0_1.append(java.net.URLEncoder.encode(v3, "UTF-8").replace("+", "%20"));
            } catch (Exception) {
                v0_1.append(v3);
            }
            v2++;
        }
        return v0_1.toString();
    }

    private void fail(String p3, String p4)
    {
        this.mUi.post(new com.sancak2.client.DownloadActivity$6(this, p3, p4));
        return;
    }

    private static String fmtMb(long p3)
    {
        return String.format(java.util.Locale.US, "%.1f", new Object[] {Double.valueOf((((double) p3) / 4697254411347427328))}));
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

    private int installedVersionCode()
    {
        try {
        } catch (Exception) {
        }
        return this.getPackageManager().getPackageInfo(this.getPackageName(), 0).versionCode;
    }

    private static boolean isUserSettingsFile(String p2)
    {
        boolean v2_1 = p2.toLowerCase();
        int v1 = 0;
        if (!v2_1.contains("/")) {
            if ((v2_1.endsWith(".cfg")) || ((v2_1.endsWith(".inf")) || (v2_1.equals("mobile_layout.json")))) {
                v1 = 1;
            }
            return v1;
        } else {
            return 0;
        }
    }

    private void launchGame()
    {
        this.mUi.postDelayed(new com.sancak2.client.DownloadActivity$7(this), 400);
        return;
    }

    private void post(String p2, String p3)
    {
        this.post(p2, p3, -1);
        return;
    }

    private void post(String p3, String p4, int p5)
    {
        this.mUi.post(new com.sancak2.client.DownloadActivity$5(this, p3, p4, p5));
        return;
    }

    private static byte[] readAll(java.io.InputStream p4)
    {
        try {
            byte[] v0_1 = new java.io.ByteArrayOutputStream();
            byte[] v1_1 = new byte[65536];
        } catch (byte[] v0_2) {
            p4.close();
            throw v0_2;
        }
        while(true) {
            int v2 = p4.read(v1_1);
            if (v2 <= 0) {
                break;
            }
            v0_1.write(v1_1, 0, v2);
        }
        byte[] v0_3 = v0_1.toByteArray();
        p4.close();
        return v0_3;
    }

    private static String sha1Of(java.io.File p5)
    {
        try {
            byte[] v0_1 = java.security.MessageDigest.getInstance("SHA-1");
            int v1_2 = new java.io.BufferedInputStream(new java.io.FileInputStream(p5), 65536);
        } catch (Exception) {
            return "";
        }
        String v5_7 = new byte[65536];
        while(true) {
            String v2_0 = v1_2.read(v5_7);
            int v3 = 0;
            if (v2_0 <= null) {
                break;
            }
            v0_1.update(v5_7, 0, v2_0);
        }
        v1_2.close();
        String v5_3 = new StringBuilder();
        byte[] v0_2 = v0_1.digest();
        int v1_0 = v0_2.length;
        while (v3 < v1_0) {
            v5_3.append(String.format("%02x", new Object[] {Byte.valueOf(v0_2[v3])})));
            v3++;
        }
        return v5_3.toString();
    }

    private void startInstall()
    {
        StringBuilder v1_0 = this.mPendingApk;
        if ((v1_0 != null) && (v1_0.exists())) {
            if (this.getPackageManager().canRequestPackageInstalls()) {
                try {
                    String v0_2 = new android.content.Intent("android.intent.action.VIEW");
                    v0_2.setDataAndType(com.sancak2.client.ApkProvider.uri(this), "application/vnd.android.package-archive");
                    v0_2.addFlags(268435457);
                    this.mStatus.setText("G\u00fcncelleme kuruluyor...");
                    this.mDetail.setText("Kurulum bitince oyunu yeniden a\u00e7\u0131n.");
                    this.mBar.setIndeterminate(0);
                    this.mRetry.setText("Kur");
                    this.mRetry.setVisibility(0);
                    this.startActivity(v0_2);
                } catch (String v0_3) {
                    android.util.Log.w("m2download", new StringBuilder("kurucu acilamadi: ").append(v0_3).toString());
                    this.fail("G\u00fcncelleme kurulamad\u0131", v0_3.toString());
                }
            } else {
                this.mStatus.setText("G\u00fcncelleme haz\u0131r");
                this.mDetail.setText("Kurulum i\u00e7in \'Bu kaynaktan izin ver\' se\u00e7ene\u011fini a\u00e7\u0131p geri d\u00f6n\u00fcn.");
                this.mBar.setIndeterminate(0);
                this.mRetry.setText("Kur");
                this.mRetry.setVisibility(0);
                try {
                    this.startActivity(new android.content.Intent("android.settings.MANAGE_UNKNOWN_APP_SOURCES", android.net.Uri.parse(new StringBuilder("package:").append(this.getPackageName()).toString())));
                } catch (String v0_9) {
                    android.util.Log.w("m2download", new StringBuilder("izin sayfasi acilamadi: ").append(v0_9).toString());
                }
                return;
            }
        }
        return;
    }

    private void startWork()
    {
        this.mCancelled = 0;
        this.mRetry.setText("Tekrar Dene");
        this.mRetry.setVisibility(8);
        this.mBar.setIndeterminate(1);
        this.mStatus.setText("Averos2 haz\u0131rlan\u0131yor...");
        this.mDetail.setText("Sunucuya ba\u011flan\u0131l\u0131yor...");
        new Thread(new com.sancak2.client.DownloadActivity$2(this), "m2download").start();
        return;
    }

    private void work()
    {
        int v3_3 = "sha1";
        String v4_1 = "path";
        int v5_3 = "m2download";
        String v6_0 = "HTTP ";
        String v7_1 = this.dataDir();
        long v8_1 = this.baseUrl();
        if (!this.checkApkUpdate(v8_1)) {
            try {
                String v14_4;
                String v0_35 = ((java.net.HttpURLConnection) new java.net.URL(new StringBuilder().append(v8_1).append("manifest.json").toString()).openConnection());
                v0_35.setConnectTimeout(8000);
                v0_35.setReadTimeout(20000);
                v0_35.setUseCaches(0);
                v0_35.setRequestProperty("Cache-Control", "no-cache");
            } catch (String v0_62) {
                android.util.Log.w("m2download", new StringBuilder("manifest alinamadi: ").append(v0_62).toString());
                v14_4 = 0;
                StringBuilder v13_1 = new java.io.File(v7_1, "bundle_manifest.json");
                boolean v15_5 = "";
                if (v14_4 != null) {
                    long v12_1 = new java.util.HashMap();
                    try {
                        if (v13_1.exists()) {
                            String v0_82 = new org.json.JSONObject(new String(com.sancak2.client.DownloadActivity.readAll(new java.io.FileInputStream(v13_1)), java.nio.charset.StandardCharsets.UTF_8)).getJSONArray("files");
                            int v9_12 = 0;
                            while (v9_12 < v0_82.length()) {
                                int v10_19 = v0_82.getJSONObject(v9_12);
                                v12_1.put(v10_19.getString("path"), v10_19.getString("sha1"));
                                v9_12++;
                            }
                        }
                    } catch (String v0_83) {
                        android.util.Log.w("m2download", new StringBuilder("yerel manifest okunamadi: ").append(v0_83).toString());
                    }
                    int v9_1 = new java.util.ArrayList();
                    try {
                        String v0_2 = v14_4.getJSONArray("files");
                        void v1_1 = this.post("Dosyalar kontrol ediliyor...", new StringBuilder().append(v0_2.length()).append(" dosya").toString());
                        String v2_2 = 0;
                        long v18_0 = 0;
                    } catch (String v0_69) {
                        v1_1.fail("Dosya listesi okunamad\u0131", v0_69.toString());
                        return;
                    }
                    while(true) {
                        int v11_2 = "size";
                        String v22 = v15_5;
                        boolean v23 = 1;
                        if (v2_2 >= v0_2.length()) {
                            break;
                        }
                        int v10_16 = v0_2.getJSONObject(v2_2);
                        StringBuilder v24_1 = v0_2;
                        String v0_68 = v10_16.getString("path");
                        long v25_1 = v5_3;
                        if (v0_68.contains("..")) {
                        } else {
                            if (!v0_68.startsWith("/")) {
                                int v26_3 = v10_16.getLong("size");
                                int v5_7 = v10_16.getString("sha1");
                                int v11_19 = new java.io.File(v7_1, v0_68);
                                if ((!com.sancak2.client.DownloadActivity.isUserSettingsFile(v0_68)) || ((!v11_19.exists()) || (v11_19.length() <= 0))) {
                                    if ((!v11_19.exists()) || ((v11_19.length() != v26_3) || (!v5_7.equals(v12_1.get(v0_68))))) {
                                        v23 = 0;
                                    } else {
                                    }
                                    if ((!v23) && ((v11_19.exists()) && ((v11_19.length() == v26_3) && (!v12_1.containsKey(v0_68))))) {
                                        v23 = v5_7.equalsIgnoreCase(com.sancak2.client.DownloadActivity.sha1Of(v11_19));
                                        if (v23) {
                                            v12_1.put(v0_68, v5_7);
                                        }
                                    }
                                    if (v23) {
                                    } else {
                                        v9_1.add(v10_16);
                                        v18_0 += v26_3;
                                    }
                                } else {
                                }
                            } else {
                            }
                        }
                        v2_2++;
                        v15_5 = v22;
                        v0_2 = v24_1;
                        v5_3 = v25_1;
                    }
                    long v25_0 = v5_3;
                    long v30_0 = v18_0;
                    String v2_3 = "Oyun ba\u015flat\u0131l\u0131yor...";
                    if (!v9_1.isEmpty()) {
                        long v18_1 = System.currentTimeMillis();
                        v1_1.mUi.post(new com.sancak2.client.DownloadActivity$4(v1_1));
                        int v5_2 = 0;
                        int v26_0 = 0;
                        long v28_0 = 0;
                        while (v5_2 < v9_1.size()) {
                            if (!v1_1.mCancelled) {
                                String v0_10 = ((org.json.JSONObject) v9_1.get(v5_2));
                                try {
                                    int v10_7 = v0_10.getString(v4_1);
                                    java.io.File v32 = v13_1;
                                    StringBuilder v24_0 = v14_4;
                                    try {
                                        StringBuilder v13_0 = v0_10.getLong(v11_2);
                                        String v33 = v4_1;
                                        try {
                                            String v4_0 = v0_10.getString(v3_3);
                                            long v34 = v3_3;
                                            int v3_2 = new java.io.File(v7_1, v10_7);
                                            java.io.File v35 = v11_2;
                                            int v36_1 = v2_3;
                                            v11_2 = new java.io.File(v7_1, new StringBuilder().append(v10_7).append(".part").toString());
                                            String v0_17 = v3_2.getParentFile();
                                        } catch (Exception) {
                                            v36_1 = ".part";
                                            v34 = v3_2;
                                            long v48_0 = v6_0;
                                            java.io.File v38 = v7_1;
                                            boolean v40_0 = v8_1;
                                            long v17_0 = v9_1;
                                            v35 = v11_2;
                                            int v10_8 = v12_1;
                                            long v8_0 = v25_0;
                                            int v3_4 = v30_0;
                                            v5_2++;
                                            v30_0 = v3_4;
                                            v25_0 = v8_0;
                                            v12_1 = v10_8;
                                            v9_1 = v17_0;
                                            v14_4 = v24_0;
                                            v13_1 = v32;
                                            v4_1 = v33;
                                            v3_3 = v34;
                                            v11_2 = v35;
                                            v2_3 = v36_1;
                                            v7_1 = v38;
                                            v8_1 = v40_0;
                                            v6_0 = v48_0;
                                        }
                                        if ((v0_17 == null) || ((v0_17.isDirectory()) || (v0_17.mkdirs()))) {
                                            v38 = v7_1;
                                            String v0_19 = v22;
                                            String v2_8 = 0;
                                            boolean v37 = 0;
                                            while ((v2_8 < 3) && (!v37)) {
                                                try {
                                                    String v39_1 = v0_19;
                                                    boolean v40_1 = v8_1;
                                                    try {
                                                        String v7_3 = ((java.net.HttpURLConnection) new java.net.URL(new StringBuilder().append(v8_1).append("data/").append(com.sancak2.client.DownloadActivity.encodePath(v10_7)).toString()).openConnection());
                                                        try {
                                                            long v17_1;
                                                            long v8_6;
                                                            v7_3.setConnectTimeout(8000);
                                                            v7_3.setReadTimeout(20000);
                                                            try {
                                                                if (!v11_2.exists()) {
                                                                    v17_1 = v9_1;
                                                                    v8_6 = 0;
                                                                } else {
                                                                    v17_1 = v9_1;
                                                                    v8_6 = v11_2.length();
                                                                }
                                                                try {
                                                                    if ((v8_6 <= 0) || (v8_6 >= v13_0)) {
                                                                        int v42 = v2_8;
                                                                        int v43 = v10_7;
                                                                        v8_6 = 0;
                                                                        long v8_7;
                                                                        int v10_12;
                                                                        String v0_40 = v7_3.getResponseCode();
                                                                        long v44 = v8_6;
                                                                        if (v0_40 != 206) {
                                                                            v8_7 = 200;
                                                                            v10_12 = 0;
                                                                        } else {
                                                                            v10_12 = 1;
                                                                            v8_7 = 200;
                                                                        }
                                                                        if ((v0_40 != v8_7) && (v0_40 != 206)) {
                                                                            throw new Exception(new StringBuilder().append(v6_0).append(v0_40).toString());
                                                                        } else {
                                                                            if (v10_12 == 0) {
                                                                                v44 = 0;
                                                                            }
                                                                            String v2_21 = new java.io.BufferedInputStream(v7_3.getInputStream(), 65536);
                                                                            long v8_9 = new java.io.FileOutputStream(v11_2, v10_12);
                                                                            String v0_44 = new byte[65536];
                                                                            try {
                                                                                while(true) {
                                                                                    long v46_0;
                                                                                    int v3_5;
                                                                                    long v48_1;
                                                                                    int v9_8 = v2_21.read(v0_44);
                                                                                    v11_2 = int v16_1;
                                                                                    v13_0 = long v30_3;
                                                                                    v7_3 = v46_0;
                                                                                    v12_1 = int v47_2;
                                                                                    v6_0 = v48_1;
                                                                                    v30_0 = v3_5;
                                                                                    v4_0 = String v51_1;
                                                                                    v3_2 = int v52_1;
                                                                                }
                                                                                int v52_0 = v3_2;
                                                                                String v51_0 = v4_0;
                                                                                v48_1 = v6_0;
                                                                                v46_0 = v7_3;
                                                                                int v16_0 = v11_2;
                                                                                int v47_0 = v12_1;
                                                                                v3_5 = v30_0;
                                                                                long v30_1 = v13_0;
                                                                                int v10_9;
                                                                                int v11_6;
                                                                                String v6_1;
                                                                                int v9_3;
                                                                                v8_9.close();
                                                                                v2_21.close();
                                                                                if (v16_0.length() != v30_1) {
                                                                                    v9_3 = v16_0;
                                                                                    v11_6 = v43;
                                                                                    v10_9 = v47_0;
                                                                                    v6_1 = v51_0;
                                                                                    v7_3 = v52_0;
                                                                                    v12_1 = v30_1;
                                                                                    throw new Exception(new StringBuilder().append("boyut uyusmuyor ").append(v9_3.length()).append("/").append(v12_1).toString());
                                                                                } else {
                                                                                    v6_1 = v51_0;
                                                                                    if (!v6_1.equalsIgnoreCase(com.sancak2.client.DownloadActivity.sha1Of(v16_0))) {
                                                                                        v9_3 = v16_0;
                                                                                        v11_6 = v43;
                                                                                        v10_9 = v47_0;
                                                                                        v7_3 = v52_0;
                                                                                        v9_3.delete();
                                                                                        throw new Exception("sha1 uyusmuyor");
                                                                                    } else {
                                                                                        if (v52_0.exists()) {
                                                                                            try {
                                                                                                v52_0.delete();
                                                                                            } catch (String v0_27) {
                                                                                                v9_3 = v16_0;
                                                                                                v12_1 = v30_1;
                                                                                                v11_6 = v43;
                                                                                                v10_9 = v47_0;
                                                                                                v7_3 = v52_0;
                                                                                                v0_19 = v0_27.toString();
                                                                                                long v8_11 = v25_0;
                                                                                                android.util.Log.w(v8_11, new StringBuilder().append(v11_6).append(": ").append(v0_19).toString());
                                                                                                try {
                                                                                                    Thread.sleep(800);
                                                                                                } catch (InterruptedException) {
                                                                                                }
                                                                                                if (v46_0 == 0) {
                                                                                                    v2_8 = (v42 + 1);
                                                                                                    v30_0 = v3_5;
                                                                                                    v4_0 = v6_1;
                                                                                                    v3_2 = v7_3;
                                                                                                    v25_0 = v8_11;
                                                                                                    v13_0 = v12_1;
                                                                                                    v8_1 = v40_1;
                                                                                                    v6_0 = v48_1;
                                                                                                    v12_1 = v10_9;
                                                                                                    v10_7 = v11_6;
                                                                                                    v11_2 = v9_3;
                                                                                                    v9_1 = v17_1;
                                                                                                } else {
                                                                                                    v46_0.disconnect();
                                                                                                }
                                                                                            }
                                                                                        }
                                                                                        v9_3 = v16_0;
                                                                                        v7_3 = v52_0;
                                                                                        if (!v9_3.renameTo(v7_3)) {
                                                                                            v11_6 = v43;
                                                                                            v10_9 = v47_0;
                                                                                            throw new Exception("dosya yerlestirilemedi");
                                                                                        } else {
                                                                                            v28_0 += v30_1;
                                                                                            v11_6 = v43;
                                                                                            v10_9 = v47_0;
                                                                                            try {
                                                                                                v10_9.put(v11_6, v6_1);
                                                                                            } catch (String v0_27) {
                                                                                                v37 = 1;
                                                                                                v12_1 = v30_1;
                                                                                            }
                                                                                            if (v46_0 != 0) {
                                                                                                v46_0.disconnect();
                                                                                            }
                                                                                            v37 = 1;
                                                                                            v8_11 = v25_0;
                                                                                            v12_1 = v30_1;
                                                                                            v0_19 = v39_1;
                                                                                        }
                                                                                    }
                                                                                }
                                                                            } catch (String v0_27) {
                                                                            }
                                                                            if (v9_8 <= 0) {
                                                                            } else {
                                                                                try {
                                                                                    if (!v1_1.mCancelled) {
                                                                                        v8_9.write(v0_44, 0, v9_8);
                                                                                        v16_1 = v11_2;
                                                                                        v44 += ((long) v9_8);
                                                                                        try {
                                                                                            int v9_9 = System.currentTimeMillis();
                                                                                        } catch (String v0_45) {
                                                                                            v52_1 = v3_2;
                                                                                            v51_1 = v4_0;
                                                                                            v48_1 = v6_0;
                                                                                            v46_0 = v7_3;
                                                                                            int v47_1 = v12_1;
                                                                                            v3_5 = v30_0;
                                                                                            v9_3 = v16_1;
                                                                                            v12_1 = v13_0;
                                                                                            v11_6 = v43;
                                                                                            v10_9 = v47_1;
                                                                                        }
                                                                                        if ((v9_9 - v26_0) <= 100) {
                                                                                            v52_1 = v3_2;
                                                                                            v51_1 = v4_0;
                                                                                            v48_1 = v6_0;
                                                                                            v46_0 = v7_3;
                                                                                            v47_2 = v12_1;
                                                                                            v3_5 = v30_0;
                                                                                            v30_3 = v13_0;
                                                                                        } else {
                                                                                            v46_0 = v7_3;
                                                                                            String v6_3 = (v28_0 + v44);
                                                                                            v48_1 = v6_0;
                                                                                            v47_2 = v12_1;
                                                                                            int v49 = v9_9;
                                                                                            try {
                                                                                                v52_1 = v3_2;
                                                                                                v51_1 = v4_0;
                                                                                                v3_5 = v30_0;
                                                                                                try {
                                                                                                    v30_3 = v13_0;
                                                                                                    v13_0 = 1000;
                                                                                                    try {
                                                                                                        int v11_17 = ((int) Math.min(1000, ((v6_3 * 1000) / Math.max(1, v3_5))));
                                                                                                        v1_1 = v1_1.post(new StringBuilder().append("\u0130ndiriliyor... %").append((v11_17 / 10)).toString(), new StringBuilder().append(com.sancak2.client.DownloadActivity.fmtMb(v6_3)).append(" / ").append(com.sancak2.client.DownloadActivity.fmtMb(v3_5)).append(" MB   ").append(com.sancak2.client.DownloadActivity.fmtMb(((long) (((double) v6_3) / Math.max(4562254508917369340, (((double) (v9_9 - v18_1)) / 4652007308841189376)))))).append(" MB/sn   (").append((v5_2 + 1)).append("/").append(v17_1.size()).append(")").toString(), v11_17);
                                                                                                        v26_0 = v49;
                                                                                                    } catch (String v0_45) {
                                                                                                        v9_3 = v16_1;
                                                                                                        v12_1 = v30_3;
                                                                                                        v11_6 = v43;
                                                                                                        v10_9 = v47_2;
                                                                                                        v26_0 = v49;
                                                                                                        v6_1 = v51_1;
                                                                                                        v7_3 = v52_1;
                                                                                                        v8_9.close();
                                                                                                        v2_21.close();
                                                                                                        throw v0_45;
                                                                                                    }
                                                                                                } catch (String v0_45) {
                                                                                                    v30_3 = v13_0;
                                                                                                }
                                                                                            } catch (String v0_45) {
                                                                                                v52_1 = v3_5;
                                                                                                v51_1 = v4_0;
                                                                                                v3_5 = v30_0;
                                                                                            }
                                                                                        }
                                                                                    } else {
                                                                                        v8_9.close();
                                                                                        v2_21.close();
                                                                                        if (v7_3 != null) {
                                                                                            v7_3.disconnect();
                                                                                        }
                                                                                        return;
                                                                                    }
                                                                                } catch (String v0_45) {
                                                                                    v52_1 = v3_2;
                                                                                    v51_1 = v4_0;
                                                                                    v48_1 = v6_0;
                                                                                    v46_0 = v7_3;
                                                                                    v16_1 = v11_2;
                                                                                }
                                                                            }
                                                                        }
                                                                    } else {
                                                                        try {
                                                                            v42 = v2_8;
                                                                            try {
                                                                                v43 = v10_7;
                                                                            } catch (String v0_27) {
                                                                                v43 = v10_7;
                                                                            }
                                                                            v7_3.setRequestProperty("Range", new StringBuilder().append("bytes=").append(v8_6).append("-").toString());
                                                                        } catch (String v0_27) {
                                                                            v42 = v2_8;
                                                                        }
                                                                    }
                                                                    v48_1 = v6_0;
                                                                    v46_0 = v7_3;
                                                                    v9_3 = v11_2;
                                                                    v10_9 = v12_1;
                                                                    v12_1 = v13_0;
                                                                    v11_6 = v43;
                                                                    v7_3 = v3_2;
                                                                    v6_1 = v4_0;
                                                                    v3_5 = v30_0;
                                                                } catch (String v0_27) {
                                                                }
                                                            } catch (String v0_33) {
                                                                StringBuilder v13_2 = v7_3;
                                                                if (v13_2 != null) {
                                                                    v13_2.disconnect();
                                                                }
                                                                throw v0_33;
                                                            }
                                                        } catch (String v0_27) {
                                                            v42 = v2_8;
                                                            v48_1 = v6_0;
                                                            v46_0 = v7_3;
                                                            v17_1 = v9_1;
                                                            v9_3 = v11_2;
                                                            v7_3 = v3_2;
                                                            v6_1 = v4_0;
                                                            v11_6 = v10_7;
                                                            v10_9 = v12_1;
                                                            v12_1 = v13_0;
                                                        } catch (String v0_33) {
                                                            v46_0 = v7_3;
                                                            v13_2 = v46_0;
                                                        }
                                                    } catch (String v0_27) {
                                                        v42 = v2_8;
                                                        v7_3 = v3_2;
                                                        v48_1 = v6_0;
                                                        v17_1 = v9_1;
                                                        v9_3 = v11_2;
                                                        v6_1 = v4_0;
                                                        v11_6 = v10_7;
                                                        v10_9 = v12_1;
                                                        v12_1 = v13_0;
                                                        v3_5 = v30_0;
                                                        v46_0 = 0;
                                                    }
                                                } catch (String v0_27) {
                                                    v42 = v2_8;
                                                    v7_3 = v3_2;
                                                    v48_1 = v6_0;
                                                    v40_1 = v8_1;
                                                } catch (String v0_33) {
                                                    v13_2 = 0;
                                                } catch (String v0_33) {
                                                }
                                            }
                                            v48_0 = v6_0;
                                            v40_0 = v8_1;
                                            v17_0 = v9_1;
                                            v10_8 = v12_1;
                                            v8_0 = v25_0;
                                            v3_4 = v30_0;
                                            if (v37) {
                                            } else {
                                                v1_1.fail(new StringBuilder("\u0130ndirme ba\u015far\u0131s\u0131z: ").append(v10_7).toString(), v0_19);
                                                return;
                                            }
                                        } else {
                                            v1_1.fail("Klas\u00f6r olu\u015fturulamad\u0131", v10_7);
                                            return;
                                        }
                                    } catch (Exception) {
                                        v36_1 = v2_3;
                                        v34 = v3_3;
                                        v33 = v4_1;
                                    }
                                } catch (Exception) {
                                    v36_1 = v2_3;
                                    v34 = v3_3;
                                    v33 = v4_1;
                                    v48_0 = v6_0;
                                    v38 = v7_1;
                                    v40_0 = v8_1;
                                    v17_0 = v9_1;
                                    v35 = v11_2;
                                    v10_8 = v12_1;
                                    v32 = v13_1;
                                    v24_0 = v14_4;
                                }
                            } else {
                                return;
                            }
                        }
                        v1_1.writeLocalManifest(v13_1, v14_4).post("G\u00fcncelleme tamamland\u0131", v2_3, 1000);
                        this.launchGame();
                        return;
                    } else {
                        v1_1.writeLocalManifest(v13_1, v14_4).post("Dosyalar g\u00fcncel", "Oyun ba\u015flat\u0131l\u0131yor...");
                        this.launchGame();
                        return;
                    }
                } else {
                    if ((!new java.io.File(v7_1, "pack/Index").exists()) || (!new java.io.File(v7_1, "lib").isDirectory())) {
                        this.fail("Sunucuya ula\u015f\u0131lamad\u0131", "\u0130nternet ba\u011flant\u0131n\u0131z\u0131 kontrol edip tekrar deneyin.");
                        return;
                    } else {
                        this.post("\u00c7evrimd\u0131\u015f\u0131: mevcut dosyalarla ba\u015flat\u0131l\u0131yor", "");
                        this.launchGame();
                        return;
                    }
                }
            }
            if (v0_35.getResponseCode() != 200) {
                throw new Exception(new StringBuilder("HTTP ").append(v0_35.getResponseCode()).toString());
            } else {
                v14_4 = new org.json.JSONObject(new String(com.sancak2.client.DownloadActivity.readAll(v0_35.getInputStream()), java.nio.charset.StandardCharsets.UTF_8));
            }
        } else {
            return;
        }
    }

    private android.widget.LinearLayout$LayoutParams wrap()
    {
        android.widget.LinearLayout$LayoutParams v0_1 = new android.widget.LinearLayout$LayoutParams(-2, -2);
        v0_1.gravity = 1;
        return v0_1;
    }

    private void writeLocalManifest(java.io.File p2, org.json.JSONObject p3)
    {
        try {
            String v0_1 = new java.io.FileOutputStream(p2);
            v0_1.write(p3.toString().getBytes(java.nio.charset.StandardCharsets.UTF_8));
            v0_1.close();
        } catch (String v2_5) {
            android.util.Log.w("m2download", new StringBuilder("yerel manifest yazilamadi: ").append(v2_5).toString());
        }
        return;
    }

    protected void onCreate(android.os.Bundle p2)
    {
        super.onCreate(p2);
        this.getWindow().addFlags(128);
        if (android.os.Build$VERSION.SDK_INT >= 28) {
            this.getWindow().getAttributes().layoutInDisplayCutoutMode = 1;
        }
        this.hideSystemBars();
        this.setContentView(this.buildUi());
        this.startWork();
        return;
    }

    protected void onDestroy()
    {
        this.mCancelled = 1;
        super.onDestroy();
        return;
    }

    protected void onResume()
    {
        super.onResume();
        if ((this.mPendingApk != null) && ((this.mPendingApk.exists()) && (this.getPackageManager().canRequestPackageInstalls()))) {
            this.startInstall();
        }
        return;
    }

    public void onWindowFocusChanged(boolean p1)
    {
        super.onWindowFocusChanged(p1);
        if (p1) {
            this.hideSystemBars();
        }
        return;
    }
}
