from time import sleep
import requests
import threading
        
def verifyUrl(url):
    status = requests.head(url)
    if status.status_code == 200:
        print(url + ', 200, se proceso correctamente')
    else:
        print( url  +', 400, no se proceso correctamente')

class Hilo(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        h1 = threading.Thread(target=verifyUrl, args=[self.url])
        h1.start()

while True:
    hilos = [
        Hilo('https://www.facebook.com/'),
        Hilo('https://www.google.com/'),
        Hilo('https://www.youtube.com'),
        Hilo('https://www.github.com/'),
        Hilo('https://www.steampowered.com/'),
        Hilo('https://www.twitch.tv/'),
        Hilo('https://ww.amazon.com/'),
        Hilo('https://www.reddit.com/'),
        Hilo('https://www.linkedin.com/'),
        Hilo('https://www.microsoft.com/'),
        Hilo('https://www.tumblr.com/'),
        Hilo('https://www.pinterest.com/'),
        Hilo('https://www.netflix.com/'),
        Hilo('https://www.twitter.com/'),
        Hilo('https://ww.twitter.com/'),
        Hilo('https://ww.amazon.com/'),
        Hilo('https://ww.coppel.com/'),
        Hilo('https://www.coppel.com/'),
        Hilo('https://www.adobe.com/'),
        Hilo('https://ww.adobe.com/'),
        Hilo('https://www.resume.io/'),
        Hilo('https://www.resume.com/'),
        Hilo('https://www.python.org/'),
        Hilo('https://ww.python.org/'),
        Hilo('https://www.wikipedia.org/'),
    ]
    for hilo in hilos:
        hilo.start()
    sleep(300)
    
    
       