package com.sancak2.client;
 class Sancak2Activity$1 implements android.view.View$OnApplyWindowInsetsListener {
    final synthetic com.sancak2.client.Sancak2Activity this$0;

    Sancak2Activity$1(com.sancak2.client.Sancak2Activity p1)
    {
        this.this$0 = p1;
        return;
    }

    public android.view.WindowInsets onApplyWindowInsets(android.view.View p4, android.view.WindowInsets p5)
    {
        com.sancak2.client.Sancak2Activity.-$$Nest$mupdateSafeInsets(this.this$0, p5);
        if ((android.os.Build$VERSION.SDK_INT >= 30) && ((p5 != null) && (!p5.isVisible(android.view.WindowInsets$Type.ime())))) {
            p4.removeCallbacks(com.sancak2.client.Sancak2Activity.-$$Nest$fgetmRehideBars(this.this$0));
            p4.postDelayed(com.sancak2.client.Sancak2Activity.-$$Nest$fgetmRehideBars(this.this$0), 400);
        }
        return p4.onApplyWindowInsets(p5);
    }
}
