#!/usr/bin/env python

import json
import requests
import re


class Base:
    token = None
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

    def get_profiles(self):
        url = "https://" + self.host + "/v1/profiles"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }

        r = self.make_request(url, headers, 'GET')
        return r

    def get_advertisers(self):
        i_sentinel = 1
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

    def generate_json_response(self, r, results_json, data):

        response_json = {
            'response_code': r.status_code,
            'request_body': self.generate_curl_command(r.request.method, r.url, self.object_headers, data)
        }
        if r.status_code in [200, 201]:
            response_json['msg_type'] = 'success'
            response_json['msg'] = ''
            response_json['data'] = results_json
        else:
            response_json['msg_type'] = 'error'
            response_json['msg'] = results_json['error']
            response_json['data'] = results_json['error']

        return response_json

    def make_request(self, url, headers, method_type, data=None):
        r, results_json = self.make_new_request(url, self.token, method_type, headers, data)

        if r.status_code in [400, 401]:
            # refresh access token
            self.token = self.connection.auto_refresh_token()['access_token']
            # apply headers with new token, return response and response dict
            r, results_json = self.make_new_request(url, self.connection.token, method_type, headers)

        # use results_json to create updated json dict
        response_json = self.generate_json_response(r, results_json, data)

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

    def generate_curl_command(self, method, url, headers, data=None):
        command = 'curl -v -H {headers} {data} -X {method} "{uri}"'
        
        header_list = ['"{0}: {1}"'.format(k, v) for k, v in headers.items()]
        header = " -H ".join(header_list)

        return command.format(method=method, headers=header, data=data, uri=url)
