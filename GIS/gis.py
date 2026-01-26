import folium
import pandas as pd
import os

# 1. KONFIGURASI PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Mengambil data hasil perhitungan Bayesian (rating_outlet)
importPath = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")

# 2. MEMBACA FILE CSV (Sesuai Praktikum 4)
df = pd.read_csv(importPath)

# 3. TENTUKAN TITIK TENGAH PETA (Bandung)
center_lat = -6.9175 
center_lon = 107.6191
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# 4. TAMBAHKAN CIRCLE MARKER DENGAN UKURAN DINAMIS
for index, row in df.iterrows():
    # Penentuan warna berdasarkan brand
    brand_color = "pink" if row['e_commerce'].lower() == 'sociolla' else "black"
    
    # LOGIKA UKURAN: Rating tinggi = Radius besar
    # Kita kalikan dengan 5 agar perbedaan ukurannya terlihat jelas di peta
    ukuran_radius = row['rating_outlet'] * 5 

    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=ukuran_radius, # Ukuran otomatis membesar sesuai rating
        popup=f"Outlet: {row['outlet_id']}<br>Rating: {row['rating_outlet']}",
        tooltip=row['outlet_id'],
        color=brand_color,
        fill=True,
        fill_color=brand_color,
        fill_opacity=0.6
    ).add_to(m)

# 5. SIMPAN HASIL KE HTML
exportPath = os.path.join(BASE_DIR, "Data", "Visualisasi", "peta_proportional.html")
m.save(exportPath)
print(f"Peta Proportional berhasil dibuat: {exportPath}")