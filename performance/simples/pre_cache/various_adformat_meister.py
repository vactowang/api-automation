from performance.tasks.realtime_pre_cache_apis import *


class various_adformat_meister(TaskSet):

    def on_start(self):
        """ on_start is called when the TaskSet is starting """
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    tasks = {vungle_mraid.hb_mrec_meister_precached: 1, vungle_mraid.hb_banner_meister_precached: 1,
             vungle_mraid.hb_video_meister_precached: 1}



