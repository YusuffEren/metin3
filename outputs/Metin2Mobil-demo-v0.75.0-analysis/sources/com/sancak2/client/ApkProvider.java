package com.sancak2.client;
public class ApkProvider extends android.content.ContentProvider {
    public static final String FILE_NAME = "update.apk";

    public ApkProvider()
    {
        return;
    }

    public static String authority(android.content.Context p1)
    {
        return new StringBuilder().append(p1.getPackageName()).append(".apk").toString();
    }

    private java.io.File file()
    {
        return new java.io.File(this.getContext().getExternalFilesDir("apk"), "update.apk");
    }

    public static android.net.Uri uri(android.content.Context p2)
    {
        return android.net.Uri.parse(new StringBuilder("content://").append(com.sancak2.client.ApkProvider.authority(p2)).append("/update.apk").toString());
    }

    public int delete(android.net.Uri p1, String p2, String[] p3)
    {
        return 0;
    }

    public String getType(android.net.Uri p1)
    {
        return "application/vnd.android.package-archive";
    }

    public android.net.Uri insert(android.net.Uri p1, android.content.ContentValues p2)
    {
        return 0;
    }

    public boolean onCreate()
    {
        return 1;
    }

    public android.os.ParcelFileDescriptor openFile(android.net.Uri p3, String p4)
    {
        java.io.FileNotFoundException v4_0 = this.file();
        if ((!"update.apk".equals(p3.getLastPathSegment())) || (!v4_0.exists())) {
            throw new java.io.FileNotFoundException(p3.toString());
        } else {
            return android.os.ParcelFileDescriptor.open(v4_0, 268435456);
        }
    }

    public android.database.Cursor query(android.net.Uri p5, String[] p6, String p7, String[] p8, String p9)
    {
        p5 = this.file();
        p9 = 0;
        if (p6 == null) {
            p6 = new String[2];
            p6[0] = "_display_name";
            p6[1] = "_size";
        }
        android.database.MatrixCursor v1_1 = new android.database.MatrixCursor(p6, 1);
        Object[] v0_1 = new Object[p6.length];
        while (p9 < p6.length) {
            if (!"_display_name".equals(p6[p9])) {
                if (!"_size".equals(p6[p9])) {
                    v0_1[p9] = 0;
                } else {
                    v0_1[p9] = Long.valueOf(p5.length());
                }
            } else {
                v0_1[p9] = "update.apk";
            }
            p9++;
        }
        v1_1.addRow(v0_1);
        return v1_1;
    }

    public int update(android.net.Uri p1, android.content.ContentValues p2, String p3, String[] p4)
    {
        return 0;
    }
}
