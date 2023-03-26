from locust import HttpUser, between
from performance.simples.pre_cache.various_adformat_meister import *
from performance.simples.various_adformat_meister import various_adformat_meister_non_hb
from performance.generate_token_file import main
from performance.common.config import *


class WebsiteUser(HttpUser):
    host = HBP_HOST
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    main()
    main('real_time')
    tasks = {various_adformat_meister: 1, various_adformat_meister_non_hb: 1}


