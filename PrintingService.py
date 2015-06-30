
class PrintingService:
    def __init__(self):
        pass

    @staticmethod
    def tenant(tenant):
        PrintingService.default_start("TENANT")
        print "name: " + tenant["name"]
        print "description: " + tenant["description"]
        print "id: " + tenant["id"]
        print "enabled: " + str(tenant["enabled"])
        PrintingService.default_end()

    @staticmethod
    def tenants(tenants):
        for tenant in tenants:
            PrintingService.tenant(tenant)

    @staticmethod
    def default_start(name):
        print "------------ "+name+" -----------"

    @staticmethod
    def default_end():
        print "------------   END    -----------"
