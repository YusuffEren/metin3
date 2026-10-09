package com.sancak2.client;
final class Sancak2Activity$ShowKeyboardAttempt implements java.lang.Runnable {
    private final int mAttempt;
    final synthetic com.sancak2.client.Sancak2Activity this$0;

    Sancak2Activity$ShowKeyboardAttempt(com.sancak2.client.Sancak2Activity p1, int p2)
    {
        this.this$0 = p1;
        this.mAttempt = p2;
        return;
    }

    public void run()
    {
        if (com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0) != null) {
            if (!com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).hasFocus()) {
                com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).requestFocus();
            }
            com.sancak2.client.Sancak2Activity$InputView v0_8;
            com.sancak2.client.Sancak2Activity$InputView v0_5 = ((android.view.inputmethod.InputMethodManager) this.this$0.getSystemService("input_method"));
            if ((v0_5 == null) || (!v0_5.showSoftInput(com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0), 1))) {
                v0_8 = 0;
            } else {
                v0_8 = 1;
            }
            android.util.Log.i("sancak2", new StringBuilder("showKeyboard deneme ").append(this.mAttempt).append(": showSoftInput=").append(v0_8).append(" hasFocus=").append(com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).hasFocus()).append(" windowFocus=").append(com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).hasWindowFocus()).toString());
            if ((v0_8 == null) && (this.mAttempt < 5)) {
                com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).postDelayed(new com.sancak2.client.Sancak2Activity$ShowKeyboardAttempt(this.this$0, (this.mAttempt + 1)), 100);
            }
            return;
        } else {
            return;
        }
    }
}
