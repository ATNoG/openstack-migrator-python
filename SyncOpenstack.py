__author__ = "Rafael Ferreira and Andre Rainho"
__copyright__ = "Copyright (C) 2015, ATNoG, Insituto de Telecomunicacoes - Aveiro"
__license__ = "GPL 3.0"
__version__ = "1.0"

import json


class SyncOpenstack:
    """
    openstack_1 old openstack
    openstack_2 new openstack
    """
    def __init__(self):
        file_export_name = 'export.json'

        # load from json
        try:
            f = file(file_export_name, 'r')
        except IOError:
            open(file_export_name, 'a').close()
            f = file(file_export_name, 'r')

        try:
            self.export = json.loads(f)

            if "openstack_1" not in self.export:
                raise TypeError

            if "openstack_2" not in self.export:
                raise TypeError
        except TypeError:
            self.export = {}
            self.export["openstack_1"] = {}
            self.export["openstack_2"] = {}
            # tenants
            self.export["openstack_1"]["tenants"] = {}
            self.export["openstack_2"]["tenants"] = {}
            self.save()

    def add_tenant_id(self, stack_1_tenant_id, stack_2_tenant_id):
        self.export["openstack_1"]["tenants"][stack_1_tenant_id] = stack_2_tenant_id
        self.export["openstack_2"]["tenants"][stack_2_tenant_id] = stack_1_tenant_id
        self.save()

    def get_tenant_id(self, tenant_id, openstack="openstack_1"):
        try:
            return self.export[openstack]["tenants"][tenant_id]
        except AttributeError:
            return False

    def get_tenants_id(self, openstack="openstack_1"):
        tenants = self.export[openstack]["tenants"]
        return tenants.keys()

    def save(self):
        f = file('export.json', 'w')
        json.dump(self.export, f)
        f.close()