package com.sancak2.client;
final class M2WebBrowser$GamePopup extends android.widget.PopupWindow {
    private boolean mDismissAllowed;

    M2WebBrowser$GamePopup(android.view.View p2, int p3, int p4)
    {
        super(p2, p3, p4, 0);
        return;
    }

    public void dismiss()
    {
        if (this.mDismissAllowed) {
            super.dismiss();
        }
        return;
    }

    void dismissFromGame()
    {
        this.mDismissAllowed = 1;
        super.dismiss();
        return;
    }
}
