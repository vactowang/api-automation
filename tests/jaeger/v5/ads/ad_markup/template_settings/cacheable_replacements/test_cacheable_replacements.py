import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestCacheableReplacements(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('cacheable replacements')
    @allure.description('Verify cacheable replacements font url from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_cacheable_replacements_font_url(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(str(cacheable_replacements['FONT_URL']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['FONT_URL'])

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('cacheable replacements')
    @allure.description('Verify cacheable replacements main video from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_cacheable_replacements_main_video(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(str(cacheable_replacements['MAIN_VIDEO']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['MAIN_VIDEO'])

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('cacheable replacements')
    @allure.description('Verify cacheable replacements vungle info from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_cacheable_replacements_vungle_info(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(str(cacheable_replacements['POWERED_BY_VUNGLE']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['POWERED_BY_VUNGLE'])

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('cacheable replacements')
    @allure.description('Verify cacheable replacements app icon from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_cacheable_replacements_app_icon(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(str(cacheable_replacements['APP_ICON']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['APP_ICON'])

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('cacheable replacements')
    @allure.description('Verify cacheable replacements app rating from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_cacheable_replacements_app_rating(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(str(cacheable_replacements['APP_RATING']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['APP_RATING'])


    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1359 programmatic end card'
                  'PBJ-4899 Sunset customized endcard for bytedance')
    @allure.description('Verify the programmatic end card info in cacheable replacements')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_programmatic_end_card_info_cacheable_replacements(self, pub_app_id):
        '''
        End card info in vast adm:
            <![CDATA[<EndCardAdParameters>
              <cover_url>http://sf3-ttcdn-tos.pstatp.com/obj/ad.union.api/30860ab264d086db052bea3b76e17e73</cover_url>
              <icon>http://sf3-ttcdn-tos.pstatp.com/obj/web.business.image/202002135d0d86dc9a765bca41948ec9</icon>
              <app_name>疯狂猜成语-红包版</app_name>
              <description>休闲小游戏，躺着玩游戏就能赚钱，随时可以提现</description>
              <app_stars>4.5</app_stars>
              <button_text>立即下载</button_text>
              <download_url>https://www.crazyccy.com/download/ccy_csjfkccy313.apk</download_url>
            </EndCardAdParameters>]]>
        '''
        override_adm = 'seatbid.0.bid.0.adm@"<VAST version=\\"2.0\\"><Ad><InLine><AdSystem><![CDATA[Bytedance]]><\\/AdSystem><AdTitle><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\/AdTitle><Impression><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/show_event\\/?req_id=5ec796d603e1e7c01267c88fu8791&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&source_type=1&pack_time=1590630440.65&pc=OMkaunPpDyKzZarhJKk3BmafV%2FjcG%2FID2AgSFwMkc6M%3D&ttdsp_price=${AUCTION_PRICE}]]><\\/Impression><Creatives><Creative id=\\"1665015151804428\\"><Linear><Duration>00:00:46<\\/Duration><TrackingEvents><Tracking event=\\"start\\"><![CDATA[https:\\/\\/is.snssdk.com\\/api\\/ad\\/union\\/event_report\\/?event_type=4&user_timezone={timezone}&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=0]]><\\/Tracking><Tracking event=\\"complete\\"><![CDATA[https:\\/\\/is.snssdk.com\\/api\\/ad\\/union\\/event_report\\/?event_type=6&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=27]]><\\/Tracking><Tracking event=\\"creativeView\\"><![CDATA[http:\\/\\/app05.adfalcon.com\\/E\\/78c1743833b34d43991083f92bd5b392_0_b338d452-96f4-4d37-b6e1-d10de8271ff4?ev=creativeview]]><\\/Tracking><\\/TrackingEvents><VideoClicks><ClickThrough><![CDATA[https:\\/\\/events-dca.bidder.kayzen.io\\/click?ppid=313f8c39-0eb3-45ad-88ff-891559d47302&raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\/ClickThrough><ClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=1&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/ClickTracking><CustomClick id=\\"ClickCoordinates-1\\"><![CDATA[https:\\/\\/c2.gdt.qq.com\\/gdt_mclick.fcg?viewid=!s6A4zH!POBbWj7ZQJudpxTBaTzOitZ8Zrj2cUWt!HRqifXlxVXVFYsSbE41QXp8NkVBskWi5Xu3It3wZDq05WhMsgfMLVxU41AQqVoe3wHYs6zZtEO_OtSDOHBiIm_Jn3xRWbR93zoDNI2kpylT7ltMreMCvonlVZ2Br0DCTf8SQOYklg8NNwTiMJCaTcC4xb7pIVEr5A5nkmccS3H9UpiMiJTk3eT_Yn57f4UxnMy9cxrAgVDosJFLJ6rXP6tZHCWVS3kSr0l5iRK1V956hwoVlIAVZCLcI!!qfcKzeS548ctKsM2Ps6ip5M9Cpx60&jtype=0&i=1&os=2&acttype=1&s={\\"req_width\\":\\"__REQ_WIDTH__\\",\\"req_height\\":\\"__REQ_HEIGHT__\\",\\"width\\":\\"__WIDTH__\\",\\"height\\":\\"__HEIGHT__\\",\\"down_x\\":\\"__DOWN_X__\\",\\"down_y\\":\\"__DOWN_Y__\\",\\"up_x\\":\\"__UP_X__\\",\\"up_y\\":\\"__UP_Y__\\"}&lpp=click_ext=eyJleHBfcGFyYW0iOiJjYXJyaWVyX2VuYWJsZToyIn0=&clklpp=__CLICK_LPP__&nxjp=1&cdnxj=1&xp=1&tl=1]]><\\/CustomClick><CustomClick id=\\"ClickCoordinates-2\\"><![CDATA[http:\\/\\/link\\/to\\/customclick\\/2]]><\\/CustomClick><CustomClick id=\\"customclick-3\\"><![CDATA[http:\\/\\/link\\/to\\/customclick\\/3]]><\\/CustomClick><\\/VideoClicks><MediaFiles><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[ asdjfklajsd;fkja;sdlkfjklasdjfklasdjfkl.mp4 ]]><\\/MediaFile><MediaFile bitrate=\\"206\\" delivery=\\"progressive\\" height=\\"180\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"320\\"><![CDATA[ test\\/jsldfjlksdfjk.mp4 ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[ v3-ad.ixigua.com\\/kghkhk\\/toutiao123werwerew.abc ]]><\\/MediaFile><MediaFile bitrate=\\"56\\" delivery=\\"progressive\\" height=\\"144\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"176\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/17\\/source\\/doubleclick_dmm\\/ctier\\/L\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748511\\/sparams\\/id,itag,source,ctier,ip,ipbits,expire\\/signature\\/8044BE9E3E1793FF36C03998BA13848E7C845ABE.75B6CAFBF57F6F96C78BDFCEB9653E601FD7E8D8\\/key\\/ck2\\/file\\/file.3gpp ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[https:\\/\\/v3-ad.ixigua.com\\/kghkhk\\/toutiao123]]><\\/MediaFile><MediaFile bitrate=\\"206\\" delivery=\\"progressive\\" height=\\"180\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"320\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/36\\/source\\/doubleclick_dmm\\/ctier\\/L\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748512\\/sparams\\/id,itag,source,ctier,ip,ipbits,expire\\/signature\\/29EC5A3574F0873D71FF75DEA54B89FD30A0D0B1.82B0C3EBBBAF7046A8DFBF3D94AAD9FC69C5C9A4\\/key\\/ck2\\/file\\/file.3gpp ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[https:\\/\\/cdn-cn.vungle.cn\\/zen\\/497a5dead8498d62d7c65967729639f7-1280x720-Q2.mp4]]><\\/MediaFile><MediaFile bitrate=\\"372\\" delivery=\\"progressive\\" height=\\"360\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/mp4\\" width=\\"640\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/18\\/source\\/doubleclick_dmm\\/ctier\\/L\\/acao\\/yes\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748513\\/sparams\\/id,itag,source,ctier,acao,ip,ipbits,expire\\/signature\\/484784AD6E9C1516EC07970AB978D11555654A9A.57EFB4F5F3CCE7F30CFBA1951E6434319300BE12\\/key\\/ck2\\/file\\/file.mp4 ]]><\\/MediaFile><MediaFile bitrate=\\"1879\\" delivery=\\"progressive\\" height=\\"720\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/mp4\\" width=\\"1280\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/22\\/source\\/doubleclick_dmm\\/ctier\\/L\\/acao\\/yes\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748528\\/sparams\\/id,itag,source,ctier,acao,ip,ipbits,expire\\/signature\\/7136B1FF2CD283E5A90276E455C5F970B91A35FF.8E6707BA3249059D7BA09F6E3D59FF6BA1D78FE0\\/key\\/ck2\\/file\\/file.mp4 ]]><\\/MediaFile><\\/MediaFiles><\\/Linear><\\/Creative><Creative><CompanionAds><Companion id=\\"post-roll\\" width=\\"1280\\" height=\\"720\\"><CompanionClickThrough><![CDATA[https:\\/\\/events-dca.bidder.kayzen.io\\/click?raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\/CompanionClickThrough><CompanionClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=2&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/CompanionClickTracking><TrackingEvents><Tracking event=\\"creativeView\\"><\\/Tracking><\\/TrackingEvents><StaticResource creativeType=\\"image\\/jpeg\\"><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/obj\\/mosaic-legacy\\/2ff3f000e60c223e67984]]><\\/StaticResource><\\/Companion><Companion id=\\"vungle_endcard_v1\\"><CompanionClickThrough><![CDATA[https:\\/\\/events-dca.bidder.kayzen.io\\/click?raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\/CompanionClickThrough><CompanionClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=2&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/CompanionClickTracking><TrackingEvents><\\/TrackingEvents><AdParameters xmlEncoded=\\"true\\"><![CDATA[<EndCardAdParameters><icon>https:\\/\\/p3-tt.byteimg.com\\/img\\/ad.union.api\\/7c51525c9163b92843a26bf89aaded1f~100x100.image<\\/icon><app_name>\\u70B9\\u4EAE\\u57CE\\u5E02-\\u5168\\u7F51\\u5F00\\u670D<\\/app_name><cover_url>https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/mosaic-legacy\\/2ff3f000e60c223e67984~noop.jpg<\\/cover_url><app_stars>5<\\/app_stars><button_text>\\u70B9\\u51FB\\u4E0B\\u8F7D<\\/button_text><download_url>https%3A%2F%2Fwww.crazyccy.com%2Fdownload%2Fccy_csjfkccy313.apk<\\/download_url><description>\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417<\\/description><\\/EndCardAdParameters>]]><\\/AdParameters><\\/Companion><\\/CompanionAds><\\/Creative><\\/Creatives><Description><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\/Description><Survey><\\/Survey><Extensions><Extension type=\\"AdVerifications\\"><AdVerifications><Verification vendor=\\"moat.com-omsdkvungleinappvideo781943494431\\"><JavaScriptResource apiFramework=\\"omid\\" browserOptional=\\"true\\"><![CDATA[https:\\/\\/z.moatads.com\\/omsdkvungleinappvideo781943494431\\/moatvideo.js]]><\\/JavaScriptResource><VerificationParameters><![CDATA[{\\"moatClientLevel1\\":\\"{{{app_id}}}\\",\\"moatClientLevel2\\":\\"{{{campaign_id}}}\\",\\"moatClientLevel3\\":\\"{{{creative_id}}}\\",\\"moatClientLevel4\\":\\"{{{placement_id}}}\\",\\"moatClientSlicer1\\":\\"{{{pub_app_id}}}\\",\\"moatClientLevel5\\":\\"{{{rtb_deal_id}}}\\",\\"moatClientLevel6\\":\\"{{{rtb_connection_id}}}\\"}]]><\\/VerificationParameters><\\/Verification><\\/AdVerifications><\\/Extension><Extension type=\\"Extra\\"><CTA><![CDATA[\\u70B9\\u51FB\\u4E0B\\u8F7D]]><\\/CTA><SystemIcon><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/07c04164de3140d2cfe4bdd9812aef22~c1_0x0_q100.png]]><\\/SystemIcon><FullStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/48c275deda9f2daa92acccf8218fc59f~c1_0x0_q100.jpeg]]><\\/FullStar><HalfStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/b273598ab25fec09a467d2b895e3c53e~c1_0x0_q100.jpeg]]><\\/HalfStar><EmptyStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/fedbae142b79804e383eed3f4d06e9d5~c1_0x0_q100.jpeg]]><\\/EmptyStar><Review><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/297845a2690ec96bd1290a0a289ab373~c1_0x0_q100.jpeg]]><\\/Review><MoPubCtaText><\\/MoPubCtaText><\\/Extension><\\/Extensions><\\/InLine><\\/Ad><\\/VAST>"'
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        override_bid_response_any=override_adm))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm'] and 'templateSettings' in ad_markup:
            cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_keys_not_exist(cacheable_replacements, 'BACKGROUND_IMAGE')  # cover_url
            assert_keys_not_exist(cacheable_replacements, 'APP_ICON')  # icon

    @allure.feature('static image end card')
    @allure.tag('normal', 'test_mode', 'R_1.125.0')
    @allure.story('PBJ-1498 Jaeger can support static image and html endcard'
                  'PBJ-4899 Sunset customized endcard for bytedance')
    @allure.description('Verify cacheable template info of the static image end card inside China')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_static_image_end_card_china(self, pub_app_id):
        '''
        End card info in vast adm:
            <![CDATA[<EndCardAdParameters>
                <icon>https://p3-tt.byteimg.com/img/ad.union.api/7c51525c9163b92843a26bf89aaded1f~100x100.image</icon>
                <app_name>点亮城市-全网开服</app_name>
                <cover_url>https://sf1-ttcdn-tos.pstatp.com/img/mosaic-legacy/2ff3f000e60c223e67984~noop.jpg</cover_url>
                <app_stars>5</app_stars><button_text>点击下载</button_text>
                <download_url>https://apps.apple.com/cn/app/id1490962424</download_url>
                <description>只有5%的人能点亮整座城市，你敢挑战吗</description>
            </EndCardAdParameters>]]>
        '''
        override_adm = 'seatbid.0.bid.0.adm@"<VAST version=\\"2.0\\"><Ad><InLine><AdSystem><![CDATA[Bytedance]]><\\/AdSystem><AdTitle><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\/AdTitle><Impression><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/show_event\\/?req_id=5ec796d603e1e7c01267c88fu8791&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&source_type=1&pack_time=1590630440.65&pc=OMkaunPpDyKzZarhJKk3BmafV%2FjcG%2FID2AgSFwMkc6M%3D&ttdsp_price=${AUCTION_PRICE}]]><\\/Impression><Creatives><Creative id=\\"1665015151804428\\"><Linear><Duration>00:00:46<\\/Duration><TrackingEvents><Tracking event=\\"start\\"><![CDATA[https:\\/\\/is.snssdk.com\\/api\\/ad\\/union\\/event_report\\/?event_type=4&user_timezone={timezone}&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=0]]><\\/Tracking><Tracking event=\\"complete\\"><![CDATA[https:\\/\\/is.snssdk.com\\/api\\/ad\\/union\\/event_report\\/?event_type=6&extra=4AfhtQRp22DGOBvA5zI0lS%2FcT%2Bw9JJgawOAhIgmdGSHq9mhg2WowlxaVMCnpX9aEnCvZlJ%2F4XnX9Y3ft9EE3jGL6S2ry5oiX6rZbqXq0sxJUwk6QzU%2B01i3d7ImYEWp6enFEt09MtFFv7b48W%2FZZvC%2BTQVUys9SLkZnSUnYc6Q5CX7dTPTqNbxlIs9nqK1F0KLvOxM8q%2Bm1Gz900kSWp4GY%2Fz1AO7%2Bhn43CSs46qVMvHQ5qlcUHNwDBVEqvR%2BZMvsoAwtPPCEEtn1bsriy4PSRosSNLnm5t2jwE%2FnBnj0SlvoC66lIy28a6hdhzOy4LIKGaiuXVujp6TxDzCdjpA7X1Szd%2FrjdCgbfI%2BLcYoeol23e%2BBmoUgqX%2FH%2F7WphfNoIJSQSOnGyTHlCY6H1w2t1E3sg51A4D3JWIVLB2WYzF448pt09nqylG1mJuc6HKOlKdmaXQsLMnmKHg9gVPU5nCTYzRFKx95hlxv%2BexR%2FwUWA%2FFAoOIKyfLDu%2BD6jnvnQ0%2FQKX8EkYvroCF8vbwYCC00trnzQxrzwYJLwPQirebVH7Oahrqz9GC0AWA9eA97aF%2BP4luLedTXeRXiOaV2Z9Ve%2FUiPgVId9oybFaJRbfTHpqGdCCqHmVYhy%2FEsO5Cc%2BQUqd%2FkRSRiqMTFCGbldY2yDqSZw64N8nuy8Q96AyqFxx8c6WzQYgrnl3hNW0h4z9xcGUrpHYMZ77Ur3slw9NZ0bKa57Vabhdr1x5OYeiS7vIzRDpCAbpuj6DfmvWMLp348CcYnwzWuKpXMO3dVopSQ5g9mhqW%2BFMNVwkq1Am9qT1qrLfa%2B1dQEw%2Fy0wIRDiehbfWn6k2HjSptp3j%2BzS4WKomHeWEC4bVofpOKx4hEF73kGEvxzfPjo%2FvM4xTiuH8Fw%2Ftwx3xR%2BCjABzmEmzPMsoGOGdHiGnkYWYekOUmFS8h%2Fi8Jw2JqzHfZF8f%2F2K1dh1jvULJ4N43QBPb4lsbmYS4T6K65SKkJmjYlq4eaFeXjKk40r9KIYmbHhRBeXnFBvc%2FXLPIReEDDLC9HXmnll%2FdgY3JD1e8RBDzUgdF7cRmJDlocZqnJEOFEoT9LO1JpiU4hH7xEXEFul4Z6EgM97YXTfqEBYeQ%2FftyIee07L%2Fo%2Fx0nUdi1El42uLyPyvwzVbzHFeUBprI1M0Svxq1KERKrTVQz%2Fxmxx4YkPhOeU2CmA9cv8IUhsaf%2F%2FCw%2F%2Fv2wwjcZeJG4gdeHp9CfteShvQokMKtq3clCiTf4WkYf9AcgobPOxy6bXQku9aycXoVNKtl%2F4cM9rOe25AwjBFkatpfkUTiOjQVLf5d1me2eUYIU%2FXr1Il4xn%2BbVtahT304xf%2Fy1fQG828mpapX2vSds2dALGa2AFXntrk3%2Bm2KiYKKDSE6MNcn7X80JUWKAcOOZpejPrOYSTo6BN%2BIbvC%2FxTLmn153zkkVvEiaIVVMqwU2aPZX%2FY2PHOkIz9hhSm%2FhQ2%2FDLbizMKEoQ3avvhlz%2B6dP8UlCXQILjqQuoO2sZf80pwEwsBYFAvB2DKRAJzYSsBoTLrjmM4ynP9duq4LGtpakfqjnJdlElsER%2FnWwYQV9OIi3RZPF2EHyjj%2BH7IcqxOAzvK1kyqoC7W8fAWeeDoEvegnTtRwDuzHuP1LsAkQZxB0REPYa0Q%2BP0sn4zipSJv7UHerEHdxSqegawjnqP33o8BrARxatwd1FccDPXVQ%2BARDyQspfmJDFTyw6b%2Fh%2FngyQUsdA8bqAO1Wilg7XdenuaXkNJlXHQaP4bDNS9Q0F94HZiLSmS6OBhgV3IQm79XYxX5%2BlCA%2BEC%2FU%2F6Ec94hNWafV%2FjcG%2FID2AgSFwMkc6M%3D&video_play_time=27]]><\\/Tracking><Tracking event=\\"creativeView\\"><![CDATA[http:\\/\\/app05.adfalcon.com\\/E\\/78c1743833b34d43991083f92bd5b392_0_b338d452-96f4-4d37-b6e1-d10de8271ff4?ev=creativeview]]><\\/Tracking><\\/TrackingEvents><VideoClicks><ClickThrough><![CDATA[https:\\/\\/events-dca.bidder.kayzen.io\\/click?ppid=313f8c39-0eb3-45ad-88ff-891559d47302&raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\/ClickThrough><ClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=1&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/ClickTracking><CustomClick id=\\"ClickCoordinates-1\\"><![CDATA[https:\\/\\/c2.gdt.qq.com\\/gdt_mclick.fcg?viewid=!s6A4zH!POBbWj7ZQJudpxTBaTzOitZ8Zrj2cUWt!HRqifXlxVXVFYsSbE41QXp8NkVBskWi5Xu3It3wZDq05WhMsgfMLVxU41AQqVoe3wHYs6zZtEO_OtSDOHBiIm_Jn3xRWbR93zoDNI2kpylT7ltMreMCvonlVZ2Br0DCTf8SQOYklg8NNwTiMJCaTcC4xb7pIVEr5A5nkmccS3H9UpiMiJTk3eT_Yn57f4UxnMy9cxrAgVDosJFLJ6rXP6tZHCWVS3kSr0l5iRK1V956hwoVlIAVZCLcI!!qfcKzeS548ctKsM2Ps6ip5M9Cpx60&jtype=0&i=1&os=2&acttype=1&s={\\"req_width\\":\\"__REQ_WIDTH__\\",\\"req_height\\":\\"__REQ_HEIGHT__\\",\\"width\\":\\"__WIDTH__\\",\\"height\\":\\"__HEIGHT__\\",\\"down_x\\":\\"__DOWN_X__\\",\\"down_y\\":\\"__DOWN_Y__\\",\\"up_x\\":\\"__UP_X__\\",\\"up_y\\":\\"__UP_Y__\\"}&lpp=click_ext=eyJleHBfcGFyYW0iOiJjYXJyaWVyX2VuYWJsZToyIn0=&clklpp=__CLICK_LPP__&nxjp=1&cdnxj=1&xp=1&tl=1]]><\\/CustomClick><CustomClick id=\\"ClickCoordinates-2\\"><![CDATA[http:\\/\\/link\\/to\\/customclick\\/2]]><\\/CustomClick><CustomClick id=\\"customclick-3\\"><![CDATA[http:\\/\\/link\\/to\\/customclick\\/3]]><\\/CustomClick><\\/VideoClicks><MediaFiles><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[ asdjfklajsd;fkja;sdlkfjklasdjfklasdjfkl.mp4 ]]><\\/MediaFile><MediaFile bitrate=\\"206\\" delivery=\\"progressive\\" height=\\"180\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"320\\"><![CDATA[ test\\/jsldfjlksdfjk.mp4 ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[ v3-ad.ixigua.com\\/kghkhk\\/toutiao123werwerew.abc ]]><\\/MediaFile><MediaFile bitrate=\\"56\\" delivery=\\"progressive\\" height=\\"144\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"176\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/17\\/source\\/doubleclick_dmm\\/ctier\\/L\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748511\\/sparams\\/id,itag,source,ctier,ip,ipbits,expire\\/signature\\/8044BE9E3E1793FF36C03998BA13848E7C845ABE.75B6CAFBF57F6F96C78BDFCEB9653E601FD7E8D8\\/key\\/ck2\\/file\\/file.3gpp ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[https:\\/\\/v3-ad.ixigua.com\\/kghkhk\\/toutiao123]]><\\/MediaFile><MediaFile bitrate=\\"206\\" delivery=\\"progressive\\" height=\\"180\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/3gpp\\" width=\\"320\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/36\\/source\\/doubleclick_dmm\\/ctier\\/L\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748512\\/sparams\\/id,itag,source,ctier,ip,ipbits,expire\\/signature\\/29EC5A3574F0873D71FF75DEA54B89FD30A0D0B1.82B0C3EBBBAF7046A8DFBF3D94AAD9FC69C5C9A4\\/key\\/ck2\\/file\\/file.3gpp ]]><\\/MediaFile><MediaFile delivery=\\"progressive\\" type=\\"video\\/mp4\\" width=\\"1280\\" height=\\"720\\"><![CDATA[https:\\/\\/cdn-cn.vungle.cn\\/zen\\/497a5dead8498d62d7c65967729639f7-1280x720-Q2.mp4]]><\\/MediaFile><MediaFile bitrate=\\"372\\" delivery=\\"progressive\\" height=\\"360\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/mp4\\" width=\\"640\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/18\\/source\\/doubleclick_dmm\\/ctier\\/L\\/acao\\/yes\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748513\\/sparams\\/id,itag,source,ctier,acao,ip,ipbits,expire\\/signature\\/484784AD6E9C1516EC07970AB978D11555654A9A.57EFB4F5F3CCE7F30CFBA1951E6434319300BE12\\/key\\/ck2\\/file\\/file.mp4 ]]><\\/MediaFile><MediaFile bitrate=\\"1879\\" delivery=\\"progressive\\" height=\\"720\\" maintainAspectRatio=\\"false\\" scalable=\\"false\\" type=\\"video\\/mp4\\" width=\\"1280\\"><![CDATA[ https:\\/\\/gcdn.2mdn.net\\/videoplayback\\/id\\/1fe270df6ccb6f2c\\/itag\\/22\\/source\\/doubleclick_dmm\\/ctier\\/L\\/acao\\/yes\\/ip\\/0.0.0.0\\/ipbits\\/0\\/expire\\/3738748528\\/sparams\\/id,itag,source,ctier,acao,ip,ipbits,expire\\/signature\\/7136B1FF2CD283E5A90276E455C5F970B91A35FF.8E6707BA3249059D7BA09F6E3D59FF6BA1D78FE0\\/key\\/ck2\\/file\\/file.mp4 ]]><\\/MediaFile><\\/MediaFiles><\\/Linear><\\/Creative><Creative><CompanionAds><Companion id=\\"post-roll\\" width=\\"1280\\" height=\\"720\\"><CompanionClickThrough><![CDATA[https:\\/\\/events-dca.bidder.kayzen.io\\/click?raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\/CompanionClickThrough><CompanionClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=2&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/CompanionClickTracking><TrackingEvents><Tracking event=\\"creativeView\\"><\\/Tracking><\\/TrackingEvents><StaticResource creativeType=\\"image\\/jpeg\\"><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/obj\\/mosaic-legacy\\/2ff3f000e60c223e67984]]><\\/StaticResource><\\/Companion><Companion id=\\"vungle_endcard_v1\\"><CompanionClickThrough><![CDATA[https:\\/\\/events-dca.bidder.kayzen.io\\/click?raw=BH4f6iRihnLulIzOXQMUXomi6R2lyBeL6MGU81R%2FVDRIFVcxvyj5kbHDx6lRmuk35AuEIPkGnJB0xLx1lvWnuD00Bh02ghKFeiI8RONNSJ%2BNSb4ANGQvmlTdDS7apSoLjpix1Mwd7isfwajPwP1jSaXYbaYEQ8seFjqNU5XghUC%2FYSYvVq9aObfH04qjspVlAmJGMg10b4t3nikZHK5Bxo7eE4W0h7OCKb1I9%2FXdka8kudVFGEDyXhIOi%2FIgFdU5WaxS5h03E6kil3FD64UQVrV5vWjF5s%2B1UzoRwuZL895Gmm57ddCq2LmX0u4Z9t%2B42WQSOI4HYKHI9UiS58a4FTvM5mDYa0lBH5gQzOF2oNHBIMva7AcQMj7ACSiuBXdKUPX8%2FPwQpWiWHrIsjvRgumlunroJm2eZw9BR4Bw%2BejeJYCp7IgXwsdK7cbedrdKF4LaNOqOMUUdeZV4RXeAw8aVFecojzaGo4PsJ9NAaxX7h5RstugfNIBsB19J3dqRO7jwM03XkVlwy5mdByl%2F38cLjCYWUjrJJbTNIu0kotSZnlwbynqFuMT%2BJ%2F4G2mhLljNv5F8vZ1unnc0v9Al7u4eyfJzKDK1HQsEmNrU8pxzC3Xv3WkFvwmvqcaJTvN7%2FlasL8UPvAr8N4nUeVftr2%2BkAd63EF6%2B%2FeSJ4CPS10J6OePGDIgzAK9de6Nxzz7GoFMd%2FIorShKbGJ6wJCMpTewLV9HGcUjLgUKEQtcuQGFkOsz4W1oqbwSNzjHIpJ7wmdNAhkiJn8ounkC2VxAIVUsNhsCaiZbSRRlio2hMPgdHwQ6BC45Je4KAQcjPwKNvtEUXtE8WRVtWl%2BHu4q%2BNVMDb%2FaH2upa8aqy2gZ8nmoTRIMWdUuOOtQZ0LgheYiX5XJkECA1TvwFMkTSN2JMffi1hLzEIjV%2B4frpzv3Eo3NJawOyiaAQSm8oIAOofhvykWKZFANezUgSSys8UL3hMzAWR46SdrQ%2BttcVxvfcMQ9lt4uJxKDYopHZV1Ij8zdHquvzkyAjpRzSigxcTl%2FcQgO1DS9%2FyXpxDyQbQVRZon80S8DROhReR3sYtCyII7VgF0EDNFN9YrJIpFq7PkX%2FFCTcA%3D%3D&p=0&durl=https%3A%2F%2Fapp.adjust.com%2Fao3hqf5%3Ftracker_limit%3D20000%26campaign%3D170881%26adgroup%3D5d8e165cbea62600175a0b7d%26creative%3DCrossword+Jam%26idfa%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26gps_adid%3D3CE171BC-65B1-4EA2-A179-AC14B47E17B9%26publisher_id%3D5d8e165cbea62600175a0b7d%26impression_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26kayzen_click_id%3D107206517-1630409350-090-1-34-172-4-8V3lq-612e12868d020cc18a72ef8e-10064-170881-50461238%26sk_network_id%3D4468km3ulz.skadnetwork%26sk_campaign_id%3D0%26sk_network_token%3Dxylyea2j143k]]><\\/CompanionClickThrough><CompanionClickTracking><![CDATA[https:\\/\\/lf.snssdk.com\\/api\\/ad\\/union\\/redirect\\/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=2&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]><\\/CompanionClickTracking><TrackingEvents><\\/TrackingEvents><AdParameters xmlEncoded=\\"true\\"><![CDATA[<EndCardAdParameters><icon>https:\\/\\/p3-tt.byteimg.com\\/img\\/ad.union.api\\/7c51525c9163b92843a26bf89aaded1f~100x100.image<\\/icon><app_name>\\u70B9\\u4EAE\\u57CE\\u5E02-\\u5168\\u7F51\\u5F00\\u670D<\\/app_name><cover_url>https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/mosaic-legacy\\/2ff3f000e60c223e67984~noop.jpg<\\/cover_url><app_stars>5<\\/app_stars><button_text>\\u70B9\\u51FB\\u4E0B\\u8F7D<\\/button_text><download_url>https%3A%2F%2Fwww.crazyccy.com%2Fdownload%2Fccy_csjfkccy313.apk<\\/download_url><description>\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417<\\/description><\\/EndCardAdParameters>]]><\\/AdParameters><\\/Companion><\\/CompanionAds><\\/Creative><\\/Creatives><Description><![CDATA[\\u53EA\\u67095%\\u7684\\u4EBA\\u80FD\\u70B9\\u4EAE\\u6574\\u5EA7\\u57CE\\u5E02\\uFF0C\\u4F60\\u6562\\u6311\\u6218\\u5417]]><\\/Description><Survey><\\/Survey><Extensions><Extension type=\\"AdVerifications\\"><AdVerifications><Verification vendor=\\"moat.com-omsdkvungleinappvideo781943494431\\"><JavaScriptResource apiFramework=\\"omid\\" browserOptional=\\"true\\"><![CDATA[https:\\/\\/z.moatads.com\\/omsdkvungleinappvideo781943494431\\/moatvideo.js]]><\\/JavaScriptResource><VerificationParameters><![CDATA[{\\"moatClientLevel1\\":\\"{{{app_id}}}\\",\\"moatClientLevel2\\":\\"{{{campaign_id}}}\\",\\"moatClientLevel3\\":\\"{{{creative_id}}}\\",\\"moatClientLevel4\\":\\"{{{placement_id}}}\\",\\"moatClientSlicer1\\":\\"{{{pub_app_id}}}\\",\\"moatClientLevel5\\":\\"{{{rtb_deal_id}}}\\",\\"moatClientLevel6\\":\\"{{{rtb_connection_id}}}\\"}]]><\\/VerificationParameters><\\/Verification><\\/AdVerifications><\\/Extension><Extension type=\\"Extra\\"><CTA><![CDATA[\\u70B9\\u51FB\\u4E0B\\u8F7D]]><\\/CTA><SystemIcon><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/07c04164de3140d2cfe4bdd9812aef22~c1_0x0_q100.png]]><\\/SystemIcon><FullStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/48c275deda9f2daa92acccf8218fc59f~c1_0x0_q100.jpeg]]><\\/FullStar><HalfStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/b273598ab25fec09a467d2b895e3c53e~c1_0x0_q100.jpeg]]><\\/HalfStar><EmptyStar><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/fedbae142b79804e383eed3f4d06e9d5~c1_0x0_q100.jpeg]]><\\/EmptyStar><Review><![CDATA[https:\\/\\/sf1-ttcdn-tos.pstatp.com\\/img\\/ad.union.api\\/297845a2690ec96bd1290a0a289ab373~c1_0x0_q100.jpeg]]><\\/Review><MoPubCtaText><\\/MoPubCtaText><\\/Extension><\\/Extensions><\\/InLine><\\/Ad><\\/VAST>"'
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        override_bid_response_any=override_adm))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm'] and 'templateSettings' in ad_markup:
            cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_keys_not_exist(cacheable_replacements, 'BACKGROUND_IMAGE')  # cover_url

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.130.0')
    @allure.story('PBJ-1667 Verify video URL validation for programmatic ads')
    @allure.description('Verify Jaeger serves when media file is valid from ADM')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_jaeger_check_media_file_format(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version='Vungle/6.6.9',
                                                                        rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm'] and 'templateSettings' in ad_markup:
            cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(cacheable_replacements['MAIN_VIDEO']['extension'], equal_to('mp4'))
            assert_that(str(cacheable_replacements['MAIN_VIDEO']['url']).count('http'), equal_to(1))
            assert_that(str(cacheable_replacements['MAIN_VIDEO']['url']).count('.mp4'), equal_to(1))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.130.0')
    @allure.story('PBJ-1686 Verify adding click tracking for programmatic end card')
    @allure.description('Verify the click tracking for programmatic ad with end card')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_click_tracking_for_programmatic_end_card(self, pub_app_id):
        '''
        CompanionClickTracking in ADM:

         <CompanionClickTracking>
            <![CDATA[https://lf.snssdk.com/api/ad/union/redirect/?active_extra=dBAOZluLpbktg88y1awPD2bg7gF9T%2BF6Sll
            wqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_back=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw1
            7uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&click_source=2&extra=K%2FmpeEAU9gTcAOwvQsxp
            EXCQ0RSkek%2FS2SNNUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCIIWbNqr4
            cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BUtw5D99v%2F553nJNfOQIhUPVUCX7ukh
            8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpT
            P1MPDrXZ4raX29Vw6eUkt98LsllUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg5
            1GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44v51I1Xh4mcaehI5klVYi14P
            BEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbTpzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2Fwrn
            vRQfiaQKHWis4uNJ6WFEs5bz2nKETUZeid7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q
            0F3wpWbK8wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBCjCJPSWnHrUf8vlr
            Z4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3D&is_dsp=1&pack_time=1590630440.65&
            req_id=5ec796d603e1e7c01267c88fu8791&rit=920685236&source_type=1&use_pb=1]]>
         </CompanionClickTracking>
        '''
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        companion_click_tracking = 'https://lf.snssdk.com/api/ad/union/redirect/?active_extra=dBAOZluLpbktg88y1awPD2' \
                                   'bg7gF9T%2BF6SllwqYXihRKdbZEAoq9kCTbQPfHeGuWj21kYt5Qc63RSfRlL91A1hg%3D%3D&call_ba' \
                                   'ck=4OeszuGPR9JzWtROWbsgyFBgcUsU1ve3UPw17uco1n9ePHi0qf7oGq7vfSE%2FgprAZp9X%2BNwb8' \
                                   'gPYCBIXAyRzow%3D%3D&click_source=2&extra=K%2FmpeEAU9gTcAOwvQsxpEXCQ0RSkek%2FS2SN' \
                                   'NUe7hSz1Rl2DO0%2FTy2PAfb9FWkVKsPQzZvb6OJQUB1GzO1L66cb48QDsoKtHAjqfr0Yv468vCtJKCI' \
                                   'IWbNqr4cSxdNJRdnIhG0Rq9roAyGBxUMcLJ%2FFPqn%2BEI3maAdb%2B5UsXPL05UsXkxhJrhiNR%2BU' \
                                   'tw5D99v%2F553nJNfOQIhUPVUCX7ukh8Bz6bsA7LS2JNLhIcGUMTjKk40r9KIYmbHhRBeXnFBfHdkWpf' \
                                   '6aEMtqeKTkeUCZlrh%2FRhPWJlVG3GW%2FhDdvXlYGcIT5XqmPjrHpTP1MPDrXZ4raX29Vw6eUkt98Ls' \
                                   'llUhQVoweCBlkcyHNmdEgyYY52w99mssEqM%2FpgaG%2B%2BiUBqu%2BDJiO1kcY%2FJtJMIyW%2Fg51' \
                                   'GC8C9d%2B9Jc8frsb7Xw3deAyp5Ep5I1fgXPZFM7wPzUu%2ByA4OhQa%2BkmY6EbvTqXqgCckW774o44' \
                                   'v51I1Xh4mcaehI5klVYi14PBEYJabir4wU%2FgEoObr9IalC2lNHys8VIB3pZjCbQPQue3xnmyFAkJbT' \
                                   'pzK%2FpXRuoH9ofbr50tAYRBIWMIWjMugZk7quJtS%2FwrnvRQfiaQKHWis4uNJ6WFEs5bz2nKETUZei' \
                                   'd7zKEpbs4xQ4GXwe%2Bbx9qOx1IBv6ud6fF7dJnCQIPo0pXUmkt7c98DxDeglFltD2KRt3Q0F3wpWbK8' \
                                   'wst5E42%2FMpvaBWtv4v9HMsAAE6kdKfKblBFHDeY66C3LdW37yWyA1Egk%2F%2FSpxv%2Fzrik2WCBC' \
                                   'jCJPSWnHrUf8vlrZ4fK%2BpNNisrBHUCcyYcJ%2FrX2bvWI3I2NZp9X%2BNwb8gPYCBIXAyRzow%3D%3' \
                                   'D&is_dsp=1&pack_time=1590630440.65&req_id=5ec796d603e1e7c01267c88fu8791' \
                                   '&rit=920685236&source_type=1&use_pb=1'

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm'] and 'templateSettings' in ad_markup:

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(ad_markup['tpat']['postroll.click'][0], equal_to(companion_click_tracking))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.133.0')
    @allure.story('PBJ-1824 Media file selection logic for vast ADM change')
    @allure.description('Verify that Jaeger will pick up the first valid mp4 video from ADM as the returned video')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_jaeger_pick_up_first_valid_video(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version='Vungle/6.6.9',
                                                                        rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm'] and 'templateSettings' in ad_markup:
            cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(cacheable_replacements['MAIN_VIDEO']['extension'], equal_to('mp4'))
            assert_that(str(cacheable_replacements['MAIN_VIDEO']['url']).count('http'), equal_to(1))
            assert_that(str(cacheable_replacements['MAIN_VIDEO']['url']).count('.mp4'), equal_to(1))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.133.0')
    @allure.story('PBJ-1824 Media file selection logic for vast ADM change')
    @allure.description('Verify that Jaeger will not pick up the first valid mp4 video from ADM as the returned '
                        'video when SDK version >= 6.7.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.7.0', 'Vungle/6.7.1'])
    def test_jaeger_not_pick_up_first_valid_video(self, pub_app_id, sdk_v, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                                                        rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm'] and 'templateSettings' in ad_markup:
            cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(cacheable_replacements['MAIN_VIDEO']['extension'], equal_to('mp4'))
            assert_that(str(cacheable_replacements['MAIN_VIDEO']['url']).count('http'), equal_to(0))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0')
    @allure.story('PBJ-3037 bid response for native placement')
    @allure.description('Verify the cacheable replacements info for native type placement via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_cacheable_replacements_native_placement_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=us_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']

        assert_that('APP_ICON' in cacheable_replacements)
        assert_that(str(cacheable_replacements['APP_ICON']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['APP_ICON'])
        assert_that('VUNGLE_PRIVACY_ICON_URL' in cacheable_replacements)
        assert_that(str(cacheable_replacements['VUNGLE_PRIVACY_ICON_URL']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['VUNGLE_PRIVACY_ICON_URL'])
        assert_that('MAIN_IMAGE' in cacheable_replacements)
        assert_that(str(cacheable_replacements['MAIN_IMAGE']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['MAIN_IMAGE'])

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'test_mode')
    @allure.story('PBJ-3037 bid response for native placement')
    @allure.description('Verify the cacheable replacements info for native type placement via iDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_cacheable_replacements_native_placement_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=test_default_real_time_sdk_version,
                                                                        rtb_selector=test_mode_kraken_rtb_ids, debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']

        assert_that('APP_ICON' in cacheable_replacements)
        assert_that(str(cacheable_replacements['APP_ICON']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['APP_ICON'])
        assert_that('VUNGLE_PRIVACY_ICON_URL' in cacheable_replacements)
        assert_that(str(cacheable_replacements['VUNGLE_PRIVACY_ICON_URL']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['VUNGLE_PRIVACY_ICON_URL'])
        assert_that('MAIN_IMAGE' in cacheable_replacements)
        assert_that(str(cacheable_replacements['MAIN_IMAGE']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['MAIN_IMAGE'])

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'v1.172.0')
    @allure.story('PBJ-3037 bid response for native placement, PBJ-3075 Ads response for native ads')
    @allure.description('Verify the cacheable replacements info for native type placement via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_cacheable_replacements_native_placement_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']

        assert_that('APP_ICON' in cacheable_replacements)
        assert_that(str(cacheable_replacements['APP_ICON']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['APP_ICON'])
        assert_that('VUNGLE_PRIVACY_ICON_URL' in cacheable_replacements)
        assert_that(str(cacheable_replacements['VUNGLE_PRIVACY_ICON_URL']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['VUNGLE_PRIVACY_ICON_URL'])
        assert_that('MAIN_IMAGE' in cacheable_replacements)
        assert_that(str(cacheable_replacements['MAIN_IMAGE']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['MAIN_IMAGE'])

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'v1.172.0', 'test_mode')
    @allure.story('PBJ-3037 bid response for native placement, PBJ-3075 Ads response for native ads')
    @allure.description('Verify the cacheable replacements info for native type placement via eDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_cacheable_replacements_native_placement_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        cacheable_replacements = ad_markup['templateSettings']['cacheable_replacements']

        assert_that('APP_ICON' in cacheable_replacements)
        assert_that(str(cacheable_replacements['APP_ICON']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['APP_ICON'])
        assert_that('VUNGLE_PRIVACY_ICON_URL' in cacheable_replacements)
        assert_that(str(cacheable_replacements['VUNGLE_PRIVACY_ICON_URL']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['VUNGLE_PRIVACY_ICON_URL'])
        assert_that('MAIN_IMAGE' in cacheable_replacements)
        assert_that(str(cacheable_replacements['MAIN_IMAGE']['url']).count('http'), equal_to(1))
        assert_that('extension' in cacheable_replacements['MAIN_IMAGE'])