import threading
import requests
from ast import While


def get_service(request_data):
    print(request_data)


def get_error():
    print("error request")
    
def get_service1(request_data):
    print(request_data)


def get_error1():
    print("error request")


def request_data(url, success_callback, error_callback):
    response = requests.get(url)
    if response.status_code == 200:
        success_callback(response.json())
    else:
        error_callback()


class Hilo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        h1 = threading.Thread(target=request_data, kwargs={
            'url': 'https://randomuser.me/api/',
            'success_callback': get_service,
            'error_callback': get_error
        })
        h1.start()

        h2 = threading.Thread(target=request_data, kwargs={
            'url': 'https://randomuser.me/api/',
            'success_callback': get_service1,
            'error_callback': get_error1
        })
        h2.start()


hilo = Hilo()
hilo.start()
