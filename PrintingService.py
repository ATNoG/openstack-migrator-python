
class PrintingService:
    def __init__(self):
        pass

    @staticmethod
    def tenant(tenant):
        PrintingService.default_start()
        pass
        PrintingService.default_end()

    @staticmethod
    def tenants(tenants):
        for tenant in tenants:
            PrintingService.tenant(tenant)

    @staticmethod
    def default_start():
        print "------------ STARTING -----------"

    @staticmethod
    def default_end():
        print "------------   END    -----------"
