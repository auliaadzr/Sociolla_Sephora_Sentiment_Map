import folium
import pandas as pd
import os
import math
from folium.plugins import MarkerCluster

def calculate_distance(lat1, lon1, lat2, lon2):
    """Menghitung jarak lurus (Haversine) secara manual"""
    R = 6371 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def generate_map(user_lat, user_lon, min_rating):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rating_path = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")
    website_path = os.path.join(BASE_DIR, "Data", "Raw", "data_website.csv")
    export_path = os.path.join(BASE_DIR, "Data", "Visualisasi", "peta_outlet.html")

    # Load data outlet & website
    df_outlet = pd.read_csv(rating_path)
    df_web = pd.read_csv(website_path)

    # Filter rating outlet
    df_outlet = df_outlet[df_outlet["rating_outlet"] >= min_rating].copy()

    m = folium.Map(location=[user_lat, user_lon], zoom_start=13, tiles="CartoDB positron")
    marker_cluster = MarkerCluster().add_to(m)

    for i, row in df_outlet.iterrows():
        lat, lon = row["lat"], row["lon"]
        dist = calculate_distance(user_lat, user_lon, lat, lon)
        
        outlet_name = row["Outlet"]
        rating_val = round(row["rating_outlet"], 2)
        brand = str(row["e-commere"]).lower().strip() # Menggunakan nama kolom sesuai file
        
        color = "pink" if "sociolla" in brand else "black"
        stars = "★" * int(rating_val) + "☆" * (5 - int(rating_val))

        # --- AMBIL 7 PRODUK SESUAI NAMA KOLOM DI CSV ANDA ---
        # Mencari produk berdasarkan kolom 'e-commere' dan 'Produk_BestSeller'
        brand_key = "sociolla" if "sociolla" in brand else "sephora"
        mask = df_web['e-commere'].str.lower().str.contains(brand_key, na=False)
        best_sellers = df_web[mask]['Produk_BestSeller'].head(7).tolist()
        
        product_list_html = "".join([f"<li>{p}</li>" for p in best_sellers])

        popup_html = f"""
        <div style="font-family: Arial; width:250px;">
            <center><b>{outlet_name}</b></center>
            <hr style="margin:5px 0;">
            <b>Brand:</b> {brand.capitalize()}<br>
            <b>Rating:</b> {rating_val} <span style="color:#fbbc04;">{stars}</span><br>
            <b>Jarak:</b> {dist:.2f} km<br><br>
            <b>7 Produk Best Seller:</b>
            <ol style="margin-top:5px; padding-left:20px; font-size:11px;">
                {product_list_html if best_sellers else "<li>Data tidak ditemukan</li>"}
            </ol>
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=outlet_name,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(marker_cluster)

    folium.Marker(location=[user_lat, user_lon], icon=folium.Icon(color="blue", icon="user")).add_to(m)
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    m.save(export_path)
    return export_path