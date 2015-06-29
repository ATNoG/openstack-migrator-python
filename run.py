from OpenstackRequests import Request
import json


if __name__ == '__main__':
    authentication_file = open('authentication.json', 'r')
    auth_args = json.load(authentication_file)

    openstack = Request(auth_url=auth_args['auth_url'],
                        project_name=auth_args['project_name'],
                        username=auth_args['username'],
                        password=auth_args['password'])

    # list tenants
    response = openstack.get(slug_url="tenants")

    for tenant in response["tenants"]:
        print tenant["name"]

    pass