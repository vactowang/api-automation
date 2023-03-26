from performance.tasks.realtime_ad_only_apis import *


class various_adformat_invalid_token(TaskSet):

    def on_start(self):
        """ on_start is called when the TaskSet is starting """
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    tasks = {vungle_mraid.hb_full_screen_invalid, vungle_mraid.hb_banner_invalid,
             vungle_mraid.hb_video_mrec_invalid,
          }






