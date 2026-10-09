package com.sancak2.client;
 class DownloadActivity$5 implements java.lang.Runnable {
    final synthetic com.sancak2.client.DownloadActivity this$0;
    final synthetic String val$detail;
    final synthetic int val$progress;
    final synthetic String val$status;

    DownloadActivity$5(com.sancak2.client.DownloadActivity p1, String p2, String p3, int p4)
    {
        this.this$0 = p1;
        this.val$status = p2;
        this.val$detail = p3;
        this.val$progress = p4;
        return;
    }

    public void run()
    {
        com.sancak2.client.DownloadActivity.-$$Nest$fgetmStatus(this.this$0).setText(this.val$status);
        com.sancak2.client.DownloadActivity.-$$Nest$fgetmDetail(this.this$0).setText(this.val$detail);
        if (this.val$progress >= 0) {
            com.sancak2.client.DownloadActivity.-$$Nest$fgetmBar(this.this$0).setIndeterminate(0);
            com.sancak2.client.DownloadActivity.-$$Nest$fgetmBar(this.this$0).setProgress(this.val$progress);
        }
        return;
    }
}
