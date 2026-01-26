import pandas as pd
import os

def main():
    # KONFIGURASI PATH
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # MENGAMBIL DATA DARI HASIL CLEANING KAMU
    importPath = os.path.join(BASE_DIR, "Data", "Clean", "data_cleaning.csv")
    exportPath = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")

    try:
        df = pd.read_csv(importPath)
        
        # --- PROSES RUMUS BAYESIAN ---
        # 1. Hitung Rs (Rata-rata rating produk) dan n (Jumlah ulasan produk)
        produk_stats = df.groupby(['e_commerce', 'outlet_id', 'lat', 'lon', 'produk_id', 'Rating_global_produk']).agg(
            Rs=('rating', 'mean'),
            n=('rating', 'count')
        ).reset_index()

        # 2. Rumus: ((n * Rs) + (k * Rg)) / (n + k)
        k = 5
        produk_stats['P_score'] = (
            (produk_stats['n'] * produk_stats['Rs']) + (k * produk_stats['Rating_global_produk'])
        ) / (produk_stats['n'] + k)

        # 3. Agregasi per Outlet (Atribut baru untuk GIS)
        outlet_final = produk_stats.groupby(['e_commerce', 'outlet_id', 'lat', 'lon']).agg(
            rating_outlet=('P_score', 'mean')
        ).reset_index()

        outlet_final['rating_outlet'] = outlet_final['rating_outlet'].round(2)

        # SIMPAN HASIL
        outlet_final.to_csv(exportPath, index=False)
        print(f"Berhasil! Atribut 'rating_outlet' disimpan di: {exportPath}")

    except Exception as e:
        print(f"Terjadi kesalahan pada perhitungan: {e}")

if __name__ == "__main__":
    main()