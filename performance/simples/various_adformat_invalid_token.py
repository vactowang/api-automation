from settings import test_common_os



if test_common_os == 'android':
    from performance.tasks.android_auto_precaching_only_apis import *
else:
    from performance.tasks.ios_auto_precaching_only_apis import *


class various_adformat_invalid_token(TaskSet):

    def on_start(self):
        """ on_start is called when the TaskSet is starting """
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    tasks = {vungle_mraid.hb_full_screen_invalid: 1, vungle_mraid.hb_banner_invalid: 1,
             vungle_mraid.hb_image_mrec_invalid: 1,
             vungle_mraid.hb_video_mrec_invalid: 1, programmatic_vast.hb_video_Kraken_invalid: 1,
             programmatic_mraid.hb_banner_Kraken_invalid: 1, programmatic_mraid.hb_mrec_Kraken_invalid: 1}






