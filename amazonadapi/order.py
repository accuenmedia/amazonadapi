import requests

from .base import Base


class Order(Base):
    # id = None
    # advertiserId = None
    # name = None
    # startDateTime = None
    # endDateTime = None
    # status = None
    # budget = {}
    # deliveryCaps = []

    def __init__(self, connection, region, profile_id):
        super().__init__(connection, region, profile_id)
        # self.status = 'INACTIVE'

    def get_orders(self, ad_id):
        i_sentinel = 1

        while i_sentinel == 1:
            if self.page_token == None:
                if self.page_size == None:
                    url = "https://" + self.host + "/da/v1/advertisers/" + str(ad_id) + "/orders"
                else:
                    url = "https://" + self.host + "/da/v1/advertisers/" + str(ad_id) + "/orders?page_size=" + str(
                        self.page_size)
                    self.page_size = None
            else:
                url = "https://" + self.host + "/da/v1/advertisers/" + str(ad_id) + "/orders?page_token=" + self.page_token

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

    def get_order(self, order_id):
        url = "https://" + self.host + "/da/v1/orders/" + order_id
        r = self.make_request(url, self.object_headers, 'GET')

        return r

    def create_order(self, order):
        url = "https://" + self.host + "/da/v1/orders"
        self.data = order

        r = self.make_request(url, self.object_headers, 'POST', self.data)
        return r

    def update_order(self, order):
        url = "https://" + self.host + "/da/v1/orders"
        self.data = order

        r = self.make_request(url, self.object_headers, 'PUT', self.data)
        return r
