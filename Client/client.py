# ---------------------------------------
# | Projekt: Laboratoria z PIR          |
# | Autor: Jakub Smolka                 |
# | Data: 28.03.2020                    |
# | Prowadzacy: Mgr. Natalia Piórkowska |
# ---------------------------------------

from datetime import datetime, date
import paho.mqtt.client as mqtt
import time
import os.path
import csv


class Client:

    __client_id = 0

    broker = "art3mis"
    port = 8883
    client = mqtt.Client()
    client.tls_set("ca.crt")
    client.username_pw_set(username="client", password="P@ssw0rd")

    def __init__(self, name):
        Client.__client_id += 1
        self.client_id = Client.__client_id
        self.name = name

    def run(self):
        print("\nPodaj id. karty, ktora chcesz odbic. Podaj 0 aby wrocic do menu.")
        card_id = input()
        card_time = datetime.now().strftime("%H:%M:%S")
        if not card_id.isdigit() or int(card_id) <= 0:
            print("Powrot do menu!")
        else:
            # return int(card_id), card_time
            self.client.publish("IoT/MQTT/RFID-Server", "{};{};{}".format(self.name, card_id, card_time))
            print("Komunikat przeslany!")
            time.sleep(1)

    def connect_to_broker(self):
        self.client.connect(self.broker, self.port)
        print("Klient {} polaczony!".format(self.client_id))

    def disconnect_from_broker(self):
        self.client.disconnect()
        print("Klient {} rozlaczony!".format(self.client_id))


clients = []


def init_clients():
    filename = "database/clients_database-" + date.today().strftime("%Y") + ".csv"
    if os.path.exists(filename):
        with open(filename, newline='') as database:
            db_reader = csv.reader(database, delimiter=',')
            for row in db_reader:
                clients.append(Client(row[0]))
    else:
        clients.append(Client("Ksiegowosc"))
        clients.append(Client("IT"))
        clients.append(Client("Biuro Zarzadu"))


def run_clients():
    for client in clients:
        client.connect_to_broker()
        time.sleep(0.3)

    while True:
        print("\nID: 0, Powrot do menu")
        print_clients()
        terminal_number = int(input("\nWybierz terminal: "))
        if terminal_number <= 0 or terminal_number > len(clients):
            break
        clients[terminal_number-1].run()

    print()
    for client in clients:
        client.disconnect_from_broker()
        time.sleep(0.2)


def add_client(client):
    clients.append(client)


def remove_client(client_name):
    for client in clients:
        if client.name.lower() == client_name.lower():
            clients.remove(client)


def print_clients():
    for client in clients:
        print("ID: {}, {}".format(client.client_id, client.name))


def write_clients_to_db():
    filename = "database/clients_database-" + date.today().strftime("%Y") + ".csv"
    with open(filename, 'w', newline='') as database:
        db_writer = csv.writer(database, delimiter=',')
        for client in clients:
            db_writer.writerow([client.name])
