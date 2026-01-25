import sys
from Scraping import Scrapping_Data
from Data import Data_cleaning


def menu():
    print("\n====== MENU APLIKASI ======")
    print("1. Jalankan Scraping Data")
    print("2. Jalankan Data Cleaning")
    print("3. Jalankan Semua")
    print("0. Keluar")
    print("===========================")


def main():
    while True:
        menu()
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            print("\n--- Mulai Scraping ---")
            Scrapping_Data.main()

        elif pilihan == "2":
            print("\n--- Mulai Cleaning ---")
            Data_cleaning.main()

        elif pilihan == "3":
            print("\n--- Mulai Semua Proses ---")
            Scrapping_Data.main()
            Data_cleaning.main()

        elif pilihan == "0":
            print("Keluar...")
            sys.exit()

        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()