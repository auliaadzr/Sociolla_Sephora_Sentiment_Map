import folium
import pandas as pd
import os
from folium.plugins import MarkerCluster

def main(user_lat=-6.9175, user_lon=107.6191, min_rating=4.0):
    """
    Membuat peta GIS outlet dengan rating tinggi.
    - user_lat, user_lon: lokasi user
    - min_rating: rating minimal filter
    """
    # =====================
    # KONFIGURASI PATH
    # =====================
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rating_path = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")
    export_path = os.path.join(BASE_DIR, "Data", "Visualisasi", "peta_outlet_final.html")

    if not os.path.exists(rating_path):
        raise FileNotFoundError("Data rating outlet belum tersedia. Jalankan proses Rating Outlet terlebih dahulu.")

    # =====================
    # LOAD DATA
    # =====================
    df = pd.read_csv(rating_path)
    df = df[df["rating_outlet"] >= min_rating].copy()  # filter rating

    # =====================
    # SETUP MAP
    # =====================
    m = folium.Map(
        location=[user_lat, user_lon],
        zoom_start=13,
        tiles="CartoDB positron"
    )

    marker_cluster = MarkerCluster().add_to(m)

    # =====================
    # TAMBAHKAN MARKER OUTLET
    # =====================
    for i, row in df.iterrows():
        lat = row["lat"]
        lon = row["lon"]

        # Offset kecil supaya marker tidak bertumpuk
        lat += (i % 5) * 0.0001
        lon += (i % 5) * 0.0001

        outlet = row["Outlet"]
        rating_val = round(row["rating_outlet"], 2)
        brand = str(row["e-commere"]).lower()
        color = "pink" if "sociolla" in brand else "black"

        # Bintang rating
        full_stars = int(rating_val)
        stars = "★" * full_stars + "☆" * (5 - full_stars)

        popup_html = f"""
        <div style="width: 220px; font-family: Arial;">
            <b>{outlet}</b><br>
            <b>Brand:</b> {brand.capitalize()}<br>
            <b>Rating:</b> {rating_val} <span style="color:#fbbc04">{stars}</span><br>
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            popup=popup_html,
            tooltip=outlet,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(marker_cluster)

    # =====================
    # TAMBAHKAN MARKER USER
    # =====================
    folium.Marker(
        location=[user_lat, user_lon],
        tooltip="📍 Lokasi Anda",
        popup="Ini lokasi Anda",
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)

    # =====================
    # SIMPAN MAP
    # =====================
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    m.save(export_path)
    print("✅ Peta GIS berhasil dibuat:", export_path)