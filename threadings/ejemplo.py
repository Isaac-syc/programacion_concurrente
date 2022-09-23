import requests
import mysql.connector
import time 


mydb = mysql.connector.connect(
    host = "127.0.0.1",
    database = "sismos",
    user = "root",
    password = ""
)
cursor = mydb.cursor();

def get_service():
    r = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-03-05&limit=5000')
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
    get_service()
    end_time = time.time() - init_time
    print(end_time)
    
    