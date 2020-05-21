# ---------------------------------------
# | Projekt: Laboratoria z PIR          |
# | Autor: Jakub Smolka                 |
# | Data: 28.03.2020                    |
# | Prowadzacy: Mgr. Natalia Piórkowska |
# ---------------------------------------

import time
import server
import database as db

if __name__ == "__main__":

    print("\nWitaj w RFID-Magic, programie do obslugi RFID, stworzonym przez: Jakub Smolka! :)")
    server.init()
    while True:
        print("\n\t[1] URUCHOM SYSTEM")
        print("\t[2] Dodaj klienta do systemu")
        print("\t[3] Usun klienta z systemu")
        print("\t[4] Dodaj pracownika")
        print("\t[5] Usun pracownika")
        print("\t[6] Przypisz karte RFID do pracownika")
        print("\t[7] Usun przypisane karty do pracownika")
        print("\t[8] Wygeneruj Raport")
        print("\t[9] Wyswietl klientow")
        print("\t[10] Wyswietl pracownikow")
        print("\t[Any] Wyjscie\n")
        user_input = input("Wybierz akcje: ")
        print()

        if user_input == '1':
            server.run()

        elif user_input == '2':
            client_name = input("Podaj nazwe nowego terminalu: ")
            client = db.Client(client_name)
            db.add_client(client)
            print("\nTerminal dodano!")

        elif user_input == '3':
            db.print_clients()
            rem_client = input("\nPodaj nazwe terminalu do usuniecia: ")
            db.remove_client(rem_client)

        elif user_input == '4':
            worker_name = input("Podaj imie i nazwisko nowego pracownika: ")
            worker = db.Worker(worker_name)
            db.add_worker(worker)

        elif user_input == '5':
            db.print_workers()
            rem_worker = input("Podaj imie i nazwisko pracownika do usuniecia: ")
            db.remove_worker(rem_worker)

        elif user_input == '6':
            db.print_workers()
            worker = input("\nPodaj ID pracownika, do ktorego chcesz przypisac nowa karte: ")
            card_id = input("Podaj ID karty: ")
            if (not worker.isdigit()) or (not card_id.isdigit()):
                print("Prosze wprowadzic numer!")
                time.sleep(1)
            else:
                db.add_card_to_worker(int(worker), int(card_id))

        elif user_input == '7':
            db.print_workers()
            worker_id = input("\nPodaj ID pracownika, dla ktorego chcesz usunac przypisane karty: ")
            if not worker_id.isdigit():
                print("Prosze wprowadzic numer!")
                time.sleep(1)
            db.remove_cards_from_worker(int(worker_id))

        elif user_input == '8':
            db.print_workers()
            worker_name = input("\nPodaj Imie i Nazwisko pracownika, dla ktorego chcesz wygenerowac raport: ")
            db.generate_report(worker_name)

        elif user_input == '9':
            db.print_clients()
            time.sleep(1)

        elif user_input == '10':
            db.print_workers()
            time.sleep(1)

        else:
            db.write_changes_to_db()
            break
