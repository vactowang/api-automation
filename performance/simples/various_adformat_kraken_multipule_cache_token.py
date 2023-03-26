from settings import test_common_os



if test_common_os == 'android':
    from performance.tasks.android_auto_precaching_only_apis import *
else:
    from performance.tasks.ios_auto_precaching_only_apis import *


class various_adformat_Kraken_multipule_cache_token(TaskSet):

    def on_start(self):
        """ on_start is called when the TaskSet is starting """
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    tasks = {vungle_mraid_ios.hb_full_screen_kraken_multiple_cache: 1, vungle_mraid_ios.hb_banner_kraken_multiple_cache: 1,
             vungle_mraid_ios.hb_image_mrec_kraken_multiple_cache: 1, vungle_mraid_ios.hb_video_mrec_kraken_multiple_cache: 1,
             programmatic_vast_ios.hb_video_Kraken_multiple_cache: 1,
             programmatic_mraid_ios.hb_banner_Kraken_multiple_cache: 1}






