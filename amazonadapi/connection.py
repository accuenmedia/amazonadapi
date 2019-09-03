import requests

class Connection:
    def __init__(self, ad_client_id, ad_client_secret, profile_id, region, refresh_token):

        self.client_id = ad_client_id
        self.client_secret = ad_client_secret
        self.profile_id = profile_id
        self.refresh_token = refresh_token

    def auto_refresh_token(self):
        i_sentinel = 1
        i_counter = 0
        while i_sentinel > 0:
            get_token_url = "https://api.amazon.com/auth/o2/token"
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }

            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
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
