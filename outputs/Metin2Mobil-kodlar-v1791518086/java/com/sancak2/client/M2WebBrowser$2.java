package com.sancak2.client;
 class M2WebBrowser$2 extends android.webkit.WebChromeClient {
    final synthetic com.sancak2.client.M2WebBrowser this$0;

    M2WebBrowser$2(com.sancak2.client.M2WebBrowser p1)
    {
        this.this$0 = p1;
        return;
    }

    public boolean onCreateWindow(android.webkit.WebView p1, boolean p2, boolean p3, android.os.Message p4)
    {
        int v1_2 = new android.webkit.WebView(com.sancak2.client.M2WebBrowser.-$$Nest$fgetmActivity(this.this$0));
        v1_2.setWebViewClient(new com.sancak2.client.M2WebBrowser$2$1(this));
        ((android.webkit.WebView$WebViewTransport) p4.obj).setWebView(v1_2);
        p4.sendToTarget();
        return 1;
    }
}
