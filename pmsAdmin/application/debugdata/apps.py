import threading
import time

from django.apps import AppConfig

class DebugdataConfig(AppConfig):
    name = 'application.debugdata'

    def ready(self):
        from application.debugdata.services import receive_udp_data
        thread = threading.Thread(target=receive_udp_data)
        thread.daemon = True
        thread.start()