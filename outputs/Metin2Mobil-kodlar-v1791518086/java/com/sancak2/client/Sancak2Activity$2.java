package com.sancak2.client;
 class Sancak2Activity$2 implements java.lang.Runnable {
    final synthetic com.sancak2.client.Sancak2Activity this$0;

    Sancak2Activity$2(com.sancak2.client.Sancak2Activity p1)
    {
        this.this$0 = p1;
        return;
    }

    public void run()
    {
        if (com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0) != null) {
            com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).setFocusable(1);
            com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).setFocusableInTouchMode(1);
            com.sancak2.client.Sancak2Activity$InputView v0_4 = com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).requestFocus();
            com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).newSession();
            com.sancak2.client.Sancak2Activity$ShowKeyboardAttempt v1_4 = ((android.view.inputmethod.InputMethodManager) this.this$0.getSystemService("input_method"));
            if (v1_4 != null) {
                v1_4.restartInput(com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0));
            }
            android.util.Log.i("sancak2", new StringBuilder("showKeyboard: requestFocus=").append(v0_4).append(" hasFocus=").append(com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).hasFocus()).append(" windowFocus=").append(com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).hasWindowFocus()).toString());
            com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).post(new com.sancak2.client.Sancak2Activity$ShowKeyboardAttempt(this.this$0, 0));
            return;
        } else {
            return;
        }
    }
}
