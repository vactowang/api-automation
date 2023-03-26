from settings import *
from utils.s3_access import upload_file


class TestPrepareKrakenAds(object):

    def test_jaeger_prepare_test_ads(self):
        kraken_meta_ext_file = 'data/kraken_ads/meta_ext_reg.json'
        kraken_meta_file = 'data/kraken_ads/meta.json'
        target_meta_ext = 'test-model/meta_ext.json'
        target_meta = 'test-model/meta.json'
        upload_file(kraken_meta_file, kraken_s3_bucket_qa, target_meta)
        upload_file(kraken_meta_ext_file, kraken_s3_bucket_qa, target_meta_ext)

    def test_jaeger_rollback_test_ads(self):
        kraken_meta_ext_file = 'data/kraken_ads/meta_ext.json'
        target = 'test-model/meta_ext.json'
        upload_file(kraken_meta_ext_file, kraken_s3_bucket_qa, target)