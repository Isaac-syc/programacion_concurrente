
import threading
import time
import queue
import random

buffer = queue.Queue(maxsize=10)


class Productor(threading.Thread):
    def __init__(self, buffer):
        threading.Thread.__init__(self)
        self.buffer = buffer
        
        
    def run(self):
        while True:
            if buffer.qsize() < 10:
                valor = random.randint(1, 10)
                self.buffer.put(valor)
                print(f'Productor inserta producto: {valor}')
                
                time.sleep(3)
            else:
                time.sleep(3)
                

              
class Consumidor(threading.Thread):
    def __init__(self, buffer):
        threading.Thread.__init__(self)
        self.buffer = buffer

    def run(self):
        while True:
            if self.buffer.qsize() > 0:
                valor = self.buffer.get()
                print(f'Consumidor toma producto: {valor}')
                
                time.sleep(3)
            else:
                time.sleep(3)
            



def main():
    productor = Productor(buffer)
    consumidor = Consumidor(buffer)

    productor.start()
    consumidor.start()
    


main()