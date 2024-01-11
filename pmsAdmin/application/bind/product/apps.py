import threading
import time

from django.apps import AppConfig

class ProductConfig(AppConfig):
    name = 'application.bind.product'

    # def ready(self):
    #     from application.testdata.services import receive_udp_data
    #     thread = threading.Thread(target=receive_udp_data)
    #     thread.daemon = True
    #     thread.start()