import requests
import re


class LineItem:
    id = None
    orderId = None
    advertiserId = None
    name = None
    type = None
    status = None
    budget = {}
    deliveryCaps = []

    def __init__(self, connection, region, profile_id):
        super().__init__(connection, region, profile_id)
        # self.status = 'INACTIVE'

    def get_line_items(self, order_id):
        i_sentinel = 1
        while i_sentinel == 1:
            if self.page_token == None:
                if self.page_size == None:
                    url = "https://" + self.host + "/da/v1/orders/" + order_id + "/line-items"
                else:
                    url = "https://" + self.host + "/da/v1/orders/" + order_id + "/line-items?page_size=" + str(
                        self.page_size)
                    self.page_size = None
            else:
                url = "https://" + self.host + "/da/v1/orders/" + order_id + "/line-items?page_token=" + self.page_token

            r = self.make_request(url, self.object_headers, 'GET')

            try:
                self.next_page_url = r.headers['Link']
            except:
                i_sentinel = 0

            if self.next_page_url != None:
                p = re.compile('.*page_token=(.*)>')
                matches = p.findall(self.next_page_url)
                self.page_token = matches[0]

        self.page_token = None
        self.page_size = None
        return r

    def get_line_item(self, line_item_id):
        url = "https://" + self.host + "/da/v1/line-items/" + line_item_id
        r = self.make_request(url, self.object_headers, 'GET')

        return r

    def create_line_item(self, line_item):
        url = "https://" + self.host + "/da/v1/line-items"
        self.data = line_item

        r = self.make_request(url, self.object_headers, 'POST', self.data)
        return r

    def update_line_item(self, line_item):
        # url = self.host + "/da/v1/line-items/" + line_item.id # <-- expected behavior for update
        url = "https://" + self.host + "/da/v1/line-items"
        self.data = line_item

        r = self.make_request(url, self.object_headers, 'PUT', self.data)
        return r
