from OpenstackRequests import Request
from PrintingService import PrintingService
import json


if __name__ == '__main__':
    authentication_file_old = open('authentication_old.json', 'r')
    auth_args_old = json.load(authentication_file_old)

    try:
        openstack_old = Request(auth_url=auth_args_old['auth_url'],
                                project_name=auth_args_old['project_name'],
                                username=auth_args_old['username'],
                                password=auth_args_old['password'])
    except Exception, e:
        print e.message
        exit()

    authentication_file_new = open('authentication_new.json', 'r')
    auth_args_new = json.load(authentication_file_new)

    try:
        openstack_new = Request(auth_url=auth_args_new['auth_url'],
                                project_name=auth_args_new['project_name'],
                                username=auth_args_new['username'],
                                password=auth_args_new['password'])
    except Exception, e:
        print e.message
        exit()

    # list tenants
    response = openstack_old.get(slug_url="tenants")

    for tenant in response["tenants"]:
        PrintingService.tenant(tenant)
        payload = {'tenant': {'name': tenant['name'], 'description': tenant['description'], 'enabled': tenant['enabled']}}

        # the fuel network has a management network to add tenants, [mac] sudo route -n add 10.10.1.2/32 193.136.92.148
        tenants_new = openstack_new.post(url="http://10.10.1.2:35357/v2.0/", slug_url="tenants", payload=payload)

    # new, list tenants
    response = openstack_new.get(slug_url="tenants")
    PrintingService.tenants(response["tenants"])

    pass