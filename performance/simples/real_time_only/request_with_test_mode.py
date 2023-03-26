from performance.tasks.realtime_ad_only_apis import *


class various_adformat_test_mode_meister(TaskSet):

    def on_start(self):
        """ on_start is called when the TaskSet is starting """
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    tasks = {vungle_mraid.hb_video_hbp_meister_precached}

    # tasks = {vungle_mraid.hb_banner_hbp_meister_precached, vungle_mraid.hb_video_hbp_meister_precached,
    #          vungle_mraid.hb_hbp_mrec_meister_precached}




class various_adformat_test_mode_kraken(TaskSet):

    def on_start(self):
        """ on_start is called when the TaskSet is starting """
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    tasks = {vungle_mraid.hb_video_kraken_precached}



