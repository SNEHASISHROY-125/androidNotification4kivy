from kivy.app import App
from kivy.uix.button import Button

import Notify


class NotifyApp(App):

  def build(self):
    btn = Button(text="notify test")
    btn.bind(on_release=self.notify)
    return btn


  def notify(self,*args):
    print("showing Notification!")
    Notify.notify(
      title="Demo Notification",
      large_icon="congrats_image.jpg",
      content="The custom close button (round ❌ icon on the right) is not a standard Android NotificationCompat.Action button.",
      expanded_image="congrats_image.jpg",
      Action=[
        {
          "name" : "Reset",
          "intent_filter" : "com.example.ACTION_RESET",
          "action_class" : "org.test.notify.ResetReceiver",
          "data" : {
            "ADDRESS" : "localhost"
            }
        },
      ],
      open_mActivity=True
    )

NotifyApp().run()