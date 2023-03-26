from settings import test_common_os

if test_common_os == 'android':
    from performance.tasks.android_auto_precaching_only_apis import *
else:
    from performance.tasks.ios_auto_precaching_only_apis import *




class various_adformat_meister_hb(TaskSet):

    def on_start(self):
        """ on_start is called when the TaskSet is starting """
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    tasks = {vungle_mraid_ios.hb_full_screen_kraken: 1,
             # vungle_mraid_ios.hb_image_mrec_kraken: 1, vungle_mraid_ios.hb_video_mrec_kraken: 1,
             }



class various_adformat_meister_non_hb(TaskSet):

    def on_start(self):
        """ on_start is called when the TaskSet is starting """
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    tasks = {vungle_mraid_ios.non_hb_full_screen_meister: 1, vungle_mraid_ios.non_hb_banner_meister: 1,
             vungle_mraid_ios.non_hb_image_mrec_meister: 1, vungle_mraid_ios.non_hb_video_mrec_meister: 1,
             legacy_ios.non_hb_video_meister: 1}





