import unittest

import config

from amazonadapi.connection import Connection

class ConnectionTestCase(unittest.TestCase):
    def test_connection(self):
        connection = Connection(config.ad_client_id, config.ad_client_secret, config.region, config.refresh_token)

        token = connection.auto_refresh_token()
        print(token)

        self.assertIsNotNone(token["access_token"])
        self.assertIsNotNone(connection.token)
