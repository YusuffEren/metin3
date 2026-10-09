package com.sancak2.client;
 class DownloadActivity$1 implements android.view.View$OnClickListener {
    final synthetic com.sancak2.client.DownloadActivity this$0;

    DownloadActivity$1(com.sancak2.client.DownloadActivity p1)
    {
        this.this$0 = p1;
        return;
    }

    public void onClick(android.view.View p1)
    {
        if ((com.sancak2.client.DownloadActivity.-$$Nest$fgetmPendingApk(this.this$0) == null) || (!com.sancak2.client.DownloadActivity.-$$Nest$fgetmPendingApk(this.this$0).exists())) {
            com.sancak2.client.DownloadActivity.-$$Nest$mstartWork(this.this$0);
            return;
        } else {
            com.sancak2.client.DownloadActivity.-$$Nest$mstartInstall(this.this$0);
            return;
        }
    }
}
