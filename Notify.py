'''
androidNotification4kivy©SnehasishRoy & Contributors 2025-2026
'''

## Notification
from jnius import autoclass, cast
from android import activity
from android.permissions import request_permissions, check_permission,Permission

# helpers
from helper import load_remote_views , set_text , set_progress
# tcp bridge
from tcp.TcpComms.tcp import start_tcp_server

# Android context and classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
NotificationCompatBuilder = autoclass('androidx.core.app.NotificationCompat$Builder')
NotificationManagerCompat = autoclass('androidx.core.app.NotificationManagerCompat')
NotificationChannel = autoclass('android.app.NotificationChannel')
Build = autoclass('android.os.Build')
BitmapFactory = autoclass('android.graphics.BitmapFactory')
Uri = autoclass('android.net.Uri')
BigPictureStyle = autoclass('androidx.core.app.NotificationCompat$BigPictureStyle')
BigTextStyle = autoclass('androidx.core.app.NotificationCompat$BigTextStyle')

NotificationCompat = autoclass('androidx.core.app.NotificationCompat')
Build_VERSION = autoclass('android.os.Build$VERSION')
SDK_INT = Build_VERSION.SDK_INT  # ✅ This works

# Context
context = PythonActivity.mActivity

# Notification Channel (for Android 8+)
channel_id = "androidNotification4kivy"
if SDK_INT >= 26:
    importance = autoclass('android.app.NotificationManager').IMPORTANCE_DEFAULT
    channel = NotificationChannel(channel_id, "androidNotification4kivy_channel", importance)
    manager = context.getSystemService(Context.NOTIFICATION_SERVICE)
    manager.createNotificationChannel(channel)

else : manager = getattr(NotificationManagerCompat, "from")(context)

def load(src:str) -> any:
  # Load an image from resources
  # image_path = 'congrats_image.jpg'  # must be accessible and readable
  return BitmapFactory.decodeFile(src)


def get_mActivity_pending_intent():
  # launch App instance
  Intent = autoclass('android.content.Intent')
  PendingIntent = autoclass('android.app.PendingIntent')

  PythonActivity = autoclass('org.kivy.android.PythonActivity')

  intent = Intent(context, PythonActivity)
  intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP)

  pending_intent = PendingIntent.getActivity(
      context, 0, intent,
      PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
  )
  return pending_intent



import random , datetime
from typing import NewType


Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')
JavaString = autoclass('java.lang.String')
JInteger = autoclass("java.lang.Integer")
JBool = autoclass("java.lang.Boolean")
Color = autoclass('android.graphics.Color')

RemoteViews = NewType("RemoteViews" , object)

def action_button_pending_intent(pid:int,intent_filter,action_class,data:dict):
  # ACTION NAME must match manifest
  action_intent = Intent(intent_filter)  # "com.example.ACTION_RESET" in mainfest
  action_intent.setClassName(context.getPackageName(), action_class)   # "org.test.notify.ResetReceiver" in mainfest

  # put data to retrive in java
  action_intent.putExtra("NOTIFID", pid)#JInteger(pid).intValue())
  # set additional data
  for key in data.keys():
    action_intent.putExtra(key, JavaString(data.get(key)))

  action_pending_intent = PendingIntent.getBroadcast(
      context, pid, action_intent,
      PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
  )
  return action_pending_intent

# Deprecated so avoid using in upcomming API  | tested on API.36 works fine
# .addAction(Notification.Action) as recomended :TODO
# builder.addAction(context.getApplicationInfo().icon, "Reset", action_pending_intent)


def to_signed_int32(val):
    return val if val < 0x80000000 else val - 0x100000000

# #######

def parcel_notification(**kwargs):
  views = load_remote_views("notification_parcel")

  set_text(
      views, "parcel_title",
      "Your parcel is out for delivery"
  )
  set_text(views, "parcel_order", "Order #PKG2048")
  set_text(views, "parcel_eta", "Expected today by 8:00 PM")

  # Build notification with BigPictureStyle
  builder = NotificationCompatBuilder(context, channel_id)
  pid = random.randint(0, 32767) 

  builder.setSmallIcon(context.getApplicationInfo().icon)

  builder.setCustomContentView(views)
  builder.setCustomBigContentView(views)

  manager.notify(pid, builder.build())

def show_social_profile():
  views = load_remote_views("notification_social")

  set_text(views, "social_person", "Priya Sharma")
  set_text(
      views, "social_message",
      "Viewed your profile and sent you a message."
  )
  set_text(
      views, "social_subtitle",
      "Software Engineer · 2 min ago"
  )

  # Build notification with BigPictureStyle
  builder = NotificationCompatBuilder(context, channel_id)
  pid = random.randint(0, 32767) 

  builder.setSmallIcon(context.getApplicationInfo().icon)

  builder.setCustomContentView(views)
  builder.setCustomBigContentView(views)

  manager.notify(pid, builder.build())

def show_upload_download():
  # views = load_remote_views("notification_transfer")

  # set_text(views, "transfer_title", "Uploading backup.zip")
  # set_text(views, "transfer_speed", "2.1 MB/s")
  # set_text(views, "transfer_status", "42% complete")
  # set_progress(views, "transfer_progress", 42)

  # Compact version
  compact = load_remote_views("notification_transfer_compact")
  set_text(compact, "transfer_compact_title", "Uploading backup.zip")
  set_text(compact, "transfer_compact_status", "42% · 2.4 MB/s")
  set_progress(compact, "transfer_compact_progress", 42)

  # Expanded upload notification
  expanded = load_remote_views("notification_transfer")
  set_text(expanded, "transfer_title", "Uploading backup.zip")
  set_text(expanded, "transfer_speed", "2.4 MB/s · 8.4 MB / 20 MB")
  set_text(expanded, "transfer_percent", "42%")
  set_text(expanded, "transfer_eta", "ETA 00:00:06")
  set_progress(expanded, "transfer_progress", 42)

  # Build notification with BigPictureStyle
  builder = NotificationCompatBuilder(context, channel_id)
  pid = random.randint(0, 32767) 

  builder.setSmallIcon(context.getApplicationInfo().icon)

  # Attach to your existing notification builder.
  builder.setCustomContentView(compact)
  builder.setCustomBigContentView(expanded)

  # Use your existing notification manager and notification ID.
  notification = builder.build()
  manager.notify(pid, notification)

def notify(**kwargs) -> int:
  '''
  *nid  ``notification id``
  *title  ``notification title``
  *MS:int ``Timeout in ms after auto dismiss``
  *content ``notification content text``
  *small_icon ``notification small-icon-right``
  *large_icon ``notification large-icon-left``
  *big_content ``huge notification content text``
  *color  ``color like: (0..255 , 0..255, 0..255, 0..255)``
  *Action:list ``Action Button Data [action1:dict, action2:dict, action3:dict] | max 3 Action buttons``
  *expanded_image ``notification big-image when expanded``
  *dismissable:bool ``user can't dismiss notification``
  *progress_bar:bool ``enable progressbar``
  *remote_views:bool  ``enable remoteViews``
  *remote_custom_view: RemoteViews  ``android RemoteView compact``
  *remote_custom_big_view: RemoteViews  ``android RemoteView expanded``

  *progress_value:int ``progress bar value | max:100 (value==0 > in-determinate)``
  *open_mActivity:bool ``notification on click opens App activity``  
  '''
  # nid:
  pid = random.randint(0, 32767) 
  notification_id = int(kwargs.get("nid" , pid))
  # id = int(datetime.datetime.now().strftime("%H%M%S"))  # it generates 6-digit but I found trouble using it with .putExtra(Bundle) :TODO
  # Build notification with BigPictureStyle
  builder = NotificationCompatBuilder(context, channel_id)
  # notification title
  if kwargs.get("title") : builder.setContentTitle(kwargs['title'])
  else: builder.setContentTitle("New Image Notification")
  # notification text
  if kwargs.get("content") : builder.setContentText(kwargs["content"]) 
  # else: builder.setContentText("Check out this image!")
  # small tiny icon
  if kwargs.get("small_icon") : builder.setSmallIcon(kwargs["small_icon"]) 
  else: builder.setSmallIcon(context.getApplicationInfo().icon)
  # icon on left
  if kwargs.get("large_icon") : builder.setLargeIcon(load(kwargs['large_icon'])) 
  # else: builder.setLargeIcon(load('congrats_image.jpg'))
  # big text when expanded
  if kwargs.get("big_content") : builder.setStyle(BigTextStyle().bigText(kwargs["big_content"]))   #### Either Big-picture or Big-ext ##
  # image when expaned
  if kwargs.get("expanded_image") and not kwargs.get("big_content") : builder.setStyle(BigPictureStyle().bigPicture(load(kwargs["expanded_image"])))
  # progress bar
  if bool(kwargs.get("progress_bar")) and int(kwargs.get("progress_value")) !=0 : builder.setProgress(100, kwargs["progress_value"], JBool.FALSE); # false = determinate
  elif bool(kwargs.get("progress_bar")) and int(kwargs.get("progress_value")) == 0 : builder.setProgress(0 , 0 , JBool.TRUE)
  # sticky notification
  if bool(kwargs.get("dismissable")) : builder.setOngoing(True)   # https://developer.android.com/reference/android/app/Notification.Builder#setOngoing(boolean)  | works api <=36 
  # Action Button
  ''' As of Android Build.VERSION_CODES.S, apps targeting API level Build.VERSION_CODES.S or higher 
      won't be able to start activities while processing broadcast receivers or services in response to notification action clicks. 
      To launch an activity in those cases, provide a PendingIntent for the activity itself.  :TODO'''
  if kwargs.get("Action"):
    for action in kwargs["Action"]:
      builder.addAction(context.getApplicationInfo().icon, JavaString(action.get("name")) , action_button_pending_intent(notification_id,action["intent_filter"],action["action_class"],data=action["data"]))
  
  # Auto dismiss-timeout    https://developer.android.com/reference/android/app/Notification.Builder#setTimeoutAfter(long)
  if kwargs.get("MS") : builder.setTimeoutAfter(int(kwargs["MS"])) # long: durationMs 1s = 1000ms

  # Colorize  
  if kwargs.get("color"):
    color = Color.argb(*tuple(kwargs.get("color"))) # tuple(a , r , g , b)
    builder.setColor(color) # ARGB |  https://developer.android.com/reference/android/graphics/Color#argb(int,%20int,%20int,%20int)
    # builder.setColor(to_signed_int32(kwargs["color"]));      # 0xFFFF5722 Orange color  | worked on api.28 :TODO newer api's
    builder.setColorized(True);        # Enable full background coloring

  # Sound : TODO
  # https://developer.android.com/reference/android/app/Notification.Builder#setSound(android.net.Uri,%20int)
  #  NotificationChannel.setSound(Uri,AudioAttributes).

  # Vibration : TODO
  # NotificationChannel.enableVibration (boolean vibration)
  # https://developer.android.com/reference/android/app/NotificationChannel#enableVibration(boolean)
  
  # Time-Count Meter
  # builder.setWhen(System.currentTimeMillis()).setUsesChronometer(true)   # https://developer.android.com/reference/android/app/Notification.Builder#setUsesChronometer(boolean)
  # .setChronometerCountDown(boolean)   # count in reverse

  # RemoteViews
  if bool(kwargs.get("remote_views")):
    normal = kwargs.get("remote_custom_view")
    expanded = kwargs.get("remote_custom_big_view")
    # safe check
    if normal and expanded:
      # Attach to your existing notification builder.
      builder.setCustomContentView(normal)  # https://developer.android.com/reference/android/app/Notification.Builder#setCustomBigContentView(android.widget.RemoteViews)
      builder.setCustomBigContentView(expanded)
  
  builder.setPriority(NotificationCompat.PRIORITY_HIGH)   # https://developer.android.com/reference/android/app/Notification.Builder#setPriority(int)
  # other FLAGS : PRIORITY_LOW | PRIORITY_DEFAULT | PRIORITY_MAX  | PRIORITY_MIN    https://developer.android.com/reference/android/app/Notification#PRIORITY_DEFAULT
  
  builder.setVisibility(NotificationCompat.VISIBILITY_PUBLIC) # lock-screen visibility  https://developer.android.com/reference/android/app/Notification.Builder#setPublicVersion(android.app.Notification)
  # other FLAGS : VISIBILITY_PRIVATE | VISIBILITY_SECRET https://developer.android.com/reference/android/app/Notification#VISIBILITY_PRIVATE
  
  # Make this notificatSion automatically dismissed when the user touches it.
  builder.setAutoCancel(True)   # https://developer.android.com/reference/android/app/Notification.Builder#setAutoCancel(boolean)
  
  # on click open App
  if bool(kwargs.get("open_mActivity")) : builder.setContentIntent(get_mActivity_pending_intent())  # bind on click open app-Mainactivity

  # helpfull for updates 
  builder.setOnlyAlertOnce(True)

  # API 33+ 
  if SDK_INT >= 33 :
    if check_permission(Permission.POST_NOTIFICATIONS):
      manager.notify(notification_id, builder.build())
    else : print("POST_NOTIFICATIONS not granted...") ; request_permissions([Permission.POST_NOTIFICATIONS]) ; return

  # Show the notification
  else : manager.notify(notification_id, builder.build())

  return notification_id

