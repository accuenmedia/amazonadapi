import unittest

import config

from amazonadapi.amazonclient import AmazonClient

class ConnectionTestCase(unittest.TestCase):
    def test_connection(self):
        connection = AmazonClient(config.ad_client_id, config.ad_client_secret, config.profile_id, config.region, config.refresh_token)
        connection.auto_refresh_token()
        
        id = "5801781520901"

        orders = connection.get_orders(id)
        print(orders)
