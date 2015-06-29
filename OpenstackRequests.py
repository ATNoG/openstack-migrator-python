import requests
import json
from SyncOpenstack import SyncOpenstack


class Request:
    def __init__(self, auth_url, project_name, username, password):
        self.auth_url = auth_url
        self.project_name = project_name
        self.username = username
        self.password = password

        self.sync = SyncOpenstack()

        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({'auth': {'tenantName': '', 'passwordCredentials': {'username': self.username, 'password': self.password}}})
        r = requests.post(url=self.auth_url+"/tokens",
                          data=payload,
                          headers=headers)
        response = json.loads(r.text)
        self.token = response["access"]["token"]["id"]

    def get(self, slug_url, url=None):
        headers = {'X-Auth-Token': self.token}

        if url is None:
            r = requests.get(url=self.auth_url + "/" + slug_url,
                             headers=headers)
        else:
            r = requests.get(url=url + "/" + slug_url,
                             headers=headers)

        return json.loads(r.text)

    def post(self, slug_url):
        pass