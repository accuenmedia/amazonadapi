import unittest

import config

from amazonadapi.amazonclient import AmazonClient

class ConnectionTestCase(unittest.TestCase):
    def test_connection(self):
        connection = AmazonClient(config.ad_client_id, config.ad_client_secret, config.profile_id, config.region, config.refresh_token)

        token = connection.auto_refresh_token()
        print(token)

        self.assertIsNotNone(token["access_token"])
