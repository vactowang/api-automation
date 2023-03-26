from locust import HttpUser, between
from performance.simples.real_time_only.real_time_various_adformat_kraken import *
from performance.simples.various_adformat_kraken import various_adformat_kraken_non_hb
from performance.generate_token_file import main
from performance.common.config import *


class WebsiteUser(HttpUser):
    host = HBP_HOST
    wait_time = between(WAIT_TIME_FROM, WAIT_TIME_TO)
    main()
    main('real_time')
    tasks = {various_adformat_precached_kraken: 1,
             various_adformat_kraken_non_hb: 1}


