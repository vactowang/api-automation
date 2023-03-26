from locust import HttpUser, between
from performance.simples.real_time_only.real_time_various_adformat_mixed_mid_meister import *

from performance.common.config import *
from performance.generate_token_file import main


class WebsiteUser(HttpUser):
    host = HBP_HOST
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    main('real_time')
    tasks = {various_adformat_precached_meister: 1}


