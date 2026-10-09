package com.sancak2.client;
public class KeepAliveService extends android.app.Service {
    public static final String ACTION_START = "com.averos2.mobile.KEEPALIVE_START";
    public static final String ACTION_STOP = "com.averos2.mobile.KEEPALIVE_STOP";
    private static final String CHANNEL_ID = "averos2_keepalive";
    private static final int NOTIFICATION_ID = 1001;
    private static final String TAG = "sancak2";
    private android.os.PowerManager$WakeLock mWakeLock;

    public KeepAliveService()
    {
        return;
    }

    private void acquireWakeLock()
    {
        if (this.mWakeLock == null) {
            android.os.PowerManager$WakeLock v0_5 = ((android.os.PowerManager) this.getSystemService("power"));
            if (v0_5 != null) {
                android.os.PowerManager$WakeLock v0_1 = v0_5.newWakeLock(1, "sancak2:keepalive");
                this.mWakeLock = v0_1;
                v0_1.setReferenceCounted(0);
                this.mWakeLock.acquire();
                return;
            } else {
                return;
            }
        } else {
            return;
        }
    }

    private android.app.Notification buildNotification()
    {
        android.app.Notification v0_1 = new android.content.Intent(this, com.sancak2.client.Sancak2Activity);
        v0_1.setFlags(805306368);
        android.app.Notification v0_6 = android.app.PendingIntent.getActivity(this, 0, v0_1, 201326592);
        android.app.Notification$Builder v1_1 = new android.app.Notification$Builder(this, "averos2_keepalive");
        v1_1.setContentTitle(this.getString(com.sancak2.client.R$string.app_name)).setContentText("Oyun arka planda ba\u011fl\u0131 kal\u0131yor").setSmallIcon(com.sancak2.client.R$mipmap.ic_launcher).setContentIntent(v0_6).setOngoing(1).setOnlyAlertOnce(1);
        v1_1.setCategory("service");
        return v1_1.build();
    }

    private void createChannel()
    {
        android.app.NotificationManager v0_2 = ((android.app.NotificationManager) this.getSystemService("notification"));
        if (v0_2 != null) {
            android.app.NotificationChannel v1_1 = new android.app.NotificationChannel("averos2_keepalive", "Oyun ba\u011flant\u0131s\u0131", 2);
            v1_1.setDescription("Oyun arka plandayken sunucu ba\u011flant\u0131s\u0131n\u0131 korur");
            v1_1.setShowBadge(0);
            v1_1.setSound(0, 0);
            v1_1.enableVibration(0);
            v0_2.createNotificationChannel(v1_1);
            return;
        } else {
            return;
        }
    }

    private void releaseWakeLock()
    {
        android.os.PowerManager$WakeLock v0_0 = this.mWakeLock;
        if (v0_0 != null) {
            try {
                if (v0_0.isHeld()) {
                    this.mWakeLock.release();
                }
            } catch (Exception) {
            }
            this.mWakeLock = 0;
            return;
        } else {
            return;
        }
    }

    public static void start(android.content.Context p2)
    {
        try {
            p2.startForegroundService(new android.content.Intent(p2, com.sancak2.client.KeepAliveService).setAction("com.averos2.mobile.KEEPALIVE_START"));
        } catch (String v2_3) {
            android.util.Log.w("sancak2", new StringBuilder("KeepAliveService baslatilamadi: ").append(v2_3).toString());
        }
        return;
    }

    public static void stop(android.content.Context p2)
    {
        try {
            p2.stopService(new android.content.Intent(p2, com.sancak2.client.KeepAliveService));
        } catch (String v2_2) {
            android.util.Log.w("sancak2", new StringBuilder("KeepAliveService durdurulamadi: ").append(v2_2).toString());
        }
        return;
    }

    public android.os.IBinder onBind(android.content.Intent p1)
    {
        return 0;
    }

    public void onCreate()
    {
        super.onCreate();
        this.createChannel();
        return;
    }

    public void onDestroy()
    {
        this.releaseWakeLock();
        try {
            this.stopForeground(1);
        } catch (Exception) {
        }
        android.util.Log.i("sancak2", "KeepAliveService: durdu");
        super.onDestroy();
        return;
    }

    public int onStartCommand(android.content.Intent p4, int p5, int p6)
    {
        if ((p4 == null) || (!"com.averos2.mobile.KEEPALIVE_STOP".equals(p4.getAction()))) {
            String v4_1 = this.buildNotification();
            try {
                if (android.os.Build$VERSION.SDK_INT < 34) {
                    this.startForeground(1001, v4_1);
                } else {
                    this.startForeground(1001, v4_1, 1073741824);
                }
            } catch (String v4_2) {
                android.util.Log.w("sancak2", new StringBuilder("startForeground basarisiz: ").append(v4_2).toString());
            }
            this.acquireWakeLock();
            android.util.Log.i("sancak2", "KeepAliveService: on plan servisi aktif (oyun arka planda bagli kalir)");
            return 2;
        } else {
            this.stopSelf();
            return 2;
        }
    }
}
