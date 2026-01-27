import folium
import pandas as pd
import os
import math

# =====================================
# 1. KONFIGURASI PATH FILE
# =====================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ratingPath = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")
produkPath = os.path.join(BASE_DIR, "Data", "Clean", "data_cleaning.csv")

# =====================================
# 2. BACA DATA CSV
# =====================================
df_rating = pd.read_csv(ratingPath)
df_produk = pd.read_csv(produkPath)

# =====================================
# 3. TITIK TENGAH PETA
# =====================================
center_lat = -6.9175
center_lon = 107.6191
m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

# =====================================
# 4. FUNGSI RATING BINTANG ⭐
# =====================================
def rating_to_stars(rating):
    full_star = int(math.floor(rating))
    half_star = 1 if rating - full_star >= 0.5 else 0
    empty_star = 5 - full_star - half_star
    
    stars = "⭐" * full_star
    stars += "✨" if half_star else ""
    stars += "☆" * empty_star
    return stars

# =====================================
# 5. LOOP DATA OUTLET
# =====================================
for index, row in df_rating.iterrows():
    
    outlet_id = row['outlet_id']
    nama_outlet = row['Outlet']
    rating = float(row['rating_outlet'])
    lat = float(row['lat'])
    lon = float(row['lon'])
    brand = str(row['e-commere']).lower()
    
    # Ambil 7 produk best seller sesuai outlet
    data_produk_outlet = df_produk[df_produk['outlet_id'] == outlet_id]
    produk_list = data_produk_outlet['Produk_BestSeller'].tolist()
    
    produk_html = "<ol>"
    for p in produk_list[:7]:
        produk_html += f"<li>{p}</li>"
    if len(produk_list) == 0:
        produk_html += "<li>Data produk tidak tersedia</li>"
    produk_html += "</ol>"
    
    # =====================================
    # WARNA MARKER BERDASARKAN BRAND
    # =====================================
    if brand == "sociolla":
        marker_color = "#ff4da6"  # pink
    elif brand == "sephora":
        marker_color = "black"   # hitam
    else:
        marker_color = "blue"    # default
    
    # =====================================
    # UKURAN MARKER BERDASARKAN RATING
    # =====================================
    radius_marker = rating * 3
    
    # =====================================
    # POPUP
    # =====================================
    popup_html = f"""
    <b>{nama_outlet}</b><br>
    Brand: {brand.capitalize()}<br>
    Rating: {rating}<br>
    {rating_to_stars(rating)}<br><br>
    <b>7 Produk Best Seller:</b>
    {produk_html}
    """
    
    # =====================================
    # MARKER LOKASI (CIRCLEMARKER)
    # =====================================
    folium.CircleMarker(
        location=[lat, lon],
        radius=radius_marker,
        popup=popup_html,
        tooltip=nama_outlet,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.7
    ).add_to(m)

# =====================================
# 6. SIMPAN PETA
# =====================================
exportPath = os.path.join(BASE_DIR, "Data", "Visualisasi", "peta_outlet.html")
m.save(exportPath)

print("✅ Peta GIS berhasil dibuat!")
print(f"📍 File: {exportPath}")
