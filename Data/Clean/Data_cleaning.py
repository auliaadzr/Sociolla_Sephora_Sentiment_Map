import pandas as pd

importPath = "./Data/Raw/data_scrapping.csv"
exportPath = "./Data/Clean/data_cleaned.csv"

print("--- Memulai Proses Cleaning ---")

try:
    df = pd.read_csv(importPath)
    print(f"Berhasil membaca file dari: {importPath}")
    print(f"Jumlah data awal: {len(df)} baris")

    df_clean = df.drop_duplicates().copy()

    nama_kolom_ulasan = 'review' 
    
    if nama_kolom_ulasan in df_clean.columns:
        df_clean[nama_kolom_ulasan] = df_clean[nama_kolom_ulasan].astype(str).str.lower()
        print(f"Berhasil mengubah teks di kolom '{nama_kolom_ulasan}' menjadi huruf kecil.")
    else:
        print(f"Peringatan: Kolom '{nama_kolom_ulasan}' tidak ditemukan!")
        print(f"Kolom yang tersedia adalah: {list(df_clean.columns)}")

    df_clean.to_csv(exportPath, index=False)
    
    print("-" * 30)
    print(f"Selesai! File bersih dibuat: data_cl.xlsx")
    print(f"Jumlah data sekarang: {len(df_clean)} baris")
    print(f"Berhasil menghapus {len(df) - len(df_clean)} baris duplikat.")

except Exception as e:
    print(f"Terjadi kesalahan: {e}")