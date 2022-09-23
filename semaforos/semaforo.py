from threading import Thread, Semaphore
import pytube
semaforo = Semaphore(1)

def crito(id):
    global x;
    x = x + id
    print("Hilo =" +str(id)+ " =>" + str(x))
    #print("link: " + urls[id-1])
    yt = pytube.YouTube(urls[id-1])
    yt.streams.first().download("C:/Users/kevin/Documents/universidad/concurrencia/code1/videos")
    x=1

class Hilo(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id=id

    def run(self):
        semaforo.acquire() #Inicializa semaforo , l
        crito(self.id)  
        semaforo.release()

urls = ['https://youtu.be/WTWyosdkx44', 'https://youtu.be/jNQXAC9IVRw', 'https://youtu.be/BtLSaxRnIhc']
threads_semaphore = [Hilo(1), Hilo(2), Hilo(3)]
x=1;

for t in threads_semaphore:
    t.start()