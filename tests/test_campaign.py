import unittest
import json

import config

from amazonadapi.amazonclient import AmazonClient

class ConnectionTestCase(unittest.TestCase):
    def test_get_all_orders(self):
        connection = AmazonClient(config.ad_client_id, config.ad_client_secret, config.profile_id, config.region, config.refresh_token)
        connection.auto_refresh_token()
        
        id = "5801781520901"

        orders = json.loads(connection.get_orders(id))
        print(orders)
        self.assertEqual(orders["response_code"], 200)
