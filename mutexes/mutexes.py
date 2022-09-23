
import threading
from time import sleep
import pytube

mutex = threading.Lock()

def crito(id):
    global x;
    x = x + id
    print("Hilo =" +str(id)+ " =>" + str(x))
    yt = pytube.YouTube(urls[id-1])
    yt.streams.first().download("C:/Users/kevin/Documents/universidad/concurrencia/code1/videos")
    x=1

class Hilo(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
        
    def run(self):
        mutex.acquire()
        #sleep(3-self.id)
        crito(self.id)
        #print("valor: " + str(self.id))
        mutex.release()
        
hilos = [Hilo(1), Hilo(2), Hilo(3)]
urls = ['https://youtu.be/WTWyosdkx44', 'https://youtu.be/jNQXAC9IVRw', 'https://youtu.be/BtLSaxRnIhc']
x=1;


for h in hilos:
    h.start()