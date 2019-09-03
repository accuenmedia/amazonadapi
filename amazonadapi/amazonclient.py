#!/usr/bin/env python

import json
import requests
import time
import os
import sys
import re


class AmazonOrder:
    id = None
    advertiserId = None
    name = None
    startDateTime = None
    endDateTime = None
    status = None
    budget = {}
    deliveryCaps = []

    def __init__(self):
        self.status = 'INACTIVE'


class AmazonLineItem:
    id = None
    orderId = None
    advertiserId = None
    name = None
    type = None
    startDateTime = None
    endDateTime = None
    status = None
    budget = {}
    deliveryCaps = []

    def __init__(self):
        self.status = 'INACTIVE'


class AmazonClient:
    client_id = None
    client_secret = None
    api_key = None
    id_host = None
    one_host = None
    aud = None
    payload = None
    encoded_payload = None
    payload_url = None
    headers = None
    authorized_headers = None
    token = None
    refresh_token = None
    profile_id = None
    region = None
    host = None
    data = None
    page_token = None
    page_size = None
    next_page_url = None

    def __init__(self, connection, region, profile_id):
        self.connection = connection
        self.host = self.set_region(region)
        self.profile_id = profile_id
        self.object_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.connection.token,
            'Host': self.host,
            'Amazon-Advertising-API-Scope': self.profile_id
        }

    def set_region(self, region='US'):
        region_list = {
            "UK": "advertising-api-eu.amazon.com",
            "IN": "advertising-api-eu.amazon.com",
            "US": "advertising-api.amazon.com",
            "JP": "advertising-api-fe.amazon.com"
        }
        self.region = region
        
        try:
            self.host = region_list[region]
        except KeyError as e:
            self.host = region_list["US"]
            self.region = "US"

        return self.host

    # curl -X GET -H "Content-Type:application/json" -H "Authorization: Bearer $AMZN_TOKEN" https://advertising-api.amazon.com/v1/profiles
    def get_profiles(self):
        url = "https://" + self.host + "/v1/profiles"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }

        r = self.make_request(url, headers, 'GET')
        return r

    # -H Authorization: Bearer self.token
    # -H Host: advertising-api.amazon
    # -H Amazon-Advertising-API-Scope: PROFILE_ID
    # -H Content-Type: application/json
    # url: https://advertising-api.amazon.com/da/v1/advertisers
    def get_advertisers(self):
        i_sentinel = 1
        ids = []
        response_json = {}
        while i_sentinel == 1:
            if self.page_token == None:
                if self.page_size == None:
                    url = "https://" + self.host + "/da/v1/advertisers"
                else:
                    url = "https://" + self.host + "/da/v1/advertisers?page_size=" + str(self.page_size)
                    self.page_size = None
            else:
                url = "https://" + self.host + "/da/v1/advertisers?page_token=" + self.page_token

            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.token,
                'Host': self.host,
                'Amazon-Advertising-API-Scope': self.profile_id
            }

            r = self.make_request(url, self.object_headers, 'GET')
            try:
                print(r.headers['Link'])
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

    # -H Authorization: Bearer self.token
    # -H Host: advertising-api.amazon
    # -H Amazon-Advertising-API-Scope: PROFILE_ID
    # -H Content-Type: application/json
    # url: https://advertising-api.amazon.com/da/v1/advertisers/AD_ID/orders

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

    # -H Authorization: Bearer self.token
    # -H Host: advertising-api.amazon
    # -H Amazon-Advertising-API-Scope: PROFILE_ID
    # -H Content-Type: application/json
    # url: https://advertising-api.amazon.com/da/v1/orders/ORDER_ID
    def get_order(self, order_id):
        url = "https://" + self.host + "/da/v1/orders/" + order_id
        r = self.make_request(url, self.object_headers, 'GET')

        return r

    # -H Authorization: Bearer self.token
    # -H Host: advertising-api.amazon
    # -H Amazon-Advertising-API-Scope: PROFILE_ID
    # -H Content-Type: application/json
    # url: https://advertising-api.amazon.com/da/v1/orders/ORDER_ID/line-items
    def get_line_items(self, order_id):
        i_sentinel = 1
        ids = []
        response_json = {}
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

    def create_line_item(self, line_item):
        url = "https://" + self.host + "/da/v1/line-items"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token,
            'Host': self.host,
            'Amazon-Advertising-API-Scope': self.profile_id
        }

        self.data = line_item

        r = self.make_request(url, headers, 'POST', self.data)
        return r

    def update_line_item(self, line_item):
        # url = self.host + "/da/v1/line-items/" + line_item.id # <-- expected behavior for update
        url = "https://" + self.host + "/da/v1/line-items"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token,
            'Host': self.host,
            'Amazon-Advertising-API-Scope': self.profile_id
        }

        self.data = line_item

        r = self.make_request(url, headers, 'PUT', self.data)
        return r

    # create response_json method to abstract away the creation of return response that matt wants
    def generate_json_response(self, r, results_json, request_body):

        response_json = {
            'response_code': r.status_code,
            'request_body': request_body
        }
        # if request is successful, ensure msg_type is success
        if r.status_code in [200, 201]:
            response_json['msg_type'] = 'success'
            response_json['msg'] = ''
            response_json['data'] = results_json
        else:
            response_json['msg_type'] = 'error'
            # display the error message that comes back from request
            response_json['msg'] = results_json['error']
            response_json['data'] = results_json['error']

        return response_json

    # make_request(method_type) --> pass in method_type
    def make_request(self, url, headers, method_type, data=None):
        request_body = url, headers, data
        r, results_json = self.make_new_request(url, self.token, method_type, headers, data)

        if r.status_code in [400, 401]:
            # refresh access token
            self.token = self.connection.auto_refresh_token()['access_token']
            # apply headers with new token, return response and response dict
            r, results_json = self.make_new_request(url, self.connection.token, method_type, headers)

        # use results_json to create updated json dict
        response_json = self.generate_json_response(r, results_json, request_body)

        return json.dumps(response_json)

    def make_new_request(self, url, token, method_type, headers, data=None):

        # modify headers with new access token
        headers['Authorization'] = 'Bearer ' + self.connection.token
        if method_type == 'GET':
            r = requests.get(url, headers=headers, verify=False)
        if method_type == 'POST':
            r = requests.post(url, headers=headers, verify=False, data=json.dumps(data))
        if method_type == 'PUT':
            r = requests.put(url, headers=headers, verify=False, data=json.dumps(data))
        results_json = r.json()
        return r, results_json

    def generate_curl_command(self):
        pass
