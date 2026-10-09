package com.sancak2.client;
 class Sancak2Activity$3 implements java.lang.Runnable {
    final synthetic com.sancak2.client.Sancak2Activity this$0;

    Sancak2Activity$3(com.sancak2.client.Sancak2Activity p1)
    {
        this.this$0 = p1;
        return;
    }

    public void run()
    {
        if (com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0) != null) {
            com.sancak2.client.Sancak2Activity$InputView v0_8 = ((android.view.inputmethod.InputMethodManager) this.this$0.getSystemService("input_method"));
            if (v0_8 != null) {
                v0_8.hideSoftInputFromWindow(com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).getWindowToken(), 0);
            }
            com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).newSession();
            com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).dropFocus();
            return;
        } else {
            return;
        }
    }
}
