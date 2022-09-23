from ast import arg
import requests
import mysql.connector
import time 
import concurrent.futures
import threading
import pytube

threading_local = threading.local()

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    database = "sismos",
    user = "root",
    password = ""
)
cursor = mydb.cursor();


def service(url):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(get_service, url)

def get_service(url):
    r = requests.get(url)
    #consumir un servicio que descargue por lo menos 5k registros 
    write_db(r.json())
     

def write_db(data):
    
    for i in data['features']:
        cursor.execute("INSERT INTO sismos (place) VALUES ('" + i['properties']['place'] + "')")    
        mydb.commit()   
    
    
    #escribir el response en una db 
    
def get_users(x=0):

    
    response = requests.get('https://randomuser.me/api/')
    if response.status_code==200:
        results = response.json().get('results')
        name = results[0].get('name').get('first')
        print(name)
            
def get_videos():
    urls = ['https://youtu.be/WTWyosdkx44', 'https://youtu.be/jNQXAC9IVRw', 'https://youtu.be/BtLSaxRnIhc']
    for i in range(0,3):
        yt = pytube.YouTube(urls[i])
        yt.streams.first().download("C:/Users/kevin/Documents/universidad/concurrencia/code1/videos")
        
    


if __name__ == "__main__":
    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-03-05&limit=5000'
    x = 0
    
    init_time = time.time()
    
    for i in range(0,700):
      th2 = threading.Thread(target=get_users, args=[x])  
      th2.start()
    
    th3 = threading.Thread(target=get_videos)
    th1 = threading.Thread(target=get_service, args=[url])
    th1.start()
    th3.start()
    
    #service('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-03-05&limit=5000')
    end_time = time.time() - init_time
    print(end_time)
    
    



