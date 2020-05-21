# ---------------------------------------
# | Projekt: Laboratoria z PIR          |
# | Autor: Jakub Smolka                 |
# | Data: 28.03.2020                    |
# | Prowadzacy: Mgr. Natalia Piórkowska |
# ---------------------------------------

import time
# import getpass
from datetime import datetime
import paho.mqtt.client as mqtt
import database as db

mqtt_broker = "art3mis"
mqtt_port = 8883
mqtt_client = mqtt.Client("Server")
mqtt_client.tls_set("ca.crt")
mqtt_client.username_pw_set(username="server", password="P@ssw0rd")


def init():
    db.init_logs()
    db.init_clients()
    db.init_workers()


def run():
    mqtt_client.connect(mqtt_broker, mqtt_port)
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()
    mqtt_client.subscribe("IoT/MQTT/RFID-Server")

    print("SYSTEM URUCHOMIONY, oczekuje na wiadomosci terminali")
    print("[0] Powrot do menu\n")
    i = 1
    while i != "0":
        # i = getpass.getpass("", stream=None)
        i = input()

    print("SYSTEM ZAKONCZYL POLACZENIE")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    time.sleep(0.5)


def on_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(";")
    success = False
    card_id = int(message_decoded[1])
    card_time = datetime.strptime(message_decoded[2], "%H:%M:%S")
    card_time = card_time.strftime("%H:%M:%S")

    for client in db.clients:
        if message_decoded[0] == client.name:
            print("Terminal rozpoznany!")
            success = True
            card_read(client, card_id, card_time)

    if not success:
        print("Nieznany terminal: {}".format(message_decoded[0]))
        add = input("Czy chcesz dodac terminal do bazy? [T/N]: ")
        if add.upper() == "T":
            db.add_client(db.Client(message_decoded[0]))
            print("\nTerminal dodany")
            time.sleep(0.5)
            card_read(db.clients[-1], card_id, card_time)
        else:
            print("Wiadomosc pominieta")
            time.sleep(0.5)


def card_read(client, card_id, card_time):
    for worker in db.workers:
        for card in worker.cards_id:
            if card == card_id:
                new_entry(client, worker, card_time, card_id)
                return
    unknown_card_entry(client, card_id, card_time)


def new_entry(client, worker, card_time, card_id):
    entry = ""
    if worker.in_work:
        print("Opuszczenie pracy: ", end='')
        entry += "Opuszczenie,"
        worker.in_work = False
    else:
        print("Przybycie do pracy; ", end='')
        entry += "Przybycie,"
        worker.in_work = True
    print("{}, id: {}, karta: {}, czas: {}, terminal: {}\n".format(worker.full_name, worker.worker_id,
                                                                   card_id, card_time, client.name))
    entry += "{},{},{},{},{}".format(worker.full_name, worker.worker_id, card_id, card_time, client.name)
    db.entry_to_file(entry)
    time.sleep(0.5)


def unknown_card_entry(client, card_id, card_time):
    print("Nieznana karta: {}, czas: {}, terminal: {}".format(card_id, card_time, client.name))
    entry = ",NIEZNANA KARTA,,{},{},{}".format(card_id, card_time, client.name)
    db.entry_to_file(entry)
    time.sleep(0.5)
