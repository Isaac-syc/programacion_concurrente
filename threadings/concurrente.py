import requests
import mysql.connector
import time 
import concurrent.futures
import threading

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
    pass 

def write_db(data):
    
    for i in data['features']:
        cursor.execute("INSERT INTO sismos (place) VALUES ('" + i['properties']['place'] + "')")    
        mydb.commit()   
    
    pass
    #escribir el response en una db 


if __name__ == "__main__":
    init_time = time.time()
    service('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-03-05&limit=5000')
    end_time = time.time() - init_time
    print(end_time)
    
    