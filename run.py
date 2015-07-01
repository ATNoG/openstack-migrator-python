from OpenstackRequests import Request
from PrintingService import PrintingService
from SyncOpenstack import SyncOpenstack
import json


if __name__ == '__main__':
    try:
        authentication_file_old = open('authentication_old.json', 'r')
    except IOError:
        content = {"auth_url": "http://172.20.1.108:5000/v3", "auth_admin_url": "", "project_name": "admin", "username": "admin", "password": "admin"}
        f = file("authentication_old.json", "a")
        json.dump(content, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.close()
        print "Please fill the authentication_old.json"
        exit()
    auth_args_old = json.load(authentication_file_old)

    try:
        openstack_old = Request(auth_url=auth_args_old['auth_url'],
                                project_name=auth_args_old['project_name'],
                                username=auth_args_old['username'],
                                password=auth_args_old['password'])
    except Exception, e:
        print e.message
        exit()

    try:
        authentication_file_new = open('authentication_new.json', 'r')
    except IOError:
        content = {"auth_url": "http://172.32.1.108:5000/v3", "auth_admin_url": "", "project_name": "admin",
                   "username": "admin", "password": "admin"}
        f = file("authentication_new.json", "a")
        json.dump(content, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.close()
        print "Please fill the authentication_new.json"
        exit()
    auth_args_new = json.load(authentication_file_new)

    try:
        openstack_new = Request(auth_url=auth_args_new['auth_url'],
                                project_name=auth_args_new['project_name'],
                                username=auth_args_new['username'],
                                password=auth_args_new['password'])
    except Exception, e:
        print e.message
        exit()

    # sync class for store id from the old and new openstack
    sync = SyncOpenstack()

    # list tenants
    response = openstack_old.get(slug_url="tenants")

    """
    ---------------------------------------- TENANTS -----------------------------------------------
    This first part of the code pretends to make the tenant if doesn't exists or get the tenant if
    already exists in the OpenStack. If already exists the API when we attempt to create the tenant
    returns one error () if the tenant doesn't exists it will return the tenant information.
    ------------------------------------------------------------------------------------------------
    """
    for tenant in response["tenants"]:

        PrintingService.tenant(tenant)
        payload = {'tenant': {'name': tenant['name'], 'description': tenant['description'], 'enabled': tenant['enabled']}}

        # the fuel network has a management network to add tenants, [mac] sudo route -n add NETWORK_ID/32 GATEWAY_IP
        tenants_new = openstack_new.post(url=auth_args_new["auth_admin_url"], slug_url="tenants", payload=payload)

        if "tenant" in tenants_new:
            # sync if is created
            sync.add_tenant_id(tenant["id"], tenants_new["tenant"]["id"])
        else:
            # get the already created tenant
            tenants_new = openstack_new.get(url=auth_args_new["auth_admin_url"], slug_url="tenants")
            for tenant_new in tenants_new["tenants"]:
                if tenant["description"] == tenant_new["description"] and tenant["name"] == tenant_new["name"] \
                        and tenant["enabled"] == tenant_new["enabled"]:
                    sync.add_tenant_id(tenant["id"], tenant_new["id"])
                    break

    # new, list tenants
    response = openstack_new.get(url=auth_args_new["auth_admin_url"], slug_url="tenants")
    PrintingService.tenants(response["tenants"])

    pass