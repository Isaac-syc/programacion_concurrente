import random
from time import sleep
from threading import Condition, Thread

class Customer(Thread):
    def __init__(self, customer,max_customers, max_reservations, reservations, recepcionist,enqueue, tables, queueTables):
        Thread.__init__(self)
        self.customer = customer
        self.max_customers = max_customers
        self.max_reservations = max_reservations
        self.reservations = reservations
        self.recepcionist = recepcionist
        self.condition = Condition()
        self.enqueue = enqueue
        self.tables = tables
        self.queueTables = queueTables
        
    
    def talkWithRecepcionist(self, customer, is_reserved):
        self.recepcionist.giveTable(customer, is_reserved, self.max_customers, self.reservations, self.enqueue, self.queueTables, self.tables)
        
    def reserve(self):
        self.arriving = self.recepcionist.reserve(self.customer, self.max_reservations, self.reservations, self.enqueue)
    
    def run(self):
        print(f"Cliente: {self.customer} ")
        reserva = random.randint(0,1)
        if reserva == 1: 
            self.reserve() 
            while self.arriving == False:
                self.condition.acquire()
                sleep(random.uniform(0.3,2))
                customer = self.reservations.get()
                next = self.enqueue.get()
                self.reservations.put(next)
                self.condition.notify()
                self.condition.release()
                
                if len(self.tables) < self.max_customers:
                    self.talkWithRecepcionist(customer, 1)
                else:
                   self.queueTables.put(customer)     
                
        if reserva == 0:
            self.talkWithRecepcionist(self.customer, 0)
            
        
        
        
        

        
        
        
        
    