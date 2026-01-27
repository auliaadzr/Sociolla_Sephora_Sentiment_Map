import folium
import pandas as pd
import os
import math
from folium.plugins import MarkerCluster

# 1. PATH CONFIG
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ratingPath = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")
produkPath = os.path.join(BASE_DIR, "Data", "Raw", "data_website_baru.csv")

# 2. BACA DATA
df_rating = pd.read_csv(ratingPath)
df_produk = pd.read_csv(produkPath)

# 3. INISIALISASI PETA & CLUSTER
m = folium.Map(location=[-6.9175, 107.6191], zoom_start=13, tiles="cartodbpositron")
marker_cluster = MarkerCluster().add_to(m)

# 4. FUNGSI RATING KE BINTANG (HTML Style)
def get_stars_html(rating):
    full = int(rating)
    stars = '<span style="color: #fbbc04; font-size: 16px;">' + ('★' * full) + '</span>'
    stars += '<span style="color: #ccc; font-size: 16px;">' + ('★' * (5 - full)) + '</span>'
    return stars

# 5. LOOP DATA OUTLET
for _, row in df_rating.iterrows():
    outlet_id = row["outlet_id"]
    nama_outlet = row["Outlet"]
    rating = float(row["rating_outlet"])
    lat, lon = float(row["lat"]), float(row["lon"])
    brand = str(row["e-commere"]).lower() # Pastikan kolom e_commerce sesuai nama di CSV

    # AMBIL 7 PRODUK TERUNIK
    produk_outlet = df_produk[df_produk["outlet_id"] == outlet_id]
    produk_list = produk_outlet["Produk_BestSeller"].drop_duplicates().head(7).tolist()

    produk_items = "".join([f"<li style='margin-bottom:2px;'>{p}</li>" for p in produk_list])
    if not produk_items: produk_items = "<li>Data tidak tersedia</li>"

    # WARNA BRAND
    color = "pink" if "sociolla" in brand else "black"

    # DESAIN POPUP GOOGLE MAPS STYLE
    popup_html = f"""
    <div style="width: 220px; font-family: 'Roboto', Arial, sans-serif;">
        <h4 style="margin:0; color:{'#e91e63' if color=='pink' else '#333'};">{nama_outlet}</h4>
        <div style="margin: 5px 0;">
            {get_stars_html(rating)} <b style="font-size:14px; vertical-align:middle;">{rating}</b>
        </div>
        <hr style="border:0; border-top:1px solid #eee; margin:10px 0;">
        <b style="font-size:11px; color:#555;">7 PRODUK BEST SELLER:</b>
        <ul style="font-size:11px; padding-left:18px; margin:5px 0; color:#444;">
            {produk_items}
        </ul>
    </div>
    """

    # TAMBAHKAN KE CLUSTER (Bukan langsung ke m)
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=nama_outlet,
        icon=folium.Icon(color=color, icon="shopping-cart", prefix="fa")
    ).add_to(marker_cluster)

# 6. SIMPAN
output_path = os.path.join(BASE_DIR, "Data", "Visualisasi", "peta_outlet_final.html")
m.save(output_path)
print(f"✅ Berhasil! Silakan cek file di: {output_path}")