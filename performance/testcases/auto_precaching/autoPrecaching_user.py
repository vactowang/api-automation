from locust import HttpUser, between
from performance.simples.pre_cache.various_adformat_kraken import *
from performance.generate_token_file import main
from performance.common.config import *
from locust import LoadTestShape
import math


class WebsiteUser(HttpUser):
    host = HBP_HOST
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    main('real_time')
    tasks = {various_adformat_kraken}

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
#     step_time = 600
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
