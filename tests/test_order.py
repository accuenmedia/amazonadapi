import unittest
import json

import config

from amazonadapi.order import Order
from amazonadapi.connection import Connection

class ConnectionTestCase(unittest.TestCase):
    def test_get_all_orders(self):
        connection = Connection(config.ad_client_id, config.ad_client_secret, config.region, config.refresh_token)

        orders = Order(connection, config.region, config.profile_id)
        
        id = "5801781520901"

        orders = json.loads(orders.get_orders("5801781520901"))
        print(orders)
        self.assertEqual(orders["response_code"], 200)
