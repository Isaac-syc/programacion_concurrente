import threading, time, queue, math
from random import choice, randint
from termcolor import colored

cant_limit = 10
cant_customers = 8  
cant_waiter = 1
cant_cook = 1 
cant_booking = 2

class Monitor(object):
    def __init__(self,espacio):
        #capacidad del restaurante
        self.espacio = espacio 
        self.mutex = threading.Lock()
        self.reception = threading.Condition()
        self.clientes = threading.Condition()
        self.waiter = threading.Condition()
        self.cook = threading.Condition()
        self.reservations = queue.Queue(cant_booking)
        self.queue_customers = queue.Queue(self.espacio)
        self.queue_orders = queue.Queue()
        self.ordenes_plato = queue.Queue()
        self.food = queue.Queue()

    def reserve(self,customer):
        self.reception.acquire()
        if self.reservations.full():
            self.reception.wait()
        else:
            print("Cliente " + str(customer.id) + " hizo una reservación")
            self.reservations.put(customer)
            time.sleep(1)
        self.mutex.acquire()
        self.entrar(customer)
        self.reservations.get()
        self.reception.notify()
        self.reception.release()

    def queue(self,customer):
        self.reception.acquire()
        print(colored(f"Cliente {customer.id} se formó en la cola","white","on_black"))
        time.sleep(1)
        self.mutex.acquire()
        self.entrar(customer)
        self.reception.notify()
        self.reception.release()

    def entrar(self,customer):
        self.clientes.acquire()
        if self.queue_customers.full():
            print(colored(f"Cliente {customer.id} esperando a que haya lugar","yellow"))
            self.clientes.wait()
        else:
            print(colored(f"Cliente {customer.id} entra al restaurante","blue"))
            self.queue_customers.put(customer)
            print(colored(f"Cliente {customer.id} se prepara para ordenar","blue"))
            self.waiter.acquire()
            self.waiter.notify()
            self.waiter.release()
            self.mutex.release()
            self.clientes.release()
    
    def eat(self):
        if not self.food.empty():
            customer = self.food.get()
            customer_id = list(customer.keys())[0]
            food = list(customer.values())[0]
            print(colored(f"Cliente {customer_id} está comiendo {food}","white","on_red"))
            time.sleep(randint(1,5))
            print(f"Cliente {customer_id} terminó de comer")
            print(colored(f"Cliente {customer_id} ha salido"))

    def create_order(self, waiter):
        while True:
            self.waiter.acquire()
            if self.queue_customers.empty():
                self.waiter.wait()
                print(colored(f"waiter {waiter} esta descansando","white","on_blue"))
            else:
                customer = self.queue_customers.get()
                if customer.orden == False:
                    plato = Orden()
                    print(colored(f"waiter {waiter} tomo la orden del cliente {customer.id} que comerá {plato.food}","green"))
                    time.sleep(1)
                    self.queue_orders.put({customer.id : plato.food})
                    self.cook.acquire()
                    self.cook.notify()
                    self.cook.release()
                    customer.orden = True
                    self.waiter.release()
                else:
                    self.waiter.release()

    def cooking(self,id):
        while True:
            self.cook.acquire()
            if self.queue_orders.empty():
                self.cook.wait()
                print(colored(f"Cocinero {id} esta descansando","white","on_magenta"))
            else:
                customer = self.queue_orders.get()
                customer_id = list(customer.keys())[0]
                food = list(customer.values())[0]
                print(colored(f"cook {id} está cocinando la orden del customer {customer_id}: {food}"))
                time.sleep(1)
                self.food.put(customer)
                self.cook.release()
class Orden():
    foods = ["Chilaquiles","hotdog","quesadilla","hamburguesa","pizza","tacos"]
    def __init__(self): 
        self.food = choice(self.foods)

class Customer(threading.Thread):
    def __init__(self,id,monitor):
        threading.Thread.__init__(self)
        self.id = id
        self.orden = False
        self.restaurant = monitor
    def run(self):
        reserva = randint(0,1)
        if reserva == 1: 
            self.restaurant.reserve(self) 
        if reserva == 0:
            self.restaurant.queue(self)
        self.restaurant.eat()

class Waiter(threading.Thread):
    def __init__(self,id,monitor):
        threading.Thread.__init__(self)
        self.id = id
        self.restaurant = monitor

    def run(self):
        self.restaurant.create_order(self.id)

class Cook(threading.Thread):
    def __init__(self,id,monitor):
        threading.Thread.__init__(self)
        self.id = id
        self.restaurant = monitor
    
    def run(self):
        self.restaurant.cooking(self.id)

def main():
    restaurant = Monitor(cant_limit)
    customers = []
    waiters = []
    cookers = []

    for x in range(cant_customers):
        customers.append(Customer(x+1,restaurant))
    for customer in customers:
        customer.start()

    for x in range(cant_waiter):
        waiters.append(Waiter(x+1,restaurant))
    for waiter in waiters:
        waiter.start()

    for x in range(cant_cook):
        cookers.append(Cook(x+1,restaurant))
    for cook in cookers:
        cook.start()

if __name__ == "__main__":
    main()