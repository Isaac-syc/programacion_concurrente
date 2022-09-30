import threading


mutex = threading.Lock()

def crito(id):
    print("La persona numero " + str(id) + " Ya a comio, siguiente")

class Hilo(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
        
    def run(self):
        mutex.acquire()
        crito(self.id)
        mutex.release()
        
hilos = [Hilo(1), Hilo(2), Hilo(3), Hilo(4), Hilo(5), Hilo(6), Hilo(7), Hilo(8)]



for h in hilos:
    h.start()