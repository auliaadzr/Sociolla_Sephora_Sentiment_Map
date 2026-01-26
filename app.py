import sys
from Scraping import scrapping_data
from Cleaning import data_cleaning
from Visualisasi import rating_outlet
from Visualisasi import pie_chart
from Visualisasi import bar_chart



def menu():
    print("\n====== MENU APLIKASI ======")
    print("1. Jalankan Scraping Data")
    print("2. Jalankan Cleaning Data")
    print("3. Jalankan Data Rating Outlet")
    print("4. Jalankan Visualisasi Ringkasan Kepuasan Konsumen Retail Kecantikan di Bandung")
    print("5. Jalankan Visualisasi Peringkat Kepuasan Pelanggan: Sociolla vs Sephora (Bandung)")
    print("6. Jalankan Semua")
    print("0. Keluar")
    print("===========================")


def main():
    while True:
        menu()
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            print("\n--- Mulai Scraping ---")
            scrapping_data.main()

        elif pilihan == "2":
            print("\n--- Mulai Cleaning ---")
            data_cleaning.main()
        
        elif pilihan == "3":
            print("\n--- Mulai Rating Outlet ---")
            rating_outlet.main()

        elif pilihan == "4":
            print("\n--- Mulai Visualisasi Pie Chart ---")
            pie_chart.main()
        
        elif pilihan == "5":
            print("\n--- Mulai Visualisasi Bar Chart  ---")
            bar_chart.main()

        elif pilihan == "6":
            print("\n--- Mulai Semua Proses ---")
            scrapping_data.main()
            data_cleaning.main()
            rating_outlet.main()
            pie_chart.main()
            bar_chart.main()

        elif pilihan == "0":
            print("Keluar...")
            sys.exit()

        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()