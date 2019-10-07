import requests

class Connection:
    def __init__(self, ad_client_id, ad_client_secret, region, refresh_token):
        self.client_id = ad_client_id
        self.client_secret = ad_client_secret
        self.refresh_token = refresh_token

        self.set_region(region)
        self.auto_refresh_token()

    def auto_refresh_token(self):
        i_sentinel = 1
        i_counter = 0
        get_token_url = self.host
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        while i_sentinel > 0:
            r = requests.post(get_token_url, data=payload, headers=headers, verify=False)
            results_json = r.json()

            if 'access_token' in results_json:
                self.token = results_json['access_token']
                return results_json

            i_counter += 1
            time.sleep(1)

            if i_counter >= 5:
                i_sentinel = 0

        return results_json

    def set_region(self, region='US'):
        region_list = {
            "UK": "https://api.amazon.co.uk/auth/o2/token",
            "IN": "https://api.amazon.co.uk/auth/o2/token",
            "US": "https://api.amazon.com/auth/o2/token",
            "JP": "https://api.amazon.com.jp/auth/o2/token"
        }
        self.region = region
        
        try:
            self.host = region_list[region]
        except KeyError as e:
            self.host = region_list["US"]
            self.region = "US"

        return self.host
