package com.sancak2.client;
final class Sancak2Activity$InputView$Conn extends android.view.inputmethod.BaseInputConnection {
    final synthetic com.sancak2.client.Sancak2Activity$InputView this$1;

    Sancak2Activity$InputView$Conn(com.sancak2.client.Sancak2Activity$InputView p1, android.view.View p2)
    {
        this.this$1 = p1;
        super(p2, 0);
        return;
    }

    public boolean commitText(CharSequence p2, int p3)
    {
        this.this$1.noteImeActivity();
        com.sancak2.client.Sancak2Activity$InputView v2_3 = com.sancak2.client.Sancak2Activity$InputView.-$$Nest$mconsumePending(this.this$1, p2.toString(), 1);
        if (v2_3 != null) {
            com.sancak2.client.Sancak2Activity$InputView.-$$Nest$mreplaceComposing(this.this$1, v2_3);
            return 1;
        } else {
            com.sancak2.client.Sancak2Activity$InputView.-$$Nest$mreplaceComposing(this.this$1, "");
            return 1;
        }
    }

    public boolean deleteSurroundingText(int p6, int p7)
    {
        this.this$1.noteImeActivity();
        if (!this.this$1.swallowGhost("")) {
            com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fputmComposing(this.this$1, "");
            com.sancak2.client.Sancak2Activity$InputView.-$$Nest$msessionDelete(this.this$1, p6);
            int v0_2 = 0;
            int v1_0 = 0;
            while (v1_0 < p6) {
                this.this$1.this$0.nativeKeyDown(67);
                v1_0++;
            }
            while (v0_2 < p7) {
                this.this$1.this$0.nativeKeyDown(112);
                v0_2++;
            }
            return 1;
        } else {
            return 1;
        }
    }

    public boolean finishComposingText()
    {
        com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fputmComposing(this.this$1, "");
        if (com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmSession(this.this$1).length() > 0) {
            com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fputmPendingDupe(this.this$1, "");
        }
        return 1;
    }

    public android.view.inputmethod.ExtractedText getExtractedText(android.view.inputmethod.ExtractedTextRequest p1, int p2)
    {
        android.view.inputmethod.ExtractedText v1_1 = new android.view.inputmethod.ExtractedText();
        v1_1.text = com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmSession(this.this$1).toString();
        v1_1.startOffset = 0;
        v1_1.partialStartOffset = -1;
        v1_1.partialEndOffset = -1;
        v1_1.selectionStart = com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmSession(this.this$1).length();
        v1_1.selectionEnd = com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmSession(this.this$1).length();
        return v1_1;
    }

    public CharSequence getSelectedText(int p1)
    {
        return 0;
    }

    public CharSequence getTextAfterCursor(int p1, int p2)
    {
        return "";
    }

    public CharSequence getTextBeforeCursor(int p3, int p4)
    {
        int v4_2 = com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmSession(this.this$1).length();
        return com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmSession(this.this$1).substring(Math.max(0, (v4_2 - Math.max(0, p3))), v4_2);
    }

    public boolean performEditorAction(int p2)
    {
        com.sancak2.client.Sancak2Activity$InputView.-$$Nest$marmPending(this.this$1);
        this.this$1.this$0.nativeKeyDown(66);
        return 1;
    }

    public boolean sendKeyEvent(android.view.KeyEvent p6)
    {
        if (p6.getAction() == 0) {
            String v0_3 = p6.getKeyCode();
            if (v0_3 != 66) {
                this.this$1.noteImeActivity();
                if ((v0_3 != 67) || (!this.this$1.swallowGhost(""))) {
                    if ((v0_3 != 67) && ((v0_3 != 112) && (v0_3 != 61))) {
                        StringBuilder v6_1 = p6.getUnicodeChar();
                        if (v6_1 != null) {
                            String v0_2 = new String(Character.toChars(v6_1));
                            this.this$1.this$0.nativeCommitText(v0_2);
                            com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmSession(this.this$1).append(v0_2);
                        }
                        return 1;
                    } else {
                        com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fputmComposing(this.this$1, "");
                        if (v0_3 == 67) {
                            com.sancak2.client.Sancak2Activity$InputView.-$$Nest$msessionDelete(this.this$1, 1);
                        }
                        this.this$1.this$0.nativeKeyDown(v0_3);
                        return 1;
                    }
                } else {
                    return 1;
                }
            } else {
                com.sancak2.client.Sancak2Activity$InputView.-$$Nest$marmPending(this.this$1);
                this.this$1.this$0.nativeKeyDown(v0_3);
                return 1;
            }
        } else {
            return 1;
        }
    }

    public boolean setComposingRegion(int p4, int p5)
    {
        StringBuilder v0_3 = com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmSession(this.this$1).length();
        int v1_1 = Math.max(0, Math.min(p4, p5));
        int v4_2 = Math.min(v0_3, Math.max(p4, p5));
        if ((v4_2 != v0_3) || (v1_1 >= v4_2)) {
            com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fputmComposing(this.this$1, "");
        } else {
            com.sancak2.client.Sancak2Activity$InputView v5_2 = this.this$1;
            com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fputmComposing(v5_2, com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmSession(v5_2).substring(v1_1, v4_2));
        }
        return 1;
    }

    public boolean setComposingText(CharSequence p4, int p5)
    {
        this.this$1.noteImeActivity();
        String v4_4 = p4.toString();
        if (!this.this$1.swallowGhost(v4_4)) {
            com.sancak2.client.Sancak2Activity$InputView v5_6 = this.this$1;
            v5_6.noteComposingGrowth(com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fgetmComposing(v5_6).length(), v4_4.length());
            String v4_1 = com.sancak2.client.Sancak2Activity$InputView.-$$Nest$mconsumePending(this.this$1, v4_4, 0);
            if (v4_1 != null) {
                com.sancak2.client.Sancak2Activity$InputView v5_2 = this.this$1;
                com.sancak2.client.Sancak2Activity$InputView.-$$Nest$fputmComposing(v5_2, com.sancak2.client.Sancak2Activity$InputView.-$$Nest$mreplaceComposing(v5_2, v4_1));
                return 1;
            } else {
                com.sancak2.client.Sancak2Activity$InputView.-$$Nest$mreplaceComposing(this.this$1, "");
                return 1;
            }
        } else {
            return 1;
        }
    }
}
