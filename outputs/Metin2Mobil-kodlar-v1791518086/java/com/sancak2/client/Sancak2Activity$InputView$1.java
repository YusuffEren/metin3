package com.sancak2.client;
 class Sancak2Activity$InputView$1 implements java.lang.Runnable {
    final synthetic com.sancak2.client.Sancak2Activity$InputView this$1;

    Sancak2Activity$InputView$1(com.sancak2.client.Sancak2Activity$InputView p1)
    {
        this.this$1 = p1;
        return;
    }

    public void run()
    {
        if (com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmRestartPending(this.this$1)) {
            if ((android.os.SystemClock.uptimeMillis() - com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmLastImeAt(this.this$1)) < 1200) {
                this.this$1.postDelayed(this, 700);
            } else {
                this.this$1.doRestartInput();
            }
            return;
        } else {
            return;
        }
    }
}
