from threading import Condition
from time import sleep
from Receptionist import Receptionist
from Customer import Customer
import queue

condition = Condition()

customers = ['Rodrigo','Miranda','Héctor','Francisco','Erick','Suzana','Rogelio','Fernando',"Juana",'Maria','Daniel','Pedro','Juan','David','Maria']
max_customers = 10
max_reservations = 2


enqueue = queue.Queue()
queueTables = queue.Queue()
tables = []
order = ["", False]
reservations = queue.Queue(max_reservations)

def main():
   while True:
        print("Restaurante abierto")
        global order;
        recepcionist = Receptionist(condition)
        for customer in customers:
            customer = Customer(customer, max_customers, max_reservations,reservations,recepcionist,enqueue, tables, queueTables)
            customer.start()
            sleep(3)
        sleep(4)
        

if __name__ == '__main__':
    main()