import unittest

import config

from amazonadapi.amazonclient import AmazonClient

a = AmazonClient(config.ad_client_id, config.ad_client_secret, config.profile_id, config.region, config.refresh_token)
print(a.auto_refresh_token())
