from locust import HttpUser, between
from performance.simples.various_adformat_hbp import *
from performance.generate_token_file import main
from locust import LoadTestShape
import math


class WebsiteUser(HttpUser):
    host = HBP_HOST
    main()
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    tasks = {vungle_mraid_ios.hb_full_screen_hbp_meister: 2, vungle_mraid_ios.hb_image_mrec_hbp_meister: 1,
             vungle_mraid_ios.hb_video_mrec_hbp_meister: 1}


#
# class StepLoadShape(LoadTestShape):
#     """
#     A step load shape
#     Keyword arguments:
#         step_time -- Time between steps
#         step_load -- User increase amount at each step
#         spawn_rate -- Users to stop/start per second at every step
#         time_limit -- Time limit in seconds
#     """
#
#     step_time = 120
#     step_load = 10
#     spawn_rate = 1
#     time_limit = 60000000000
#
#     def tick(self):
#         run_time = self.get_run_time()
#
#         if run_time > self.time_limit:
#             return None
#
#         current_step = math.floor(run_time / self.step_time) + 1
#
#         return (current_step * self.step_load, self.spawn_rate)

