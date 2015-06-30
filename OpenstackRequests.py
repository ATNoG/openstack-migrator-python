import requests
import json
from SyncOpenstack import SyncOpenstack


class Request:
    def __init__(self, auth_url, project_name, username, password):
        self.auth_url = auth_url
        self.project_name = project_name
        self.username = username
        self.password = password

        self.get_token()

    def get_token(self):
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({'auth': {'tenantName': self.project_name, 'passwordCredentials': {'username': self.username, 'password': self.password}}})
        r = requests.post(url=self.auth_url+"/tokens",
                          data=payload,
                          headers=headers)
        response = json.loads(r.text)
        try:
            self.token = response["access"]["token"]["id"]
        except KeyError:
            raise Exception("Authentication fail!")

    def get(self, slug_url=None, url=None):
        headers = {'X-Auth-Token': self.token}

        if url is None:
            r = requests.get(url=self.auth_url + "/" + slug_url,
                             headers=headers)
        else:
            r = requests.get(url=url + "/" + slug_url,
                             headers=headers)

        return json.loads(r.text)

    def post(self, payload, slug_url=None, url=None):
        headers = {'X-Auth-Token': self.token,
                   'Content-Type': 'application/json'}

        payload = json.dumps(payload)

        if url is None:
            r = requests.post(url=self.auth_url + "/" + slug_url, headers=headers, data=payload)
        else:
            r = requests.post(url=url + "/" + slug_url, headers=headers, data=payload)

        return json.loads(r.text)