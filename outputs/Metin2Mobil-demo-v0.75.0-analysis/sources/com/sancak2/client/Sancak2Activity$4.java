package com.sancak2.client;
 class Sancak2Activity$4 implements java.lang.Runnable {
    final synthetic com.sancak2.client.Sancak2Activity this$0;

    Sancak2Activity$4(com.sancak2.client.Sancak2Activity p1)
    {
        this.this$0 = p1;
        return;
    }

    public void run()
    {
        if (com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0) != null) {
            com.sancak2.client.Sancak2Activity.-$$Nest$fgetmInputView(this.this$0).beginReset();
            android.util.Log.i("sancak2", "klavye oturumu: oyun metni degisti (on ek kirpma etkin, restartInput yok)");
            return;
        } else {
            return;
        }
    }
}
