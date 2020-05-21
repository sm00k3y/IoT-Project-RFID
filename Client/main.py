# ---------------------------------------
# | Projekt: Laboratoria z PIR          |
# | Autor: Jakub Smolka                 |
# | Data: 28.03.2020                    |
# | Prowadzacy: Mgr. Natalia Piórkowska |
# ---------------------------------------

import client
import time

if __name__ == "__main__":

    print("\nWitaj w PANELU KLIENTA programu RFID-Magic")
    client.init_clients()

    while True:
        print("\n\t[1] URUCHOM")
        print("\t[2] Dodaj terminal")
        print("\t[3] Usun terminal")
        print("\t[4] Pokaz terminale")
        print("\t[0] Wyjscie\n")
        user_input = input("Wybierz akcje: ")
        print()

        if user_input == "1":
            client.run_clients()

        elif user_input == "2":
            new_client = client.Client(input("Podaj nazwe nowego termianalu: "))
            client.add_client(new_client)
            print("\nTerminal dodano!")

        elif user_input == "3":
            client.print_clients()
            client.remove_client(input("\nPodaj nazwe terminalu, ktory chcesz usunac: "))
            print("\nTerminal usunieto!")

        elif user_input == "4":
            client.print_clients()
            time.sleep(1)

        else:
            break

    client.write_clients_to_db()
