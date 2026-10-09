package com.sancak2.client;
 class M2WebBrowser$2$1 extends android.webkit.WebViewClient {
    final synthetic com.sancak2.client.M2WebBrowser$2 this$1;

    M2WebBrowser$2$1(com.sancak2.client.M2WebBrowser$2 p1)
    {
        this.this$1 = p1;
        return;
    }

    public boolean shouldOverrideUrlLoading(android.webkit.WebView p2, android.webkit.WebResourceRequest p3)
    {
        com.sancak2.client.M2WebBrowser.-$$Nest$mopenExternally(this.this$1.this$0, p3.getUrl().toString());
        p2.destroy();
        return 1;
    }
}
