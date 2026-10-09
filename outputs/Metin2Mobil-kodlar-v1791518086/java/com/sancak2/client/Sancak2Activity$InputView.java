package com.sancak2.client;
final class Sancak2Activity$InputView extends android.view.View {
    private static final long PENDING_MS = 20000;
    private static final java.util.Locale TR;
    private final Runnable mCheckRestart;
    private String mComposing;
    private long mLastImeAt;
    private String mLastSentLower;
    private String mPendingDupe;
    private long mPendingUntil;
    private long mResetAt;
    private boolean mRestartPending;
    private String mSentComposing;
    private final StringBuilder mSession;
    private long mVoiceUntil;
    final synthetic com.sancak2.client.Sancak2Activity this$0;

    static bridge synthetic String -$$Nest$fgetmComposing(com.sancak2.client.Sancak2Activity$InputView p0)
    {
        return p0.mComposing;
    }

    static bridge synthetic long -$$Nest$fgetmLastImeAt(com.sancak2.client.Sancak2Activity$InputView p2)
    {
        return p2.mLastImeAt;
    }

    static bridge synthetic boolean -$$Nest$fgetmRestartPending(com.sancak2.client.Sancak2Activity$InputView p0)
    {
        return p0.mRestartPending;
    }

    static bridge synthetic StringBuilder -$$Nest$fgetmSession(com.sancak2.client.Sancak2Activity$InputView p0)
    {
        return p0.mSession;
    }

    static bridge synthetic void -$$Nest$fputmComposing(com.sancak2.client.Sancak2Activity$InputView p0, String p1)
    {
        p0.mComposing = p1;
        return;
    }

    static bridge synthetic void -$$Nest$fputmPendingDupe(com.sancak2.client.Sancak2Activity$InputView p0, String p1)
    {
        p0.mPendingDupe = p1;
        return;
    }

    static bridge synthetic void -$$Nest$marmPending(com.sancak2.client.Sancak2Activity$InputView p0)
    {
        p0.armPending();
        return;
    }

    static bridge synthetic String -$$Nest$mconsumePending(com.sancak2.client.Sancak2Activity$InputView p0, String p1, boolean p2)
    {
        return p0.consumePending(p1, p2);
    }

    static bridge synthetic String -$$Nest$mreplaceComposing(com.sancak2.client.Sancak2Activity$InputView p0, String p1)
    {
        return p0.replaceComposing(p1);
    }

    static bridge synthetic void -$$Nest$msessionDelete(com.sancak2.client.Sancak2Activity$InputView p0, int p1)
    {
        p0.sessionDelete(p1);
        return;
    }

    static Sancak2Activity$InputView()
    {
        com.sancak2.client.Sancak2Activity$InputView.TR = new java.util.Locale("tr");
        return;
    }

    Sancak2Activity$InputView(com.sancak2.client.Sancak2Activity p3, android.content.Context p4)
    {
        this.this$0 = p3;
        super(p4);
        super.mComposing = "";
        super.mPendingDupe = "";
        super.mPendingUntil = 0;
        super.mResetAt = 0;
        super.mSentComposing = "";
        super.mSession = new StringBuilder();
        super.mVoiceUntil = 0;
        super.mRestartPending = 0;
        super.mLastSentLower = "";
        super.mLastImeAt = 0;
        super.mCheckRestart = new com.sancak2.client.Sancak2Activity$InputView$1(super);
        super.setFocusable(0);
        super.setFocusableInTouchMode(0);
        return;
    }

    private void armPending()
    {
        String v0_1 = this.mSession.toString();
        this.mResetAt = android.os.SystemClock.uptimeMillis();
        if (com.sancak2.client.Sancak2Activity$InputView.norm(v0_1).length() > 0) {
            this.mPendingDupe = v0_1;
            this.mPendingUntil = (this.mResetAt + 20000);
        }
        StringBuilder v1_5;
        if (this.mComposing.trim().length() <= 0) {
            v1_5 = "";
        } else {
            v1_5 = this.mComposing;
        }
        this.mSentComposing = v1_5;
        this.mComposing = "";
        this.mSession.setLength(0);
        this.notifyImeCleared(v0_1);
        return;
    }

    private String consumePending(String p6, boolean p7)
    {
        if (this.mSentComposing.length() != 0) {
            if (android.os.SystemClock.uptimeMillis() <= this.mPendingUntil) {
                int v3_0 = com.sancak2.client.Sancak2Activity$InputView.TR;
                String v0_3 = this.mSentComposing.replaceAll("^\\s+", "").toLowerCase(v3_0);
                String v2_1 = p6.replaceAll("^\\s+", "");
                int v3_1 = v2_1.toLowerCase(v3_0);
                if ((v0_3.length() <= 0) || ((!v3_1.startsWith(v0_3)) || (v2_1.length() < v0_3.length()))) {
                    this.mSentComposing = "";
                    return p6;
                } else {
                    int v6_2 = v2_1.substring(v0_3.length());
                    if (p7) {
                        this.mSentComposing = "";
                    }
                    if ((v6_2.length() != 0) && (!Character.isWhitespace(v6_2.charAt(0)))) {
                        return v6_2;
                    } else {
                        return 0;
                    }
                }
            } else {
                this.mSentComposing = "";
                return p6;
            }
        } else {
            return p6;
        }
    }

    private static String norm(String p2)
    {
        return p2.toLowerCase(com.sancak2.client.Sancak2Activity$InputView.TR).replaceAll("\\s+", " ").trim().replaceAll("^[\\p{Punct}\\s]+", "").replaceAll("[\\p{Punct}\\s]+$", "");
    }

    private String replaceComposing(String p5)
    {
        StringBuilder v0_0 = this.mComposing;
        int v2 = 0;
        StringBuilder v0_4 = v0_0.codePointCount(0, v0_0.length());
        while (v2 < v0_4) {
            this.this$0.nativeKeyDown(67);
            v2++;
        }
        this.sessionDelete(v0_4);
        this.mComposing = "";
        if (this.mSession.length() == 0) {
            p5 = p5.replaceAll("^\\s+", "");
        }
        if (p5.length() > 0) {
            this.this$0.nativeCommitText(p5);
            this.mSession.append(p5);
        }
        return p5;
    }

    private void sessionDelete(int p5)
    {
        int v0 = 0;
        while ((v0 < p5) && (this.mSession.length() > 0)) {
            int v1_4 = this.mSession;
            StringBuilder v2_0 = this.mSession;
            v2_0.setLength((v2_0.length() - Character.charCount(v1_4.codePointBefore(v1_4.length()))));
            v0++;
        }
        return;
    }

    void beginReset()
    {
        this.armPending();
        return;
    }

    void doRestartInput()
    {
        this.mRestartPending = 0;
        this.removeCallbacks(this.mCheckRestart);
        try {
            String v0_7 = ((android.view.inputmethod.InputMethodManager) this.getContext().getSystemService("input_method"));
        } catch (String v0_1) {
            android.util.Log.w("sancak2", new StringBuilder("klavye yeniden baslatma: ").append(v0_1).toString());
            return;
        }
        if (v0_7 == null) {
            return;
        } else {
            v0_7.restartInput(this);
            return;
        }
    }

    void dropFocus()
    {
        if (this.hasFocus()) {
            this.clearFocus();
        }
        this.setFocusable(0);
        this.setFocusableInTouchMode(0);
        return;
    }

    void newSession()
    {
        this.mComposing = "";
        this.mPendingDupe = "";
        this.mSentComposing = "";
        this.mSession.setLength(0);
        return;
    }

    void noteComposingGrowth(int p3, int p4)
    {
        if ((p4 - p3) > 2) {
            this.mVoiceUntil = (android.os.SystemClock.uptimeMillis() + 5000);
        }
        return;
    }

    void noteImeActivity()
    {
        this.mLastImeAt = android.os.SystemClock.uptimeMillis();
        return;
    }

    void notifyImeCleared(String p8)
    {
        try {
            String v1_3 = ((android.view.inputmethod.InputMethodManager) this.getContext().getSystemService("input_method"));
        } catch (Runnable v8_5) {
            android.util.Log.w("sancak2", new StringBuilder("klavye secim bildirimi: ").append(v8_5).toString());
            return;
        }
        if (v1_3 == null) {
            return;
        } else {
            v1_3.updateSelection(this, 0, 0, -1, -1);
            if (android.os.SystemClock.uptimeMillis() <= this.mVoiceUntil) {
                Runnable v8_2;
                this.mRestartPending = 1;
                if (p8 != null) {
                    v8_2 = p8.toLowerCase(com.sancak2.client.Sancak2Activity$InputView.TR).trim();
                } else {
                    v8_2 = "";
                }
                this.mLastSentLower = v8_2;
                this.removeCallbacks(this.mCheckRestart);
                this.postDelayed(this.mCheckRestart, 1500);
                return;
            } else {
                this.doRestartInput();
                return;
            }
        }
    }

    public boolean onCheckIsTextEditor()
    {
        return 1;
    }

    public android.view.inputmethod.InputConnection onCreateInputConnection(android.view.inputmethod.EditorInfo p2)
    {
        p2.inputType = 524289;
        p2.imeOptions = 301989894;
        return new com.sancak2.client.Sancak2Activity$InputView$Conn(this, this);
    }

    void resetComposing()
    {
        this.mComposing = "";
        return;
    }

    boolean swallowGhost(String p3)
    {
        if ((this.mRestartPending) && (this.mSession.length() <= 0)) {
            int v3_2;
            if (p3 != 0) {
                v3_2 = p3.toLowerCase(com.sancak2.client.Sancak2Activity$InputView.TR).trim();
            } else {
                v3_2 = "";
            }
            if ((v3_2.length() != 0) && ((!this.mLastSentLower.startsWith(v3_2)) || (v3_2.length() >= this.mLastSentLower.length()))) {
                return 0;
            } else {
                this.doRestartInput();
                return 1;
            }
        } else {
            return 0;
        }
    }
}
