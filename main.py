from kivy.app import App
from kivy.uix.button import Button

from threading import Thread

from Notify import (
    notify, 
    parcel_notification, 
    show_social_profile,
    show_upload_download,
    start_tcp_server
)


class NotifyApp(App):

  def build(self):
    btn = Button(text="notify test")
    btn.bind(on_release=self.btn_notify)
    return btn

  def on_start(self):
    start_tcp_server(
      {
        'show_parcel_notification' : parcel_notification,
        'show_up_down_speed' : show_upload_download,
        'show_social_profile' : show_social_profile,
        'notify_base' : notify,
      }
    )

  def btn_notify(self,*args):
    print("showing Notification!")
    notify(
      title="Demo Notification",
      large_icon="congrats_image.jpg",
      content="The custom close button (round ❌ icon on the right) is not a standard Android NotificationCompat.Action button.",
      expanded_image="congrats_image.jpg",
      Action=[
        {
          "name" : "Reset",
          "intent_filter" : "com.snehasys.notify",
          "action_class" : "com.snehasys.notify.ResetReceiver",
          "data" : {
            "ADDRESS" : "/dismiss",
            }
        },
      ],
      open_mActivity=True
    )

NotifyApp().run()