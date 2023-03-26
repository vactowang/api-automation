from settings import test_common_os

if test_common_os == 'android':
    from performance.tasks.android_auto_precaching_only_apis import *
else :
    from performance.tasks.ios_auto_precaching_only_apis import *



class various_adformat_kraken_hb(TaskSet):


    def on_start(self):

        """ on_start is called when the TaskSet is starting """
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    tasks = {vungle_mraid_ios.hb_full_screen_kraken: 1,
             vungle_mraid_ios.hb_image_mrec_kraken: 1,
             vungle_mraid_ios.hb_video_mrec_kraken: 1,
            }


class various_adformat_kraken_non_hb(TaskSet):

    def on_start(self):
        """ on_start is called when the TaskSet is starting """
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    tasks = {vungle_mraid_ios.non_hb_full_screen_kraken: 1, vungle_mraid_ios.non_hb_banner_kraken: 1,
             vungle_mraid_ios.non_hb_image_mrec_kraken: 1, vungle_mraid_ios.non_hb_video_mrec_kraken: 1,
             programmatic_vast_ios.non_hb_video_Kraken: 1,
             programmatic_mraid_ios.non_hb_banner_Kraken: 1, programmatic_mraid_ios.non_hb_mrec_Kraken: 1}
