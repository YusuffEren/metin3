package com.sancak2.client;
 class DownloadActivity$6 implements java.lang.Runnable {
    final synthetic com.sancak2.client.DownloadActivity this$0;
    final synthetic String val$detail;
    final synthetic String val$status;

    DownloadActivity$6(com.sancak2.client.DownloadActivity p1, String p2, String p3)
    {
        this.this$0 = p1;
        this.val$status = p2;
        this.val$detail = p3;
        return;
    }

    public void run()
    {
        com.sancak2.client.DownloadActivity.-$$Nest$fgetmStatus(this.this$0).setText(this.val$status);
        com.sancak2.client.DownloadActivity.-$$Nest$fgetmDetail(this.this$0).setText(this.val$detail);
        com.sancak2.client.DownloadActivity.-$$Nest$fgetmBar(this.this$0).setIndeterminate(0);
        com.sancak2.client.DownloadActivity.-$$Nest$fgetmRetry(this.this$0).setVisibility(0);
        return;
    }
}
