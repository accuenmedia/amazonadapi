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
        # self.status = 'INACTIVE'
        super().__init__(connection, region, profile_id)



