import sys
import logging
import boto3
from botocore.exceptions import ClientError


service = str(sys.argv[1])
operation = str(sys.argv[2])

kraken_s3_bucket_qa = 'vungle2-cdn-qa'


class EnvPrepare():

    def upload_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        if object_name is None:
            object_name = file_name

        s3_client = boto3.client('s3')
        try:
            s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def jaeger_prepare_test_ad(self):
        kraken_meta_ext_file = '../data/kraken_ads/meta_ext_reg.json'
        kraken_meta_file = '../data/kraken_ads/meta.json'
        target_meta_ext = 'test-model/meta_ext.json'
        target_meta = 'test-model/meta.json'

        self.upload_file(kraken_meta_file, kraken_s3_bucket_qa, target_meta)
        self.upload_file(kraken_meta_ext_file, kraken_s3_bucket_qa, target_meta_ext)

    def jaeger_rollback_test_ad(self):
        kraken_meta_ext_file = '../data/kraken_ads/meta_ext.json'
        target = 'test-model/meta_ext.json'
        self.upload_file(kraken_meta_ext_file, kraken_s3_bucket_qa, target)


if __name__ == '__main__':
    env_prepare = EnvPrepare()
    if service == 'jaeger':
        if operation == 'setup':
            env_prepare.jaeger_prepare_test_ad()
        elif operation == 'rollback':
            env_prepare.jaeger_rollback_test_ad()