import folium
import pandas as pd
import os

def main():
    # KONFIGURASI PATH
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ratingPath = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")
    produkPath = os.path.join(BASE_DIR, "Data", "Raw", "data_website.csv")

    # MEMBACA FILE
    df_rating = pd.read_csv(ratingPath)
    df_produk = pd.read_csv(produkPath)

    # TITIK TENGAH PETA (Bandung)
    center_lat = -6.9175
    center_lon = 107.6191
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    # TAMBAHKAN MARKER DARI DATA 
    for index, row in df_rating.iterrows():
        # Ambil data dasar
        outlet_id = row["outlet_id"]
        nama_outlet = row["Outlet"]
        rating_val = float(row["rating_outlet"])
        
        # Ambil Lat Lon dari file produk 
        detail = df_produk[df_produk["outlet_id"] == outlet_id]
        
        if not detail.empty:
            lat = float(detail.iloc[0]["lat"])
            lon = float(detail.iloc[0]["lon"])
            
            # LOGIKA AGAR 3 SEPHORA TIDAK BERTUMPUK (BULAT)
            lat_final = lat + (index * 0.0001)
            lon_final = lon + (index * 0.0001)

            # Penentuan Warna Brand
            brand_raw = str(row["e-commere"]).lower()
            color_marker = "pink" if "sociolla" in brand_raw else "black"

            # Membuat Bintang (Rating)
            full_stars = int(rating_val)
            stars_html = '<span style="color: #fbbc04;">' + ('★' * full_stars) + '</span>'
            stars_html += '<span style="color: #ccc;">' + ('★' * (5 - full_stars)) + '</span>'

            # Mengambil 7 Produk Best Seller
            list_p = detail["Produk_BestSeller"].drop_duplicates().head(7).tolist()
            produk_html = ""
            for i, p in enumerate(list_p, 1):
                produk_html += f"{i}. {p}<br>"

            # Desain Popup
            popup_content = f"""
            <div style="width: 200px; font-family: Arial;">
                <b>{nama_outlet}</b><br>
                Rating: {rating_val} {stars_html}<br><br>
                <b>7 Produk Best Seller:</b><br>
                {produk_html}
            </div>
            """
            
            # Tambahkan Marker ke Peta 
            folium.Marker(
                location=[lat_final, lon_final],
                popup=folium.Popup(popup_content, max_width=250),
                tooltip=nama_outlet,
                icon=folium.Icon(color=color_marker, icon="info-sign")
            ).add_to(m)

    # SIMPAN HASIL 
    exportPath = os.path.join(BASE_DIR, "Data", "Visualisasi", "peta_outlet_final.html")
    m.save(exportPath)

    print("Peta berhasil dibuat: " + exportPath)

# JIKA FILE DIJALANKAN LANGSUNG
if __name__ == "__main__":
    main()