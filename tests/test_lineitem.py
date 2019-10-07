import unittest
import json

import config

from amazonadapi.lineitem import LineItem
from amazonadapi.connection import Connection

class LineItemTestCase(unittest.TestCase):
    def test_get_lineitems_by_order(self):
        connection = Connection(config.ad_client_id, config.ad_client_secret, config.region, config.refresh_token)

        lines = LineItem(connection, config.region, config.profile_id)
        
        id = "9327887810601"

        line_items = json.loads(lines.get_line_items(id))
        print(line_items)
        self.assertEqual(line_items["response_code"], 200)
