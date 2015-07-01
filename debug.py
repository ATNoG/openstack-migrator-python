__author__ = "Rafael Ferreira and Andre Rainho"
__copyright__ = "Copyright (C) 2015, ATNoG, Insituto de Telecomunicacoes - Aveiro"
__license__ = "GPL 3.0"
__version__ = "1.0"


DEBUG = True


def debug_message(message):
    global DEBUG
    if DEBUG:
        print "[DEBUG] " + message


def debug_hash_line():
    debug_message("###############################################################################################")