package com.sancak2.client;
 class DownloadActivity$7 implements java.lang.Runnable {
    final synthetic com.sancak2.client.DownloadActivity this$0;

    DownloadActivity$7(com.sancak2.client.DownloadActivity p1)
    {
        this.this$0 = p1;
        return;
    }

    public void run()
    {
        if (!this.this$0.isFinishing()) {
            com.sancak2.client.DownloadActivity v0_4 = new android.content.Intent(this.this$0, com.sancak2.client.Sancak2Activity);
            v0_4.addFlags(268468224);
            this.this$0.startActivity(v0_4);
            this.this$0.finish();
            return;
        } else {
            return;
        }
    }
}
