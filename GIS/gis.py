# GIS/gis.py
import folium
import pandas as pd
import os
from folium.plugins import MarkerCluster

def generate_map(user_lat, user_lon, min_rating):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rating_path = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")
    export_path = os.path.join(BASE_DIR, "Data", "Visualisasi", "peta_outlet.html")

    if not os.path.exists(rating_path):
        raise FileNotFoundError("Data rating outlet belum tersedia.")

    df = pd.read_csv(rating_path)
    df = df[df["rating_outlet"] >= min_rating].copy()

    m = folium.Map(
        location=[user_lat, user_lon],
        zoom_start=13,
        tiles="CartoDB positron"
    )

    marker_cluster = MarkerCluster().add_to(m)

    for i, row in df.iterrows():
        lat = row["lat"] + (i % 5) * 0.0001
        lon = row["lon"] + (i % 5) * 0.0001

        outlet = row["Outlet"]
        rating_val = round(row["rating_outlet"], 2)
        brand = str(row["e-commere"]).lower()
        color = "pink" if "sociolla" in brand else "black"

        stars = "★" * int(rating_val) + "☆" * (5 - int(rating_val))

        popup_html = f"""
        <div style="width:220px">
            <b>{outlet}</b><br>
            Brand: {brand.capitalize()}<br>
            Rating: {rating_val} <span style="color:#fbbc04">{stars}</span>
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            popup=popup_html,
            tooltip=outlet,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(marker_cluster)

    folium.Marker(
        location=[user_lat, user_lon],
        tooltip="📍 Lokasi Anda",
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)

    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    m.save(export_path)

    return export_path
