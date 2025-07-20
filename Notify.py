from kivy.app import App
from kivy.uix.button import Button

## Notification
from jnius import autoclass, cast
from android import activity
from android.permissions import request_permissions, check_permission,Permission

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


manager = getattr(NotificationManagerCompat, "from")(context)

import random , datetime


Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')

def action_button_pending_intent(pid:int,intent_filter,action_class,data:dict):
  # ACTION NAME must match manifest
  action_intent = Intent(intent_filter)  # "com.example.ACTION_RESET" in mainfest
  action_intent.setClassName(context.getPackageName(), action_class)   # "org.test.notify.ResetReceiver" in mainfest

  # put data to retrive in java
  action_intent.putExtra("NOTIFID",pid)
  # set additional data
  for key in data.keys():
    action_intent.putExtra(key, data.get(key))

  action_pending_intent = PendingIntent.getBroadcast(
      context, pid, action_intent,
      PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
  )
  return action_pending_intent

# Deprecated so avoid using in upcomming API  | tested on API.36 works fine
# .addAction(Notification.Action) as recomended :TODO
# builder.addAction(context.getApplicationInfo().icon, "Reset", action_pending_intent)

JavaString = autoclass('java.lang.String')

def to_signed_int32(val):
    return val if val < 0x80000000 else val - 0x100000000

def notify(**kwargs):
  '''
  *title  ``notification title``
  *content ``notification content text``
  *small_icon ``notification small-icon-right``
  *large_icon ``notification large-icon-left``
  *big_content ``huge notification content text``
  *Action:list ``Action Button Data [action1:dict, action2:dict, action3:dict] | max 3 Action buttons``
  *expanded_image ``notification big-image when expanded``
  *dismissable:bool ``user can't dismiss notification``
  *progress_value:int ``progress bar value | max:100``
  *open_mActivity:bool ``notification on click opens App activity``  
  '''
  # pid:
  pid = random.randint(0, 32767) 
  id = int(datetime.datetime.now().strftime("%H%M%S"))  # it generates 6-digit but I found trouble using it with .putExtra(Bundle) :TODO
  # Build notification with BigPictureStyle
  builder = NotificationCompatBuilder(context, channel_id)
  # notification title
  if kwargs.get("title") : builder.setContentTitle(kwargs['title'])
  else: builder.setContentTitle("New Image Notification")
  # notification text
  if kwargs.get("content") : builder.setContentText(kwargs["content"]) 
  else: builder.setContentText("Check out this image!")
  # small tiny icon
  if kwargs.get("small_icon") : builder.setSmallIcon(kwargs["small_icon"]) 
  else: builder.setSmallIcon(context.getApplicationInfo().icon)
  # icon on left
  if kwargs.get("large_icon") : builder.setLargeIcon(load(kwargs['large_icon'])) 
  else: builder.setLargeIcon(load('congrats_image.jpg'))
  # big text when expanded
  if kwargs.get("big_content") : builder.setStyle(BigTextStyle().bigText(kwargs["big_content"]))   #### Either Big-picture or Big-ext ##
  # image when expaned
  if kwargs.get("expanded_image") and not kwargs.get("big_content") : builder.setStyle(BigPictureStyle().bigPicture(load(kwargs["expanded_image"])))
  # progress bar
  if kwargs.get("progress_value") : builder.setProgress(100, kwargs["progress_value"], False); # false = determinate
  # sticky notification
  if kwargs.get("dismissable") : builder.setOngoing(True)   # https://developer.android.com/reference/android/app/Notification.Builder#setOngoing(boolean)  | works api <=36 
  # Action Button
  ''' As of Android Build.VERSION_CODES.S, apps targeting API level Build.VERSION_CODES.S or higher 
      won't be able to start activities while processing broadcast receivers or services in response to notification action clicks. 
      To launch an activity in those cases, provide a PendingIntent for the activity itself.  :TODO'''
  if kwargs.get("Action"):
    for action in kwargs["Action"]:
      builder.addAction(context.getApplicationInfo().icon, JavaString(action.get("name")) , action_button_pending_intent(pid,action["intent_filter"],action["action_class"],data=action["data"]))
  
  # Auto dismiss-timeout    https://developer.android.com/reference/android/app/Notification.Builder#setTimeoutAfter(long)
  if kwargs.get("MS") : builder.setTimeoutAfter(kwargs["MS"]) # long: durationMs 1s = 1000ms

  # Colorize  
  if kwargs.get("color"):
    builder.setColor(to_signed_int32(kwargs["color"]));      # 0xFFFF5722 Orange color  | worked on api.28 :TODO newer api's
    builder.setColorized(True);        # Enable full background coloring
  
  # Time-Count Meter
  # builder.setWhen(System.currentTimeMillis()).setUsesChronometer(true)   # https://developer.android.com/reference/android/app/Notification.Builder#setUsesChronometer(boolean)
  # .setChronometerCountDown(boolean)   # count in reverse
  
  builder.setPriority(NotificationCompat.PRIORITY_HIGH)   # https://developer.android.com/reference/android/app/Notification.Builder#setPriority(int)
  # other FLAGS : PRIORITY_LOW | PRIORITY_DEFAULT | PRIORITY_MAX  | PRIORITY_MIN    https://developer.android.com/reference/android/app/Notification#PRIORITY_DEFAULT
  
  builder.setVisibility(NotificationCompat.VISIBILITY_PUBLIC) # lock-screen visibility  https://developer.android.com/reference/android/app/Notification.Builder#setPublicVersion(android.app.Notification)
  # other FLAGS : VISIBILITY_PRIVATE | VISIBILITY_SECRET https://developer.android.com/reference/android/app/Notification#VISIBILITY_PRIVATE
  
  # Make this notificatSion automatically dismissed when the user touches it.
  builder.setAutoCancel(True)   # https://developer.android.com/reference/android/app/Notification.Builder#setAutoCancel(boolean)
  
  # on click open App
  if kwargs.get("open_mActivity") : builder.setContentIntent(get_mActivity_pending_intent())  # bind on click open app-Mainactivity

  # API 33+ 
  if SDK_INT >= 33 :
    if check_permission(Permission.POST_NOTIFICATIONS):
      manager.notify(pid, builder.build())
    else : print("POST_NOTIFICATIONS not granted...") ; request_permissions([Permission.POST_NOTIFICATIONS]) ; return

  # Show the notification
  else : manager.notify(pid, builder.build())



class Notify(App):

  def build(self):
    btn = Button(text="notify test")
    btn.bind(on_release=self.notify)
    return btn


  def notify(self,*args):
    print("showing Notification!")
    notify()

Notify().run()