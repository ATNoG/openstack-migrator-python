__author__ = "Rafael Ferreira and Andre Rainho"
__copyright__ = "Copyright (C) 2015, ATNoG, Insituto de Telecomunicacoes - Aveiro"
__license__ = "GPL 3.0"
__version__ = "1.0"

import debug


class PrintingService:
    def __init__(self):
        pass

    @staticmethod
    def tenant(tenant):
        PrintingService.default_start("TENANT")
        debug.debug_message("name: " + tenant["name"])
        debug.debug_message("description: " + tenant["description"])
        debug.debug_message("id: " + tenant["id"])
        debug.debug_message("enabled: " + str(tenant["enabled"]))
        PrintingService.default_end()

    @staticmethod
    def tenants(tenants):
        for tenant in tenants:
            PrintingService.tenant(tenant)

    @staticmethod
    def default_start(name):
        debug.debug_message("------------ " + name + " -----------")

    @staticmethod
    def default_end():
        debug.debug_message("------------   END    -----------")