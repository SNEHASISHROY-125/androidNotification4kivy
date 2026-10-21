// // File: ResetReceiver.java
// package org.test.notify;

// import android.content.BroadcastReceiver;
// import android.content.Context;
// import android.content.Intent;
// import android.util.Log;
// import android.os.Bundle;

// import androidx.core.app.NotificationManagerCompat;

// public class ResetReceiver extends BroadcastReceiver {
//     @Override
//     public void onReceive(Context context, Intent intent) {
//         Log.d("ResetReceiver", "Reset button tapped!");

//         // Example: launch app if desired | api<=28 
//         Intent launchIntent = context.getPackageManager().getLaunchIntentForPackage(context.getPackageName());
//         if (launchIntent != null) {
//             launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
//             launchIntent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
//             context.startActivity(launchIntent);
//         }
//         //
//         // cancel this Notification
//         //Integer notifId = (Integer) intent.getExtras().get("NOTIFID");
//         int notifId = ((Number) intent.getExtras().get("NOTIFID")).intValue();

//         NotificationManagerCompat notificationManager = NotificationManagerCompat.from(context);
//         notificationManager.cancel(notifId);
//         Log.d("ResetReceiver", "Cancelling..."+notifId);
//         // Any code will execute here...
//     }
// }



package com.snehasys.notify;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

// import java.net.URI;
// import java.net.http.HttpClient;
// import java.net.http.HttpRequest;
// import java.net.http.HttpResponse;
import java.util.concurrent.CompletableFuture;

import android.app.NotificationManager;
import android.os.Bundle;

public class ResetReceiver extends BroadcastReceiver {
    private static final String TAG = "ResetReceiver5";

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.e(TAG, "onReceive() ENTERED");

        if (intent == null) {
            Log.e(TAG, "Intent is null");
            return;
        }

        Log.e(TAG, "Action: " + intent.getAction());
        Log.e(TAG, "Extras: " + intent.getExtras());

        Object nid = intent.getExtras().get("NOTIFID");
        Object addr = intent.getExtras().get("ADDRESS");

        int notifId = -1;
        String address = "/dismiss";
        // safe gaurding
        if (nid instanceof Number) {
            notifId = ((Number) nid).intValue();
        }
        if (addr instanceof String) {
            address = ((String) addr);
        }

        Log.e(TAG, "NOTIFID = " + notifId);

        // debug
        Bundle extras = intent.getExtras();

        if (extras != null) {
            for (String key : extras.keySet()) {
                Object value = extras.get(key);

                Log.e("ResetReceiver5",
                    "EXTRA key=" + key
                    + ", value=" + value
                    + ", type=" +
                    (value == null ? "null" : value.getClass().getName()));
            }
        }

        if (notifId >= 0) {
            NotificationManager nm =
                (NotificationManager)
                context.getSystemService(Context.NOTIFICATION_SERVICE);

            nm.cancel(notifId);
            Log.e(TAG, "Cancelled notification " + notifId);
        } else {
            Log.e(TAG, "NOTIFID missing or invalid");
        }

        // fire & forget OSc
        // Fire and forget network call
        final String oscAddress = address;
        final int oscNotifId = notifId;

        CompletableFuture.runAsync(() -> {
            try {
                UdpSender.sendOsc(oscAddress, oscNotifId);
                // HttpClient client = HttpClient.newHttpClient();
                // HttpRequest request = HttpRequest.newBuilder()
                //         .uri(URI.create("https://api.example.com/notify"))
                //         .GET()
                //         .build();

                // HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                // System.out.println("Network call completed with status: " + response.statusCode());
            } catch (Exception e) {
                // Always catch exceptions to prevent silent thread death / unhandled errors
                System.err.println("Failed to send network request: " + e.getMessage());
            }
        });

        System.out.println("Main thread continues immediately without waiting.");
        
        // Sleep briefly just to let the async thread finish printing before JVM exits in this demo
        try { Thread.sleep(1000); } catch (InterruptedException e) {}
    // }
    }
}

