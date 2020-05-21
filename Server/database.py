# ---------------------------------------
# | Projekt: Laboratoria z PIR          |
# | Autor: Jakub Smolka                 |
# | Data: 28.03.2020                    |
# | Prowadzacy: Mgr. Natalia Piórkowska |
# ---------------------------------------

import csv
import time
import os.path
from datetime import date, datetime


class Worker:
    __worker_id = 0

    def __init__(self, full_name, cards_ids=None):
        self.full_name = full_name
        Worker.__worker_id += 1
        self.worker_id = Worker.__worker_id
        self.in_work = False
        self.cards_id = []
        if cards_ids is not None:
            for card in cards_ids:
                self.cards_id.append(card)


class Client:
    __client_id = 0

    def __init__(self, name):
        Client.__client_id += 1
        self.client_id = Client.__client_id
        self.name = name


# zmienne celowo globalne
clients = []
workers = []


def init_logs():
    filename = "database/logs-" + date.today().strftime("%Y") + ".csv"
    if os.path.exists(filename):
        return
    else:
        with open(filename, 'w', newline='') as logs:
            log_writer = csv.writer(logs, delimiter=',')
            log_writer.writerow(['Przybycie/Opuszczenie', 'Pracownik', 'ID Pracownika', 'ID Karty', 'Czas', 'Terminal'])


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


def init_workers():
    filename = "database/workers_database-" + date.today().strftime("%Y") + ".csv"
    if os.path.exists(filename):
        with open(filename, newline='') as database:
            db_reader = csv.reader(database, delimiter=',')
            for row in db_reader:
                temp_worker = Worker(row[0])
                if row[1] == '1':
                    temp_worker.in_work = True
                else:
                    temp_worker.in_work = False
                for i in range(2, len(row)):
                    temp_worker.cards_id.append(int(row[i]))
                workers.append(temp_worker)
    else:
        workers.append(Worker("Samantha York", [245]))
        workers.append(Worker("Jason Clock", [123456789]))


def entry_to_file(entry):
    filename = "database/logs-" + date.today().strftime("%Y") + ".csv"
    with open(filename, 'a', newline='') as logs:
        log_writer = csv.writer(logs, delimiter=',')
        log_writer.writerow(entry.split(','))


def add_client(client):
    clients.append(client)


def remove_client(client_name):
    for client in clients:
        if client.name.lower() == client_name.lower():
            clients.remove(client)


def print_clients():
    for client in clients:
        print("ID: {}, {}".format(client.client_id, client.name))


def print_workers():
    for worker in workers:
        print("ID: {}, {}".format(worker.worker_id, worker.full_name))


def add_worker(worker):
    workers.append(worker)


def remove_worker(worker_name):
    for worker in workers:
        if worker.full_name.lower() == worker_name.lower():
            workers.remove(worker)


def add_card_to_worker(worker_id, card_id):
    for worker in workers:
        if worker.worker_id == worker_id:
            worker.cards_id.append(card_id)


def remove_cards_from_worker(worker_id):
    for worker in workers:
        if worker.worker_id == worker_id:
            worker.cards_id.clear()


def write_changes_to_db():
    filename = "database/clients_database-" + date.today().strftime("%Y") + ".csv"
    with open(filename, 'w', newline='') as database:
        db_writer = csv.writer(database, delimiter=',')
        for client in clients:
            db_writer.writerow([client.name])

    filename = "database/workers_database-" + date.today().strftime("%Y") + ".csv"
    with open(filename, 'w', newline='') as database:
        db_writer = csv.writer(database, delimiter=',')
        for worker in workers:
            in_work = 0
            if worker.in_work:
                in_work = 1
            db_writer.writerow([worker.full_name, in_work] + worker.cards_id)


def generate_report(worker_name):
    filename = "database/logs-" + date.today().strftime("%Y") + ".csv"
    if not os.path.exists(filename):
        print("Nie zanaleziono logow systemu, raport nie zostal wygenerowany. \
               System musi zostac uzyty przynajmniej raz.")
        return
    work_time = datetime.min
    with open(filename, newline='') as logs:
        logs_reader = csv.reader(logs, delimiter=',')
        start_time = datetime.min
        stop_time = datetime.min
        for row in logs_reader:
            if row[1].lower() == worker_name.lower():
                if row[0] == "Przybycie":
                    start_time = datetime.strptime(row[4], "%H:%M:%S")
                elif row[0] == "Opuszczenie":
                    stop_time = datetime.strptime(row[4], "%H:%M:%S")
                else:
                    continue

                if stop_time < start_time:
                    continue
                else:
                    work_time += stop_time - start_time
    csv_report_generator(worker_name, work_time)
    print("\nCalkowity czas pracy {} to: {}".format(worker_name, work_time.strftime("%H:%M:%S")))
    print("Raport zostal wygenerowany w folderze projektu.")
    time.sleep(1)


def csv_report_generator(worker_name, work_time):
    report_filename = "reports/" + worker_name.split(" ")[0] + "_" + worker_name.split(" ")[1]\
                      + "_" + date.today().strftime("%d-%m-%Y") + ".csv"
    logs_filename = "database/logs-" + date.today().strftime("%Y") + ".csv"
    with open(report_filename, 'w', newline='') as report:
        report_writer = csv.writer(report, delimiter=',')
        report_writer.writerow(["Calkowity czas pracy", work_time.strftime("%H:%M:%S")])
        report_writer.writerow(["Wszystkie zebrane logi: "])
        with open(logs_filename, newline='') as logs:
            logs_reader = csv.reader(logs, delimiter=',')
            for row in logs_reader:
                if row[1] == worker_name or row[0] == "Przybycie/Opuszczenie":
                    report_writer.writerow(row)
