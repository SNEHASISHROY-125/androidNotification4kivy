// File: ResetReceiver.java
package org.test.notify;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.os.Bundle;

import androidx.core.app.NotificationManagerCompat;

public class ResetReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        Log.d("ResetReceiver", "Reset button tapped!");

        // Example: launch app if desired | api<=28 
        Intent launchIntent = context.getPackageManager().getLaunchIntentForPackage(context.getPackageName());
        if (launchIntent != null) {
            launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            launchIntent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            context.startActivity(launchIntent);
        }
        //
        // cancel this Notification
        //Integer notifId = (Integer) intent.getExtras().get("NOTIFID");
        int notifId = ((Number) intent.getExtras().get("NOTIFID")).intValue();

        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(context);
        notificationManager.cancel(notifId);
        Log.d("ResetReceiver", "Cancelling..."+notifId);
        // Any code will execute here...
    }
}
