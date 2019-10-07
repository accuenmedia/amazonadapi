import unittest
import json

import config

from amazonadapi.order import Order
from amazonadapi.connection import Connection

class OrderTestCase(unittest.TestCase):
    def test_get_all_orders(self):
        connection = Connection(config.ad_client_id, config.ad_client_secret, config.region, config.refresh_token)

        orders = Order(connection, config.region, config.profile_id)
        
        id = "5801781520901"

        order_list = json.loads(orders.get_orders(id))
        print(order_list)
        self.assertEqual(order_list["response_code"], 200)

    def test_get_order_by_order_id(self):
        connection = Connection(config.ad_client_id, config.ad_client_secret, config.region, config.refresh_token)

        orders = Order(connection, config.region, config.profile_id)
        
        id = "9327887810601"

        order = json.loads(orders.get_order(id))
        print(order)
        self.assertEqual(order["response_code"], 200)
