__author__ = "Rafael Ferreira and Andre Rainho"
__copyright__ = "Copyright (C) 2015, ATNoG, Insituto de Telecomunicacoes - Aveiro"
__license__ = "GPL 3.0"
__version__ = "1.0"

from OpenstackRequests import Request
from PrintingService import PrintingService
from SyncOpenstack import SyncOpenstack
import debug
import json

# If true shows the debug information
debug.DEBUG = True

if __name__ == '__main__':
    # the variable content is used to setup the authentication files when it doesn't exists
    # you can define the values of the dictionary and make it different, but the principal idea is
    # to you fill the generated file: authentication_old.json or authentication_new.json
    content = {
        "url_keystone_admin": "http://172.20.1.108:35357/v2.0",
        "url_keystone_public": "http://172.20.1.108:5000/v2.0",
        "url_nova_api": "http://172.20.1.108:8774/v2",
        "password": "admin",
        "project_name": "admin",
        "username": "admin"
    }

    """
    ###############################################################################################
    ####### Authentication at the Old OpenStack, the one that is to be sync for the new one #######
    ###############################################################################################
    """
    debug.debug_hash_line()

    # the name used to store the credentials for the old OpenStack, the one that you want to import
    authentication_old_file_name = "authentication_old.json"

    try:
        # if it doesn't exists it will raise the IOError and then it will be created
        authentication_file_old = open(authentication_old_file_name, 'r')
        debug.debug_message("Authentication old file opened!")
    except IOError:
        # if doesn't exists, the file is created and the script ends where with a warning for you
        # telling that you must fill the generated file!
        f = file(authentication_old_file_name, "a")
        json.dump(content, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.close()
        print "Please fill the " + authentication_old_file_name
        exit()
    auth_args_old = json.load(authentication_file_old)

    try:
        # if the authentication file is read and it's ok (valid json) now is time to make the Request
        # the request can raise one Exception and for now that Exception is handle with one print and one
        # exit of the script :p
        openstack_old = Request(auth_args=auth_args_old)
        debug.debug_message("Authentication in the old OpenStack made!")
    except Exception, e:
        debug.debug_message(e.message)
        exit()

    """
    ###############################################################################################
    ####### Authentication at the NEW OpenStack, the one that is to be sync via the old one #######
    ###############################################################################################
    """
    debug.debug_hash_line()

    # this part of the code follows the above part of the authentication process
    authentication_new_file_name = "authentication_new.json"

    try:
        authentication_file_new = open(authentication_new_file_name, 'r')
        debug.debug_message("Authentication new file opened!")
    except IOError:
        f = file(authentication_new_file_name, "a")
        json.dump(content, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.close()
        print "Please fill the " + authentication_new_file_name
        exit()
    auth_args_new = json.load(authentication_file_new)

    try:
        openstack_new = Request(auth_args=auth_args_new)
        debug.debug_message("Authentication in the new OpenStack made!")
    except Exception, e:
        debug.debug_message(e.message)
        exit()

    """
    ###############################################################################################
    #######                                Sync class                                       #######
    ###############################################################################################
    """
    debug.debug_hash_line()

    # Sync class for store id from the old and new openstack, it can store all the tenants ids for
    # example, or other ones. When the data is stored the .json is saved with all the data stored
    sync = SyncOpenstack()

    """
    ###############################################################################################
    #######                                Tenants                                          #######
    ###############################################################################################
    This first part of the code pretends to make the tenant if doesn't exists or get the tenant if
    already exists in the OpenStack. If already exists the API when we attempt to create the tenant
    returns one error () if the tenant doesn't exists it will return the tenant information.
    -----------------------------------------------------------------------------------------------
    """
    # The admin must be member or admin of all projects, this is one rule of our administration. So we must
    # get the role admin admin and then add the user admin to all the projects
    # The url to make the changes is:
    # PUT http://10.11.1.2:35357/v2.0/tenants/tenant-id/users/user-id/roles/OS-KSADM/role-id
    # We must send the "tenant-id" (the new tenant id in the new OpenStack), the "user-id" is the admin "user-id"
    # the "role-id" is the role id of the admin role
    response = openstack_new.get(url=openstack_new.auth_args["url_keystone_admin"]+"/OS-KSADM/roles")

    # for other usages we must store the roles information in the sync object
    sync.add_roles(response["roles"], openstack="openstack_2")
    roles = sync.get_roles(openstack="openstack_2")

    # now we want to get the "admin" role id
    for role in roles:
        if role["name"] == "admin":
            role_admin_id = role["id"]
            break

    try:
        role_admin_id
    except NameError:
        debug.debug_message("The admin role must be defined!")
        exit()

    # now we must get the "admin" id, we will make this with a call to the openstack new API
    response = openstack_new.get(url=openstack_new.auth_args["url_keystone_admin"]+"/users?name=admin")
    admin_id = response["user"]["id"]

    # now we need to make one request to get the tenants information from the old openstack, our objective
    # is to create in the new openstack the tenant, if doesn't exists
    response = openstack_old.get(url=openstack_old.auth_args["url_keystone_public"]+"/tenants")

    debug.debug_hash_line()
    debug.debug_message("Old OpenStack tenants")

    # the response is one dictionary with tenants and tenants_links (you can make a breakpoint and debug to
    # see more details)
    for tenant in response["tenants"]:
        # This printing service only  makes prints, we send one dictionary returned by the API with the information
        # that we pretend, for example, now we want that the printing service make print of the tenant
        PrintingService.tenant(tenant)
        payload = {'tenant': {'name': tenant['name'], 'description': tenant['description'], 'enabled': tenant['enabled']}}

        # the fuel network has a management network to add tenants, [mac] sudo route -n add NETWORK_ID/32 GATEWAY_IP
        tenants_new = openstack_new.post(url=openstack_new.auth_args["url_keystone_admin"]+"/tenants", payload=payload)

        if "tenant" in tenants_new:
            # sync if is created
            sync.add_tenant(tenant, tenants_new["tenant"])
            debug.debug_message("TENANT created in the new openstack, id: " + tenants_new["tenant"]["id"])

            # now we must to add the user to the admin list and user list of the tenant
            response = openstack_new.put(url=openstack_new.auth_args["url_keystone_admin"]+"/tenants/" +
                              tenants_new["tenant"]["id"] + "/users/" + admin_id + "/roles/OS-KSADM/" + role_admin_id)
        else:
            # get the already created tenant
            tenants_new = openstack_new.get(url=openstack_new.auth_args["url_keystone_admin"]+"/tenants")
            for tenant_new in tenants_new["tenants"]:
                if tenant["description"] == tenant_new["description"] and tenant["name"] == tenant_new["name"] \
                        and tenant["enabled"] == tenant_new["enabled"]:
                    sync.add_tenant(tenant, tenant_new)
                    break
            debug.debug_message("TENANT sync done, tenant already exists, id_old:" + tenant["id"])

    # new, list tenants at the new OpenStack
    response = openstack_new.get(url=openstack_new.auth_args["url_keystone_admin"]+"/tenants")
    debug.debug_hash_line()
    debug.debug_message("Tenants at the new OpenStack")
    PrintingService.tenants(response["tenants"])

    """
    ###############################################################################################
    #######                                Flavors                                          #######
    ###############################################################################################
    Documentation comment
    -----------------------------------------------------------------------------------------------
    """

    for tenant_id in sync.get_tenants_id():
        response = openstack_old.get(url=openstack_old.auth_args["url_nova_api"] + "/" + tenant_id + "/flavors")

        for flavor in response["flavors"]:
            url = flavor["links"][0]["href"]
            flavor_details = openstack_old.get(url=url)
            flavor = flavor_details["flavor"]

            payload = {
                "name": flavor["name"],
                "ram": flavor["ram"],
                "vcpus": flavor["vcpus"],
                "disk": flavor["disk"]
            }

            openstack_new.set_project(project=sync.get_tenant(tenant_id)["name"])
            response_create = openstack_new.post(url=openstack_new.auth_args["url_nova_api"] + "/" +
                                                 sync.get_tenant(tenant_id)["id"] + "/flavors", payload=payload)
            pass
    pass