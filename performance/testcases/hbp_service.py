from locust import HttpUser, between
from performance.simples.various_adformat_hbp import *
from performance.simples.real_time_only import request_with_test_mode
from performance.generate_token_file import main
from locust import LoadTestShape

import math


class WebsiteUser(HttpUser):
    host = HBP_HOST
    main()
    # main('real_time')
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    tasks = {vungle_mraid_ios.hb_full_screen_hbp_meister,
             vungle_mraid_ios.hb_image_mrec_hbp_meister}





