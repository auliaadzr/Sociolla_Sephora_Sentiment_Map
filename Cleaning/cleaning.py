import pandas as pd
import os

def main():
    """
    Fungsi untuk membersihkan data hasil scraping:
    - Menghapus duplikat
    - Normalisasi teks ulasan
    - Menyimpan data bersih
    """

    # KONFIGURASI PATH
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    importPath = os.path.join(BASE_DIR, "Data", "Raw", "data_scrapping.csv")
    exportPath = os.path.join(BASE_DIR, "Data", "Clean", "data_cleaning.csv")

    try:
        # BACA DATA
        df = pd.read_csv(importPath)
        print(f"Berhasil membaca file")
        print(f"Jumlah data awal: {len(df)} baris")

        # HAPUS DUPLIKAT
        df_clean = df.drop_duplicates().copy()

        nama_kolom_ulasan = 'review' 
        
        # NORMALISASI TEKS
        if nama_kolom_ulasan in df_clean.columns:
            df_clean[nama_kolom_ulasan] = df_clean[nama_kolom_ulasan].astype(str).str.lower()
            print(f"Kolom '{nama_kolom_ulasan}' berhasil dinormalisasi.")
        else:
            print(f"Peringatan: Kolom '{nama_kolom_ulasan}' tidak ditemukan!")
            print(f"Kolom tersedia: {list(df_clean.columns)}")

        # SIMPAN FILE BERSIH
        df_clean.to_csv(exportPath, index=False)
        
        print("-" * 30)
        print(f"Selesai! File bersih dibuat: {exportPath}")
        print(f"Jumlah data sekarang: {len(df_clean)} baris")
        print(f"Berhasil menghapus {len(df) - len(df_clean)} baris duplikat.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# JIKA FILE DIJALANKAN LANGSUNG
if __name__ == "__main__":
    main()
