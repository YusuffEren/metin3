package com.sancak2.client;
 class M2WebBrowser$1 extends android.webkit.WebViewClient {
    final synthetic com.sancak2.client.M2WebBrowser this$0;

    M2WebBrowser$1(com.sancak2.client.M2WebBrowser p1)
    {
        this.this$0 = p1;
        return;
    }

    public boolean shouldOverrideUrlLoading(android.webkit.WebView p1, android.webkit.WebResourceRequest p2)
    {
        int v1_0 = p2.getUrl();
        if (!com.sancak2.client.M2WebBrowser.-$$Nest$smisInBrowserScheme(v1_0)) {
            com.sancak2.client.M2WebBrowser.-$$Nest$mopenExternally(this.this$0, v1_0.toString());
            return 1;
        } else {
            return 0;
        }
    }
}
