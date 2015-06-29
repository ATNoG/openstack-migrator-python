import json


class SyncOpenstack:
    """
    openstack_1 old openstack
    openstack_2 new openstack
    """
    def __init__(self):
        # load from json
        f = file('export.json', 'r')
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

    def save(self):
        f = file('export.json', 'w')
        json.dump(self.export, f)
        f.close()