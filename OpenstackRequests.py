__author__ = "Rafael Ferreira and Andre Rainho"
__copyright__ = "Copyright (C) 2015, ATNoG, Insituto de Telecomunicacoes - Aveiro"
__license__ = "GPL 3.0"
__version__ = "1.0"

import requests
import json


class Request:
    """
    This class Request was made to making POST and GET requests. It handles the authentication process when the
    Request is initialized and every request is made with the Token.
    Be aware that the token can be phished and then used for make request with a stolen account.
    You must make all the requests in HTTPS or in a secure environment.
    """
    def __init__(self, auth_args):
        self.auth_args = auth_args
        self.get_token()

    def get_token(self):
        # the request must have json content-type
        headers = {'Content-Type': 'application/json'}

        # payload, the payload must has the authentication credentials such as the project name, username and password
        payload = json.dumps({'auth': {'tenantName': self.auth_args["project_name"], 'passwordCredentials': {'username': self.auth_args["username"], 'password': self.auth_args["password"]}}})

        # this line makes the request, with the url (for the keystone public uel) with the slug tokens and with the
        # details prepared above
        r = requests.post(url=self.auth_args["url_keystone_public"]+"/tokens",
                          data=payload,
                          headers=headers)

        # the response is returned in json format, but we pretend to be an object
        response = json.loads(r.text)

        # if the authentication fails the token will not be in the access token id dictionary (make a breakpoint)
        # if you want to see the returning responses from the API.
        try:
            self.token = response["access"]["token"]["id"]
        except KeyError:
            raise Exception("Authentication fail!")

    def get(self, url):
        # every request must have the X-Auth-Token, be aware that the token can be phished and then used for
        # make request with a stolen account. You must make all the requests in HTTPS or in a secure environment.
        headers = {'X-Auth-Token': self.token}

        r = requests.get(url=url, headers=headers)

        return json.loads(r.text)

    def post(self, payload, url):
        # the difference between the get and the post is that the in the HTTP POST method the body has "data"
        # in our case the data has JSON text, so we must set the Content-Type: application/json
        headers = {'X-Auth-Token': self.token,
                   'Content-Type': 'application/json'}

        r = requests.post(url=url, headers=headers, data=json.dumps(payload))

        return json.loads(r.text)